"""Sonarr Observer class for the Observer pattern."""
from modules.subscribers.subscribers import Observer

class SonarrObserver(Observer):
    """Sonarr Observer class for the Observer pattern."""

    def on_media_deleted(self, media: str):
        print(f"SonarrObserver: {media} deleted")
