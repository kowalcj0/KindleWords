# -*- coding: utf-8 -*-
import time

from app import MEMDB, THESAURUSDB, app


def get_definitions(words):
    res = {}
    notfound = []
    start = time.time()
    for w in words:
        if w in MEMDB:
            res[w] = MEMDB[w]
    end = time.time()
    app.logger.debug("In-memory search took: {}".format(end - start))
    for w in words:
        if w not in res:
            notfound.append(w)
    return res, notfound


def get_plural_definitions(words):
    missing_plurals = [w[:-1] for w in words if w.endswith("s")]
    plural_definitions, notfound = get_definitions(missing_plurals)

    for p in plural_definitions:
        plural_definitions[p]["origin"] = "{}s".format(p)
    found_plurals = ["{}s".format(w) for w in plural_definitions]
    notfound = list(set(notfound) - set(found_plurals))

    return plural_definitions, notfound


def get_thesaurus(words, *, max_thesaurus_definitions=2):
    res = {}
    notfound = []
    start = time.time()
    for w in words:
        ctr = 0
        if ctr < max_thesaurus_definitions:
            if w in THESAURUSDB:
                res[w] = THESAURUSDB[w]
                ctr += 1
    end = time.time()
    app.logger.debug("In-memory thesaurus search took: {}".format(end - start))
    for w in words:
        if w not in res:
            notfound.append(w)
    return res, notfound
