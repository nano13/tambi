
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

from pysword.modules import SwordModules

#from modules.bituza.bituza import Bituza

class Sword(object):
    
    current_module = 'GerNeUe'
    
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "sword.commands": self.commands,
            
            "sword.word": self.word,
            
            "sword.modules": self.listModules,
            "sword.getModule": self.getCurrentModule,
            "sword.setModule": self.setCurrentModule,
            
            "sword.languages" : self.listLanguages,
            }
    
    def interpreter(self, command, args):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        print("not found in SWORD")
        raise CommandNotInThisModule("command not found in module sword")
    
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
    
    def listModules(self, c, args):
        modules = SwordModules()
        found_modules = modules.parse_modules()
        
        result = []
        for key in found_modules:
            row = []
            row.append(key)
            
            #for item in found_modules[key]:
            #    row.append(found_modules[key][item])
            row.append(found_modules[key]['lang'])
            row.append(found_modules[key]['about'].replace('\par', "\n"))
            
            if len(args) == 1:
                category = "itemized"
                if found_modules[key]['lang'] == args[0]:
                    result.append(row)
            else:
                category = "table"
                result.append(row)
        
        result_object = Result()
        result_object.category = category
        result_object.payload = sorted(result)
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
    
    def getCurrentModule(self, c, a):
        result_object = Result()
        result_object.category = "list"
        result_object.payload = self.current_module
        return result_object
    
    def setCurrentModule(self, c, args):
        self.current_module = args[0]
        
        result_object = Result()
        result_object.category = "list"
        result_object.payload = 'module set to: ' + args[0]
        return result_object
    
    def word(self, command, args):
        result_object = Result()
        result = None
        
        modules = SwordModules()
        found_modules = modules.parse_modules()
        try:
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
        except KeyError:
            result_object.error = 'current module does not exists: '+self.current_module
        
        result_object.category = "text"
        if result:
            result_object.payload = result
        return result_object
