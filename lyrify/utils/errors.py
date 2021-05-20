
class SongOrderLengthError(ValueError):
    # Used when the number of values given in the order argument does not equal
    # the number of music files in the given folder path.
    pass

class SongOrderRangeError(ValueError):
    # Used when a range value (eg. 7-10) was entered incorrectly.
    pass

class SongOrderError(ValueError):
    pass

class SongOrderValueError(ValueError):
    pass