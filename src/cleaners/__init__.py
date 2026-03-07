__version__ = "0.1.0"

from .filename_cleaner_base import BaseFilenameCleaner
from .filename_cleaner_show import ShowFilenameCleaner
from .filename_cleaner_movie import MovieFilenameCleaner
# from .filename_cleaner_special import SpecialFilenameCleaner

CLEANERS = {
    "UNKNOWN": None,
    "SHOW": ShowFilenameCleaner,
    "MOVIE": MovieFilenameCleaner,
    # "SPECIAL": SpecialFilenameCleaner,
}
