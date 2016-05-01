
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
        
        query  = "CREATE TABLE IF NOT EXISTS audio (rowid INTEGER PRIMARY KEY AUTOINCREMENT, deck_rowid INTEGER, description TEXT, filename TEXT)"
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
        query = "SELECT name, word, translation, svg_filename, audio_filenames FROM deck WHERE rowid={0}".format(rowid)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)[0]
    
    def updateDeckItem(self, rowid, name, word, translation, svg_filename, audio_filenames):
        query = "UPDATE deck SET name='{0}', word='{1}', translation='{2}', svg_filename='{3}', audio_filenames='{4}' WHERE rowid={5}".format(name, word, translation, str(svg_filename), audio_filenames, rowid)
        self.cursor.execute(query)
        
        self.connection.commit()
    
    def deleteItem(self, rowid):
        query = "SELECT svg_filename FROM deck WHERE rowid={0}".format(rowid)
        self.cursor.execute(query)
        svg_filename = self.cursor.fetchall()
        
        query = "SELECT filename FROM audio WHERE deck_rowid={0}".format(rowid)
        self.cursor.execute(query)
        audio_filenames = self.cursor.fetchall()
        audio_filenames_list = []
        for filename in audio_filenames:
            audio_filenames_list.append(filename[0])
        
        query = "DELETE FROM deck WHERE rowid={0}".format(rowid)
        self.cursor.execute(query)
        
        query = "DELETE FROM audio WHERE deck_rowid={0}".format(rowid)
        self.cursor.execute(query)
        
        self.connection.commit()
        
        return svg_filename[0][0], audio_filenames_list
    
    def insertAudioDict(self, audio_dict, deck_rowid):
        for item in audio_dict:
            query = "INSERT INTO audio (deck_rowid, description, filename) VALUES ({0}, {1}, {2})".format(deck_rowid, item["description"], item["filename"])
            self.cursor.execute(query)
        self.connection.commit()
    
    def audioFilenamesForDeckRowID(self, rowid):
        query = "SELECT description, filename FROM audio WHERE deck_rowid={0}".format(rowid)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)
