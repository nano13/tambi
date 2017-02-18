
class Wordlist2Sqlite(object):
    def __init__(self):
        self.iterate()
    
    def iterate(self):
        fobj = open("./wordlist_5000_en_US.csv", "r")
        
        for line in fobj:
            rank, word, part, frequency, dispersion = line.split("|")
            
        
        fobj.close()
    
if __name__ == '__main__':
    c = Wordlist2Sqlite()
