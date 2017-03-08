
module_description = """
Module for reading and studying the quran. The containing text was downloaded using a bot from the project at http://corpuscoranicum.de/ without any licence or permission on 2017/02/15.
"""

order = """
Returns a list of the surahs in the chronological order.

@param (optional): number, representing a surah
Returns a list of three numbers (or two for the first or last surah) with the predecessing, the given and the following surah.
"""

search = """
@param (required): [string], the search-pattern. If the search-pattern contains spaces, surround it with double quotation marks (e.g. quran.search "Sinn war")

This command searches automatically in the arabic verse, the latin transcription and the german translation. The exact search pattern in SQL is: "LIKE '%[string]%'".
"""

word = """
Returns the quran text as the original arabic, the latin transcription and the german translation.

@param (required): [number], representing a surah.

@param (optional): [number] or [number]-[number], representing an ayah (verse) or a range of them.

Examples:
quran.word 2 (returns the whole second surah)
quran.word 2 1 (returns just the first ayah of the second surah)
quran.word 2 1-10 (returns the first ten ayahs of the second surah)
"""

word_ar = """
Returns the arabic text.

@param (required): [number], representing a surah.

@param (optional): [number] or [number]-[number], representing an ayah (verse) or a range of them.

Examples:
quran.word.ar 2 (returns the whole second surah)
quran.word.ar 2 1 (returns just the first ayah of the second surah)
quran.word.ar 2 1-10 (returns the first ten ayahs of the second surah)
"""

word_de = """
Returns the german text.

@param (required): [number], representing a surah.

@param (optional): [number] or [number]-[number], representing an ayah (verse) or a range of them.

Examples:
quran.word.de 2 (returns the whole second surah)
quran.word.de 2 1 (returns just the first ayah of the second surah)
quran.word.de 2 1-10 (returns the first ten ayahs of the second surah)
"""
