
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

class Vocable(object):
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            
            }
    
    def interpreter(self, command, args):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module vocable")
    
    
