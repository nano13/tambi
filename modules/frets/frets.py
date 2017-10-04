
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

class Frets(object):
    def __init__(self):
        pass
    
    def getCommands(self):
        return {
                "frets.commands" : self.commands,
                
                "frets.capo" : self.capo,
                "frets.custom" : self.frets,
                "frets.guitar" : self.fretsGuitar,
                "frets.bass" : self.fretsBass,
                "frets.mandolin" : self.fretsMandolin,
                "frets.cello" : self.fretsCello,
                
                "frets.chord" : self.chord,
                }
    
    def interpreter(self, command, args, queue):
        commands = self.getCommands()
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module 'strings'")
    
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
    
    def fretsGuitar(self, c, a):
        return self.frets("frets", ["e", "a", "d", "g", "h", "e"])
    def fretsBass(self, c, a):
        return self.frets("frets", ["e", "a", "d", "g"])
    def fretsMandolin(self, c, a):
        return self.frets("frets", ["g", "d", "a", "e"])
    def fretsCello(self, c, a):
        return self.frets("frets", ["c", "g", "d", "a"])
    
    def frets(self, c, args):
        if len(args) == 0:
            result_object = Result()
            result_object.error = 'please specify the tuning!'
            return result_object
        
        scale = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]
        head = "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"
        color = [[160, 160, 160], [255, 255, 255], [255, 255, 255], [200, 200, 200],
                 [255, 255, 255], [200, 200, 200], [255, 255, 255], [200, 200, 200],
                 [255, 255, 255], [200, 200, 200], [255, 255, 255], [255, 255, 255],
                 [200, 200, 200]]
        
        # german_notaion: use "h" instead of "b"
        german_notation = False
        for item in args:
            if item == "h":
                german_notation = True
        
        result_table = []
        for item in args:
            if item == "h":
                item = "b"
                
            item = item.lower()
            
            result_line = []
            for i in range(13):
                result_line.append(item)
                
                try:
                    item_index = scale.index(item)
                except ValueError:
                    result_object = Result()
                    result_object.error = 'the specified tone \'' + item + '\' could not be recognized.'
                    return result_object
                    #self.ResultObject.Error.Message = "Fehler: Ton " +item+ " konnte nicht erkannt werden. (Es werden nur die Kreuztonarten erkannt)"
                    #return self.ResultObject
                
                # the successor:
                try:
                    item = scale[item_index + 1]
                except IndexError:
                    item = scale[item_index + 1 -12]
                
            if german_notation:
                result_line = ["h" if x=="b" else x for x in result_line]
                
            result_table.append(result_line)
            
        #self.ResultObject.Payload.Table = result_table[::-1]
        #self.ResultObject.Payload.TableHeader = head
        #self.ResultObject.Payload.TableColorVertical = color
        print(head)
        result_object = Result()
        result_object.category = 'table'
        result_object.payload = result_table[::-1]
        result_object.header = head
        return result_object
    
    def capo(self, c, args):
        scale = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]
        result = self.frets("frets", scale[::-1])
        
        if len(args) == 0:
            #result.Payload.TableColorVertical = None
            return result
        else:
            if not args[0].isdigit():
                result_object = Result()
                result_object.error = 'invalid parameter: parameter has to be a number!'
                return result_object
            
            args = args[::-1]
            args.append("0")
            args = args[::-1]
            
            table = result.payload
            head = result.header
            
            table_new = []
            row_new = []
            head_new = []
            
            for fret in args:
                head_new.append(fret)
                
                for row_num, row in enumerate(table):
                    
                    #for item in row:
                    #    row_new.append(item[5])
                    row_new.append(row[ int(fret) ])
                    
                    if len(table_new) < len(scale):
                        table_new.append(row_new)
                    else:
                        row_a = table_new[row_num]
                        row_a.append(row[ int(fret) ])
                    
                    row_new = []
            
            #self.ResultObject.Payload.Table = table_new
            #self.ResultObject.Payload.TableHeader = head_new
            #self.ResultObject.Payload.TableColorVertical = None
            #return self.ResultObject
            result_object = Result()
            result_object.category = "table"
            result_object.payload = table_new
            result_object.header = head_new
            return result_object
    
    def chord(self, c, args):
        from modules.frets.chords import Chords
        
        chords = Chords()
        result = chords.getAkkorde('dur')
        print(result)
        
        result_object = Result()
        result_object.category = "table"
        result_object.payload = result
        result_object.header = ['grundton', 'terz', 'quinte']
        return result_object
