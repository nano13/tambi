
import os, urllib.request
from shutil import copyfile
from ftplib import FTP

class ModuleNotFound(Exception):
    pass

class DownloadModule(object):
    
    temp_path = None
    sword_modules_path = None
    modules_struct = None
    
    module_name = None
    repository_name = None
    
    def __init__(self, temp_path, sword_modules_path, modules_struct, module_name, repository_name=None):
        super().__init__()
        
        self.temp_path = temp_path
        self.sword_modules_path = sword_modules_path
        self.modules_struct = modules_struct
        self.module_name = module_name
        self.repository_name = repository_name
        
        self.run()
    
    def run(self):
        if self.repository_name is None:
            self.__downloadModule(self.module_name)
        else:
            self.__downloadModuleFromRepository(self.repository_name, self.module_name)
    
    # install given module from given repository
    def __downloadModuleFromRepository(self, repository_name, module_name):
        try:
            repo_data = self.modules_struct[repository_name]
        except KeyError:
            raise ModuleNotFound('module "'+module_name+'" not found in repository "'+repository_name+'"')
        else:
            for language in repo_data['modules']:
                for module in self.modules_struct[repository_name]['modules'][language]:
                    if module['name'] == module_name:
                        self.__downloadData(repository_name, module, module_name)
                
    
    # search given module_name in all repositories, install first occurence
    def __downloadModule(self, module_name):
        # if a module is provided by more than one repository, we want just install the first occurence:
        module_already_installed = False
        for repo in self.modules_struct:
            # we do not want to 'install' a module from locale to locale ...
            if repo is not 'local':
                for language in self.modules_struct[repo]['modules']:
                    for module in self.modules_struct[repo]['modules'][language]:
                        #if module[language]['name'] == module_name:
                        if (module['name'] == module_name) and (not module_already_installed):
                            module_already_installed = True
                            
                            self.__downloadData(repo, module, module_name)
            
            #raise ModuleNotFound('module '+module_name+' not found on the remote repositories')
    
    def __downloadData(self, repo, module, module_name):
        # copy .conf-file from temp to sword-folder:
        source_file = os.path.join(os.sep, self.temp_path, repo, 'mods.d', module_name.lower()+'.conf')
        
        destination_file = os.path.join(os.sep, self.sword_modules_path, 'mods.d', module_name.lower()+'.conf')
        
        destination_path = os.path.dirname(os.path.abspath(destination_file))
        #print('DEST PATH', destination_path)
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        copyfile(source_file, destination_file)
        
        # download modules files from ftp to sword-folder:
        destination_folder = os.path.join(os.sep, self.sword_modules_path, module['datapath'])
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        with FTP(self.modules_struct[repo]['server_info']['site']) as ftp:
            ftp.login()
            
            ftp_folder = self.modules_struct[repo]['server_info']['dir']+module['datapath']
            
            try:
                ftp.cwd(ftp_folder)
            except:
                # module can not be installed
                raise ModuleNotFound('module broken or server down')
            else:
                listing = ftp.nlst()
                for data_file in listing:
                    source_folder = 'ftp://'+self.modules_struct[repo]['server_info']['site']+self.modules_struct[repo]['server_info']['dir']+module['datapath']+data_file
                    
                    urllib.request.urlretrieve(source_folder, destination_folder+data_file)

