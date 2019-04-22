# -*- coding: utf-8 -*-
from collections import OrderedDict

from flask import jsonify

from app import SENTENCE_IDX, app
from app.search import get_definitions, get_plural_definitions, get_thesaurus
from app.sentences import get_line_numbers, get_sentences


def handle_thesaurus_req(request):
    if request.get_json():
        app.logger.debug("got some JSON {}".format(request.get_json()))
        json = request.get_json()
        words = json["words"]
        thesaurus, _ = get_thesaurus(words)
        return jsonify(thesaurus)
    else:
        app.logger.debug("api/thesaurus - Someone submitted an empty JSON request form")
        return jsonify({"thesaurus": []})


def handle_definitions_req(request):
    if request.get_json():
        app.logger.debug("got some JSON {}".format(request.get_json()))
        json = request.get_json()
        words = json["words"]
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
        return jsonify(
            {
                "definitions": [sortedres],
                "thesaurus": [thesaurus],
                "notfound": [notfound],
            }
        )
    else:
        app.logger.debug(
            "api/definitions - Someone submitted an empty JSON request form"
        )
        return jsonify({"definitions": []})
