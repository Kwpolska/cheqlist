#!/usr/bin/env python3
import os
import pathlib
import random
import sys
MARKERS = [('*', '*'), ('**', '**'), ('_', '_'), ('__', '__'), ('~~', '~~'), ('<u>', '</u>')]
CHECKMARKS = ['', '- ', '-', '*', '* ', '- [', '- [ ]', '- [ ] ', '- [x]', '* [X]', '* [*]', '- [-]', '[ ]', '[X] ', '[x]', '[X]', '[*]', '     [x]', '    [ ]  ', '           ']
base = pathlib.Path("/usr/share/dict")

if len(sys.argv) != 3:
    print("usage: randomDemo.py entries outfile.cheqlist")
    exit(2)

entries = int(sys.argv[1])
outfile = sys.argv[2]

dictionaries = random.sample(os.listdir(str(base)), 3)
WORDS = ['', ' ', '    ']
for dictionary in dictionaries:
    with open(str(base.joinpath(dictionary)), 'r', encoding='utf-8') as fh:
        WORDS += fh.read().split()

WORDS = list(set(WORDS))

print("initialized with {0} words, {1} markers, {2} checkmarks".format(
    len(WORDS), len(MARKERS), len(CHECKMARKS)))
print("dictionaries:", ", ".join(dictionaries))

with open(outfile, 'w', encoding='utf-8') as fh:
    for _e in range(entries):
        # Text: 1-10 random words
        text = ' '.join(random.sample(WORDS, random.randint(1, 10)))
        # Checkmark: 1 random
        checkmark = random.choice(CHECKMARKS)
        # 25% chance of doubling checkmark
        # 15% chance of adding one more checkmark
        if random.random() >= 0.75:
            checkmark += ' ' + checkmark
        elif random.random() >= 0.85:
            checkmark += ' ' + random.choice(CHECKMARKS)
        markers_count = random.randint(0, 6)
        start_markers = end_markers = ''
        for s, e in random.sample(MARKERS, markers_count):
            start_markers = s + start_markers
            end_markers += e

        fh.write(checkmark + start_markers + text + end_markers + '\n')

print("written {0} entries".format(entries))
