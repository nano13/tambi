

import platform, os
import shutil

import configparser

CONFIG_FOLDER_NAME = "logos_bible"

class Config(object):
    def __init__(self, path_to_default_conf_dir, filename):
        
        self.filename = filename
        
    
class ConfigDir(object):
    def __init__(self):
        
        self.dir_path = self.checkForAndCreateConfigDir()
        
    def getConfigDirPath(self):
        return self.dir_path
    
    def getPathDelimiter(self):
        os_name = platform.uname()[0]
        
        delimiter = ""
        
        if os_name == "Linux" or os_name == "Darwin":
            delimiter = "/"
        elif os_name == "Windows":
            delimiter = "\\"
            
        return delimiter
    
    def checkForAndCreateConfigFile(self, filepath):
        
        dir_path = checkForAndCreateConfigDir()
        
        if not os.path.exists(cfgfile_path):
            pass
    
    def checkForAndCreateConfigDir(self):
        
        os_name = platform.uname()[0]
        dir_path = ""
        
        if  os_name == "Linux" or os_name == "Darwin":
            home = os.getenv("HOME")
            
            dir_path = home + "/." + CONFIG_FOLDER_NAME
            
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
        
        elif os_name == "Windows":
            
            home = os.getenv("APPDATA")
            
            dir_path = home + "\\" +  CONFIG_FOLDER_NAME + "\\"
            
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
                
        return dir_path

if __name__ == "__main__":
    c = ConfigDir()
    c.checkForAndCreateConfigDir()