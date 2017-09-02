 
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
        dbname = "eduard.sqlite"
        dbpath = os.path.join(self.deckpath, dbname)
        dbAdapter = DbAdapter(dbpath)
        
        position = self.getPosition()
        if position:
            dbAdapter.insertLogEntry(position)
            payload = 'position loggin started'
        else:
            payload = 'no working position provider found'
        
        result_object = Result()
        result_object.category = "text"
        result_object.payload = payload
        return result_object
        
    def stop_log(self, c, a):
        pass
    
    def position(self, c, a):
        result_object = Result()
        
        data = self.getPosition()
        
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
                return self.getPositionFromGpsd()
    
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
            pass
        else:
            precision = packet.position_precision()
            time = packet.get_time()
            try:
                alt = packet.altitude()
                movement = packet.movement()
            except gpsd.NoFixError:
                alt = 'N.A.'
                speed, track, climb = 'N.A.', 'N.A.', 'N.A.'
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
    
