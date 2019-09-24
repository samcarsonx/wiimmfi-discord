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
        os.mkdir('logs')
    if not os.path.exists('configs'):
        os.mkdir('configs')

    if not os.path.exists('configs/status.py'):
        with open('configs/status.py', 'a+') as f:
            f.write('''data = {
"0": "Offline",
"1": "In the menus",
"2": "In a room",
"3": "Searching for opponents",
"4": "Connecting to private room",
"5": "Hosting a room",
"6": "Special brawling"
}
''')

    if not os.path.exists('configs/friend_codes.py'):
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
            print('Config contains invalid characters.\n')
            sys.exit()


def exception_handler(exc_type, exc_value, tb):
    if exc_type == KeyboardInterrupt:
        sys.exit()  # If user manually exits, ignore

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
        if get_game_data():  # Returns True if no data found
            RPC.close()
            sys.exit()
        print()
        time.sleep(5)


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
        return True
    elif not table.text:  # Nobody online
        print('Nobody is online in this game.')
        return True

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
            state='User offline',
            instance=False,
            large_image="wiimmfi",
            large_text='Offline'
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
            print(gameData['name'], end=" : ")
            print(gameData['status'], end=" : ")
            print(len(gameData['players']), end="/12 : ")
            print(gameData['track'], end="\n")

            RPC.update(
                state=gameData['status'],
                details=gameData['track'],
                party_size=[len(gameData['players']), 12],
                instance=True,
                large_image="wiimmfi",
                large_text=gameData['name']
            )
            return
        print(f"{gameData['name']} : {gameData['status']}")
        RPC.update(
            state=gameData['status'],
            instance=False,
            large_image="wiimmfi",
            large_text=gameData['name']
        )


def main():
    check_files()
    GUI()


if __name__ == '__main__':
    main()