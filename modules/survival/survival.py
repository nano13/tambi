
from interpreter.exceptions import CommandNotInThisModule
from interpreter.structs import Result

import markdown
import codecs

import os

MODULE_PATH = os.path.join(os.getcwd(), 'modules', 'survival', 'SurvivalManual')

class Survival(object):
    def __init__(self):
        pass
         
    def getCommands(self):
        return {
            "survival.commands" : self.commands,
            
            "survival.toc" : self.tableOfContents,
            "survival.read" : self.read,
            "survival.search" : self.search,
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
        
        filepath = MODULE_PATH + os.sep + args[0]+".md"
        
        if not os.path.exists(filepath):
            result_object = Result()
            result_object.error = 'chapter '+args[0]+' not found'
            return result_object
        
        input_file = input_file = codecs.open(filepath, mode="r", encoding="utf-8")
        md_file = input_file.read()
        html = '<h1>'+args[0]+'</h1>'
        html += markdown.markdown(md_file, extensions=[
            'markdown.extensions.sane_lists',
            'markdown.extensions.nl2br',
            'markdown.extensions.extra',
            'markdown.extensions.tables',
        ])
        
        folderpath = '/modules/survival/guide/'.replace('/', os.sep)
        html = html.replace('src="', 'src="' + MODULE_PATH + os.sep)
        html = html.replace('<table>', '<table border="1">')
        
        #fobj = open("/tmp/mktest.html", "w")
        #fobj.write(html)
        #fobj.close()
        
        result_object = Result()
        result_object.category = "html"
        result_object.payload = html
        return result_object
    
    def tableOfContents(self, c, a):
        base, dirs, files = next(iter(os.walk(MODULE_PATH)))
        
        result = []
        for f in files:
            splitted = f.split('.')
            if splitted[1] == 'md':
                result.append(splitted[0])
        
        result_object = Result()
        result_object.category = 'list'
        result_object.payload = sorted(result)
        return result_object
    
    def search(self, c, args):
        try:
            pattern = args[0]
        except:
            result_object = Result()
            result_object.error = 'you have to specify a search-pattern'
            return result_object
        else:
            import fileinput, glob, string
            result = []
            for line in fileinput.input(glob.glob(MODULE_PATH + os.sep + '*.md')):
                
                num_matches = line.lower().count(pattern.lower())
                if num_matches:
                    filepath = fileinput.filename()
                    filename = filepath.replace(MODULE_PATH + os.sep, '').replace('.md', '')
                    if not filename in result:
                        result.append(filename)
                    else:
                        pass
                        # we could raise a counter here to show, how often the pattern was found in one module ...
            
            result_object = Result()
            result_object.category = 'list'
            result_object.payload = result
            return result_object
    
