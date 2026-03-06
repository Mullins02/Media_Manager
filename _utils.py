import re
from constants import MEDIA_KEYWORDS, EPISODE_PATTERN_TEMPLATE


def build_episode_pattern(show_name):
    pattern = EPISODE_PATTERN_TEMPLATE.format(
        show_name=re.escape(show_name)
    )

    return re.compile(pattern, re.IGNORECASE)

