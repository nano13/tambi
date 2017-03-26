
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon
 
class MenuBar(object):
    def __init__(self, context):
        self.addMenu(context)
        
    def addMenu(self, context):
        exitAction = QAction(QIcon.fromTheme("application-exit"), "&Exit", context)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        
        newCliTabAction = QAction(QIcon.fromTheme('utilities-terminal'), '&New Command Line Tab', context)
        newCliTabAction.setShortcut('Ctrl+T')
        newCliTabAction.setStatusTip('Open new CLI Tab')
        newCliTabAction.triggered.connect(context.addNewCliTab)
        
        newVocableTabAction = QAction(QIcon.fromTheme('input-tablet'), '&New Vocable Tab', context)
        newVocableTabAction.setShortcut('Ctrl+L')
        newVocableTabAction.setStatusTip('Open new Vocable Tab')
        newVocableTabAction.triggered.connect(context.addNewVocableTab)
        
        openFileAction = QAction(QIcon.fromTheme('document-open'), '&Open File', context)
        openFileAction.setStatusTip('Open a File')
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.triggered.connect(context.openFile)
        
        menubar = context.menuBar()
        
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newCliTabAction)
        fileMenu.addAction(newVocableTabAction)
        fileMenu.addSeparator()
        fileMenu.addAction(openFileAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
