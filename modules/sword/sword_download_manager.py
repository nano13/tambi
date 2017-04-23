
from ftplib import FTP
from io import StringIO
import tarfile


class SwordDownloadmanager(object):
    
    
    
    def __init__(self):
        
        self.fetchModulesList('ftp.crosswire.org', '/pub/sword/raw/')
    
    def fetchModulesList(self, site, repository_dir):
        
        with FTP(site) as ftp:
            ftp.login()
            ftp.cwd(repository_dir)
        
        
    
if __name__ == '__main__':
    c = SwordDownloadmanager()
