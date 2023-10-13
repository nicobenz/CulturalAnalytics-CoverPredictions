import requests
from icecream import ic
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import quote


url = "https://musicbrainz.org/ws/2/genre/all?fmt=txt"
response = requests.get(url)

genres = response.text.split("\n")
print(genres)
data = {}
for genre in genres:
    url = f"https://musicbrainz.org/tag/{genre}/artist"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    page = 1
    artists = []
    while True:
        encoded_genre = quote(genre)

        url = f"https://musicbrainz.org/tag/{encoded_genre}/artist?page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            break
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
        if page != current_page:  # leave loop when current page does not increment any more
            break
        ic(page, current_page, genre)
        artist_links = soup.select('a[href*="/artist/"]')

        extracted_values = []
        for idx, link in enumerate(artist_links):
            title = link["title"].split("(")[0].strip()
            artists.append(title)

            mbid = link['href'].replace("/artist/", "")
            extracted_values.append((title, mbid))
        page += 1
    data[genre] = artists

    """
    query_strings = []
    for idx, artist_tuple in enumerate(extracted_values):
        if idx == 0:
            url = f"https://musicbrainz.org/ws/2/artist/{artist_tuple[1]}?fmt=json&inc=releases&limit=100"
            #url = f"https://musicbrainz.org/ws/2/release?artist={artist_tuple[1]}&fmt=json&limit=100&offset=1"
            response = requests.get(url)
    
            result = json.loads(response.text)
            for release in result["releases"]:
                if release["status"] != "Bootleg" and "demo" not in release["title"].lower():
                    album = release["title"]
                    query = artist_tuple[0].lower() + " " + album.lower()
                    query_strings.append(query)
    
    query_strings = list(set(query_strings))  # remove duplicates
    for string in query_strings:
        print(string)
    """