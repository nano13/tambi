
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

import markdown
import markdown2
import codecs


class Survival(object):
    def __init__(self):
        pass
         
    def getCommands(self):
        return {
            "survival.commands" : self.commands,
            
            "survival.toc" : self.tableOfContents,
            
            "survival.read" : self.read,
        }
    
    def interpreter(self, command, args):
        print("args:", args)
        
        commands = self.getCommands()
        
        return commands.get(command, self.commandNotFound)(command, args)
    
    def commandNotFound(self, c, a):
        raise CommandNotInThisModule("command not found in module survival")
    
    def commands(self, none1, none2):
        dic = self.getCommands()
        
        commands = sorted(dic.items())
        
        all_commands = []
        for key in commands:
            line = str(key).split(",")[0]
            all_commands.append(str(line[2:-1]))
            
        result_object = Result()
        result_object.category = "list"
        result_object.payload = all_commands
        return result_object
    
    def read(self, c, a):
        input_file = input_file = codecs.open("/home/samuel/programmierung/logos/modules/survival/guide/Camouflage.md", mode="r", encoding="utf-8")
        md_file = input_file.read()
        html = markdown.markdown(md_file, extensions=['markdown.extensions.sane_lists', 'markdown.extensions.nl2br', 'markdown.extensions.extra', 'markdown.extensions.tables'])
        
        html = html.replace('src="', 'src="/home/samuel/programmierung/logos/modules/survival/guide/')
        html = html.replace('<table>', '<table border="1">')
        
        fobj = open("/home/samuel/tmp/mktest.html", "w")
        fobj.write(html)
        fobj.close()
        
        result_object = Result()
        result_object.category = "html"
        result_object.payload = html
        return result_object
    
    def tableOfContents(self, c, a):
        pass
