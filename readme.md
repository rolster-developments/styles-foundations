# Rolster Styles Foundations

Front-end style pack to develop responsive and mobile projects on the web with Rolster.

## Installation

```
npm i @rolster/styles-foundations
```

## Features

This package ships only CSS: there is no TypeScript API. It provides the design
tokens, the normalize layer, the layout utilities and the component styles that
`@rolster/react-components` and `@rolster/angular-components` render against.
Every entry point is available twice — as the compiled CSS under `dist/` and as
the Sass source under `scss/` — so a project can either import the stylesheet
or `@use` the source and reuse its mixins.

### Entry points

| Entry                                                | Sass source                              | Compiled CSS                      | Provides                                                                    |
| ---------------------------------------------------- | ---------------------------------------- | --------------------------------- | --------------------------------------------------------------------------- |
| `@rolster/styles-foundations`                        | `scss/styles.scss`                       | `dist/styles.css`                 | foundations (tokens, themes, responsives) and utilities (normalize, layout) |
| `@rolster/styles-foundations/components`             | `scss/components/index.scss`             | `dist/components.css`             | the structural styles of every atom, molecule and organism                  |
| `@rolster/styles-foundations/design-system-bordered` | `scss/design-system-bordered/index.scss` | `dist/design-system-bordered.css` | the bordered skin of the components                                         |
| `@rolster/styles-foundations/design-system-filled`   | `scss/design-system-filled/index.scss`   | `dist/design-system-filled.css`   | the filled skin of the components                                           |
| `@rolster/styles-foundations/design-system-gradient` | `scss/design-system-gradient/index.scss` | `dist/design-system-gradient.css` | the gradient skin of the components                                         |
| `@rolster/styles-foundations/scss/*`                 | any file under `scss/`                   | —                                 | direct access to a single partial, to reuse its mixins                      |

Each entry declares three conditions: `sass` resolves the `scss/` source,
while `style` and `default` resolve the compiled CSS. A Sass build therefore
gets the source and a JavaScript bundler gets the stylesheet, with the same
specifier:

```scss
// Sass: resolves scss/styles.scss and scss/components/index.scss
@use '@rolster/styles-foundations';
@use '@rolster/styles-foundations/components';
```

```typescript
// Bundler: resolves dist/styles.css and dist/components.css
import '@rolster/styles-foundations';
import '@rolster/styles-foundations/components';
```

The `./scss/*` passthrough exposes the whole source tree, so a project can
reach a single partial:

```scss
@use '@rolster/styles-foundations/scss/foundations/helpers' as helpers;
@use '@rolster/styles-foundations/scss/utilities/layout' as layout;
```

The bare specifier is resolved by the bundler (Vite, webpack `sass-loader`,
the Angular CLI). Running `sass` on its own does not resolve `node_modules`,
so there the same entries are reached with the `pkg:` scheme and the Node
package importer:

```
sass --pkg-importer=node styles.scss styles.css
```

```scss
@use 'pkg:@rolster/styles-foundations';
@use 'pkg:@rolster/styles-foundations/components';
```

The root entry is always required: the component and design system entries
consume the tokens it declares. Variants of the compiled output — the minified
`dist/*.min.css` and the right-to-left `dist/styles.rtl.css` — are published
but not listed in the exports map, so they must be referenced by their path
inside `node_modules`.

### Design systems

A design system is a skin over the component styles. Its whole stylesheet is
nested inside a wrapper class, so importing it changes nothing until that class
is present on an ancestor:

| Entry                      | Wrapper class                 |
| -------------------------- | ----------------------------- |
| `./design-system-bordered` | `.rls-design-system-bordered` |
| `./design-system-filled`   | `.rls-design-system-filled`   |
| `./design-system-gradient` | `.rls-design-system-gradient` |

`bordered` and `filled` are complete skins; `gradient` only restyles a subset
(avatar, button, button action, check box, progress bar, radio button, switch,
pagination, the day/month/year pickers and the clock picker), so it is meant to
be combined with one of the other two. Several design systems can be imported
at once and switched at runtime by toggling the class on `<body>`:

```scss
@use '@rolster/styles-foundations';
@use '@rolster/styles-foundations/components';
@use '@rolster/styles-foundations/design-system-bordered';
@use '@rolster/styles-foundations/design-system-filled';
```

```html
<body class="rls-design-system-filled">
  <div class="rls-app__body">...</div>
</body>
```

### Themes

