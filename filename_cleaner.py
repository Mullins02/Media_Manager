import re
from abc import ABC, abstractmethod

from _utils import build_episode_pattern, detect_media_type


class BaseFilenameCleaner:
    media_type = None
    filename_og = None
    filename_working = None
    filename_formatted = None
    
    def __init__(self, directory, filename):
        self.filename_og = filename
        self.filename_working = filename
        self.media_type = detect_media_type(directory)

class EpisodeFilenameCleaner(BaseFilenameCleaner):
    series_name = None
    episode_details = None
    episode_number_overall = None
    episode_number = None
    season_number = None
    episode_title = None
    
    def __init__(self, directory, filename):
        super().__init__(directory, filename)
        
    def _check_if_file_formatted(self):
        #TODO
        formatted = False
        if build_episode_pattern().match(self.filename_og):
            print(f"Properly formatted: {self.filename_og}")
            formatted = True
        return formatted
        

    def clean_filename(self):
        if self._check_if_file_formatted():
            print('file already formatted')
        else:
            #TODO
            self.clean_filename()
    
    #TODO
    def clean_filename(self):
        print('cleaning file')
        return None

    #TODO
    def remove_tags(self):
        # episode specific cleanup
        return self.filename.replace("WEBRip", "")
    
