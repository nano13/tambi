
import urllib.request
import sqlite3

URL_BASE = "https://www.uibk.ac.at/theol/leseraum/bibel/{0}makk{1}.html"

class Downloader(object):
    
    def __init__(self):
        self.initDb()
        self.parser = Parser()
        self.parser.setDownloader(self)
        
        for i in range(1, 17):
            self.table = 'maccabees_one'
            url = URL_BASE.format(1, i)
            self.parseURL(url)
        
        self.connection.commit()
        
        for i in range(1, 16):
            self.table = 'maccabees_two'
            url = URL_BASE.format(2, i)
            self.parseURL(url)
        
        self.connection.commit()
    
    def parseURL(self, url):
        with urllib.request.urlopen(url) as response:
            html = response.read().decode("utf-8")
            self.parser.feed(html)
    
    def initDb(self):
        self.connection = sqlite3.connect('../../maccabees.sqlite.db')
        self.cursor = self.connection.cursor()
        
        queries = [
            "DROP TABLE IF EXISTS maccabees_one",
            "DROP TABLE IF EXISTS maccabees_two",
            "CREATE TABLE IF NOT EXISTS maccabees_one (chapter NUMERIC, verse NUMERIC, word TEXT)",
            "CREATE TABLE IF NOT EXISTS maccabees_two (chapter NUMERIC, verse NUMERIC, word TEXT)",
        ]
        
        for query in queries:
            self.cursor.execute(query)
    
    def insertWord(self, chapter, verse, word):
        query = "INSERT INTO {0} (chapter, verse, word) VALUES (?, ?, ?)".format(self.table)
        self.cursor.execute(query, [chapter, verse, word])

from html.parser import HTMLParser
import re

class Parser(HTMLParser):
    
    in_makk = False
    in_td = False
    
    def setDownloader(self, Downloader):
        self.Downloader = Downloader
    
    def handle_starttag(self, tag, attrs):
        pass
    
    def handle_endtag(self, tag):
        if self.in_makk:
            if tag == 'td':
                self.in_td = True
            else:
                self.in_td = False
    
    def handle_data(self, data):
        if data.find(' Makk ') > -1:
            self.in_makk = True
            self.chapter, self.verse = data.split(' ')[2].split(',')
            print(self.chapter, self.verse)
        
        elif self.in_makk and self.in_td:
            data = data.strip()
            if data:
                data = data.replace("\n", '')
                data = re.sub(' +', ' ', data)
                
                self.Downloader.insertWord(self.chapter, self.verse, data)
        
        else:
            self.in_makk = False

if __name__ == '__main__':
    c = Downloader()
