import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm


def get_genre_info(subgenre_ids: list):
    """
    looks up a genre_id in music-brains and extracts relevant genre information
    :param subgenre_ids: list of tuples containing genre id and genre name
    :return: no return
    """
    url_template = "https://musicbrainz.org/genre/"
    genre_collection = {}
    for subgenre_id in tqdm(subgenre_ids):
        url = url_template + subgenre_id[0]  # concat url and genre id
        response = requests.get(url)

        if response.status_code == 200:
            # parse html text
            soup = BeautifulSoup(response.content, parser="html.parser", features="lxml")
            # extract all tables to a list
            tables = soup.select('table[class="details"]')
            # check every found list
            for table in tables:
                # target table contains spans of class genrelink
                if "genrelink" in str(table):  # ugly, better change to check for classes
                    # prepare dict
                    genre_info = {
                        "genre": subgenre_id[0],
                        "name": subgenre_id[1],
                        "subgenre of": [],
                        "subgenres": [],
                        "has fusion genres": [],
                        "fusion of": [],
                        "influenced by": [],
                        "influenced genres": []
                    }
                    # the genre items are in tr tags
                    genre_items = table.select("tr")
                    for item in genre_items:
                        # entry type (subgenre of, subgenres, influenced by, ...) are in th tags
                        entry_type = item.select("th")
                        # always only one item in list
                        if entry_type[0].text:
                            # genres are in <a> tags with their genre id in href
                            genres = item.select('a[href]')
                            for genre in genres:
                                # remove leading /genre/
                                genre_id = genre.get("href").replace("/genre/", "")
                                info = {
                                    "title": genre.text,
                                    "id": genre_id
                                }
                                dict_name = entry_type[0].text[:-1]  # remove colon at the end of dict key
                                genre_info[dict_name].append(info)
                    genre_collection[subgenre_id[0]] = genre_info
    with open("data/genres.json", "w", encoding="utf-8") as file_out:
        json.dump(genre_collection, file_out)


genres_found = []
with open("data/artists.json") as f:
    for line in f:
        json_data = json.loads(line)
        genres_found.append(json_data)

ids = []
for genre_data in genres_found:
    for k, v in genre_data.items():
        for genre_dict in v["genres"]:
            name_and_id = (genre_dict["genre-id"], genre_dict["genre-name"])
            if name_and_id not in ids:
                ids.append(name_and_id)

get_genre_info(ids)
