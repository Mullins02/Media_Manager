from abc import ABC, abstractmethod
import os
import re
from pathlib import PureWindowsPath
import logging

from constants import (
    FORMATTED_PATTERN_TEMPLATE,
    EPISODE_EXTRACTION_PATTERNS,
    SEASON_PATTERN,
    SUB_EXTENSIONS,
)

from cleaners.filename_cleaner_base import BaseFilenameCleaner

logger = logging.getLogger(__name__)


# TODO - add Part 1, 2, etc instead of (1), (2), etc
class ShowFilenameCleaner(BaseFilenameCleaner):
    def __init__(self, directory: str, filename: str, config=None):
        super().__init__(directory, filename, config)
        path = PureWindowsPath(directory)
        folder_name = path.name
        if config and getattr(config, "show_name", None):
            self.show_name = config.show_name
        elif re.match(SEASON_PATTERN, folder_name, re.IGNORECASE):
            self.show_name = path.parent.name
        else:
            self.show_name = folder_name
        self.pattern = re.compile(
            FORMATTED_PATTERN_TEMPLATE.format(show_name=re.escape(self.show_name)),
            re.IGNORECASE,
        )

    def remove_ver_ind(self):
        self.filename_working = re.sub(r"\s*[Vv]\d+\s*$", "", self.filename_working)

    def get_abbreviated_show_name(self, show_name: str) -> str:
        words = show_name.split()
        if len(words) <= 1:
            return show_name
        return "".join(word[0] for word in words if word)

    def convert_overall_to_season_episode(self, overall_episode):
        episodes_per_season = getattr(self.config, "episodes_per_season", [])

        if episodes_per_season:
            current_episode = overall_episode
            season_num = 1

            for season_total in episodes_per_season:
                if current_episode <= season_total:
                    return season_num, current_episode
                current_episode -= season_total
                season_num += 1

        return None, None

    def strip_show_name_from_filename(self) -> str:
        clean_name = self.filename_working
        alt_names = getattr(self.config, "alt_names", [])
        show_names_to_check = [self.show_name] + alt_names

        for show_name in show_names_to_check[:]:
            abbreviated_name = self.get_abbreviated_show_name(show_name)
            if abbreviated_name.lower() != show_name.lower():
                show_names_to_check.append(abbreviated_name)

        for alt_name in show_names_to_check:
            candidates = [
                alt_name,
                alt_name.replace(" ", "."),
                alt_name.replace(" ", "_"),
            ]
            seen = set()
            candidates = [
                c for c in candidates if not (c.lower() in seen or seen.add(c.lower()))
            ]

            clean_lower = clean_name.lower()
            matched = None
            for cand in candidates:
                if cand.lower() in clean_lower:
                    matched = cand
                    break
            if matched:
                clean_name = re.sub(
                    re.escape(matched), "", clean_name, flags=re.IGNORECASE
                )
                break

        return clean_name

    def extract_episode_info(self):
        clean_name = self.strip_show_name_from_filename()

        season_num = 1
        episode_num = None
        season_found_in_filename = False
        single_number_match = False

        for pattern in EPISODE_EXTRACTION_PATTERNS:
            match = re.search(pattern, clean_name)
            if match:
                groups = match.groups()
                if len(groups) == 1:
                    episode_str = groups[0]
                    single_number_match = True
                else:
                    season_num = int(groups[0])
                    episode_str = groups[1]
                    season_found_in_filename = True
                try:
                    if "." in episode_str:
                        episode_num = float(episode_str)
                    else:
                        episode_num = int(episode_str)
                    break
                except ValueError:
                    continue
        if not season_found_in_filename:
            folder_name = folder_name = PureWindowsPath(self.directory).name
            season_match = re.search(r"[Ss]eason\s*(\d+)", folder_name, re.IGNORECASE)
            if season_match:
                season_num = int(season_match.group(1))
            elif single_number_match and isinstance(episode_num, int):
                converted = self.convert_overall_to_season_episode(episode_num)
                if converted != (None, None):
                    season_num, episode_num = converted
        if episode_num is not None:
            if isinstance(episode_num, float):
                return f"{self.show_name} - S{season_num:02}E{episode_num:g}{self.file_extension}"
            return f"{self.show_name} - S{season_num:02}E{episode_num:02}{self.file_extension}"
        return None

    def clean_filename(self) -> dict:
        if not self.cleanable():
            logger.debug("Skipped file type")
        elif self.formatted():
            logger.debug("Already formatted")
        else:
            self.remove_common_fluff()
            self.remove_ver_ind()
            self.invalid_char_corrector()
            self.collapse_spaces()
            cleaned_episode_name = self.extract_episode_info()
            if cleaned_episode_name:
                self.filename_working = cleaned_episode_name
            self.final_cleanup()
        return self.results()
