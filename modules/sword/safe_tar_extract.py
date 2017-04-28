
# http://stackoverflow.com/questions/10060069/safely-extract-zip-or-tar-using-python

import tarfile
from os.path import abspath, realpath, dirname, join as joinpath
from sys import stderr

resolved = lambda x: realpath(abspath(x))

class SafeTarExtract(object):
    
    def badpath(self, path, base):
        # joinpath will ignore base if path is absolute
        return not resolved(joinpath(base, path)).startswith(base)
    
    def badlink(self, info, base):
        # links are interpredet relative to the directory containing the link
        tip = resolved(joinpath(base, dirname(info.name)))
        return badpath(info.linkname, base=tip)
    
    def safemembers(self, members):
        base = resolved(".")
        
        for finfo in members:
            if self.badpath(finfo.name, base):
                sys.stderr.write(finfo.name, "is blocked (illegal path)")
            elif finfo.issym() and badlink(finfo, base):
                sys.stderr.write(finfo.name, "is blocked: Hard link to", finfo.linkname)
            elif finfo.islnk() and badlink(finfo, base):
                sys.stderr.write(finfo.name, "is blocked: Symlink to", finfo.linkname)
            else:
                yield finfo
    
    def extractSafely(self, extract_path, tar_file):
        tar_file.extractall(path=extract_path, members=self.safemembers(tar_file))
        tar_file.close()
    
if __name__ == '__main__':
    c = SafeTarExtract()
    
    
