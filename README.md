# Prunerr
This is a command line python app for cleaning up old media from Plex and optionally notifying Sonarr, Radarr and Overseerr.

For a more robust and automated solution, see: [Eraserr](https://github.com/everettsouthwick/Eraserr)

## Installing
Currently no installer exists. Clone the repo and run main.py using python in a shell of your choice.

## Usage
### Configure Plex
This is a required first-run command.
```bash
$ python main.py config plex --host "https://plex.mysite.com" --token "myplextoken"
```

### Configure RR modules
These modules are all optional.
```bash
$ python main.py config sonarr --host "https://sonarr.mysite.com" --api-key "myapikey"
```
```bash
$ python main.py config radarr --host "https://radarr.mysite.com" --api-key "myapikey"
```
```bash
$ python main.py config overseerr --host "https://overseerr.mysite.com" --api-key "myapikey"
```

> Note: The config.ini file is located in `~/.config/prunerr` where `~` represents your home/user directory.
Keep in mind there's an optional Enable= property for each module that gets set to `True` upon first configuration. If you later want to disable a module, update the `config.ini` file and set it to `False`.

### Prune
The prune command is the main command. 

A prune will:
- Delete Movies if last watched or added > {days-to-expire} ago.
- Delete Shows if last watched or added > {days-to-expire} ago.
    - Only considers entire show; not per episode or per season.
    - Note: In order for Plex to consider a show "watched," it must have one episode marked as watched. This means it will not consider a show watched if only part of an episode was watched.

#### Prune for 30 days:
```bash
$ python main.py prune --days-to-expire 30
```

#### Preview a Prune (don't actually delete anything):
```bash
$ python main.py prune --days-to-expire 30 --dry-run
```

#### Prune and refresh Plex libraries after finished.
```bash
$ python main.py prune --days-to-expire 30 --refresh-libraries
```