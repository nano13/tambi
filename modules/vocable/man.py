
module_description = """
This module provides some functionality for searching and managing the data in the decks.
"""

summary = """
Returns a summary of a deck containing the descriptions and the filenames as strings.

@param (required): string, representing the name of the deck.

Examples:
vocable.summary arabic_alphabet (returns the summary of the deck "arabic_alphabet")
"""

search = """
Returns a list of decks where the given search-pattern could be found in.

@param (required): string, representing the search-pattern we want to look for.

Examples:
vocable.search Buch (returns which decks contains the string "Buch" somewhere)
"""
