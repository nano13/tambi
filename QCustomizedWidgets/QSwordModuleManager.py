
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QGridLayout, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from modules.sword.sword_module_manager.sword_module_manager import SwordModuleManager

INSTALLED_MODULES = '[Installed]'

class QSwordModuleManager(QWidget):
    
    data = None
    
    def __init__(self):
        super().__init__()
        
        self.module_manager_thread = SwordModuleManagerThread()
        self.module_manager_thread.download_modules_lists_finished.connect(self.downloadModulesListsFinished)
        self.module_manager_thread.download_module_finished.connect(self.reloadDataAndView)
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        self.addTreeWidget()
        
        ok_button = QPushButton('apply changes')
        cancel_button = QPushButton('revert changes')
        ok_button.clicked.connect(self.okButtonClicked)
        cancel_button.clicked.connect(self.canchelButtonClicked)
        self.layout.addWidget(ok_button, 1, 0)
        self.layout.addWidget(cancel_button, 1, 1)
    
    def addTreeWidget(self):
        self.tree = QTreeWidget()
        self.tree.itemExpanded.connect(self.expanded)
        self.tree.itemSelectionChanged.connect(self.itemSelectionChanged)
        self.layout.addWidget(self.tree, 0, 0, 1, 0)
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['module', 'description'])
        
        self.addRemoteModules()
    
    def downloadModulesListsFinished(self, modules_lists):
        self.data = modules_lists
        
        self.addRemoteModules()
        
        self.tree.deleteLater()
        self.addTreeWidget()
    
    def addRemoteModules(self):
        if not self.data:
            self.module_manager_thread.setAction(SwordModuleManagerAction.download_list)
            self.module_manager_thread.start()
        
        else:
            for repo_name in sorted(self.data):
                parent = QTreeWidgetItem(self.tree)
                if repo_name is not 'local':
                    parent.setText(0, repo_name)
                else:
                    parent.setText(0, INSTALLED_MODULES)
                parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                
                for language in sorted(self.data[repo_name]['modules']):
                    child = QTreeWidgetItem(parent)
                    child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                    child.setText(0, language)
                    
                    for module in self.data[repo_name]['modules'][language]:
                        grandchild = QTreeWidgetItem(child)
                        grandchild.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                        grandchild.setText(0, module['name'])
                        grandchild.setText(1, module['description'])
                        if repo_name is not 'local':
                            grandchild.setCheckState(0, Qt.Unchecked)
                        else:
                            grandchild.setCheckState(0, Qt.Checked)
            self.tree.resizeColumnToContents(0)
    
    def itemSelectionChanged(self):
        print(self.tree.selectedItems())
    
    def expanded(self):
        self.tree.resizeColumnToContents(0)
    
    def okButtonClicked(self):
        modules_to_process = {'delete': [], 'install': []}
        
        iterator = QTreeWidgetItemIterator(self.tree)
        
        item = iterator.value()
        while item is not None:
            if item.parent() is not None:
                if item.parent().parent() is not None:
                    # handle the installed modules to delete
                    repo_name = item.parent().parent().text(0)
                    if repo_name == INSTALLED_MODULES:
                        if item.checkState(0) == Qt.Unchecked:
                            modules_to_process['delete'].append(item.text(0))
                    # handle the remote modules to install
                    else:
                        if item.checkState(0) == Qt.Checked:
                            item_dict = {
                                'name': item.text(0),
                                'repository': repo_name,
                            }
                            modules_to_process['install'].append(item_dict)
            iterator += 1
            item = iterator.value()
        
        self.installAndUninstallModules(modules_to_process)
    
    def canchelButtonClicked(self):
        self.tree.deleteLater()
        self.addTreeWidget()
    
    def installAndUninstallModules(self, modules_to_process):
        for module in modules_to_process['delete']:
            module_manager = SwordModuleManager()
            module_manager.deleteModule(module)
            
            self.reloadDataAndView()
        
        for module in modules_to_process['install']:
            self.module_manager_thread.setAction(SwordModuleManagerAction.download_module)
            self.module_manager_thread.setArgs([module['repository'], module['name']])
            self.module_manager_thread.start()
    
    def reloadDataAndView(self):
        self.module_manager_thread.setAction(SwordModuleManagerAction.download_list)
        self.module_manager_thread.start()
    

class SwordModuleManagerThread(QThread):
    
    action = None
    args = None
    
    module_manager = SwordModuleManager()
    
    download_modules_lists_finished = pyqtSignal(object)
    download_module_finished = pyqtSignal()
    
    def __init_(self):
        super().__init__()
    """
    def start(self, args):
        self.args = args
        super().start()
    """
    def run(self):
        if self.action == SwordModuleManagerAction.download_list:
            modules_lists = self.module_manager.downloadModulesLists()
            self.download_modules_lists_finished.emit(modules_lists)
        
        elif self.action == SwordModuleManagerAction.download_module:
            if len(self.args) == 2:
                self.module_manager.downloadModuleFromRepository(self.args[0], self.args[1])
                self.download_module_finished.emit()
        
        elif self.action == SwordModuleManagerAction.delete_module:
            if args:
                self.module_manager.deleteModule(self.args)
    
    def setAction(self, action):
        self.action = action
    
    def setArgs(self, args):
        self.args = args

from enum import Enum
class SwordModuleManagerAction(Enum):
    download_list = 1
    download_module = 2
    delete_module = 3
