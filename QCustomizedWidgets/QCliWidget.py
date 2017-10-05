
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QGraphicsScene, QGraphicsView, QLabel, QFileDialog
#from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtGui import QIcon, QTextFormat, QPixmap, QImage, QPainter, QMovie
from PyQt5.QtCore import QRect, QRectF, Qt, QSize, pyqtSignal
from PyQt5.QtChart import QChart, QXYSeries, QLineSeries#, QChartView

from QCustomizedWidgets.QInputLine import QInputLine
from QCustomizedWidgets.QItemizedWidget import QItemizedWidget
from QCustomizedWidgets.QVirtualKeyboardWindow import QVirtualKeyboardWindow
from QCustomizedWidgets.QBeamerWindow import QBeamerWindow
from QCustomizedWidgets.QChartViewEnhanced import QChartViewEnhanced
from QCustomizedWidgets.QDeckOverviewWidget import QAudioItems
from QCustomizedWidgets.QTextEditEnhanced import QTextEditEnhanced
from QCustomizedWidgets.QCustomizedGraphicsView import QCustomizedGraphicsView
from QCustomizedWidgets.QMapWidget import QMapWidget

from interpreter.interpreter import Interpreter
from interpreter.exceptions import ClearCalled, SnapshotCalled
from interpreter.structs import Result

from misc.unicodeFonts import UnicodeFonts
from configs.configFiles import ConfigFile

from functools import partial
from os import path
import queue

SCALE_FACTOR = 1.15

