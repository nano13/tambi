
import requests
from html.parser import HTMLParser
import sqlite3, re, json

URL = 'http://www.corpuscoranicum.de/index/index/sure/{0}/vers/{1}'
SURAH_COUNT = 114

class QuranDownloader(HTMLParser):
    def __init__(self, surah, ayah, word_count, database):
        super().__init__()
        self.surah = surah
        self.ayah = ayah
        self.word_count = word_count
        self.db = database
    
    in_arabic = False
    in_transcription = False
    in_translation = False
    
    data_arabic = ''
    data_transcription = ''
    data_translation = ''
    
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name == 'id' and value == 'sure-vers-arabic':
                self.in_arabic = True
            elif name == 'id' and value == 'transkription':
                self.in_transcription = True
            elif name == 'id' and value == 'sure-vers-translation':
                self.in_translation = True
                
            #elif name == 'id' and value == 'druckausgabe-image':
    
    def handle_endtag(self, tag):
        if self.in_arabic and tag == 'div':
            self.in_arabic = False
        if self.in_transcription and tag == 'div':
            self.in_transcription = False
        if self.in_translation and tag == 'div':
            self.in_translation = False
        
        if tag == 'html':
            #db = DbAdapter()
            print(self.surah, self.ayah)
            self.db.insertVerse(self.surah, self.ayah, self.word_count, self.data_arabic, self.data_transcription, self.data_translation)
            #print(self.surah, self.data_arabic, self.data_transcription, self.data_translation)
    
    def handle_data(self, data):
        if self.in_arabic:
            data = data.strip()
            data = re.sub(' +', '', data)
            self.data_arabic = data
        elif self.in_transcription:
            data = data.strip()
            if data:
                self.data_transcription += ' '+data
                self.data_transcription = self.data_transcription.strip()
        elif self.in_translation:
            self.data_translation = data.strip()

class DbAdapter(object):
    def __init__(self):
        self.connection = sqlite3.connect('./quran.db')
        self.cursor = self.connection.cursor()
        
        self.createTable()
        
    def createTable(self):
        query = "CREATE TABLE IF NOT EXISTS quran (surah, ayah, word_count, arabic, transcription, de_DE)"
        self.cursor.execute(query)
        
    def insertVerse(self, surah, ayah, word_count, arabic, transcription, de_DE):
        #query = 'INSERT INTO quran (surah, ayah, arabic, transcription, de_DE) VALUES ("{0}", "{1}", "{2}", "{3}", "{4}")'.format(surah, ayah, arabic, transcription, de_DE)
        query = 'INSERT INTO quran (surah, ayah, word_count, arabic, transcription, de_DE) VALUES (?, ?, ?, ?, ?, ?)'
        self.cursor.execute(query, [surah, ayah, word_count, arabic, transcription, de_DE])
        #self.connection.commit()
        
    def commit(self):
        self.connection.commit()
        
if __name__ == '__main__':
    database = DbAdapter()
    
    for surah in range(1, SURAH_COUNT+1):
        get_max_verse_url = "http://www.corpuscoranicum.de/ajax/getversanzahl/?sure={0}".format(surah)
        json_string = requests.get(get_max_verse_url)
        json_obj = json.loads(json_string.content.decode("utf-8"))
        
        for ayah in range(int(json_obj['minVers']), int(json_obj['maxVers'])+1):
            get_word_count_url = "http://www.corpuscoranicum.de/ajax/getwortanzahl?sure={0}&vers={1}".format(surah, ayah)
            word_count_string = requests.get(get_word_count_url)
            word_count_obj = json.loads(word_count_string.content.decode("utf-8"))
            
            page = requests.get(URL.format(surah, ayah))
            
            parser = QuranDownloader(surah, ayah, word_count_obj['wortanzahl'], database)
            parser.feed(page.content.decode("utf-8"))
        
        database.commit()
