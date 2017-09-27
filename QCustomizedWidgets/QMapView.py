
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGridLayout, QWidget, QGraphicsEllipseItem, QPushButton, QApplication
from PyQt5.QtGui import QPen, QPainter, QIcon
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QRectF

from configs.configFiles import ConfigFile

import urllib.request
import _thread, os

from modules.gps.convert_coordinates import ConvertCoordinates

class QMapView(QGraphicsView):
    
    convert = ConvertCoordinates()
    
    zoom = 16
    #zoom = 10
    boundings_path = None
    bounds = None
    download_thread = None
    
    corners_mercator = None
    
    point_list = []
    last_mouse_pos = None
    
    PEN_RADIUS = 4
    COLOUR = QtCore.Qt.darkRed

    def __init__(self, boundings):
        super().__init__()
        self.boundings_path = boundings
        
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        
        config = ConfigFile()
        self.cache_path = config.readPath('cache', 'cachepath')
        self.cache_path = os.path.join(self.cache_path, 'maps')
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        
        self.calculateNeededTiles(boundings)

        #self.scene_rect = self.scene().itemsBoundingRect()
        
        grid = QGridLayout()
        grid.setRowStretch(0, 10000)
        grid.setColumnStretch(0, 10000)
        self.setLayout(grid)
        
        zoom_in_button = QPushButton()
        zoom_in_button.setIcon(QIcon.fromTheme('zoom-in'))
        zoom_in_button.setMaximumSize(25, 25)
        grid.addWidget(zoom_in_button, 1, 1)
        zoom_in_button.clicked.connect(self.zoomInClicked)
        
        zoom_out_button = QPushButton()
        zoom_out_button.setIcon(QIcon.fromTheme('zoom-out'))
        zoom_out_button.setMaximumSize(25, 25)
        grid.addWidget(zoom_out_button, 2, 1)
        zoom_out_button.clicked.connect(self.zoomOutClicked)
        
    def zoomInClicked(self):
        if self.download_thread:
            self.download_thread.stop()
        
        if self.zoom < 19:
            self.zoom += 1
        self.scene().clear()
        """ because this seems to be the best way to shrink the scene again: """
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        
        self.calculateNeededTiles(self.boundings_path)
        self.drawPointList()
    
    def zoomOutClicked(self):
        if self.download_thread:
            self.download_thread.stop()
        
        if self.zoom > 0:
            self.zoom -= 1
        self.scene().clear()
        self.items().clear()
        
        """ because this seems to be the best way to shrink the scene again: """
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        
        self.calculateNeededTiles(self.boundings_path)
        self.drawPointList()

    def calculateNeededTiles(self, boundings):
        tile_min_x, tile_max_y = self.convert.degToTileNumber(self.zoom, boundings['lat_min'], boundings['lon_min'])
        
        tile_max_x, tile_min_y = self.convert.degToTileNumber(self.zoom, boundings['lat_max'], boundings['lon_max'])
        
        tile_max_x += 1
        tile_max_y += 1
        
        self.scene_rect = QRectF(0, 0, (tile_max_x - tile_min_x)*256, (tile_max_y - tile_min_y)*256)
        print(self.scene_rect)
        
        self.download_thread = QDownloadMapTilesThread(self.cache_path, self.zoom, tile_min_x, tile_max_x, tile_min_y, tile_max_y)
        self.download_thread.drawMapTile.connect(self.drawMapTile)
        self.download_thread.start()
        
        self.corners_mercator = self.convert.calculateCorners(self.zoom, tile_min_x, tile_max_x, tile_min_y, tile_max_y)
    
    def drawMapTile(self, pixmap, pos_x, pos_y):
        tile_size = 256
        #pixmap = pixmap.scaled(tile_size, tile_size, QtCore.Qt.KeepAspectRatio)

        item = self.scene().addPixmap(pixmap)
        item.setPos(pos_y*tile_size, pos_x*tile_size)
        print("POS", item.pos(), pos_y*tile_size, pos_x*tile_size)
        item.setZValue(-10)
    
    def addPointList(self, point_list):
        self.point_list = point_list
    
    def drawPointList(self):
        self.draw_point_list_thread = QAddPointListThread(self.point_list)
        self.draw_point_list_thread.addPoint.connect(self.addPoint)
        self.draw_point_list_thread.start()
    
    """
    adds a point marker specified by gps-coordinates to the canvas
    """
    def addPoint(self, point_x, point_y):
        print("addPoint", point_x, point_y)
        point_x, point_y = self.convert.convertGeoToCanvas(self.scene_rect, point_x, point_y)
        #point_x, point_y = self.convertToCanvas(point_x, point_y)
        
        ellipseItem = QGraphicsEllipseItem(point_x + self.PEN_RADIUS / 2, point_y + self.PEN_RADIUS / 2, self.PEN_RADIUS, self.PEN_RADIUS)
        ellipseItem.setZValue(10)
        ellipseItem.setPen(QPen(self.COLOUR, QtCore.Qt.SolidPattern))
        ellipseItem.setBrush(self.COLOUR)
        
        self.scene().addItem(ellipseItem)
    
    def convertToCanvas(self, x, y):
        x, y = self.convert.convertDegToWebMercator(y, x)
        
        delta_path_x = x - self.boundings_path['lon_min']
        delta_path_y = y - self.boundings_path['lat_min']
        
        
        print("\n")
        print("DELTA", delta_path_x, delta_path_y)
        print("SCENE BOUNDS", self.scene_rect.x(), self.scene_rect.y(), self.scene_rect.width(), self.scene_rect.height())
        print("CORNERS", self.corners_mercator)
        print("POINT", x, y)
        
        
        x = x - self.corners_mercator['nw'][0]
        y = y - self.corners_mercator['nw'][1]
        
        #aspect_ratio = self.scene_rect.width() / (self.corners_mercator['se'][0] - self.corners_mercator['nw'][0])
        #print("ASPECT RATIO", aspect_ratio)
        
        aspect_ratio = self.scene_rect.width() / (self.corners_mercator['se'][0] - self.corners_mercator['nw'][0])
        print("ASPECT RATIO", aspect_ratio)
        x = x * aspect_ratio
        y = y * aspect_ratio
        
        return x, y
    
    
    
    
    
    def scaleViewToContents(self):
        bounds = self.scene().itemsBoundingRect()
        self.fitInView(bounds, Qt.KeepAspectRatio)
    
    def mousePressEvent(self, event):
        button = event.buttons()
        if button == Qt.LeftButton:
            self.last_mouse_pos = event.pos()
        elif button == Qt.RightButton:
            #print(event.pos())
            print(self.mapToScene(event.pos()))
        elif button == Qt.MidButton:
            mapped = self.mapToScene(event.pos().x(), event.pos().y())
            x = mapped.x()
            y = mapped.y()
            geo = self.convert.convertCanvasToGeo(self.scene_rect, x, y)
            print(geo[0], geo[1])
            print(self.scene().itemsBoundingRect())
    
    def mouseMoveEvent(self, event):
        vert = self.verticalScrollBar().value()
        hor = self.horizontalScrollBar().value()
        
        button = event.buttons()
        if button == Qt.LeftButton and self.last_mouse_pos:
            delta_x = self.last_mouse_pos.x() - event.x()
            new_x = hor + delta_x
            
            delta_y = self.last_mouse_pos.y() - event.y()
            new_y = vert + delta_y
            
            self.horizontalScrollBar().setValue(new_x)
            self.verticalScrollBar().setValue(new_y)
        
        self.last_mouse_pos = event.pos()
    

