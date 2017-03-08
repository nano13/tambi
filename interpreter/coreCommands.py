# -*- coding: utf_8 -*-

from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result
#from interpreter.loadModules import LoadModules

import sys, time

class CoreCommands(object):
    
    #modules_man_list = loadModules().loadModulesManPages()
    
    def __init__(self):
        pass
    
    def execute(self, command, args):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def getCommands(self):
        return {
            "commands": self.commands,
            
            "man": self.man,
            
            "clear" : self.clear,
            "exit" : self.exit,
            
            "date" : self.date,
            "time" : self.time,
            
            
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
    
    def man(self, c, args):
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
        exec(import_query, globals())
        exec_result = "result"
        exec(exec_result + " = man."+command_name, globals())
        
        result_object = Result()
        result_object.category = 'text'
        result_object.payload = args[0] +"\n"+result
        return result_object
    
    def clear(self, command, args):
        pass
    
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
