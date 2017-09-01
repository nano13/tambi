# -*- coding: utf_8 -*-

from interpreter.exceptions import CommandNotInThisModule, ClearCalled
from interpreter.structs import Result
import interpreter.man as builtin_man_pages

from configs.history import History
from misc.unicodeFonts import UnicodeFonts

import sys, time, os

class CoreCommands(object):
    
    def __init__(self):
        pass
    
    def execute(self, command, args):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def getCommands(self):
        return {
            "commands": self.commands,
            "modules": self.modules,
            
            "man": self.man,
            
            "clear" : self.clear,
            "exit" : self.exit,
            
            "date" : self.date,
            "time" : self.time,
            
            "history" : self.history,
            
            "fonts" : self.fonts,
            
            "position" : self.position,
            }
    
    def commandNotFound(self, command, args):
        raise CommandNotInThisModule("command not found as a built-in one")
    
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
    
    def modules(self, c, a):
        base, dirs, files = next(iter(os.walk('./modules')))
        dirs.sort()
        dirs.remove('__pycache__')
        
        result_object = Result()
        result_object.category = "list"
        result_object.payload = dirs
        return result_object
    
    def man(self, c, args):
        result_object = Result()
        
        try:
            args[0]
        except IndexError:
            result_object.payload = builtin_man_pages.module_description
        else:
            if args[0].find('.') == -1:
                module_name = args[0]
                command_name = 'module_description'
            else:
                splitted = args[0].split('.')
                command_name = ""
                for i, fragment in enumerate(splitted):
                    if i <= 0:
                        module_name = fragment
                    elif i > 0:
                        command_name += fragment + '_'
                command_name = command_name[:-1]
            
            import_query = "import modules."+module_name+".man as man"
            try:
                exec(import_query, globals())
            except ModuleNotFoundError:
                
                exec_result = "result"
                try:
                    exec(exec_result + " = builtin_man_pages."+args[0], globals())
                except AttributeError:
                    result_object.error = 'no man-page for this command or module found'
                else:
                    result_object.payload = args[0] +"\n"+result
            else:
                exec_result = "result"
                try:
                    exec(exec_result + " = man."+command_name, globals())
                except AttributeError:
                    result_object.error = 'no man page for this command'
                else:
                    result_object.payload = args[0] +"\n"+result
        
        result_object.category = 'text'
        return result_object
    
    def clear(self, command, args):
        raise ClearCalled("clear the display widget!")
    
    def exit(self, command, args):
        sys.exit()
    
    def time(self, command, args):
        result = Result()
        result.category = "string"
        result.payload = time.strftime("%H:%M")
        return result
    
    def date(self, command, args):
        result = Result()
        result.category = "string"
        result.payload = time.strftime("%d.%m.%Y %A %B")
        return result
    
    def history(self, c, args):
        history = History()
        if len(args) < 1:
            result = history.historyReadAll()
        else:
            result = history.historyReadAllWithFilter(args[0])
        
        result_object = Result()
        result_object.payload = result[::-1]
        result_object.category = "list"
        return result_object
    
    def fonts(self, c, args):
        filter_str = None
        if len(args) > 0:
            filter_str = str(args[0])
        
        fonts = UnicodeFonts()
        available_fonts = fonts.printFonts(filter_str)
        
        result_object = Result()
        result_object.category = 'list'
        result_object.payload = available_fonts
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
            
            result_object.payload = "using qt-backend"
        else:
            gpsd.connect()
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
                
                #result_object.payload = "Latitude: "+str(pos[0])+" | Longitude: "+str(pos[1])+" | Altitude: "+str(alt)+" | Time: "+str(time)
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
