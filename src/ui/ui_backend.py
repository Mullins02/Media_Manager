import os, re
import logging


from utils.lib_scanner import LibraryScanner
from utils.filename_renamer import FilenameRenamer


logger = logging.getLogger(__name__)


class UIBackend:
    def __init__(self, media_files: list[dict] = None):
        self.media_files = media_files
        self.renamer = FilenameRenamer()

    def _from_scan(self) -> list[dict]:
        """Explicitly perform library scan."""
        media_files = LibraryScanner().scan()
        return media_files

    def grouped_media(self) -> dict:
        grouped = {}

        if not self.media_files:
            self.media_files = self._from_scan()

        for media_file in self.media_files:
            media_type = media_file["media_type"]
            library_item = media_file["library_item"]

            if media_type not in grouped:
                grouped[media_type] = {}

            if library_item not in grouped[media_type]:
                grouped[media_type][library_item] = {"files": []}

            grouped[media_type][media_file["library_item"]]["files"].append(media_file)

        return grouped

    def rename_files(self, selected_data: list[dict]) -> dict:
        renamed_files = []
        for item in selected_data:
            library_item = item["library_item"]
            media_type = item["media_type"]

            logger.debug(f"{library_item} | {media_type}")

            for file in item["data"]["files"]:
                filename_og = file["filename"]
                logger.debug(f'   ↪{file["filename"]}')
                print(file["filename"])

                cleaned_filename_results = file["cleaner"].clean_filename()
                if cleaned_filename_results:
                    cleanable = cleaned_filename_results["cleanable"]
                    if cleanable:
                        formatted = cleaned_filename_results["formatted"]
                        if not formatted:
                            filename_cln = cleaned_filename_results["filename"]
                            rename_results = self.renamer.rename(
                                media_type=media_type,
                                filename_og=filename_og,
                                filename_cln=filename_cln,
                                library_item=library_item,
                            )
                            renamed_files.append(rename_results)
                            print(rename_results["filename_db"])
                            continue

                        logger.debug(f"      Already formatted.")
                    logger.debug(f"      ↪Could not be cleaned.")
                logger.debug(f"Issue during cleaning")
                renamed_files.append(
                    {
                        "filename_og": filename_og,
                        "filename_cln": None,
                        "filename_db": None,
                    }
                )
            print("completed files")

        return renamed_files
