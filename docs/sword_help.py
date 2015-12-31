
fobj = open("./sword_help_raw.txt", "r")

content = []
for line in fobj:
    
    new_line = ""
    last_char_was_shit = False
    for char in line:
        if char == "":
            last_char_was_shit = True
        else:
            if not last_char_was_shit:
                new_line += char
                
            last_char_was_shit = False
            
    content.append(new_line)
            

fobj.close()

fobj = open("./sword_help.txt", "w")

for line in content:
    fobj.write(line)
fobj.close()