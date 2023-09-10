"""Module for handling the config file"""
import os
from argparse import Namespace
from configparser import ConfigParser


def __get_config_path() -> str:
    """Get the path to the config file"""
    config_root_dir = os.getenv("ETC")
    if config_root_dir is None:
        config_root_dir = os.path.expanduser("~\\.config")
    config_dir = os.path.join(config_root_dir, "prunerr")
    config_file_path = os.path.join(config_dir, "config.ini")
    os.makedirs(config_dir, exist_ok=True)
    return config_file_path


def load_config() -> ConfigParser:
    """Load the config file into memory"""
    config = ConfigParser()
    config.read(__get_config_path())
    return config


def __save_config(config: ConfigParser):
    """Save the config file to disk"""
    with open(__get_config_path(), mode="w", encoding="utf-8") as file:
        config.write(file)


def __configure_plex(config: ConfigParser, plex_host: str, plex_token: str):
    """Configure the Plex settings"""
    config["plex"] = {"host": plex_host, "token": plex_token}
    __save_config(config)


def __configure_radarr(
    config: ConfigParser, host: str, api_key: str, enable: bool
):
    """Configure the Radarr settings"""
    config["radarr"] = {
        "host": host,
        "api_key": api_key,
        "enable": str(enable),
    }
    __save_config(config)


def __configure_sonarr(
    config: ConfigParser, host: str, api_key: str, enable: bool
):
    """Configure the Sonarr settings"""
    config["sonarr"] = {
        "host": host,
        "api_key": api_key,
        "enable": str(enable),
    }
    __save_config(config)


def __configure_overseerr(
    config: ConfigParser,
    host: str,
    api_key: str,
    enable: bool,
):
    """Configure the Overseerr settings"""
    config["overseerr"] = {
        "host": host,
        "api_key": api_key,
        "enable": str(enable),
    }
    __save_config(config)


def run(args: Namespace):
    """Run the config command"""
    if args.config_type == "plex":
        __configure_plex(load_config(), args.host, args.token)
    elif args.config_type == "radarr":
        __configure_radarr(
            load_config(), args.host, args.api_key, args.enable
        )
    elif args.config_type == "sonarr":
        __configure_sonarr(
            load_config(), args.host, args.api_key, args.enable
        )
    elif args.config_type == "overseerr":
        __configure_overseerr(
            load_config(),
            args.host,
            args.api_key,
            args.enable,
        )
    else:
        raise NotImplementedError("Invalid config type")
    print("Configuration saved")


def plex_is_configured() -> bool:
    """Returns True if Plex has been configured"""
    config = load_config()
    if "plex" not in config:
        return False
    if "host" not in config["plex"]:
        return False
    if "token" not in config["plex"]:
        return False
    return True
