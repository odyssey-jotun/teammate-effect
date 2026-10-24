#!/usr/bin/env python3
"""Export the site images. Run from the repo root: python3 tools/images.py
Sources: the handout's Unsplash photos in ~/livia-impact-project/src/img (credits in
that folder's CREDITS.md) and a render of the handout's first page."""
import glob, os
from PIL import Image

SRC = os.path.expanduser("~/livia-impact-project/src/img")

def crop(im, ratio, fx=0.5, fy=0.5):
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio); x = int((w - nw) * fx); return im.crop((x, 0, x + nw, h))
    nh = int(w / ratio); y = int((h - nh) * fy); return im.crop((0, y, w, y + nh))

# Hero: girls in navy jerseys together on the bench, seen from behind (Unsplash ymVaGKsBQXM), 4:5.
# The cheering-team photo is on the handout cover, so the hero uses a different one.
im = crop(Image.open(f"{SRC}/habit4.jpg").convert("RGB"), 4 / 5, 0.22, 0.5)
for w in (480, 680, 800):
    im.resize((w, round(w * 5 / 4)), Image.LANCZOS).save(f"images/hero-team-{w}.webp", quality=72, method=6)

# Livia's section: the handout's first page
pg = sorted(glob.glob(os.environ.get("PAGE_GLOB", "/tmp/none")))
if pg:
    p = Image.open(pg[0]).convert("RGB")
    for w in (480, 760):
        p.resize((w, round(p.height * w / p.width)), Image.LANCZOS).save(f"images/handout-cover-{w}.webp", quality=78, method=6)
    print("handout", p.size)

# Huddle photo for the plan section (Unsplash g-dZ1h7nQ0E), 4:3
hud = crop(Image.open(f"{SRC}/intro.jpg").convert("RGB"), 4 / 3, 0.5, 0.5)
for w in (600, 900):
    hud.resize((w, round(w * 3 / 4)), Image.LANCZOS).save(f"images/huddle-{w}.webp", quality=74, method=6)
print("done")
