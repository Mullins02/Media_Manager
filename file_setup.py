

class FilenameCleanerFactory:
    @staticmethod
    def create(directory: str, filename: str) -> BaseFilenameCleaner:
        media_type = MediaDetector.detect_type(directory, filename)

        if media_type == "SHOW":
            return EpisodeFilenameCleaner(directory, filename)
        if media_type == "MOVIE":
            return MovieFilenameCleaner(directory, filename)

        raise ValueError("Could not determine media type")