from string import digits
import enchant
from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    """
    Will groupd lines in an opened file into chunks of n lines.
    SRC: http://stackoverflow.com/a/5845141
    """
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def open_clippings(filename):
    correct = set()
    N = 5
    with open(filename, 'r') as infile:
        clippings = set()
        for lines in grouper(infile, N, ''):
            assert len(lines) == N
            clippings.add(lines[3].strip().lower())
        for line in clippings:
            if len(line.split()) <= 2:
                no_specials = line.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`‘~-=_+/[] ·ˈˌ–—„\"“”"})
                if no_specials.strip():
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


if __name__ == '__main__':
    open_clippings('./clippings.txt')
