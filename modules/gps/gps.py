 
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

from configs.configFiles import ConfigFile
from modules.gps.dbAdapter import DbAdapter

import os

class Gps(object):
    
    deckpath = None
    
    def __init__(self):
        config = ConfigFile()
        self.deckpath = config.readPath("positioning", "storagepath")
        if not os.path.exists(self.deckpath):
            os.makedirs(self.deckpath)
    
    def getCommands(self):
        return {
            "gps.commands" : self.commands,
            
            "gps.position" : self.position,
            "gps.start_log" : self.start_log,
            "gps.stop_log" : self.stop_log,
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
        result_object = Result()
        
        dbname = "eduard.sqlite"
        dbpath = os.path.join(self.deckpath, dbname)
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
        pass
    
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
        packet = gpsd.get_current()
        
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
    
class NoFixError(Exception):
    pass
