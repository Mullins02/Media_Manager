__version__ = "0.1.0"

from .filename_renamer_base import BaseFilenamerenamer
from .filename_renamer_show import ShowFilenamerenamer
from .filename_renamer_movie import MovieFilenamerenamer

RENAMERS = {
    "UNKNOWN": BaseFilenameRenamer,
    "SHOW": ShowFilenameRenamer,
    "MOVIE": MovieFilenameRenamer,
}