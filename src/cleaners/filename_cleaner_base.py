import os, re
from utils.tmdb_helper import TMDB_Utils
import logging

from constants import FILE_EXTENSIONS_TO_SKIP, VIDEO_EXTENSIONS


logger = logging.getLogger(__name__)

class BaseFilenameCleaner():
    def __init__(self, directory, filename, config=None):
        self.directory = directory
        self.filename_og = filename
        self.filename_working = filename
        _, self.file_extension = os.path.splitext(filename)
        self.changed = False
        self.config = config
        self.tmdb = TMDB_Utils()

    def cleanable(self):
        return not self.file_extension in FILE_EXTENSIONS_TO_SKIP and self.file_extension in VIDEO_EXTENSIONS

    def remove_common_fluff(self):
        self.filename_working = self.filename_working.replace(self.file_extension, "")
        self.filename_working = re.sub(r"^\[.*?\]\s*", "", self.filename_working)

    def invalid_char_corrector(self):
        invalid_chars = ["(", ")", "-", ".", ":", "_"]
        for char in invalid_chars:
            self.filename_working = self.filename_working.replace(char, " ")
        self.filename_working = re.sub(r"\s+", " ", self.filename_working).strip()

    def normalize_separators(self) -> str:
        self.filename_working = self.filename_working.replace(".", " ").replace(
            "_", " "
        )

    def collapse_spaces(self) -> str:
        self.filename_working = " ".join(self.filename_working.split())

    def final_cleanup(self) -> str:
        self.filename_working = self.filename_working.strip()

    def compare_og_to_work(self) -> bool:
        return self.filename_og != self.filename_working

    def results(self) -> dict:
        return {"filename": self.filename_working, "changed": self.compare_og_to_work(), "cleanable": self.cleanable()}

    def clean_filename(self) -> dict:
        if not self.cleanable():
            logger.debug("File not formattable")
        elif self.cleanable():
            self.remove_common_fluff()
            self.normalize_separators()
            self.collapse_spaces()
            self.final_cleanup()
        return self.results()
