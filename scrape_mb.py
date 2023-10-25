import time
import requests
import json
import os
from tqdm import tqdm
import logging


def save_cover_ids():
    """
    parses music-brains release json file and extracts front cover ids
    """
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


def get_covers(release_id_path:  str, clear_log=False):
    """
    iterates over all cover ids to save cover through coverarchive api
    :param release_id_path: path to file with release ids
    :param clear_log: overwrites log on start
    :return:
    """
    if clear_log:
        # opening a file in write mode and doing nothing clears the file
        with open("temp/progress.log", "w"):
            pass
    # read release ids from file
    with open(release_id_path, "r") as f:
        release_ids = f.readlines()
    release_ids = [rel_id.rstrip("\n") for rel_id in release_ids]

    last_request_time = time.time()  # needed for first iteration

    # get the release ids of all covers that are already saved (to skip when script restarted)
    covers_500 = [f.split(".")[0] for f in os.listdir("/Volumes/Data/covers/covers/500")]
    covers_1200 = [f.split(".")[0] for f in os.listdir("/Volumes/Data/covers/covers/1200")]
    base_covers = [f.split(".")[0] for f in os.listdir("/Volumes/Data/covers/covers/image")]
    large_covers = [f.split(".")[0] for f in os.listdir("/Volumes/Data/covers/covers/large")]
    # list of release ids that 404'd or 403'd when requested
    with open("temp/black_list.txt", "r") as f:
        black_list = f.readlines()
    black_list = [f.strip() for f in black_list]

    # not sure if needed, but header with contact information
    headers = {
        "User-Agent": "CulturalAnalyticsResearchCrawler/1.0 (nico.benz@studserv.uni-leipzig.de)"
    }
    for rel_id in tqdm(release_ids, bar_format="{percentage:.2f}%|{bar}{r_bar}"):
        # pass if cover already present in any resolution or not available
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
                                # go through resolution priority: 500, 1200, large (which is between 400 and 1000)
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
                                    # try accessing download path, if any
                                    try:
                                        response = requests.get(download_url, headers=headers, timeout=15)
                                        if response.status_code == 200:
                                            image_path = f"/Volumes/Data/covers/covers/{save_path}/{rel_id}.jpg"
                                            with open(image_path, 'wb') as f:
                                                f.write(response.content)
                                            # leave loop after first found cover has been saved
                                            break
                                    except requests.exceptions.Timeout as timeout:
                                        logging.error(f"Error {timeout}. Trying again in two minutes.")
                                        time.sleep(120)  # zzzZZZzzz for 2 min if request timed out
                                    except requests.exceptions.HTTPError as httperror:
                                        logging.error(f"Error {httperror}. Trying again now.")
                                    except requests.exceptions.RequestException as reqex:
                                        logging.error(f"Error {reqex}. Trying again now.")
                            else:
                                # if no cover could be found, put release id on blacklist to skip on next startup
                                with open("temp/black_list.txt", "a") as f:
                                    f.write(f"{rel_id}\n")
                    # 503 means api limit exceeded
                    elif response.status_code == 503:
                        logging.error("Limit exceeded. Trying again in two minutes.")
                        time.sleep(120)
                    # 404 (and 403 as well?) means no cover for that release id
                    elif response.status_code == 404 or response.status_code == 403:
                        keep_trying = False
                        # put release id on blacklist if 404 or 403
                        with open("temp/black_list.txt", "a") as f:
                            f.write(f"{rel_id}\n")
                except requests.exceptions.Timeout as timeout:
                    logging.error(f"Error {timeout}. Trying again in two minutes.")
                    time.sleep(120)
                except requests.exceptions.HTTPError as httperror:
                    logging.error(f"Error {httperror}. Trying again now.")
                except requests.exceptions.RequestException as reqex:
                    logging.error(f"Error {reqex}. Trying again now.")


# logging for debug
logging.basicConfig(
    filename="temp/progress.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

get_covers("data/cover_ids.txt", clear_log=True)
