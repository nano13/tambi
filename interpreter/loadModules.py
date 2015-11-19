# -*- coding: utf_8 -*-

import os

class LoadModules(object):
    def __init__(self):
        pass
    
    def loadModules(self):
        modules_list = []
        
        base, dirs, files = next(iter(os.walk('./modules')))
        dirs.sort()
        
        try:
            for d in dirs:
                if d == "__pycache__":
                    continue
                
                print("\n")
                imports = "from modules."+d+"."+d+" import "+d[0].upper() + d[1:]+" as CurrentModule"
                print("importing: ",imports)
                
                try:
                    exec(imports, globals())
                    
                    try:
                        current_module = CurrentModule()
                        
                        modules_list.append(current_module)
                    except Exception as e:
                        print("Could not instantiate: CurrentModule = CurrentModule()")
                        print("ERROR:", e)
                except Exception as e:
                    print("Could not load module:", imports)
                    print("ERROR:", e)
        except Exception as e:
            print("ERROR while importing modules:", e)
            
        return modules_list