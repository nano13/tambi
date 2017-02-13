

import platform, os
import shutil

import configparser

CONFIG_FOLDER_NAME = "logos_bible"
DEFAULT_CONFIG_FILE_NAME = "logos.conf"

class ConfigFile(object):
    def __init__(self):
        
        #self.filename = filename
        #self.filename = DEFAULT_CONFIG_FILE_NAME
        
        configDir = ConfigDir()
        self.configDirPath = configDir.getConfigDirPath()
        self.configFilePath = os.path.join(self.configDirPath, DEFAULT_CONFIG_FILE_NAME)
        
        self.config = configparser.ConfigParser()
        self.config.read(self.configFilePath)
        
    def readVar(self, section, option):
        result = self.config.get(section, option)
        return result
    
    def readPath(self, section, option):
        result = self.config.get(section, option)
        result =  self.resolvePathConstants(result)
        
        return os.path.normpath(result)
        #return os.path.normcase(result)
        
    def resolvePathConstants(self, confresult):
        if "$" in confresult:
            confresult = confresult.replace("$CONFDIR", self.configDirPath)
            
        return confresult
    
    def write(self, section, option, value):
        self.config.set(section, option, value)
        
        cfgfile = open(self.configFilePath, "w")
        self.config.write(cfgfile)
        
    
class ConfigDir(object):
    def __init__(self):
        
        self.configDirPath = self.checkForAndCreateConfigDir()
        self.checkForAndCreateConfigFile(DEFAULT_CONFIG_FILE_NAME)
        
    def getConfigDirPath(self):
        return self.configDirPath
    
    def checkForAndCreateConfigFile(self, confName):
        
        targetConfPath = os.path.join(self.configDirPath, confName)
        
        if not os.path.exists(targetConfPath):
            defaultConf = os.path.join(os.getcwd(), "configs", confName)
            targetConf = os.path.join(self.configDirPath, confName)
            
            shutil.copyfile(defaultConf, targetConf)
    
    def checkForAndCreateConfigDir(self):
        
        os_name = platform.uname()[0]
        dir_path = ""
        
        if os_name == "Windows":
            home = os.getenv("APPDATA")
            dir_path = os.path.join(home, CONFIG_FOLDER_NAME)
        #elif  os_name == "Linux" or os_name == "Darwin":
        else:
            home = os.getenv("HOME")
            dir_path = os.path.join(home, "."+CONFIG_FOLDER_NAME)
            
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
                
        return dir_path
    
#    def moveFile(self, source_path, target_path):
#        os.makedirs(os.path.dirname(target_path))
#        shutil.copyfile(source_path, target_path)
    
class WriteMissingValueToConfig(object):
    def __init__(self, filename, config, cfgfile_path):
        self.filename = "./configs" + filename
        self.config = config
        self.cfgfile_path = cfgfile_path

if __name__ == "__main__":
    c = ConfigDir()
    c.checkForAndCreateConfigDir()
