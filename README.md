#Portfolio

## Markov Mutagen
Combine online documents pulled from Project Gutenberg & Archive.org and run them through a Markov chain based text generator.

## Setlist Spy
Find every track a DJ has ever played. This app pulls info from [MixesDB](http://www.mixesdb.com/).

## Build & development
* Run `npm install` and `bower install` to install the Angular/frontend dependencies.
* Run `pip3 install` to install the Flask/Python3.x dependencies
* Run `python3 server/runserver.py` to start the Python backend.
* Run `grunt` for building and `grunt serve` to run.

## Testing

Running `grunt test` will run the unit tests with karma.

## Issues

* Sometimes the Gutenberg database cache will stop working and require updating.
* To fix, remove the Gutenberg database files (saved in ~/gutenberg_data/ by default) and re-run `python3 server/update_cache.py` to re-seed the cache.
