
import sqlite3, re

class HenochParser(object):
    
    struct = []
    
    def __init__(self):
        self.initDB()
        
        fobj = open('henoch_stripped.txt')
        
        for line in fobj:
            line = line.strip()
            
            if line.startswith('Kap.'):
                verse_entry = {'chapter' : line.split(' ')[1]}
                print(verse_entry)
            
            else:
                if line:
                    splitted = re.split('[1-9]\.', line)
                    print(splitted)
                    """
                    last_char = None
                    for i, char in enumerate(line):
                        if char == '.' and last_char.isdigit():
                            verse = 
                        
                        
                        last_char = char
                    """
                    
                    """
                    last_char = None
                    verse = ''
                    for char in line:
                        if char == '.':
                            if last_char.isdigit():
                                verse_entry['verse'] = last_char + char
                                
                                verse_entry['word'] = verse
                                verse = ''
                            
                            else:
                                verse += char
                        
                        else:
                            verse += char
                            
                            last_char = char
                    """
        
        fobj.close()
    
    def initDB(self):
        self.connection = sqlite3.connect("./henoch.sqlite.db")
        self.cursor = self.connection.cursor()
        
        query = "CREATE TABLE IF NOT EXISTS henoch (chapter, verse, word)"
        self.cursor.execute(query)

if __name__ == '__main__':
    c = HenochParser()
