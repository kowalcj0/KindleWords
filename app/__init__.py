# -*- coding: utf-8 -*-
import time
import sqlite3

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOADED_CLIPPINGS_DEST'] = '/var/uploads'

def load_into_dict_sqlite():
    res = {}
    start = time.time()
    conn = sqlite3.connect('./app/static/wn31-slim3.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rs = c.execute('''SELECT word, pos, ipa, definition
                      FROM words
                      ORDER BY word''')
    for r in rs:
        if r['word'] not in res:
            res[r['word']] = {}
            res[r['word']]['ipa'] = None
            res[r['word']]['origin'] = None
            res[r['word']]['definitions'] = []
        if not res[r['word']]['ipa']:
            res[r['word']]['ipa'] = r['ipa']
        res[r['word']]['definitions'].append({'pos': r['pos'], 'definition': r['definition']})
    end = time.time()
    conn.close()
    print('Successfully loaded {} word definitions from SQLite DB into Dict in: {}'.format(len(res), end - start))
    return res


def load_thesaurus_into_dict_sqlite():
    res = {}
    start = time.time()
    conn = sqlite3.connect('./app/static/thesaurus.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    rs = c.execute('''SELECT word, pos, origin, thesaurus
                      FROM words
                      ORDER BY word''')
    for r in rs:
        if r['word'] not in res:
            res[r['word']] = {}
            res[r['word']]['pos'] = None
            res[r['word']]['origin'] = None
            res[r['word']]['thesaurus'] = []
        res[r['word']]['thesaurus'].append({'pos': r['pos'], 'origin': r['origin'], 'thesaurus': r['thesaurus']})
    end = time.time()
    conn.close()
    print('Successfully loaded {} thesaurus definitions from SQLite DB into Dict in: {}'.format(len(res), end - start))
    return res

MEMDB = load_into_dict_sqlite()
THESAURUSDB = load_thesaurus_into_dict_sqlite()

from app import sentences

SENTENCE_IDX = sentences.load_idx()

from app import views
