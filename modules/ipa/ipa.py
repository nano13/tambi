
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

DENTAL = chr(810)
VOICELESS = chr(805)

class Ipa(object):
    
    
    
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "ipa.commands" : self.commands,
            
            "ipa.vowels" : self.generateRawIpaTable,
            "ipa.consonants" : self.generateRawIpaTable,
        }
    
    def interpreter(self, command, args):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module vocable")
    
    def commands(self, none1, none2):
        dic = self.getCommands()
        
        commands = sorted(dic.items())
        
        all_commands = []
        for key in commands:
            line = str(key).split(",")[0]
            all_commands.append(str(line[2:-1]))
            
        result_object = Result()
        result_object.category = "list"
        result_object.payload = all_commands
        return result_object
    
    def generateRawIpaTable(self, command, a):
        if command == 'ipa.vowels':
            phones = self.__getVowelsDict()
            result_table, header, header_vertical = self.__getVowelsRawTable()
        elif command == 'ipa.consonants':
            phones = self.__getConsonantsDict()
            result_table, header, header_vertical = self.__getConsonantsRawTable()
        
        keys = phones.keys()
        for key in keys:
            position = phones[key]
            try:
                result_table[position[0]][position[1]] = key
            except IndexError:
                pass
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = result_table
        result_object.header = header
        result_object.header_left = header_vertical
        return result_object
    
    def _generateIpaTableFromData(self, table_type, string_data):
        if table_type == 'vowels':
            phones = self.__getVowelsDict()
            result_table, header, header_vertical = self.__getVowelsRawTable()
        elif table_type == 'consonants':
            phones = self.__getConsonantsDict()
            result_table, header, header_vertical = self.__getConsonantsRawTable()
        
        for char in string_data:
            if char in phones:
                position = phones[char]
                result_table[position[0]][position[1]] = char
        
        return result_table, header, header_vertical
    
    def __getVowelsRawTable(self):
        header = ['VV', 'VV o', 'ZV', 'ZV o', 'HV', 'HV o']
        header_vertical = ['geschl.', 'fast geschl.', 'halb geschl.', 'halb offen', 'fast offen', 'offen']
        
        table = [['' for _ in range(6)] for _ in range(6)]
        
        return table, header, header_vertical
    
    def __getConsonantsRawTable(self):
        header = ['bl', 'ld', 'd', 'al', 'post-al', 're', 'al-pal', 'pal', 'lab-pal', 'vel', 'lab-vel', 'uv', 'phar', 'epi', 'glot']
        header_vertical = ['plosiv (stl)', 'plosiv (sth)', 'nasal (stl)', 'nasal (sth)', 'frikativ (stl)', 'frikativ (sth)', 'rinnen-frik (stl)', 'rinnen-frik (sth)', 'lateral-frik (stl)', 'lateral-frik (sth)', 'lateral-approx (stl)', 'lateral-approx (sth)', 'vibrant (stl)', 'vibrant (sth)', 'flap (stl)', 'flap (sth)', 'approx (stl)', 'approx (sth)', 'implosiv (stl)', 'implosiv (sth)', 'ejektiv (stl)', 'click']
        
        table = [['' for _ in range(15)] for _ in range(22)]
        
        return table, header, header_vertical
    
    def __getVowelsDict(self):
        return {
            'i' : [0, 0],
            'y' : [0, 1],
            'ɨ' : [0, 2],
            'ʉ' : [0, 3],
            'ɯ' : [0, 4],
            'u' : [0, 5],
            #= near-close =
            'ɪ' : [1, 0],
            'ʏ' : [1, 1],
            'ʊ' : [1, 5],
            #= close-mid =
            'e' : [2, 0],
            'ø' : [2, 1],
            'ɘ' : [2, 2],
            'ɵ' : [1, 3],
            'ɤ' : [2, 4],
            'o' : [2, 5],
            #= mid =
            'ə' : [2, 2],
            #= open-mid =
            'ɛ' : [3, 0],
            'œ' : [3, 1],
            #'ɜ' : [],
            'ɞ' : [3, 3],
            'ʌ' : [3, 4],
            'ɔ' : [3, 5],
            #= near-open =
            'æ' : [4, 0],
            'ɐ' : [4, 2],
            #= open =
            'a' : [5, 0],
            'ɶ' : [5, 1],
            'ɑ' : [5, 4],
            'ɒ' : [5, 5],
            }
    
    def __getConsonantsDict(self):
        return {
            #= plosive =
            'p' : [0, 0],
            'b' : [1, 0],
            't'+DENTAL : [0, 2],
            't' : [0, 3],
            'd'+DENTAL : [1, 2],
            'd' : [1, 3],
            'ʈ' : [0, 5],
            'ɖ' : [1, 5],
            'c' : [0, 7],
            'ɟ' : [1, 7],
            'k' : [0, 9],
            'g' : [1, 9],
            'g' : [1, 9],
            
            'q' : [0, 11],
            'ɢ' : [1, 11],
            'ʔ' : [0, 14],
            #= nasal =
            'm'+VOICELESS : [2, 0],
            'ɱ'+VOICELESS : [2, 1],
            'n'+DENTAL+VOICELESS : [2, 2],
            'n'+VOICELESS : [2, 3],
            'ɳ'+VOICELESS : [2, 5],
            'ɲ'+VOICELESS : [2, 7],
            'ŋ'+VOICELESS : [2, 9],
            'ɴ'+VOICELESS : [2, 11],
            
            'm' : [3, 0],
            'ɱ' : [3, 1],
            'n'+DENTAL : [3, 2],
            'n' : [3, 3],
            'ɳ' : [3, 5],
            'ɲ' : [3, 7],
            'ŋ' : [3, 9],
            'ɴ' : [3, 11],
            #= trill =
            'ʙ' : [13, 0],
            'r'+DENTAL : [13, 2],
            'r' : [13, 3],
            'ʀ' : [13, 11],
            #= tap or flap =
            #'v<' : '', # !!!
            'ɾ'+DENTAL : [15, 2],
            'ɾ' : [15, 3],
            'ɽ' : [15, 5],
            #= fricative =
            'ɸ' : [4, 0],
            'β' : [5, 0],
            'f' : [4, 1],
            'v' : [5, 1],
            'θ' : [4, 2],
            'ð' : [5, 2],
            'ç' : [4, 7],
            'ʝ' : [5, 7],
            'x' : [4, 9],
            'ɣ' : [5, 9],
            'χ' : [4, 11],
            'ʁ' : [5, 11],
            'ħ' : [4, 12],
            'ʕ' : [5, 12],
            'h' : [4, 14],
            'ɦ' : [5, 14],
            
            's'+DENTAL : [6, 2],
            's' : [6, 3],
            'z'+DENTAL : [7, 2],
            'z' : [7, 3],
            'ʃ' : [6, 4],
            'ʒ' : [7, 4],
            'ʂ' : [6, 5],
            'ʐ' : [7, 5],
            #= lateral fricative =
            'ɬ' : [8, 3],
            'ɮ' : [9, 3],
            #= approximate =
            'ʋ' : [17, 2],
            'ɹ' : [17, 3],
            'ɻ' : [17, 5],
            'j' : [17, 7],
            'ɰ' : [17, 9],
            #= lateral approximate =
            'l'+DENTAL : [11, 2],
            'l' : [11, 3],
            'ɭ' : [11, 5],
            'ʎ' : [11, 7],
            'ʟ' : [11, 9],
            #== other consonants ==
            #= clicks =
            'ʘ' : [21, 0],
            'ǀ' : [21, 2],
            'ǃ' : [21, 3],
            'ǂ' : [21, 4],
            'ǁ' : [21, 3],
            #= voiced implosives =
            'ɓ' : [19, 0],
            'ɗ' : [19, 2],
            'ɗ' : [19, 3],
            'ʄ' : [19, 7],
            'ɠ' : [19, 9],
            'ʛ' : [19, 11],
            
            #== other symbols ==
            'ʍ' : [4, 10],
            'w' : [17, 10],
            'ɥ' : [17, 8], # or h=
            'ʜ' : [4, 13],
            'ʢ' : [5, 13],
            'ʡ' : [0, 13],
            
            'ɕ' : [6, 6],
            'ʑ' : [7, 6],
            'ɺ' : [],
            'ɧ' : [],
            }
