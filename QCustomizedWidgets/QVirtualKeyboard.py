# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal

import functools

class QVirtualKeyboard(QMainWindow):
    
    keyPressedAny = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("virtual keyboard")
        self.resize(450, 150)
        
        self.drawKeyboard("ar", "qwertz")
        
        self.show()
        
    def drawKeyboard(self, language, layout):
        chars = self.getChars(language)
        keys = self.getKeys(layout)
        
        line_pos = 0
        line_width = 30
        
        #self.drawFirstLine(chars[0], keys[0], line_pos)
        #self.drawSecondLine(chars[1], keys[1], line_pos+line_width)
        #self.drawThirdLine(chars[2], keys[2], line_pos + 2*line_width)
        #self.drawForthLine(chars[3], keys[3], line_pos + 3*line_width)
        #self.drawFifthLine(chars[4], keys[4], line_pos + 4*line_width)
        self.drawButtons(chars, keys)
        
        self.enter = QPushButton("\u23ce", self)
        self.enter.resize(50, 60)
        self.enter.move(400, line_pos + line_width)
        
    def drawButtons(self, chars, keys):
        button_sizes = self.getButtonSizes()
        
        for row in range(0, 5):
            for i in range(len(chars[row])):
                button = QPushButton(chars[row][i], self)
                button.resize(button_sizes[row][i], 30)
                button.move(i*30, row*30)
                
                self.connectButton(button, chars[row][i], keys[row][i])
        
    def drawFirstLine(self, chars, keys, line_pos):
        for i in range(len(chars)):
            button = QPushButton(chars[i], self)
            if i == 13:
                button.resize(60, 30)
                button.move(i*30, line_pos)
            else:
                button.resize(30, 30)
                button.move(i*30, line_pos)
            
            self.connectButton(button, chars[i], keys[i])
            #button.show()
    
    def drawSecondLine(self, chars, keys, line_pos):
        for i in range(len(chars)):
            button = QPushButton(chars[i], self)
            if i == 0:
                button.resize(40, 30)
                button.move(i*30, line_pos)
            else:
                button.resize(30, 30)
                button.move((i+.35)*30, line_pos)
            
            self.connectButton(button, chars[i], keys[i])
            
    def drawThirdLine(self, chars, keys, line_pos):
        for i in range(len(chars)):
            button = QPushButton(chars[i], self)
            if i == 0:
                button.resize(50, 30)
                button.move(i*30,line_pos)
            elif i == 12:
                button.resize(20, 30)
                button.move((i+.67)*30, line_pos)
            else:
                button.resize(30, 30)
                button.move((i+.67)*30, line_pos)
                
            self.connectButton(button, chars[i], keys[i])
            
    def drawForthLine(self, chars, keys, line_pos):
        for i in range(len(chars)):
            button = QPushButton(chars[i], self)
            if i == 0:
                button.resize(40, 30)
                button.move(0, line_pos)
            elif i == 12:
                button.resize(80, 30)
                button.move((i+.35)*30, line_pos)
            else:
                button.resize(30, 30)
                button.move((i+.35)*30, line_pos)
                
            self.connectButton(button, chars[i], keys[i])
            
    def drawFifthLine(self, chars, keys, line_pos):
        for i in range(len(chars)):
            button = QPushButton(chars[i], self)
            if i == 3:
                button.resize(150, 30)
                button.move(90, line_pos)
            elif i > 3:
                button.resize(30, 30)
                button.move((i+4)*30, line_pos)
            else:
                button.resize(30, 30)
                button.move(i*30, line_pos)
                
            self.connectButton(button, chars[i], keys[i])
            
    def connectButton(self, button, char, key):
        button.clicked.connect(functools.partial(self.printChar, char))
        self.keyPressedAny.connect(functools.partial(self.keyPressed, key, button))
        
    def printChar(self, char):
        print("char")
        print(char)
        
    def keyPressed(self, key, button, event):
        print("key")
        print(event, key, button)
        
        if event == key:
            button.animateClick()
        
    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_Return:
            pass
        elif e.key() == Qt.Key_Escape:
            pass
        elif e.key() >= Qt.Key_F1 and e.key() <= Qt.Key_F12:
            pass
        else:
            self.keyPressedAny.emit(e.key())
        
    def getChars(self, language):
        if language == "de":
            return self.getGermanChars()
        elif language == "gr":
            return self.getGreekChars()
        elif language == "he":
            return self.getHebrewChars()
        elif language == "ar":
            return self.getArabChars()
        
    def getGreekChars(self):
        return [["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "\u232b"],
                ["⇄", ";", "ς", "ε", "ρ", "τ", "υ", "θ", "ι", "ο", "π", "[", "]"],
                ["\u21ea", "α", "σ", "δ", "φ", "γ", "η", "ξ", "κ", "λ", "´", "'", ""],
                ["\u21E7", "|", "ζ", "χ", "ψ", "ω", "β", "ν", "μ", ",", ".", "/", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
        
    def getHebrewChars(self):
        return [[";", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "\u232b"],
                ["⇄", "/", "'", "ק", "ר", "א", "ט", "ו", "ן", "ם", "פ", "]", "["],
                ["\u21ea", "ש", "ד", "ג", "כ", "ע", "י", "ח", "ל", "ך", "ף", ",", ""],
                ["\u21E7", "", "ז", "ס", "ב", "ה", "נ", "מ", "צ", "ת", "ץ", ".", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
        
    def getGermanChars(self):
        return [["^", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "ß", "´", "\u232b"],
                ["⇄", "q", "w", "e", "r", "t", "z", "u", "i", "o", "p", "ü", "+"],
                ["\u21ea", "a", "s", "d", "f", "g", "h", "j", "k", "l", "ö", "ä", "#"],
                ["\u21E7", "<", "y", "x", "c", "v", "b", "n", "m", ",", "." ,"-", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "agr", "\u2325", "ctrl"]]
        
    def getLevel2GermanChars(self):
        return [["°", "!", "\"", "§", "$", "%", "\u0038", "/", "(", ")", "=", "?", "`", "\u232b"],
                ["⇄", "Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P", "Ü", "*"],
                ["\u21ea", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Ö", "Ä", "'"],
                ["\u21E7", ">", "Y", "X", "C", "V", "B", "N", "M", ";", ":" ,"_", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "agr", "\u2325", "ctrl"]]
    
    def getArabChars(self):
        return [["ذ", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩", "٠", "~", "!", "\u232b"],
                ["⇄", "ض", "ص", "ث", "ق", "ف", "غ", "ع", "ه", "خ", "ح", "ج", "د"],
                ["\u21ea", "ش", "س", "ي", "ب", "ل", "ا", "ت", "ن", "م", "ك", "ط", "\\"],
                ["\u21E7", "ئ", "ء", "ؤ", "ر", "لا", "ى", "ة", "و", "ز", "ظ" ,"ـ", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
        
    "Template for copying it if you want to make new layouts"
    def getCharsTemplate(self):
        return [["", "", "", "", "", "", "", "", "", "", "", "", "", "\u232b"],
                ["⇄", "", "", "", "", "", "", "", "", "", "", "", ""],
                ["\u21ea", "", "", "", "", "", "", "", "", "", "", "", ""],
                ["\u21E7", "", "", "", "", "", "", "", "", "", "", "", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
    
    def getButtonSizes(self):
        return [[30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 60],
                [40, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
                [50, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 20],
                [40, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 80],
                [30, 30, 30, 150, 30, 30, 30, 30, 30, 30, 30]]
    
    def getKeys(self, layout):
        if layout == "qwertz":
            return self.getQwertzKeys()
        
    def getQwertzKeys(self):
        return [[16781906, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9, Qt.Key_0, Qt.Key_ssharp, 16781905, Qt.Key_Backspace],
                [Qt.Key_Tab, Qt.Key_Q, Qt.Key_W, Qt.Key_E, Qt.Key_R, Qt.Key_T, Qt.Key_Z, Qt.Key_U, Qt.Key_I, Qt.Key_O, Qt.Key_P, Qt.Key_Udiaeresis, Qt.Key_Plus],
                [Qt.Key_CapsLock, Qt.Key_A, Qt.Key_S, Qt.Key_D, Qt.Key_F, Qt.Key_G, Qt.Key_H, Qt.Key_J, Qt.Key_K, Qt.Key_L, Qt.Key_Odiaeresis, Qt.Key_Adiaeresis, Qt.Key_NumberSign],
                [Qt.Key_Shift, Qt.Key_Less, Qt.Key_Y, Qt.Key_X, Qt.Key_C, Qt.Key_V, Qt.Key_B, Qt.Key_N, Qt.Key_M, Qt.Key_Comma, Qt.Key_Period, Qt.Key_Minus, -1],
                [Qt.Key_Control, Qt.Key_Meta, Qt.Key_Alt, Qt.Key_Space,  Qt.Key_Left, Qt.Key_Down, Qt.Key_Up, Qt.Key_Right, Qt.Key_AltGr, -1, -1]]
        
if __name__ == "__main__":
    import signal
    # to make program closeable with ctr-c in terminal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    c = QVirtualKeyboard()
    sys.exit(app.exec_())
