
import sqlite3, time

class DeckDbAdapter(object):
    def __init__(self, dbpath):
        
        self.connection = sqlite3.connect(dbpath)
        #self.connection.row_factory = self.dict_factory()
        self.cursor = self.connection.cursor()
        
        self.initializeTables()
        
    def initializeTables(self):
        query = "CREATE TABLE IF NOT EXISTS deck (rowid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, word TEXT, translation TEXT, svg_filename TEXT, audio_filenames TEXT, created NUMERIC, known NUMERIC, priority NUMERIC, changed NUMERIC)"
        
        self.cursor.execute(query)
        self.connection.commit()
    
#    def dict_factory(cursor, row):
#        d = {}
#        for idx, col in enumerate(cursor.description):
#            d[col[0]] = row[idx]
#        return d
    
    def dictFactory(self, result):
        result_list = []
        
        for row in result:
            dic = {}
            
            for i, col in enumerate(self.cursor.description):
                dic[col[0]] = row[i]
            result_list.append(dic)
        
        return result_list
        
    def saveDeckItem(self, name, word, translation, svg_filename, audio_filenames):
        query = "INSERT INTO deck (name, word, translation, svg_filename, audio_filenames, created, known, priority, changed) VALUES (?, ?, ?, ?, ?, ?, 0, 0, ?)"
        
        created = int(time.time())
        changed = int(time.time())
        
        self.cursor.execute(query, (name, word, translation, svg_filename, audio_filenames, created, changed))
        self.connection.commit()
        
    def selectDeckItems(self):
        query = "SELECT rowid, name, word, translation, svg_filename, audio_filenames FROM deck"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)
    
    def selectDeckItem(self, rowid):
        query = "SELECT name, word, translation, svg_filename, audio_filenames FROM deck WHERE rowid=?"
        self.cursor.execute(query, (rowid))
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)
    
    def deleteItem(self, rowid):
        query = "DELETE FROM deck WHERE rowid={0}".format(rowid)
        self.cursor.execute(query)
        self.connection.commit()
        
