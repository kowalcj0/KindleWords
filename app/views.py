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
from app.models.definition import wordsXsensesXsynsets


def get_definitions(words):
    db.connect()
    #res = (wordsXsensesXsynsets
           #.select(wordsXsensesXsynsets.lemma, fn.GROUP_CONCAT(wordsXsensesXsynsets.definition, '\r')).alias('definition')
           #.where(wordsXsensesXsynsets.lemma << words)
           #.group_by(wordsXsensesXsynsets.lemma))
    rs = (wordsXsensesXsynsets
           .select(wordsXsensesXsynsets.lemma, wordsXsensesXsynsets.definition)
           .where(wordsXsensesXsynsets.lemma << words))
    res = {}
    for r in rs:
        if r.lemma not in res:
            res[r.lemma] = []
            res[r.lemma].append(r.definition)
        else:
            res[r.lemma].append(r.definition)

    #definitions = [{'word': r.lemma, 'definition': r.definition} for r in res]
    return res


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
        words = [w.strip().lower() for w in form.words.data.split(',')]
        definitions = get_definitions(words)
        return render_template('definitions.html',
                               title='Definitions',
                               definitions=definitions)
    else:
        app.logger.debug('Empty words form')
        return redirect('/')
