
from ftplib import FTP
from io import StringIO
import tarfile
import urllib.request
import tempfile
import os, sys
import configparser

from safe_tar_extract import SafeTarExtract

class SwordDownloadmanager(object):
    
    remote_modules = []
    locale_modules = []
    
    
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
    
    def _listRemoteModules(self, site, repository_dir):
        
        with FTP(site) as ftp:
            ftp.login()
            ftp.cwd(repository_dir)
        
        
    
    def listRemoteModules(self):
        server_list = self.getServerList()
        
        for mod in server_list:
            print(mod['name'])
            self.processRemoteModule(mod['name'], mod['base'], mod['path'])
        #print(self.remote_modules)
        
    def processRemoteModule(self, name, site, repository_dir):
        thetarfile = "ftp://"+site+repository_dir+"mods.d.tar.gz"
        ftpstream = urllib.request.urlopen(thetarfile)
        thetarfile = tarfile.open(fileobj=ftpstream, mode="r|gz")
        
        temp_path = os.path.join(os.sep, tempfile.gettempdir(), 'logos_sword')
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
        temp_file_path = os.path.join(os.sep, temp_path, name)
        
        safe_tar_extract = SafeTarExtract()
        safe_tar_extract.extractSafely(temp_file_path, thetarfile)
        
        self.processConfigFiles(name, site, repository_dir, temp_file_path)
        
    def listLocalModules(self):
        self.processConfigFiles(None, None, None, self.sword_modules_path)
        
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
                except KeyError:
                    # we are still not interested in broken or problematic modules
                    pass
                else:
                    current_module = {
                        'repository_name': name,
                        'repository_base': site,
                        'repository_path': repository_dir,
                        
                        'name': sections[0],
                        'description': description,
                        'version': version,
                    }
                    if name is not None:
                        self.remote_modules.append(current_module)
                    else:
                        self.locale_modules.append(current_module)
    
    def listModulesWithNeverVersionAvailable(self):
        if len(self.locale_modules) is 0:
            self.listLocalModules()
        if len(self.remote_modules) is 0:
            self.listRemoteModules()
        
        for local_module in self.locale_modules:
            for remote_module in self.remote_modules:
                if local_module['name'] == remote_module['name']:
                    if self.isVersionNumberGreater(remote_module['version'], local_module['version']):
                        print("Module "+local_module['name']+" needs update!")
            
            #newer = self.isVersionNumberGreater(local_module['version'], 
    
    # is number_a > number_b ?
    def isVersionNumberGreater(self, number_a, number_b):
        a = number_a.split('.')
        b = number_b.split('.')
        print(a, b)
        
        for i in range(0, len(a)):
            for j in range(0, len(b)):
                if a[i] > b[i]:
                    return True
        """
        if a[0] > b[0]:
            return True
        elif a[1] > b[1]:
            return True
        elif a[2] > b[2]:
            return True
        else:
            return False
        """
    
if __name__ == '__main__':
    c = SwordDownloadmanager()
    #c.listRemoteModules()
    #c.listLocalModules()
    
    print(c.remote_modules)
    print(c.locale_modules)
    
    #c.listModulesWithNeverVersionAvailable()
    print(c.isVersionNumberGreater('1.1.1', '2.2.2'))
    
