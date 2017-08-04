
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

from configs.configFiles import ConfigFile
from misc.deckDbAdapter import DeckDbAdapter
import os

class Vocable(object):
    
    config = ConfigFile()
    dbAdapter = DeckDbAdapter()
    
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "vocable.search" : self.search,
        }
    
    def interpreter(self, command, args):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module vocable")
    
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
        result_object.category = "table"
        result_object.payload = result_list
        result_object.header = result_header
        return result_object
