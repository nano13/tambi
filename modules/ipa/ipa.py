
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

class Ipa(object):
    
    
    
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
            "ipa.commands" : self.commands,
            
            "ipa.vowels" : self.vowels,
            "ipa.consonants" : self.consonants,
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
    
    def vowels(self, c, a):
        vowels = self.getVowelsDict()
        
        result_table = [['' for _ in range(6)] for _ in range(6)]
        keys = vowels.keys()
        for key in keys:
            position = vowels[key]
            result_table[position[0]][position[1]] = key
        
        header = ['VV', 'VV o', 'ZV', 'ZV o', 'HV', 'HV o']
        header_left = ['geschl.', 'fast geschl.', 'halb geschl.', 'halb offen', 'halb offen', 'fast offen', 'offen']
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = result_table
        result_object.header = header
        result_object.header_left = header_left
        return result_object
    
    def consonants(self, c, a):
        consonants = self.getConsonantsDict()
        
        result_table = [['' for _ in range(15)] for _ in range(20)]
        keys = consonants.keys()
        for key in keys:
            position = consonants[key]
            try:
                result_table[position[0]][position[1]] = key
            except IndexError:
                pass
        
        header = ['bl', 'ld', 'd', 'al', 'post-al', 're', 'al-pal', 'pal', 'lab-pal', 'vel', 'lab-vel', 'uv', 'phar', 'epi', 'glot']
        header_left = ['plosiv (stl)', 'plosiv (sth)', 'nasal (stl)', 'nasal (sth)', 'frikativ (stl)', 'frikativ (sth)', 'rinnen-frik (stl)', 'rinnen-frik (sth)', 'lateral-frik (stl)', 'lateral-frik (sth)', 'lateral-approx (stl)', 'lateral-approx (sth)', 'vibrant (stl)', 'vibrant (sth)', 'flap (stl)', 'flap (sth)', 'approx (stl)', 'approx (sth)', 'ejektiv (stl)', 'click']
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = result_table
        result_object.header = header
        result_object.header_left = header_left
        return result_object
    
    def getVowelsDict(self):
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
    
    def getConsonantsDict(self):
        return {
            #= plosive =
            'p' : [0, 0],
            'b' : [1, 0],
            't' : [0, 3],
            'd' : [1, 3],
            'ʈ' : [0, 5],
            'ɖ' : [1, 5],
            'c' : [0, 7],
            'ɟ' : [1, 7],
            'k' : [0, 9],
            'ɡ' : [1, 9],
            'q' : [0, 11],
            'ɢ' : [1, 11],
            'ʔ' : [0, 14],
            #= nasal =
            'm' : [3, 0],
            'ɱ' : [3, 1],
            'n' : [3, 3],
            'ɳ' : [3, 5],
            'ɲ' : [3, 7],
            'ŋ' : [3, 9],
            'ɴ' : [3, 11],
            #= trill =
            'ʙ' : [13, 0],
            'r' : [13, 3],
            'ʀ' : [13, 11],
            #= tap or flap =
            #'v<' : '', # !!!
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
            
            's' : [6, 3],
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
            'l' : [11, 3],
            'ɭ' : [11, 5],
            'ʎ' : [11, 7],
            'ʟ' : [11, 9],
            #== other consonants ==
            #= clicks =
            'ʘ' : [19, 0],
            'ǀ' : [19, 2],
            'ǃ' : [19, 3],
            'ǂ' : [19, 4],
            'ǁ' : [19, 3],
            #= voiced implosives =
            'ɓ' : [],
            'ɗ' : [],
            'ʄ' : [],
            'ɠ' : [],
            'ʛ' : [],
            
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
