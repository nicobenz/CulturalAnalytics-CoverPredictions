import json
from icecream import ic
import os
from tqdm import tqdm

def read_chunked_file(path, num_artists=0, chunk_size=4096):
    filesize = os.path.getsize(path)
    num_chunks = filesize // chunk_size
    artists = []
    collector = ""
    count = 1
    with open(path, 'r') as f:
        while True:
            print(f"\rLoop Progress: {count:08d}/{num_chunks}", end="")
            count += 1
            chunk = f.read(chunk_size)
            if not chunk:
                break  # end of file
            collector += chunk
            # find json objects in chunk
            json_objects = collector.split('\n')
            for json_obj in json_objects[:-1]:
                try:
                    artist_data = json.loads(json_obj)
                    artists.append(artist_data)
                    if 0 < num_artists == len(artists):
                        return artists  # return when specified number of artists reached
                except json.JSONDecodeError:
                    # continue if json object incomplete
                    pass
            # save incomplete json object for next iteration
            collector = json_objects[-1]

    return artists  # will not stop till end of file when num_artists == 0


db = "release"
file_path = f'/Volumes/Data/covers/mb_db/{db}/mbdump/{db}'
num_of_artists = 0

items = read_chunked_file(file_path, num_artists=num_of_artists)
print("")
artist_collection = {}
for idx, item in enumerate(items):
    release_data = {
        "release-id": item["id"],
        "release-title": item["title"],
        "release-status": item["status"],
        "release-group-id": item["release-group"]["id"],
        "release-group-date": item["release-group"]["first-release-date"],
        "front-cover-available": item["cover-art-archive"]["front"]
    }
    if item["artist-credit"]:
        if len(item["artist-credit"]) > 1:
            # exclude multiple artists for one album (?!)
            pass
        else:
            artist_dict = item["artist-credit"][0]["artist"]
            if artist_dict["id"] not in artist_collection:
                artist_data = {
                    "id": artist_dict["id"],
                    "name": artist_dict["name"],
                    "sort-name": artist_dict["sort-name"],
                    "genres": [],
                    "releases": []
                }
                if artist_dict["genres"]:
                    for genre in artist_dict["genres"]:
                        genre_data = {
                            "genre-id": genre["id"],
                            "genre-name": genre["name"],
                            "genre-count": genre["count"]
                        }
                        artist_data["genres"].append(genre_data)
                artist_collection[artist_dict["id"]] = artist_data
            artist_collection[artist_dict["id"]]["releases"].append(release_data)

with open("data/covers/artists.json", "w", encoding="utf-8") as f:
    json.dump(artist_collection, f)
