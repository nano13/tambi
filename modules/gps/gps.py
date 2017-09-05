 
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

from configs.configFiles import ConfigFile
from modules.gps.dbAdapter import DbAdapter

import os, _thread, time, math

class Gps(object):
    
    logpath = None
    
    terminate_thread = False
    thread_running = False
    
    def __init__(self):
        config = ConfigFile()
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
        }
    
    def interpreter(self, command, args):
        commands = self.getCommands()
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
    
    def start_log(self, c, a):
        log_db_name = str(time.time()).split('.')[0]+".sqlite"
        result_object = Result()
        
        if not self.thread_running:
            self.terminate_thread = False
            self.logging_thread = _thread.start_new_thread(self.__loggingThread, (log_db_name,))
            result_object.payload = "gps logging started"
        else:
            result_object.payload = "gps logging already running"
        
        result_object.category = "text"
        return result_object
    
    def __loggingThread(self, log_db_name):
        self.thread_running = True
        delay = 1
        while not self.terminate_thread:
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
                dbAdapter.insertLogEntry(position)
                result_object.payload = 'position logging started'
            else:
                result_object.payload = 'no working position provider found'
            
            result_object.category = "text"
            
        return result_object
    
    def stop_log(self, c, a):
        self.terminate_thread = True
        self.thread_running = False
        
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
        #try:
            #import gpsd
        #except ModuleNotFoundError:
            #from QCustomizedWidgets.QLocationManager import QLocationManager
            #location = QLocationManager()
            #pos = location.getGpsPosition()
        #else:
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
    
    def plot(self, c, args):
        result_object = Result()
        try:
            filename = args[0]
        except IndexError:
            result_object.error = 'please specify the filename of the gps recording you want to plot'
            return result_object
        
        #if not filename.endswith('.sqlite'):
        #    filename = filename + '.sqlite'
        files = self.logs(None, None).payload
        if filename in files:
            return self.plotHelper(result_object, filename)
        elif filename.endswith('*'):
            filename = filename[:-1]
            matches = []
            for _f in files:
                if _f.startswith(filename):
                    matches.append(_f)
            if len(matches) == 1:
                return self.plotHelper(result_object, matches[0])
    
    def plotHelper(self, result_object, filename):
        filepath = os.path.join(self.logpath, filename)
        
        from modules.gps.QMapView import QMapView
        
        dbAdapter = DbAdapter(filepath)
        boundings = dbAdapter.selectMinMaxLogCoordinate()
        mapView = QMapView(boundings)
        
        data = dbAdapter.selectLogData()
        for pos in data:
            mapView.addPoint(pos['longitude'], pos['latitude'])
            pass
        #mapView.scaleViewToContents()
        
        result_object.category = "qt_widget"
        result_object.payload = mapView
        return result_object
    

class NoFixError(Exception):
    pass
