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