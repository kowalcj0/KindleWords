# -*- coding: utf-8 -*-
import os
from collections import OrderedDict

from flask import redirect, render_template, request
from werkzeug.utils import secure_filename

from app import SENTENCE_IDX, app
from app.forms import ClippingsForm, WordsForm
from app.handlers import handle_definitions_req, handle_thesaurus_req
from app.search import get_definitions, get_plural_definitions, get_thesaurus
from app.sentences import get_line_numbers, get_sentences
from app.wort import Options, open_clippings


@app.route("/", methods=["GET"])
def index():
    words_form = WordsForm()
    clippings_form = ClippingsForm()
    return render_template(
        "index.html", title="Home", words_form=words_form, clippings_form=clippings_form
    )


@app.route("/api/thesaurus", methods=["POST"])
def api_thesaurus():
    return handle_thesaurus_req(request)


@app.route("/api/definitions", methods=["POST"])
def api_definitions():
    return handle_definitions_req(request)


@app.route("/definitions", methods=["POST"])
def definitions():
    form = WordsForm()
    if form.validate_on_submit():
        words = set(w.strip().lower() for w in form.words.data.split(","))

        definitions, notfound = get_definitions(words)
        thesaurus, _ = get_thesaurus(words)
        plural_definitions, notfound = get_plural_definitions(notfound)
        notfound = sorted(notfound)

        words_w_defs = {**definitions, **plural_definitions}

        sortedres = OrderedDict(sorted(words_w_defs.items(), key=lambda t: t[0]))

        app.logger.debug("Words: {}".format(", ".join(words)))
        app.logger.debug("Not found: {}".format(", ".join(notfound)))

        line_numbers = get_line_numbers(idx=SENTENCE_IDX, words=words, max_sentences=5)
        word_sentences = get_sentences(line_numbers)
        for word in word_sentences:
            if word in sortedres:
                sortedres[word]["sentences"] = word_sentences[word]
        return render_template(
            "definitions.html",
            title="Definitions",
            words=sortedres,
            thesaurus=thesaurus,
            notfound=notfound,
        )
    else:
        app.logger.debug("Someone submitted an empty words form")
        return redirect("/")


@app.route("/upload", methods=["POST"])
def upload_clippings():
    form = ClippingsForm()
    if form.validate_on_submit():
        f = form.clippings.data
        filename = secure_filename(f.filename)
        path = os.path.join(app.instance_path, "clippings", filename)
        f.save(path)
        app.logger.debug("Saving file ing: {}".format(path))
        options = Options(remove_specials=True)
        words = [w for w in open_clippings(path, options)]

        definitions, notfound = get_definitions(words)
        thesaurus, _ = get_thesaurus(words)
        plural_definitions, notfound = get_plural_definitions(notfound)
        notfound = sorted(notfound)

        words_w_defs = {**definitions, **plural_definitions}

        sortedres = OrderedDict(sorted(words_w_defs.items(), key=lambda t: t[0]))

        app.logger.debug("Words: {}".format(", ".join(words)))
        app.logger.debug("Not found: {}".format(", ".join(notfound)))

        line_numbers = get_line_numbers(idx=SENTENCE_IDX, words=words, max_sentences=5)
        word_sentences = get_sentences(line_numbers)
        for word in word_sentences:
            if word in sortedres:
                sortedres[word]["sentences"] = word_sentences[word]
        return render_template(
            "definitions.html",
            title="Clippings Definitions",
            words=sortedres,
            thesaurus=thesaurus,
            notfound=notfound,
        )

    return redirect("/")
