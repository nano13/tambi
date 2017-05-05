
from ftplib import FTP
from shutil import copyfile, rmtree
import tarfile
import urllib.request
import tempfile
import os, sys
import configparser
import getpass
from threading import Thread

try:
    from modules.sword.safe_tar_extract import SafeTarExtract
except:
    from safe_tar_extract import SafeTarExtract

class ModuleNotFound(Exception):
    pass

class SwordModuleManager(Thread):
    
    modules_struct = {}
    
    def __init__(self, sword_modules_path=None):
        super().__init__()
        
        
        
    
    
    
    
    
    
    
    
    
    
    
        
    
        
    
    
    def listModulesWithNeverVersionAvailable(self):
        self.listLocalModules()
        self.listRemoteModules()
        
        """
        for local_module in self.local_modules:
            for remote_module in self.modules_struct:
                if local_module['name'] == remote_module['name']:
                    if self.isVersionNumberGreater(remote_module['version'], local_module['version']):
                        print("Module "+local_module['name']+" needs update!")
        """
    
    
    
if __name__ == '__main__':
    c = SwordModuleManager()
    #c.listRemoteModules()
    #c.listLocalModules()
    
    #print(c.modules_struct)
    #print(c.local_modules)
    
    #c.listModulesWithNeverVersionAvailable()
    #print(c.isVersionNumberGreater('2.1', '1.1.1'))
    
    #c.downloadModule('CzeBKR')
    #c.deleteModule('CzeBKR')
