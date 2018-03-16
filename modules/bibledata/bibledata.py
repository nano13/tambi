# -*- coding: utf_8 -*-

from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

#import sqlite3



class Bibledata(object):
    def __init__(self):
        pass
    
    #def initDbConnection(self):
        #self.connection = sqlite3.connect("./modules/quran/quran.db")
        #self.cursor = self.connection.cursor()
         
    def getCommands(self):
        return {
            "bibledata.commands" : self.commands,
            
            "bibledata.guys" : self.guys,
        }
    
    def interpreter(self, command, args, queue):
        print("args:", args)
        
        commands = self.getCommands()
        
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module bibledata")
    
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
    
    def guys(self, c, a):
        import json
        
        fobj = open("./modules/bibledata/data/kings_south.json")
        loaded = json.load(fobj)
        
        result_object = Result()
        result_object.category = "bloodline"
        result_object.payload = loaded
        return result_object
