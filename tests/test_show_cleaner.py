from cleaners import ShowFilenameCleaner


def test_show_cleaner_detects_already_formatted():
    cleaner = ShowFilenameCleaner(
        directory="Z:\\Shows\\Television\\The Office",
        filename="The Office - S02E03 - Bubble.mkv"
    )
    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert "filename" in result
    assert "changed" in result


def test_show_cleaner_detects_newly_formatted():
    cleaner = ShowFilenameCleaner(
        directory="Z:\\Shows\\Television\\The Office",
        filename="The.Office.S02E03.WEBRip.mkv"
    )

    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert result["filename"] is not None
    assert result["changed"] is True


def test_show_cleaner_basic_cleanup():
    cleaner = ShowFilenameCleaner(
        directory="Z:\\Shows\\Animation\\Hell's Paradise",
        filename="Hells.Paradise.S02E06.Conflict.and.Growing.Together.1080p.CR.WEB-DL.DUAL.AAC2.0.H.264.MSubs-ToonsHub.mkv"
    )

    result = cleaner.clean_filename()
    assert isinstance(result, dict)
    assert result["filename"] == "Hell's Paradise - S02E06.mkv"
    assert result["changed"] is True