`scss/foundations/colors.scss` declares seventeen palettes — `standard`,
`primary`, `secondary`, `tertiary`, `success`, `info`, `warning`, `danger`,
`berry`, `ross`, `hope`, `mountains`, `amaizing`, `purple`, `amber`,
`smartness` and `obsidian` — each one as `--rls-<palette>-color-050` through
`--rls-<palette>-color-950`, plus the derived gradients, backdrops, skeletons
and shadows.

`scss/foundations/themes.scss` turns one of those palettes into the **active
theme**: the `--rls-theme-*` variables every component reads. It applies
`primary` on `body` by default and re-maps the active theme for any element
carrying `rls-theme="<palette>"`, so a subtree can use a different palette
without touching the components:

```html
<body app-theme="dark">
  <button class="rls-button" rls-theme="danger">Delete</button>
</body>
```

The light and dark variants are the same palette mapped in opposite
directions: `rolster-theme-light` uses the low tokens as backgrounds and the
high ones as text, `rolster-theme-dark` does the reverse. The dark variant is
applied under `body[app-theme='dark']`, so the theme switch of an application
is a single attribute.

The application chrome is separate from the theme: `--rls-app-color-050` …
`--rls-app-color-950` follow `app-theme` on their own and each one falls back
to a `--rls-project-color-*` override, which is the supported way of rebranding
without forking the pack:

```scss
@use '@rolster/styles-foundations';

body {
  --rls-project-color-900: #12263f;
  --rls-project-color-050: #fbfbfd;
}
```

To build a theme from your own colors, declare a palette with the
`rolster-theme` mixin of `foundations/helpers` and map it with the mixins of
`foundations/themes`:

```scss
@use '@rolster/styles-foundations';
@use '@rolster/styles-foundations/scss/foundations/helpers' as helpers;
@use '@rolster/styles-foundations/scss/foundations/themes' as themes;

body {
  @include helpers.rolster-theme(
    'brand',
    #0b2446,
    #103a6a,
    #0c4380,
    #094e9b,
    #0a63bf,
    #1780e0,
    #409cf0,
    #82bdf7,
    #bddbfa,
    #ddebfc,
    #f0f7fe
  );

  @include themes.rolster-border-token('brand');
  @include themes.rolster-theme('brand');
  @include themes.rolster-theme-light('brand');
  @include themes.rolster-datatable-light('brand');

  &[app-theme='dark'] {
    @include themes.rolster-theme-dark('brand');
    @include themes.rolster-datatable-dark('brand');
  }
}
```

### Mixins

**`scss/foundations/helpers.scss`** — palette declaration; the only foundations
partial that emits no CSS of its own.

| Signature                                                                                            | Description                                                                          |
| ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `rolster-theme($theme, $c950, $c900, $c800, $c700, $c600, $c500, $c400, $c300, $c200, $c100, $c050)` | declares the eleven color steps of a palette and its nine `--rls-<theme>-gradient-*` |
| `rolster-theme-900($theme, $color)`                                                                  | sets `color-900` and derives `--rls-<theme>-backdrop-100` … `-900`                   |
| `rolster-theme-700($theme, $color)`                                                                  | sets `color-700` and derives `--rls-<theme>-skeleton-100` … `-500` (light surfaces)  |
| `rolster-theme-300($theme, $color)`                                                                  | sets `color-300` and derives `--rls-<theme>-skeleton-dark-100` … `-500` (dark)       |
| `rolster-theme-500($theme, $color)`                                                                  | sets `color-500` and derives `--rls-<theme>-shadow-color-500` and `-shadow-500`      |

**`scss/foundations/themes.scss`** — theme and border mapping.

| Signature                              | Description                                                                                  |
| -------------------------------------- | -------------------------------------------------------------------------------------------- |
| `rolster-theme($theme)`                | maps a palette onto the active theme: colors, shadow, backdrops and borders                  |
| `rolster-theme-light($theme)`          | maps the palette onto `--rls-theme-background/font-color/border/gradient/skeleton-*` (light) |
| `rolster-theme-dark($theme)`           | the same mapping inverted, for dark mode                                                     |
| `rolster-app-border($token)`           | builds `--rls-app-border-{1,2,4}-<token>` from `--rls-app-color-<token>`                     |
| `rolster-border-color($theme, $token)` | builds `--rls-<theme>-border-{1,2,4}-<token>` for one token of a palette                     |
| `rolster-border-token($theme)`         | applies `rolster-border-color` to the tokens `100` … `900` of a palette                      |
| `rolster-border-theme($theme, $token)` | maps a palette border onto the active `--rls-theme-border-{1,2,4}-<token>`                   |
| `rolster-datatable-light($theme)`      | datatable background, border and floating tokens of a palette, for light mode                |
| `rolster-datatable-dark($theme)`       | the same datatable tokens, for dark mode                                                     |

