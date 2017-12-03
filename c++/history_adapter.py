#!/usr/bin/env python

import sys, os
os.chdir("..")
sys.path.append(".")

from configs.history import History

history = History()

def historyWrite(text):
    history.historyWrite(text)

def getHistorySize():
    return history.getHistorySize()

def historyReadWithIndexAndPrefix(history_counter, search_pattern_prefix):
    return history.historyReadWithIndexAndPrefix(history_counter, search_pattern_prefix)

def historyReadAtIndex(history_counter):
    return history.historyReadAtIndex(history_counter)
