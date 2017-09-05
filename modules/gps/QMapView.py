
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGridLayout, QWidget, QGraphicsEllipseItem
from PyQt5.QtGui import QPen, QPainter
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QRectF

import urllib.request
import math, _thread

class QMapView(QGraphicsView):
    
    zoom = 16
    boundings_path = None
    bounds = None
    corners = {
        'nw' : None,
        'sw' : None,
        'ne' : None,
        'se' : None,
        }
    corners_mercator = {
        'nw' : None,
        'sw' : None,
        'ne' : None,
        'se' : None,
        }
    
    PEN_RADIUS = 4
    COLOUR = QtCore.Qt.darkGreen
    
    def __init__(self, boundings):
        super().__init__()
        self.boundings_path = boundings
        
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        
        self.calculateNeededTiles(boundings)
        
        #self.bounds = self.scene().itemsBoundingRect()
    
    def calculateNeededTiles(self, boundings):
        tile_min_x, tile_max_y = self.degToTileNumber(boundings['lat_min'], boundings['lon_min'])
        
        tile_max_x, tile_min_y = self.degToTileNumber(boundings['lat_max'], boundings['lon_max'])
        
        print(tile_min_x, tile_max_x, tile_min_y, tile_max_y)
        
        #self.tileRange(tile_min_x, tile_max_x+1, tile_min_y, tile_max_y+1)
        self.bounds = QRectF(0, 0, (tile_max_x+1 - tile_min_x)*256, (tile_max_y+1 - tile_min_y)*256)
        print(self.bounds)
        
        self.download_thread = QDownloadMapTilesThread(self.zoom, tile_min_x, tile_max_x+1, tile_min_y, tile_max_y+1)
        self.download_thread.drawMapTile.connect(self.drawMapTile)
        self.download_thread.start()
        
        self.calculateCorners(tile_min_x, tile_max_x+1, tile_min_y, tile_max_y+1)
    
    def calculateCorners(self, x_min, x_max, y_min, y_max):
        self.corners['nw'] = self.tileNumberToDeg(x_min, y_min)
        self.corners['ne'] = self.tileNumberToDeg(x_min, y_max+1)
        self.corners['sw'] = self.tileNumberToDeg(x_max+1, y_min)
        self.corners['se'] = self.tileNumberToDeg(x_max+1, y_max+1)
        
        self.corners_mercator['nw'] = self.convertToWebMercator_(self.corners['nw'])
        self.corners_mercator['ne'] = self.convertToWebMercator_(self.corners['ne'])
        self.corners_mercator['sw'] = self.convertToWebMercator_(self.corners['sw'])
        self.corners_mercator['se'] = self.convertToWebMercator_(self.corners['se'])
    
    
    
    def drawMapTile(self, pixmap, pos_x, pos_y):
        tile_size = 256
        #pixmap = pixmap.scaled(tile_size, tile_size, QtCore.Qt.KeepAspectRatio)
        
        item = self.scene().addPixmap(pixmap)
        item.setPos(pos_y*tile_size, pos_x*tile_size)
        item.setZValue(-10)
    
    def degToTileNumber(self, lat_deg, lon_deg):
        """ source: http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#X_and_Y """
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** self.zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (xtile, ytile)
    
    def tileNumberToDeg(self, xtile, ytile):
        """ source: http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#X_and_Y """
        """ this will return the nw-corner of the tile """
        n = 2.0 ** self.zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return (lat_deg, lon_deg)
    
    def addPoint(self, point_x, point_y):
        point_x, point_y = self.convertCoords(point_x, point_y)
        
        #pos = QtCore.QPointF(self.mapToScene(point_x, point_y*-1))
        pos = QtCore.QPointF(point_x, point_y*-1)
        ellipseItem = QGraphicsEllipseItem(pos.x(), pos.y(), self.PEN_RADIUS, self.PEN_RADIUS)
        ellipseItem.setZValue(10)
        ellipseItem.setPen(QPen(self.COLOUR, QtCore.Qt.SolidPattern))
        ellipseItem.setBrush(self.COLOUR)
        
        self.scene().addItem(ellipseItem)
    
    def convertCoords(self, x, y):
        x, y = self.convertToWebMercator(y, x)
        
        delta_path_x = x - self.boundings_path['lon_min']
        delta_path_y = y - self.boundings_path['lat_min']
        print("\n")
        print("DELTA", delta_path_x, delta_path_y)
        print("SCENE BOUNDS", self.bounds.x(), self.bounds.y(), self.bounds.width(), self.bounds.height())
        print("CORNERS", self.corners_mercator)
        print("POINT", x, y)
        
        x = x - self.corners_mercator['nw'][0]
        y = y - self.corners_mercator['nw'][1]
        
        #aspect_ratio = self.bounds.width() / (self.corners_mercator['se'][0] - self.corners_mercator['nw'][0])
        #print("ASPECT RATIO", aspect_ratio)
        
        aspect_ratio = self.bounds.width() / (self.corners_mercator['se'][0] - self.corners_mercator['nw'][0])
        print("ASPECT RATIO", aspect_ratio)
        aspect_ratio = aspect_ratio + 0.0072
        x = x * aspect_ratio
        y = y * aspect_ratio
        
        return x, y
    
    def convertToWebMercator_(self, coords):
        return self.convertToWebMercator(coords[0], coords[1])
    
    def convertToWebMercator(self, lat, lon):
        # derived from the Java version explained here: http://wiki.openstreetmap.org/wiki/Mercator
        RADIUS = 6378137.0 # in meters on the equator
        
        lat = math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * RADIUS
        
        lon = math.radians(lon) * RADIUS
        
        return lon, lat
    
    """
    def convertToWebMercatorWithPyproj(self, pos):
        from pyproj import Proj, transform
        
        inProj = Proj(init='epsg:4326') # WGS-84, usually used by GPS
        outProj = Proj(init='epsg:3857') # web-mercator, used by virtually all major online map providers, including Google Maps, Bing Maps, OpenStreetMap, Mapquest, Esri, Mapbox, and many others
        longitude, latitude = transform(inProj, outProj, pos['longitude'], pos['latitude'])
        
        return longitude, latitude
    """
    
    def scaleViewToContents(self):
        bounds = self.scene().itemsBoundingRect()
        self.fitInView(bounds, Qt.KeepAspectRatio)


class QDownloadMapTilesThread(QThread):
    
    
    drawMapTile = pyqtSignal(object, float, float)
    
    def __init__(self, zoom, x_min, x_max, y_min, y_max):
        super().__init__()
        
        self.zoom = zoom
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
    
    def run(self):
        for i, x in enumerate(range(self.x_min, self.x_max)):
            #QApplication.processEvents()
            for j, y in enumerate(range(self.y_min, self.y_max)):
                #print(x, y, i, j)
                #print(self.x_min, self.x_max, self.y_min, self.y_max)
                self.fetchTile(x, y, j, i)
    
    def fetchTile(self, x, y, pos_x, pos_y):
        tile = urllib.request.urlopen("http://a.tile.openstreetmap.org/{0}/{1}/{2}.png".format(self.zoom, x, y))
        image = tile.read()
        
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image)
        self.drawMapTile.emit(pixmap, pos_x, pos_y)

from PyQt5.QtWidgets import QMainWindow

class QMapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.resize(500, 500)
        
        grid = QGridLayout()
        
        mapView = QMapView()
        grid.addWidget(mapView, 0, 0)
        
        self.setCentralWidget(mapView)

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    c = QMapWindow()
    c.show()
    sys.exit(app.exec_())
