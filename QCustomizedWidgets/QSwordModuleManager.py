
from PyQt5.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QGridLayout, QPushButton
from PyQt5.QtCore import Qt

from modules.sword.sword_module_manager import SwordModuleManager, ModuleNotFound

INSTALLED_MODULES = 'Installed'

class QSwordModuleManager(QWidget):
    
    module_manager = SwordModuleManager()
    #data = module_manager.getAllModules()
    data = None
    
    def __init__(self):
        super().__init__()
        
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
        
        self.addRemoteModules(self.data)
    
    def addRemoteModules(self, data):
        for repo_name in sorted(data):
            parent = QTreeWidgetItem(self.tree)
            if repo_name is not 'local':
                parent.setText(0, repo_name)
            else:
                parent.setText(0, INSTALLED_MODULES)
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            
            for language in sorted(data[repo_name]['modules']):
                child = QTreeWidgetItem(parent)
                child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                child.setText(0, language)
                
                for module in data[repo_name]['modules'][language]:
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
                    if item.parent().parent().text(0) == INSTALLED_MODULES:
                        if item.checkState(0) == Qt.Unchecked:
                            modules_to_process['delete'].append(item.text(0))
                    # handle the remote modules to install
                    else:
                        if item.checkState(0) == Qt.Checked:
                            modules_to_process['install'].append(item.text(0))
            iterator += 1
            item = iterator.value()
        
        self.installAndUninstallModules(modules_to_process)
    
    def canchelButtonClicked(self):
        self.tree.deleteLater()
        self.addTreeWidget()
    
    def installAndUninstallModules(self, modules_to_process):
        for module in modules_to_process['delete']:
            self.module_manager.deleteModule(module)
        
        for module in modules_to_process['install']:
            try:
                self.module_manager.downloadModule(module)
            except ModuleNotFound as e:
                print(e)
        
        # reload data and view
        self.data = self.module_manager.getAllModules()
        self.tree.deleteLater()
        self.addTreeWidget()
    
