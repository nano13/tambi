#!/bin/env python
# coding: UTF-8

# ! use python3 !

import sys

SKALA_GANZTON = ["a", "b", "c", "d", "e", "f", "g"]
SKALA_HALBTON = ["a", "ais", "b", "c", "cis", "d", "dis", "e", "f", "fis", "g", "gis"]

QUINTENZIRKEL = ["g", "d", "a", "e"]

KLEINE_TERZ = 3
GROSSE_TERZ = 4
QUINTE = 5
GROSSE_SEPTIME = 11
KLEINE_SEPTIME = 10

class Chords(object):
    def __init__(self):
        args = sys.argv
        if "-a" in args:
            self.skala = SKALA_HALBTON
        else:
            self.skala = SKALA_GANZTON
        
    def getAkkorde(self, tonart):
        result = []
        result_line = []
        for grundton in self.skala:
            for note in self.getAkkord(grundton, tonart):
                if note != None:
                    #print(note, end="\t")
                    result_line.append(note)
                    
            result.append(result_line)
            result_line = []
            
        return result
        
    def printAkkorde(self, tonart):
        for grundton in self.skala:
            for note in self.getAkkord(grundton, tonart):
                if note != None:
                    print(note, end="\t")
                
            print("\n", end="")
            
    def getAkkord(self, grundton, tonart):
        index = SKALA_HALBTON.index(grundton)
        
        first_index = None
        second_index = None
        third_index = None
        
        first_note = None
        second_note = None
        third_note = None
        
        if tonart == "dur":
            first_index = self.handleOverflow(index + GROSSE_TERZ)
            second_index = self.handleOverflow(index + GROSSE_TERZ + KLEINE_TERZ)
        elif tonart == "moll":
            first_index = self.handleOverflow(index + KLEINE_TERZ)
            second_index = self.handleOverflow(index + KLEINE_TERZ + GROSSE_TERZ)
        elif tonart == "dur_sept":
            first_index = self.handleOverflow(index + GROSSE_TERZ)
            second_index = self.handleOverflow(index + GROSSE_TERZ + KLEINE_TERZ)
            third_index = self.handleOverflow(index + GROSSE_SEPTIME)
        elif tonart == "moll_sept":
            first_index = self.handleOverflow(index + KLEINE_TERZ)
            second_index = self.handleOverflow(index + KLEINE_TERZ + GROSSE_TERZ)
            third_index = self.handleOverflow(index + KLEINE_SEPTIME)
        
        if first_index != None:
            first_note = SKALA_HALBTON[first_index]
        if second_index != None:
            second_note = SKALA_HALBTON[second_index]
        if third_index != None:
            third_note = SKALA_HALBTON[third_index]
        
        return [grundton, first_note, second_note, third_note]
            
    def handleOverflow(self, index):
        if index >= len(SKALA_HALBTON):
            return index - len(SKALA_HALBTON)
        else:
            return index
    
class Tabs(object):
    def __init__(self):
        chords = Chords()
        
    def printTabs(self):
        pass
    
    def getSaite(self):
        pass
    
if __name__ == "__main__":
    c = Chords()
    
    print("Dur")
    c.printAkkorde("dur")
    print("\nmoll")
    c.printAkkorde("moll")
    print("\nDur-7")
    c.printAkkorde("dur_sept")
    print("\nmoll-7")
    c.printAkkorde("moll_sept")
    
    t = Tabs()
