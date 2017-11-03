
from QCustomizedWidgets.QMapView import QMapView
#from QCustomizedWidgets.QMapWidget import QMapWidget
 
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

from configs.configFiles import ConfigFile
from modules.gps.dbAdapter import DbAdapter
from modules.gps.importGpx import GpxParser

import os, _thread, time, math
from datetime import datetime
from geopy.distance import vincenty

class Gps(object):
    
    logpath = None
    
    terminate_log_thread = False
    log_thread_running = False
    
    import_thread_running = False
    
    def __init__(self):
        config = ConfigFile(None, None)
        self.logpath = config.readPath("positioning", "storagepath")
        if not os.path.exists(self.logpath):
            os.makedirs(self.logpath)
    
    def getCommands(self):
        return {
            "gps.commands" : self.commands,
            
            "gps.position" : self.position,
            "gps.start_log" : self.start_log,
            "gps.stop_log" : self.stop_log,
            "gps.logs" : self.logs,
            "gps.plot" : self.plot,
            "gps.height_diagram" : self.height_diagram,
            "gps.stats" : self.stats,
            
            "gps.import_gpx" : self.import_gpx,
            "gps.export_gpx" : self.export_gpx,
            
            "gps.map" : self.showMap,
            "gps.heightmap" : self.showHeightmap,
        }
    
    def interpreter(self, command, args, queue):
        commands = self.getCommands()
        try:
            return commands.get(command, self.commandNotFound)(command, args, queue)
        except TypeError:
            return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module vocable")
    
    def commands(self, none1, none2):
        dic = self.getCommands()
        
        commands = sorted(dic.items())
        
        all_commands = []
        for key in commands:
            line = str(key).split(",")[0]
            all_commands.append(str(line[2:-1]))
            
        result_object = Result()
        result_object.category = "list"
        result_object.payload = all_commands
        return result_object
    
    def import_gpx(self, c, args):
        filename = args[0]
        print(filename)
        
        _thread.start_new_thread(self.__importThread, (filename,))
    
    def __importThread(self, filename):
        self.import_thread_running = True
        
        log_db_name = str(time.time()).split('.')[0]+".sqlite"
        dbpath = os.path.join(self.logpath, log_db_name)
        
        parser = GpxParser(dbpath)
        parser.parse(filename)
        
        self.import_thread_running = False
    
    def export_gpx(self, c, args):
        pass
    
    def start_log(self, c, a):
        log_db_name = str(time.time()).split('.')[0]+".sqlite"
        result_object = Result()
        
        if not self.log_thread_running:
            self.terminate_log_thread = False
            self.logging_thread = _thread.start_new_thread(self.__loggingThread, (log_db_name,))
            result_object.payload = "gps logging started"
        else:
            result_object.payload = "gps logging already running"
        
        result_object.category = "text"
        return result_object
    
    def __loggingThread(self, log_db_name):
        self.log_thread_running = True
        delay = 1
        while not self.terminate_log_thread:
            self.__logging(log_db_name)
            time.sleep(delay)
    
    def __logging(self, log_db_name):
        result_object = Result()
        
        dbpath = os.path.join(self.logpath, log_db_name)
        dbAdapter = DbAdapter(dbpath)
        
        try:
            position = self.getPosition()
        except NoFixError:
            result_object.category = "text"
            result_object.payload = "no gps fix available"
        else:
            if position:
                dbAdapter.insertLogEntryWithTimestamp(position)
                result_object.payload = 'position logging started'
            else:
                result_object.payload = 'no working position provider found'
            
            result_object.category = "text"
            
        return result_object
    
    def stop_log(self, c, a):
        self.terminate_log_thread = True
        self.log_thread_running = False
        
        result_object = Result()
        result_object.category = "text"
        result_object.payload = "gps logging stopped"
        return result_object
    
    def logs(self, c, a):
        base, dirs, files = next(iter(os.walk(self.logpath)))
        
        result_object = Result()
        result_object.category = "list"
        result_object.payload = sorted(files)
        return result_object
    
    def position(self, c, a):
        result_object = Result()
        
        try:
            data = self.getPosition()
        except NoFixError:
            result_object.category = "text"
            result_object.payload = "no gps fix available"
        else:
            if data:
                result_object.category = "table"
                result_object.payload = [
                    ['Latitude', data['latitude']],
                    ['Longitude', data['longitude']],
                    ['Altitude', data['altitude']],
                    
                    ['Speed', data['speed']],
                    ['Track', data['track']],
                    ['Climb', data['climb']],
                    
                    ['Time', data['time']],
                    
                    ['Error Horizontal', data['error_horizontal']],
                    ['Error Vertical', data['error_vertical']],
                ]
            else:
                result_object.category = "text"
                result_object.payload = 'could not find any working position provider (like gpsd or geoclue)'
        return result_object
    
    def getPosition(self):
        module_found = False
        """ maybe we are on linux with a gps device,
        so we try to use gpsd """
        try:
            import gpsd
        except ModuleNotFoundError:
            pass
        else:
            try:
                gpsd.connect()
            except ConnectionRefusedError:
                pass
            else:
                module_found = True
                return self.getPositionFromGpsd()
        
        if not module_found:
            """ we could implement accessing geoclue here """
            pass
    
    def getPositionFromGpsd(self):
        import gpsd
        gpsd.connect()
        try:
            packet = gpsd.get_current()
        except KeyError as e:
            return
        
        try:
            pos = packet.position()
        except gpsd.NoFixError:
            raise NoFixError
        else:
            precision = packet.position_precision()
            time = packet.get_time()
            try:
                alt = packet.altitude()
                movement = packet.movement()
            except gpsd.NoFixError:
                alt, speed, track, climb = ['n/a'] * 4
            else:
                speed, track, climb = movement['speed'], movement['track'], movement['climb']
            
            return {
                'latitude' : pos[0],
                'longitude' : pos[1],
                'altitude' : alt,
                
                'speed' : speed,
                'track' : track,
                'climb' : climb,
                
                'time' : time,
                
                'error_horizontal' : precision[0],
                'error_vertical' : precision[1],
            }
    
    def __determineFilename(self, args):
        try:
            filename = args[0]
        except IndexError:
            return None
        
        #if not filename.endswith('.sqlite'):
        #    filename = filename + '.sqlite'
        files = self.logs(None, None).payload
        if filename in files:
            return filename
        elif filename.endswith('*'):
            filename = filename[:-1]
            matches = []
            for _f in files:
                if _f.startswith(filename):
                    matches.append(_f)
            if len(matches) == 1:
                return matches[0]
    
    def plot(self, c, args):
        result_object = Result()
        filename = self.__determineFilename(args)
        if not filename:
            result_object.error = 'a file matching to the specified one could not be found'
            return result_object
        
        filepath = os.path.join(self.logpath, filename)
        
        dbAdapter = DbAdapter(filepath)
        boundings = dbAdapter.selectMinMaxCoordinate()
        mapView = QMapView(boundings)
        
        data = dbAdapter.selectLatLon()
        points_list = []
        for pos in data:
            #mapView.addPoint(pos['longitude'], pos['latitude'])
            x, y = pos['latitude'], pos['longitude']
            points_list.append([x, y])
        mapView.addPointList(points_list)
        mapView.drawPointList()
        
        #mapView.scaleViewToContents()
        
        result_object.category = "qt_widget"
        result_object.payload = mapView
        return result_object
    
    def showMap(self, c, args, queue):
        """
        import time
        for i in range(10):
            queue.put(str(i))
            print("putted:", i)
            time.sleep(1)
        """
        result_object = Result()
        result_object.category = "command"
        result_object.payload = {
            "command": "qmapview",
            "args": args,
            }
        return result_object
    
    def showHeightmap(self, c, args):
        
        lat_min = float(args[0])
        lat_max = float(args[1])
        lon_min = float(args[2])
        lon_max = float(args[3])
        
        delta_lat = vincenty([lat_min, lon_min], [lat_max, lon_min]).kilometers
        delta_lon = vincenty([lat_min, lon_min], [lat_min, lon_max]).kilometers
        
        print(delta_lat, delta_lon)
        
        import srtm
        geo_elevation_data = srtm.get_data()
        width = 1000
        height = (delta_lon * width) / delta_lat
        print(width, height)
        #image = geo_elevation_data.get_image((1000, 1000), (50, 51), (8, 9), 800)
        image = geo_elevation_data.get_image((round(width), round(height)), (lat_min, lat_max), (lon_min, lon_max), int(args[4]))
        
        result_object = Result()
        result_object.category = "image"
        result_object.payload = image
        return result_object
    
    def height_diagram(self, c, args):
        result_object = Result()
        
        filename = self.__determineFilename(args)
        if not filename:
            result_object.error = 'a file matching to the specified one could not be found'
            return result_object
        
        filepath = os.path.join(self.logpath, filename)
        dbAdapter = DbAdapter(filepath)
        data = dbAdapter.selectDiagramData()
        
        result_object.category = "diagram"
        result_object.payload = data
        result_object.name = filename
        return result_object
    
    def stats(self, c, args):
        result_object = Result()
        filename = self.__determineFilename(args)
        if not filename:
            result_object.error = 'a file matching to the specified one could not be found'
            return result_object
        
        filepath = os.path.join(self.logpath, filename)
        
        result_table = []
        
        dbAdapter = DbAdapter(filepath)
        
        distance = 0
        data = dbAdapter.selectLogData()
        last_pos = None
        for pos in data:
            if last_pos:
                vincenty_dist = vincenty(
                    [
                        last_pos['latitude'],
                        last_pos['longitude'],
                    ],
                    [
                        pos['latitude'],
                        pos['longitude'],
                    ]
                ).kilometers
                distance += vincenty_dist
            
            last_pos = pos
        
        result_table.append(['distance (path) [km]', round(distance, 2)])
        
        start_stop = dbAdapter.selectStartStopCoordinates()
        distance_air = vincenty([
                                    start_stop['start_lat'],
                                    start_stop['start_lon']
                                ],
                                [
                                    start_stop['stop_lat'],
                                    start_stop['stop_lon']
                                ]
                                ).kilometers
        result_table.append(['distance (air) [km]', round(distance_air, 2)])
        
        t_stats = dbAdapter.selectTimeStats()
        
        try:
            time_min = datetime.fromtimestamp(t_stats['time_min']).strftime("%d.%m.%Y %R")
            time_max = datetime.fromtimestamp(t_stats['time_max']).strftime("%d.%m.%Y %R")
        except TypeError:
            result_table.append(['time_start', 'n/a'])
            result_table.append(['time_end', 'n/a'])
        else:
            result_table.append(['time_start', time_min])
            result_table.append(['time_end', time_max])
        
        try:
            speed = round(distance / ((t_stats['time_max'] - t_stats['time_min'])/60/60), 2)
        except TypeError:
            result_table.append(['speed [km/h]', 'n/a'])
        else:
            result_table.append(['speed [km/h]', speed])
        
        boundings = dbAdapter.selectMinMaxCoordinate()
        result_table.append(['lat_min', boundings['lat_min']])
        result_table.append(['lat_max', boundings['lat_max']])
        result_table.append(['lon_min', boundings['lon_min']])
        result_table.append(['lon_max', boundings['lon_max']])
        
        altitude_min_max = dbAdapter.selectMinMaxAltitude()
        result_table.append(['alt_min', altitude_min_max['alt_min']])
        result_table.append(['alt_max', altitude_min_max['alt_max']])
        
        speed = dbAdapter.selectSpeedStats()
        result_table.append(['speed_min', speed['speed_min']])
        result_table.append(['speed_max', speed['speed_max']])
        result_table.append(['speed_average', speed['speed_average']])
        
        count = dbAdapter.selectCount()
        result_table.append(['samples count', count['count']])
        
        result_object.category = "table"
        result_object.payload = result_table
        return result_object

class NoFixError(Exception):
    pass
