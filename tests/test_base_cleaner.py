from cleaners import BaseFilenameCleaner


def test_base_cleaner_format_file_allows_valid_extension():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Movies\MovieLibrary",
        filename="The.Movie.2024.mkv",
    )

    assert cleaner.format_file() is True


def test_base_cleaner_format_file_skips_invalid_extension():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Movies\MovieLibrary",
        filename="poster.jpg",
    )

    assert cleaner.format_file() is False


def test_base_cleaner_remove_common_fluff():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Shows\Animation",
        filename="[EMBER] Fire.Force.S03E19.mkv",
    )

    cleaner.remove_common_fluff()
    assert cleaner.filename_working == "Fire.Force.S03E19"


def test_base_cleaner_invalid_char_corrector():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Movies\MovieLibrary",
        filename="Movie-Name_(2024):Part.1.mkv",
    )

    cleaner.invalid_char_corrector()
    assert cleaner.filename_working == "Movie Name 2024 Part 1"


def test_base_cleaner_normalize_separators():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Movies\MovieLibrary",
        filename="The.Movie_Name.2024.mkv",
    )

    cleaner.normalize_separators()
    assert cleaner.filename_working == "The Movie Name 2024"


def test_base_cleaner_collapse_spaces():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Movies\MovieLibrary",
        filename="Movie.mkv",
    )
    cleaner.filename_working = "Movie    Name     2024"

    cleaner.collapse_spaces()
    assert cleaner.filename_working == "Movie Name 2024"


def test_base_cleaner_final_cleanup():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Movies\MovieLibrary",
        filename="Movie.mkv",
    )
    cleaner.filename_working = "   Movie Name   "

    cleaner.final_cleanup()
    assert cleaner.filename_working == "Movie Name"


def test_base_cleaner_compare_og_to_work_detects_change():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Movies\MovieLibrary",
        filename="Movie.Name.mkv",
    )
    cleaner.filename_working = "Movie Name"

    assert cleaner.compare_og_to_work() is True


def test_base_cleaner_compare_og_to_work_detects_no_change():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Movies\MovieLibrary",
        filename="Movie.Name.mkv",
    )

    assert cleaner.compare_og_to_work() is False


def test_base_cleaner_results():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Movies\MovieLibrary",
        filename="Movie.Name.mkv",
    )
    cleaner.filename_working = "Movie Name"

    result = cleaner.results()
    assert isinstance(result, dict)
    assert result["filename"] == "Movie Name"
    assert result["changed"] is True


def test_base_cleaner_clean_filename_runs_basic_pipeline():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Movies\MovieLibrary",
        filename="The.Movie_Name.2024.mkv",
    )

    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert result["filename"] == "The Movie Name 2024"
    assert result["changed"] is True


def test_base_cleaner_clean_filename_skips_filetype():
    cleaner = BaseFilenameCleaner(
        directory=r"Z:\Movies\MovieLibrary",
        filename="poster.jpg",
    )

    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert result["filename"] == "poster"
    assert result["changed"] is False