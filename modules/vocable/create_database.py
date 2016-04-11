#!/bin/env python
# -*- coding: utf_8 -*-

import sqlite3
from xml.sax import make_parser, handler
import os

class DatabaseAdapter(object):
    def __init__(self):
        print("init dbase")
        
        self.table_name = ""
        
        self.connection = sqlite3.connect("./vocables.db")
        self.cursor = self.connection.cursor()
        
    def setName(self, name):
        self.table_name = name
        self.createTables(name)
    
    def createTables(self, name):
        print("TABLE NAME:", name)
        self.cursor.execute("DROP TABLE IF EXISTS " + name)
        query = "CREATE TABLE IF NOT EXISTS " + name + " (rowid INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT KEY, display TEXT, gloss TEXT, priority NUMERIC, known NUMERIC, changed NUMERIC)"
        self.cursor.execute(query)
        
    def writeToDatabase(self, word, display, gloss):
        
        gloss_string = ""
        for i, item in enumerate(gloss):
            if i == 0:
                gloss_string = item
            else:
                gloss_string += " | " + item
        
        query = 'INSERT INTO ' +self.table_name+ ' (word, display, gloss, priority, known) VALUES ( ?, ?, ?, 0, 0 )'
        print(query)
        print(word, display, gloss_string)
        
        self.cursor.execute(query, (word, display, gloss_string))
        
    def commit(self):
        self.connection.commit()
    
    def existsInDatabase(self, display):
        print("DISPLAY:", display)
        
        query = "SELECT * FROM "+self.table_name+" WHERE display=?"
        self.cursor.execute(query, (display,))
        result = self.cursor.fetchall()
        
        if len(result) > 0:
            return True
        else:
            return False
    
    def writeIfNotExists(self, word, display, gloss):
        if not self.existsInDatabase(display):
            print("neu anlegen")
            self.writeToDatabase(word, display, gloss)
        else:
            print("gibt es schon")

class ParseXML(handler.ContentHandler):
    def __init__(self):
        print("init parse")
        
        self.word = ""
        self.display = ""
        self.gloss = []
        self.current_content = ""
        
        self.db = DatabaseAdapter()
    
    def startElement(self, name, attrs):
        self.current_content = ""
    
    def characters(self, content):
        self.current_content += content.strip()
        
    def endElement(self, name):
        if name == "gloss":
            self.gloss.append(self.current_content)
        elif name == "word":
            self.word = self.current_content
        elif name == "display":
            self.display = self.current_content
        elif name == "entry":
            # save the setting
            
            #print(self.word, " :: ", self.display, " :: ", self.gloss)
            self.db.writeIfNotExists(self.word, self.display, self.gloss)
            
            self.gloss = []
            
    def commit(self):
        self.db.commit()
        
    def setDBaseName(self, name):
        self.db.setName(name)
    
if __name__ == "__main__":
    
    parser = make_parser()
    p = ParseXML()
    parser.setContentHandler(p)
    
    base, dirs, files = next(iter(os.walk("./")))
    print(base, dirs, files)
    
    for d in dirs:
        if d != "__pycache__":
            p.setDBaseName(d)
            
            base, dirs, files = next(iter(os.walk(d)))
        
            #print(base, dirs, files)
        
            for f in files:
                print(f)
                parser.parse(base + "/" + f)
            
    p.commit()