
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

from configs.configFiles import ConfigFile
from misc.deckDbAdapter import DeckDbAdapter
from modules.ipa.ipa import Ipa

import os

class Deck(object):
    
    config = ConfigFile()
    dbAdapter = DeckDbAdapter()
    
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "deck.commands" : self.commands,
            
            "deck.toString" : self.toString,
            "deck.toTable" : self.toTable,
            
            "deck.count" : self.count,
            "deck.search" : self.search,
            
            "deck.ipaVowels" : self.ipaVowels,
            "deck.ipaConsonants" : self.ipaConsonants,
        }
    
    def interpreter(self, command, args):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module vocable")
    
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
    
    def toString(self, c, args):
        result_object = Result()
        
        try:
            deckname = args[0]
        except IndexError:
            result_object.error = 'please specify the deck by name!'
        else:
            deckpath = self.config.readPath("vocable", "deckpath")
            db_path = os.path.join(deckpath, deckname, 'database.sqlite')
            print(db_path)
            self.dbAdapter.initialize(db_path)
            result, header = self.dbAdapter.summary()
            
            result_object.category = "text"
            result_object.payload = result
            result_object.header = header
        
        return result_object
    
    def toTable(self, c, args):
        result_object = self.toString(c, args)
        result_object.category = "table"
        return result_object
    
    def count(self, c, args):
        result_object = Result()
        
        deck_prefix = None
        try:
            deck_prefix = args[0]
        except IndexError:
            """ everything is fine, we just do not have an argument """
            pass
        
        deckpath = self.config.readPath("vocable", "deckpath")
        root, dirs, path = next(iter(os.walk(deckpath)))
        dirs.sort()
        
        counter = 0
        for directory in dirs:
            if directory.startswith(deck_prefix):
                db_path = os.path.join(root, directory, "database.sqlite")
                self.dbAdapter.initialize(db_path)
                result = self.dbAdapter.count()
                counter += int(result)
        
        result_object.category = "string"
        result_object.payload = str(counter)
        
        return result_object
    
    def search(self, c, args):
        deckpath = self.config.readPath("vocable", "deckpath")
        root, dirs, path = next(iter(os.walk(deckpath)))
        dirs.sort()
        
        result_list = []
        result_header = ["deckname"]
        for directory in dirs:
            db_path = os.path.join(root, directory, "database.sqlite")
            self.dbAdapter.initialize(db_path)
            
            result = self.dbAdapter.search(args[0])
            
            if result:
                try:
                    result = result[0]
                except KeyError:
                    pass
                else:
                    result_line = []
                    result_line.append(directory)
                    for key in result.keys():
                        result_line.append(result[key])
                        
                        result_header.append(key)
                        
                    result_list.append(result_line)
            
            self.dbAdapter.closeDB()
        
        result_object = Result()
        result_object.category = "multimedia_table"
        #result_object.category = "table"
        result_object.payload = result_list
        result_object.header = result_header
        return result_object
    
    def ipaVowels(self, c, args):
        try:
            deck_prefix = args[0]
        except IndexError:
            """ everything is fine, we just do not have an argument """
            deck_prefix = ''
        
        ipa = Ipa()
        vowels = ipa.getVowelsDict()
        result_table = [['' for _ in range(6)] for _ in range(6)]
        
        deckpath = self.config.readPath("vocable", "deckpath")
        root, dirs, path = next(iter(os.walk(deckpath)))
        dirs.sort()
        for directory in dirs:
            if directory.startswith(deck_prefix):
                db_path = os.path.join(root, directory, "database.sqlite")
                self.dbAdapter.initialize(db_path)
                result = self.dbAdapter.selectDeckItems()
                
                for entry in result:
                    phonetical = entry["phonetical"]
                    if phonetical:
                        for char in phonetical:
                            if char in vowels:
                                position = vowels[char]
                                result_table[position[0]][position[1]] = char
        
        header = ['VV', 'VV o', 'ZV', 'ZV o', 'HV', 'HV o']
        header_left = ['geschl.', 'fast geschl.', 'halb geschl.', 'halb offen', 'fast offen', 'offen']
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = result_table
        result_object.header = header
        result_object.header_left = header_left
        return result_object
    
    def ipaConsonants(self, c, args):
        try:
            deck_prefix = args[0]
        except IndexError:
            """ everything is fine, we just do not have an argument """
            deck_prefix = ''
        
        ipa = Ipa()
        consonants = ipa.getConsonantsDict()
        result_table = [['' for _ in range(15)] for _ in range(20)]
        
        deckpath = self.config.readPath("vocable", "deckpath")
        root, dirs, path = next(iter(os.walk(deckpath)))
        dirs.sort()
        for directory in dirs:
            if directory.startswith(deck_prefix):
                db_path = os.path.join(root, directory, "database.sqlite")
                print(db_path)
                self.dbAdapter.initialize(db_path)
                result = self.dbAdapter.selectDeckItems()
                
                for entry in result:
                    phonetical = entry["phonetical"]
                    if phonetical:
                        for char in phonetical:
                            if char in consonants:
                                position = consonants[char]
                                result_table[position[0]][position[1]] = char
        
        header = ['bl', 'ld', 'd', 'al', 'post-al', 're', 'al-pal', 'pal', 'lab-pal', 'vel', 'lab-vel', 'uv', 'phar', 'epi', 'glot']
        header_left = ['plosiv (stl)', 'plosiv (sth)', 'nasal (stl)', 'nasal (sth)', 'frikativ (stl)', 'frikativ (sth)', 'rinnen-frik (stl)', 'rinnen-frik (sth)', 'lateral-frik (stl)', 'lateral-frik (sth)', 'lateral-approx (stl)', 'lateral-approx (sth)', 'vibrant (stl)', 'vibrant (sth)', 'flap (stl)', 'flap (sth)', 'approx (stl)', 'approx (sth)', 'ejektiv (stl)', 'click']
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = result_table
        result_object.header = header
        result_object.header_left = header_left
        return result_object
