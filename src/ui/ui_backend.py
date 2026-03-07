import os, re
import logging


from utils.lib_scanner import LibraryScanner


logger = logging.getLogger(__name__)

class UIBackend():
    def __init__(self, media_files:list[dict]=None):
        if not media_files:
            media_files = LibraryScanner().scan()
        self.media_files = media_files
    
    def grouped_media(self):
        grouped = {}

        for media_file in self.media_files:
            media_type  = media_file["media_type"]
            library_item = media_file["library_item"]

            if media_type not in grouped:
                grouped[media_type] = {}

            if library_item not in grouped[media_type]:
                grouped[media_type][library_item] = {
                    "files": []
                }

            grouped[media_type ][media_file["library_item"]]["files"].append(media_file)

        return grouped