 
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

class Gps(object):
    
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "gps.commands" : self.commands,
            
            "gps.position" : self.position,
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
    
    def position(self, c, a):
        result_object = Result()
        result_object.payload = ""
        try:
            import gpsd
        except ModuleNotFoundError:
            from QCustomizedWidgets.QLocationManager import QLocationManager
            location = QLocationManager()
            pos = location.getGpsPosition()
            
            result_object.category = "text"
            result_object.payload = "using qt-backend"
        else:
            try:
                gpsd.connect()
            except ConnectionRefusedError:
                result_object.category = "text"
                result_object.payload = "could not connect to gpsd"
            else:
                packet = gpsd.get_current()
                
                try:
                    pos = packet.position()
                except gpsd.NoFixError:
                    result_object.category = 'text'
                    result_object.payload = "gpsd: No Fix"
                else:
                    result_object.category = 'table'
                    
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
                    
                    result_object.payload = [
                        ['Latitude', pos[0]],
                        ['Longitude', pos[1]],
                        ['Altitude', alt],
                        
                        ['Speed', speed],
                        ['Track', track],
                        ['Climb', climb],
                        
                        ['Time', time],
                        
                        ['Error Horizontal', precision[0]],
                        ['Error Vertical', precision[1]],
                    ]
        
        return result_object
