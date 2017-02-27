import json
import random
import time
from collections import OrderedDict
from pprint import pformat


def word_idx():
    start = time.time()
    ignored = set(["a", "all", "am", "an", "and", "are", "as", "at", "b", "be",
        "been", "but", "by", "c", "can", "d", "did", "do", "e", "f", "first",
        "for", "from", "g", "get", "go", "h", "has", "have", "he", "he'd",
        "he's", "he'll", "his", "how", "i", "i'd", "i'll", "i'm", "if", "in",
        "is", "it", "its", "it's", "it'll", "j", "k", "l", "m", "me", "my",
        "n", "new", "no", "not", "o", "of", "ok", "on", "one", "or", "our", "p",
        "pm", "q", "r", "re", "s", "she", "she'd", "she'll", "she's", "so",
        "t", "than", "that", "the", "their", "they", "they're", "this", "to",
        "u", "up", "us", "v", "w", "was", "we", "were", "what", "which",
        "will", "with", "would", "x", "y", "you", "you'll", "your", "you're",
        "z"])
    with open('./static/en_sorted.txt', 'r', newline='\n') as f:
        res = {}
        for i, line in enumerate(f):
            words = line.split(' ')
            words = [w.replace('\n', '') for w in words]
            words = [w.replace('"', '') for w in words]
            words = [w.replace('.', '') for w in words]
            words = [w.replace(',', '') for w in words]
            words = [w.replace('!', '') for w in words]
            words = [w.replace('?', '') for w in words]
            words = [w.replace(':', '') for w in words]
            words = [w.replace(';', '') for w in words]
            words = [w.replace(')', '') for w in words]
            words = [w.replace('(', '') for w in words]
            words = [w.replace(']', '') for w in words]
            words = [w.replace('[', '') for w in words]
            words = [w.replace('*', '') for w in words]
            words = [w.replace('--', '-') for w in words]
            words = [w.strip().lower() for w in words]
            words = list(set(words) - ignored)
            for w in words:
                if w in res:
                    res[w].append(i)
                else:
                    res[w] = [i]
    end = time.time()
    print('Building the list of frequencies took: {}'.format(end - start))
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
    print('Getting a list of example sentence line numbers took: {}'.format(end - start))
    return res


def get_sentences(word_lines):
    res = {}
    start = time.time()
    with open('./app/static/en_sorted.txt', 'r', newline='\n') as f:
        sentences = f.readlines()
        for word in word_lines:
            lines = word_lines[word]
            for line in lines:
                if word in res:
                    res[word].append(sentences[line].replace('\n', ''))
                else:
                    res[word] = []
                    res[word].append(sentences[line].replace('\n', ''))
    end = time.time()
    print('Getting sentences from the file took: {}'.format(end - start))
    return res


def save_idx(idx):
    start = time.time()
    with open('./static/idx', 'w') as f:
        json.dump(idx, f)
    end = time.time()
    print('Saving idx to a file took: {}'.format(end - start))


def load_idx():
    start = time.time()
    with open('./app/static/idx', 'r') as f:
        res = json.load(f)
        end = time.time()
        print('Loading idx from a file took: {}'.format(end - start))
        return res


if __name__ == '__main__':
    idx = word_idx()
    save_idx(idx)
