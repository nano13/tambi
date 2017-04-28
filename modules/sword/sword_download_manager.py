
from ftplib import FTP
from io import StringIO
import tarfile
import urllib.request
import tempfile
import os
import configparser

from safe_tar_extract import SafeTarExtract

class SwordDownloadmanager(object):
    
    available_modules = []
    
    def __init__(self):
        
        modules = [
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
        
        #self.fetchModulesList('ftp.crosswire.org', '/pub/sword/raw/')
        for mod in modules:
            print(mod['name'])
            self.fetchModulesList(mod['name'], mod['base'], mod['path'])
    
    def _fetchModulesList(self, site, repository_dir):
        
        with FTP(site) as ftp:
            ftp.login()
            ftp.cwd(repository_dir)
        
        
    
    def fetchModulesList(self, name, site, repository_dir):
        thetarfile = "ftp://"+site+repository_dir+"mods.d.tar.gz"
        ftpstream = urllib.request.urlopen(thetarfile)
        thetarfile = tarfile.open(fileobj=ftpstream, mode="r|gz")
        
        #for conf in thetarfile:
            #print(conf.name)
            #print(conf.mtime)
        
        temp_path = os.path.join(os.sep, tempfile.gettempdir(), 'logos_sword')
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)
        temp_file_path = os.path.join(os.sep, temp_path, name)
        
        safe_tar_extract = SafeTarExtract()
        safe_tar_extract.extractSafely(temp_file_path, thetarfile)
        
        self.processConfigFiles(name, site, repository_dir, temp_file_path)
        
    def processConfigFiles(self, name, site, repository_dir, temp_path):
        mod_d_path = os.path.join(os.sep, temp_path, 'mods.d')
        base, dirs, files = next(iter(os.walk(mod_d_path)))
        
        
        
        for conf in files:
            mod_name = conf.split('.')[0]
            print('### '+mod_name+' ###')
            
            config = configparser.ConfigParser(strict=False)
            try:
                config.read(os.path.join(os.sep, base, conf))
            except:
                # we are not interested in broken or problematic modules
                pass
            else:
                sections = config.sections()
                
                description = config[sections[0]]['Description']
            
            
            
    
if __name__ == '__main__':
    c = SwordDownloadmanager()
