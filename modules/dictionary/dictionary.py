 
# -*- coding: utf_8 -*-

from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

import sqlite3

class Dictionary(object):
    def __init__(self):
        pass
    
    def initDbConnection(self):
        self.connection = sqlite3.connect("./modules/vocable/vocables.db")
        self.cursor = self.connection.cursor()
    
    def getCommands(self):
        return {
            "dictionary.commands" : self.commands,
            
            "dictionary.hebrew" : self.hebrew,
            "dictionary.greek" : self.greek,
            "dictionary.aramaic" : self.aramaic,
            "dictionary.akkadian" : self.akkadian,
        }
    
    def interpreter(self, command, args):
        print("args:", args)
        
        commands = self.getCommands()
        
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module quran")
    
    def commands(self, c, a):
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
    
    def hebrew(self, c, args):
        return self.dictionaryHelper(args, 'hebrew')
    def greek(self, c, args):
        return self.dictionaryHelper(args, 'greek')
    def aramaic(self, c, args):
        return self.dictionaryHelper(args, 'aramaic')
    def akkadian(self, c, args):
        return self.dictionaryHelper(args, 'akkadian')
    
    def dictionaryHelper(self, args, language):
        result_object = Result()
        
        query = """
        SELECT display, gloss
        FROM {0}
        WHERE display LIKE ? OR gloss LIKE ?
        """.format(language)
        try:
            param = '%'+str(args[0])+'%'
        except IndexError:
            result_object.error = 'invalid parameter'
        else:
            self.initDbConnection()
            self.cursor.execute(query, [param, param])
            result_object.payload = self.cursor.fetchall()
            
        result_object.category = "itemized"
        result_object.name = "dictionary result"
        return result_object
    
