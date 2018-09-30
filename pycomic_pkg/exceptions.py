"""
Exceptions definition of pycomic program

Author:
    haw
"""


class pycomicError(Exception):
    """
    Base class for other exceptions
    """
    pass


class ComicNotFoundError(pycomicError):
    """
    Raise when cannot find comic name
    """
    pass


class UpdateError(pycomicError):
    """
    Raise when failed to update file content
    """
    pass