**`scss/foundations/flex-boxs.scss`**

| Signature           | Description                                                       |
| ------------------- | ----------------------------------------------------------------- |
| `flex_row($gap)`    | a row flexbox with `column-gap: $gap`; backs `.rls-flex-row-*`    |
| `flex_column($gap)` | a column flexbox with `row-gap: $gap`; backs `.rls-flex-column-*` |

**`scss/foundations/responsives.scss`**

| Signature           | Description                                                                            |
| ------------------- | -------------------------------------------------------------------------------------- |
| `responsive($size)` | emits the `.<size>-2-5` … `.<size>` width percentage classes for one breakpoint prefix |

It is applied as `rls-width-xs` (no query), `rls-width-sm` (≥ 361px),
`rls-width-md` (≥ 641px), `rls-width-lg` (≥ 961px) and `rls-width-xl`
(≥ 1241px).

**`scss/utilities/helpers.scss`** — spacing utilities.

| Signature                   | Description                                                             |
| --------------------------- | ----------------------------------------------------------------------- |
| `padding($size)`            | emits `.rls-pdg-{top,rgt,bot,lft,hrz,vrt}-<size>` and `.rls-pdg-<size>` |
| `padding-box-sizing($size)` | the same set as `.rls-pdx-*`, adding `box-sizing: border-box`           |
| `margin($size)`             | emits `.rls-mrg-{top,rgt,bot,lft,hrz,vrt}-<size>` and `.rls-mrg-<size>` |

All three are applied for the sizes `x4`, `x8`, `x12`, `x16`, `x24` and `x36`,
and read the value from the matching `--rls-sizing-<size>` token.

**`scss/utilities/layout.scss`** — responsive grid.

| Signature                | Description                                                                  |
| ------------------------ | ---------------------------------------------------------------------------- |
| `grid-base()`            | the shared grid container: `repeat(var(--rls-grid-columns), minmax(0, 1fr))` |
| `grid-responsive($size)` | emits the grid, column-count and span classes of one breakpoint prefix       |

It is applied for `xs` (no query), `sm` (≥ 420px), `md` (≥ 720px), `lg`
(≥ 1024px) and `xl` (≥ 1440px), producing `.rls-flex-<size>-grid-{8,12,16}`
(the container and its gap), `.rls-flex-<size>-grid-col-{12,8,6,4,2,1}` (the
column count) and `.rls-flex-<size>-col-1` … `-col-12` (the span of a child,
clamped to the column count of its container).

**`scss/utilities/typographics.scss`**

| Signature                  | Description                                                                      |
| -------------------------- | -------------------------------------------------------------------------------- |
| `typographic($name, $key)` | emits `.rls-<name>-font` and its weight variants from the `--rls-<key>-*` tokens |

It is applied to the eighteen scales `h1` … `h6`, `title`, `subtitle`, `body`,
`input`, `button`, `paragraph`, `label`, `span`, `smalltext`, `caption`,
`overline` and `tiny`. Each scale yields `.rls-<name>-font-default` (size,
letter spacing and line height), `.rls-<name>-font` (adding the default weight)
and the `-regular`, `-medium`, `-semibold`, `-bold`, `-extrabold` and `-black`
variants.

**`scss/components/organisms/data-table.scss`** — datatable cells; useful when
building a custom cell that must match the table.

| Signature                  | Description                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------- |
| `datatable_cell_vars()`    | the `--rlc-*` overrides that shrink fields, posters and buttons to cell size           |
| `datatable_cell_control()` | layout of a control cell: centered, fixed width and reduced avatar, image and switch   |
| `datatable_cell_styles()`  | the `--truncated`, `--control` and `--actions` cell modifiers and their inner elements |

```scss
@use '@rolster/styles-foundations/scss/utilities/layout' as layout;

.dashboard__panel {
  --rls-grid-columns: 3;

  @include layout.grid-base();
}
```

A Sass module is evaluated once per build, so `@use`-ing a partial that also
emits CSS does not duplicate it when the pack is already imported.

### CSS custom properties

Every token is a CSS custom property, which is what makes the pack themeable at
runtime. Two prefixes coexist: `--rls-*` are the design tokens declared by this
package, and `--rlc-*` are the per-component overrides a consumer sets to tweak
one instance (for example `--rlc-icon-dimension` or
`--rlc-app-header-height`).

