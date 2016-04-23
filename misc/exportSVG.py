

class ExportSVG(object):
    def __init__(self):
        pass
    
    def testExport(self, outpath):
        
        self.setFilepath(outpath)
        self.header(700, 400, 0, 0, 700, 400)
        
        self.addLine(0, 200, 700, 200, "black", 10)
        
        self.footer()
        self.fobj.close()
        
    def setFilepath(self, filepath):
        self.fobj = open(filepath, "w")
    
    def writeHeader(self, width, height, box_a, box_b, box_c, box_d):
        
        self.fobj.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        self.fobj.write('<svg xmlns="http://www.w3.org/2000/svg"\n')
        self.fobj.write('\tversion="1.1" baseProfile="full"\n')
        self.fobj.write('\twidth="{0}px" height="{1}px" viewBox="{2} {3} {4} {5}">\n'.format(width, height, box_a, box_b, box_c, box_d))
        self.fobj.write('\n')
        
    def addLine(self, x1, y1, x2, y2, colour, width):
        self.fobj.write('<line x1="{0}" y1="{1}" x2="{2}" y2="{3}" stroke="{4}" stroke-width="{5}px"/>\n'.format(x1, y1, x2, y2, colour, width))
        
    def addEllipse(self, cx, cy, rx, ry, colour, width):
        self.fobj.write('<ellipse cx="{0}" cy="{1}" rx="{2}" ry="{3}" fill="{4}"/>\n'.format(cx, cy, rx, ry, colour))
        
    def writeFooter(self):
        self.fobj.write('</svg>')
        self.fobj.close()
        
if __name__ == "__main__":
    c = ExportSVG()
    c.testExport("output.svg")
