
from PyQt5.QtGui import QFontDatabase, QFont
import os
import platform

class UnicodeFonts(object):
    
    arabic_block = [1536, 1791]
    hebrew_block = [1424, 1535]
    greek_block = [880, 1023]
    
    arabic_font = "Scheherazade"
    hebrew_font = "Ezra SIL"
    greek_font = "Galatia SIL"
    
    arabic_size = 40
    hebrew_size = 20
    greek_size = 15
    
    def __init__(self):
        scriptpath = os.path.dirname(os.path.abspath(__file__))
        print(scriptpath)
        print(os.getcwd())
        fonts = [
            "./assets/fonts/SILEOT.ttf",
            "./assets/fonts/Scheherazade-Regular.ttf",
            #"assets/fonts/Scheherazade-2.100/Scheherazade-Regular.ttf",
            #"assets/fonts/EzraSIL2.51/SILEOT.ttf",
            "assets/fonts/GalSIL21/GalSILR.ttf",
        ]
        for font in fonts:
            """
            fontpath = os.getcwd() + '/' + font
            if platform.system() == 'Windows':
                fontpath = fontpath.replace('/', '\\')
            print(fontpath)
            """
            fontpath = font
            
            print("loading Font:", font.split('/')[-1], QFontDatabase.addApplicationFont(fontpath))
        
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
#            widget.setFont(QFont(self.greek_font))
            widget.setFontPointSize(self.greek_size)
    
    def applyFontToQWidget(self, string, widget):
        if self.isInUnicodeRange(self.arabic_block[0], self.arabic_block[1], string):
            widget.setFont(QFont(self.arabic_font))
        elif self.isInUnicodeRange(self.hebrew_block[0], self.hebrew_block[1], string):
            widget.setFont(QFont(self.hebrew_font))
#        elif self.isInUnicodeRange(self.greek_block[0], self.greek_block[1], string):
#            widget.setFont(QFont(self.greek_font))
    
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
    
    def printFonts(self, filter_str):
        result = []
        print(filter_str, type(filter_str))
        db = QFontDatabase()
        fonts = QFontDatabase.families(db)
        
        for font in fonts:
            print(font, '|', filter_str)
            
            if filter_str == None:
                print("A")
                result.append(str(font))
            
            elif filter_str in font:
                print("B")
                result.append(font)
            
        return result
