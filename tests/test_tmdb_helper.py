import pytest
from src.tmdb_helper import TMDB_Utils


class MockResponse:
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


@pytest.fixture
def tmdb():
    return TMDB_Utils(api_key="fake_api_key")


def test_title_formatting(tmdb):
    title = "child of-the coold: code / white? <test'S"
    result = tmdb._title_formatting(title)

    assert result == "Child Of-The Coold, Code + White. Test's"


def test_get_show_id_success(monkeypatch, tmdb):
    def mock_get(url, params=None):
        return MockResponse({
            "results": [
                {"id": 120089, "name": "SPY x FAMILY"}
            ]
        })

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb._get_show_id("Spy X Family")
    assert result == 120089


def test_get_show_id_not_found(monkeypatch, tmdb):
    def mock_get(url, params=None):
        return MockResponse({"results": []})

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb._get_show_id("Not A Real Show")
    assert result is None


def test_get_series_details_with_show_name(monkeypatch, tmdb):
    def mock_get(url, params=None):
        if "search/tv" in url:
            return MockResponse({
                "results": [{"id": 120089, "name": "SPY x FAMILY"}]
            })
        elif "/tv/120089" in url:
            return MockResponse({
                "id": 120089,
                "seasons": [
                    {"id": 1, "season_number": 0, "episode_count": 2},
                    {"id": 2, "season_number": 1, "episode_count": 12},
                    {"id": 3, "season_number": 2, "episode_count": 12},
                ]
            })
        return MockResponse({})

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb.get_series_details(show_name="Spy X Family")

    assert result == [
        {
            "show_id": 120089,
            "season_id": 2,
            "season_number": 1,
            "episode_count": 12,
        },
        {
            "show_id": 120089,
            "season_id": 3,
            "season_number": 2,
            "episode_count": 12,
        },
    ]


def test_get_series_details_with_show_id(monkeypatch, tmdb):
    def mock_get(url, params=None):
        if "/tv/120089" in url:
            return MockResponse({
                "id": 120089,
                "seasons": [
                    {"id": 2, "season_number": 1, "episode_count": 12}
                ]
            })
        return MockResponse({})

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb.get_series_details(show_id=120089)

    assert result == [
        {
            "show_id": 120089,
            "season_id": 2,
            "season_number": 1,
            "episode_count": 12,
        }
    ]


def test_get_series_details_missing_inputs(tmdb):
    result = tmdb.get_series_details()
    assert result is None


def test_get_episode_list_with_show_name(monkeypatch, tmdb):
    def mock_get(url, params=None):
        if "search/tv" in url:
            return MockResponse({
                "results": [{"id": 120089, "name": "SPY x FAMILY"}]
            })
        elif url.endswith("/tv/120089"):
            return MockResponse({
                "id": 120089,
                "name": "SPY x FAMILY",
                "seasons": [
                    {"id": 2, "season_number": 1, "episode_count": 2}
                ]
            })
        elif url.endswith("/tv/120089/season/1"):
            return MockResponse({
                "episodes": [
                    {"episode_number": 1, "name": "Operation Strix", "id": 1001},
                    {"episode_number": 2, "name": "Secure a Wife", "id": 1002},
                ]
            })
        return MockResponse({})

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb.get_episode_list(show_name="Spy X Family")

    assert len(result) == 2
    assert result[0]["show_id"] == 120089
    assert result[0]["season_number"] == 1
    assert result[0]["episode_number"] == 1
    assert result[0]["episode_name"] == "Operation Strix"
    assert result[0]["formatted_title"] == "Spy X Family - S01E01 - Operation Strix"


def test_get_episode_list_with_show_id(monkeypatch, tmdb):
    def mock_get(url, params=None):
        if url.endswith("/tv/120089"):
            return MockResponse({
                "id": 120089,
                "name": "SPY x FAMILY",
                "seasons": [
                    {"id": 2, "season_number": 1, "episode_count": 1}
                ]
            })
        elif url.endswith("/tv/120089/season/1"):
            return MockResponse({
                "episodes": [
                    {"episode_number": 1, "name": "Operation Strix", "id": 1001}
                ]
            })
        return MockResponse({})

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb.get_episode_list(show_id=120089)

    assert len(result) == 1
    assert result[0]["formatted_title"] == "Spy X Family - S01E01 - Operation Strix"


def test_get_episode_list_with_series_details(monkeypatch, tmdb):
    series_details = [
        {
            "show_id": 120089,
            "season_id": 2,
            "season_number": 1,
            "episode_count": 1,
        }
    ]

    def mock_get(url, params=None):
        if url.endswith("/tv/120089"):
            return MockResponse({
                "id": 120089,
                "name": "SPY x FAMILY"
            })
        elif url.endswith("/tv/120089/season/1"):
            return MockResponse({
                "episodes": [
                    {"episode_number": 1, "name": "Operation Strix", "id": 1001}
                ]
            })
        return MockResponse({})

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb.get_episode_list(series_details=series_details, show_id=120089)

    assert len(result) == 1
    assert result[0]["episode_id"] == 1001


def test_get_episode_list_missing_inputs(tmdb):
    result = tmdb.get_episode_list()
    assert result is None


def test_get_movie_id_success(monkeypatch, tmdb):
    def mock_get(url, params=None):
        return MockResponse({
            "results": [
                {"id": 348, "title": "Alien"}
            ]
        })

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb._get_movie_id("Alien")
    assert result == 348


def test_get_movie_id_not_found(monkeypatch, tmdb):
    def mock_get(url, params=None):
        return MockResponse({"results": []})

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb._get_movie_id("Definitely Not Real")
    assert result is None


def test_get_movie_details_with_name(monkeypatch, tmdb):
    def mock_get(url, params=None):
        if "search/movie" in url:
            return MockResponse({
                "results": [{"id": 348, "title": "Alien"}]
            })
        elif url.endswith("/movie/348"):
            return MockResponse({
                "id": 348,
                "title": "Alien",
                "release_date": "1979-05-25"
            })
        return MockResponse({})

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb.get_movie_details(movie_name="Alien")

    assert result == {
        "movie_id": 348,
        "title": "Alien",
        "year": "1979",
        "formatted_title": "Alien (1979)"
    }


def test_get_movie_details_with_id(monkeypatch, tmdb):
    def mock_get(url, params=None):
        if url.endswith("/movie/348"):
            return MockResponse({
                "id": 348,
                "title": "Alien",
                "release_date": "1979-05-25"
            })
        return MockResponse({})

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb.get_movie_details(movie_id=348)

    assert result["movie_id"] == 348
    assert result["title"] == "Alien"
    assert result["year"] == "1979"
    assert result["formatted_title"] == "Alien (1979)"


def test_get_movie_details_missing_inputs(tmdb):
    result = tmdb.get_movie_details()
    assert result is None


def test_get_movie_details_not_found(monkeypatch, tmdb):
    def mock_get(url, params=None):
        if "search/movie" in url:
            return MockResponse({"results": []})
        return MockResponse({})

    monkeypatch.setattr("src.tmdb_helper.requests.get", mock_get)

    result = tmdb.get_movie_details(movie_name="Not A Real Movie")
    assert result is None