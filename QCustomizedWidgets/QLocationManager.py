

from PyQt5.QtWidgets import QWidget

from PyQt5.QtPositioning import QGeoCoordinate
from PyQt5.QtPositioning import QNmeaPositionInfoSource
from PyQt5.QtPositioning import QGeoSatelliteInfoSource
from PyQt5.QtPositioning import QGeoSatelliteInfo

from PyQt5.QtPositioning import QGeoPositionInfo
from PyQt5.QtPositioning import QGeoPositionInfoSource

class QLocationManager(QWidget):
    
    
    def __init__(self):
        super().__init__()
    
    def getGpsPosition(self):
        
        #geo = QGeoCoordinate()
        
        
        #nmea = QNmeaPositionInfoSource(QNmeaPositionInfoSource.SimulationMode)
        #nmea = QNmeaPositionInfoSource(QNmeaPositionInfoSource.RealTimeMode)
        #nmea.requestUpdate()
        #print(nmea.device())
        #geo = nmea.lastKnownPosition().coordinate()
        
        #payload = 'latitude: '+str(geo.latitude())+' | longitude: '+str(geo.longitude())
        
        #sat = QGeoSatelliteInfoSource()
        
        print(QGeoPositionInfoSource.availableSources())
        src = QGeoPositionInfoSource.createDefaultSource(self)
        src.requestUpdate()
        print(src.sourceName()) # geoclue
        
        
