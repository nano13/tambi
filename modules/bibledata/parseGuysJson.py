
import json

class ParseGuysJson(object):
    def __init__(self):
        
        fobj = open("./data/kings_south.json")
        loaded = json.load(fobj)
        
        for guy in loaded:
            print(guy["name_original"])
        

if __name__ == "__main__":
    c = ParseGuysJson()
