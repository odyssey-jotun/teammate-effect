# The Teammate Effect

Landing page for Livia McGraw's project on being a good teammate: six habits from peer-reviewed research, with a free printable handout for young athletes (`downloads/teammate-handout.pdf`).

"The Teammate Effect" is a working name.

## Live preview

https://odyssey-jotun.github.io/teammate-effect/

GitHub Pages serves `main` at root. The page is `noindex,nofollow` and `robots.txt` disallows all for now. To open it to search, set the robots meta in `build.py` to `index,follow,max-image-preview:large` and write `Allow: /` plus a `Sitemap:` line to `robots.txt`.

## Editing

`index.html`, `robots.txt`, `sitemap.xml` and `favicon.svg` are generated. Change copy in `build.py`, then run:

    python3 build.py

- Styles: `styles.css`, minified and inlined by the build.
- Images: `python3 tools/images.py` (photos come from the handout's Unsplash set; credits in the handout project's `src/img/CREDITS.md`).
- Fonts: Barlow Condensed 700 and Source Sans 3, self-hosted latin subsets from Google Fonts.

## Rules this page follows

- Every page is written in the first person ("I"). The name appears only in the "I'm Livia McGraw" introductions.
- StoryBrand order: hero, problem (three cited points: external, internal, philosophical), guide, three-step plan, the six habits, stakes, closing call to action.
- Every figure is cited in plain text. Zero external links. No em dashes.
