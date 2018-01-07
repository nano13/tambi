
from PyQt5.QtGui import QFontDatabase, QFont
import os
import platform

from configs.configFiles import ConfigFile

class UnicodeFonts(object):
    
    config = ConfigFile(None, None)
    
    arabic_block = [1536, 1791]
    hebrew_block = [1424, 1535]
    greek_block = [880, 1023]
    ipa_block = [250, 687]
    
    arabic_font = "Scheherazade"
    hebrew_font = "Ezra SIL"
    greek_font = "Galatia SIL"
    ipa_font = "Doulos SIL"
    
    def __init__(self):
        self.arabic_size = int(self.config.readVar("fonts", "arabic_size"))
        self.hebrew_size = int(self.config.readVar("fonts", "hebrew_size"))
        self.greek_size = int(self.config.readVar("fonts", "greek_size"))
        self.ipa_size = int(self.config.readVar("fonts", "ipa_size"))
        
        scriptpath = os.path.dirname(os.path.abspath(__file__))
        #print(scriptpath)
        #print(os.getcwd())
        fonts = [
            "./assets/fonts/SILEOT.ttf",
            "./assets/fonts/Scheherazade-Regular.ttf",
            #"assets/fonts/Scheherazade-2.100/Scheherazade-Regular.ttf",
            "./assets/fonts/EzraSIL2.51/SILEOT.ttf",
            "./assets/fonts/GalSIL21/GalSILR.ttf",
            "./assets/fonts/DoulosSIL-R.ttf",
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
            
        #self.printFonts('Ezra')
        
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
            #widget.setFont(QFont(self.arabic_font))
            #widget.setFontPointSize(self.arabic_size)
            #self.setFontSize(widget, self.arabic_size)
            font = QFont(self.arabic_font, self.arabic_size, -1, False)
            widget.setFont(font)
        
        elif self.isInUnicodeRange(self.hebrew_block[0], self.hebrew_block[1], string):
            #widget.setFont(QFont(self.hebrew_font))
            #widget.setFontPointSize(self.hebrew_size)
            #self.setFontSize(widget, self.hebrew_size)
            font = QFont(self.hebrew_font, self.hebrew_size, -1, False)
            widget.setFont(font)
        
        elif self.isInUnicodeRange(self.greek_block[0], self.greek_block[1], string):
#            widget.setFont(QFont(self.greek_font))
            #widget.setFontPointSize(self.greek_size)
            self.setFontSize(widget, self.greek_size)
        
        elif self.isInUnicodeRange(self.ipa_block[0], self.ipa_block[1], string):
            #widget.setFont(QFont(self.ipa_font))
            #widget.setFontPointSize(self.ipa_size)
            #self.setFontSize(widget, self.ipa_size)
            pass
    
    def applyFontToQWidget(self, string, widget):
        if self.isInUnicodeRange(self.arabic_block[0], self.arabic_block[1], string):
            widget.setFont(QFont(self.arabic_font))
        elif self.isInUnicodeRange(self.hebrew_block[0], self.hebrew_block[1], string):
            widget.setFont(QFont(self.hebrew_font))
#        elif self.isInUnicodeRange(self.greek_block[0], self.greek_block[1], string):
#            widget.setFont(QFont(self.greek_font))
    
    def setFont(self, font_category, widget):
        if font_category == 'ipa':
            widget.setFont(QFont(self.ipa_font))
            self.setFontSize(widget, self.ipa_size)
    
    def setFontSize(self, widget, size, font_name=None):
        try:
            widget.setFontPointSize(size)
        except AttributeError:
            if font_name:
                font = QFont(font_name, size)
            else:
                font = QFont()
                font.setPointSize(size)
            widget.setFont(font)
    
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
        #print(filter_str, type(filter_str))
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
