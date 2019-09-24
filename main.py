import os
import sys
import traceback
import urllib.request as r
import requests
import json
import time
from pypresence import Presence
from bs4 import BeautifulSoup as BeautifulSoup
from datetime import datetime

now = datetime.utcnow()

# Client ID for the rich presence, only change if you know what you're doing!
client_id = '625708112883613707'
RPC = Presence(client_id)


def check_files():
    if not os.path.exists('logs'):
        print("Error log folder not found, creating...")
        os.mkdir('logs')
    if not os.path.exists('configs'):
        print("Config folder not found, creating...")
        os.mkdir('configs')

    if not os.path.exists('configs/status.py'):
        print("Status language file not found, creating...")
        with open('configs/status.py', 'a+') as f:
            f.write('''data = {
"0": "User offline",
"1": "In the menus",
"2": "In a room",
"3": "Searching for opponents",
"4": "Connecting to private room",
"5": "Hosting a room",
"6": "Special brawling"
}
''')

    if not os.path.exists('configs/friend_codes.py'):
        print("Friend codes config not found, creating...")
        with open('configs/friend_codes.py', 'a+') as f:
            f.write('''data = [
    {
        "game": "XXXX",
        "friend_code": "XXXX-XXXX-XXXX-XXXX"
    }
]
''')
    from configs.friend_codes import data as fc_data
    if len(fc_data) > 1:
        print('Only one friend code is supported at this time.\n')
        sys.exit()
    for x in fc_data:
        if any(not c.isdigit() for c in x['friend_code'].replace('-', '')):
            print('Friend code has non-digits or default values.\n')
            sys.exit()


def exception_handler(exc_type, exc_value, tb):
    if exc_type == KeyboardInterrupt:
        RPC.close()
        sys.exit()  # If user manually exits, don't log crash

    print('\nOh no! An unhandled error has occured. Building traceback log...')

    with open('logs/{0.day}.{0.month}.{0.year}.log'.format(now), 'a+') as f:
        f.write('-- CRASH AT {0.hour}:{0.minute}:{0.second} --\n'.format(now))
        f.write(f'LINE: {tb.tb_lineno}\n')
        f.write(f'NEXT: {tb.tb_next}\n')
        f.write(f'TYPE: {exc_type}\n')
        f.write(f'VALUE: {exc_value}\n')
        f.write('-- FULL TRACEBACK --\n')
        f.write(''.join(traceback.format_exception(exc_type, exc_value, tb)))

    print('Created traceback. Please send this file as an issue on GitHub:')
    print('logs/{0.day}.{0.month}.{0.year}.log\n'.format(now))

    RPC.close()
    sys.exit()


sys.excepthook = exception_handler


class GUI():
    def __init__(self):
        self.main_menu()

    def clear(self):
        os.system('cls' if sys.platform.startswith('win') else 'clear')
        print('Wiimmfi-Discord by @samcarsonx on GitHub')
        print('Discord rich presence client for the Wiimmfi servers')
        print('----------------------------------------------------\n')

    def main_menu(self):
        self.clear()
        print('What would you like to do?')
        print('1. Connect to RPC')
        print('2. Exit\n')

        done = False
        while not done:
            choice = input('> ')
            print(choice)
            actions = {
                '1': listen,
                '2': sys.exit
                }
            try:
                to_do = actions[choice]
            except KeyError:
                print('Unknown choice.')
                continue
            done = True
            self.clear()
            to_do()


def listen():
    RPC.connect()
    while True:
        get_game_data()
        time.sleep(5)
        print()


def get_game_data():
    gameData = {}
    dataFound = False

    from configs.friend_codes import data as fc_data
    from configs.status import data as status

    game = fc_data[0]['game']
    player = fc_data[0]['friend_code']

    html = requests.get('https://wiimmfi.de/game/' + game).text
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find(id='online')
    if not table:  # Game not found
        print(f'No such game with ID "{game}" was found!')
        return
    elif not table.text:  # Nobody online
        print('Nobody is online in this game.')
        return

    rows = table.find_all('tr')
    data = [[ele.text for ele in row.find_all('td')] for row in rows[2:]]
    for i in data:
        if i[2] != player:
            continue
        gameData['name'] = i[10]
        gameData['status'] = status[i[7]]
        dataFound = True
    if not dataFound:
        print(f'User "{player}" not online.')
        RPC.update(
            state=status["0"],
            instance=False,
            large_image="wiimmfi-offline",
            large_text=status["0"]
        )
        return

    if game == "RMCJ":
        with r.urlopen("https://wiimmfi.de/mkw/room/?m=json") as url:
            data = json.loads(url.read().decode())
            for i in data:
                try:
                    if any(j['fc'] == player for j in i['members']):
                        gameData['players'] = i['members']
                        gameData['track'] = i['track_name']
                except Exception:
                    pass
        if 'track' in gameData:
            track = gameData['track']
            track = "Not in a game" if track == "" else track

            print("Mario Kart Wii : ", end="")
            print(gameData['name'], end=" : ")
            print(gameData['status'], end=" : ")
            print(len(gameData['players']), end="/12 : ")
            print(track, end="\n")

            RPC.update(
                state=gameData['status'],
                details=track,
                party_size=[len(gameData['players']), 12],
                instance=True,
                small_image="wiimmfi",
                small_text="Wiimmfi",
                large_image="mariokart",
                large_text="Mario Kart Wii"
            )
            return
        print(f"Mario Kart Wii : {gameData['name']} : {gameData['status']}")
        RPC.update(
            state=gameData['status'],
            details=gameData['name'],
            instance=False,
            small_image="wiimmfi",
            small_text="Wiimmfi",
            large_image="mariokart",
            large_text="Mario Kart Wii"
        )
        return

    print(f"{gameData['name']} : {gameData['status']}")
    RPC.update(
        state=gameData['status'],
        details=gameData['name'],
        instance=False,
        large_image="wiimmfi",
        large_text="Wiimmfi"
    )


def main():
    check_files()
    GUI()


if __name__ == '__main__':
    main()
