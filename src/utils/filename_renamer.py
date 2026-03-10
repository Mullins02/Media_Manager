import os, re
import logging

from constants import MOVIE_DETAIL_PATTERN_TEMPLATE, FORMATTED_EPISODE_DETAIL_PATTERN
from utils.metadata_utils import MetadataUtils

logger = logging.getLogger(__name__)


class FilenameRenamer:

    # def __init__(self, directory, filename, config=None):
    def __init__(self):
        self.meta = MetadataUtils()
        # self.tvbd = TVDBClient()
        self.movie_detail_pattern = re.compile(MOVIE_DETAIL_PATTERN_TEMPLATE)
        self.episode_detail_pattern = re.compile(FORMATTED_EPISODE_DETAIL_PATTERN)

    def results_renamer(
        self, filename_og: str, filename_cln: str, filename_db: str
    ) -> dict:
        return {
            "filename_og": filename_og,
            "filename_cln": filename_cln,
            "filename_db": filename_db,
        }

    def get_correct_movie_title(self, filename_cln: str) -> str:
        _, file_ext = os.path.splitext(filename_cln)
        movie_detail_match = self.movie_detail_pattern.search(filename_cln)
        if not movie_detail_match:
            return filename_cln
        title = movie_detail_match.group(1).strip()
        year = movie_detail_match.group(2)
        movie_details = self.meta.get_details_movie(title, year)
        if not movie_details:
            return filename_cln
        return f'{movie_details["formatted_title"]}{file_ext}'

    def get_correct_episode_title(
        self, filename_cln: str, library_item: str = None
    ) -> str:
        if not library_item:
            return filename_cln

        _, file_ext = os.path.splitext(filename_cln)

        episode_match = self.episode_detail_pattern.search(filename_cln)
        if not episode_match:
            return filename_cln

        season = episode_match.group(1)
        episode = episode_match.group(2)

        show_details = self.meta.get_details_show(title=library_item)
        if not show_details:
            return filename_cln

        episode_details = self.meta.get_details_episode(
            show_id=show_details["show_id"],
            season=season,
            episode=episode,
            show_title=library_item,
            year=show_details.get("year"),
        )

        if not episode_details:
            return filename_cln

        if "." in episode:
            episode_str = episode
        else:
            episode_str = f"{int(episode):02d}"

        return (
            f'{show_details["title"]} - '
            f"S{int(season):02d}E{episode_str} - "
            f'{episode_details["title"]}{file_ext}'
        )

    def rename(
        self,
        media_type: str,
        filename_og: str,
        filename_cln: str,
        library_item: str = None,
    ) -> dict:
        if media_type == "SHOW":
            filename_db = self.get_correct_episode_title(
                filename_cln=filename_cln, library_item=library_item
            )
            return self.results_renamer(
                filename_og=filename_og,
                filename_cln=filename_cln,
                filename_db=filename_db,
            )
        elif media_type == "MOVIE":
            filename_db = self.get_correct_movie_title(filename_cln=filename_cln)
            return self.results_renamer(
                filename_og=filename_og,
                filename_cln=filename_cln,
                filename_db=filename_db,
            )
        else:
            return None
