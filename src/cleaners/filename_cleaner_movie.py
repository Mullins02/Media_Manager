import re
import logging

from constants import MOVIE_PATTERN_TEMPLATE, MOVIE_DETAIL_PATTERN_TEMPLATE

from cleaners.filename_cleaner_base import BaseFilenameCleaner


logger = logging.getLogger(__name__)
class MovieFilenameCleaner(BaseFilenameCleaner):
    def __init__(self, directory: str, filename: str):
        super().__init__(directory, filename)

    def build_movie_pattern(
        self,
    ):
        pattern = MOVIE_PATTERN_TEMPLATE
        return re.compile(pattern, re.IGNORECASE)

    def extract_movie_details(self):
        match = re.match(MOVIE_DETAIL_PATTERN_TEMPLATE, self.filename_working)
        title = None
        year = None
        if match:
            title = match.group(1).strip()
            year = match.group(2)
        return {"title": title, "year": year}

    def clean_filename(self) -> str:
        if not self.cleanable():
            logger.debug("Skipped file type")
        elif self.build_movie_pattern().match(self.filename_og):
            logger.debug("Already formatted")
        else:
            self.remove_common_fluff()
            self.invalid_char_corrector()
            self.collapse_spaces()
            movie_details = self.extract_movie_details()
            if movie_details == {"title": None, "year": None}:
                logger.debug(f"failed to format {self.filename_og}")
                self.filename_working = f"{self.filename_og}"
            else:
                self.filename_working = f"{movie_details['title']} ({movie_details['year']}){self.file_extension}"
            self.final_cleanup()
        return self.results()
