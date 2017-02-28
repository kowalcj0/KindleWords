# -*- coding: utf-8 -*-
import logging
import sqlite3
import time
from collections import OrderedDict

from flask import render_template
from flask import redirect

from app import app
from app import MEMDB
from app import THESAURUSDB
from app import SENTENCE_IDX
from app.forms import WordsForm
from app.sentences import get_line_numbers
from app.sentences import get_sentences


def get_definitions(words):
    res = {}
    notfound = []
    start = time.time()
    for w in words:
        if w in MEMDB:
            res[w] = MEMDB[w]
    end = time.time()
    app.logger.debug('In-memory search took: {}'.format(end - start))
    for w in words:
        if w not in res:
            notfound.append(w)
    return res, notfound


def get_thesaurus(words):
    res = {}
    notfound = []
    start = time.time()
    for w in words:
        if w in THESAURUSDB:
            res[w] = THESAURUSDB[w]
    end = time.time()
    app.logger.debug('In-memory thesaurus search took: {}'.format(end - start))
    for w in words:
        if w not in res:
            notfound.append(w)
    return res, notfound


def get_plural_definitions(words):
    missing_plurals = [w[:-1] for w in words if w.endswith('s')]
    plural_definitions, notfound = get_definitions(missing_plurals)

    for p in plural_definitions:
        plural_definitions[p]['origin'] = '{}s'.format(p)
    found_plurals = ['{}s'.format(w) for w in plural_definitions]
    notfound = list(set(notfound) - set(found_plurals))

    return plural_definitions, notfound


@app.route('/', methods=['GET'])
def index():
    form = WordsForm()
    return render_template('index.html',
                           title='Home',
                           form=form)


@app.route('/definitions', methods=['POST'])
def definitions():
    form = WordsForm()
    if form.validate_on_submit():
        words = set(w.strip().lower() for w in form.words.data.split(','))

        definitions, notfound = get_definitions(words)
        thesaurus, _ = get_thesaurus(words)
        plural_definitions, notfound = get_plural_definitions(notfound)
        notfound = sorted(notfound)

        words_w_defs = {**definitions, ** plural_definitions}

        sortedres = OrderedDict(sorted(words_w_defs.items(), key=lambda t: t[0]))

        app.logger.debug('Words: {}'.format(', '.join(words)))
        app.logger.debug('Not found: {}'.format(', '.join(notfound)))

        line_numbers = get_line_numbers(idx=SENTENCE_IDX, words=words, max_sentences=5)
        word_sentences = get_sentences(line_numbers)
        for word in word_sentences:
            if word in sortedres:
                sortedres[word]['sentences'] = word_sentences[word]
        return render_template('definitions.html',
                               title='Definitions',
                               words=sortedres,
                               thesaurus=thesaurus,
                               notfound=notfound)
    else:
        app.logger.debug('Someone submitted an empty words form')
        return redirect('/')
