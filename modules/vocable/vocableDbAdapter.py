
import sqlite3

class VocableDbAdapter(object):
    def __init__(self):
        
        self.connection = sqlite3.connect("./vocables.db")
        self.cursor = self.connection.cursor()
        
    def getAvailableLanguages(self):
        pass
    
    def getVocableList(self, language):
        pass
