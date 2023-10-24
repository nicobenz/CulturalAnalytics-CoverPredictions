import time
import requests
from icecream import ic
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import quote
import os
from datetime import datetime
from tqdm import tqdm
import logging


def sanitize_name(name):
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '', name)  # remove characters not allowed in directories
    sanitized_name = re.sub(r'\s+', ' ', sanitized_name)  # replace all whitespace with a single space
    return sanitized_name


def crawl_mb():
    url = "https://musicbrainz.org/ws/2/genre/all?fmt=txt"
    response = requests.get(url)

    genres = response.text.split("\n")

    with open("temp/scraping_progress.txt", "r") as f:
        starting_values = json.load(f)

    starting_point = starting_values["genre"]
    start_after_break = True
    for genre_idx in range(starting_point, len(genres)):  # ugly loop but easier for progress saving through genre index
        genre = genres[genre_idx]
        try:
            url = f"https://musicbrainz.org/tag/{genre}/artist"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            if start_after_break:
                artist_page = starting_values["page"]
                start_after_break = False
            else:
                artist_page = 1
            while True:
                encoded_genre = quote(genre)
                try:
                    url = f"https://musicbrainz.org/tag/{encoded_genre}/artist?page={artist_page}"
                    response = requests.get(url, allow_redirects=False)
                    if response.status_code != 200:
                        break
                    """
                    soup = BeautifulSoup(response.content, 'html.parser')
                    script_tag = soup.find('script', string=re.compile(r'Object.defineProperty\(window,"__MB__"'))
            
                    pattern = fr'https://musicbrainz\.org/tag/{encoded_genre}/artist\?page=\d+'
                    match = re.search(pattern, script_tag.text)
            
                    if match:
                        match = match.group()
                        current_page = int(match.split("=")[-1])
                    else:
                        ic(encoded_genre, script_tag.text)
                        break
                    if artist_page != current_page:  # leave loop when current page does not increment any more
                        break
                    """
                    artist_links = soup.select('a[href*="/artist/"]')
                    for idx, link in enumerate(artist_links):
                        artist_name = link["title"].split("(")[0].strip()

                        artist_mbid = link['href'].replace("/artist/", "")
                        release_page = 1
                        while True:
                            try:
                                url = f"https://musicbrainz.org/artist/{artist_mbid}/releases?page={release_page}"
                                response = requests.get(url, allow_redirects=False)
                                if response.status_code != 200:
                                    break
                                soup = BeautifulSoup(response.content, 'html.parser')
                                selected_releases = soup.select('a[href^="/release/"]:not([href*="/cover-art"])')

                                data = []
                                for release in selected_releases:
                                    keep_trying = True
                                    rel_id = release['href'].split('/')[-1]
                                    rel_title = release.bdi.text  # extract release title
                                    data.append({'release_id': rel_id, 'title': rel_title})
                                    while keep_trying:
                                        try:
                                            url = f"https://coverartarchive.org/release/{rel_id}"
                                            response = requests.get(url, allow_redirects=False)

                                            if response.status_code == 307:
                                                redirect_url = response.headers['Location']
                                                redirected_response = requests.get(redirect_url)

                                                if redirected_response.status_code == 200:
                                                    cover_json = json.loads(redirected_response.text)

                                                    for cover in cover_json["images"]:
                                                        if cover["front"]:
                                                            url = f"https://coverartarchive.org/release/{rel_id}/{cover['id']}-1200.jpg"
                                                            response = requests.get(url, stream=True)

                                                            if response.status_code == 200:
                                                                save_path = (f"data/genre/{sanitize_name(genre)}/"
                                                                             f"{artist_mbid}_{sanitize_name(artist_name)}/"
                                                                             f"{rel_id}_{sanitize_name(rel_title)}")
                                                                if not os.path.exists(save_path):
                                                                    os.makedirs(save_path)
                                                                with open(f"{save_path}/front-1200.jpg", 'wb') as f:
                                                                    f.write(response.content)
                                                                print(f"\rSaved file: {rel_id} at {datetime.now()}", end="")
                                                            break
                                                keep_trying = False
                                            elif response.status_code == 503:
                                                print("Rate limit exeeded. Going to sleep and trying again in 10 min.")
                                                print("")
                                                for sec in range(600):
                                                    print(f"\rzzzZZZzzzZZZ... {sec:03d}/600", end="")
                                                    time.sleep(float(sec))
                                            else:
                                                keep_trying = False
                                        except ConnectionError as e:
                                            ic(e)
                                            print("Trying again in two minutes...")
                                            time.sleep(120)
                                release_page += 1
                            except ConnectionError as e:
                                ic(e)
                                print("Trying again in two minutes...")
                                time.sleep(120)
                    artist_page += 1
                    with open("temp/scraping_progress.txt", "w") as f:
                        progress = {
                            "genre": genre_idx,
                            "page": artist_page
                        }
                        json.dump(progress, f)
                except ConnectionError as e:
                    ic(e)
                    print("Trying again in two minutes...")
                    time.sleep(120)
        except ConnectionError as e:
            ic(e)
            print("Trying again in two minutes...")
            time.sleep(120)


