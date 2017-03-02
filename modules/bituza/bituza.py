# -*- coding: utf_8 -*-

from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

import sqlite3

class Bituza(object):
    def __init__(self):
        
        self.connection = sqlite3.connect("./modules/bituza/tuz.sqlite.db")
        self.cursor = self.connection.cursor()
    
    def getCommands(self):
        return {
            "bituza.commands" : self.commands,
            
            "bituza.books" : self.books,
            
            #"bituza.search" : self.searchAll,
            "bituza.search.elberfelder" : self.search,
            "bituza.search.unicode" : self.search,
            "bituza.search.ascii" : self.search,
            "bituza.search.transcription" : self.search,
            "bituza.search.code" : self.search,
            "bituza.search.latex" : self.search,
            "bituza.search.tw" : self.search,
            "bituza.search.wv" : self.search,
            "bituza.search.wk" : self.search,
            "bituza.search.wb" : self.search,
            "bituza.search.abk" : self.search,
            "bituza.search.abb" : self.search,
            "bituza.search.abv" : self.search,
            "bituza.search.anz_b" : self.search,
            
            "bituza.search.stats_verse" : self.search,
            "bituza.search.total_v" : self.search,
            "bituza.search.total_k" : self.search,
            "bituza.search.total_b" : self.search,
            "bituza.search.sum_v" : self.search,
            "bituza.search.sum_k" : self.search,
            "bituza.search.sum_b" : self.search,
            
            "bituza.stats" : self.stats,
            
            "bituza.word" : self.word,
            "bituza.elberfelder" : self.elberfelder,
            "bituza.tr" : self.textusReceptus,
            
            "bituza.sql" : self.sql,
            "bituza.schema" : self.schema,
        }
    
    def interpreter(self, command, args):
        print("args:", args)
        
        commands = self.getCommands()
        #return_value, mime_value = commands.get(command, self.commandNotFound)(command, args)
        #return return_value, mime_value
        
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module bituza")
    
    def books(self, c, a):
        query = "SELECT name_intern FROM books"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        result_object = Result()
        result_object.category = "table"
        result_object.header = ["name_intern"]
        result_object.payload = result
        result_object.name = "bituza.books"
        return result_object
    
    def sql(self, c, a):
        try:
            query = a[0]
        except:
            result = Result()
            result.error = "FEHLER: bitte SQL-Abfrage als Argument übergeben!"
            return result
        
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        head = "1"
        name = "tabelle: sql"
        
        result_object = Result()
        result_object.category = "table"
        result_object.header = head
        result_object.payload = result
        result_object.name = name
        return result_object
    
    def schema(self, c, a):
        schema = ""
        return schema
    
    def stats(self, c, a):
        dictOT = self.booksDictOT()
        dictAT = self.booksDictNT()
        
        try:
            book_id = dictOT[a[0]]
        except:
            try:
                book_id = dictAT[a[0]]
            except:
                result = Result()
                result.error = "FEHLER: bitte Buch angeben!"
                return result
        try:
            chapter = a[1]
        except:
            result = Result()
            result.error = "FEHLER: bitte Kapitel angeben!"
            return result
        
        query_head = "SELECT book_string, chapter, verse, stats_verse, total_v, total_k, total_b, sum_v, sum_k, sum_b FROM stats NATURAL JOIN structure "
        
        if len(a) == 2:
            query_tail = "WHERE book_id=? AND chapter=?"
            values = book_id, chapter
        elif len(a) == 3:
            if a[2].find("-") > -1:
                start_verse, end_verse = a[2].split("-")
                query_tail = "WHERE book_id=? AND chapter=? AND verse>=? AND verse<=?"
                values = book_id, chapter, start_verse, end_verse
            else:
                query_tail = "WHERE book_id=? AND chapter=? AND verse=?"
                verse = a[2]
                values = book_id, chapter, verse
            
        query = query_head + query_tail
        
        
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        
        head = "buch", "kapitel", "vers", "stats_verse", "total_v", "total_k", "total_b", "sum_v", "sum_k", "sum_b"
        metaLang = "de", "de", "de", "de", "de", "de", "de", "de", "de", "de"
        name = "stats"
        
        result_object = Result()
        result_object.category = "table"
        result_object.header = head
        result_object.payload = result
        result_object.metaload = metaLang
        result_object.name = name
        return result_object
    
    def searchGlobal(self, c, args):
        query = "SELECT "
    
    def search(self, c, a):
        #head = "buch", "kapitel", "vers", "unicode", "elberfelder", "ascii", "zahlencode", "tw", "wv", "wk", "wb", "abk", "abb", "abv", "anz_b"
        #query_head = "SELECT book_string, chapter, verse, unicode, translation_de, ascii, code, tw, wv, wk, wb, abk, abb, abv, anz_b FROM word NATURAL JOIN structure WHERE"
        
        if len(a) == 1:
            search_pattern = a[0]
            
            head, query_head, query_mid, metaLanguage = self.searchGetQueryMid(c)
            query_tail = None
            return self.searchGlobal(c, head, metaLanguage, query_head, query_mid, query_tail, search_pattern, True)
        
        elif len(a) == 3:
            if a[1] == "in":
                search_pattern = a[0]
                search_book = a[2]
                
                if search_book.find("-") > -1:
                    start_book, end_book = search_book.split("-")
                    return self.searchBookRange(c, start_book, end_book, search_pattern)
                else:
                    result, head, metaLanguage = self.searchSingleBook(c, search_book, search_pattern, True)
                    return result
            else:
                result = Result()
                result.error = "FEHLER: suchanfrage konnte nicht sinnvoll verarbeitet werden!"
                return result
            
        else:
            result = Result()
            result.error = "FEHLER: suchanfrage konnte nicht sinnvoll verarbeitet werden!"
            return result
        
    def searchBookRange(self, c, start_book, end_book, search_pattern):
        book_list = self.getBookList()
        try:
            book_start_index = book_list.index(start_book)
        except:
            result = Result()
            result.error = "FEHLER: Buch " + unicode(start_book) + " konnte nicht gefunden werden!"
            return result
        try:
            book_end_index = book_list.index(end_book)
        except:
            result = Result()
            result.error = "FEHLER: Buch " + unicode(end_book) + " konnte nicht gefunden werden!"
            return result
        
        result_list = []
        i = book_start_index -1
        while i < book_end_index:
            i += 1
            
            search_book = book_list[i]
            
            result, head, metaLanguage = self.searchSingleBook(c, search_book, search_pattern, False)
            result_list.append(result)
            
            print(search_book)
        
        format_list = []
        for item in result_list:
            for item2 in item:
                format_list.append(item2)
        
        name = "search result: " + search_pattern
        
        result_object = Result()
        result_object.category = "table"
        result_object.header = head
        result_object.payload = format_list
        result_object.metaload = metaLanguage
        result_object.name = name
        return result_object
            
        
    def searchSingleBook(self, c, search_book, search_pattern, result_in_table):
        dictOT = self.booksDictOT()
        dictNT = self.booksDictNT()
        try:
            book_id = dictOT[ search_book ]
        except:
            try:
                book_id = dictNT[ search_book ]
            except:
                result = Result()
                result.error = "FEHLER: bitte Buch angeben!"
                return result
        #else:
        head, query_head, query_mid, metaLanguage = self.searchGetQueryMid(c)
        query_tail = " AND book_id="+str(book_id)
        result = self.searchGlobal(c, head, metaLanguage, query_head, query_mid, query_tail, search_pattern, result_in_table)
        #return result, head, metaLanguage
        result_object = Result()
        result_object.category = "table"
        result_object.header = head
        result_object.payload = result
        result_object.metaload = metaLanguage
        result_object.name = "search result: " + search_pattern
        return result_object
        
    def searchGetQueryMid(self, c):
        query_head = "SELECT book_string, chapter, verse, unicode, translation_de, ascii, transcription, code, tw, wv, wk, wb, abk, abb, abv, anz_b FROM word NATURAL JOIN structure WHERE"
        head = "buch", "kapitel", "vers", "unicode", "elberfelder", "ascii", "transcription", "code", "tw", "wv", "wk", "wb", "abk", "abb", "abv", "anz_b"
        metaLanguage = "de", "de", "de", "gr", "de", "de", "de", "de", "de", "de", "de", "de", "de", "de", "de", "de"
        
        if c == "bituza.search.elberfelder":
            query_mid = " translation_de LIKE "#+search_pattern+"'"
        elif c == "bituza.search.unicode":
            query_mid = " unicode LIKE "#+search_pattern+"'"
        elif c == "bituza.search.ascii":
            query_mid = " ascii LIKE "#+search_pattern+"'"
        elif c == "bituza.search.transcription":
            query_mid = u" transcription LIKE "#+search_pattern+"'"
        elif c == "bituza.search.tw":
            query_mid = " tw LIKE "#+search_pattern+"'"
        elif c == "bituza.search.wv":
            query_mid = " wv LIKE "#+search_pattern+"'"
        elif c == "bituza.search.wk":
            query_mid = " wk LIKE "#+search_pattern+"'"
        elif c == "bituza.search.wb":
            query_mid = " wb LIKE "#+search_pattern+"'"
        elif c == "bituza.search.abk":
            query_mid = " abk LIKE "#+search_pattern+"'"
        elif c == "bituza.search.abb":
            query_mid = " abb LIKE "#+search_pattern+"'"
        elif c == "bituza.search.abv":
            query_mid = " abv LIKE "#+search_pattern+"'"
        elif c == "bituza.search.anz_b":
            query_mid = " anz_b LIKE "#+search_pattern+"'"
        elif c == "bituza.search.code":
            query_mid = " code LIKE "#+search_pattern+"'"
            
        else:
            head = "buch", "kapitel", "vers", "stats_verse", "total_v", "total_k", "total_b", "sum_v", "sum_k", "sum_b"
            query_head = "SELECT book_string, chapter, verse, stats_verse, total_v, total_k, total_b, sum_v, sum_k, sum_b FROM stats NATURAL JOIN structure WHERE"
            metaLanguage = "de", "de", "de", "de", "de", "de", "de", "de", "de", "de"
            
            if c == "bituza.search.stats_verse":
                query_mid = " stats_verse LIKE "#+search_pattern+"'"
            elif c == "bituza.search.total_v":
                query_mid = " total_v LIKE "#+search_pattern+"'"
            elif c == "bituza.search.total_k":
                query_mid = " total_k LIKE "#+search_pattern+"'"
            elif c == "bituza.search.total_b":
                query_mid = " total_b LIKE "#+search_pattern+"'"
            elif c == "bituza.search.sum_v":
                query_mid = " sum_v LIKE "#+search_pattern+"'"
            elif c == "bituza.search.sum_k":
                query_mid = " sum_k LIKE "#+search_pattern+"'"
            elif c == "bituza.search.sum_b":
                query_mid = " sum_b LIKE "#+search_pattern+"'"
            
        return head, query_head, query_mid, metaLanguage
    
    def searchGlobal(self, c, head, metaLanguage, query_head, query_mid, query_tail, search_pattern, result_in_table):
        if query_tail:
            query = query_head + query_mid +"?"+ query_tail
        else:
            query = query_head + query_mid +"?"
            
        print(query, result_in_table)
        
        if c == "bituza.search.elberfelder":
            value = [ "%" + str(search_pattern) + "%" ]
        elif c == "bituza.search.unicode":
            value = [ "%" + str(search_pattern) + "%" ]
        else:
            value = [ str(search_pattern) ]
            
        self.cursor.execute(query, value)
        result = self.cursor.fetchall()
        print(result)
        
        if len(result) == 0:
            if result_in_table:
                result = Result()
                result.error = "FEHLER: keine Ergebnisse gefunden!"
                return result
            else:
                return []
        else:
            if result_in_table:
                name = "suchergebnis: " + search_pattern
                result_object = Result()
                result_object.category = "table"
                result_object.header = head
                result_object.payload = result
                result_object.metaload = metaLanguage
                result_object.name = name
                return result_object

            else:
                return(result)
        
    def word(self, c, a):
        query_head = "SELECT book_string, chapter, verse, unicode, translation_de, transcription, tw, code, wv, wk, wb, abk, abb, abv, anz_b FROM word NATURAL JOIN structure WHERE book_id=? AND chapter=?"
        head = "buch", "kapitel", "vers", "unicode", "elberfelder", "transcription", "tw", "code", "wv", "wk", "wb", "abk", "abb", "abv", "anz_b"
        
        dictOT = self.booksDictOT()
        dictNT = self.booksDictNT()
        testament = None
        
        try:
            book_id = dictOT[a[0]]
        except:
            try:
                book_id = dictNT[a[0]]
            except:
                result = Result()
                result.error = "FEHLER: bitte Buch angeben!"
                return result
            else:
                testament = "NEW"
                metaLanguage = "de", "de", "de", "gr", "de", "de", "de", "de", "de", "de", "de", "de", "de", "de", "de"
        else:
            testament = "OLD"
            metaLanguage = "de", "de", "de", "il", "de", "de", "de", "de", "de", "de", "de", "de", "de", "de", "de"
        
        if len(a) == 2:
            query = query_head
            if a[1].isdigit():
                values = book_id, a[1]
            else:
                result = Result()
                result.error = "FEHLER: bitte Kapitel als Zahl angeben!"
                return result
        elif len(a) == 3:
            query = query_head + " AND verse=?"
            if a[1].isdigit():
                if a[2].isdigit():
                    values = book_id, a[1], a[2]
                else:
                    #return "fehler: bitte vers als zahl angeben!;", "msg/error"
                    first, last = a[2].split("-")
                    
                    query = query_head + " AND verse>=? AND verse<=?"
                    values = book_id, a[1], first, last
            else:
                result_object = Result()
                result_object.error = "FEHLER: bitte Kapitel als Zahl angeben!"
                return result_object
        else:
            result_object = Result()
            result_object.error = "FEHLER: bitte Kapitel als Zahl angeben!"
            return result_object
            
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        
        if len(result) == 0:
            result_object = Result()
            result_object.error = "FEHLER: diese Stelle existiert nicht!"
            return result
        else:
            name = ["tabelle: "]
            for i in range(len(a)):
                name.append(a[i])
                
            name = " ".join(name)
            
            result_object = Result()
            result_object.category = "table"
            result_object.payload = result
            result_object.metaload = metaLanguage
            result_object.header = head
            result_object.name = name
            return result_object
        
    def resultInTextWidget(self, head, result, name):
        from lib.widgets.speakingTextWidget import SpeakingTextWidget
        textWidget = SpeakingTextWidget(self.Universe, name)
        
        return textWidget, "tw"
        
    def resultInTable(self, head, result, metaLang, name):
        result = Result()
        result.payload = result
        result.metaload = metaLang
        print("NAME:", name)
        return result
        
    def resultInTableOLD(self, head, result, metaLanguage, name):
        try:
            result_first_element = result[0]
        except:
            result = Result()
            result.error = "FEHLER: kein Ergebnis gefunden!"
            return result
        else:
            #table = SpeakingTableWidget(len(result), len(result_first_element), self.Universe, name)
            
            #table.setHorizontalHeaderLabels(head)
            
            row = -1
            for line in result:
                row += 1
                
                column = -1
                for item in line:
                    column += 1
                    
                    table.setItem(row, column, QtGui.QTableWidgetItem(unicode(item)) )
                    metaData = MetaData()
                    metaData.Language = metaLanguage[column]
                    table.setDescription(row, column, metaData)
                    
                    #print item, metaData.Language
            
            table.resizeColumnsToContents()
            
            self.ResultObject.Payload.SpeakingTableWidget = table
            return self.ResultObject
        #return table, "table"
