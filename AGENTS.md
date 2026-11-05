# Agent guidelines

## Typographic fonts

`fonts/<Family>/` holds generated `.woff2` files only. They are never edited,
replaced or committed by hand: the binaries that ship are always the output of
`scripts/fonts-woff2.py`, run through `npm run fonts:build`.

The script reads `fonts-source/<Family>/` (the original binaries in `.ttf`,
`.otf`, `.woff` or `.woff2`, not published because the `files` list in
`package.json` leaves the folder out) and writes `fonts/<Family>/<Name>.woff2`
for each one, subset to the Latin and Latin Extended unicode ranges declared
in the script and compressed with Brotli. It needs `fonttools` and `brotli`
available to `python3`:

```
pip3 install fonttools brotli
npm run fonts:build
```

### Adding a family or a weight

1. Put the original binaries in `fonts-source/<Family>/`, one file per weight,
   named `<Family><Weight>` (`SoraSemibold.ttf`). Never put them in `fonts/`.
2. Run `npm run fonts:build`. It regenerates every family, so unrelated
   `.woff2` files may change by a few bytes; that is expected.
3. For a new family, add `fonts/<family-name>.scss` next to the existing ones:
   one `@font-face` per weight range pointing at `./<Family>/<Name>.woff2` with
   `format('woff2')`, `font-display: swap`, the `--rls-app-font-family`
   override and only the `--rls-<scale>-line-height` tokens that differ from
   the foundations defaults. Then add its row to the assets table of
   `readme.md`.
4. For a changed or added weight of an existing family, update the matching
   `@font-face` in `fonts/<family-name>.scss` and bump its header version and
   date.

### Changing the character coverage

The subset is the `LATIN` and `LATIN_EXT` lists in `scripts/fonts-woff2.py`.
Extending the coverage (Greek, Cyrillic, Vietnamese) means adding the ranges
there and regenerating with `npm run fonts:build`; the originals in
`fonts-source/` keep every glyph, so nothing is lost by regenerating. Never
subset a `.woff2` from `fonts/` again: it already lacks the glyphs outside the
current ranges.

## Icon font

`icons/` is outside this pipeline and keeps its own `.eot`, `.ttf`, `.woff`
and `.svg` binaries exported from the icon tool. Do not run them through the
fonts script.
