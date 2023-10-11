import requests
from icecream import ic
from bs4 import BeautifulSoup
import json

url = "https://musicbrainz.org/tags?show_list=1"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

get_tag = soup.find('a', href='/tag/jazz')

extracted_tag = get_tag.text.replace(" ", "%20")

new_url = f"https://musicbrainz.org/tag/{extracted_tag}/artist?page=1"
new_response = requests.get(new_url)
new_soup = BeautifulSoup(new_response.content, 'html.parser')

artist_links = new_soup.select('a[href*="/artist/"]')

mbids = []
for link in artist_links:
    mbid = link['href'].replace("/artist/", "")
    mbids.append(mbid)

for mbid in mbids:
    url = f"https://musicbrainz.org/ws/2/artist/{mbid}?fmt=json&inc=releases"

    response = requests.get(url)

    result = json.loads(response.text)

    ic(result)
