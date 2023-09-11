"""Get the parsers for the command-line application."""
import argparse


def __create_subparser_config(subparsers):
    """Create the subparser for the config command"""
    subparser = subparsers.add_parser(
        "config", help="Configure: Plex, Radarr, Sonarr or Overseerr"
    )

    subsubparsers = subparser.add_subparsers(dest="config_type", required=True)

    # Plex
    plex_parser = subsubparsers.add_parser("plex", help="Configure Plex")
    plex_parser.add_argument(
        "--host", required=True, help="Plex Hostname or IP Address"
    )
    plex_parser.add_argument("--token", required=True, help="Plex API Token")

    # Optional modules

    # Radarr
    radarr_parser = subsubparsers.add_parser("radarr", help="Configure Radarr")
    radarr_parser.add_argument(
        "--host", required=False, help="Radarr Hostname or IP Address"
    )
    radarr_parser.add_argument(
        "--api-key", required=False, help="Radarr API Token"
    )
    radarr_parser.add_argument(
        "--enable",
        required=False,
        help="Enable/disable posting to Radarr when movies are deleted",
        default=True
    )

    # Sonarr
    sonarr_parser = subsubparsers.add_parser("sonarr", help="Configure Sonarr")
    sonarr_parser.add_argument(
        "--host", required=True, help="Sonarr Hostname or IP Address"
    )
    sonarr_parser.add_argument("--api-key", required=True, help="Sonarr API Token")
    sonarr_parser.add_argument(
        "--enable",
        required=False,
        help="Enable/disable posting to Sonarr when shows or episodes are deleted",
        default=True
    )

    # Overseerr
    overserr_parser = subsubparsers.add_parser("overseerr", help="Configure Overseerr")
    overserr_parser.add_argument(
        "--host", required=True, help="Overseerr Hostname or IP Address"
    )
    overserr_parser.add_argument(
        "--api-key", required=True, help="Overseerr API Token"
    )
    overserr_parser.add_argument(
        "--enable",
        required=False,
        help="Enable/disable posting to Overseerr when media is deleted",
        default=True
    )

    return subparser


def __create_subparser_prune(subparsers):
    """Create the subparser for the prune command"""
    subparser = subparsers.add_parser("prune", help="Prune media from Plex")

    subparser.add_argument(
        "-de", "--days-to-expire", required=True, help="Number of days to keep media"
    )

    subparser.add_argument(
        "--dry-run",
        required=False,
        help="Dry run, do not delete media",
        action="store_true",
    )

    subparser.add_argument(
        "-rl", "--refresh-libraries",
        required=False,
        help="Refresh Plex libraries after pruning",
        action="store_true"
    )

    return subparser


def create_parser():
    """Create the parsers for the command-line application"""
    parser = argparse.ArgumentParser(
        prog="Prunerr",
        description="Command Line tool for pruning a Plex Media Library \
            and optionally syncing Radarr/Sonarr/Overseerr",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    __create_subparser_config(subparsers)
    __create_subparser_prune(subparsers)

    return parser
