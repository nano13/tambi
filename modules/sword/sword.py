
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

#from modules.bituza.bituza import Bituza

import Sword
from Sword import *

class Sword(object):
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "sword": self.readBible,
            }
    
    def interpreter(self, command, args):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        print("not found in SWORD")
        raise CommandNotInThisModule("command not found in module sword")
    
    
    def readBible(self, command, args):
        print("reading bible")
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = ["a", "b", "c"]
        return result_object