
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5.QtGui import QPen
from PyQt5 import QtCore

from xml.dom import minidom
from xml.parsers.expat import ExpatError

class ImportSVG(object):
    def __init__(self):
        pass
        
    def importSVG(self, filepath, view):
        
        try:
            doc = minidom.parse(filepath)
        except ExpatError:
            # xml file is broken: we can't import it
            pass
        else:
        
            lines = doc.getElementsByTagName("line")
            for line in lines:
                x1 = line.getAttribute("x1")
                y1 = line.getAttribute("y1")
                x2 = line.getAttribute("x2")
                y2 = line.getAttribute("y2")
                width = line.getAttribute("width")
                
                lineItem = QGraphicsLineItem(float(x1), float(y1), float(x2), float(y2))
                lineItem.setPen(QPen(view.colour, view.penRadius, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
                view.scene().addItem(lineItem)
                
            ellipses = doc.getElementsByTagName("ellipse")
            for ellipse in ellipses:
                cx = ellipse.getAttribute("cx")
                cy = ellipse.getAttribute("cy")
                rx = ellipse.getAttribute("rx")
                ry = ellipse.getAttribute("ry")
                width = ellipse.getAttribute("width")
                
                ellipseItem = QGraphicsEllipseItem(float(cx)-float(rx), float(cy)-float(ry), float(rx)*2, float(ry)*2)
                ellipseItem.setPen(QPen(view.colour, QtCore.Qt.SolidPattern))
                ellipseItem.setBrush(view.colour)
                
                view.scene().addItem(ellipseItem)
            
