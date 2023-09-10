"""Overseerr Observer class for the Observer pattern."""
import requests
from observers import Observer


class OverseerrObserver(Observer):
    """Overseerr Observer class for the Observer pattern."""

    def __init__(self, overseerr_host: str, overseerr_api_key: str):
        """Initialize the Overseerr observer."""
        super().__init__("all")
        self.session = requests.Session()
        self.session.headers.update({"X-API-KEY": overseerr_api_key})
        self.session.base_url = overseerr_host
        self.page_size = 150

    def __search_requests(self, rating_key: str, page: int = 0):
        """Search requests from Overseerr."""
        url = f"{self.session.base_url}/api/v1/request?take={self.page_size}&skip={page * self.page_size}"
        response = self.session.get(url).json()
        result = next(
            iter(
                [
                    result
                    for result in response["results"]
                    if result["media"]["ratingKey"] == str(rating_key)
                ]
            ),
            None,
        )
        if result is None and page < int(response["pageInfo"]["pages"]):
            return self.__search_requests(rating_key, page + 1)
        return result

    def __search_media(self, rating_key: str, page: int = 0):
        """Search media from Overseerr."""
        response = self.session.get(
            f"{self.session.base_url}/api/v1/media?take={self.page_size}&skip={page * self.page_size}"
        ).json()
        result = next(
            iter(
                [
                    result
                    for result in response["results"]
                    if result["ratingKey"] == str(rating_key)
                ]
            ),
            None,
        )
        if result is None and page < int(response["pageInfo"]["pages"]):
            return self.__search_media(rating_key, page + 1)
        return result

    def __delete_request(self, rating_key: str, dry_run: bool):
        """Delete a request from Overseerr."""
        request = self.__search_requests(rating_key)
        if request is None:
            print(f"Overseerr: {rating_key} Request not found")
            return
        if not dry_run:
            response = self.session.delete(
                f'{self.session.base_url}/api/v1/request/{request["id"]}'
            )
            print(f"[OVERSEERR][DELETE][REQUEST]: {response.status_code}")
        else:
            print("Dry run, not sending DELETE REQUEST to Overseerr")

    def __delete_media(self, rating_key: str, dry_run: bool):
        """Delete a media from Overseerr."""
        media = self.__search_media(rating_key)
        if media is None:
            print(f"Overseerr: {rating_key} Media not found")
            return
        if not dry_run:
            response = self.session.delete(
                f'{self.session.base_url}/api/v1/media/{media["id"]}'
            )
            print(f"[OVERSEERR][DELETE][MEDIA]: {response.status_code}")
        else:
            print("Dry run, not sending DELETE MEDIA to Overseerr")

    def on_media_deleted(self, media, dry_run: bool):
        """Called when a media item is deleted."""
        self.__delete_request(media.ratingKey, dry_run)
        self.__delete_media(media.ratingKey, dry_run)
