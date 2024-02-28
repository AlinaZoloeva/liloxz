import getpass
import os
import sys
from pathlib import Path
from urllib.parse import urljoin
from pathlib import Path

import mutagen
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init, Fore
from tqdm import tqdm

init(autoreset=True)



def get_html(url: str) -> (str, bool):
    try:
        rs = requests.get(url=url,  timeout=5)
        return rs.text if rs.status_code == 200 else False
    except Exception:
        return False

def get_track(txt, t):
    temp = []
    soup = BeautifulSoup(txt, 'html.parser')
    all_muz = soup.find_all('div', class_="track__info")
    num = t * 48 + 1
    for muz in all_muz:
        title = muz.find('div', class_="track__title").text.strip()

        link = muz.find('div', class_="track__info-r").find('a').get('href')
        artist_song = muz.find('div', class_="track__desc").text.strip()

        duration = soup.find('div', class_="track__time").find('div', class_='track__fulltime').text.strip()
        time_track = f'{int(duration.split(":")[0]) * 60 + int(duration.split(":")[1])}'
        temp.append(f'#EXTINF:{time_track}, group-title="{artist_song}", {title}\n{link}\n')
        print(f'{num}) {artist_song} - {title}: {link}')
        num += 1
    return temp

def get_links(path: Path, iter_num: int, iter_link: str) -> (list, bool):
    temp = []

    if iter_num == 0:
        if txt := get_html(f'{iter_link}0'):
            temp.extend(get_track(txt, 0))
    else:
        for i in range(0, iter_num+1, 48):
            link = f'{iter_link}/start/{i}'

            if txt := get_html(link):
                temp.extend(get_track(txt, i // 48))


    if temp:
        path.mkdir(exist_ok=True)
        with open(path / f'{path.name}_web.m3u', mode='w', encoding='utf-8') as file:
            file.write("#EXTM3U\n")
            for item in temp:
                file.write(item)
        return [x.split("\n")[1].strip() for x in temp], len(temp)
    return False

def track_download(url, path) -> bool:
    filename = ""
    try:
        rs = requests.get(url=url, stream=True)
        if rs.status_code == 200:
            file_size = int(rs.headers.get("Content-Length", 0))
            filename = Path(url).name
            if os.path.exists(f'{path}\{filename}'):
                print(Fore.RED + 'Трек уже загружен')
                return
            progress = tqdm(rs.iter_content(1024), f"{Fore.GREEN}Downloading: {Fore.RESET}"
                                                   f"{filename}", total=file_size, unit="B",
                            unit_scale=True, unit_divisor=1024)
            with open(path / filename, "wb") as f:
                for data in progress.iterable:
                    f.write(data)
                    progress.update(len(data))
        return False
    except KeyboardInterrupt:
        (path / filename).unlink()
        print(f"\n{Fore.GREEN}До свидания: {Fore.RESET}{getpass.getuser()}\n")
        sys.exit(0)
    except Exception:
        print(f"Не удалось загрузить: {url}")
        return False


url = 'https://rus.hitmotop.com/songs/top-today'
dir_path = Path.home()
path = Path(dir_path, 'repos', 'parsing_tracks', 'music')
try:
    count_list = int(input('Сколько страниц из раздела "Популярные треки" вы хотите загрузить? '))
except:
    count_list = 1
count_list -= 1
temp = get_links(path, count_list * 48, url)

tracks = temp[0]

for track in tracks:
    track_download(track, path)

