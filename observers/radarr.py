"""Radarr Observer class for the Observer pattern."""
import requests
from observers import Observer


class RadarrObserver(Observer):
    """Radarr Observer class for the Observer pattern."""

    def __init__(self, host: str, api_key: str):
        """Initialize the Radarr observer."""
        super().__init__("movie")
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": api_key})
        self.session.base_url = host
        self.page_size = 150

    def __search_movie(self, media):
        """Search movie from Radarr by tmbdid"""
        tmdbid = next(
            iter([guid for guid in media.guids if guid.id.startswith("tmdb://")]), None
        )
        if tmdbid is None:
            print("Radarr - No tmdbid found for media, skipping delete from Radarr")
            return
        tmdbid_str = str(tmdbid.id).removeprefix("tmdb://")
        response = self.session.get(
            f"{self.session.base_url}/api/v3/movie?tmdbid={tmdbid_str}"
        ).json()[0]
        if response["id"] is None:
            return None
        return response

    def __delete_movie(self, media, dry_run: bool):
        """Delete a movie from Radarr"""
        movie = self.__search_movie(media)
        if movie is None:
            print(f"Radarr - Movie {media.title} not found")
            return
        if dry_run:
            print("Dry run, not deleting from Radarr")
            return
        response = self.session.delete(
            f"{self.session.base_url}/api/v3/movie/{movie.id}"
        )
        if response.status_code > 300:
            print((
                f"Radarr: {movie.title} failed to delete, "
                f"status code: {response.status_code}"
            ))

    def on_media_deleted(self, media: str, dry_run: bool):
        """Delete a movie from Radarr."""
        self.__delete_movie(media, dry_run)
