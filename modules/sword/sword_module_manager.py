
from ftplib import FTP
from shutil import copyfile, rmtree
import tarfile
import urllib.request
import tempfile
import os, sys
import configparser
import getpass

try:
    from modules.sword.safe_tar_extract import SafeTarExtract
except:
    from safe_tar_extract import SafeTarExtract

class ModuleNotFound(Exception):
    pass

class SwordModuleManager(object):
    
    remote_modules = {}
    local_modules = {}
    #modules_struct = {}
    
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
        
    def getServerList(self):
        return [
            {
                'name': 'CrossWire Bible Society (main)',
                'base': 'ftp.crosswire.org',
                'path': '/pub/sword/raw/',
            },
            {
                'name': 'CrossWire Bible Society Attic',
                'base': 'ftp.crosswire.org',
                'path': '/pub/sword/atticraw/',
            },
            {
                'name': 'CrossWire Wycliffe',
                'base': 'ftp.crosswire.org',
                'path': '/pub/sword/wyclifferaw/',
            },
        ]
    
    def getTempPath(self):
        return os.path.join(os.sep, tempfile.gettempdir(), 'logos_sword_'+getpass.getuser())
    
    def downloadModule(self, module_name):
        self.downloadListsIfNeccessary()
        
        temp_path = self.getTempPath()
        
        for module in self.remote_modules:
            if module['name'] == module_name:
                
                # copy .conf-file from temp to sword-folder:
                source_file = os.path.join(os.sep, temp_path, module['repository_name'], 'mods.d', module_name.lower()+'.conf')
                destination_file = os.path.join(os.sep, self.sword_modules_path, 'mods.d', module_name.lower()+'.conf')
                
                copyfile(source_file, destination_file)
                
                # download modules files from ftp to sword-folder:
                destination_folder = os.path.join(os.sep, self.sword_modules_path, module['datapath'])
                if not os.path.exists(destination_folder):
                    os.mkdir(destination_folder)
                
                
                with FTP(module['repository_base']) as ftp:
                    ftp.login()
                    ftp.cwd(module['repository_path']+'/'+module['datapath'])
                    
                    listing = ftp.nlst()
                    for data_file in listing:
                        source_folder = 'ftp://'+module['repository_base']+module['repository_path']+module['datapath']+data_file
                        
                        urllib.request.urlretrieve(source_folder, destination_folder+data_file)
                        
                
            #raise ModuleNotFound('module '+module_name+' not found on the remote repositories')
    
    def deleteModule(self, module_name):
        # we could parse the cofig file separately (would be a lot more performant),
        # but we can just use the already implemented infrastructure:
        if len(self.local_modules) is 0:
            self.listLocalModules()
        
        for module in self.local_modules:
            if module['name'] == module_name:
                
                conf_path = os.path.join(os.sep, self.sword_modules_path, 'mods.d', module_name.lower()+'.conf')
                dir_path = os.path.join(os.sep, self.sword_modules_path, module['datapath'])
                
                os.remove(conf_path)
                rmtree(dir_path)
                
    
    def listRemoteModules(self):
        server_list = self.getServerList()
        
        for mod in server_list:
            print(mod['name'])
            self.processRemoteModule(mod['name'], mod['base'], mod['path'])
            
        return self.remote_modules
        
    def processRemoteModule(self, name, site, repository_dir):
        thetarfile = "ftp://"+site+repository_dir+"mods.d.tar.gz"
        ftpstream = urllib.request.urlopen(thetarfile)
        thetarfile = tarfile.open(fileobj=ftpstream, mode="r|gz")
        
        temp_path = self.getTempPath()
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
        temp_file_path = os.path.join(os.sep, temp_path, name)
        
        safe_tar_extract = SafeTarExtract()
        safe_tar_extract.extractSafely(temp_file_path, thetarfile)
        
        self.processConfigFiles(name, site, repository_dir, temp_file_path)
        
    def listLocalModules(self):
        self.processConfigFiles(None, None, None, self.sword_modules_path)
        
        return self.local_modules
        
    def processConfigFiles(self, name, site, repository_dir, temp_path):
        mod_d_path = os.path.join(os.sep, temp_path, 'mods.d')
        base, dirs, files = next(iter(os.walk(mod_d_path)))
        
        for conf in files:
            mod_name = conf.split('.')[0]
            #print('=== '+mod_name+' ===')
            
            config = configparser.ConfigParser(strict=False)
            try:
                config.read(os.path.join(os.sep, base, conf))
            except:
                # we are not interested in broken or problematic modules
                pass
            else:
                sections = config.sections()
                
                try:
                    description = config[sections[0]]['Description']
                    version = config[sections[0]]['Version']
                    datapath = config[sections[0]]['DataPath']
                    language = config[sections[0]]['Lang']
                except KeyError:
                    # we are still not interested in broken or problematic modules
                    pass
                else:
                    item = {
                        'name': sections[0],
                        'description': description,
                        'datapath': datapath,
                        'version': version,
                    }
                    # we are dealing with the remote modules:
                    if name is not None:
                        if not name in self.remote_modules:
                            self.remote_modules[name] = {}
                            pass
                            
                        if True:
                            if language in self.remote_modules[name]:
                                self.remote_modules[name][language].append(item)
                            else:
                                self.remote_modules[name][language] = [item]
                            
                        
                    # we are dealing with the localy installed modules:
                    else:
                        if language in self.local_modules:
                            self.local_modules[language].append(item)
                        else:
                            self.local_modules[language] = [item]
                    
                    
                    """
                    current_module = {
                        'repository_name': name,
                        'repository_base': site,
                        'repository_path': repository_dir,
                        
                        'name': sections[0],
                        'description': description,
                        'version': version,
                        'datapath': datapath,
                        'language': language,
                    }
                    if name is not None:
                        self.remote_modules.append(current_module)
                    else:
                        self.local_modules.append(current_module)
                    """
        #self.modules_struct['remote'] = self.remote_modules
        #self.modules_struct['local'] = self.local_modules
    
    def downloadListsIfNeccessary(self):
        if len(self.local_modules) is 0:
            self.listLocalModules()
        if len(self.remote_modules) is 0:
            self.listRemoteModules()
    
    def listModulesWithNeverVersionAvailable(self):
        self.downloadListsIfNeccessary()
        
        for local_module in self.local_modules:
            for remote_module in self.remote_modules:
                if local_module['name'] == remote_module['name']:
                    if self.isVersionNumberGreater(remote_module['version'], local_module['version']):
                        print("Module "+local_module['name']+" needs update!")
            
    
    # is number_a > number_b ?
    def isVersionNumberGreater(self, number_a, number_b):
        a = number_a.split('.')
        b = number_b.split('.')
        print(a, b)
        
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
    c.listRemoteModules()
    #c.listLocalModules()
    
    print(c.remote_modules)
    print(c.local_modules)
    
    #c.listModulesWithNeverVersionAvailable()
    #print(c.isVersionNumberGreater('2.1', '1.1.1'))
    
    #c.downloadModule('CzeBKR')
    #c.deleteModule('CzeBKR')
