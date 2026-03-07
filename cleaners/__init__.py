__version__ = "0.1.0"

from .filename_cleaner_base import BaseFilenameCleaner
from .filename_cleaner_show import ShowFilenameCleaner
from .filename_cleaner_movie import MovieFilenameCleaner

CLEANERS = {
    "UNKNOWN": BaseFilenameCleaner,
    "SHOW": ShowFilenameCleaner,
    "MOVIE": MovieFilenameCleaner,
}