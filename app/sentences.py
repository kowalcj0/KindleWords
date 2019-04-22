# -*- coding: utf-8 -*-
import json
import random
import time
from pprint import pformat


def word_idx():
    start = time.time()
    ignored = set(
        [
            "",
            "+",
            "-",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "$1",
            "a",
            "about",
            "ago",
            "all",
            "also",
            "am",
            "an",
            "and",
            "any",
            "are",
            "aren't",
            "as",
            "at",
            "b",
            "back",
            "be",
            "been",
            "before",
            "better",
            "but",
            "by",
            "c",
            "can",
            "can't",
            "car",
            "cat",
            "comes",
            "couldn't",
            "d",
            "dan",
            "did",
            "didn't",
            "do",
            "does",
            "doesn't",
            "don't",
            "e",
            "else",
            "f",
            "few",
            "first",
            "for",
            "from",
            "g",
            "gave",
            "get",
            "give",
            "go",
            "going",
            "good",
            "got",
            "h",
            "had",
            "has",
            "hasn't",
            "have",
            "haven't",
            "he",
            "he'd",
            "he'll",
            "he's",
            "her",
            "here",
            "him",
            "his",
            "how",
            "i",
            "i'd",
            "i'll",
            "i'm",
            "i've",
            "if",
            "in",
            "into",
            "is",
            "isn't",
            "it",
            "it'll",
            "it's",
            "its",
            "j",
            "just",
            "k",
            "know",
            "knows",
            "l",
            "let",
            "let's",
            "like",
            "lot",
            "m",
            "make",
            "makes",
            "man",
            "many",
            "mary",
            "mary's",
            "me",
            "men",
            "mr",
            "must",
            "my",
            "n",
            "need",
            "new",
            "no",
            "not",
            "now",
            "o",
            "of",
            "off",
            "ok",
            "on",
            "one",
            "or",
            "our",
            "out",
            "own",
            "p",
            "pm",
            "q",
            "r",
            "re",
            "reason",
            "s",
            "see",
            "seem",
            "seen",
            "she",
            "she'd",
            "she'll",
            "she's",
            "should",
            "shouldn't",
            "so",
            "such",
            "t",
            "taking",
            "talk",
            "tell",
            "ten",
            "than",
            "thank",
            "that",
            "that's",
            "the",
            "their",
            "them",
            "then",
            "there",
            "they",
            "they're",
            "there's",
            "think",
            "this",
            "three",
            "time",
            "to",
            "tom",
            "tom's",
            "too",
            "two",
            "u",
            "up",
            "us",
            "use",
            "v",
            "very",
            "w",
            "want",
            "was",
            "wasn't",
            "we",
            "we'll",
            "we're",
            "we've",
            "well",
            "went",
            "were",
            "what",
            "what's",
            "when",
            "where",
            "who",
            "whole",
            "why",
            "will",
            "with",
            "won't",
            "work",
            "would",
            "wouldn't",
            "x",
            "y",
            "you",
            "you'd",
            "you'll",
            "you're",
            "you've",
            "your",
            "z",
        ]
    )
    with open("./static/eng_sentences.txt", "r", newline="\n") as f:
        res = {}
        for i, line in enumerate(f):
            words = line.split(" ")
            words = [w.strip().lower() for w in words]
            words = [w.replace("\n", "") for w in words]
            words = [w.replace('"', "") for w in words]
            words = [w.replace(".", "") for w in words]
            words = [w.replace(",", "") for w in words]
            words = [w.replace("!", "") for w in words]
            words = [w.replace("?", "") for w in words]
            words = [w.replace(":", "") for w in words]
            words = [w.replace(";", "") for w in words]
            words = [w.replace(")", "") for w in words]
            words = [w.replace("(", "") for w in words]
            words = [w.replace("]", "") for w in words]
            words = [w.replace("[", "") for w in words]
            words = [w.replace("*", "") for w in words]
            words = [w.replace("--", "-") for w in words]
            tmp = []
            for w in words:
                if w.startswith("'"):
                    w = w[1:]
                if w.endswith("'"):
                    w = w[:-1]
                tmp.append(w)
            words = tmp
            words = list(set(words) - ignored)
            for w in words:
                if w in res:
                    res[w].append(i)
                else:
                    res[w] = [i]
    end = time.time()
    print("Building the list of frequencies took: {}".format(end - start))
    max_key = [(w, len(res[w])) for w in res if len(res[w]) > 999]
    max_key = sorted(max_key, key=lambda x: x[1])
    print("The longest list is \n{}".format(pformat(max_key)))
    return res


def get_line_numbers(idx, words, max_sentences=2):
    res = {}
    start = time.time()
    for word in words:
        sentence_indexes = idx.get(word, None)
        if sentence_indexes:
            indexes = set()
            if len(sentence_indexes) > max_sentences:
                while len(indexes) < max_sentences:
                    indexes.add(random.choice(sentence_indexes))
            else:
                indexes = sentence_indexes
            res[word] = indexes
    end = time.time()
    print(
        "Getting a list of example sentence line numbers took: {}".format(end - start)
    )
    return res


def get_sentences(word_lines):
    result = {}
    start = time.time()
    with open("./app/static/eng_sentences.txt", "r", newline="\n") as file:
        sentences = file.readlines()
        for word in word_lines:
            lines = word_lines[word]
            for line in lines:
                if word in result:
                    result[word].append(sentences[line].replace("\n", ""))
                else:
                    result[word] = []
                    result[word].append(sentences[line].replace("\n", ""))
    end = time.time()
    print("Getting sentences from the file took: {}".format(end - start))
    return result


def save_idx(idx):
    start = time.time()
    with open("./static/idx", "w") as f:
        json.dump(idx, f, sort_keys=True)
    end = time.time()
    print("Saving idx to a file took: {}".format(end - start))


def load_idx():
    start = time.time()
    with open("./app/static/idx", "r") as f:
        res = json.load(f)
        end = time.time()
        print("Loading idx from a file took: {}".format(end - start))
        return res


if __name__ == "__main__":
    idx = word_idx()
    save_idx(idx)
