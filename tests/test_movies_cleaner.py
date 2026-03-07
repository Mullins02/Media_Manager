from cleaners import MovieFilenameCleaner


def test_Movie_cleaner_detects_already_formatted():
    cleaner = MovieFilenameCleaner(
        directory="Z:\\Movies\\MovieLibrary\\The Office",
        filename="The Office (2024).mkv"
    )
    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert "filename" in result
    assert "changed" in result


def test_Movie_cleaner_detects_newly_formatted():
    cleaner = MovieFilenameCleaner(
        directory="Z:\\Movies\\MovieLibrary\\The Office",
        filename="The.Office.2024.WEBRip.mkv"
    )
    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert result["filename"] is not None
    assert result["changed"] is True


def test_Movie_cleaner_basic_cleanup():
    cleaner = MovieFilenameCleaner(
        directory="Z:\\Movies\\MovieLibrary\\28 Years Later The Bone Temple (2026)",
        filename="28.Years.Later.The.Bone.Temple.2026.mkv"
    )
    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert result["filename"] == "28 Years Later The Bone Temple (2026).mkv"
    assert result["changed"] is True
    
def test_Movie_cleaner_bad_dir():
    cleaner = MovieFilenameCleaner(
        directory="Z:\\Movies\\MovieLibrary\\28 Years",
        filename="28.Years.Later.The.Bone.Temple.2026.mkv"
    )
    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert result["filename"] == "28 Years Later The Bone Temple (2026).mkv"
    assert result["changed"] is True
    
def test_extract_movie_details_standard_format():
    cleaner = MovieFilenameCleaner(
        directory="Media/Movies",
        filename="The Dark Knight (2008).mkv"
    )
    cleaner.filename_working = "The Dark Knight (2008)"
    result = cleaner.extract_movie_details()
    assert result["title"] == "The Dark Knight"
    assert result["year"] == "2008"
    
def test_extract_movie_details_dot_format():
    cleaner = MovieFilenameCleaner(
        directory="Media/Movies",
        filename="The.Dark.Knight.2008.1080p.mkv"
    )
    cleaner.filename_working = "The Dark Knight 2008"
    result = cleaner.extract_movie_details()
    assert result["title"] == "The Dark Knight"
    assert result["year"] == "2008"
    
def test_extract_movie_details_square_brackets():
    cleaner = MovieFilenameCleaner(
        directory="Media/Movies",
        filename="Test.mkv"
    )
    cleaner.filename_working = "The Dark Knight [2008]"
    result = cleaner.extract_movie_details()
    assert result["title"] == "The Dark Knight"
    assert result["year"] == "2008"
    
def test_extract_movie_details_no_year():
    cleaner = MovieFilenameCleaner(
        directory="Media/Movies",
        filename="Test.mkv"
    )
    cleaner.filename_working = "The Dark Knight"
    result = cleaner.extract_movie_details()
    assert result["title"] is None
    assert result["year"] is None