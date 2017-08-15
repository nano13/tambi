
import sqlite3, time

"""
SELECT name, word, translation, GROUP_CONCAT(filename)
FROM deck JOIN audio ON deck.rowid=deck_rowid
GROUP BY name, word, translation
"""

class DeckDbAdapter(object):
    def __init__(self):
        pass
    
    def initialize(self, dbpath):
        self.connection = sqlite3.connect(dbpath)
        self.cursor = self.connection.cursor()
        
        self.initializeTables()
        
        self.checkAndUpdateSchema()
    
    def closeDB(self):
        self.connection.close()
    
    def initializeTables(self):
        query = "CREATE TABLE IF NOT EXISTS deck (rowid INTEGER PRIMARY KEY AUTOINCREMENT, order_index INTEGER, name TEXT, word TEXT, phonetical TEXT, translation TEXT, svg_filename TEXT, image TEXT, created NUMERIC, known NUMERIC, priority NUMERIC, changed NUMERIC)"
        self.cursor.execute(query)
        
        query  = "CREATE TABLE IF NOT EXISTS audio (rowid INTEGER PRIMARY KEY AUTOINCREMENT, deck_rowid INTEGER, description TEXT, filename TEXT)"
        self.cursor.execute(query)
        
        self.connection.commit()
    
    def checkAndUpdateSchema(self):
        #select_query = "SELECT * FROM deck LIMIT 1"
        select_query = "PRAGMA table_info('deck')"
        self.cursor.execute(select_query)
        result = self.dictFactory(self.cursor.fetchall())
        
        columns = []
        for line in result:
            columns.append(line["name"])
        
        if not 'image' in columns:
            alter_query = "ALTER TABLE deck ADD COLUMN image TEXT"
            self.cursor.execute(alter_query)
        if not 'phonetical' in columns:
            alter_query = "ALTER TABLE deck ADD COLUMN phonetical TEXT"
            self.cursor.execute(alter_query)
        self.connection.commit()
    
    def dictFactory(self, result):
        result_list = []
        for row in result:
            dic = {}
            for i, col in enumerate(self.cursor.description):
                dic[col[0]] = row[i]
            result_list.append(dic)
        
        return result_list
    
    def saveDeckItem(self, name, word, phonetical, translation, svg_filename):
        query = "INSERT INTO deck (name, word, phonetical, translation, svg_filename, created, known, priority, changed) VALUES (?, ?, ?, ?, ?, ?, 0, 0, ?)"
        
        created = int(time.time())
        changed = int(time.time())
        
        self.cursor.execute(query, (name, word, phonetical, translation, svg_filename, created, changed))
        self.connection.commit()
    
    def getDeckItemRowID(self, name, word, phonetical, translation, svg_filename):
        query = "SELECT rowid FROM deck WHERE name=? AND word=? AND phonetical=? AND translation=? AND svg_filename=?"
        self.cursor.execute(query, (name, word, phonetical, translation, svg_filename))
        #query = "SELECT rowid FROM deck WHERE name='{0}' AND word='{1}' AND translation='{2}' AND svg_filename='{3}'".format(name, word, translation, svg_filename)
        #self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return result[0][0]
    
    def selectDeckItems(self):
        query = "SELECT rowid, order_index, name, word, phonetical,  translation, svg_filename, image FROM deck ORDER BY order_index"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)
    
    def selectDeckItemsWithAudio(self):
        query = "SELECT deck.rowid, name, word, translation, svg_filename, source, description, audio.filename FROM deck JOIN audio ON (deck.rowid = audio.deck_rowid) ORDER BY deck.rowid"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)
    def selectDeckDirtyDozenItems(self):
        query = "SELECT image, rowid, order_index, name, word, translation, svg_filename FROM deck ORDER BY RANDOM() LIMIT 12"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        except sqlite3.OperationalError:
            query = "SELECT rowid, order_index, name, word, translation, svg_filename FROM deck ORDER BY RANDOM()"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        
        return self.dictFactory(result)
    
    def selectDeckItem(self, rowid):
        query = "SELECT name, word, phonetical, translation, svg_filename, image FROM deck WHERE rowid={0}".format(rowid)
        
        self.cursor.execute(query)
        
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)[0]
    
    def updateDeckItem(self, rowid, name, word, phonetical, translation, svg_filename):
        query = "UPDATE deck SET name=?, word=?, phonetical=?, translation=?, svg_filename=? WHERE rowid=?"
        self.cursor.execute(query, (name, word, phonetical, translation, str(svg_filename), rowid))
        #query = "UPDATE deck SET name='{0}', word='{1}', phonetical='{2}' translation='{3}', svg_filename='{4}' WHERE rowid={5}".format(name, word, phonetical, translation, str(svg_filename), rowid)
        #self.cursor.execute(query)
        
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
    
    def deleteImage(self, rowid):
        query = "UPDATE deck SET image=NULL"
        self.cursor.execute(query)
        self.connection.commit()
    
    def saveAudioDict(self, audio_dict, deck_rowid):
        for item in audio_dict:
            if item["rowid"]:
                query = "UPDATE audio SET description='{0}' WHERE rowid={1}".format(item["description"], item["rowid"])
                
                self.cursor.execute(query)
            else:
                """ check if this item was already inserted """
                check_query = "SELECT filename FROM audio WHERE filename=?"
                self.cursor.execute(check_query, [item["filename"]])
                existing = self.cursor.fetchall()
                
                if not existing:
                    query = "INSERT INTO audio (deck_rowid, description, filename) VALUES ({0}, '{1}', '{2}')".format(deck_rowid, item["description"], item["filename"])
                    
                    self.cursor.execute(query)
        self.connection.commit()
    
    def selectAudio(self):
        query = "SELECT deck_rowid, filename FROM audio"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)
    
    def audioFilenamesForDeckRowID(self, rowid):
        query = "SELECT rowid, description, filename FROM audio WHERE deck_rowid={0}".format(rowid)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)
    
    def getMaxAudioCount(self):
        query = "SELECT COUNT(*) AS result FROM audio GROUP BY deck_rowid ORDER BY result DESC LIMIT 1"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print("RESULT: ", result)
        
        if result:
            return result[0][0]
        else:
            return 0
    
    def deleteAudioItem(self, rowid):
        query = "DELETE FROM audio WHERE rowid={0}".format(rowid)
        self.cursor.execute(query)
        self.connection.commit()
    def deleteAudioItemByFilename(self, filename):
        query = "DELETE FROM audio WHERE filename=?"
        self.cursor.execute(query, [filename])
        self.connection.commit()
        
    def getDataset(self):
        query = "SELECT * FROM deck ORDER BY RANDOM() LIMIT 10"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)
    
    def updateKnown(self, rowid, value):
        query_increment = '''UPDATE deck
        SET known = CASE
                    WHEN known >= 20 THEN 20
                                     ELSE known + {0}
                    END
        WHERE rowid={1}'''.format(value, rowid)
        
        query_decrement = '''UPDATE deck
        SET known = CASE
                    WHEN known <= -5 THEN -5
                                     ELSE known + {0}
                    END
        WHERE rowid={1}'''.format(value, rowid)
        
        if value < 0:
            query = query_decrement
        else:
            query = query_increment
        
        self.cursor.execute(query)
        self.connection.commit()
    
    def summary(self):
        query = '''SELECT name, word, translation, audio.description, audio.filename
        FROM deck
        JOIN audio ON deck.rowid=audio.deck_rowid'''
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        header = ['name', 'word', 'translation', 'audio.description', 'audio.filename']
        
        #return self.dictFactory(result)
        return result, header
    
    def count(self):
        query = 'SELECT COUNT(*) FROM deck'
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return result[0][0]
    
    def search(self, pattern):
        query = '''SELECT name, word, phonetical, translation, svg_filename, image, GROUP_CONCAT(filename) AS filenames
        FROM deck
        JOIN audio ON deck.rowid=deck_rowid 
        WHERE name LIKE ? OR word LIKE ? OR translation LIKE ?
        GROUP BY name, word, translation'''
        self.cursor.execute(query, ('%'+pattern+'%', '%'+pattern+'%', '%'+pattern+'%'))
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)
    
    def insertImage(self, rowid, filename):
        query = 'UPDATE deck SET image=? WHERE rowid=?'
        self.cursor.execute(query, [filename, rowid])
        self.connection.commit()
    
