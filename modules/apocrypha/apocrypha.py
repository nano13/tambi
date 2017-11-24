# -*- coding: utf_8 -*-

from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

import sqlite3

class Apocrypha(object):
    def __init__(self):
        pass
    
    def initDbConnection(self):
        self.connection = sqlite3.connect("./modules/apocrypha/henoch.sqlite.db")
        self.cursor = self.connection.cursor()
         
    def getCommands(self):
        return {
            "apocrypha.commands" : self.commands,
            
            "apocrypha.word" : self.word,
            "apocrypha.structure" : self.structure,
            
        }
    
    def interpreter(self, command, args, queue):
        print("args:", args)
        
        commands = self.getCommands()
        
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module quran")
    
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
    
    def word(self, c, args):
        result_object = Result()
        result_object.category = "text"
        
        if len(args) > 0 and args[0] == 'henoch':
            result = self.henoch(args, result_object)
        
        return result_object
    
    def henoch(self, args, result_object):
        self.initDbConnection()
        
        if len(args) == 2:
            query = "SELECT verse, word FROM henoch WHERE chapter=?"
            print(int(args[1]))
            self.cursor.execute(query, [int(args[1])])
        
        elif len(args) == 3:
            if args[1].find('-') == -1:
                query = "SELECT verse, word FROM henoch WHERE chapter=? AND verse=?"
                self.cursor.execute(query, [int(args[1]), int(args[2])])
        
            elif len(args) == 4:
                query = "SELECT verse, word FROM henoch WHERE chapter=? AND verse>=? AND verse<=?"
                self.cursor.execute(query, [int(args[1]), int(args[2]), int(args[3])])
        
        result = self.cursor.fetchall()
        
        result_object.payload = result
        return result_object
    
    def structure(self, c, args):
        self.initDbConnection()
        
        query = "SELECT chapter, COUNT(verse) FROM henoch GROUP BY chapter ORDER BY chapter"
        self.cursor.execute(query)
        
        result = self.cursor.fetchall()
        
        result_object = Result()
        result_object.category = 'table'
        result_object.payload = result
        result_object.header = ['chapter', 'verses']
        return result_object

