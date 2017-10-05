
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGridLayout, QPushButton, QApplication
from PyQt5.QtGui import QPainter, QIcon
from PyQt5.QtCore import QRectF

import urllib.request
import queue

from QCustomizedWidgets.QCustomizedGraphicsView import QCustomizedGraphicsView

from modules.gps.convert_coordinates import ConvertCoordinates

from configs.configFiles import ConfigFile

# to make program closeable with ctr-c in terminal
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

TILE_SIZE = 256
class QMapWidget(QCustomizedGraphicsView):
    
    zoom = 10
    
    convert = ConvertCoordinates()
    
    tiles_matrix = {'x_min': None, 'x_max': None, 'y_min': None, 'y_max': None}
    
    def __init__(self):
        super().__init__()
        
        self.setRenderHint(QPainter.Antialiasing)
        
        self.addControlElements()
        self.startDownloadThread()
    
    def addControlElements(self):
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
    
    def startDownloadThread(self):
        self.download_queue = queue.Queue()
        
        self.download_thread = QDownloadMapTilesThread(self.download_queue, self.scene())#self.scene(), self.zoom, tile_min_x, tile_max_x, tile_min_y, tile_max_y, 'init')
        self.download_thread.drawMapTile.connect(self.__drawMapTile)
        self.download_thread.start()
    
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
    
    def calculateNeededTiles(self, lat_min, lat_max, lon_min, lon_max):
        x_min, y_max = self.convert.degToTileNumber(self.zoom, lat_min, lon_min)
        
        x_max, y_min = self.convert.degToTileNumber(self.zoom, lat_max, lon_max)
        
        x_max += 1
        y_max += 1
        
        self.scene_rect = QRectF(0, 0, (x_max - x_min)*TILE_SIZE, (y_max - y_min)*TILE_SIZE)
        
        self.download_queue.put({
            'zoom': self.zoom,
            'x_min': x_min,
            'x_max': x_max,
            'y_min': y_min,
            'y_max': y_max,
            'mode': 'init',
            })
        
        #self.corners_mercator = self.convert.calculateCorners(self.zoom, x_min, x_max, y_min, y_max)
    
    def showPosition(self):
        #self.calculateNeededTiles(51.476852, 51.476852, 0, 0})
        self.calculateNeededTiles(51, 52, -1, 1)
    
    def __drawMapTile(self, pixmap, pos_x, pos_y):
        item = self.scene().addPixmap(pixmap)
        #item.setPos(pos_x*TILE_SIZE, pos_y*TILE_SIZE)
        item.setPos(pos_x, pos_y)
        item.setZValue(-10)
    
    def scrollContentsBy(self, dx, dy):
        
        hor_cur = self.horizontalScrollBar().value()
        vert_cur = self.verticalScrollBar().value()
        
        hor_min = self.horizontalScrollBar().minimum()
        vert_min = self.verticalScrollBar().minimum()
        
        hor_max = self.horizontalScrollBar().maximum()
        vert_max = self.verticalScrollBar().maximum()
        
        if hor_cur <= hor_min: # + TILE_SIZE:
            self.download_queue.put({'mode': 'left'})
        
        elif hor_cur >= hor_max: # - TILE_SIZE:
            self.download_queue.put({'mode': 'right'})
        
        if vert_cur <= vert_min: # + TILE_SIZE:
            self.download_queue.put({'mode': 'top'})
        
        elif vert_cur >= vert_max: # - TILE_SIZE:
            self.download_queue.put({'mode': 'bottom'})
        
        super().scrollContentsBy(dx, dy)

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
import os, time
class QDownloadMapTilesThread(QThread):
    
    __stop = False
    drawMapTile = pyqtSignal(object, float, float)
    
    scene_rect = None
    tile_rect = None
    
    def __init__(self, queue, scene):
        super().__init__()
        
        self.queue = queue
        self.scene = scene
        
        config = ConfigFile()
        self.cache_path = config.readPath('cache', 'cachepath')
        self.cache_path = os.path.join(self.cache_path, 'maps')
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
    
    def run(self):
        while not self.__stop:
            if not self.queue.empty():
                item = self.queue.get()
                if item['mode'] == 'init':
                    print("INIT _-_______________________")
                    self.initialRun(item)
                
                elif item['mode'] == 'left':
                    #TODO
                    """
                    self.scene_rect = self.scene.itemsBoundingRect()
                    
                    x = self.tile_rect['x_min']-1
                    
                    x_pos = self.scene_rect.x()-1 * TILE_SIZE
                    
                    for j, y in enumerate(range(self.tile_rect['y_min'], self.tile_rect['y_max'])):
                        
                        y_pos = self.scene_rect.y()+j * TILE_SIZE
                        
                        self.fetchTile(self.tile_rect['zoom'], x, y, x_pos, y_pos)
                    
                    self.tile_rect['x_min'] = self.tile_rect['x_min'] -1
                    """
                    pass
                
                elif item['mode'] == 'right':
                    self.scene_rect = self.scene.itemsBoundingRect()
                    
                    x = self.tile_rect['x_max']
                    self.tile_rect['x_max'] = self.tile_rect['x_max'] +1
                    
                    x_pos = self.scene_rect.width()+0 * TILE_SIZE
                    
                    for j, y in enumerate(range(self.tile_rect['y_min'], self.tile_rect['y_max'])):
                        
                        y_pos = self.scene_rect.y()+j * TILE_SIZE
                        
                        self.fetchTile(self.tile_rect['zoom'], x, y, x_pos, y_pos)
                
                elif item['mode'] == 'top':
                    #self.scene_rect = self.scene.itemsBoundingRect()
                    pass
                    
                
                elif item['mode'] == 'bottom':
                    self.scene_rect = self.scene.itemsBoundingRect()
                    
                    y = self.tile_rect['y_max']
                    self.tile_rect['y_max'] = self.tile_rect['y_max'] +1
                    
                    y_pos = self.scene_rect.height()+0 * TILE_SIZE
                    
                    for i, x in enumerate(range(self.tile_rect['x_min'], self.tile_rect['x_max'])):
                        
                        x_pos = self.scene_rect.x()+i * TILE_SIZE
                        
                        self.fetchTile(self.tile_rect['zoom'], x, y, x_pos, y_pos)
            
            time.sleep(0.001)
    
    def initialRun(self, item):
        self.tile_rect = item
        
        for i, x in enumerate(range(item['x_min'], item['x_max'])):
            if self.__stop:
                break
            QApplication.processEvents()
            for j, y in enumerate(range(item['y_min'], item['y_max'])):
                if self.__stop:
                    break
                QApplication.processEvents()
                self.fetchTile(item['zoom'], x, y, i*TILE_SIZE, j*TILE_SIZE)
    
    def fetchTile(self, zoom, x, y, pos_x, pos_y):
        pixmap = QPixmap()
        
        image_filename = os.path.join(self.cache_path, str(zoom)+'_'+str(x)+'_'+str(y)+'.png')
        
        if not os.path.exists(image_filename):
            tile = urllib.request.urlopen("http://a.tile.openstreetmap.org/{0}/{1}/{2}.png".format(zoom, x, y))
            
            image = tile.read()
            pixmap.loadFromData(image)
            
            with open(image_filename, 'bw') as binary:
                binary.write(image)
        
        else:
            pixmap.load(image_filename)
        
        self.drawMapTile.emit(pixmap, pos_x, pos_y)
    
    def stop(self):
        self.__stop = True

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QMainWindow
    import sys
    app = QApplication(sys.argv)
    win = QMainWindow()
    c = QMapWidget()
    win.setCentralWidget(c)
    win.resize(500, 500)
    win.show()
    sys.exit(app.exec_())
