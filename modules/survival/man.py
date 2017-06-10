
module_description = """
Module for offline reading and studying the survival-manual found at https://github.com/ligi/SurvivalManual/wiki
"""

toc = """
Returns the table of contents ordered alphabetically.
"""

read = """
Use this command to read any chapter of the survival-manual included in this module.

@param (required): string, representing the case-sensitive name of the chapter
Returns the HTML-formatted chapter for reading and studying.

Examples:
survival.read Tropical

See also:
survival.toc for getting the names of the available chapters.
"""

search = """
Returns a list of modules the given search-pattern could be found in.

@param (required): string, the search-pattern. If the search-pattern contains spaces, enclose the whole pattern with double quotes: ""

Examples:
survival.search oily
survival.search "oily skin"
"""
