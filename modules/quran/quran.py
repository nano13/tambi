# -*- coding: utf_8 -*-

from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

import sqlite3

class Quran(object):
    def __init__(self):
        self.connection = sqlite3.connect("./modules/quran/quran.db")
        self.cursor = self.connection.cursor()
         
    def getCommands(self):
        return {
            "quran.commands" : self.commands,
            
            "quran.search" : self.search,
            
            "quran.word" : self.word,
        }
    
    def interpreter(self, command, args):
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
    
    def search(self, c, args):
        key = '%'+args[0]+'%'
        query = """SELECT surah, ayah, arabic, transcription, de_DE
        FROM quran
        WHERE arabic LIKE ? OR transcription LIKE ? OR de_DE LIKE ?"""
        self.cursor.execute(query, [key, key, key])
        
        result = self.cursor.fetchall()
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = result
        result_object.header = ['surah', 'ayah', 'arabic', 'transcription', 'de_DE']
        result_object.name = "quran_search"
        return result_object
    
    def word(self, c, args):
        
        if len(args) == 1:
            print("LEN 1", args[0])
            query = "SELECT surah, ayah, arabic, transcription, de_DE FROM quran WHERE surah=?"
            self.cursor.execute(query, [int(args[0])])
        elif len(args) == 2:
            if args[1].find('-') == -1:
                query = "SELECT surah, ayah, arabic, transcription, de_DE FROM quran WHERE surah=? AND ayah=?"
                self.cursor.execute(query, [int(args[0]), int(args[1])])
            else:
                ayah_min, ayah_max = args[1].split('-')
                query = "SELECT surah, ayah, arabic, transcription, de_DE FROM quran WHERE surah=? AND ayah>=? AND ayah<=?"
                self.cursor.execute(query, [int(args[0]), int(ayah_min), int(ayah_max)])
        
        result = self.cursor.fetchall()
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = result
        result_object.header = ['surah', 'ayah', 'arabic', 'transcription', 'de_DE']
        result_object.name = "quran"
        return result_object
    
