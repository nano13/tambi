
import sqlite3

class Po2Sqlite(object):
    def __init__(self):
        self.connection = sqlite3.connect("./arabic_english_dict.db")
        self.cursor = self.connection.cursor()
        
        self.iterateFiles()
        
    def iterateFiles(self):
        for i in range(ord('A'), ord('Z')+1):
            filename = 'full_wordlist_'+chr(i)+'.po'
            
            fobj_src = open('./arabic_wordlist-0.6.1/'+filename, 'r')
            
            lastline = ""
            for line in fobj_src:
                if line.startswith("msgstr"):
                    word_english = line.split(" ")[1].replace('"', '').strip()
                    word_arabic = lastline.split(" ")[1].replace('"', '').strip()
                    
                    print(word_english, word_arabic)
                    
                lastline = line
            
            fobj_src.close()
    
if __name__ == '__main__':
    c = Po2Sqlite()
