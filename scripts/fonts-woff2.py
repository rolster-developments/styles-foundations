# Rolster Technology Fonts WOFF2
# v1.0.0
# @license MIT
# Author: Rolster Developers
# Created: 05/Nov/2026
# Updated: 05/Nov/2026

import logging
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'fonts-source'
TARGET = ROOT / 'fonts'
EXTENSIONS = {'.ttf', '.otf', '.woff', '.woff2'}

LATIN = [
    'U+0000-00FF', 'U+0131', 'U+0152-0153', 'U+02BB-02BC', 'U+02C6',
    'U+02DA', 'U+02DC', 'U+0304', 'U+0308', 'U+0329', 'U+2000-206F',
    'U+20AC', 'U+2074', 'U+2122', 'U+2191', 'U+2193', 'U+2212', 'U+2215',
    'U+FEFF', 'U+FFFD',
]

LATIN_EXT = [
    'U+0100-02BA', 'U+02BD-02C5', 'U+02C7-02CC', 'U+02CE-02D7',
    'U+02DD-02FF', 'U+1E00-1E9F', 'U+1EF2-1EFF', 'U+2020', 'U+20A0-20AB',
    'U+20AD-20C0', 'U+2113', 'U+2C60-2C7F', 'U+A720-A7FF',
]

UNICODES = subset.parse_unicodes(','.join(LATIN + LATIN_EXT))


def convert(source: Path, target: Path) -> int:
    font = TTFont(source)

    options = subset.Options()
    options.flavor = 'woff2'
    options.layout_features = ['*']
    options.name_IDs = ['*']
    options.notdef_outline = True

    subsetter = subset.Subsetter(options)
    subsetter.populate(unicodes=UNICODES)
    subsetter.subset(font)

    target.parent.mkdir(parents=True, exist_ok=True)
    font.flavor = 'woff2'
    font.save(target)

    return target.stat().st_size


def main() -> None:
    logging.getLogger('fontTools').setLevel(logging.ERROR)

    total_source = 0
    total_target = 0

    for family in sorted(path for path in SOURCE.iterdir() if path.is_dir()):
        family_source = 0
        family_target = 0

        for source in sorted(family.iterdir()):
            if source.suffix.lower() not in EXTENSIONS:
                continue

            target = TARGET / family.name / f'{source.stem}.woff2'

            family_source += source.stat().st_size
            family_target += convert(source, target)

        total_source += family_source
        total_target += family_target

        print(f'{family.name:<18}{family_source / 1024:>8.0f} KB ->{family_target / 1024:>7.0f} KB')

    print(f'{"total":<18}{total_source / 1024:>8.0f} KB ->{total_target / 1024:>7.0f} KB')


if __name__ == '__main__':
    main()
