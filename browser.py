import sys
import pathlib
import requests
from bs4 import BeautifulSoup
import colorama

saved_tabs = {}
history = []
colorama.init()

if len(sys.argv) == 2:
    save_folder = sys.argv[1]
else:
    print("error: invalid  num of arguments")


def tab_is_saved(name):
    if name.startswith('https://'):
        name = name.replace('https://', '')
    for adr in saved_tabs:
        if name in adr:
            return adr
    return None


while True:
    req = input('> ')
    if req == 'exit':
        break
    elif tab_is_saved(req):
        with open(saved_tabs[tab_is_saved(req)]) as f:
            print(f.read())
        history.append(req)
    elif '.' in req:
        if not req.startswith('https://'):
            req = 'https://' + req

        resp = requests.get(req)
        soup = BeautifulSoup(resp.content)
        text =''
        for tag in soup.find_all('a'):
            tag.string = colorama.Fore.BLUE + tag.text + colorama.Fore.WHITE
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',  'a', 'ul', 'ol', 'li']):
            text += tag.text
        print(text)
        file_name = req.replace('https://', '')
        saved_tabs[req] = save_folder + '/' + file_name + '.txt'
        pathlib.Path(save_folder).mkdir(parents=True, exist_ok=True)

        with open(saved_tabs[req], 'w', encoding='utf-8') as f:
            f.write(text)
            history.append(req)

    elif req == 'back':
        if prev_req != 'back':
            history.pop()
        if history:
            with open(saved_tabs[tab_is_saved(history.pop())]) as f:
                print(f.read())
    else:
        print('error')
    prev_req = req