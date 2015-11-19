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
    
    header = None
    
    name = None
    
    error = None
    
    cursorPosition = None
