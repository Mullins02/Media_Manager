from media_detector import MediaDetector

def test_show_from_shows_directory():
    result = MediaDetector._detect_type(
        directory="Media/Shows",
        filename="The.Office.S02E03.WEBRip.mkv"
    )
    assert result == "SHOW"

def test_movie_from_movies_directory():
    result = MediaDetector._detect_type(
        directory="Media/Movies",
        filename="The.Dark.Knight.2008.1080p.mkv"
    )
    assert result == "MOVIE"

def test_unknown_when_no_keyword_found():
    result = MediaDetector._detect_type(
        directory="Media/Downloads",
        filename="random_file.mkv"
    )
    assert result == "UNKNOWN"

def test_type_is_case_insensitive():
    result = MediaDetector._detect_type(
        directory="MEDIA/SHows",
        filename="Some.Show.S01E01.mkv"
    )
    assert result == "SHOW"

def test_filename_does_not_affect_detection_yet():
    result = MediaDetector._detect_type(
        directory="Media/Downloads",
        filename="Some.Show.S01E01.mkv"
    )
    assert result == "UNKNOWN"