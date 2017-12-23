#!/usr/bin/env python

import sys, os
os.chdir("..")
sys.path.append(".")

from configs.history import History
history = History()

from interpreter.exceptions import ClearCalled, SnapshotCalled

def historyWrite(text):
    history.historyWrite(text)

def getHistorySize():
    return history.getHistorySize()

def historyReadWithIndexAndPrefix(history_counter, search_pattern_prefix):
    return history.historyReadWithIndexAndPrefix(history_counter, search_pattern_prefix)

def historyReadAtIndex(history_counter):
    return history.historyReadAtIndex(history_counter)


from interpreter.interpreter import Interpreter

from json import JSONEncoder
import json, queue

def interpreter(command):#, queue):
    q = queue.Queue()
    
    c = Interpreter()
    try:
        result = c.interpreter(command, q)
    except ClearCalled:
        result = {"exception": "clear"};
        return json.dumps(result);
    except SnapshotCalled:
        result = {"exception": "snapshot"};
        return json.dumps(result);
    
    else:
        json_string = json.dumps(result.__dict__)
        return json_string
