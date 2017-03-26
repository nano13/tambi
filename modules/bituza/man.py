
module_description = """
"Bibel in Text und Zahl"
Module for accessing a database for numerological analysis of the bible. This database was created by Paul Gerhard Zint from http://www.zeitundzahl.de/

Particularly interesting could be the also included interlinear translation between the original languages (hebrew, aramaic, greek) and the german 'Elberfelder' translation. This can be accessed by the command "bituza.word"
"""

books = """
Returns a list of books as to be used with the command bituza.word
"""

search_unicode = """
Search the given pattern in the original language.

@param (required): [string], containing the search-pattern.
"""

word = """
Returns the specified bible passage with an interlinear view and all numerological data.

@param (required): [string], the name of the book we want to read. See the command bituza.books.
@param (required): [number], the chapter of the book we want to read.
@param (optional): [number] or [number]-[number], the verse or a range of verses to be shown.

Examples:
bituza.word 1mose 1
bituza.word 1mose 1 1
bituza.word 1mose 1 10-20
"""

structure = """
Returns the structure of the bible or the specified book

@param (optional): [string], the name of the book we want to see the structure for.

Examples:
bituza.structure
bituza.structure jona
"""
