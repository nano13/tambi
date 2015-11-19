# -*- coding: utf_8 -*-

from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

import sys, time

class CoreCommands(object):
    def __init__(self):
        pass
    
    def execute(self, command, args):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def getCommands(self):
        return {
            "clear" : self.clear,
            "exit" : self.exit,
            
            "date" : self.date,
            "time" : self.time,
            
            
            }
    
    def commandNotFound(self, command, args):
        raise CommandNotInThisModule("command not found as a built-in one")
    
    def clear(self, command, args):
        pass
    
    def exit(self, command, args):
        #sys.exit()
        pass
    
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