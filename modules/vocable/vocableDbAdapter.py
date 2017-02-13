
from configs.configFiles import ConfigFile, ConfigDir

import sqlite3, time, random, os, shutil

MASTER_DB_PATH = "modules/vocable/vocables.db"

class VocableDbAdapter(object):
    def __init__(self):
        
        # copy vocables.db to config dir first
        config = ConfigFile()
        dbpath = config.readPath("vocable", "vocableDBPath")
        if not os.path.exists(dbpath):
            moveToConfigDir = ConfigDir()
            sourcepath = os.path.join(os.getcwd(), MASTER_DB_PATH)
            os.makedirs(os.path.dirname(dbpath))
            shutil.copyfile(sourcepath, dbpath)
        
        
        self.connection = sqlite3.connect(dbpath)
        self.cursor = self.connection.cursor()
        
    def getAvailableLanguages(self):
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        result_cleaned = []
        
        for res in result:
            if not res[0].startswith("sqlite"):
                result_cleaned.append(res[0])
        
        return sorted(result_cleaned)
    
    def getRandomVocableList(self, language, count):
        query = "SELECT display, gloss FROM {0} ORDER BY RANDOM() LIMIT {1}".format(language, count)
        
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        vocable_list = []
        translation_list = []
        
        for vocable in result:
            vocable_list.append(vocable[0])
            translation_list.append(vocable[1])
        
        return vocable_list, translation_list
    
    def getIntelligentVocableList(self, language, count):
        #control_list = ["p", "p", "p", "w", "w", "w", "s", "s", "r", "r"]
        POOR_COUNT = 5
        WEAK_COUNT = 3
        STRONG_COUNT = 1
        NEW_COUNT = 1
        
        query_poor = "SELECT display, gloss FROM {0} WHERE known < 0 ORDER BY RANDOM() LIMIT {1}".format(language, count)
        query_weak = "SELECT display, gloss FROM {0} WHERE known <= 5 AND known > 0 ORDER BY RANDOM() LIMIT {1}".format(language, count)
        query_strong = "SELECT display, gloss FROM {0} WHERE known > 5 ORDER BY RANDOM() LIMIT {1}".format(language, count)
        query_random = "SELECT display, gloss FROM {0} ORDER BY RANDOM() LIMIT {1}".format(language, count)
        
        query_list = [query_poor, query_weak, query_strong, query_random]
        result_list = []
        for query in query_list:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            result_list.append(result)
        
        vocable_list = []
        translation_list = []
        
        for i, item in enumerate(result_list):
            
            if len(item) > 0:
                if i == 0:
                    for j, vocable in enumerate(item):
                        if j < POOR_COUNT:
                            vocable_list.append(vocable[0])
                            translation_list.append(vocable[1])
                elif i == 1:
                    for j, vocable in enumerate(item):
                        if j < WEAK_COUNT:
                            vocable_list.append(vocable[0])
                            translation_list.append(vocable[1])
                elif i == 2:
                    for j, vocable in enumerate(item):
                        if random.randint(0, 1) == 1:
                            if j < STRONG_COUNT:
                                vocable_list.append(vocable[0])
                                translation_list.append(vocable[1])
                elif i == 3:
                    for j, vocable in enumerate(item):
                        #if random.randint(0, 2) == 1:
                            if j < NEW_COUNT:
                                vocable_list.append(vocable[0])
                                translation_list.append(vocable[1])
        
        ## wenn noch platz ist, versuchen wir erstmal mit schwachen woertern voll zu machen:
        #j = len(result_list[0])-1
        #while len(vocable_list) < count:
            #vocable_list.append(result_list[0][j][0])
            #translation_list.append(result_list[0][j][1])
            #j -= 1
        
        # fuelle, falls noch platz ist, mit neuen woertern auf:
        j = 0
        while len(vocable_list) < count:
            vocable_list.append(result_list[-1][j][0])
            translation_list.append(result_list[-1][j][1])
            j += 1
        
        return vocable_list, translation_list
    
    def updatePriority(self, language, display, priority):
        select_query = 'SELECT priority FROM {0} WHERE display="{1}"'.format(language, display)
        update_query = 'UPDATE {0} SET priority="#" WHERE display="{1}"'.format(language, display)
        self.updateCalculator(select_query, priority, update_query)
    
    def updateKnown(self, language, display, value):
        select_query = 'SELECT known FROM {0} WHERE display="{1}"'.format(language, display)
        update_query = 'UPDATE {0} SET known="#" WHERE display="{1}"'.format(language, display)
        self.updateCalculator(select_query, value, update_query)
        
    # adds (or subtracts) the value from the selected one and saves it back to the db
    def updateCalculator(self, select, value, update):
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        
        res = int(result[0][0])
        new_value = res + int(value)
        
        # known = 0 means 'not learned' in db, we want to avoid this state for already learned ones:
        if new_value == 0:
            new_value = res + int(value)
            
        update = update.replace('#', '{0}').format(new_value)
        
        self.cursor.execute(update)
        self.connection.commit()
        
    def updateLastLearnedDate(self, language, display):
        date = int(time.time())
        
        query = "UPDATE {0} SET changed={1} WHERE display='{2}'".format(language, date, display)
        self.cursor.execute(query)
        self.connection.commit()
        
    def getStats(self, language):
        query = "SELECT display, gloss, COUNT(word), known FROM {0} GROUP BY known".format(language)
        
        self.cursor.execute(query)
        result = self.cursor.fetchall()
                
        return result
    
