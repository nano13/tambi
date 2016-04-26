
import sqlite3, time

class DeckDbAdapter(object):
    def __init__(self, dbpath):
        
        self.connection = sqlite3.connect(dbpath)
        self.cursor = self.connection.cursor()
        
        self.initializeTables()
        
    def initializeTables(self):
        query = "CREATE TABLE IF NOT EXISTS deck (rowid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, word TEXT, translation TEXT, svg_filename TEXT, audio_filenames TEXT, created NUMERIC, known NUMERIC, priority NUMERIC, changed NUMERIC)"
        
        self.cursor.execute(query)
        self.connection.commit()
        
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
        
        return result