def process_request(url, save_name, resolution="500"):
    pass
    """
            for cover in cover_json["images"]:
                if cover["front"]:
                    url = f"https://coverartarchive.org/release/{rel_id}/{cover['id']}-1200.jpg"
                    response = requests.get(url, stream=True)

                    if response.status_code == 200:
                        save_path = (f"data/covers/genre/{sanitize_name(genre)}/"
                                     f"{artist_mbid}_{sanitize_name(artist_name)}/"
                                     f"{rel_id}_{sanitize_name(rel_title)}")
                        if not os.path.exists(save_path):
                            os.makedirs(save_path)
                        with open(f"{save_path}/front-1200.jpg", 'wb') as f:
                            f.write(response.content)
                        print(f"\rSaved file: {rel_id} at {datetime.now()}", end="")
                    break
        keep_trying = False
    elif response.status_code == 503:
        print("Rate limit exeeded. Going to sleep and trying again in 10 min.")
        print("")
        for sec in range(600):
            print(f"\rzzzZZZzzzZZZ... {sec:03d}/600", end="")
            time.sleep(float(sec))
    else:
        keep_trying = False
        """


def save_cover_ids():
    release_ids = []
    with open("data/releases.json", "r") as file:
        for idx, line in enumerate(file):
            release = json.loads(line)
            if release["front-cover-available"]:
                release_ids.append(release["release-id"])

    with open("data/cover_ids.txt", "w") as f:
        for release_id in release_ids:
            f.write(release_id)
            f.write("\n")


def get_covers(clear_log=False):
    if clear_log:
        with open("temp/progress.log", "w"):
            pass
    with open("data/cover_ids.txt", "r") as f:
        release_ids = f.readlines()
    release_ids = [rel_id.rstrip("\n") for rel_id in release_ids]

    last_request_time = time.time()

    # get the release ids of all covers that are already saved (to skip when script restarted)
    covers_500 = [f.split(".")[0] for f in os.listdir("/Volumes/Data/covers/covers/500")]
    covers_1200 = [f.split(".")[0] for f in os.listdir("/Volumes/Data/covers/covers/1200")]
    base_covers = [f.split(".")[0] for f in os.listdir("/Volumes/Data/covers/covers/image")]
    large_covers = [f.split(".")[0] for f in os.listdir("/Volumes/Data/covers/covers/large")]
    with open("temp/black_list.txt", "r") as f:
        black_list = f.readlines()
    black_list = [f.strip() for f in black_list]

    headers = {
        "User-Agent": "CulturalAnalyticsResearchCrawler/1.0 (nico.benz@studserv.uni-leipzig.de)"
    }

    for rel_id in tqdm(release_ids, bar_format="{percentage:.1f}%|{bar}{r_bar}"):
        # pass if cover already present in any resolution
        if any(rel_id in covers for covers in [covers_1200, covers_500, base_covers, large_covers, black_list]):
            pass
        else:
            # while true loop to not skip the id if server refuses request
            keep_trying = True
            while keep_trying:
                try:
                    url = f"https://coverartarchive.org/release/{rel_id}"
                    # calculate time passed since last request
                    passed_time = time.time() - last_request_time

                    # wait a bit because of limitation of 1 request per second
                    if passed_time < 1:
                        time.sleep(1 - passed_time)

                    response = requests.get(url, headers=headers, timeout=15)
                    last_request_time = time.time()
                    if response.status_code == 200:
                        # if valid request, server returns cover json
                        cover_json = json.loads(response.text)
                        keep_trying = False
                        # go over all covers returned by server
                        for image in cover_json["images"]:
                            # only process front covers
                            if image["front"]:
                                # go through resolution priority
                                download_url = image.get("thumbnails", {}).get("500", False)
                                save_path = "500"
                                if not download_url:
                                    download_url = image.get("thumbnails", {}).get("1200", False)
                                    save_path = "1200"
                                if not download_url:
                                    download_url = image.get("thumbnails", {}).get("large", False)
                                    save_path = "large"
                                if not download_url:
                                    download_url = image.get("image", False)
                                    save_path = "other"

                                if download_url:
                                    try:
                                        response = requests.get(download_url, headers=headers, timeout=15)
                                        if response.status_code == 200:
                                            with open(f"/Volumes/Data/covers/covers/{save_path}/{rel_id}.jpg", 'wb') as f:
                                                f.write(response.content)
                                            # leave loop after at least one cover has been saved
                                            break
                                    except requests.exceptions.Timeout:
                                        #print("Request timed out. Trying again in two minutes...")
                                        time.sleep(120)
                                    except requests.exceptions.HTTPError:
                                        pass
                                    except requests.exceptions.RequestException:
                                        pass
                            else:
                                with open("temp/black_list.txt", "a") as f:
                                    f.write(f"{rel_id}\n")
                    # 503 means api limit exceeded
                    elif response.status_code == 503:
                        logging.error("Limit exceeded. Trying again in two minutes.")
                        time.sleep(120)
                    # 404 means no cover for that release id
                    elif response.status_code == 404 or response.status_code == 403:
                        keep_trying = False
                        with open("temp/black_list.txt", "a") as f:
                            f.write(f"{rel_id}\n")
                except requests.exceptions.Timeout as timeout:
                    logging.error(f"Error {timeout}. Trying again in two minutes.")
                    time.sleep(120)
                except requests.exceptions.HTTPError as httperror:
                    logging.error(f"Error {httperror}. Trying again now.")
                except requests.exceptions.RequestException as reqex:
                    logging.error(f"Error {reqex}. Trying again now.")


logging.basicConfig(
    filename="temp/progress.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

get_covers(clear_log=True)
