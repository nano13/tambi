
from PyQt5.QtGui import QFontDatabase, QFont

class UnicodeFonts(object):
    def __init__(self):
        QFontDatabase.addApplicationFont("./assets/fonts/Scheherazade-2.100/Scheherazade-Regular.ttf")
        QFontDatabase.addApplicationFont("./assets/fonts/EzraSIL2.51/SILEOT.ttf")
        QFontDatabase.addApplicationFont("./assets/fonts/GalSIL21/GalSILR.ttf")
        
    def isInUnicodeRange(self, start, end, string):
        result = False
        for char in string.strip():
            if ord(char) > start and ord(char) < end:
                result = True
        return result
    
    def applyFontSizeToQWidget(self, string, widget):
        if self.isInUnicodeRange(1536, 1791, string):
            widget.setFont(QFont("Scheherazade"))
            widget.setFontPointSize(40)
        
        elif self.isInUnicodeRange(1424, 1535, string):
            widget.setFont(QFont("Ezra SIL"))
            widget.setFontPointSize(20)
        
        elif self.isInUnicodeRange(880, 1023, string):
            widget.setFont(QFont("Galatia SIL"))
            widget.setFontPointSize(20)
    
    def printFonts(self):
        db = QFontDatabase()
        fonts = QFontDatabase.families(db)
        for font in fonts:
            #if font.find("zra"):
            print(font)
