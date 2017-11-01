
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

from configs.configFiles import ConfigFile
from misc.deckDbAdapter import DeckDbAdapter
from modules.ipa.ipa import Ipa

import os, datetime

class Deck(object):
    
    config = ConfigFile(None, None)
    dbAdapter = DeckDbAdapter()
    
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "deck.commands" : self.commands,
            
            "deck.toString" : self.toString,
            "deck.toTable" : self.toTable,
            
            "deck.count" : self.count,
            "deck.chronological" : self.chronological,
            "deck.search" : self.search,
            
            "deck.ipaVowels" : self.generateIPATable,
            "deck.ipaConsonants" : self.generateIPATable,
        }
    
    def interpreter(self, command, args, queue):
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
    
    def generateIPATable(self, command, args):
        if command == 'deck.ipaVowels':
            table_type = 'vowels'
        elif command == 'deck.ipaConsonants':
            table_type = 'consonants'
        try:
            deck_prefix = args[0]
        except IndexError:
            """ everything is fine, we just do not have an argument """
            deck_prefix = ''
        
        deckpath = self.config.readPath("vocable", "deckpath")
        root, dirs, path = next(iter(os.walk(deckpath)))
        dirs.sort()
        
        """ append all 'phonetical'-characters from all decks to the variable 'result_char_list' and pass it to the ipa-class to generate the table """
        result_char_list = []
        for directory in dirs:
            if directory.startswith(deck_prefix):
                db_path = os.path.join(root, directory, "database.sqlite")
                self.dbAdapter.initialize(db_path)
                result = self.dbAdapter.selectDeckItems()
                
                for entry in result:
                    phonetical = entry["phonetical"]
                    if phonetical:
                        for char in phonetical:
                            result_char_list.append(char)
                
        ipa = Ipa()
        result_table, header, header_vertical = ipa._generateIpaTableFromData(table_type, result_char_list)
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = result_table
        result_object.header = header
        result_object.header_left = header_vertical
        return result_object
    
    def chronological(self, c, args):
        try:
            deck_prefix = args[0]
        except IndexError:
            deck_prefix = ''
        
        deckpath = self.config.readPath("vocable", "deckpath")
        root, dirs, path = next(iter(os.walk(deckpath)))
        
        entries_list = []
        for directory in dirs:
            if directory.startswith(deck_prefix):
                db_path = os.path.join(root, directory, "database.sqlite")
                self.dbAdapter.initialize(db_path)
                result = self.dbAdapter.selectDeckItems()
                
                for entry in result:
                    print(entry)
                    created = entry["created"]
                    created = datetime.datetime.fromtimestamp(int(created)).strftime('%Y-%m-%d %H:%M:%S')
                    entries_list.append([created, entry["name"], entry["word"], entry["phonetical"], entry["translation"], directory])
        entries_list.sort()
        
        header = ['date', 'name', 'word', 'phonetical', 'translation', 'deck_name']
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = entries_list
        result_object.header = header
        return result_object
