
from configs.configFiles import ConfigFile, ConfigDir

import sqlite3, time, random, os, shutil, math

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
        
    def dictFactory(self, result):
        result_list = []
        
        for row in result:
            dic = {}
            
            for i, col in enumerate(self.cursor.description):
                dic[col[0]] = row[i]
            result_list.append(dic)
        
        return result_list
        
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
    
    def getBordersForKnownStatus(self, language):
        stats = self.getStats(language)
        known_worst = stats[0][-1]
        known_best = stats[-2][-1] # [-1][-1] would be 'none' ...
        
        # divide the range between worst and best into three equal parts
        length = len(range(known_worst, known_best)) +1
        partition_size = math.ceil(length / 3)
        
        range_poor = known_worst + partition_size
        range_weak = known_worst + 2*partition_size
        range_strong = known_worst + 3*partition_size
        
        #print(range_poor, range_weak, range_strong)
        return {
            'weak_lower_limit' : range_poor,
            'weak_upper_limit' : range_weak,
        }
    
    def getIntelligentVocableList(self, language, count):
        CONTROL_LIST = ["p", "p", "p", "w", "w", "w", "p", "s", "r", "r"]
        
        borders = self.getBordersForKnownStatus(language)
        
        query_poor = 'SELECT display, gloss FROM {0} WHERE known < {1} AND priority!="never" ORDER BY RANDOM() LIMIT {2}'.format(language, borders['weak_lower_limit'], count)
        
        query_weak = 'SELECT display, gloss FROM {0} WHERE known >= {1} AND known < {2} AND priority!="never" ORDER BY RANDOM() LIMIT {3}'.format(language, borders['weak_lower_limit'], borders['weak_upper_limit'], count)
        
        query_strong = 'SELECT display, gloss FROM {0} WHERE known >= {1} AND known!="none" AND priority!="never"ORDER BY RANDOM() LIMIT {2}'.format(language, borders['weak_upper_limit'], count)
        
        query_random = 'SELECT display, gloss FROM {0} WHERE priority!="never" ORDER BY RANDOM() LIMIT {1}'.format(language, count)
        
        query_list = [
            {'query': query_poor, 'category' : 'p'},
            {'query' : query_weak, 'category' : 'w'},
            {'query' : query_strong, 'category' : 's'},
            {'query' : query_random, 'category' : 'r'},
        ]
        #result_list = []
        result_dict = {}
        for query in query_list:
            self.cursor.execute(query['query'])
            result = self.cursor.fetchall()
            result_dict[query['category']] = self.dictFactory(result)
            
        vocable_list = []
        translation_list = []
        carry = 1
        for category in CONTROL_LIST:
            print(carry)
            try:
                for i in range(0, carry):
                    vocable_item = result_dict[category].pop()
                    vocable_list.append(vocable_item['display'])
                    translation_list.append(vocable_item['gloss'])
                    print("ADDING VOCABLE FROM", category)
            except IndexError:
                carry += 1
                print("INCREMENTING CARRY", category)
            else:
                carry = 1
                print("RESETTING CARRY", category)
        
        return vocable_list[:count], translation_list[:count]
        
    def updatePriority(self, language, display, priority):
        select_query = 'SELECT priority FROM {0} WHERE display="{1}"'.format(language, display)
        update_query = 'UPDATE {0} SET priority="#" WHERE display="{1}"'.format(language, display)
        self.updateCalculator(select_query, priority, update_query)
    
    def markVocableAsNotToLearn(self, language, vocable):
        update_query = 'UPDATE {0} SET priority="never" WHERE display=?'.format(language)
        self.cursor.execute(update_query, [vocable])
        self.connection.commit()
    
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
    
