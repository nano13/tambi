

class ExportSVG(object):
    def __init__(self):
        pass
    
    def startExport(self):
        self.fobj = open("experiments/out.svg", "w")
        self.header()
        
        self.fobj.close()
    
    def header(self):
        self.fobj.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        self.fobj.write('<svg xmlns="http://www.w3.org/2000/svg"\n')
        self.fobj.write('\tversion="1.1" baseProfile="full"\n')
        self.fobj.write('\twidth="{0}px" height="{1}"px viewBox="{2} {3} {4} {5}">\n'.format())
        
        
    def footer(self):
        self.fobj.write('</svg>')
