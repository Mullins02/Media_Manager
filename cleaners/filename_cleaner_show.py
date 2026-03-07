from abc import ABC, abstractmethod
import os
import re
from pathlib import Path

from constants import EPISODE_PATTERN_TEMPLATE, EPISODE_EXTRACTION_PATTERNS

from cleaners.filename_cleaner_base import BaseFilenameCleaner

class ShowFilenameCleaner(BaseFilenameCleaner):
    show_name =None
    
    def __init__(self, directory: str, filename: str):
        super().__init__(directory, filename)
        self.show_name = Path(directory).name
        
    def build_episode_pattern(self, show_name):
        pattern = EPISODE_PATTERN_TEMPLATE.format(
            show_name=re.escape(show_name)
        )
        return re.compile(pattern, re.IGNORECASE)
    
    def remove_ver_ind(self):
        self.filename_working = re.sub(r'\s*[Vv]\d+\s*$', '', self.filename_working) 
        
    def get_abbreviated_show_name(self, show_name: str) -> str:
        words = show_name.split()
        if len(words) <= 1:
            return show_name
        return "".join(word[0] for word in words if word)

    def extract_episode_info(self, alt_names=None):
        clean_name = self.filename_working
        alt_names = alt_names or []
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
                c for c in candidates
                if not (c.lower() in seen or seen.add(c.lower()))
            ]
            clean_lower = clean_name.lower()
            matched = None
            for cand in candidates:
                if cand.lower() in clean_lower:
                    matched = cand
                    break
            if matched:
                clean_name = re.sub(re.escape(matched), "", clean_name, flags=re.IGNORECASE)
                break
        season_num = 1
        episode_num = None
        season_found_in_filename = False
        for pattern in EPISODE_EXTRACTION_PATTERNS:
            match = re.search(pattern, clean_name)
            if match:
                groups = match.groups()
                if len(groups) == 1:
                    episode_str = groups[0]
                else:
                    season_num = int(groups[0])
                    episode_str = groups[1]
                    season_found_in_filename = True
                try:
                    if '.' in episode_str:
                        episode_num = float(episode_str)
                    else:
                        episode_num = int(episode_str)
                    break
                except ValueError:
                    continue
        if not season_found_in_filename:
            folder_name = os.path.basename(self.directory)
            season_match = re.search(r'[Ss]eason\s*(\d+)', folder_name, re.IGNORECASE)
            if season_match:
                season_num = int(season_match.group(1))
        if episode_num is not None:
            if isinstance(episode_num, float):
                return f'{self.show_name} - S{season_num:02}E{episode_num:g}.{self.file_extension}'
            return f'{self.show_name} - S{season_num:02}E{episode_num:02}.{self.file_extension}'
        return None

    def clean_filename(self) -> str:
        if not self.format_file():
            print('Skipped file type')
        elif self.build_episode_pattern(self.show_name).match(self.filename_og):
            print('Already formatted')
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
            

            
            
