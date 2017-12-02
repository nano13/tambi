#!/usr/bin/env python

import sys, os
os.chdir("..")
sys.path.append('.')
print(os.getcwd())

from interpreter.interpreter import Interpreter

from json import JSONEncoder
import json, queue

def interpreter(command):#, queue):
    q = queue.Queue()
    
    c = Interpreter()
    result = c.interpreter(command, q)
    
    json_string = json.dumps(result.__dict__)
    
    return json_string
