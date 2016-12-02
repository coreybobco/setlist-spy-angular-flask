#Portfolio

## Markov Mutagen
Combine online documents pulled from Project Gutenberg & Archive.org and run them through a Markov chain based text generator.

## Setlist Spy
Find every track a DJ has ever played. This app pulls info from [MixesDB](http://www.mixesdb.com/).

## Dependencies
* Python 3.x, flask
### Markov Mutagen
* markovify, rdflib, internetarchive, capturer
* python Gutenberg API (requires the [git version](https://github.com/c-w/Gutenberg) and Berkeley database)
    - For Ubuntu-based systems, first `sudo apt-get install python3-bsddb3` for Berkeley database dependency
    - Clone or download repo: `git clone https://github.com/c-w/Gutenberg.git` and cd into directory
    - Copy over requirements.pip with requirements-py3.pip (on Linux, cp requirements-py3.pip requirements.pip)
    - To install Gutenberg API, sudo pip3 install .
* Archive.org API
    - sudo pip3 install internetarchive
### Setlist Spy
* requests, lxml

## Build & development

- Run `python3 server/update_cache.py` to seed the Project Gutenberg database (takes a couple hours).
* Run `python3 server/runserver.py` to start the Python backend.
* Run `grunt` for building and `grunt serve` for preview.

## Testing

Running `grunt test` will run the unit tests with karma.

## Issues

* Sometimes the Gutenberg database cache will stop working and require updating.
* To fix, remove the Gutenberg database files (saved in ~/gutenberg_data/ by default) and re-run `python3 server/update_cache.py` to re-seed the cache.
