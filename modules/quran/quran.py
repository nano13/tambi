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
            "quran.word.ar" : self.wordAR,
            "quran.word.de" : self.wordDE,
            
            "quran.order" : self.order,
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
        result_object.category = "itemized"#"table"
        result_object.payload = result
        result_object.header = ['surah', 'ayah', 'arabic', 'transcription', 'de_DE']
        result_object.name = "quran_search"
        return result_object
    
    def word(self, c, args):
        columns = ["surah", "ayah", "arabic", "transcription", "de_DE"]
        return self.wordHelper(args, columns)
    
    def wordAR(self, c, args):
        columns = ["surah", "ayah", "arabic"]
        result = self.wordHelper(args, columns)
        result.category = "text"
        return result
    
    def wordDE(self, c, args):
        columns = ["surah", "ayah", "de_DE"]
        result = self.wordHelper(args, columns)
        result.category = "text"
        return result
    
    def wordHelper(self, args, header):
        columns = ", ".join(header)
        if len(args) == 1:
            #print("LEN 1", args[0])
            query = "SELECT {0} FROM quran WHERE surah=?".format(columns)
            self.cursor.execute(query, [int(args[0])])
        elif len(args) == 2:
            if args[1].find('-') == -1:
                query = "SELECT {0} FROM quran WHERE surah=? AND ayah=?".format(columns)
                self.cursor.execute(query, [int(args[0]), int(args[1])])
            else:
                ayah_min, ayah_max = args[1].split('-')
                query = "SELECT {0} FROM quran WHERE surah=? AND ayah>=? AND ayah<=?".format(columns)
                self.cursor.execute(query, [int(args[0]), int(ayah_min), int(ayah_max)])
        
        result = self.cursor.fetchall()
        
        result_object = Result()
        result_object.category = "itemized"#"table"
        result_object.payload = result
        result_object.header = header#['surah', 'ayah', 'arabic', 'transcription', 'de_DE']
        result_object.name = "quran_word"
        return result_object
    
    def order(self, c, args):
        order = [96, 68, 73, 74, 1, 111, 81, 87, 92, 89, 93, 94, 103, 100, 108, 102, 107, 109, 105, 113, 114, 112, 53, 80, 97, 91, 85, 95, 106, 101, 75, 104, 77, 50, 90, 86, 54, 38, 7, 72, 36, 25, 35, 19, 20, 56, 26, 27, 28, 17, 10, 11, 12, 15, 6, 37, 31, 34, 39, 40, 41, 42, 43, 44, 45, 46, 51, 88, 18, 16, 71, 14, 21, 23, 32, 52, 67, 69, 70, 78, 79, 82, 84, 30, 29, 83, 2, 8, 3, 33, 60, 4, 99, 57, 47, 13, 55, 76, 65, 98, 59, 24, 22, 63, 58, 49, 66, 64, 61, 62, 48, 5, 9, 110]
        result = []
        for item in order:
            result.append(str(item))
        
        if args:
            try:
                index = result.index(str(args[0]))
            except ValueError:
                pass
            else:
                if index == 0:
                    result = result[:2]
                elif index == 113:
                    result = result[-2:]
                else:
                    result = result[index-1:index+2]
            
        
        result_object = Result()
        result_object.category = "list"
        result_object.payload = result
        result_object.header = ""
        result_object.name = "quran_order"
        return result_object
