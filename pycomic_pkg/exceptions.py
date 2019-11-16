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


class FileExistError(pycomicError):
    """
    Raise when file already exist
    """
    pass


class DataIndexError(pycomicError):
    """
    Raise when index out of range finding data
    """
    pass


class CSVError(pycomicError):
    """
    Raise when failed to make action on csv file
    """
    pass


# class CSVContentError(pycomicError):
#     """
#     Raise when failed to find matching data within csv file
#     """
#     pass


class TXTError(pycomicError):
    """
    Raise when failed to make action on txt file
    """
    pass


# class DriverError(pycomicError):
#     """
#     Raise when exception happened on selenium driver
#     """
#     pass


class configError(Exception):
    """
    Base class of config exception
    """
    pass

class ConfigNotFoundError(configError):
    """
    Raise if no config ini file is found
    """
    pass

class NoSectionError(configError):
    """
    Raised by configparser.NoSectionError
    """
    pass

class NoOptionError(configError):
    """
    Raised by configparser.NoOptionError
    """
    pass