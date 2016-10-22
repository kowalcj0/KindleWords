from string import digits

def open_clippings(file_name):
    correct = set()
    with open(file_name, 'r') as clippings:
        for line in clippings:
            if line != '==========\r\n':
                if line.strip():
                    words = line.split()
                    if len(words) <= 2:
                        word = ' '.join(words)
                        no_specials = word.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`‘~-=_+/[] ·ˈˌ–—„\"“”"})
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
                            correct.add(no_end_qoutes)

    sort = sorted(correct)
    print(sort)
    print(len(sort))


if __name__ == '__main__':
    open_clippings('./clippings.txt')
