
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

from pysword.modules import SwordModules
from pysword.books import BibleStructure
import pysword.canons as pysword_canons

#from modules.bituza.bituza import Bituza

class Sword(object):
    
    current_module = 'GerNeUe'
    canon = 'default'
    
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "sword.commands": self.commands,
            
            "sword.books": self.books,
            "sword.aliases": self.booksAliases,
            #"sword.structure": self.structure,
            
            "sword.canons": self.listCanons,
            "sword.setCanon": self.setCanon,
            "sword.getCanon": self.getCanon,
            
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
        result = []
        try:
            found_modules = modules.parse_modules()
        except FileNotFoundError:
            category = 'list'
        else:
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
        result_object.payload = 'sword bible-module set to: ' + args[0]
        return result_object
    
    def listCanons(self, c, a):
        canons = pysword_canons.canons
        
        result = []
        for key, value in canons.items():
            result.append(key)
        
        result_object = Result()
        result_object.category = 'list'
        result_object.payload = result
        return result_object
    
    def getCanon(self, c, a):
        result_object = Result()
        result_object.category = 'list'
        result_object.payload = self.canon
        return result_object
    
    def setCanon(self, c, args):
        result_object = Result()
        
        canons = self.listCanons(None, None)
        if len(args) > 0 and args[0] in canons.payload:
            self.canon = args[0]
            result_object.payload = 'canon changed to: '+args[0]
        else:
            result_object.error = 'no canon specified or canon unknown'
        
        result_object.category = 'list'
        return result_object
    
    def books(self, c, args):
        structure = BibleStructure(self.canon)
        books = structure.get_books()
        result = []
        
        if ((not len(args) == 0) and (args[0] == 'ot')) or (len(args) == 0):
            for book in books['ot']:
                formatted = str(book)[5:][:-1]
                result.append(formatted)
        if ((not len(args) == 0) and (args[0] == 'nt')) or (len(args) == 0):
            for book in books['nt']:
                formatted = str(book)[5:][:-1]
                result.append(formatted)
        
        result_object = Result()
        result_object.category = "list"
        result_object.payload = result
        return result_object
    
    def canons(self):
        result = []
        
        canons = pysword_canons.canons
        
        books = canons[self.canon]
        return books
        """
        if testament == 'ot':
            for book in books['ot']:
                result.append(book)
        
        if testament == 'nt':
            for book in books['nt']:
                result.append(book)
        
        return result
        """
    
    def booksAliases(self, c, args):
        result_object = self.books(c, args)
        
        result = []
        import modules.sword.book_names.books_de as books_de
        for book in result_object.payload:
            for key, value in books_de.books.items():
                if value == book:
                    result.append(key)
        
        result_object.payload = result
        return result_object
    
    def word(self, command, args):
        result_object = Result()
        
        modules = SwordModules()
        try:
            found_modules = modules.parse_modules()
        except FileNotFoundError:
            result_object.error = 'no sword modules found on this computer. please install some!'
        else:
            try:
                bible = modules.get_bible_from_module(self.current_module)
                
                try:
                    book = args[0]
                    
                    import modules.sword.book_names.books_de as books_de
                    if book in books_de.books:
                        book = books_de.books[book]
                    
                    if len(args) == 2:
                        result = bible.get(books=[book], chapters=[int(args[1])], clean=True, join='#|#')
                        
                        splitted = result.split('#|#')
                        result = []
                        for i, line in enumerate(splitted):
                            result.append([i+1, line.strip()])
                    
                    elif args[2].find('-') > -1:
                        verse_min, verse_max = args[2].split('-')
                        verse_range = range(int(verse_min), int(verse_max)+1)
                        
                        try:
                            result = bible.get(books=[book], chapters=[int(args[1])], verses=verse_range, clean=True, join='#|#')
                        except IndexError:
                            result_object.error = 'invalid verse range'
                        else:
                            splitted = result.split('#|#')
                            result = []
                            for i, line in enumerate(splitted):
                                result.append([i+int(verse_min), line.strip()])
                    else:
                        verse_range = int(args[2])
                        
                        result = bible.get(books=[book], chapters=[int(args[1])], verses=verse_range, clean=True, join='\n')
                except ValueError as e:
                    result_object.error = str(e)
                except KeyError as e:
                    result_object.error = 'book not found in current bible: '+str(book)+"\n\n"+str(e)
                except IndexError as e:
                    result_object.error = 'invalid input. please have a look at the man-page'+"\n\n"+str(e)
            except KeyError:
                result_object.error = 'current module does not exist: '+self.current_module
            except ValueError as e:
                result_object.error = str(e)
        
        result_object.category = "text"
        if result:
            for item in args:
                command += ' '+str(item)
            result.insert(0, command)
            result_object.payload = result
        return result_object
