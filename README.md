# CulturalAnalytics-CoverPredictions
(related repo: [MetadataPrediction](https://github.com/nicobenz/CulturalAnalytics-MetadataPredictions/tree/master))
## What to expect in this repo
This repo contains the code for my term paper in the module Cultural Analytics of the MSc Digital Humanities at Leipzig University. Here I will explore classifier training using album covers or alternatively text descriptions from BLIP for the classification of genres and subgenres in music. For my analysis I use album covers crawled from [MusicBrainz](https://musicbrainz.org) along with their meta data on artists, releases, genres and subgenres.

In the related repo (linked above) I pursue a similar project on musical metadata of the album cover data set. 
The results of both project are aimed to be comparable, giving insight on the same research question from two different perspectives. 

## Working title
Genre-Defining Features in Album Cover Art: Investigating Common Visual Motifs Across Musical Subgenres with BLIP-2 Captions and Machine Learning Classifiers

## Outline and research questions
In my research paper, I aim to explore the classification of musical subgenres through their album covers using machine learning algorithms. 
Music genres typically encompass various subgenres, each possessing unique yet subtly connected features that tie them to their overarching genre. 
However, these connecting features are often nuanced and challenging to pinpoint. 
My study will investigate whether machine learning algorithms can detect statistical patterns in album cover designs, both within individual subgenres and across their broader genre categories. 
A key method of analysis will be examining the confusion matrix from the classification results. 
I will argue that a significant number of true positives in the matrix may indicate a statistical relationship within a subgenre. 
More importantly, the rate of false positives, especially between subgenres of the same genre, could reveal genre-spanning features. 
For example, I anticipate a higher rate of false positives within subgenres of Metal compared to false positives between a Metal subgenre and a Hip Hop subgenre. 
This pattern, if observed, could suggest the presence of distinct, genre-specific characteristics in album cover designs.


## Possible challenges
- album covers are extremely diverse and artistic; lots of noise in the data is to be expected
- rate of false positives might not necessarily be an indicator for features connecting subgenres to a genre; there could be a bias in distribution of other factors between genres like release date or geographical origin
  
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
