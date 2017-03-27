
from PyQt5.QtGui import QFontDatabase, QFont

class UnicodeFonts(object):
    
    arabic_block = [1536, 1791]
    hebrew_block = [1424, 1535]
    greek_block = [880, 1023]
    
    arabic_font = "Scheherazade"
    hebrew_font = "Ezra SIL"
    greek_font = "Galatia SIL"
    
    arabic_size = 40
    hebrew_size = 20
    greek_size = 20
    
    def __init__(self):
        QFontDatabase.addApplicationFont("./assets/fonts/Scheherazade-2.100/Scheherazade-Regular.ttf")
        QFontDatabase.addApplicationFont("./assets/fonts/EzraSIL2.51/SILEOT.ttf")
        QFontDatabase.addApplicationFont("./assets/fonts/GalSIL21/GalSILR.ttf")
        
    def isInUnicodeRange(self, start, end, string):
        result = False
        try:
            for char in string.strip():
                if ord(char) > start and ord(char) < end:
                    result = True
        except AttributeError:
            pass
        
        return result
    
    def applyFontAndSizeToQWidget(self, string, widget):
        if self.isInUnicodeRange(self.arabic_block[0], self.arabic_block[1], string):
            widget.setFont(QFont(self.arabic_font))
            widget.setFontPointSize(self.arabic_size)
        
        elif self.isInUnicodeRange(self.hebrew_block[0], self.hebrew_block[1], string):
            widget.setFont(QFont(self.hebrew_font))
            widget.setFontPointSize(self.hebrew_size)
        
        elif self.isInUnicodeRange(self.greek_block[0], self.greek_block[1], string):
            widget.setFont(QFont(self.greek_font))
            widget.setFontPointSize(self.greek_size)
    
    def applyFontToQWidget(self, string, widget):
        if self.isInUnicodeRange(self.arabic_block[0], self.arabic_block[1], string):
            widget.setFont(QFont(self.arabic_font))
        elif self.isInUnicodeRange(self.hebrew_block[0], self.hebrew_block[1], string):
            widget.setFont(QFont(self.hebrew_font))
        elif self.isInUnicodeRange(self.greek_block[0], self.greek_block[1], string):
            widget.setFont(QFont(self.greek_font))
    
    def applyFontToQWidgetFiltered(self, string, widget, languages_filter):
        if 'arabic' in languages_filter:
            if self.isInUnicodeRange(self.arabic_block[0], self.arabic_block[1], string):
                widget.setFont(QFont(self.arabic_font))
        if 'hebrew' in languages_filter:
            if self.isInUnicodeRange(self.hebrew_block[0], self.hebrew_block[1], string):
                widget.setFont(QFont(self.hebrew_font))
        if 'greek' in languages_filter:
            if self.isInUnicodeRange(self.greek_block[0], self.greek_block[1], string):
                widget.setFont(QFont(self.greek_font))
    
    def printFonts(self):
        db = QFontDatabase()
        fonts = QFontDatabase.families(db)
        for font in fonts:
            #if font.find("zra"):
            print(font)
