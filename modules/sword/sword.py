
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

from pysword.modules import SwordModules

#from modules.bituza.bituza import Bituza

import Sword
from Sword import *

class Sword(object):
    
    current_module = 'GerNeUe'
    
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "sword": self.readBible,
            
            "sword.modules": self.listModules,
            "sword.languages" : self.listLanguages,
            }
    
    def interpreter(self, command, args):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        print("not found in SWORD")
        raise CommandNotInThisModule("command not found in module sword")
    
    def listModules(self, c, a):
        modules = SwordModules()
        found_modules = modules.parse_modules()
        
        result = []
        for key in found_modules:
            row = []
            row.append(key)
            for item in found_modules[key]:
                row.append(found_modules[key][item])
            
            result.append(row)
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = result
        return result_object
    
    def listLanguages(self, c, a):
        result = []
        
        modules = SwordModules()
        found_modules = modules.parse_modules()
        for main_key in found_modules:
            language = found_modules[main_key]['lang']
            #for sub_key in found_modules[main_key]:
            #    language = found_modules[main_key][sub_key]
            
            if not language in result:
                result.append(language)
        
        result = sorted(result)
        
        result_object = Result()
        result_object.category = "list"
        result_object.payload = result
        return result_object
    
    def readBible(self, command, args):
        result_object = Result()
        result = None
        
        modules = SwordModules()
        found_modules = modules.parse_modules()
        bible = modules.get_bible_from_module(self.current_module)
        
        try:
            if len(args) == 2:
                result = bible.get(books=[args[0]], chapters=[int(args[1])], clean=True, join='#|#')
                
                splitted = result.split('#|#')
                result = []
                for i, line in enumerate(splitted):
                    result.append([i+1, line])
            
            elif args[2].find('-') > -1:
                verse_min, verse_max = args[2].split('-')
                verse_range = range(int(verse_min), int(verse_max)+1)
                
                result = bible.get(books=[args[0]], chapters=[int(args[1])], verses=verse_range, clean=True, join='#|#')
                
                splitted = result.split('#|#')
                result = []
                for i, line in enumerate(splitted):
                    result.append([i+int(verse_min), line])
            else:
                verse_range = int(args[2])
                
                result = bible.get(books=[args[0]], chapters=[int(args[1])], verses=verse_range, clean=True, join='\n')
        except ValueError as e:
            result_object.error = str(e)
        
        
        result_object.category = "text"
        if result:
            result_object.payload = result
        return result_object
