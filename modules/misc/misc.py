
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

from modules.amazinggrace.QAmazingGraceWidget import QAmazingGraceWidget

class Misc(object):
    
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "misc.commands": self.commands,
            }
    
    def interpreter(self, command, args, queue):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        print("not found in AmazingGrace")
        raise CommandNotInThisModule("command not found in module amazinggrace")
    
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
    
