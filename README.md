# CulturalAnalytics-CoverPredictions
(related repo: tba)
## What to expect in this repo
This repo contains the code for my term paper in the module Cultural Analytics of the MSc Digital Humanities at Leipzig University. Here I will explore classifier training using album covers for the classification of genres and subgenres in music. For my analysis I use album covers crawled from [MusicBrainz](https://musicbrainz.org) along with their meta data on artists, releases, genres and subgenres.

## Working title
tba
## TODO:
### Data collection and preparation
- [x] get list of all genres and subgenres from MusicBrainz
- [ ] extract information of artists, their releases and their genres
- [ ] get the ids of all releases listed on MusicBrainz
- [ ] use these ids to download all front covers
  - [ ] in 500x500
  - [ ] in 1200x1200
- [ ] map all genres to their respective subgenres
- [ ] check resolution of all scraped covers and decide on most useful resolution
- [ ] plot distribution of available covers among all (sub)genres
- [ ] decide on included subgenres based on that distribution (some smaller subgenres might not have enough data)
- [ ] sample (balanced) dataset with at least 20.000 (?!) covers for earch genre and 2000 (?) for each subgenre
### Processing and analysis
- [ ] study best practice of preprocessing of visual data
- [ ] train classifiers
- [ ] evaluate
- [ ] repeat
- [ ] ???
- [ ] profit
