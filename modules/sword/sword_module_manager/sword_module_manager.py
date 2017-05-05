
from download_module_lists_thread import DownloadModulesListsThread
from download_module_thread import DownloadModuleThread

from queue import Queue
import sys, os, tempfile, getpass, configparser
from shutil import rmtree

class SwordModuleManager(object):
    
    modules_struct = {}
    sword_modules_path = None
    q = Queue()
    
    def __init__(self, sword_modules_path=None):
        if sword_modules_path is None:
            if sys.platform.startswith('win32'):
                self.sword_modules_path = os.path.join(os.getenv('APPDATA'), 'Sword')
            elif sys.platform.startswith('darwin'):
                self.sword_modules_path = os.path.join(os.getenv('HOME'), 'Library', 'Application Support', 'Sword')
            else: # linux, etc.
                self.sword_modules_path = os.path.join(os.getenv('HOME'), '.sword')
        else:
            self.sword_modules_path = sword_modules_path
            
        if not os.path.exists(self.sword_modules_path):
            os.makedirs(self.sword_modules_path)
        
        
    def downloadModulesLists(self):
        temp_path = self.__getTempPath()
        
        download_lists_thread = DownloadModulesListsThread(temp_path, self.sword_modules_path, self.q)
        self.modules_struct = download_lists_thread.start()
        print('BLA')
        self.modules_struct = self.q.get()
        download_lists_thread.join()
        #print(self.modules_struct)
    
    def downloadModuleFromRepository(self, repository_name, module_name):
        temp_path = self.__getTempPath()
        
        download_module_thread = DownloadModuleThread(temp_path, self.sword_modules_path, self.modules_struct, module_name, repository_name)
        download_module_thread.start()
        print('DOWNLOADING:', module_name)
    
    def downloadModule(self, module_name):
        temp_path = self.__getTempPath()
        
        download_module_thread = DownloadModuleThread(temp_path, self.sword_modules_path, self.modules_struct, module_name)
        download_module_thread.start()
        print('DOWNLOADING:', module_name)
    
    def __getTempPath(self):
        return os.path.join(os.sep, tempfile.gettempdir(), 'logos_sword_'+getpass.getuser())
    
    def deleteModule(self, module_name):
        print('DELETING MODULE')
        mods_d_path = os.path.abspath(os.path.join(os.sep, self.sword_modules_path, 'mods.d'))
        config_file_name = module_name.lower()+'.conf'
        
        config = configparser.ConfigParser(strict=False)
        config.read(os.path.join(os.sep, mods_d_path, config_file_name))
        sections = config.sections()
        try:
            datapath = config[sections[0]]['DataPath'].replace('/', os.sep)
        except IndexError:
            print('ERROR: Module '+module_name+' not found')
        else:
            conf_path = os.path.abspath(os.path.join(os.sep, mods_d_path, config_file_name))
            
            dir_path = os.path.abspath(os.path.join(os.sep, self.sword_modules_path, datapath))
            
            print(conf_path)
            print(dir_path)
            
            rmtree(dir_path)
            os.remove(conf_path)
    
if __name__ == '__main__':
    c = SwordModuleManager()
    c.downloadModulesLists()
    #c.q.join()
    c.downloadModule('alzat')
    #c.downloadModuleFromRepository('CrossWire Bible Society Attic', 'AraNAV')
    #c.deleteModule('AraNAV')
