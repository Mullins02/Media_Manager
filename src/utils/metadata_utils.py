import os, re
from dotenv import load_dotenv
import tvdb_v4_official
import requests

import logging

load_dotenv()

logger = logging.getLogger(__name__)


class MetadataUtils:
    def __init__(self, tmdb_api_key=None, tvdb_api_key=None):
        self.tmdb_api_key = tmdb_api_key or os.getenv("TMDB_API_KEY")
        self.tvdb_api_key = tvdb_api_key or os.getenv("TVDB_API_KEY")
        self.tvdb = tvdb_v4_official.TVDB(self.tvdb_api_key)
        self.base_url = "https://api.themoviedb.org/3"
        self.movie_cache = {}
        self.show_cache = {}
        self.episode_cache = {}

    def _title_formatting(self, title):
        title = re.sub(r"'([A-Z])", lambda m: "'" + m.group(1).lower(), title)
        title = re.sub(r'["*]', "'", title)  # replace " and *
        title = re.sub(r"[<>]", " ", title)  # remove < >
        title = re.sub(r"[\\/|]", "+", title)  # / \ | -> +
        title = re.sub(r"\?", ".", title)  # ? -> .
        title = re.sub(r":", ",", title)  # : -> ,
        title = re.sub(r"- $", " ", title)  # : -> ,
        return re.sub(r"\s+", " ", title).strip()

    def _get_movie_year_from_releases(self, movie_name=None, year=None, movie_id=None):
        if not (movie_name or movie_id):
            logger.info("Required movie_name or movie_id")
            return None

        if not movie_id and movie_name:
            movie_id = self._get_id_movie(movie_name, year)

        if not movie_id:
            logger.info("Could not find movie")
            return None
        url = f"{self.base_url}/movie/{movie_id}/release_dates"
        params = {"api_key": self.tmdb_api_key}

        response = requests.get(url, params=params)
        data = response.json()

        for country in data.get("results", []):
            if country["iso_3166_1"] == "US":
                for r in country["release_dates"]:
                    return r["release_date"][:4]

        return None

    def _make_lookup_key_movie(self, title: str, year: str = None):
        return (
            str(title).strip().lower() if title else None,
            str(year).strip() if year else None,
        )

    def _make_lookup_key_show(self, title: str, year: str = None):
        return (
            str(title).strip().lower() if title else None,
            str(year).strip() if year else None,
        )

    def _make_lookup_key_episode(self, show_id: str, season: str, episode: str):
        return (
            int(show_id) if show_id is not None else None,
            int(season) if season is not None else None,
            float(episode) if episode is not None else None,
        )

    def _get_id_movie(self, movie_name: str, year=None) -> dict | None:
        url = f"{self.base_url}/search/movie"

        params = {
            "api_key": self.tmdb_api_key,
            "query": movie_name,
            "language": "en-US",
        }

        if year:
            params["primary_release_year"] = year

        response = requests.get(url, params=params)
        data = response.json()

        if "results" in data and data["results"]:
            return data["results"][0]["id"]

        params = {"api_key": self.tmdb_api_key, "query": movie_name}

        response = requests.get(url, params=params)
        data = response.json()

        if "results" in data and data["results"]:
            return data["results"][0]["id"]

        return None

    def _get_id_show(self, show_name: str, year=None):
        url = f"{self.base_url}/search/tv"

        search_attempts = []

        if year:
            search_attempts.append(
                {
                    "api_key": self.tmdb_api_key,
                    "query": show_name,
                    "first_air_date_year": year,
                    "language": "en-US",
                }
            )

        search_attempts.append(
            {
                "api_key": self.tmdb_api_key,
                "query": show_name,
            }
        )

        for params in search_attempts:
            response = requests.get(url, params=params)
            data = response.json()

            results = data.get("results", [])
            if results:
                return results[0]["id"]

        return None

    def _get_uncached_details_movie(
        self, movie_name: str = None, year: str = None, movie_id: str = None
    ) -> dict | None:
        if not (movie_name or movie_id):
            logger.info("Required movie_name or movie_id")
            return None

        if not movie_id and movie_name:
            movie_id = self._get_id_movie(movie_name, year)

        if not movie_id:
            logger.info("Could not find movie")
            return None

        url = f"{self.base_url}/movie/{movie_id}"
        params = {
            "api_key": self.tmdb_api_key,
            "language": "en-US",
        }
        response = requests.get(url, params=params)
        data = response.json()

        if not data:
            return None

        title = self._title_formatting(data.get("title"))
        year = self._get_movie_year_from_releases(movie_id=movie_id)

        if not year:
            release_date = data.get("release_date")
            if release_date:
                year = release_date[:4]

        return {
            "movie_id": movie_id,
            "title": title,
            "year": year,
            "formatted_title": f"{title} ({year})",
        }

    def _get_uncached_details_show(
        self, show_name: str = None, year: str = None, show_id: str = None
    ) -> dict | None:
        if not (show_name or show_id):
            logger.info("Required show_name or show_id")
            return None

        if not show_id and show_name:
            show_id = self._get_id_show(show_name, year)

        if not show_id:
            logger.info("Could not find show")
            return None

        url = f"{self.base_url}/tv/{show_id}"
        params = {
            "api_key": self.tmdb_api_key,
            "language": "en-US",
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        
        

        if not data:
            return None

        raw_title = data.get("name")
        if not raw_title:
            return None

        title = self._title_formatting(raw_title)

        first_air_date = data.get("first_air_date")
        resolved_year = first_air_date[:4] if first_air_date else None

        return {
            "show_id": show_id,
            "title": title,
            "year": resolved_year,
            "formatted_title": f"{title} ({resolved_year})" if resolved_year else title,
        }

    def _get_uncached_details_show_tvdb(
        self, show_name: str = None, year: str = None, show_id: str = None
    ) -> dict | None:
        if not show_name:
            return None

        try:
            results = self.tvdb.search(show_name, type="series")
        except Exception as e:
            logger.info(f"TVDB show search failed for {show_name}: {e}")
            return None

        if not results:
            return None

        best_match = results[0]

        if year:
            for result in results:
                first_air = result.get("year") or result.get("firstAired")
                if first_air and str(first_air).startswith(str(year)):
                    best_match = result
                    break

        show_id = best_match.get("tvdb_id") or best_match.get("id")
        if not show_id:
            return None

        try:
            series = self.tvdb.get_series_extended(show_id)
        except Exception as e:
            logger.info(f"TVDB extended series lookup failed for {show_name}: {e}")
            return None

        first_air = series.get("firstAired") or best_match.get("firstAired")
        resolved_year = first_air[:4] if first_air else None

        clean_title = self._title_formatting(show_name)

        return {
            "show_id": show_id,
            "year": resolved_year,
            "formatted_title": (
                f"{clean_title} ({resolved_year})" if resolved_year else clean_title
            ),
            "source": "tvdb",
        }

    def _get_uncached_details_episode(
        self, show_id: int, season: int, episode: float
    ) -> dict | None:
        if show_id is None or season is None or episode is None:
            logger.info("Required show_id, season, and episode")
            return None

        url = f"{self.base_url}/tv/{show_id}/season/{season}/episode/{episode}"
        params = {
            "api_key": self.tmdb_api_key,
            "language": "en-US",
        }
        response = requests.get(url, params=params)
        data = response.json()

        if not data:
            return None

        raw_title = data.get("name")
        if not raw_title:
            return None

        return {
            "show_id": int(show_id),
            "season": int(season),
            "episode": float(episode),
            "title": self._title_formatting(raw_title),
        }

    def _get_uncached_details_episode_tvdb(
        self, show_id: int, season: int, episode: float
    ) -> dict | None:
        if show_id is None or season is None or episode is None:
            return None

        episode_str = str(episode)
        if episode_str.endswith(".0"):
            episode_str = episode_str[:-2]

        try:
            info = self.tvdb.get_series_episodes(show_id)
        except Exception as e:
            logger.info(f"TVDB episode lookup failed for show_id={show_id}: {e}")
            return None

        episodes = info.get("episodes", [])

        for ep in episodes:
            ep_season = ep.get("seasonNumber")
            if int(ep_season) != int(season):
                continue

            ep_number = ep.get("number") or ep.get("episodeNumber")
            if float(ep_number) != float(episode_str):
                continue

            self.tvdb.get_episode_translation(ep["id"], "eng")
            raw_title = self.tvdb.get_episode_translation(ep["id"], "eng")["name"]

            return {
                "show_id": int(show_id),
                "season": int(season),
                "episode": float(episode),
                "title": self._title_formatting(raw_title),
                "source": "tvdb",
            }

        return None

    def get_details_movie(self, title: str, year: str = None) -> dict | None:
        key = self._make_lookup_key_movie(title, year)
        if key in self.movie_cache:
            return self.movie_cache[key]

        movie_details = self._get_uncached_details_movie(title, year)
        self.movie_cache[key] = movie_details
        return movie_details

    def get_details_show(self, title, year=None) -> dict | None:
        key = self._make_lookup_key_show(title, year)

        if key in self.show_cache:
            return self.show_cache[key]

        show_details = self._get_uncached_details_show(title, year)

        if not show_details:
            logger.debug(f"TMDB failed for show '{title}', trying TVDB")
            show_details = self._get_uncached_details_show_tvdb(title, year)

        self.show_cache[key] = show_details
        return show_details

    def get_details_episode(
        self,
        show_id: str,
        season: str,
        episode: str,
        show_title: str = None,
        year: str = None,
    ) -> dict | None:
        key = self._make_lookup_key_episode(show_id, season, episode)

        if key in self.episode_cache:
            return self.episode_cache[key]

        episode_details = self._get_uncached_details_episode(show_id, season, episode)

        if not episode_details and show_title:
            logger.debug(
                f"TMDB failed for episode {show_title} S{season}E{episode}, trying TVDB"
            )

            tvdb_show = self._get_uncached_details_show_tvdb(show_title, year)
            if tvdb_show:
                episode_details = self._get_uncached_details_episode_tvdb(
                    tvdb_show["show_id"], season, episode
                )

        self.episode_cache[key] = episode_details
        return episode_details



######## IDEA FOR PER library_item API CALL

    def _get_uncached_details_episode_v2(
        self, show_id: int, season: int, episode: float
    ) -> dict | None:
        if show_id is None or season is None or episode is None:
            logger.info("Required show_id, season, and episode")
            return None

        url = f"{self.base_url}/tv/{show_id}/season/{season}"
        # url = f"{self.base_url}/tv/{show_id}/season/{season}/episode/{episode}"
        params = {
            "api_key": self.tmdb_api_key,
            "language": "en-US",
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        print(data)

        if not data:
            return None

        raw_title = data.get("name")
        if not raw_title:
            return None

        return {
            "show_id": int(show_id),
            "season": int(season),
            "episode": float(episode),
            "title": self._title_formatting(raw_title),
        }

    def get_details_show_v2(
        self, show_name: str = None, year: str = None, show_id: str = None
    ) -> dict | None:
        if not (show_name or show_id):
            logger.info("Required show_name or show_id")
            return None

        if not show_id and show_name:
            show_id = self._get_id_show(show_name, year)

        if not show_id:
            logger.info("Could not find show")
            return None

        url = f"{self.base_url}/tv/{show_id}"
        params = {
            "api_key": self.tmdb_api_key,
            "language": "en-US",
        }
        response = requests.get(url, params=params)
        data = response.json()

        if not data:
            return None
        
        season_data = {}        
        for season in range(0, len(data["seasons"])):
            # skip specials for now
            if 'specials' != season["name"].lower():
                season_data[season] = {}
                
                #call api with season id
                #get episode detials from season queries
                #add to season_
                
        episode_data = {}
        for season in season_data:
            for episode in range(0, season["episode_count"]):
                self._get_uncached_details_episode_v2()
                
            

        raw_title = data.get("name")
        if not raw_title:
            return None

        title = self._title_formatting(raw_title)

        first_air_date = data.get("first_air_date")
        resolved_year = first_air_date[:4] if first_air_date else None

        return {
            "show_id": show_id,
            "title": title,
            "year": resolved_year,
            "formatted_title": f"{title} ({resolved_year})" if resolved_year else title,
        }

    def get_media_details(self, media_type: str, library_item:str)  -> dict | None:
        match media_type:
            case "SHOW":
                logger.debug("searching for show details")
                show_details = self.get_details_show(library_item)

                if not show_details:
                    return None

                show_id = show_details["show_id"]

                episodes_lookup = {}

                seasons = self._get_uncached_details_show_seasons(show_id)

                for season in seasons:
                    season_num = season["season_number"]

                    episodes = self._get_uncached_details_season(show_id, season_num)

                    for ep in episodes:
                        key = (season_num, ep["episode_number"])
                        episodes_lookup[key] = ep["name"]

                return {
                    "title": show_details["title"],
                    "year": show_details.get("year"),
                    "show_id": show_id,
                    "episodes_lookup": episodes_lookup
                }

        
            # case "MOVIE":
            #     logger.debug("searching for movie details")
            #     pass
        