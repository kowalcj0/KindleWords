wort
===========

Get definitions for multiple English words at once.
Simply enter a list of comma-separated words and hit the "Get Definitions"
button.

Dictionary sources:
* [WordNet](https://wordnet.princeton.edu/download/current-version) [3.1](http://wordnetcode.princeton.edu/wn3.1.dict.tar.gz)
* Spelling (in IPA notation) [English Spelling DictData](https://play.google.com/store/apps/details?id=colordict.dictdata.cmuaes)
* example sentences come from [Tatoeba](https://tatoeba.org/eng/downloads)
    project
* Thesaurus comes from [WordNet 3.0](https://play.google.com/store/apps/details?id=colordict.dictdata.dictionary.english.wordnet3&hl=en)

Tested with Python 3.8.0a3


# Stats

There are:

* 146625 unique words in the DB
* 206353 word definitions as many words have multiple meanings
* out of all unique words 57275 spellings in
    [IPA](https://en.wikipedia.org/wiki/International_Phonetic_Alphabet)
    notation 
* 608632 example English sentences
* approx 20000 expressions in the thesaurus

# Benchmarks
------------

Searching for [20k](https://github.com/first20hours/google-10000-english/blob/master/20k.txt)
 most common English words as determined by n-gram frequency analysis of the 
Google's Trillion Word Corpus, takes around 0.0158s.
Out of those words only 542 definitions weren't found.

Searching for random unordered 1000 words takes around: 0.000804s


# TODO

* generate Anki flash-cards
* get word definitions directly from a CSV file


# Docker
--------

## Build image

```bash
    docker build -t wort:latest .
```

## Run the container

```bash
    docker run --rm --name web wort run.py
```

## Run the app by mounting local host src dir
```bash
    docker run -d -p 5000:5000 --name web --rm -v ~/git/wort:/app wort /app/run.py
```

## Get the logs

```bash
    docker logs web -f
```

