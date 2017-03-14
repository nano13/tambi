
from PyQt5.QtGui import QFontDatabase, QFont

def isArabic(string):
    #return all(ord(char) > 1536 and ord(char) < 1791 for char in string)
    result = False
    for char in string.strip():
        if ord(char) > 1536 and ord(char) < 1791:
            result = True
    return result

def isHebrew(string):
    #return all(ord(char) > 1424 and ord(char) < 1535 for char in string)
    result = False
    for char in string.strip():
        if ord(char) > 1424 and ord(char) < 1535:
            result = True
    return result 

def applyCoranicaFontToQWidget(widget):
    QFontDatabase.addApplicationFont("./assets/fonts/Scheherazade-2.100/Scheherazade-Regular.ttf")
    font = QFont("Scheherazade")
    widget.setFont(font)

def applyHebrewFontToQWidget(widget):
    QFontDatabase.addApplicationFont("./assets/fonts/EzraSIL2.51/SILEOT.ttf")
    font = QFont("Ezra SIL")
    widget.setFont(font)
    
    printFonts()

def applyFontSizeToQWidget(string, widget):
    if isArabic(string):
        applyCoranicaFontToQWidget(widget)
        widget.setFontPointSize(40)
    
    if isHebrew(string):
        applyHebrewFontToQWidget(widget)
        widget.setFontPointSize(20)

def printFonts():
    db = QFontDatabase()
    fonts = QFontDatabase.families(db)
    for font in fonts:
        #if font.find("zra"):
        print(font)
