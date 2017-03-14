
from PyQt5.QtGui import QFontDatabase, QFont

class UnicodeFonts(object):
    def __init__(self):
        QFontDatabase.addApplicationFont("./assets/fonts/Scheherazade-2.100/Scheherazade-Regular.ttf")
        QFontDatabase.addApplicationFont("./assets/fonts/EzraSIL2.51/SILEOT.ttf")
        
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
    
    def applyCoranicaFontToQWidget(self, widget):
        font = QFont("Scheherazade")
        widget.setFont(font)
    
    def applyHebrewFontToQWidget(self, widget):
        font = QFont("Ezra SIL")
        widget.setFont(font)
        
        self.printFonts()
    
    def applyFontSizeToQWidget(self, string, widget):
        if self.isArabic(string):
            self.applyCoranicaFontToQWidget(widget)
            widget.setFontPointSize(40)
        
        if self.isHebrew(string):
            self.applyHebrewFontToQWidget(widget)
            widget.setFontPointSize(20)
    
    def printFonts(self):
        db = QFontDatabase()
        fonts = QFontDatabase.families(db)
        for font in fonts:
            #if font.find("zra"):
            print(font)
