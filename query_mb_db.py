import json
from tqdm import tqdm
import time


def collect_by_release(line):
    item = json.loads(line)
    if len(item.get("artist-credit", [])) == 1:
        artist_dict = item["artist-credit"][0]["artist"]
        release_data = {
            "artist-id": artist_dict.get("id", None),
            "release-id": item.get("id", None),
            "release-title": item.get("title", None),
            "release-status": item.get("status", None),
            "release-group-id": item.get("release-group", {}).get("id", None),
            "release-group-date": item.get("release-group", {}).get("first-release-date", None),
            "front-cover-available": item.get("cover-art-archive", {}).get("front", False)
        }
        return release_data
    return False


def collect_by_artist(line):
    """
    item = json.loads(line)
    release_data = {
        "release-id": item.get("id", None),
        "release-title": item.get("title", None),
        "release-status": item.get("status", None),
        "release-group-id": item.get("release-group", {}).get("id", None),
        "release-group-date": item.get("release-group", {}).get("first-release-date", None),
        "front-cover-available": item.get("cover-art-archive", {}).get("front", False)
    }
    if item["artist-credit"]:
        if len(item["artist-credit"]) > 1:
            # exclude multiple artists for one album (?!)
            pass
        else:
            artist_dict = item["artist-credit"][0]["artist"]
            if artist_dict["id"] not in artist_collection:
                artist_data = {
                    "id": artist_dict.get("id", None),
                    "name": artist_dict.get("name", None),
                    "sort-name": artist_dict.get("sort-name", None),
                    "genres": [],
                    "releases": []
                }
                if artist_dict["genres"]:
                    for genre in artist_dict["genres"]:
                        genre_data = {
                            "genre-id": genre.get("id", None),
                            "genre-name": genre.get("name", None),
                            "genre-count": genre.get("count", 0)
                        }
                        artist_data["genres"].append(genre_data)
        return artist_data
"""


def query_json_file():
    start_time = time.time()

    db = "release"
    file_path = f'/Volumes/Data/covers/mb_db/{db}/mbdump/{db}'
    num_of_artists = 0

    json_length = 3714201  # value calculated by just incrementing a counter once
    data_collection = []
    with open(file_path, "r") as f:
        for line in tqdm(f, total=json_length):
            data = collect_by_release(line)
            if data:
                data_collection.append(data)

    with open("data/covers/releases.json", "w", encoding="utf-8") as f:
        for data in data_collection:
            json_data = json.dumps(data, ensure_ascii=False)
            f.write(json_data)
            f.write('\n')

    end_time = time.time()
    execution_time = end_time - start_time

    hours = int(execution_time // 3600)
    minutes = int((execution_time % 3600) // 60)
    seconds = int(execution_time % 60)

    print(f"Finished after: {hours:02}:{minutes:02}:{seconds:02}")


query_json_file()
