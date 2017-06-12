
module_description = """
Module for calculating tone positions on a string based instrument.
"""

capo = """
Returns the transformation matrix for the specified capo position.

@param (optional): numeric, the capo-position.
With an empty param, this returns the whole capo-matrix (for 12 frets).

Examples:
frets.capo 5
"""

custom = """
Returns the fret matrix for a specified tuning.

@param (required): list of strings, representing the tuning

Examples:
frets.custom e a d g b e
"""

guitar = """
Returns the fret matrix for the default guitar-tuning.

Hint: This is a shortcut for:
frets.custom e a d g b e
"""

bass = """
Return the fret matrix for the default bass-tuning.

Hint: This is a shortcut for:
frets.custom e a d g
"""

mandolin = """
Returns the fret matrix for the default mandolin-tuning.

Hint: This is a shortcut for:
frets.custom g d a e
"""

cello = """
Returns the tone-positions for the default cello-tuning.

Hint: This is a shortcut for:
frets.custom c g d a
"""
