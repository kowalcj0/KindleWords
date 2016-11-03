from typing import NamedTuple
from string import digits
import enchant
from itertools import zip_longest
import sqlite3


Options = NamedTuple('Options', [('remove_specials', bool)])


def grouper(iterable, n, fillvalue=None):
    """
    Will group lines in an opened file into chunks of n lines.
    SRC: http://stackoverflow.com/a/5845141
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def remove_specials(line, options):
    """Will remove special characters from given string and strip it.

    :param line: string with special characters
    :type  line: str
    :return: a stripped string without the special characters
    :rtype: str
    """
    if options.remove_specials:
        specials = "!@#$%^&*()[]{};:,./<>?\|`‘~-=_+/[] ·ˈˌ–—„\"“”"
        line.translate({ord(c): " " for c in specials}).strip()
    return line


def open_clippings(filename, options):
    correct = set()
    N = 5
    with open(filename, 'r') as infile:
        clippings = set()
        for lines in grouper(infile, N, ''):
            assert len(lines) == N
            clippings.add(lines[3].strip().lower())
        for line in clippings:
            if len(line.split()) <= 2:
                no_specials = remove_specials(line, options)
                if no_specials:
                    no_eses = no_specials.replace('’s', '')
                    no_eses = no_eses.replace('\'s', '')
                    no_backticks = no_eses.replace('’', '\'')
                    no_end_qoutes = no_backticks.rstrip("'")
                    remove_digits = str.maketrans('', '', digits)
                    no_digits = no_end_qoutes.translate(remove_digits)
                    lower = no_digits.lower().strip()
                    no_end_qoutes = lower.rstrip("'")
                    no_end_qoutes = no_end_qoutes.replace('  ', ' ')
                    us = enchant.Dict("en_US")
                    gb = enchant.Dict("en_GB")
                    clean_words = no_end_qoutes.split()
                    is_us = all([us.check(w) for w in clean_words])
                    is_gb = all([gb.check(w) for w in clean_words])
                    if is_us or is_gb:
                        correct.add(no_end_qoutes)

    sort = sorted(correct)
    print(sort)
    print(len(sort))
    return sort

def transalate(words):
    conn = sqlite3.connect('android-08-08-primary.sqlite')
    c = conn.cursor()
    to_translate = words[-10:]
    for word in to_translate:
        t = (word,)
        query = ('SELECT e.entry, e.pronunciation_ipa, cb.content '
                 'FROM entries e '
                 'JOIN content_blocks cb '
                 'ON e.id = cb.entry_id '
                 'WHERE entry=?')
        res = c.execute(query, t)
        for row in res:
            print(row)
        #print('{} - {}'.format(word, str(dictionary.meaning(word))))

if __name__ == '__main__':
    options = Options(remove_specials=True)
    words = open_clippings('./clippings.txt', options)
    transalate(words)
