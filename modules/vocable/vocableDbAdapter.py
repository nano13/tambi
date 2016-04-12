
import sqlite3

class VocableDbAdapter(object):
    def __init__(self):
        
        self.connection = sqlite3.connect("./modules/vocable/vocables.db")
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
    
    def getVocableList(self, language, count):
        query = "SELECT display, gloss FROM {0} ORDER BY RANDOM() LIMIT {1}".format(language, count)
        
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return result
    
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
        update = update.replace('#', '{0}').format(new_value)
        
        self.cursor.execute(update)
        self.connection.commit()
