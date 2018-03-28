# -*- coding: utf_8 -*-

from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

import os, re

#import sqlite3



class Bibledata(object):
    def __init__(self):
        pass
    
    #def initDbConnection(self):
        #self.connection = sqlite3.connect("./modules/quran/quran.db")
        #self.cursor = self.connection.cursor()
         
    def getCommands(self):
        return {
            "bibledata.commands" : self.commands,
            
            "bibledata.guys" : self.guys,
        }
    
    def interpreter(self, command, args, queue):
        print("args:", args)
        
        commands = self.getCommands()
        
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module bibledata")
    
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
    
    def guys(self, c, a):
        result_object = Result()
        
        import json
        
        base, dirs, files = next(iter(os.walk("./modules/bibledata/data")))
        files.sort(key=self.alphanum_key)
        
        guys_merged = []
        guys_unmerged = []
        
        try:
            ids = []
            for f in files:
                fobj = open(os.path.join(base, f))
                loaded = json.load(fobj)
                
                for guy_new in loaded:
                    if guy_new["id"] in ids:
                        raise DuplicateID()
                    ids.append(guy_new["id"])
                    
                    if len(guys_merged) <= 0:
                        guys_merged.append(guy_new)
                    else:
                        guys_merged, status = self.insertGuys(guys_merged, guy_new)
                        
                        if status == False:
                            guys_unmerged.append(guy_new)
        except DuplicateID as e:
            result_object.error = "duplicated id found in the json-data: "
        except InvalidID as e:
            result_object.error = "illegal id found in the json-data"
        else:
            result_object.category = "bloodline"
            result_object.payload = guys_merged
        
        return result_object
    
    def insertGuys(self, guys_merged, guy_new):
        
        inserted = False
        for i, guy_old in enumerate(guys_merged):
            if guy_new["id"]:
                
                if guy_new["id"] == guy_old["successor"]:
                    guys_merged.insert(i+1, guy_new)
                    inserted = True
                    break
                    
                elif guy_new["id"] == guy_old["predecessor"]:
                    guys_merged.insert(i, guy_new)
                    inserted = True
                    break
            else:
                raise InvalidID()
        
        if inserted == False:
            guys_merged.append(guy_new)
        #    return guys_merged, False
        
        return guys_merged, True;
    
    def alphanum_key(self, s):
        """ Turn a string into a list of string and number chunks.
            "z23a" -> ["z", 23, "a"]
        """
        return [ self.tryint(c) for c in re.split('([0-9]+)', s) ]
    
    def tryint(self, s):
        try:
            return int(s)
        except:
            return s

class InvalidID(Exception):
    pass

class DuplicateID(Exception):
    pass
