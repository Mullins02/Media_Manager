import os, re
from tmdb_helper import TMDB_Utils

from constants import FILE_EXTENSIONS_TO_SKIP, VIDEO_EXTENSIONS


class BaseFilenameCleaner():
    def __init__(self, directory, filename, config=None):
        self.directory = directory
        self.filename_og = filename
        self.filename_working = filename
        _, self.file_extension = os.path.splitext(filename)
        self.changed = False
        self.config = config
        self.tmdb = TMDB_Utils()

    def format_file(self):
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
        return {"filename": self.filename_working, "changed": self.compare_og_to_work()}

    def clean_filename(self) -> str:
        if not self.format_file():
            print("Skipped file type")
        elif self.format_file():
            self.remove_common_fluff()
            self.normalize_separators()
            self.collapse_spaces()
            self.final_cleanup()
        return self.results()