| Family       | Declared in                     | Tokens                                                                                                                                                                            |
| ------------ | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Colors       | `foundations/colors.scss`       | `--rls-app-color-050…950` (overridable with `--rls-project-color-*`), `--rls-<theme>-color-050…950`, `-gradient-*`, `-backdrop-*`, `-skeleton-*`, `-skeleton-dark-*`, `-shadow-*` |
| Themes       | `foundations/themes.scss`       | the active `--rls-theme-color-*`, `-background-*`, `-font-color-*`, `-border-*`, `-gradient-*`, `-backdrop-*`, `-skeleton-*`, `-datatable-*`                                      |
| Borders      | `foundations/borders.scss`      | `--rls-app-border-{1,2,4}-transparent`, plus the `--rls-app-border-{1,2,4}-<token>` built by `rolster-app-border`                                                                 |
| Sizings      | `foundations/sizings.scss`      | `--rls-sizing-x1` … `--rls-sizing-x48`, `--rls-border-1/2/4` widths and the `--rls-sizing-safe-*` inset variables                                                                 |
| Elevations   | `foundations/elevations.scss`   | `--rls-z-index-1…32`, `--rls-app-shadow-1…6` and the directional `--rls-app-shadow-{bottom,top,left,right,center}-{2…32}`                                                         |
| Typographics | `foundations/typographics.scss` | `--rls-font-weight-thin…black`                                                                                                                                                    |
| Typographics | `utilities/typographics.scss`   | `--rls-<scale>-font-size`, `-letter-spacing`, `-line-height` and `-font-weight` for the eighteen scales                                                                           |
| Animations   | `foundations/animations.scss`   | `--rls-standard-curve`, `--rls-deceleration-curve`, `--rls-acceleration-curve`, `--rls-sharp-curve`                                                                               |

The root entry adds the variables that bound the application shell, which the
`.rls-app__*` layout reads to size itself:

```css
:root {
  --rls-html-max-width: 100%;
  --rls-html-max-height: 100%;
}
```

Set them to a fixed value to embed the application in a region instead of the
whole viewport.

### Responsive font size

Every measure in the pack is expressed in `rem`, and `html` takes its font size
from `--rls-app-font-size`, whose default is `2px`. Scaling that single token
scales the whole interface — sizings, typography and component dimensions
alike.

The root entry ships a ready-made scale under the `.rls-aspect-ratio` class,
which grows the base size on wide screens:

| Viewport | `--rls-app-font-size` |
| -------- | --------------------- |
| < 1360px | `2px`                 |
| ≥ 1360px | `2.5px`               |
| ≥ 1820px | `2.925px`             |

```html
<body class="rls-aspect-ratio">
  ...
</body>
```

### Assets

The package ships three font families and an icon font. They are published
under `fonts/` and `icons/` but are not listed in the exports map, so they are
referenced through their path inside `node_modules`:

| Asset                                    | Format                          | Declares                                       |
| ---------------------------------------- | ------------------------------- | ---------------------------------------------- |
| `fonts/mont/mont.scss`                   | `.otf`                          | `-rolster-system-font`, weights 100–900        |
| `fonts/poppins/poppins.scss`             | `.woff2`                        | `-rolster-system-font`, weights 100–900        |
| `fonts/space-grotesk/space-grotesk.scss` | `.woff`                         | `-rolster-system-font`, weights 100–900        |
| `icons/rolster-icons.scss`               | `.woff`, `.ttf`, `.eot`, `.svg` | `-rolster-icons` and 248 `.rls-icon-*` classes |

The three families declare the same `-rolster-system-font` family name, which
is the first entry of `--rls-app-font-family`, so importing one of them is what
picks the typeface of the application. Import exactly one:

```scss
@import '../node_modules/@rolster/styles-foundations/scss/styles';
@import '../node_modules/@rolster/styles-foundations/fonts/poppins/poppins';
@import '../node_modules/@rolster/styles-foundations/icons/rolster-icons';
```

An icon is rendered by applying its class to an element; the icon stylesheet
resolves the glyph through a `::before` pseudo-element:

```html
<div class="rls-icon">
  <i class="rls-icon-activity"></i>
</div>
```

The `.rls-icon` wrapper comes from the components entry and sizes the glyph
through `--rlc-icon-dimension`; the `.rls-icon-*` class alone is enough when no
wrapper is needed.

### Consumers

`@rolster/react-components` and `@rolster/angular-components` are built against
this pack: their markup uses these class names and their appearance is driven
entirely by these tokens. Installing one of them means installing this package
as well, and the application is responsible for importing the root entry, the
components entry, at least one design system, a font and the icon font.

## Contributing

- Daniel Andrés Castillo Pedroza :rocket:
