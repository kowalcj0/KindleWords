KindleWords
===========

Extract words from Kindle's "My Clippings.txt" file, so that you can send them
to a dictionary

Tested with Python 3.5


# Docker
--------

## Build image

```bash
    docker build -t kindle-words:latest .
```

## Run the container

```bash
    docker run --rm --name web kindle-words run.py
```

## Run the app by mounting local host src dir
```bash
    docker run -d -p 5000:5000 --name web --rm -v ~/git/KindleWords:/app kindle-words /app/run.py
```

## Get the logs

```bash
    docker logs web -f
```
