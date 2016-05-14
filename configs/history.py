
import os

from configs.configFiles import ConfigDir

HISTORY_MAX_SIZE = 100
HISTORY_FILE_NAME = "history"

class History(object):
    def __init__(self):
        
        config_dir = ConfigDir()
        path = config_dir.getConfigDirPath()
        self.filepath = os.path.join(path, HISTORY_FILE_NAME)
        
        self.checkForAndCreateHistoryFile()
        self.cropFileToSize(HISTORY_MAX_SIZE)
        
    def checkForAndCreateHistoryFile(self):
        if not os.path.exists(self.filepath):
            history_file = open(self.filepath, "w+")
            history_file.close()
    
    def cropFileToSize(self, history_max_size):
        
        history_file = open(self.filepath, "r")
        
        history_list = []
        for line in history_file:
            history_list.append(line)
        
        history_file.close()
        
        if len(history_list) > history_max_size:
            history_file = open(self.filepath, "w")
            
            value = (len(history_list) - history_max_size) * -1
            history_list = history_list[::-1][:value][::-1]
            
            for line in history_list:
                if not line == "\n":
                    history_file.write(line)
            
            history_file.close()
            
    def getHistorySize(self):
        return sum(1 for line in open(self.filepath, "r"))
    
    def historyReadAll(self):
        
        history_file = open(self.filepath, "r")
        
        history_list = []
        for line in history_file:
            history_list.append(line)
        
        history_file.close()
        
        return history_list
    
    def historyReadAtIndex(self, index):
        
        history_file = open(self.filepath, "r")
        
        history_list = []
        for line in history_file:
            history_list.append(line)
        # the last history-entry should be the empty line:
        history_list.append("")
        
        history_file.close()
        
        result = ""
        try:
            result = history_list[::-1][index][:-1]
        except IndexError:
            pass
        
        return result
    
    def historyWrite(self, text):
        
        # we do not want to append the new text, if the last history entry is already the same:
        if not self.historyReadAtIndex(1) == text:
            history_file = open(self.filepath, "a")
            
            history_file.write(text)
            history_file.write("\n")
            
            history_file.close()
