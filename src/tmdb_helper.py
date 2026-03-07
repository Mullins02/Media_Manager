import os, re
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")


class TMDB_Utils:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"

    def _title_formatting(self, title):
        title = title.title()
        title = re.sub(r"'S(\s|$)", "'s\\1", title)
        title = re.sub(r'["*]', "'", title)  # replace " and *
        title = re.sub(r"[<>]", " ", title)  # remove < >
        title = re.sub(r"[\\/|]", "+", title)  # / \ | -> +
        title = re.sub(r"\?", ".", title)  # ? -> .
        title = re.sub(r":", ",", title)  # : -> ,
        return re.sub(r"\s+", " ", title).strip()

    def _get_show_id(self, show_name: str):
        url = url = f"{self.base_url}/search/tv"
        params = {"api_key": self.api_key, "query": show_name}

        response = requests.get(url, params=params)
        data = response.json()

        if data["results"]:
            return data["results"][0]["id"]

        return None

    def get_series_details(self, show_name=None, show_id=None):
        if not (show_id or show_name):
            print("Required show_id or show_name")
            return None

        if not show_id and show_name:
            show_id = self._get_show_id(show_name=show_name)

        if not show_id:
            print("Could not find show (series_details)")
            return None

        url = furl = f"{self.base_url}/tv/{show_id}"
        params = {"api_key": self.api_key}

        response = requests.get(url, params=params)
        data = response.json()

        if not data or "seasons" not in data:
            return None

        series_details = []

        for season in data["seasons"]:
            # skip specialss
            if season["season_number"] == 0:
                continue
            else:
                series_details.append(
                    {
                        "show_id": show_id,
                        "season_id": season["id"],
                        "season_number": season["season_number"],
                        "episode_count": season["episode_count"],
                    }
                )

        return series_details

    def get_episode_list(self, series_details=None, show_name=None, show_id=None):
        if not (show_id or show_name or series_details):
            print("Required show_id or show_name or series_details")
            return None

        if not show_name:
            url = f"{self.base_url}/tv/{show_id}"
            params = {"api_key": self.api_key}
            response = requests.get(url, params=params)
            data = response.json()
            show_name = data.get("name")

        if not show_id and show_name:
            show_id = self._get_show_id(show_name=show_name)

        if not show_id:
            print("Could not find show (episode_list)")
            return None

        if not series_details:
            series_details = self.get_series_details(show_id=show_id)

        if not series_details:
            print("Could not get series details")
            return None

        episode_list = []

        for season in series_details:
            season_number = season["season_number"]

            url = f"{self.base_url}/tv/{show_id}/season/{season_number}"
            params = {"api_key": self.api_key}

            response = requests.get(url, params=params)
            data = response.json()

            if "episodes" not in data:
                continue

            for episode in data["episodes"]:
                episode_list.append(
                    {
                        "show_id": show_id,
                        "season_number": season_number,
                        "episode_number": episode["episode_number"],
                        "episode_name": self._title_formatting(episode["name"]),
                        "episode_id": episode["id"],
                        "formatted_title": f"{self._title_formatting(show_name)} - S{season_number:02}E{episode['episode_number']:02} - {self._title_formatting(episode['name'])}",
                    }
                )

        return episode_list

    def _get_movie_id(self, movie_name: str, year=None):
        url = f"{self.base_url}/search/movie"

        params = {"api_key": self.api_key, "query": movie_name}

        if year:
            params["year"] = year

        response = requests.get(url, params=params)
        data = response.json()

        if "results" in data and data["results"]:
            return data["results"][0]["id"]

        return None

    def get_movie_details(self, movie_name=None, movie_id=None):
        if not (movie_name or movie_id):
            print("Required movie_name or movie_id")
            return None

        if not movie_id and movie_name:
            movie_id = self._get_movie_id(movie_name)

        if not movie_id:
            print("Could not find movie")
            return None

        url = f"{self.base_url}/movie/{movie_id}"

        params = {"api_key": self.api_key}

        response = requests.get(url, params=params)
        data = response.json()

        if not data:
            return None

        title = self._title_formatting(data.get("title"))
        release_date = data.get("release_date")

        year = None
        if release_date:
            year = release_date[:4]

        return {
            "movie_id": movie_id,
            "title": title,
            "year": year,
            "formatted_title": f"{title} ({year})",
        }


if __name__ == "__main__":
    tmdb = TMDB_Utils()
    print("Show test:")
    print(tmdb.get_episode_list(show_name="Spy X Family")[27])
    print("\nMovie test:")
    print(tmdb.get_movie_details(movie_name="ALIEN"))
