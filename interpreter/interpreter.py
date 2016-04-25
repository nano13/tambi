# -*- coding: utf_8 -*-

from interpreter.coreCommands import CoreCommands
from interpreter.loadModules import LoadModules
from interpreter.exceptions import CommandNotInThisModule

class Interpreter(object):
    
    core_commands = CoreCommands()
    modules_list = LoadModules().loadModules()
    
    def __init__(self):
        pass
    
    def commaSplit(self, input):
        return_args = []
        
        comma_splitted = input[-1].rsplit(",", 1)
        
        try:
            if (comma_splitted[1]).isdigit():
                line = comma_splitted[1]
                return_args = input[:-1]
                
                return_args.append(comma_splitted[0])
            else:
                line = 0
                return_args = input
        except IndexError:
            line = 0
            return_args = input
            
        return return_args, line
    
    def interpreter(self, input):
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
        
        result = self.tryCommandInCoreCommands(command, args)
        try:
            result.cursorPosition = line
        except AttributeError:
            pass
        
        return result
    
    def tryCommandInCoreCommands(self, command, args):
        try:
            return_value = self.core_commands.execute(command, args)
        except CommandNotInThisModule:
            return self.tryCommandInModules(command, args)
        else:
            return return_value
    
    def tryCommandInModules(self, command, args):
        for current_module in self.modules_list:
            try:
                return_value = current_module.interpreter(command, args)
            except CommandNotInThisModule:
                pass
            else:
                return return_value
