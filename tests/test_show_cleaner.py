from cleaners import ShowFilenameCleaner


def test_show_cleaner_detects_already_formatted():
    cleaner = ShowFilenameCleaner(
        directory="Z:\\Shows\\Television\\The Office",
        filename="The Office - S02E03 - Bubble.mkv",
    )
    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert "filename" in result
    assert "changed" in result


def test_show_cleaner_detects_newly_formatted():
    cleaner = ShowFilenameCleaner(
        directory="Z:\\Shows\\Television\\The Office",
        filename="The.Office.S02E03.WEBRip.mkv",
    )

    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert result["filename"] is not None
    assert result["changed"] is True


def test_show_cleaner_basic_cleanup():
    cleaner = ShowFilenameCleaner(
        directory="Z:\\Shows\\Animation\\Hell's Paradise",
        filename="Hells.Paradise.S02E06.Conflict.and.Growing.Together.1080p.CR.WEB-DL.DUAL.AAC2.0.H.264.MSubs-ToonsHub.mkv",
    )

    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert result["filename"] == "Hell's Paradise - S02E06.mkv"
    assert result["changed"] is True


def test_show_cleaner_basic_cleanup_2():
    cleaner = ShowFilenameCleaner(
        directory="Z:\\Shows\\Animation\\Fire Force\\Season 3",
        filename="[EMBER] Enen no Shouboutai S3 - 19.mkv",
    )

    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert result["filename"] == "Fire Force - S03E19.mkv"
    assert result["changed"] is True


def test_show_cleaner_basic_cleanup_3():
    cleaner = ShowFilenameCleaner(
        directory="Z:\\Shows\\Animation\\Fire Force\\Season 3",
        filename="[EMBER] S3 - 19.mkv",
    )

    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert result["filename"] == "Fire Force - S03E19.mkv"
    assert result["changed"] is True


def test_remove_ver_ind_removes_version_suffix():
    cleaner = ShowFilenameCleaner(
        directory="Z:\\Shows\\Animation\\The Office\\Season 2",
        filename="The Office - S02E03 v2.mkv",
    )
    cleaner.filename_working = "The Office - S02E03 v2"
    cleaner.remove_ver_ind()
    assert cleaner.filename_working == "The Office - S02E03"
