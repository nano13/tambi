
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

import markdown
import codecs

import os


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
    
    def read(self, c, args):
        if len(args) <= 0:
            result_object = Result()
            result_object.error = 'please specify the chapter you want to read. see for the command "survival.toc"'
            return result_object
        
        path_prefix = os.getcwd()
        filepath = "/modules/survival/guide/"+args[0]+".md".replace('/', os.sep)
        print(filepath)
        
        if not os.path.exists(path_prefix+filepath):
            result_object = Result()
            result_object.error = 'chapter '+args[0]+' not found'
            return result_object
        
        input_file = input_file = codecs.open(path_prefix+filepath, mode="r", encoding="utf-8")
        md_file = input_file.read()
        html = '<h1>'+args[0]+'</h1>'
        html += markdown.markdown(md_file, extensions=[
            'markdown.extensions.sane_lists',
            'markdown.extensions.nl2br',
            'markdown.extensions.extra',
            'markdown.extensions.tables',
        ])
        
        folderpath = '/modules/survival/guide/'.replace('/', os.sep)
        html = html.replace('src="', 'src="'+path_prefix+folderpath)
        html = html.replace('<table>', '<table border="1">')
        
        #fobj = open("/home/samuel/tmp/mktest.html", "w")
        #fobj.write(html)
        #fobj.close()
        
        result_object = Result()
        result_object.category = "html"
        result_object.payload = html
        return result_object
    
    def tableOfContents(self, c, a):
        base, dirs, files = next(iter(os.walk(os.path.join(os.getcwd() + '/modules/survival/guide'.replace('/', os.sep)))))
        
        result = []
        for f in files:
            splitted = f.split('.')
            if splitted[1] == 'md':
                result.append(splitted[0])
        
        result_object = Result()
        result_object.category = 'list'
        result_object.payload = sorted(result)
        return result_object
        
