
try:
    from download_module_lists import DownloadModulesLists
except:
    from modules.sword.sword_module_manager.download_module_lists import DownloadModulesLists

try:
    from download_module import DownloadModule
except:
    from modules.sword.sword_module_manager.download_module import DownloadModule

import sys, os, tempfile, getpass, configparser
from shutil import rmtree

class SwordModuleManager(object):
    
    modules_struct = {}
    sword_modules_path = None
    
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
        
        download_lists = DownloadModulesLists(temp_path, self.sword_modules_path)
        
        download_lists.getAllModules()
        self.modules_struct = download_lists.getModulesData()
        
        return self.modules_struct
    
    # install given module from given repository
    def downloadModuleFromRepository(self, repository_name, module_name):
        temp_path = self.__getTempPath()
        
        download_module = DownloadModule(temp_path, self.sword_modules_path, self.modules_struct, module_name, repository_name)
        #download_module.start()
        print('DOWNLOADING:', module_name)
    
    # search given module_name in all repositories, install first occurence
    def downloadModule(self, module_name):
        temp_path = self.__getTempPath()
        
        download_module = DownloadModule(temp_path, self.sword_modules_path, self.modules_struct, module_name)
        #download_module.start()
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
    
    def showAvailableUpgrades(self):
        modules_to_upgrade = {}
        
        for local_module_lang in self.modules_struct['local']['modules']:
            local_modules_list = self.modules_struct['local']['modules'][local_module_lang]
            
            for local_module_item in local_modules_list:
                local_version = local_module_item['version']
                
                for remote_repository_name in self.modules_struct:
                    if not remote_repository_name == 'local':
                        remote_repository = self.modules_struct[remote_repository_name]
                        
                        try:
                            remote_modules_list = remote_repository['modules'][local_module_lang]
                        except KeyError:
                            pass # the current remote module does not have this language, we can just do nothing
                        else:
                            for remote_module_item in remote_modules_list:
                                if remote_module_item['name'] == local_module_item['name']:
                                
                                    remote_version = remote_module_item['version']
                                    
                                    if self.__isVersionNumberGreater(remote_version, local_version):
                                        server_site = self.modules_struct[remote_repository_name]['server_info']['site']
                                        server_dir = self.modules_struct[remote_repository_name]['server_info']['dir']
                                        
                                        if not remote_repository_name in modules_to_upgrade:
                                            modules_to_upgrade[remote_repository_name] = {'modules': {local_module_lang: [remote_module_item]}, 'server_info': {'site': server_site, 'dir': server_dir}}
                                        
                                        else:
                                            if not local_module_lang in modules_to_upgrade[remote_repository_name]['modules']:
                                                modules_to_upgrade[remote_repository_name]['modules'][local_module_lang] = [remote_module_item]
                                            else:
                                                modules_to_upgrade[remote_repository_name]['modules'][local_module_lang].append(remote_module_item)
        
        return modules_to_upgrade
    
    # is number_a > number_b ?
    def __isVersionNumberGreater(self, number_a, number_b):
        a = number_a.split('.')
        b = number_b.split('.')
        
        for i in range(0, len(a)):
            if len(b) > i:
                if a[i] > b[i]:
                    return True
                elif a[i] < b[i]:
                    return False
            else:
                return True # because: something > nothing
        return False
    
if __name__ == '__main__':
    c = SwordModuleManager()
    c.downloadModulesLists()
    #c.q.join()
    c.downloadModule('alzat')
    #c.downloadModuleFromRepository('CrossWire Bible Society Attic', 'AraNAV')
    #c.deleteModule('AraNAV')
