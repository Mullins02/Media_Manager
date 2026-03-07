from abc import ABC, abstractmethod
import re
from pathlib import Path

from constants import EPISODE_PATTERN_TEMPLATE

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

    def clean_filename(self) -> str:
        if not self.format_file():    
            print('Skipped file type')        
        elif self.build_episode_pattern(self.show_name).match(self.filename_og):
            print('Already formatted')
            return self.filename_og
        else:
            self.remove_common_fluff()
            self.remove_ver_ind()            
            self.final_cleanup()
        return self.filename_working
            

            
            
