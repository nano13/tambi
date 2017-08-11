# -*- coding: utf_8 -*-

class Result:
    # category is one of:
    # - table
    # - list
    # - text
    # - string
    # - error
    # (as a string)
    category = None
    
    payload = None
    metaload = None
    
    # header is a list or None
    header = None
    header_left = None
    
    # name is a string or None
    name = None
    
    error = None
    
    cursorPosition = None
    
    def toString(self):
        result = ""
        if type(self.payload) == list:
            for line in self.payload:
                for column in line:
                    result += str(column)
                    if type(line) == tuple or type(line) == list:
                        result += " | "
                if type(line) == tuple or type(line) == list:
                    result = result[:-3]
                result += "\n"
            result = result.strip()
        else:
            result = self.payload
        return result
