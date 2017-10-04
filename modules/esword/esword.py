
 
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

import os, sqlite3, re

MODULE_PATH = os.path.join(os.getcwd(), 'modules', 'esword', 'assets')

class Esword(object):
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "esword.commands" : self.commands,
            
            "esword.word" : self.word,
            "esword.interlinear" : self.word,
        }
    
    def interpreter(self, command, args, queue):
        print("args:", args)
        
        commands = self.getCommands()
        
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module 'survival'")
    
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
    
    def word(self, command, args):
        connection = sqlite3.connect(os.path.join(MODULE_PATH, 'TRi.bbl.mybible'))
        cursor = connection.cursor()
        
        try:
            book_id = self.booksDict(args[0])
        except:
            result_object = Result()
            result_object.error = 'ERROR: You have to specify a book! See command "bituza.books" for a list of the possible book names!'
            return result_object
        else:
            if len(args) == 1:
                result_object = Result()
                result_object.error = 'ERROR: You have to specify at least a chapter!'
                return result_object
            elif len(args) == 2:
                query = "SELECT Chapter, Verse, Scripture FROM Bible WHERE Book=? AND Chapter=?"
                cursor.execute(query, [book_id, args[1]])
            elif len(args) == 3:
                if args[2].find('-') == -1:
                    query = "SELECT Chapter, Verse, Scripture FROM Bible WHERE Book=? AND Chapter=? AND Verse=?"
                    cursor.execute(query, [book_id, args[1], args[2]])
                else:
                    verse_min, verse_max = args[2].split('-')
                    query = "SELECT Chapter, Verse, Scripture FROM Bible WHERE Book=? AND Chapter=? AND Verse>=? AND Verse<=?"
                    cursor.execute(query, [book_id, args[1], verse_min, verse_max])
            
            result = cursor.fetchall()
            
            if command == 'esword.word':
                payload = []
                for i, verse in enumerate(result):
                    payload.append([verse[0], verse[1], self.parseText(verse[2])])
                category = 'text'
            elif command == 'esword.interlinear':
                payload = []
                for i, verse in enumerate(result):
                    parsed = self.parseInterlinear(result[i][2])
                    """ flatten the output:"""
                    for item in parsed:
                        """ to show the chapter, verse, greek, english ..."""
                        payload.append([result[i][0], result[i][1], item[0], item[1]])
                    #payload.append(parsed)
                category = 'table'
            
            result_object = Result()
            result_object.category = category
            result_object.payload = payload
            return result_object
    
    def parseText(self, text):
        text = text.replace('<Q>', '')
        splitted = text.split('<q>')
        
        result = ''
        for word in splitted:
            greek = re.search('<wg>(.*)<E>', word)
            if greek:
                result += greek.group(1)
                result += ' '
        
        return result
    
    def parseInterlinear(self, text):
        text = text.replace('<Q>', '')
        text = text.replace('<FI>', '(')
        text = text.replace('<Fi>', ')')
        splitted = text.split('<q>')
        
        result = []
        for word in splitted:
            greek = re.search('<wg>(.*)<E>', word)
            english = re.search('<E>(.*)<e>', word)
            
            if greek and english:
                result.append([greek.group(1), english.group(1)])
        
        return result
    
    def booksDict(self, book_name):
        books =  {
            "1mose"        : 1,
            "2mose"        : 2,
            "3mose"        : 3,
            "4mose"        : 4,
            "5mose"        : 5,
            "josua"        : 6,
            "richter"    : 7,
            "rut"        : 8,
            "1samuel"    : 9,
            "2samuel"    : 10,
            "1könige"    : 11,
            "2könige"    : 12,
            "1chronik"    : 13,
            "2chronik"    : 14,
            "esra"        : 15,
            "nehemia"    : 16,
            "ester"        : 17,
            "hiob"        : 18,
            "psalm"    : 19,
            "sprüche"    : 20,
            "prediger"    : 21,
            "hohelied"    : 22,
            "jesaja"    : 23,
            "jeremia"    : 24,
            "klagelieder"    : 25,
            "hesekiel"    : 26,
            "daniel"    : 27,
            "hosea"        : 28,
            "joel"        : 29,
            "amos"        : 30,
            "obadja"    : 31,
            "jona"        : 32,
            "micha"        : 33,
            "nahum"        : 34,
            "habakuk"    : 35,
            "zefanja"    : 36,
            "haggai"    : 37,
            "sacharja"    : 38,
            "maleachi"    : 39,
            
            "matthäus"    : 40,
            "markus"    : 41,
            "lukas"        : 42,
            "johannes"    : 43,
            "apostelgeschichte"    : 44,
            "römer"        : 45,
            "1korinther"    : 46,
            "2korinther"    : 47,
            "galater"    : 48,
            "epheser"    : 49,
            "philipper"    : 50,
            "kolosser"    : 51,
            "1thessalonicher"    : 52,
            "2thessalonicher"    : 53,
            "1timotheus"    : 54,
            "2timotheus"    : 55,
            "titus"        : 56,
            "philemon"    : 57,
            "hebräer"    : 58,
            "jakobusbrief"    : 59,
            "1petrus"    : 60,
            "2petrus"    : 61,
            "1johannes"    : 62,
            "2johannes"    : 63,
            "3johannes"    : 64,
            "judas"        : 65,
            "offenbarung"    : 66 
        }
        
        return books[book_name]
    
