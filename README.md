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

## Example Output
```
Pruning media older than 2023-08-11 18:25:53.115871...
Getting expired movies...
Found 1 expired movies:
Movie: Unforgiven, Last Viewed: None, Added: 2023-08-11 18:20:53, Age: 30 days, 0:05:06.705732
1/1 - Deleting Unforgiven (7892)...
[PLEX][DELETE]: OK
[RADARR][DELETE]: 200
[OVERSEERR][DELETE][REQUEST]: 204
[OVERSEERR][DELETE][MEDIA]: 204
Done deleting expired movies.
---------------------------------------
Getting expired shows...
Found 4 expired shows:
Show: The Walking Dead, Last Viewed: None, Added: 2022-10-10 03:37:24, Age: 335 days, 14:48:39.375397
Show: The Rehearsal, Last Viewed: 2022-08-21 20:31:07, Added: 2022-11-12 07:01:04, Age: 384 days, 21:54:56.376397
Show: Berserk, Last Viewed: 2022-04-15 04:26:34, Added: 2022-11-12 07:12:20, Age: 513 days, 13:59:29.376397
Show: Demon Slayer: Kimetsu no Yaiba, Last Viewed: 2022-04-10 17:21:16, Added: 2022-04-10 16:14:09, Age: 518 days, 1:04:47.376397
1/4 - Deleting The Walking Dead (4101)...
[PLEX][DELETE]: OK
[SONARR][DELETE]: 200
[OVERSEERR][DELETE][REQUEST]: 204
[OVERSEERR][DELETE][MEDIA]: 204
2/4 - Deleting The Rehearsal (4467)...
[PLEX][DELETE]: OK
[SONARR][DELETE]: 200
[OVERSEERR][DELETE][REQUEST]: 204
[OVERSEERR][DELETE][MEDIA]: 204
3/4 - Deleting Berserk (4883)...
[PLEX][DELETE]: OK
[SONARR][DELETE]: 200
[OVERSEERR][DELETE][REQUEST]: 204
[OVERSEERR][DELETE][MEDIA]: 204
4/4 - Deleting Demon Slayer: Kimetsu no Yaiba (6209)...
[PLEX][DELETE]: OK
[SONARR][DELETE]: 200
Overseerr: 6209 Request not found
[OVERSEERR][DELETE][MEDIA]: 204
Done deleting expired shows.
```