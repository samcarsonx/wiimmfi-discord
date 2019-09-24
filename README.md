
# wiimmfi-discord
 ![Last Commit](https://img.shields.io/github/last-commit/samcarsonx/wiimmfi-discord)
 ![Commits since last release](https://img.shields.io/github/commits-since/samcarsonx/wiimmfi-discord/latest)
 [![MIT Licence](https://img.shields.io/github/license/samcarsonx/wiimmfi-discord)](https://github.com/samcarsonx/wiimmfi-discord/blob/master/LICENSE)
 [![Forks](https://img.shields.io/github/forks/samcarsonx/wiimmfi-discord)](https://github.com/samcarsonx/wiimmfi-discord/fork)
 [![Stars](https://img.shields.io/github/stars/samcarsonx/wiimmfi-discord)](https://github.com/samcarsonx/wiimmfi-discord/stargazers)
 [![Open Issues](https://img.shields.io/github/issues/samcarsonx/wiimmfi-discord)](https://github.com/samcarsonx/wiimmfi-discord/issues)
 ![Using PyPresence](https://img.shields.io/badge/using-pypresence-00bb88.svg)
 ![Max-used language](https://img.shields.io/github/languages/top/samcarsonx/wiimmfi-discord)

Python 3.6+ rich presence client by **Sam Carson** for the **Wiimmfi servers.** Please reference [their wiki page](http://wiki.tockdom.com/wiki/Wiimmfi) for extra information.

## How to use
Using this is as simple as cloning the repo or heading over to the [releases section](https://github.com/samcarsonx/wiimmfi-discord/releases) and downloading it. Run `python3 main.py` in a terminal and after the first use it will probably say that the config contains default values. That will be covered in the next section:

## Configuration
There are two config files, `friend_codes.py` and `status.py` (they are in py format so loading is as simple as importing)
### friend_codes.py
```
data = [
    {
        "game": "XXXX",
        "friend_code": "XXXX-XXXX-XXXX-XXXX"
    }
]
```
**To edit:** 
* change `game` to any in [this huge list](https://wiimmfi.de/stat?m=25)
* change `friend_code` to the 16 digit code you have in the specified game.

*Extended functionality is supported for Mario Kart Wii, its code is `RMCJ`.*
*Only hyphens and digits are supported in the friend code.*

### status.py
```
data = {
    "0": "Offline",
    "1": "In the menus",
    "2": "In a room",
    "3": "Searching for opponents",
    "4": "Connecting to private room",
    "5": "Hosting a room",
    "6": "Special brawling"
}
```
**To edit:**
* **keep the key names, such as `"1"` the same**, but the messages can be edited; these are the default values.

*Status 6 is specific for Super Smash Bros Brawl for an unknown reason*

## Roadmap
In the future, I plan on re-writing this to make it clearer and faster to use.
