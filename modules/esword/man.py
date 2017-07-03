
module_description = """
Module for reading the .mybible modules prepared for esword.
"""

word = """
Returns the specified bible passage.

@param (required): [string], the name of the book we want to read. (If it contains spaces, put it between double quotation marks).
@param (required): [number], the chapter of the book we want to read.
@param (optional): [number] or [number]-[number], the verse or a range of verses to be shown.

Examples:
sword.word markus 1
sword.word markus 1 1
sword.word markus 1 10-20
"""

interlinear = """
Returns the specified bible passage in an interlinear view.

@param (required): [string], the name of the book we want to read. (If it contains spaces, put it between double quotation marks).
@param (required): [number], the chapter of the book we want to read.
@param (optional): [number] or [number]-[number], the verse or a range of verses to be shown.

Examples:
sword.word markus 1
sword.word markus 1 1
sword.word markus 1 10-20
"""
