# Rolster Technology Colors SCSS
# v1.0.0
# @license MIT
# Author: Rolster Developers
# Created: 20/Nov/2026
# Updated: 20/Nov/2026

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'scss' / 'foundations' / 'colors.scss'

STEPS = [950, 900, 800, 700, 600, 500, 400, 300, 200, 100, 50]

LADDER = [
    0.271863, 0.392395, 0.443443, 0.511686, 0.597811, 0.676147,
    0.747710, 0.824965, 0.895499, 0.945721, 0.975624,
]

CHROMA = [
    0.424484, 0.607330, 0.726239, 0.867423, 0.994674, 1.000000,
    0.876628, 0.661196, 0.414569, 0.217046, 0.091128,
]

APP = {
    'light': [
        '#152132', '#1d293b', '#2c394c', '#404d61', '#5a6474', '#757d8a',
        '#9ba1ab', '#c3c7ce', '#e1e3e6', '#f8f8f8', '#ffffff',
    ],
    'dim': [
        '#ffffff', '#f8f8f8', '#e1e3e6', '#c3c7ce', '#9ba1ab', '#757d8a',
        '#5b697e', '#4c596e', '#414e62', '#354255', '#2f3c4f',
    ],
    'dark': [
        '#ffffff', '#f8f8f8', '#e1e3e6', '#c3c7ce', '#9ba1ab', '#757d8a',
        '#5a6474', '#404d61', '#2c394c', '#1d293b', '#152132',
    ],
}

THEMES = [
    ('standard', APP['light']),
    ('primary', '#4e73f8'),
    ('secondary', '#00cf99'),
    ('tertiary', '#ff3c0a'),
    ('success', '#07a287'),
    ('info', '#06b6f1'),
    ('warning', '#fca549'),
    ('danger', '#f43c3c'),
    ('berry', '#c026d3'),
    ('ross', '#ff4b6e'),
    ('hope', '#65a30d'),
    ('mountains', [
        '#1b231e', '#222b25', '#303b34', '#425047', '#54695c', '#6c8375',
        '#90a898', '#b8cdbf', '#d9e7de', '#f2fbf5', '#ffffff',
    ]),
    ('amaizing', '#eab308'),
    ('purple', '#5552d9'),
    ('amber', '#ef6f20'),
    ('smartness', '#b67959'),
    ('obsidian', [
        '#23201a', '#2d281e', '#3e372b', '#544b3b', '#6e624c', '#897b61',
        '#ae9f82', '#d2c5ae', '#eae2d3', '#fcf8ef', '#ffffff',
    ]),
    ('neutral', [
        '#1e1e31', '#26263c', '#35354e', '#494964', '#60607d', '#797a95',
        '#9d9eb7', '#c4c5d8', '#e1e2ee', '#f7f7ff', '#ffffff',
    ]),
]


def linear(channel: float) -> float:
    if channel <= 0.04045:
        return channel / 12.92

    return ((channel + 0.055) / 1.055) ** 2.4


def encoded(channel: float) -> float:
    if channel <= 0.0031308:
        return 12.92 * channel

    return 1.055 * channel ** (1 / 2.4) - 0.055


def to_oklch(color: str) -> tuple[float, float, float]:
    r, g, b = (linear(int(color[i:i + 2], 16) / 255) for i in (1, 3, 5))

    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)

    lightness = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    b = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s

    return lightness, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def to_rgb(lightness: float, chroma: float, hue: float) -> tuple[float, float, float]:
    a = chroma * math.cos(math.radians(hue))
    b = chroma * math.sin(math.radians(hue))

    l = (lightness + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (lightness - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (lightness - 0.0894841775 * a - 1.2914855480 * b) ** 3

    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def in_gamut(rgb: tuple[float, float, float]) -> bool:
    return all(-0.0005 <= channel <= 1.0005 for channel in rgb)


def to_hex(lightness: float, chroma: float, hue: float) -> str:
    if not in_gamut(to_rgb(lightness, chroma, hue)):
        low, high = 0.0, chroma

        for _ in range(30):
            middle = (low + high) / 2

            if in_gamut(to_rgb(lightness, middle, hue)):
                low = middle
            else:
                high = middle

        chroma = low

    rgb = (encoded(max(0.0, min(1.0, channel))) for channel in to_rgb(lightness, chroma, hue))

    return '#%02x%02x%02x' % tuple(max(0, min(255, round(channel * 255))) for channel in rgb)


def ramp(base: str) -> tuple[int, list[str]]:
    lightness, chroma, hue = to_oklch(base)
    anchor = min(range(len(STEPS)), key=lambda i: abs(LADDER[i] - lightness))

    colors = [
        base.lower() if i == anchor else to_hex(LADDER[i], chroma * CHROMA[i] / CHROMA[anchor], hue)
        for i in range(len(STEPS))
    ]

    return STEPS[anchor], colors


def app_block(mode: str, indent: str) -> list[str]:
    lines = []

    for step, color in zip(STEPS, APP[mode]):
        lines.append(f'{indent}--rls-app-color-{step:03d}: var(--rls-project-color-{step:03d}, {color});')
        lines.append('')

    return lines


def theme_block(name: str, colors: list[str]) -> list[str]:
    lines = ['  @include helpers.rolster-theme(', f"    '{name}',"]

    for i, color in enumerate(colors):
        lines.append(f'    {color}' + (',' if i < len(colors) - 1 else ''))

    lines += ['  );', '']

    return lines


def render(header: list[str]) -> str:
    lines = header + ['', "@use 'helpers' as helpers;", '', 'body {']
    lines += app_block('light', '  ')

    for name, source in THEMES:
        colors = source if isinstance(source, list) else ramp(source)[1]
        lines += theme_block(name, colors)

    for mode in ('dim', 'dark'):
        lines += [f"  &[app-theme='{mode}'] {{"]
        lines += app_block(mode, '    ')
        lines[-1:] = ['  }', '']

    lines[-1:] = ['}']

    return '\n'.join(lines) + '\n'


def main() -> None:
    header = TARGET.read_text().splitlines()[:6]
    content = render(header)

    for name, source in THEMES:
        if isinstance(source, str):
            anchor, _ = ramp(source)
            print(f'{name:<12}{source}  anchor {anchor}')

    if '--check' in sys.argv:
        if TARGET.read_text() != content:
            print(f'{TARGET.relative_to(ROOT)} is out of date')
            sys.exit(1)

        print(f'{TARGET.relative_to(ROOT)} is up to date')
        return

    TARGET.write_text(content)
    print(f'{TARGET.relative_to(ROOT)} written')


if __name__ == '__main__':
    main()
