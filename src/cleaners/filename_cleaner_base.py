import os, re
import logging

from constants import FILE_EXTENSIONS_TO_SKIP, VIDEO_EXTENSIONS, SUB_EXTENSIONS


logger = logging.getLogger(__name__)


class BaseFilenameCleaner:
    def __init__(self, directory, filename, config=None):
        self.directory = directory
        self.filename_og = filename
        self.filename_working = filename
        _, self.file_extension = os.path.splitext(filename)
        self.changed = False
        self.config = config
        self.pattern = None

    def cleanable(self):
        return not self.file_extension in FILE_EXTENSIONS_TO_SKIP and (
            self.file_extension in VIDEO_EXTENSIONS
            or self.file_extension in SUB_EXTENSIONS
        )

    def formatted(self) -> bool:
        if not self.pattern:
            return False
        filename_no_ext, _ = os.path.splitext(self.filename_og)
        return bool(self.pattern.match(filename_no_ext))

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

    def results(self) -> dict:
        return {
            "filename": self.filename_working,
            "cleanable": self.cleanable(),
            "formatted": self.formatted(),
        }

    def clean_filename(self) -> dict:
        if not self.cleanable():
            logger.debug("File not formattable")
            return self.results()
        elif self.cleanable():
            self.remove_common_fluff()
            self.normalize_separators()
            self.collapse_spaces()
            self.final_cleanup()
        return self.results()
