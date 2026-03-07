from abc import ABC, abstractmethod
import re
from tmdb_helper import TMDB_Utils 

from constants import FILE_EXTENSIONS_TO_SKIP

class BaseFilenameCleaner(ABC):
    def __init__(self, directory, filename, config=None):
        self.directory = directory
        self.filename_og = filename
        self.filename_working = filename
        self.file_extension = filename.split(".")[-1].lower()
        self.changed = False
        self.config = config
        self.tmdb = TMDB_Utils()
        
    def format_file(self):
        return not self.file_extension in FILE_EXTENSIONS_TO_SKIP
        
    def remove_common_fluff(self):
        self.filename_working = self.filename_working.replace(self.file_extension, "")
        self.filename_working = re.sub(r'^\[.*?\]\s*', '', self.filename_working)
        
    def invalid_char_corrector(self):
        invalid_chars = ['(', ')', '-', '.', ':', '_']
        for char in invalid_chars:
            self.filename_working = self.filename_working.replace(char, ' ')
        self.filename_working = re.sub(r'\s+', ' ', self.filename_working).strip()

    def normalize_separators(self) -> str:
        self.filename_working = self.filename_working.replace(".", " ").replace("_", " ")
        return self.filename_working

    def collapse_spaces(self) -> str:
        self.filename_working = " ".join(self.filename_working.split())
        return self.filename_working

    def final_cleanup(self) -> str:
        self.filename_working = self.filename_working.strip()
        return self.filename_working
    
    def compare_og_to_work(self) -> bool:
        print(self.filename_og, self.filename_working)
        return not self.filename_og is self.filename_working
        
    def results(self) -> dict:
        return {'filename': self.filename_working, 'changed': self.compare_og_to_work()}

    def clean_filename(self) -> str:
        if not self.format_file():    
            print('Skipped file type')        
        elif self.format_file():
            self.normalize_separators()
            self.collapse_spaces()
            self.final_cleanup()
        return self.results()