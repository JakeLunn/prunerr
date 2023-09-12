"""Utility functions for Prunerr"""
from datetime import datetime, timedelta
from plexapi.media import Media

# Note: Sometimes lastViewedAt is younger than addedAt because
# it was previously viewed, deleted, then re-added

class ExtendedMedia(Media):
    """Extended Media class with added attributes."""
    lastViewedAt: datetime
    addedAt: datetime

def media_age(media: ExtendedMedia) -> timedelta:
    """Get the age timedelta of a media item."""
    age = datetime.now() - media.addedAt

    if media.lastViewedAt is not None and media.lastViewedAt > media.addedAt:
        age = datetime.now() - media.lastViewedAt
    return age

def media_is_expired(media: ExtendedMedia, exp_date: datetime) -> bool:
    """True if media is expired"""
    if media.lastViewedAt is not None and media.lastViewedAt > media.addedAt:
        return media.lastViewedAt < exp_date
    return media.addedAt < exp_date
