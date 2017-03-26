
from PyQt5.QtWidgets import QAction, qApp
from PyQt5.QtGui import QIcon

import os

class MenuBar(object):
    def __init__(self, context):
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
        
        module_menus = self.loadModuleMenus(context, menubar)
        
    def loadModuleMenus(self, context, menubar):
        menues_list = []
        base, dirs, files = next(iter(os.walk('./modules')))
        dirs.sort()
        
        for d in dirs:
            if d == "__pycache__":
                continue
            
            imports = "from modules."+d+".menu import Menu as Menu"
            print(imports)
            try:
                exec(imports, globals())
            except ModuleNotFoundError as e:
                print("Module not found:", e)
            else:
                current_menu = Menu(context, menubar)
                menues_list.append(current_menu)
                
        
