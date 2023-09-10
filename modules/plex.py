"""Plex module for interacting with the Plex API."""
from plexapi.server import PlexServer
from datetime import datetime


class PlexService:
    """Plex Service class for interacting with the Plex API."""

    plex_server: PlexServer

    def __init__(self, plex_url: str, plex_token: str):
        """Initialize the Plex Service class."""
        self.plex_server = PlexServer(plex_url, plex_token)

    def __media_is_expired(self, media, exp_date: datetime) -> bool:
        """True if media is expired"""
        if media.lastViewedAt is not None:
            if media.lastViewedAt < exp_date:
                return True
        elif media.addedAt is not None:
            if media.addedAt < exp_date:
                return True
        return False

    # def __season_is_expired(self, season, exp_date: datetime) -> bool:
    #     """True if season is expired"""
    #     return all(
    #         self.__media_is_expired(episode, exp_date)
    #         for episode in season.episodes()
    #     )
    
    # def __show_is_expired(self, show, exp_date: datetime) -> bool:
    #     """True if show is expired"""
    #     return all(
    #         self.__season_is_expired(season, exp_date)
    #         for season in show.seasons()
    #     )

    def __get_library_media(self, media_type: str):
        """Get all media from the Plex server."""
        return self.plex_server.library.search(libtype=media_type)

    def get_expired_media(self, media_type: str, exp_date: datetime):
        """Get all movies that have expired."""
        media = self.__get_library_media(media_type)
        expired_media = []
        for item in media:
            if self.__media_is_expired(item, exp_date):
                expired_media.append(item)
        return expired_media

    def get_expired_seasons(self, exp_date: datetime):
        """Get all seasons that have expired."""
        seasons = self.plex_server.library.search(libtype="season")
        expired_seasons = []
        for season in seasons:
            if self.__media_is_expired(season, exp_date):
                expired_seasons.append(season)
        return expired_seasons

    def get_expired_shows(self, exp_date: datetime):
        """Get all shows that have expired."""
        shows = self.plex_server.library.search(libtype="show")
        expired_shows = []
        for show in shows:
            if self.__media_is_expired(show, exp_date):
                expired_shows.append(show)
        return expired_shows