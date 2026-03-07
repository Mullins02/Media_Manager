import os, re
import logging

from .media_detector import MediaDetector

from constants import MEDIA_DIRECTORIES, MEDIA_FOLDERS


logger = logging.getLogger(__name__)

class LibraryScanner():
    def __init__(self, directories: list=None):
        #TODO - replace with config var
        self.directories = directories or MEDIA_DIRECTORIES
            
    def scan(self) -> list[dict]:
        media_files = []
        
        for directory_path in self.directories:
            logger.info(f"Scanning library root: {directory_path}")
            
            if not os.path.exists(directory_path):
                logger.warning(f"Directory does not exist: {directory_path}")
                continue
            
            for root, dirs, files in os.walk(directory_path):
                relative = os.path.relpath(root, directory_path)
                parts = relative.split(os.sep)

                if parts[0] == ".":
                    continue

                library_item = parts[0]

                for file in files:
                    media_type = MediaDetector.detect_type(root, file)
                    if media_type is None:
                        continue
                    
                    full_path = os.path.join(root, file)

                    media_entry = {
                        "library_item": library_item,
                        "directory": root,
                        "filename": file,
                        "full_path": full_path,
                        "media_type": media_type,
                    }
                    
                    media_files.append(media_entry)
                    
        logger.debug("end of test")
        return media_files