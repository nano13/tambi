# -*- coding: utf_8 -*-

from interpreter.loadModules import LoadModules

class Interpreter(object):
    
    modules_list = LoadModules()
    
    def __init__(self):
        pass
    
    def commaSplit(self, input):
        return_args = []
        
        comma_splitted = input[-1].rsplit(",", 1)
        
        try:
            if (comma_splitted[1]).isdigit():
                line = commma_splitted[1]
                return_args = input[:-1]
                
                return_args.append(commma_splitted[0])
            else:
                line = 0
                return_args = input
        except IndexError:
            line = 0
            return_args = input
            
        return return_args, line
    
    def interprete(self, input):
        input = input.strip()
        input = input.replace("\"", "'")
        space_splitted = input.split(None)
        
        try:
            command = space_splitted[0]
        except IndexError:
            print("no input")
            
        args = []
        quotation_found = False
        qoutation_joined = ""
        
        for element in space_splitted[1:]:
            if element.startswith("'"):
                quotation_found = True
                
                if element.endswith("'"):
                    quotation_found = False
                    args.append(element[1:-1])
                else:
                    quotation_joined = element[1:] 
                    # (to drop the quotation mark)
            elif quotation_found:
                if element.endswith("'"):
                    quotation_found = False
                    quotation_joined = quotation_joined + " " + element[:-1]
                    
                    args.append(quotation_joined)
                    quotation_joined = ""
                else:
                    quotation_joined = quotation_joined + " " + element
            else:
                args.append(element)
            
        try:
            args, line = self.commaSplit(args)
        except IndexError:
            line = 0
                
        print("command, args, line:", command, args, line)