
import sqlite3, time

class DbAdapter(object):
    
    def __init__(self, dbpath):
        self.connection = sqlite3.connect(dbpath)
        self.cursor = self.connection.cursor()
        
        self.initializeTables()
        
    
    def dictFactory(self, result):
        result_list = []
        for row in result:
            dic = {}
            for i, col in enumerate(self.cursor.description):
                dic[col[0]] = row[i]
            result_list.append(dic)
        
        return result_list
    
    def initializeTables(self):
        query = "CREATE TABLE IF NOT EXISTS gps (rowid INTEGER PRIMARY KEY AUTOINCREMENT, latitude NUMERIC, longitude NUMERIC, altitude NUMERIC, speed NUMERIC, track NUMERIC, climb NUMERIC, error_horizontal NUMERIC, error_vertical NUMERIC, time_gps, timestamp_local)"
        self.cursor.execute(query)
        self.connection.commit()
    
    def insertLogEntry(self, data_dict):
        query = "INSERT INTO gps (latitude, longitude, altitude, speed, track, climb, error_horizontal, error_vertical, time_gps, timestamp_local) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, [
            data_dict['latitude'],
            data_dict['longitude'],
            data_dict['altitude'],
            data_dict['speed'],
            data_dict['track'],
            data_dict['climb'],
            data_dict['error_horizontal'],
            data_dict['error_vertical'],
            data_dict['time'],
            time.time(),
        ])
        self.connection.commit()
    
    def selectLogData(self):
        query = "SELECT * FROM gps"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)
    
    def selectMinMaxLogCoordinate(self):
        query = "SELECT MIN(latitude) AS lat_min, MAX(latitude) AS lat_max, MIN(longitude) AS long_min, MAX(longitude) AS long_max FROM gps"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        
        return self.dictFactory(result)[0]
    
