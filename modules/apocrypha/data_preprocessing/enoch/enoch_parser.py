
import sqlite3, re

class EnochParser(object):
    
    def __init__(self):
        self.initializeDb()
        
        fobj = open('./book_of_enoch.txt')
        
        word = ""
        for line in fobj:
            
            if line.strip():
                # get the headlines
                if re.match('\A[0-9]+\)', line):
                    if word:
                        try:
                            self.saveWordToDb(book_id, chapter, verse, word.strip())
                        except UnboundLocalError:
                            pass
                        else:
                            word = ""
                    
                    book_id = line.split(')')[0]
                    headline = line.split(')')[1].strip()
                    
                    self.saveHeadlineToDb(book_id, headline)
                
                # get the first lines of the verses
                elif re.match('\A[0-9]+\.[0-9]+', line):
                    if word:
                        try:
                            self.saveWordToDb(book_id, chapter, verse, word.strip())
                        except UnboundLocalError:
                            pass
                        else:
                            word = ""
                    
                    number = line.split(' ')[0]
                    chapter, verse = number.split('.')
                    
                    word = re.sub('\A[0-9]+\.[0-9]+', '', line.strip()).strip()
                    
                
                else:
                    word = word.strip() + ' ' + line.strip()
        
        fobj.close()
        self.connection.commit()
    
    def initializeDb(self):
        self.connection = sqlite3.connect("../../enoch.sqlite.db")
        self.cursor = self.connection.cursor()
        
        query = "DROP TABLE IF EXISTS enoch"
        self.cursor.execute(query)
        
        query = "CREATE TABLE IF NOT EXISTS enoch (book_id NUMERIC, chapter NUMERIC, verse NUMERIC, word TEXT)"
        self.cursor.execute(query)
        
        query = "DROP TABLE IF EXISTS enoch_headlines"
        self.cursor.execute(query)
        
        query = "CREATE TABLE IF NOT EXISTS enoch_headlines (book_id NUMERIC, headline TEXT)"
        self.cursor.execute(query)
    
    def saveWordToDb(self, book_id, chapter, verse, word):
        query = "INSERT INTO enoch (book_id, chapter, verse, word) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, [book_id, chapter, verse, word])
    
    def saveHeadlineToDb(self, book_id, headline):
        query = "INSERT INTO enoch_headlines (book_id, headline) VALUES (?, ?)"
        self.cursor.execute(query, [book_id, headline])
    
    """
    def processBook(self, book):
        
        splitted = book.split("\n")
        verse = ""
        for line in splitted:
            
            # get the titles
            if re.match('\A[0-9]+\)', line):
                #print(line)
                pass
            
            # get the first lines of the verses
            elif re.match('\A[0-9]+\.[0-9]+', line):
                #print(line)
                verse = line
            
            elif re.match('Notes', line):
                print(line)
    """

if __name__ == '__main__':
    c = EnochParser()
