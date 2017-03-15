
module_description = """
Module for providing a dictionary for multiple languages.

DEPENDENCIES:
Module 'vocable' for providing the language-databases.
"""

hebrew = """
Looks for the given word (englisch or hebrew) and returns the according translation in the other language.

@param (required): [string], the word you want to look for.

Examples:
dictionary.hebrew heaven
dictionary.hebrew שָׁמַיִם
"""

greek = """
Looks for the given word (englisch or greek) and returns the according translation in the other language.

@param (required): [string], the word you want to look for.

Examples:
dictionary.greek more
dictionary.greek και
"""

aramaic = """
Looks for the given word (englisch or aramaic) and returns the according translation in the other language.

@param (required): [string], the word you want to look for.

Examples:
dictionary.aramaic man
dictionary.aramaic אֱנָשׁ
"""

akkadian = """
Looks for the given word (englisch or akkadian) and returns the according translation in the other language.

@param (required): [string], the word you want to look for.

Examples:
dictionary.akkadian man
dictionary.akkadian awīlum
"""
