# -*- coding: utf_8 -*-

from interpreter.coreCommands import CoreCommands
from interpreter.loadModules import LoadModules
from interpreter.exceptions import CommandNotInThisModule

class Interpreter(object):
    
    core_commands = CoreCommands()
    modules_list = LoadModules().loadModules()
    
    def __init__(self):
        pass
    
    def commaSplit(self, input_):
        return_args = []
        
        comma_splitted = input_[-1].rsplit(",", 1)
        
        try:
            if (comma_splitted[1]).isdigit():
                line = comma_splitted[1]
                return_args = input_[:-1]
                
                return_args.append(comma_splitted[0])
            else:
                line = 0
                return_args = input_
        except IndexError:
            line = 0
            return_args = input_
            
        return return_args, line
    
    def interpreter(self, input_, queue):
        input_ = input_.strip()
        input_ = input_.replace("\"", "'")
        space_splitted = input_.split(None)
        
        try:
            command = space_splitted[0]
        except IndexError:
            print("no input_")
            
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
        
        try:
            print("command, args, line:", command, args, line)
        except UnboundLocalError:
            # we have probably an empty input_ here
            return
        
        result = self.tryCommandInCoreCommands(command, args, queue)
        try:
            result.cursorPosition = line
        except AttributeError:
            pass
        
        return result
    
    def tryCommandInCoreCommands(self, command, args, queue):
        try:
            return_value = self.core_commands.execute(command, args, queue)
        except CommandNotInThisModule:
            return self.tryCommandInModules(command, args, queue)
        else:
            return return_value
    
    def tryCommandInModules(self, command, args, queue):
        for current_module in self.modules_list:
            try:
                return_value = current_module.interpreter(command, args, queue)
            except CommandNotInThisModule:
                pass
            else:
                return return_value

if __name__ == '__main__':
    c = Interpreter()
    
