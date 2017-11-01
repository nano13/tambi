
module_description = """
On this interface you can access some built in commands and other commands provided by additional modules.

To get an idea of what you can do here, you can try to:
- type the command 'commands' for getting a list of the builtin ones
- type the command 'modules' for getting a list of the available modules
- type the command '[modulename].commands' for getting a list of the available commands provided by this module
- type the command 'man [command]' for getting a description of the builtin command
- type the command 'man [modulename]' for getting a description of the module
- type the command 'man [modulename].[command]' for getting a description of the particular command provided by the given modulename
"""

commands = """
Returns a list of all builtin commands.
"""

commandline = """
The command line is for typing in commands.

Use the up and the down arrow keys for navigating the history up or down.

Type in the command 'man' to get started with an overview, what you can do here.
"""

modules = """
Returns a list of all available modules.
"""

man = """
Returns a description of the given command.

Examples:
man history
man sword
man sword.word
"""

clear = """
Clears the display.
"""

exit = """
Quits this program.
"""

date = """
Returns the current date.
"""

time = """
Returns the current time.
"""

history = """
Returns the history of the commands you have typed in the command line interface with the last command on the top

@param (optional): [string], filter for commands containing this string.

Examples:
history
history story
"""

fonts = """
Returns a list of all available fonts in this software.

@param (optional): [string], filter the result list for fonts only contains this string in the name.

Examples:
fonts
fonts TeX
"""

snapshot = """
Makes a snapshot of the content which is actually displayed.
"""
