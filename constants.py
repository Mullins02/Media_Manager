import re

RESOLUTION_PATTERN = re.compile(r"\b(480p|720p|1080p|2160p|4k)\b", re.IGNORECASE)

CODEC_PATTERN = re.compile(
    r"\b(x264|x265|h\.264|h\.265|hevc|avc)\b",
    re.IGNORECASE
)

SOURCE_PATTERN = re.compile(
    r"\b(webrip|web-dl|webdl|bluray|brrip|dvdrip|hdrip|remux)\b",
    re.IGNORECASE
)

YEAR_PATTERN = re.compile(
    r"\b(19\d{2}|20\d{2})\b"
)

EPISODE_PATTERN_TEMPLATE = (
    r"^{show_name} - (?:Ep \d+ )?"
    r"(?:\(S\d{{2}}E\d{{3}}\) - |S\d{{2}}E\d+(?:\.\d+)? - )"
    r".+\."
)


MEDIA_KEYWORDS = {
    "MOVIE": ["movie", "movies", "film"],
    "SHOW": ["show", "shows", "tv", "series"]
}