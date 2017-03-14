
from PyQt5.QtGui import QFontDatabase, QFont

class UnicodeFonts(object):
    def __init__(self):
        QFontDatabase.addApplicationFont("./assets/fonts/Scheherazade-2.100/Scheherazade-Regular.ttf")
        QFontDatabase.addApplicationFont("./assets/fonts/EzraSIL2.51/SILEOT.ttf")
        QFontDatabase.addApplicationFont("./assets/fonts/GalSIL21/GalSILR.ttf")
        
    def isArabic(self, string):
        #return all(ord(char) > 1536 and ord(char) < 1791 for char in string)
        result = False
        for char in string.strip():
            if ord(char) > 1536 and ord(char) < 1791:
                result = True
        return result
    
    def isHebrew(self, string):
        #return all(ord(char) > 1424 and ord(char) < 1535 for char in string)
        result = False
        for char in string.strip():
            if ord(char) > 1424 and ord(char) < 1535:
                result = True
        return result
    
    def isGreek(self, string):
        result = False
        for char in string.strip():
            if ord(char) > 880 and ord(char) < 1023:
                result = True
        
        return result
    
    def applyFontSizeToQWidget(self, string, widget):
        if self.isArabic(string):
            widget.setFont(QFont("Scheherazade"))
            widget.setFontPointSize(40)
        
        if self.isHebrew(string):
            widget.setFont(QFont("Ezra SIL"))
            widget.setFontPointSize(20)
        
        if self.isGreek(string):
            widget.setFont(QFont("Galatia SIL"))
            widget.setFontPointSize(20)
            self.printFonts()
    
    def printFonts(self):
        db = QFontDatabase()
        fonts = QFontDatabase.families(db)
        for font in fonts:
            #if font.find("zra"):
            print(font)