class QCliWidget(QWidget):
    
    interpreter = Interpreter()
    display_widget = None
    vkbd = None
    beamer = None
    
    result_from_queue = False
    
    set_tab_text = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        self.unicode_fonts = UnicodeFonts()
        
        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 6)
        self.setLayout(self.grid)
        
        self.display_widget = QTextEditEnhanced()
        self.display_widget.setText("type in the command 'man' for getting started ...")
        self.display_widget.setReadOnly(True)
        
        self.addDisplayWidget()
        
        line = QInputLine()
        line.return_pressed.connect(self.commandEntered)
        self.grid.addWidget(line, 1, 0)
        
        vkbdButton = QPushButton(self)
        vkbdButton.clicked.connect(partial(self.vkbdButtonClicked, line))
        vkbdButton.setIcon(QIcon.fromTheme('input-keyboard'))
        self.grid.addWidget(vkbdButton, 1, 1)
        
        zoomInButton = QPushButton(self)
        zoomInButton.setIcon(QIcon.fromTheme('zoom-in'))
        zoomInButton.clicked.connect(self.onZoomInClicked)
        self.grid.addWidget(zoomInButton, 1, 4)
        
        zoomOutButton = QPushButton(self)
        zoomOutButton.setIcon(QIcon.fromTheme('zoom-out'))
        zoomOutButton.clicked.connect(self.onZoomOutClicked)
        self.grid.addWidget(zoomOutButton, 1, 2)
        
        zoomResetButton = QPushButton(self)
        zoomResetButton.setIcon(QIcon.fromTheme('zoom-original'))
        zoomResetButton.clicked.connect(self.onZoomResetClicked)
        self.grid.addWidget(zoomResetButton, 1, 3)
        
        self.applyStylesheet()
    
    def applyStylesheet(self):
        config = ConfigFile()
        path = config.readVar('global', 'stylesheet')
        stylesheet = ''
        try:
            with open(path) as css:
                for line in css:
                    stylesheet += line
            
            self.display_widget.setStyleSheet(stylesheet)
        except FileNotFoundError:
            pass
    
    def addDisplayWidget(self):
        #self.grid.addWidget(self.display_widget, 0, 0, 1, 0)
        
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        
        self.scene.addWidget(self.display_widget)
        self.view.setScene(self.scene)
        self.view.setStyleSheet("QGraphicsView { border-style: none; }")
        
        self.grid.addWidget(self.view, 0, 0, 1, 0)
        
        self.resizeDisplayWidget()
        
        self.applyStylesheet()
        
    def resizeDisplayWidget(self):
        x = self.view.width() -2.1
        y = self.view.height() -2.1
        self.x, self.y = x, y
        
        mapped_rect = self.view.mapToScene(QRect(0, 0, x, y)).boundingRect()
        
        self.display_widget.setFixedSize(mapped_rect.width(), mapped_rect.height())
        self.scene.setSceneRect(0, 0, mapped_rect.width(), mapped_rect.height())
        
        #self.display_widget.setFixedSize(x, y)
        #self.scene.setSceneRect(0, 0, x, y)
    
    def resizeEvent(self, event):
        #super().resizeEvent(event)
        self.resizeDisplayWidget()
    
    def vkbdButtonClicked(self, lineEdit):
        self.vkbd = QVirtualKeyboardWindow()
        self.vkbd.setLineEdit(lineEdit)
    
    def commandEntered(self, command):
        # to keep the display_widget in the correct size
        self.resize(self.x, self.y)
        
        print("command:", command)
        if '|' in command:
            command, pipe = command.split('|')
            self.handleCommand(command)
            
            pipe = pipe.strip()
            if pipe == 'beamer':
                if self.beamer:
                    self.beamer.destroy()
                    print('destroyed!!!')
                
                self.beamer = QBeamerWindow()
                
                from PyQt5.QtWidgets import QLabel, QPushButton
                widget = QLabel('blaaaa')
                
                self.beamer.setWidget(self.display_widget)
                #self.beamer.setText('test')
                self.beamer.routeToScreen()
                self.beamer.showFullScreen()
        else:
            #self.handleCommand(command)
            self.set_tab_text.emit(command)
            
            #self.activityIndicator()
            
            q = queue.Queue()
            
            self.interpreter_thread = HandleCommandThread(command, q)
            self.interpreter_thread.processResult.connect(self.processResult)
            self.interpreter_thread.clearDisplayWidget.connect(self.clearDisplayWidget)
            self.interpreter_thread.makeSnapshot.connect(self.makeSnapshot)
            self.interpreter_thread.stopQueueListener.connect(self.stopQueueListener)
            self.interpreter_thread.start()
            
            self.queue_thread = GetQueueItemsThread(q)
            self.queue_thread.processQueueItem.connect(self.processQueueItem)
            self.queue_thread.start()
    
    def stopQueueListener(self):
        self.queue_thread.stop()
    
    def processQueueItem(self, item):
        self.result_from_queue = True
        
        result_object = Result()
        result_object.payload = item.getItem()
        self.resultInTextEdit(result_object)
    
    def processResult(self, result):
        if self.result_from_queue:
            self.result_from_queue = False
        
        else:
            if hasattr(result, 'payload') and result.payload:
                if hasattr(result, 'error') and result.error:
                    self.showErrorMessage(result.error)
                elif result is None:
                    self.showErrorMessage('no result found')
                elif hasattr(result, 'category') and result.category == "table":
                    try:
                        result.payload[0]
                    except IndexError:
                        pass # datastructure does not fit to display type 'table'
                    else:
                        self.resultInTable(result)
                
                elif hasattr(result, 'category') and result.category == "multimedia_table":
                    self.resultInMultimediaTable(result)
                
                elif hasattr(result, 'category') and result.category == "list":
                    self.resultInTextEdit(result)
                
                elif hasattr(result, 'category') and result.category == "text":
                    self.resultInTextEdit(result)
                
                elif hasattr(result, 'category') and result.category == "string":
                    self.resultInTextEdit(result)
                
                elif hasattr(result, 'category') and result.category == "itemized":
                    self.resultInItemizedWidget(result)
                
                elif hasattr(result, 'category') and result.category == "image":
                    self.resultInImageWidget(result)
                
                elif hasattr(result, 'category') and result.category == "html":
                    #self.resultInHTMLWidget(result)
                    self.resultInTextEdit(result)
                
                elif hasattr(result, 'category') and result.category == 'diagram':
                    self.resultInDiagram(result)
                
                elif hasattr(result, 'category') and result.category == 'command':
                    self.showMapWidget()
                
            else:
                result = Result()
                result.payload = 'empty result set'
                self.resultInTextEdit(result)
        
    
    def activityIndicator(self):
        self.display_widget.deleteLater()
        
        label = QLabel()
        movie = QMovie('./assets/images/activity_indicator.gif')
        movie.start()
        label.setMovie(movie)
        
        self.display_widget = QWidget()
        layout = QVBoxLayout()
        self.display_widget.setLayout(layout)
        layout.addWidget(label, Qt.AlignCenter)
        
        self.addDisplayWidget()
    
    def clearDisplayWidget(self):
        self.display_widget.deleteLater()
        self.display_widget = QTextEditEnhanced()
        self.display_widget.setReadOnly(True)
        self.addDisplayWidget()
    
    def makeSnapshot(self):
        image = QImage(self.display_widget.size(), QImage.Format_ARGB32)
        painter = QPainter(image)
        
        if painter.isActive():
            self.render(painter)
        
        painter.end()
        
        default_dir = path.join(path.expanduser('~'))
        filename = QFileDialog.getSaveFileName(self, 'Save Snapshot', default_dir)
        
        image.save(filename[0])
    
    def resultInTable(self, result):
        self.display_widget.deleteLater()
        self.display_widget = QTableWidget()
        self.display_widget.setRowCount(len(result.payload))
        self.display_widget.setColumnCount(len(result.payload[0]))
        
        try:
            self.display_widget.setHorizontalHeaderLabels(result.header)
        except TypeError:
            pass
        try:
            self.display_widget.setVerticalHeaderLabels(result.header_left)
        except TypeError:
            pass
        
        for row, line in enumerate(result.payload):
            for column, item in enumerate(line):
                table_item = QTableWidgetItem(str(item))
                table_item.setFlags(Qt.ItemIsEnabled)
                self.unicode_fonts.applyFontToQWidget(str(item), table_item)
                self.display_widget.setItem(row, column, table_item)
        
        self.display_widget.resizeColumnsToContents()
        self.addDisplayWidget()
    
    def resultInMultimediaTable(self, result):
        self.display_widget.deleteLater()
        
        max_length = 0
        for line in result.payload:
            if len(line) > max_length:
                max_length = len(line)
        
        self.display_widget = QTableWidget()
        self.display_widget.setRowCount(len(result.payload))
        self.display_widget.setColumnCount(max_length)
        
        audio_count = 0
        config = ConfigFile()
        deckpath = config.readPath("vocable", "deckpath")
        for row, line in enumerate(result.payload):
            deckname = line[0]
            for column, item in enumerate(line):
                if self.isImage(str(item)):
                    pixmap = QPixmap()
                    pixmap.load(path.join(deckpath, deckname, str(item)))
                    pixmap = pixmap.scaled(QSize(60, 30), Qt.KeepAspectRatio)
                    image_widget = QLabel()
                    image_widget.setPixmap(pixmap)
                    self.display_widget.setCellWidget(row, column, image_widget)
                elif self.isAudio(str(item)):
                    splitted = item.split(',')
                    if audio_count < len(splitted):
                        audio_count = len(splitted)
                    audio_widget = QAudioItems(path.join(deckpath, deckname), self.display_widget, 7, max_length)
                    audio_widget.appendPlayButtonsList(splitted, row)
                else:
                    table_item = QTableWidgetItem(str(item))
                    table_item.setFlags(Qt.ItemIsEnabled)
                    #self.unicode_fonts.applyFontToQWidget(str(item), table_item)
                    self.display_widget.setItem(row, column, table_item)
        
        self.display_widget.setColumnCount(max_length + audio_count)
        self.display_widget.resizeColumnsToContents()
        self.addDisplayWidget()
    
    def resultInTextEdit(self, result):
        self.display_widget.deleteLater()
        self.display_widget = QTextEditEnhanced()
        
        self.unicode_fonts.applyFontAndSizeToQWidget(result.toString(), self.display_widget)
        
        self.display_widget.setAcceptRichText(True)
        
        self.display_widget.setText(result.toString())
        self.display_widget.setReadOnly(True)
        self.addDisplayWidget()
        
    def resultInHTMLWidget(self, result):
        self.display_widget.deleteLater()
        self.display_widget = QWebView()
        
        self.display_widget.setHtml(result.payload)
        self.addDisplayWidget()
    
    def resultInItemizedWidget(self, result):
        self.display_widget.deleteLater()
        self.display_widget = QItemizedWidget(result.payload)
        self.addDisplayWidget()
    
    def resultInImageWidget(self, result):
        self.display_widget.deleteLater()
        
        self.display_widget = QCustomizedGraphicsView()
        
        import PIL
        if type(result.payload) == PIL.Image.Image:
            from PIL.ImageQt import ImageQt
            qimage = ImageQt(result.payload)
            pixmap = QPixmap.fromImage(qimage)
        
        #pixmap = QPixmap("/tmp/tmprp3q0gi9.PNG")
        #pixmap.fromImage(image)
        
        item = self.display_widget.scene().addPixmap(pixmap)
        item.setPos(0, 0)
        self.addDisplayWidget()
    
    def resultInDiagram(self, result):
        self.display_widget.deleteLater()
        
        curve = QLineSeries()
        pen = curve.pen()
        pen.setColor(Qt.red)
        pen.setWidthF(2)
        curve.setPen(pen)
        
        for data in result.payload:
            if type(data['y']) == str:
                data['y'] = 0
            curve.append(data['x'], data['y'], 10)
        
        chart = QChart()
        chart.setTitle(result.name)
        chart.legend().hide()
        chart.addSeries(curve)
        chart.createDefaultAxes()
        
        view = QChartViewEnhanced(chart)
        view.setRenderHint(QPainter.Antialiasing)
        self.display_widget = view
        self.addDisplayWidget()
    
    def showMapWidget(self):
        self.display_widget.deleteLater()
        
        self.display_widget = QMapWidget()
        self.display_widget.showPosition()
        
        self.addDisplayWidget()
    
    def showErrorMessage(self, message):
        self.display_widget.deleteLater()
        self.display_widget = QTextEditEnhanced()
        self.display_widget.setText(message)
        self.display_widget.setReadOnly(True)
        self.addDisplayWidget()
    
    def onZoomInClicked(self):
        if type(self.display_widget) == QTextEditEnhanced:
            self.display_widget.zoomIn()
        elif type(self.display_widget) == QChartViewEnhanced:
            self.display_widget.chart().zoomIn()
        else:
            self.view.scale(SCALE_FACTOR, SCALE_FACTOR)
            self.resizeDisplayWidget()
    
    def onZoomOutClicked(self):
        if type(self.display_widget) == QTextEditEnhanced:
            self.display_widget.zoomOut()
        elif type(self.display_widget) == QChartViewEnhanced:
            self.display_widget.chart().zoomOut()
        else:
            self.view.scale(1 / SCALE_FACTOR, 1 / SCALE_FACTOR)
            self.resizeDisplayWidget()
    
    def onZoomResetClicked(self):
        if type(self.display_widget) == QTextEditEnhanced:
            self.display_widget.zoomReset()
        elif type(self.display_widget) == QChartViewEnhanced:
            self.display_widget.chart().zoomReset()
        else:
            self.view.resetTransform()
            self.resizeDisplayWidget()
    
    def keyPressEvent(self, event):
        if (event.modifiers() & Qt.ControlModifier):
            if event.key() == Qt.Key_Plus:
                self.onZoomInClicked()
            
            elif event.key() == Qt.Key_Minus:
                self.onZoomOutClicked()
    
    def isImage(self, data):
        suffixes = ['.png', '.jpg', '.jpe', '.jpeg', '.svg', '.bmp']
        for suffix in suffixes:
            if data.lower().endswith(suffix):
                return True
        return False
    
    def isAudio(self, data):
        suffixes = ['.ogg', '.wav', '.mp3', '.aiff', '.wma']
        for suffix in suffixes:
            if data.lower().endswith(suffix):
                return True
        return False
    

from PyQt5.QtCore import QThread, pyqtSignal
class HandleCommandThread(QThread):
    
    processResult = pyqtSignal(object)
    clearDisplayWidget = pyqtSignal()
    makeSnapshot = pyqtSignal()
    
    stopQueueListener = pyqtSignal()
    
    interpreter = Interpreter()
    
    def __init__(self, command, queue):
        super().__init__()
        self.command = command
        self.queue = queue
    
    def run(self):
        try:
            result = self.interpreter.interpreter(self.command, self.queue)
        except ClearCalled:
            self.stopQueueListener.emit()
            self.clearDisplayWidget.emit()
        except SnapshotCalled:
            self.stopQueueListener.emit()
            self.makeSnapshot.emit()
        else:
            self.stopQueueListener.emit()
            self.processResult.emit(result)

class GetQueueItemsThread(QThread):
    
    __stop = False
    processQueueItem = pyqtSignal(object)
    
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
    
    def run(self):
        while not self.__stop:
            if not self.queue.empty():
                item = QueueItem(self.queue.get())
                self.processQueueItem.emit(item)
    
    def stop(self):
        self.__stop = True

class QueueItem(object):
    def __init__(self, item):
        self.item = item
    
    def getItem(self):
        return self.item
