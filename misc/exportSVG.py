
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem

class ExportSVG(object):
    def __init__(self):
        pass
        
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
        
    def exportSVG(self, filepath, view):
        self.setFilepath(filepath)
        
        view_rect = view.mapToScene(view.viewport().geometry()).boundingRect()
        a, b, c, d = view_rect.getRect()
        self.writeHeader(abs(a), abs(b), a, b, c, d)
        
        items = view.scene().items()
        for item in items:
            if type(item) == QGraphicsEllipseItem:
                
                cx, cy, rx, ry = item.rect().getRect()
                self.addEllipse(cx+rx/2, cy+ry/2, rx/2, ry/2, "green", view.penRadius)
                
            elif type(item) == QGraphicsLineItem:
                x1 = item.line().x1()
                y1 = item.line().y1()
                x2 = item.line().x2()
                y2 = item.line().y2()
                self.addLine(x1, y1, x2, y2, "green", view.penRadius)
                
        self.writeFooter()
