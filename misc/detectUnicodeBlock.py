
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

def applyFontSizeToQWidget(string, widget):
    if isArabic(string) or isHebrew(string):
        widget.setFontPointSize(20)
