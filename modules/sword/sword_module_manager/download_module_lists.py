
import urllib.request, tarfile, os, configparser

try:
    from modules.sword.safe_tar_extract import SafeTarExtract
except:
    from safe_tar_extract import SafeTarExtract

class DownloadModulesLists(object):
    
    temp_path = None
    sword_modules_path = None
    modules_struct = {}
    
    def __init__(self, temp_path, sword_modules_path):
        super().__init__()
        
        self.temp_path = temp_path
        self.sword_modules_path = sword_modules_path
    
    def getModulesData(self):
        return self.modules_struct
    
    def getServerList(self):
        repositories = [
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
            {
                'name': 'Bible.org',
                'base': 'ftp.bible.org',
                'path': '/sword/',
            },
            {
                'name': 'Xiphos',
                'base': 'ftp.xiphos.org',
                'path': '',
            },
            {
                'name': 'IBT',
                'base': 'ftp.ibt.org.ru',
                'path': 'pub/modsword/raw',
            },
            {
                'name': 'eBible.org',
                'base': 'ftp.ebible.org',
                'path': '/sword/',
            },
        ]
        return self.__prepareRepositories(repositories)
    
    def __prepareRepositories(self, repositories):
        for i, repo in enumerate(repositories):
            if not repo['path'].startswith('/'):
                path = repo['path']
                repositories[i]['path'] = '/'+path
            if not repo['path'].endswith('/'):
                repositories[i]['path'] += '/'
        return repositories
    
    def getAllModules(self):
        self.modules_struct = {}
        
        self.listRemoteModules()
        self.listLocalModules()
        return self.modules_struct
    
    def listRemoteModules(self):
        server_list = self.getServerList()
        
        for mod in server_list:
            print('fetching list:', mod['name'])
            self.__processRemoteModule(mod['name'], mod['base'], mod['path'])
            
        return self.modules_struct
    
    def __processRemoteModule(self, name, site, repository_dir):
        thetarfile = "ftp://"+site+repository_dir+"mods.d.tar.gz"
        ftpstream = urllib.request.urlopen(thetarfile)
        thetarfile = tarfile.open(fileobj=ftpstream, mode="r|gz")
        
        if not os.path.exists(self.temp_path):
            os.mkdir(self.temp_path)
        temp_file_path = os.path.join(os.sep, self.temp_path, name)
        
        safe_tar_extract = SafeTarExtract()
        safe_tar_extract.extractSafely(temp_file_path, thetarfile)
        
        self.__processConfigFiles(name, site, repository_dir, temp_file_path)
        
    def listLocalModules(self):
        self.__processConfigFiles(None, None, None, self.sword_modules_path)
        
        return self.modules_struct
    
    def __processConfigFiles(self, name, site, repository_dir, temp_path):
        mod_d_path = os.path.join(os.sep, temp_path, 'mods.d')
        if os.path.exists(mod_d_path):
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
                        if name is None:
                            name = 'local'
                            
                        if not name in self.modules_struct:
                            self.modules_struct[name] = {'modules': {}, 'server_info': {'site': site, 'dir': repository_dir}}
                            
                        if language in self.modules_struct[name]['modules']:
                            self.modules_struct[name]['modules'][language].append(item)
                        else:
                            self.modules_struct[name]['modules'][language] = [item]
        
