"""Sonarr Observer class for the Observer pattern."""
import requests
from plexapi.exceptions import NotFound
from observers import Observer


class SonarrObserver(Observer):
    """Sonarr Observer class for the Observer pattern."""

    def __init__(self, host: str, api_key: str):
        """Initialize the Sonarr observer."""
        super().__init__("show")
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": api_key})
        self.session.base_url = host

    def __search_series(self, media):
        """Search series from Sonarr"""
        tvdbid = next(
            iter([guid for guid in media.guids if guid.id.startswith("tvdb://")]), None
        )
        if tvdbid is None:
            print("Sonarr - No tmdbid found for media, skipping delete from Sonarr")
            return
        id_str = str(tvdbid.id).removeprefix("tvdb://")
        response = self.session.get(
            f"{self.session.base_url}/api/v3/series?tvdbid={id_str}"
        ).json()[0]
        if response["id"] is None:
            return None
        return response

    def __delete_series(self, media, dry_run: bool):
        """Delete series from Sonarr"""
        series = self.__search_series(media)
        if series is None:
            print(f"Sonarr - Series {media.title} not found")
            return
        if dry_run:
            print("Dry run, not deleting from Sonarr")
            return
        response = self.session.delete(
            f"{self.session.base_url}/api/v3/series/{series['id']}"
        )
        print(f"[SONARR][DELETE]: {response.status_code}")

    def on_media_deleted(self, media, dry_run: bool):
        """Delete a show from Sonarr."""
        try:
            self.__delete_series(media, dry_run)
        except NotFound as exception:
            print(f"Sonarr - exception occurred trying to delete series: {exception}")
