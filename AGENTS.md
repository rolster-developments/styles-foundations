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

## Color palettes

`scss/foundations/colors.scss` is generated: never edit its values by hand.
`scripts/colors-scss.py`, run through `npm run colors:build`, writes the whole
file from the constants at its top and keeps only the six header lines of the
existing file, so bump the version and date there before running it.

- `APP` holds the eleven greys of the `--rls-app-color-*` scale for `light`,
  `dim` and `dark`, from `950` to `050`, written as literals.
- `THEMES` lists the eighteen palettes in file order. A palette whose value is
  a single hex is chromatic: the script derives its eleven steps in OKLCH from
  that base, which stays in the ramp as the step whose lightness is nearest
  (`LADDER`), scaling the chroma curve (`CHROMA`) so that step keeps the base
  chroma and clamping to sRGB by reducing chroma only. A palette whose value is
  a list of eleven hexes is achromatic and goes in verbatim; those sit on the
  lightness ladder of the `app` scale, not on `LADDER`.

To change a chromatic palette, change its base hex. To add one, add its tuple
to `THEMES` and the name to `$rolster-themes` and to the `rolster-border-token`
list in `scss/foundations/themes.scss`. `npm run colors:check` exits 1 when
`colors.scss` differs from what the script would write; run it before
committing a change to either file.

`LADDER` and `CHROMA` are the per-step means measured on the thirteen chromatic
palettes that existed before the OKLCH regeneration of 20/Nov/2026; they are
the shared shape of every ramp and should not change without regenerating all
of them.

## Testing local changes in a consumer (react-components)

Never symlink this folder into a consumer's `node_modules`. Vite rewrites the
`url('./Sora/SoraLight.woff2')` references in `fonts/*.scss` to the symlink's
real path, which lies outside the consumer's root, and serves them as
`/@fs/...` 403: the fonts never load. Install a packed copy instead, exactly
what npm would put there:

```
cd styles-foundations && npm run build
npm pack --pack-destination /tmp
rm -rf ../react-components/node_modules/@rolster/styles-foundations
mkdir -p ../react-components/node_modules/@rolster/styles-foundations
tar -xzf /tmp/rolster-styles-foundations-<version>.tgz \
  -C ../react-components/node_modules/@rolster/styles-foundations \
  --strip-components=1
```

The consumer compiles the SCSS from source and now serves fonts and icons from
inside its own root. Repeat the pack after each change you want to see, then
**restart the consumer's Vite**: it does not watch `node_modules`, and
`npm pack` stamps every file with a fixed 1985 mtime, so a reload alone keeps
serving the cached transform. `npm install` in the consumer restores the
published version.

## Icon font

`icons/` is outside this pipeline and keeps its own `.eot`, `.ttf`, `.woff`
and `.svg` binaries exported from the icon tool. Do not run them through the
fonts script.
