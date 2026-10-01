"""
Builds every derived web image for the MOEMODI site from the source files.

  products/studio/*.png  ->  products/*.webp   transparent cutouts
  (products/product-group-hero.png is the group photo, used as-is)
  logos/*-transparent    ->  logos/web/*.png   right-sized logo marks
  (cutouts + logo)       ->  social/*.jpg      1200x630 link-preview cards

The studio renders sit on a white sweep with a soft floor shadow. The cutout
removes the sweep with a strict border flood (the sweep is darkness 0-2; every
product outline jumps to 10+), then removes the floor shadow under the dark
contact line where each product meets the floor.

Run from the moemodi-dev repo root (needs Pillow, numpy, scipy):
    python assets/images/_build_web_images.py

Social cards use Georgia Pro / Segoe UI from C:/Windows/Fonts.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage as ndi

IMG = Path(__file__).resolve().parent
STUDIO = IMG / "products" / "studio"
FONTS = Path("C:/Windows/Fonts")

IVORY = (246, 244, 238)
GREEN = (31, 75, 58)
FOREST = (21, 58, 45)
GOLD = (200, 163, 90)

# Floor-shadow tuning, measured on the studio renders.
STEP = 4          # max darkness rise per pixel still treated as shadow
SHADOW_MAX = 48
CHROMA_MAX = 10
CONTACT = 70      # darkness of the line where a product meets the floor
CONTACT_ZONE = 90


# ----------------------------------------------------------------- cutouts --

def strict_bg(d):
    lab, _ = ndi.label(d <= 3)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    return np.isin(lab, border[border > 0])


def floor_shadow(d, chroma, bg):
    """Climb each column from the floor through gently darkening grey."""
    h, w = d.shape
    shadow = np.zeros_like(bg)
    for x in range(w):
        prev = 0
        for y in range(h - 1, -1, -1):
            if bg[y, x]:
                prev = int(d[y, x])
                continue
            v = int(d[y, x])
            if v <= SHADOW_MAX and chroma[y, x] <= CHROMA_MAX and v - prev <= STEP:
                shadow[y, x] = True
                prev = v
            else:
                break
    return shadow


def contact_points(d, bg):
    h, w = d.shape
    y1 = np.where((~bg).any(1))[0].max()
    y0 = y1 - CONTACT_ZONE
    yc = np.full(w, -1)
    for x in range(w):
        idx = np.where(d[y0:y1 + 1, x] >= CONTACT)[0]
        if len(idx):
            yc[x] = y0 + idx.max()
    have = yc >= 0
    if have.sum() > 15:
        yc[have] = ndi.median_filter(yc[have], size=15, mode="nearest")
    return yc


def single_mask(d, chroma):
    """One front-facing container: vertical sides meeting an elliptical base."""
    h, w = d.shape
    bg = strict_bg(d)
    yc = contact_points(d, bg)
    xs = np.where(yc >= 0)[0]
    top_contact = yc[xs].min()

    obj = ~bg
    band = obj[top_contact - 140: top_contact - 50]
    cols = np.where(band.any(0))[0]
    xl, xr = cols.min(), cols.max()

    # Near the base corners the shadow blends into shaded plastic with no edge
    # or colour change, so the base outline comes from the contact arc.
    coef = np.polyfit(xs, yc[xs], 2)
    xx = np.arange(w)
    arc = np.where(yc >= 0, yc, np.polyval(coef, xx)).astype(int)
    yy = np.arange(h)[:, None]
    obj &= ~(yy > arc[None, :] + 1)
    obj &= ~((yy > top_contact - 50) & ((xx[None, :] < xl) | (xx[None, :] > xr)))
    obj &= ~floor_shadow(d, chroma, ~obj)

    # A container only narrows towards its base.
    left, right = xl, xr
    for y in range(top_contact - 60, h):
        row = np.where(obj[y])[0]
        if not len(row):
            continue
        left, right = max(left, row.min()), min(right, row.max())
        obj[y, :left] = False
        obj[y, right + 1:] = False

    r = 22
    disk = np.hypot(*np.mgrid[-r:r + 1, -r:r + 1]) <= r
    zone = yy > top_contact - 80
    obj = np.where(zone, ndi.binary_opening(obj, structure=disk), obj)

    pale = zone & (d <= 12) & (chroma <= 3)
    lab, _ = ndi.label(pale | ~obj)
    outside = np.unique(lab[~obj & zone])
    obj &= ~(np.isin(lab, outside[outside > 0]) & pale)
    return obj


def cutout(path):
    rgb = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    h, w = rgb.shape[:2]
    d = 255 - rgb.min(2)
    chroma = rgb.max(2) - rgb.min(2)

    obj = ndi.binary_opening(single_mask(d, chroma), iterations=2)
    lab, n = ndi.label(obj)
    sizes = ndi.sum(obj, lab, range(1, n + 1))
    obj = ndi.binary_fill_holes(lab == 1 + int(np.argmax(sizes)))

    # Pull the edge in 1px to drop the white halo, then anti-alias.
    obj = ndi.binary_erosion(obj, iterations=1)
    a = ndi.gaussian_filter(obj.astype(np.float32), 0.8)
    a = np.clip((a - 0.15) / 0.85, 0, 1)

    ys, xs = np.where(a > 0.02)
    pad = 8
    y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad + 1, h)
    x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad + 1, w)
    rgba = np.dstack([rgb.astype(np.uint8), (a * 255).round().astype(np.uint8)])
    return Image.fromarray(rgba[y0:y1, x0:x1], "RGBA")


def fit(im, max_w, max_h):
    s = min(max_w / im.width, max_h / im.height, 1)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS) if s < 1 else im


def build_cutouts():
    out = {}
    for src in sorted(STUDIO.glob("*.png")):
        im = fit(cutout(src), 1400, 1100)
        im.save(IMG / "products" / f"{src.stem}.webp", "WEBP", quality=86, method=6)
        out[src.stem] = im
        print(f"products/{src.stem}.webp {im.size}")
    return out


# ------------------------------------------------------------------- logos --

def build_logos():
    web = IMG / "logos" / "web"
    web.mkdir(exist_ok=True)
    jobs = [
        ("moemodi-icon-transparent.png", "moemodi-icon-112.png", 112),
        ("moemodi-horizontal-logo-transparent.png", "moemodi-horizontal-logo-480.png", 480),
        ("moemodi-icon-watermark.png", "moemodi-icon-watermark-520.png", 520),
    ]
    for src, dst, width in jobs:
        im = Image.open(IMG / "logos" / src).convert("RGBA")
        im = im.crop(im.getbbox())
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(web / dst, optimize=True)
        print(f"logos/web/{dst} {im.size}")


# ------------------------------------------------------------ social cards --

def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def shadowed(canvas, im, xy, blur=18, offset=22, strength=0.28):
    a = im.getchannel("A").point(lambda v: int(v * strength))
    sh = Image.new("RGBA", im.size, FOREST + (0,))
    sh.putalpha(a)
    pad = blur * 3
    layer = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), FOREST + (0,))
    layer.alpha_composite(sh, (pad, pad))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(layer, (xy[0] - pad, xy[1] - pad + offset))
    canvas.alpha_composite(im, xy)


def base_card():
    card = Image.new("RGBA", (1200, 630), IVORY + (255,))
    tex = Image.open(IMG / "backgrounds" / "botanical-2.jpg").convert("RGB")
    tex = tex.resize((1200, round(tex.height * 1200 / tex.width)), Image.LANCZOS).crop((0, 0, 1200, 630))
    # Multiply the botanical texture at low strength, as the site hero does.
    t = np.asarray(tex).astype(np.float32) / 255
    c = np.asarray(card.convert("RGB")).astype(np.float32) / 255
    mixed = c * (1 - 0.35 + 0.35 * t)
    card = Image.fromarray((mixed * 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(card)
    d.rectangle((0, 618, 1200, 630), fill=GREEN)
    return card


def text_block(card, eyebrow, title_lines, sub, foot):
    d = ImageDraw.Draw(card)
    logo = Image.open(IMG / "logos" / "web" / "moemodi-horizontal-logo-480.png")
    logo = logo.resize((360, round(logo.height * 360 / logo.width)), Image.LANCZOS)
    card.alpha_composite(logo, (64, 56))
    y = 56 + logo.height + 40
    d.text((66, y), eyebrow.upper(), font=font("seguisb.ttf", 19), fill=GOLD)
    y += 38
    for i, line in enumerate(title_lines):
        f = font("GeorgiaPro-SemiBoldItalic.ttf" if i == len(title_lines) - 1 and len(title_lines) > 1
                 else "GeorgiaPro-SemiBold.ttf", 54)
        d.text((62, y), line, font=f, fill=GOLD if f.path.endswith("Italic.ttf") else GREEN)
        y += 64
    y += 12
    for line in sub:
        d.text((66, y), line, font=font("segoeui.ttf", 23), fill=(65, 85, 77))
        y += 32
    d.text((66, 556), foot, font=font("seguisb.ttf", 22), fill=GREEN)


def build_social(cut):
    out = IMG / "social"
    out.mkdir(exist_ok=True)

    card = base_card()
    text_block(card, "Natural skincare, made in South Africa",
               ["Botanical care,", "rooted in heritage."],
               ["Agave Herbal Lotion, Aloe Vera and", "Rosehip Petroleum Jelly."],
               "moemodi.co.za  ·  WhatsApp +27 72 212 1348")
    # The range on one shelf: jars either side of the bottle, 250ml outermost.
    lineup = [("rosehip-250ml", 135), ("aloe-vera-500ml", 182), ("agave-500ml", 300),
              ("rosehip-500ml", 182), ("aloe-vera-250ml", 135)]
    pieces = [fit(cut[k], 400, h) for k, h in lineup]
    overlap, floor, centre = 10, 515, 872
    x = centre - (sum(p.width for p in pieces) - overlap * (len(pieces) - 1)) // 2
    spots = []
    for p in pieces:
        spots.append(x)
        x += p.width - overlap
    for i in (0, 4, 1, 3, 2):  # back to front, bottle last
        shadowed(card, pieces[i], (spots[i], floor - pieces[i].height), blur=14, offset=14)
    card.convert("RGB").save(out / "og-moemodi.jpg", quality=88, optimize=True)

    products = [
        ("og-agave-herbal-lotion.jpg", "Agave · Lotion", ["Agave Herbal", "Lotion"],
         ["Light, fast-absorbing everyday", "lotion. 500ml."], ["agave-500ml"]),
        ("og-aloe-vera-petroleum-jelly.jpg", "Aloe Vera · Petroleum Jelly", ["Aloe Vera", "Petroleum Jelly"],
         ["The classic jelly with aloe vera.", "250ml and 500ml."], ["aloe-vera-250ml", "aloe-vera-500ml"]),
        ("og-rosehip-petroleum-jelly.jpg", "Rosehip · Petroleum Jelly", ["Rosehip", "Petroleum Jelly"],
         ["Rich, slow-melting comfort.", "250ml and 500ml."], ["rosehip-250ml", "rosehip-500ml"]),
    ]
    for fname, eyebrow, title, sub, keys in products:
        card = base_card()
        text_block(card, eyebrow, title, sub, "Order direct  ·  WhatsApp +27 72 212 1348")
        if len(keys) == 1:
            p = fit(cut[keys[0]], 360, 520)
            shadowed(card, p, (1200 - p.width - 150, 315 - p.height // 2))
        else:
            small, big = fit(cut[keys[0]], 250, 270), fit(cut[keys[1]], 330, 380)
            base = 470
            shadowed(card, small, (650, base - small.height + 60))
            shadowed(card, big, (1200 - big.width - 60, base - big.height + 60))
        card.convert("RGB").save(out / fname, quality=88, optimize=True)
    for f in sorted(out.glob("*.jpg")):
        print(f"social/{f.name}")


if __name__ == "__main__":
    build_logos()
    build_social(build_cutouts())
