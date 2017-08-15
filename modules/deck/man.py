
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

ipaVowels = """
Returns the IPA table with all vowels found in the specified decks.

@param (optional): string, representing the prefix/beginning of the decks we want to generate the IPA-table from.

Examples:
deck.ipaVowels (generates and returns the ipa-table for all decks)
deck.ipaVowels arabic_ (generates and returns the ipa-table for all decks prefixed with "arabic_")
"""

ipaConsonants = """
Returns the IPA table with all consonants found in the specified decks.

@param (optional): string, representing the prefix/beginning of the decks we want to generate the IPA-table from.

Examples:
deck.ipaConsonants (generates and returns the ipa-table for all decks)
deck.ipaConsonants arabic_ (generates and returns the ipa-table for all decks prefixed with "arabic_")
"""

chronological = """
Returns a table showing which deck item was created on wich date.

@param (optional): string, representing the prefix/beginning of the decks we want to generate the IPA-table from.

Examples:
deck.chronological (shows the chronological order of all deck entries)
deck.chronological arabic_ (shows the chronological order of all items of all decks whose name starts with "arabic_*")
"""

search = """
Returns a list of decks where the given search-pattern could be found in.

@param (required): string, representing the search-pattern we want to look for.

Examples:
deck.search Buch (returns which decks contains the string "Buch" somewhere)
"""