class QDownloadMapTilesThread(QThread):
    
    __stop = False
    drawMapTile = pyqtSignal(object, float, float)
    
    def __init__(self, cache_path, zoom, x_min, x_max, y_min, y_max):
        super().__init__()
        
        self.cache_path = cache_path
        self.zoom = zoom
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
    
    def run(self):
        for i, x in enumerate(range(self.x_min, self.x_max)):
            if self.__stop:
                break
            QApplication.processEvents()
            for j, y in enumerate(range(self.y_min, self.y_max)):
                if self.__stop:
                    break
                QApplication.processEvents()
                #print(x, y, i, j)
                #print(self.x_min, self.x_max, self.y_min, self.y_max)
                self.fetchTile(x, y, j, i)
    
    def fetchTile(self, x, y, pos_x, pos_y):
        pixmap = QtGui.QPixmap()
        
        image_filename = os.path.join(self.cache_path, str(self.zoom)+'_'+str(x)+'_'+str(y)+'.png')
        if not os.path.exists(image_filename):
            tile = urllib.request.urlopen("http://a.tile.openstreetmap.org/{0}/{1}/{2}.png".format(self.zoom, x, y))
            
            """ for google: max-zoom-level: 22
            h = roads only
            m = standard roadmap
            p = terrain
            r = somehow altered roadmap
            s = satellite only
            t = terrain only
            y = hybrid
            """
            #tile = urllib.request.urlopen("http://mt.google.com/vt/lyrs=s&x={0}&y={1}&z={2}".format(x, y, self.zoom))
            #image_filename = os.path.join(self.cache_path, str(self.zoom)+'_'+str(x)+'_'+str(y)+'.jpg')
            
            image = tile.read()
            pixmap.loadFromData(image)
            
            with open(image_filename, 'bw') as _b:
                _b.write(image)
        else:
            pixmap.load(image_filename)
        
        self.drawMapTile.emit(pixmap, pos_x, pos_y)
    
    def stop(self):
        self.__stop = True

class QAddPointListThread(QThread):
    
    __stop = False
    point_list = []
    addPoint = pyqtSignal(float, float)
    
    def __init__(self, point_list):
        super().__init__()
        self.point_list = point_list
    
    def run(self):
        for point in self.point_list:
            QApplication.processEvents()
            if self.__stop:
                break
            self.addPoint.emit(point[0], point[1])
    
    def stop(self):
        self.__stop = True
