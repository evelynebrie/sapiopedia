#!/usr/bin/env python3
"""The engraved plates of the dream entries (data/dream_images.json), whole: downloads each original (Wellcome Collection IIIF,
fish from Wikimedia Commons / Biodiversity Heritage Library), crops to the edge of the picture (no page text, nothing of the
picture cut), tints it in the site's wine duotone and writes assets/dreams/<name>.webp.
Run:  python3 tools/dream_plates.py [download folder]"""
import io, os, sys, urllib.request
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "_pins_batch", "plates")
UA = {"User-Agent": "sapiopedia-plates/1.0"}
WELLCOME = "https://iiif.wellcomecollection.org/image/{}/full/1800,/0/default.jpg"
SRC = {"mouse": WELLCOME.format("V0020536"), "death": WELLCOME.format("V0041912EL"), "mort": WELLCOME.format("V0042118"),
       "wedding": WELLCOME.format("V0040575"), "ghost": WELLCOME.format("V0036040"), "mere": WELLCOME.format("V0038817"),
       "sang": WELLCOME.format("V0008385ER"),
       "fish": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Ichthyologie%3B_ou%2C_Histoire_naturelle_des_poissons_%28Plate_12%29_%287064397515%29.jpg/2000px-Ichthyologie%3B_ou%2C_Histoire_naturelle_des_poissons_%28Plate_12%29_%287064397515%29.jpg"}
# picture edges as fractions of the scan (left, top, right, bottom); None = the whole print
CROP = {"death": (92 / 600, 212 / 1018, 512 / 600, 748 / 1018),     # the woodcut frame, without the Latin verses above and below
        "mere": (40 / 600, 42 / 900, 560 / 600, 800 / 900),        # the plate with its signatures, without the title line
        "mouse": (60 / 600, 30 / 556, 530 / 600, 410 / 556),       # the vignette, without the column of text
        "wedding": (0, 0, 1, 398 / 460),                            # the scene, without the caption band
        "mort": None, "sang": None, "ghost": None, "fish": None}
STOPS = [(0.0, (74, 16, 32)), (0.55, (196, 128, 145)), (1.0, (249, 237, 234))]   # sampled from the first set of plates

def lut():
    out = []
    for c in range(3):
        for v in range(256):
            x = v / 255
            for (a, ca), (b, cb) in zip(STOPS, STOPS[1:]):
                if a <= x <= b: out.append(round(ca[c] + (cb[c] - ca[c]) * (x - a) / (b - a))); break
    return out

def fetch(name):
    os.makedirs(DL, exist_ok=True); p = os.path.join(DL, name + ".jpg")
    if not os.path.exists(p):
        with urllib.request.urlopen(urllib.request.Request(SRC[name], headers=UA), timeout=60) as r: open(p, "wb").write(r.read())
    return Image.open(p)

if __name__ == "__main__":
    L = lut()
    for name in SRC:
        im = fetch(name); W, H = im.size
        if CROP[name]: l, t, r, b = CROP[name]; im = im.crop((round(l * W), round(t * H), round(r * W), round(b * H)))
        g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)
        out = Image.merge("RGB", (g, g, g)).point(L)
        out.thumbnail((1600, 1600), Image.LANCZOS)
        out.save(os.path.join(ROOT, "assets", "dreams", name + ".webp"), "WEBP", quality=82, method=6)
        print(name, out.size)
