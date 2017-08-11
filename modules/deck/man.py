
module_description = """
This module provides some functionality for searching and managing the data in the decks.
"""

summary = """
Returns a summary of a deck containing the descriptions and the filenames as strings.

@param (required): string, representing the name of the deck.

Examples:
deck.summary arabic_alphabet (returns the summary of the deck "arabic_alphabet")
"""

count = """
Counts how many entries are in all decks / decks with the given prefix.

@param (optional): string, representing the prefix/beginning of the decks we want to count the entries in.

Examples:
deck.count (returns how many entries are in all decks together)
deck.count arabic_ (returns how many entries are in all decks prefixed with "arabic_")
"""

search = """
Returns a list of decks where the given search-pattern could be found in.

@param (required): string, representing the search-pattern we want to look for.

Examples:
deck.search Buch (returns which decks contains the string "Buch" somewhere)
"""
