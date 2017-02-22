import logging

import json
import sqlite3
from flask import render_template
from flask import redirect

from peewee import fn
from playhouse.shortcuts import model_to_dict

from app import app
from app.forms import WordsForm
from app.models.definition import db
from app.models.definition import words as words_tbl


def get_definitions(words):
    db.connect()
    rs = (words_tbl
          .select(words_tbl.word, words_tbl.pos, words_tbl.definition)
          .where(words_tbl.word << words))
    res = {}
    notfound = []
    for r in rs:
        if r.word not in res:
            res[r.word] = {}
            res[r.word]['origin'] = None
            res[r.word]['definitions'] = []
        res[r.word]['definitions'].append({'pos': r.pos, 'definition': r.definition})
    for w in words:
        if w not in res:
            notfound.append(w)
    return res, notfound


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
        missing_plurals = [w[:-1] for w in notfound if w.endswith('s')]
        plural_definitions, _ = get_definitions(missing_plurals)
        for p in plural_definitions:
            plural_definitions[p]['origin'] = '{}s'.format(p)
        found_plurals = ['{}s'.format(w) for w in plural_definitions]
        notfound = list(set(notfound) - set(found_plurals))
        words_w_defs = {**definitions, ** plural_definitions}
        app.logger.debug('Words: {}'.format(', '.join(words)))
        app.logger.debug('Not found: {}'.format(', '.join(notfound)))
        return render_template('definitions.html',
                               title='Definitions',
                               words=words_w_defs,
                               notfound=notfound)
    else:
        app.logger.debug('Empty words form')
        return redirect('/')
