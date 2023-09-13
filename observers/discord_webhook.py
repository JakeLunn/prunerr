"""Sends message to configured webhook endpoint at the end of a dry run."""

import json
import requests
from textwrap import dedent
from plexapi.media import Media
from observers import Observer


class DiscordWebhook(Observer):
    """Webhook Observer class for the Observer pattern"""

    def __init__(self, webhook_url: str):
        super().__init__("all")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.webhook_url = webhook_url
        self.deleted_media = []

    def __get_json_body(self, fields: [], dry_run: bool) -> dict:
        embed_title = "Leaving Plex Soon"
        embed_description = "The following titles will be leaving Plex soon:"
        if not dry_run:
            embed_title = "Gone From Plex"
            embed_description = "The following titles have been deleted from Plex:"

        return {
            "embeds": [
                {
                    "title": embed_title,
                    "description": embed_description,
                    "fields": fields,
                    "color": 0xFFA700,
                    "thumbnail": {
                        "url": "https://media.discordapp.net/attachments/1087097209536921750/1151392300308627456/goodbye.gif"
                    },
                }
            ]
        }

    def on_media_deleted(self, media, _):
        self.deleted_media.append(media)

    def on_prune_finished(self, dry_run: bool):
        """When a prune has finished executing"""
        if len(self.deleted_media) == 0:
            return
        
        fields = []

        movie_titles = [f"- {media.title}" for media in self.deleted_media if media.type == "movie"]
        if len(movie_titles) > 0:
            movie_titles_str = "\n".join(movie_titles)
            fields.append({
                "name": "Movies",
                "value": f"{movie_titles_str}",
                "inline": False 
            })

        show_titles = [f"- {media.title}" for media in self.deleted_media if media.type == "show"]
        if len(show_titles) > 0:
            show_titles_str = "\n".join(show_titles)
            fields.append({
                "name": "Shows",
                "value": f"{show_titles_str}",
                "inline": False
            })

        fields.append({
            "name": "See a keeper?",
            "value": "Then get watching! Movies and shows are deleted if they go unwatched for too long. You can always re-request the deleted media on Overseerr, too.",
            "inline": False
        })

        body = self.__get_json_body(fields, dry_run)
        jsn = json.dumps(body)
        
        response = self.session.post(self.webhook_url, jsn)

        print(f"[DISCORD][WEBHOOK][POST]: {response.status_code}")
