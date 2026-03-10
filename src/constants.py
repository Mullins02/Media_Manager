import re

MEDIA_DIRECTORIES = [
    "Z:\\Movies\\MovieLibrary",
    "Z:\\Shows\\Animation",
    "Z:\\Shows\\Television",
]

FORMATTED_PATTERN_TEMPLATE = (
    r"^{show_name} - (?:Ep \d+ )?"
    r"(?:\(S\d{{2}}E\d{{3}}\) - |S\d{{2}}E\d+(?:\.\d+)? - )"
    r".+\."
)

FORMATTED_EPISODE_DETAIL_PATTERN = r"[Ss](\d+)[Ee](\d+)"

EPISODE_EXTRACTION_PATTERNS = [
    r"[Ss](\d+)[Ee](\d+(?:\.\d+)?)(?:[.\s_-]|$)",
    r"(\d+)x(\d+(?:\.\d+)?)(?:[.\s_-]|$)",
    r"[Ee][Pp]?\.?\s*(\d+\.\d+)(?:\s*[-\s].*)?$",
    r"[Ee]pisode\s*(\d+\.\d+)(?:\s*[-\s].*)?$",
    r"(?:Special|OVA|OAD)\s*[Ee]p?\.?\s*(\d+(?:\.\d+)?)(?:\s*[-\s].*)?$",
    r"(?:Special|OVA|OAD)\s*(\d+(?:\.\d+)?)(?:\s*[-\s].*)?$",
    r"[Ee][Pp]?\.?\s*(\d+)(?:\s*[-\s].*)?$",
    r"[Ee]pisode\s*(\d+)(?:\s*[-\s].*)?$",
    r"[-\s]+(\d+\.\d+)\s*$",
    r"\s+(\d+\.\d+)\s*$",
    r"[-\s]+(\d+)\s*$",
    r"\s+(\d+)\s*$",
    r"(?:^|.*\s)-\s*(\d+\.\d+)\s*$",
    r"(?:^|.*\s)-\s*(\d+)\s*$",
    r"[_.-][Ee][Pp]?\.?\s*(\d+)(?:\s*[-\s].*)?[_.-]",
    r"[Ss](\d+) - (\d+)",
]

SEASON_PATTERN = r"[Ss]eason [0-9]*"


FORMATTED_MOVIE_PATTERN = r"^[A-Za-z0-9\s&',!\[\]-]+?" r"\(\d{4}\)"

MOVIE_DETAIL_PATTERN_TEMPLATE = r"(.+?)[\s\(\[]*(\d{4})[\)\]\s]*"


MEDIA_KEYWORDS = {
    # "SPECIAL": ["special", "specials"],
    "MOVIE": ["movie", "movies", "film"],
    "SHOW": ["show", "shows", "tv", "series"],
}

VIDEO_EXTENSIONS = [".mkv", ".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v"]

SUB_EXTENSIONS = [".srt"]

MEDIA_FOLDERS = [
    r"Z:\Movies\MovieLibrary",
    r"Z:\Shows\Animation",
    r"Z:\Shows\Television",
]

FILE_EXTENSIONS_TO_SKIP = [".ico", ".ini", ".torrent", ".png", ".txt"]
