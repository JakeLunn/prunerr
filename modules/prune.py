"""Prune command module."""
from argparse import Namespace
from datetime import datetime, timedelta
from retrying import retry
from observers import Subject
from observers.overseerr import OverseerrObserver
from observers.radarr import RadarrObserver
from observers.sonarr import SonarrObserver
from requests.exceptions import ReadTimeout
from modules.plex import PlexService
from modules.config import load_config


class PruneService(Subject):
    """Pruner class with Observer pattern."""

    def __init__(self):
        super().__init__()
        config = load_config()
        self._api = PlexService(config["plex"]["host"], config["plex"]["token"])
        self.__init_observers()

    def __init_observers(self):
        """Initialize all observers."""
        config = load_config()
        if (
            config.has_option("radarr", "enable")
            and config["radarr"]["enable"] == "True"
        ):
            self.attach(
                RadarrObserver(config["radarr"]["host"], config["radarr"]["api_key"])
            )
        if (
            config.has_option("sonarr", "enable")
            and config["sonarr"]["enable"] == "True"
        ):
            self.attach(
                SonarrObserver(config["sonarr"]["host"], config["sonarr"]["api_key"])
            )
        if (
            config.has_option("overseerr", "enable")
            and config["overseerr"]["enable"] == "True"
        ):
            self.attach(
                OverseerrObserver(
                    config["overseerr"]["host"], config["overseerr"]["api_key"]
                )
            )

    def __get_age(self, media):
        """Get the age timedelta of a media item."""
        age = datetime.now() - media.addedAt
        if media.lastViewedAt is not None:
            age = datetime.now() - media.lastViewedAt
        return age

    def __retry_if_read_timeout(self, exception):
        """Return True if we should retry (in this case when it's a ReadTimeout), False otherwise"""
        return isinstance(exception, ReadTimeout)

    @retry(
        stop_max_attempt_number=3,
        wait_fixed=5000,
        retry_on_exception=__retry_if_read_timeout,
    )
    def __delete_media(self, media, dry_run: bool):
        """Delete a media item."""
        if not dry_run:
            media.delete()
            print("[PLEX][DELETE]: OK")
        else:
            print("Dry run, not deleting from Plex")
        self.notify_media_deleted(media, dry_run)

    def __prune_expired_movies(self, exp_date: datetime, dry_run: bool):
        """Process all expired movies."""
        print("Getting expired movies...")
        expired_movies = self._api.get_expired_media("movie", exp_date)
        print(f"Found {len(expired_movies)} expired movies:")
        expired_movies.sort(key=self.__get_age)
        for movie in expired_movies:
            print(
                (
                    f"Movie: {movie.title}, "
                    f"Last Viewed: {movie.lastViewedAt}, "
                    f"Added: {movie.addedAt}, "
                    f"Age: {self.__get_age(movie)}"
                )
            )
        count = 1
        for movie in expired_movies:
            print(
                f"{count}/{len(expired_movies)} - Deleting {movie.title} ({movie.ratingKey})..."
            )
            self.__delete_media(movie, dry_run)
            count += 1
        print("Done deleting expired movies.")

    def __prune_expired_shows(self, exp_date: datetime, dry_run: bool):
        """Process all expired shows"""
        print("Getting expired shows...")
        expired_shows = self._api.get_expired_shows(exp_date)
        print(f"Found {len(expired_shows)} expired shows:")
        expired_shows.sort(key=self.__get_age)
        for show in expired_shows:
            print(
                (
                    f"Show: {show.title}, "
                    f"Last Viewed: {show.lastViewedAt}, "
                    f"Added: {show.addedAt}, "
                    f"Age: {self.__get_age(show)}"
                )
            )
        count = 1
        for show in expired_shows:
            print(
                f"{count}/{len(expired_shows)} - Deleting {show.title} ({show.ratingKey})..."
            )
            self.__delete_media(show, dry_run)
            count += 1
        print("Done deleting expired shows.")

    def prune(self, args: Namespace):
        """Prune media from Plex."""
        exp_date = datetime.now() - timedelta(days=int(args.days_to_expire))
        dry_run = args.dry_run

        print(f"Pruning media older than {exp_date}...")
        self.__prune_expired_movies(exp_date, dry_run)
        print("---------------------------------------")
        self.__prune_expired_shows(exp_date, dry_run)
        print("Done pruning media.")
        print("---------------------------------------")

        if args.refresh_libraries and not dry_run:
            print("Refreshing Plex libraries...")
            self._api.refresh_libraries()
            print("Done refreshing Plex libraries.")
