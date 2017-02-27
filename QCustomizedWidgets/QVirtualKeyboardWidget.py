# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QComboBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import pyqtSignal, QEvent

import functools
import math

class QVirtualKeyboardWidget(QWidget):
    
    keyPressedAny = pyqtSignal(int)
    lineEdit = None
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("virtual keyboard")
        self.resize(450, 150)
        
        #self.language = None
        self.keys = None
        self.chars = None
        self.level_two_chars = None
        
        self.modifier = Qt.NoModifier
        
    def setLineEdit(self, lineEdit):
        self.lineEdit = lineEdit
        
    def drawKeyboard(self, layout, language):
        self.chars, self.level_two_chars = self.getChars(language)
        self.keys = self.getKeys(layout)
        
        self.drawButtons(self.chars, self.keys)
        
        #self.enter = QPushButton("\u23ce", self)
        #self.enter.resize(50, 60)
        #self.enter.move(400, line_pos + line_width)
        
    def drawLevelTwoKeyboard(self):
        self.destroyKeyboard()
        
        self.drawButtons(self.level_two_chars, self.keys)
        
    def drawButtons(self, chars, keys):
        button_sizes = self.getButtonSizes()
        
        for row in range(0, 5):
            
            row_offset = 0
            for i in range(len(chars[row])):
                
                if i > 0:
                    
                    button_a, button_b = button_sizes[row][i-1], button_sizes[row][i]
                    
                    if button_a > button_b:
                        if button_b >= 30:
                            offset = button_a / button_b
                            row_offset = row_offset + offset - 1
                
                #button = QPushButton(chars[row][i], self)
                button = QVkeybdPushButton(chars[row][i], self)
                button.resize(button_sizes[row][i], 30)
                button.move((i + row_offset)*30, row*30)
                button.show()
                
                self.connectButton(button, chars[row][i], keys[row][i])
            
    def connectButton(self, button, char, key):
        button.clicked.connect(functools.partial(self.printChar, char))
        self.keyPressedAny.connect(functools.partial(self.keyPressed, key, button))
        
    def printChar(self, char):
        if self.lineEdit:
            if char == '⇄':
                print("TAB PRESSED")
            elif char == '↑':
                event = QKeyEvent(QEvent.KeyPress, Qt.Key_Up, Qt.NoModifier)
                self.lineEdit.keyPressEvent(event)
            elif char == '↓':
                event = QKeyEvent(QEvent.KeyPress, Qt.Key_Down, Qt.NoModifier)
                self.lineEdit.keyPressEvent(event)
            elif char == '←':
                event = QKeyEvent(QEvent.KeyPress, Qt.Key_Left, Qt.NoModifier)
                self.lineEdit.keyPressEvent(event)
            elif char == '→':
                event = QKeyEvent(QEvent.KeyPress, Qt.Key_Right, Qt.NoModifier)
                self.lineEdit.keyPressEvent(event)
            elif char == '⏎':
                event = QKeyEvent(QEvent.KeyPress, Qt.Key_Enter, Qt.NoModifier)
                self.lineEdit.keyPressEvent(event)
            elif char == '⌫':
                event = QKeyEvent(QEvent.KeyPress, Qt.Key_Backspace, Qt.NoModifier)
                self.lineEdit.keyPressEvent(event)
            elif char == '⇧':
                self.modifier = Qt.ShiftModifier
                self.drawLevelTwoKeyboard()
            elif char == '⇪':
                print("CAPSLOCK PRESSED")
            elif char == 'ctrl':
                print("CONTROL PRESSED")
            elif char == 'alt':
                print("ALT PRESSED")
            elif char == '⌘':
                print("WIndows key pressed")
            elif char == '⌥':
                print("anykey pressed")
            else:
                self.lineEdit.appendText(char)
        else:
            print(char)
        
    def keyPressed(self, key, button, event):
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
        if language == "german":
            return self.getGermanChars(), self.getLevel2GermanChars()
        elif language == "greek":
            return self.getGreekChars(), None
        elif language == "hebrew":
            return self.getHebrewChars(), None
        elif language == "arabic":
            return self.getArabChars(), None
        elif language == "hindi":
            return self.getDevanagariChars(), None
        elif language == "futhark":
            return self.getFutharkChars(), None
        else:
            return self.getHebrewChars(), None
        
    def getGreekChars(self):
        return [["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "\u232b"],
                ["⇄", ";", "ς", "ε", "ρ", "τ", "υ", "θ", "ι", "ο", "π", "[", "]", ""],
                ["\u21ea", "α", "σ", "δ", "φ", "γ", "η", "ξ", "κ", "λ", "´", "'", "\u23ce"],
                ["\u21E7", "|", "ζ", "χ", "ψ", "ω", "β", "ν", "μ", ",", ".", "/", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
        
    def getHebrewChars(self):
        return [[";", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "\u232b"],
                ["⇄", "/", "'", "ק", "ר", "א", "ט", "ו", "ן", "ם", "פ", "]", "[", ""],
                ["\u21ea", "ש", "ד", "ג", "כ", "ע", "י", "ח", "ל", "ך", "ף", ",", "\u23ce"],
                ["\u21E7", "", "ז", "ס", "ב", "ה", "נ", "מ", "צ", "ת", "ץ", ".", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
        
    def getGermanChars(self):
        return [["^", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "ß", "´", "\u232b"],
                ["⇄", "q", "w", "e", "r", "t", "z", "u", "i", "o", "p", "ü", "+", "#"],
                ["\u21ea", "a", "s", "d", "f", "g", "h", "j", "k", "l", "ö", "ä", "\u23ce"],
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
                ["⇄", "ض", "ص", "ث", "ق", "ف", "غ", "ع", "ه", "خ", "ح", "ج", "د", "\\"],
                ["\u21ea", "ش", "س", "ي", "ب", "ل", "ا", "ت", "ن", "م", "ك", "ط", "\u23ce"],
                ["\u21E7", "ئ", "ء", "ؤ", "ر", "لا", "ى", "ة", "و", "ز", "ظ" ,"ـ", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
        
    def getDevanagariChars(self):
        return [["ॊ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "ृ", "\u232b"],
                ["⇄", "ौ", "ै", "ा", "ी", "ू", "ब", "ह", "ग", "द", "ज", "ड", "ड़", "़"],
                ["\u21ea", "ो", "े", "्", "ि", "ु", "प", "र", "क", "त", "च", "ट", "\u23ce"],
                ["\u21E7", "ॆ", "ं", "म", "न", "व", "ल", "स", ",", ".", "य" ,"", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
    
    def getFutharkChars(self):
        return [["ᛢ", "ᚨ", "\u16b1", "", "", "", "", "", "", "", "", "", "", "\u232b"],
                ["⇄", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                ["\u21ea", "", "", "", "", "", "", "", "", "", "", "", "\u23ce"],
                ["\u21E7", "", "", "", "", "", "", "", "", "", "" ,"ـ", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
    
    "Template for copying it if you want to make new layouts"
    def getCharsTemplate(self):
        return [["", "", "", "", "", "", "", "", "", "", "", "", "", "\u232b"],
                ["⇄", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                ["\u21ea", "", "", "", "", "", "", "", "", "", "", "", "\u23ce"],
                ["\u21E7", "", "", "", "", "", "", "", "", "", "" ,"ـ", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
    
    def getButtonSizes(self):
        return [[30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 60],
                [40, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 50],
                [50, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 70],
                [40, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 80],
                [30, 30, 30, 150, 30, 30, 30, 30, 30, 30, 30]]
    
    def getKeys(self, layout):
        if layout == "qwertz":
            return self.getQwertzKeys()
        else:
            return self.getQwertzKeys()
        
    def getQwertzKeys(self):
        return [[16781906, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9, Qt.Key_0, Qt.Key_ssharp, 16781905, Qt.Key_Backspace],
                [Qt.Key_Tab, Qt.Key_Q, Qt.Key_W, Qt.Key_E, Qt.Key_R, Qt.Key_T, Qt.Key_Z, Qt.Key_U, Qt.Key_I, Qt.Key_O, Qt.Key_P, Qt.Key_Udiaeresis, Qt.Key_Plus, Qt.Key_NumberSign],
                [Qt.Key_CapsLock, Qt.Key_A, Qt.Key_S, Qt.Key_D, Qt.Key_F, Qt.Key_G, Qt.Key_H, Qt.Key_J, Qt.Key_K, Qt.Key_L, Qt.Key_Odiaeresis, Qt.Key_Adiaeresis, Qt.Key_Return],
                [Qt.Key_Shift, Qt.Key_Less, Qt.Key_Y, Qt.Key_X, Qt.Key_C, Qt.Key_V, Qt.Key_B, Qt.Key_N, Qt.Key_M, Qt.Key_Comma, Qt.Key_Period, Qt.Key_Minus, -1],
                [Qt.Key_Control, Qt.Key_Meta, Qt.Key_Alt, Qt.Key_Space,  Qt.Key_Left, Qt.Key_Down, Qt.Key_Up, Qt.Key_Right, Qt.Key_AltGr, -1, -1]]
    
    def destroyKeyboard(self):
        for button in self.findChildren(QVkeybdPushButton):
            button.clicked.disconnect()
            button.deleteLater()
        
        self.keyPressedAny.disconnect()
        
    
class QVkeybdPushButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            e.ignore()
        elif e.key() == Qt.Key_Left:
            e.ignore()
        elif e.key() == Qt.Key_Right:
            e.ignore()
        elif e.key() == Qt.Key_Up:
            e.ignore()
        elif e.key() == Qt.Key_Down:
            e.ignore()
        elif e.key() == Qt.Key_Escape:
            e.ignore()
        elif e.key() == Qt.Key_Tab:
            e.ignore()
        elif e.key() == Qt.Key_Return:
            e.ignore()
        elif e.key() == Qt.Key_Dead_Circumflex:
            e.ignore()
        else:
            super().keyPressEvent(e)
    
