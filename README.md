# CulturalAnalytics-CoverPredictions
(related repo: [MetadataPrediction](https://github.com/nicobenz/CulturalAnalytics-MetadataPredictions/tree/master))
## What to expect in this repo
This repo contains the code for my term paper in the module Cultural Analytics of the MSc Digital Humanities at Leipzig University. Here I will explore classifier training using album covers or alternatively text descriptions from BLIP for the classification of genres and subgenres in music. For my analysis I use album covers crawled from [MusicBrainz](https://musicbrainz.org) along with their meta data on artists, releases, genres and subgenres.

## Working title
tba

## Basic description and research questions
Most music genres can be divided in multiple subgenres that share different features among each other that make them belong to a common genre. However, these features are very fluid and not easily identified. 
In my project I want investigate, if machine learning algorithmns are capable of identifying statistical relations between album covers within the same subgenre and within their common genre. 
To find evidence for it, I will analyse the the confusion matrix of the classification result and argue that in addition to the number of true positives indicating a statistical relationship for a certain subgenre, the false positive rate between subgenres within a genre can be interpreted as genre specific features spaning the whole genre and therefore resulting in higher numbers of false positives within a genre.

## TODO:
### Data collection and preparation
- [x] get list of all genres and subgenres from MusicBrainz
- [x] extract information of artists, their releases and their genres
- [x] get the ids of all releases listed on MusicBrainz
- [x] use these ids to download all front covers
  - [x] in 500x500 (crawling currently in progress; finished eta end of January)
  - [ ] in 1200x1200
- [ ] map all genres to their respective subgenres
- [ ] check resolution of all scraped covers and decide on most useful resolution
- [ ] plot distribution of available covers among all (sub)genres
- [ ] decide on included subgenres based on that distribution (some smaller subgenres might not have enough data)
- [ ] sample (balanced) dataset with at least 20.000 (?!) covers for earch genre and 2000 (?) for each subgenre
- [ ] make sure all selected items also have metadata for the other project (using data of the same artists and albums results in optimal comparability)
### Processing and analysis
- [ ] study best practice of preprocessing of visual data
- [ ] train classifiers
- [ ] evaluate
- [ ] repeat
- [ ] ???
- [ ] profit
- [ ] visualise distance between subgenres or clustering of classes 
- possible approaches:
  - multidimensional scaling
  - t-distributed stochastic neighbor embedding
  - network graphs using Three.js (or some other fancy interactive 3D visualization framework)
