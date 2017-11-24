
import sqlite3, re

class HenochParser(object):
    
    struct = []
    
    def __init__(self):
        self.initDB()
        
        fobj = open('henoch_stripped.txt')
        
        verse_entry = {}
        for line in fobj:
            line = line.strip()
            
            if line.startswith('Kap. '):
                verse_entry['chapter'] = line.split(' ')[1]
                print(verse_entry)
            
            else:
                if line:
                    splitted = re.split('([0-9]+\. )', line)
                    #print(splitted)
                    
                    i = 0
                    for item in splitted:
                        item = item.strip()
                        if item:
                            if re.match('[0-9]+\.', item):
                                i += 1
                                
                                to_print = item.replace('.', '')
                                if not int(to_print.strip()) == i:
                                    print(to_print, i)
                                
                                
                                verse_entry['verse'] = item.replace('.', '')
                            
                            else:
                                verse_entry['word'] = item
                                
                                #print(verse_entry)
                                self.saveToDB(verse_entry)
                                
                                """ reset 'verse_entry' but preserver 'chapter' """
                                chapter = verse_entry['chapter']
                                verse_entry = {'chapter': chapter}
            
        
        fobj.close()
        self.connection.commit()
    
    def initDB(self):
        self.connection = sqlite3.connect("./henoch.sqlite.db")
        self.cursor = self.connection.cursor()
        
        query = "CREATE TABLE IF NOT EXISTS henoch (chapter NUMERIC, verse NUMERIC, word TEXT)"
        self.cursor.execute(query)
    
    def saveToDB(self, entry):
        query = "INSERT INTO henoch (chapter, verse, word) VALUES (?, ?, ?)"
        try:
            self.cursor.execute(query, [entry['chapter'], entry['verse'], entry['word']])
        except KeyError:
            self.cursor.execute(query, [entry['chapter'], -1, entry['word']])

if __name__ == '__main__':
    c = HenochParser()
