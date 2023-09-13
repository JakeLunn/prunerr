"""Observer classes for Subscribers"""

class Observer:
    """Observer interface for the Observer pattern."""
    def __init__(self, media_type: str):
        """Initialize the observer."""
        self.media_type = media_type

    def on_media_deleted(self, media, dry_run: bool):
        """Called when a media item is deleted."""

    def on_prune_finished(self, dry_run: bool):
        """Called when a prune has finished executing"""

class Subject(Observer):
    """Subject class for the Observer pattern."""

    def __init__(self):
        """Initialize the subject."""
        super().__init__("Subject")
        self._observers = []

    def attach(self, observer):
        """Attach an observer to the subscription."""
        self._observers.append(observer)

    def detach(self, observer):
        """Detach an observer from the subscription."""
        self._observers.remove(observer)

    def notify_media_deleted(self, media, dry_run: bool):
        """Notify all observers that a media item has been deleted."""
        for observer in self._observers:
            if observer.media_type in ("all", media.type):
                observer.on_media_deleted(media, dry_run)

    def notify_prune_finished(self, dry_run: bool):
        """Notify all observers that a dry run has completed"""
        for observer in self._observers:
            if observer.media_type == "all":
                observer.on_prune_finished(dry_run)