#        return "bla", "blub"
        
    def elberfelder(self, c, args):
        if len(args) == 2:
            # select a whole chapter
            query = """SELECT chapter, verse, elberfelder_verse FROM elberfelder
            JOIN structure ON structure.structure_row_id = elberfelder.structure_row_id
            JOIN books ON structure.book_id = books.id
            WHERE books.name_intern=? AND structure.chapter=?"""
            params = [args[0], args[1]]
        elif len(args) == 3:
            query = """SELECT verse, elberfelder_verse FROM elberfelder
            JOIN structure ON structure.structure_row_id = elberfelder.structure_row_id
            JOIN books ON structure.book_id = books.id
            WHERE books.name_intern=? AND structure.chapter=? AND structure.verse >= ? AND structure.verse <= ?"""
            if args[2].find('-') >= 0:
                verse_start, verse_end = args[2].split('-')
                params = [args[0], args[1], verse_start, verse_end]
            else:
                params = [args[0], args[1], args[2], args[2]]
            
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()
        
        result_object = Result()
        result_object.category = 'list'
        result_object.payload = result
        return result_object
        
    def textusReceptus(self, c, a):
        query = "SELECT verse, unicode FROM word NATURAL JOIN structure WHERE book_id=66 AND chapter=1 AND verse>=1 AND verse<=4"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        current_verse_number = int( result[0][0] )
        print(current_verse_number)
        result_list = []
        result_line = ""
        j = 1
        for i in range( len(result) ):
            print(current_verse_number)#, result_line
            if result[i][0] == current_verse_number:
                result_line += result[i][1] + " "
            else:
                j += 1
                current_verse = int( result[j][0] )
                
                result_list.append(result_line)
                print(i, current_verse_number)
                result_line = result[i][1] + " "
                
        self.ResultObject.Payload.List = result_list
        return self.ResultObject
                
        
    def commands(self, none1, none2):
        dic = self.getCommands()
        commands = sorted(dic.items())
        
        all_commands = []
        mime_list = []
        for key in commands:
            line = str(key).split(",")[0]
            all_commands.append(str(line[2:-1]))
            
        result_object = Result()
        result_object.category = "list"
        result_object.payload = all_commands
        return result_object
        
    def booksDictOT(self):
        return {
            "1mose"        : 1,
            "2mose"        : 2,
            "3mose"        : 3,
            "4mose"        : 4,
            "5mose"        : 5,
            "josua"        : 6,
            "richter"    : 7,
            "rut"        : 8,
            "1samuel"    : 9,
            "2samuel"    : 10,
            "1könige"    : 11,
            "2könige"    : 12,
            "1chronik"    : 13,
            "2chronik"    : 14,
            "esra"        : 15,
            "nehemia"    : 16,
            "ester"        : 17,
            "hiob"        : 18,
            "psalm"    : 19,
            "sprüche"    : 20,
            "prediger"    : 21,
            "hohelied"    : 22,
            "jesaja"    : 23,
            "jeremia"    : 24,
            "klagelieder"    : 25,
            "hesekiel"    : 26,
            "daniel"    : 27,
            "hosea"        : 28,
            "joel"        : 29,
            "amos"        : 30,
            "obadja"    : 31,
            "jona"        : 32,
            "micha"        : 33,
            "nahum"        : 34,
            "habakuk"    : 35,
            "zefanja"    : 36,
            "haggai"    : 37,
            "sacharja"    : 38,
            "maleachi"    : 39,
        }
        
    def booksDictNT(self):
        return {
            "matthäus"    : 40,
            "markus"    : 41,
            "lukas"        : 42,
            "johannes"    : 43,
            "apostelgeschichte"    : 44,
            "römer"        : 45,
            "1korinther"    : 46,
            "2korinther"    : 47,
            "galater"    : 48,
            "epheser"    : 49,
            "philipper"    : 50,
            "kolosser"    : 51,
            "1thessalonicher"    : 52,
            "2thessalonicher"    : 53,
            "1timotheus"    : 54,
            "2timotheus"    : 55,
            "titus"        : 56,
            "philemon"    : 57,
            "hebräer"    : 58,
            "jakobusbrief"    : 59,
            "1petrus"    : 60,
            "2petrus"    : 61,
            "1johannes"    : 62,
            "2johannes"    : 63,
            "3johannes"    : 64,
            "judas"        : 65,
            "offenbarung"    : 66 
        }
    
    def getBookList(self):
        book_list = ["1mose", "2mose", "3mose", "4mose", "5mose", "josua", "richter", "rut", "1samuel", "2samuel", u"1könige", u"2könige", "1chronik", "2chronik", "esra", "nehemia", "ester", "hiob", "psalm", u"sprüche", "prediger", "hohelied", "jesaja", "jeremia", "klagelieder", "hesekiel", "daniel", "hosea", "joel", "amos", "obadja", "jona", "micha", "nahum", "habakuk", "zefanja", "haggai", "sacharja", "maleachi", u"matthäus", "markus", "lukas", "johannes", "apostelgeschichte", u"römer", "1korinther", "2korinther", "galater", "epheser", "philipper", "kolosser", "1thessalonicher", "2thessalonicher", "1timotheus", "2timotheus", "titus", "philemon", u"hebräer", "jakobusbrief", "1petrus", "2petrus", "1johannes", "2johannes", "3johannes", "judas", "offenbarung" ]
        
        return book_list
    
    "used by module sword"
    def getChapterLength(self, book_id, chapter):
        query = "SELECT structure_row_id FROM structure WHERE book_id=? AND chapter=?"
        
        values = book_id, chapter
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        
        return len(result)
        
