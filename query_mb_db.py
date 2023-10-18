import json
from icecream import ic


def read_chunked_file(path, num_artists=0, chunk_size=4096):
    artists = []
    collector = ""
    with open(path, 'r') as f:
        while True:
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


db = "artist"
file_path = f'/Volumes/Data/covers/mb_db/{db}/mbdump/{db}'
num_of_artists = 100

items = read_chunked_file(file_path, num_of_artists)
for item in items:
    if item["genres"]:
        ic(item)
