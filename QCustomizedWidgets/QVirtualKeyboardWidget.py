# -*- coding: utf_8 -*-

from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QComboBox, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent, QColor
from PyQt5.QtCore import pyqtSignal, QEvent

from misc.unicodeFonts import UnicodeFonts

import functools
import math

class QVirtualKeyboardWidget(QWidget):
    
    keyPressedAny = pyqtSignal(int)
    lineEdit = None
    
    layout = None
    language = None
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("virtual keyboard")
        self.resize(450, 150)
        
        self.unicode_fonts = UnicodeFonts()
        
        #self.language = None
        self.keys = None
        self.level_one_chars = None
        self.level_two_chars = None
        
        self.modifier = Qt.NoModifier
        
        self.ipa_keyboard = IPAKeyboard()
        
    def setLineEdit(self, lineEdit):
        self.lineEdit = lineEdit
        
    def drawKeyboard(self, layout, language):
        self.layout, self.language = layout, language
        
        self.level_one_chars, self.level_two_chars = self.getChars(language)
        self.keys = self.getKeys(layout)
        
        self.drawButtons(self.level_one_chars, self.keys)
        
        #self.enter = QPushButton("\u23ce", self)
        #self.enter.resize(50, 60)
        #self.enter.move(400, line_pos + line_width)
        
    def drawLevelOneKeyboard(self):
        self.destroyKeyboard()
        self.drawButtons(self.level_one_chars, self.keys)
    def drawLevelTwoKeyboard(self):
        self.destroyKeyboard()
        self.drawButtons(self.level_two_chars, self.keys)
        
    def drawButtons(self, chars, keys):
        button_sizes = self.getButtonSizes()
        button_colors = self.getButtonColors()
        
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
                self.unicode_fonts.applyFontToQWidgetFiltered(chars[row][i], button, ['hebrew'])
                button.resize(button_sizes[row][i], 30)
                button.move((i + row_offset)*30, row*30)
                
                r, g, b = button_colors[row][i]
                button.setBackgroundColor(QColor(r, g, b))
                
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
                # shift
                self.modifier = Qt.ShiftModifier
                self.drawLevelTwoKeyboard()
            elif char == '⇪':
                # capslock
                if self.modifier == Qt.ShiftModifier:
                    self.modifier = Qt.NoModifier
                    self.drawLevelOneKeyboard()
                elif self.modifier == Qt.NoModifier:
                    self.modifier = Qt.ShiftModifier
                    self.drawLevelTwoKeyboard()
            elif char == 'ctrl':
                print("CONTROL PRESSED")
            elif char == 'alt':
                print("ALT PRESSED")
            elif char == '⌘':
                print("WIndows key pressed")
            elif char == '⌥':
                print("anykey pressed")
            else:
                if self.language == "ipa":
                    ipa_char = self.ipa_keyboard.analyzeInput(char)
                    if ipa_char:
                        event = QKeyEvent(QEvent.KeyPress, Qt.Key_Backspace, Qt.NoModifier)
                        self.lineEdit.keyPressEvent(event)
                        
                        char = ipa_char
                
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
            return self.getGreekChars(), self.getLevel2GreekChars()
        elif language == "hebrew":
            return self.getHebrewChars(), self.getLevel2HebrewChars()
        elif language == "arabic":
            return self.getArabicChars(), self.getLevel2ArabicChars()
        elif language == "hindi":
            return self.getDevanagariChars(), self.getLevel2DevanagariChars()
        elif language == "futhark":
            return self.getFutharkChars(), self.getLevel2FutharkChars()
        elif language == "ipa":
            return self.getGermanChars(), self.getLevel2GermanChars()
        else:
            return self.getHebrewChars(), self.getLevel2HebrewChars()
        
    def getGreekChars(self):
        return [["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "\u232b"],
                ["⇄", ";", "ς", "ε", "ρ", "τ", "υ", "θ", "ι", "ο", "π", "[", "]", ""],
                ["\u21ea", "α", "σ", "δ", "φ", "γ", "η", "ξ", "κ", "λ", "´", "'", "\u23ce"],
                ["\u21E7", "", "ζ", "χ", "ψ", "ω", "β", "ν", "μ", ",", ".", "/", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
    def getLevel2GreekChars(self):
        return [["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "\u232b"],
                ["⇄", ";", "Σ", "Ε", "Ρ", "Τ", "Υ", "Θ", "Ι", "Ο", "Π", "[", "]", ""],
                ["\u21ea", "Α", "Σ", "Δ", "Φ", "Γ", "Η", "Ξ", "Κ", "Λ", "΄", "'", "\u23ce"],
                ["\u21E7", "", "Ζ", "Χ", "Ψ", "Ω", "Β", "Ν", "Μ", ",", ".", "/", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
        
    def getHebrewChars(self):
        return [[";", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "\u232b"],
                ["⇄", "/", "'", "ק", "ר", "א", "ט", "ו", "ן", "ם", "פ", "]", "[", ""],
                ["\u21ea", "ש", "ד", "ג", "כ", "ע", "י", "ח", "ל", "ך", "ף", ",", "\u23ce"],
                ["\u21E7", "", "ז", "ס", "ב", "ה", "נ", "מ", "צ", "ת", "ץ", ".", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
    def getLevel2HebrewChars(self):
        return [[";", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "\u232b"],
                ["⇄", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "]", "[", ""],
                ["\u21ea", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "\u23ce"],
                ["\u21E7", "", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/" , "\u21E7"],
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
    
    def getArabicChars(self):
        return [["ذ", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩", "٠", "~", "!", "\u232b"],
                ["⇄", "ض", "ص", "ث", "ق", "ف", "غ", "ع", "ه", "خ", "ح", "ج", "د", "\\"],
                ["\u21ea", "ش", "س", "ي", "ب", "ل", "ا", "ت", "ن", "م", "ك", "ط", "\u23ce"],
                ["\u21E7", "ئ", "ء", "ؤ", "ر", "لا", "ى", "ة", "و", "ز", "ظ" ,"ـ", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
    def getLevel2ArabicChars(self):
        return [["", "", "", "", "", "", "", "", "", "", "", "", "", "\u232b"],
                ["⇄", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                ["\u21ea", "", "", "", "", "", "", "", "", "", "", "", "\u23ce"],
                ["\u21E7", "", "", "", "", "", "", "", "", "", "" ,"ـ", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
        
    def getDevanagariChars(self):
        return [["ॊ", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "ृ", "\u232b"],
                ["⇄", "ौ", "ै", "ा", "ी", "ू", "ब", "ह", "ग", "द", "ज", "ड", "ड़", "़"],
                ["\u21ea", "ो", "े", "्", "ि", "ु", "प", "र", "क", "त", "च", "ट", "\u23ce"],
                ["\u21E7", "ॆ", "ं", "म", "न", "व", "ल", "स", ",", ".", "य" ,"", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
    
    def getLevel2DevanagariChars(self):
        return [["", "", "", "", "", "", "", "", "", "", "", "", "", "\u232b"],
                ["⇄", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                ["\u21ea", "", "", "", "", "", "", "", "", "", "", "", "\u23ce"],
                ["\u21E7", "", "", "", "", "", "", "", "", "", "" ,"ـ", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
    
    def getFutharkChars(self):
        return [["ᛢ", "ᚨ", "\u16b1", "", "", "", "", "", "", "", "", "", "", "\u232b"],
                ["⇄", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                ["\u21ea", "", "", "", "", "", "", "", "", "", "", "", "\u23ce"],
                ["\u21E7", "", "", "", "", "", "", "", "", "", "" ,"ـ", "\u21E7"],
                ["ctrl", "\u2318", "alt", " ", "←", "↓", "↑", "→", "alt", "\u2325", "ctrl"]]
    
    def getLevel2FutharkChars(self):
        return [["", "", "", "", "", "", "", "", "", "", "", "", "", "\u232b"],
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
        elif layout == "neo":
            return self.getNeoKeys()
        else:
            return self.getQwertzKeys()
        
    def getQwertzKeys(self):
        return [[16781906, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9, Qt.Key_0, Qt.Key_ssharp, 16781905, Qt.Key_Backspace],
                [Qt.Key_Tab, Qt.Key_Q, Qt.Key_W, Qt.Key_E, Qt.Key_R, Qt.Key_T, Qt.Key_Z, Qt.Key_U, Qt.Key_I, Qt.Key_O, Qt.Key_P, Qt.Key_Udiaeresis, Qt.Key_Plus, Qt.Key_NumberSign],
                [Qt.Key_CapsLock, Qt.Key_A, Qt.Key_S, Qt.Key_D, Qt.Key_F, Qt.Key_G, Qt.Key_H, Qt.Key_J, Qt.Key_K, Qt.Key_L, Qt.Key_Odiaeresis, Qt.Key_Adiaeresis, Qt.Key_Return],
                [Qt.Key_Shift, Qt.Key_Less, Qt.Key_Y, Qt.Key_X, Qt.Key_C, Qt.Key_V, Qt.Key_B, Qt.Key_N, Qt.Key_M, Qt.Key_Comma, Qt.Key_Period, Qt.Key_Minus, -1],
                [Qt.Key_Control, Qt.Key_Meta, Qt.Key_Alt, Qt.Key_Space,  Qt.Key_Left, Qt.Key_Down, Qt.Key_Up, Qt.Key_Right, Qt.Key_AltGr, -1, -1]]
    
    def getNeoKeys(self):
        return [[16781906, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9, Qt.Key_0, Qt.Key_Minus, 16781905, Qt.Key_Backspace],
                [Qt.Key_Tab, Qt.Key_X, Qt.Key_V, Qt.Key_L, Qt.Key_C, Qt.Key_W, Qt.Key_K, Qt.Key_H, Qt.Key_G, Qt.Key_F, Qt.Key_Q, Qt.Key_ssharp, Qt.Key_Plus, Qt.Key_NumberSign],
                [Qt.Key_CapsLock, Qt.Key_U, Qt.Key_I, Qt.Key_A, Qt.Key_E, Qt.Key_O, Qt.Key_S, Qt.Key_N, Qt.Key_R, Qt.Key_T, Qt.Key_D, Qt.Key_Y, Qt.Key_Return],
                [Qt.Key_Shift, Qt.Key_Less, Qt.Key_Udiaeresis, Qt.Key_Odiaeresis, Qt.Key_Adiaeresis, Qt.Key_P, Qt.Key_Z, Qt.Key_B, Qt.Key_M, Qt.Key_Comma, Qt.Key_Period, Qt.Key_Minus, -1],
                [Qt.Key_Control, Qt.Key_Meta, Qt.Key_Alt, Qt.Key_Space,  Qt.Key_Left, Qt.Key_Down, Qt.Key_Up, Qt.Key_Right, Qt.Key_AltGr, -1, -1]]
    
    def getButtonColors(self):
        a = [255, 255, 255]
        b = [200, 200, 200]
        c = a
        d = b
        e = b
        f = a
        g = b
        h = a
        
        x = [127, 127, 127]
        z = [145, 145, 145]
        return [[a, a, a, b, c, d, d, e, e, f, g, h, h, z],
                [z, a, b, c, d, d, e, e, f, g, h, h, h, h],
                [z, a, b, c, x, d, e, x, f, g, h, h, z],
                [z, a, a, b, c, d, d, e, e, f, g, h, z],
                [z, z, z, z, z, z, z, z, z, z, z]]
    
    def destroyKeyboard(self):
        for button in self.findChildren(QVkeybdPushButton):
            button.clicked.disconnect()
            button.deleteLater()
        
        self.keyPressedAny.disconnect()
        

from PyQt5.QtGui import QPalette
class QVkeybdPushButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
    
    def setBackgroundColor(self, color):
        palette = QPalette()
        palette.setColor(QPalette.Button, color)
        #palette.setColor(QPalette.Foreground, color)
        self.setPalette(palette)
        #self.setAutoFillBackground(True)
    
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
    
class IPAKeyboard(object):
    
    last_char = ''
    
    def __init__(self):
        pass
    
    def analyzeInput(self, char):
        ipa_dict = self.getInputIPADict()
        
        ipa_char = None
        if char in ipa_dict:
            print("00000 if 00000")
            ipa_char = ipa_dict[char]
        if self.last_char+char in ipa_dict:
            print("00000 double 00000")
            ipa_char = ipa_dict[self.last_char+char]
        #else:
        #    print("00000 else 00000")
        #    ipa_char = char
        
        self.last_char = char
        return ipa_char
    
    def getInputIPADict(self):
        return {
            #== consonants ==
            #= plosive =
            'p' : 'p',
            'b' : 'b',
            't' : 't',
            'd' : 'd',
            't<' : 'ʈ',
            'd<' : 'ɖ',
            'c' : 'c',
            'j=' : 'ɟ',
            'k' : 'k',
            'g<' : 'ɡ',
            'q' : 'q',
            'G=' : 'ɢ',
            '?=' : 'ʔ',
            #= nasal =
            'm' : 'm',
            'm>' : 'ɱ',
            'n' : 'n',
            'n<' : 'ɳ',
            'n=' : 'ɲ',
            'n>' : 'ŋ',
            'N=' : 'ɴ',
            #= trill =
            'B=' : 'ʙ',
            'r' : 'r',
            'R=' : 'ʀ',
            #= tap or flap =
            'v<' : '', # !!!
            'r>' : 'ɾ',
            'r<' : 'ɽ',
            #= fricative =
            'f=' : 'ɸ',
            'b=' : 'β',
            'f' : 'f',
            'v' : 'v',
            't=' : 'θ',
            'd=' : 'ð',
            's' : 's',
            'z' : 'z',
            's=' : 'ʃ',
            'z=' : 'ʒ',
            's<' : 'ʂ',
            'z<' : 'ʐ',
            'c=' : 'ç',
            'j<' : 'ʝ',
            'x' : 'x',
            'g=' : 'ɣ',
            'x=' : 'χ',
            'R>' : 'ʁ',
            'h>' : 'ħ',
            '?<' : 'ʕ',
            'h' : 'h',
            'h<' : 'ɦ',
            #= lateral fricative =
            'l=' : 'ɬ',
            'l>' : 'ɮ',
            #= approximate =
            'v=' : 'ʋ',
            'r=' : 'ɹ',
            'R<' : 'ɻ',
            'j' : 'j',
            'w>' : 'ɰ',
            #= lateral approximate =
            'l' : 'l',
            'l<' : 'ɭ',
            'L<' : 'ʎ',
            'L=' : 'ʟ',
            
            #== other consonants ==
            #= clicks =
            'p=' : 'ʘ',
            '!<' : 'ǀ',
            '!' : 'ǃ',
            '!=' : 'ǂ',
            '!>' : 'ǁ',
            #= voiced implosives =
            'b>' : 'ɓ',
            'd>' : 'ɗ',
            'j>' : 'ʄ',
            'g>' : 'ɠ',
            'G>' : 'ʛ',
            
            #== other symbols ==
            'w=' : 'ʍ',
            'w' : 'w',
            'y<' : 'ɥ', # or h=
            'H=' : 'ʜ',
            'Q<' : 'ʢ',
            'Q=' : 'ʡ',
            
            'c<' : 'ɕ',
            'z>' : 'ʑ',
            'L>' : 'ɺ',
            'H>' : 'ɧ',
            
            #== vowels ==
            #= close =
            'i' : 'i',
            'y' : 'y',
            'I=' : 'ɨ',
            'U=' : 'ʉ',
            'u=' : 'ɯ',
            'u' : 'u',
            #= near-close =
            'i=' : 'ɪ',
            'y=' : 'ʏ',
            'u<' : 'ʊ',
            #= close-mid =
            'e' : 'e',
            'o>' : 'ø',
            'E=' : 'ɘ',
            'O=' : 'ɵ',
            'O>' : 'ɤ',
            'o' : 'o',
            #= mid =
            'e=' : 'ə',
            #= open-mid =
            'e<' : 'ɛ',
            'E<' : 'œ',
            'e>' : 'ɜ',
            'O<' : 'ɞ',
            'u>' : 'ʌ',
            'o<' : 'ɔ',
            #= near-open =
            'a<' : 'æ',
            'a>' : 'ɐ',
            #= open =
            'a' : 'a',
            'E>' : 'ɶ',
            'a=' : 'ɑ',
            'o=' : 'ɒ',
            
            #== suprasegmentals ==
            '}' : 'ˈ',
            '}}' : 'ˌ',
            ':' : 'ː',
            '::' : 'ˑ',
            ':::' : 'ːː',
            '***' : '', # !!!
            '.<' : '|',
            '.=' : '‖',
            '.' : '.',
            '#=' : '‿',
            
            '' : '',
            '' : '',
            '' : '',
            '' : '',
            '' : '',
            '' : '',
            '' : '',
            '' : '',
            '' : '',
            '' : '',
            '' : '',
            '' : '',
            '' : '',
            '' : '',
        }
