"""Radarr Observer class for the Observer pattern."""
from observers import Observer

class RadarrObserver(Observer):
    """Radarr Observer class for the Observer pattern."""

    def on_media_deleted(self, media: str, dry_run: bool):
        print("RadarrObserver: not implemented")
