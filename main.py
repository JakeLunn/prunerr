"""Command Line tool for pruning a Plex Media Library and syncing Radarr/Sonarr/Overseerr"""
from modules.argparser import create_parser
from modules.config import plex_is_configured
from modules.config import run as config_run
from modules.prune import PruneService


def main():
    """Main function."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "config":
        config_run(args)
    elif args.command == "prune":
        if not plex_is_configured():
            print("Plex is not configured, please run `prunerr config plex`")
            return
        PruneService().prune(args)

main()
