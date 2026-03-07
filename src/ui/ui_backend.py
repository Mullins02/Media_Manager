import os, re
import logging


from utils.lib_scanner import LibraryScanner


logger = logging.getLogger(__name__)

class UIBackend():
    def __init__(self, media_files:list[dict]=None):
        self.media_files = media_files
        
    def _from_scan(self) ->  list[dict]:
        """Explicitly perform library scan."""
        media_files = LibraryScanner().scan()
        return media_files

    def grouped_media(self) -> dict:
        grouped = {}
        
        if not self.media_files:
            self.media_files = self._from_scan()

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