"""
One-shot favicon generator for MOEMODI.
Generates: favicon.ico (16/32/48), favicon-16.png, favicon-32.png,
apple-touch-icon.png (180x180), and a maskable 512 PNG.

The icon mark is composited onto the brand Ivory (#F6F4EE) background
with rounded corners, so it stays visible against dark browser tab themes.

Run from the moemodi-dev repo root:
    python assets/images/logos/_build_favicons.py
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]  # moemodi-dev/
SRC  = ROOT / "assets" / "images" / "logos" / "moemodi-icon-transparent.png"

IVORY = (246, 244, 238, 255)   # --mm-ivory
GREEN = (31, 75, 58, 255)      # --mm-botanical-green (used for outline accent)


def make_icon(size: int, padding_ratio: float = 0.10, rounded: bool = True) -> Image.Image:
    """Composite the transparent lion mark onto an ivory rounded square."""
    src = Image.open(SRC).convert("RGBA")

    # Trim transparent borders so the mark fills the canvas evenly
    bbox = src.getbbox()
    if bbox:
        src = src.crop(bbox)

    canvas = Image.new("RGBA", (size, size), IVORY)

    # Compute the inner area for the mark
    pad = int(size * padding_ratio)
    inner = size - (pad * 2)

    # Resize the mark preserving aspect ratio
    sw, sh = src.size
    scale = inner / max(sw, sh)
    nw = max(1, int(sw * scale))
    nh = max(1, int(sh * scale))
    mark = src.resize((nw, nh), Image.LANCZOS)

    # Paste centered
    ox = (size - nw) // 2
    oy = (size - nh) // 2
    canvas.paste(mark, (ox, oy), mark)

    if rounded:
        # Apply a rounded-square mask
        radius = max(2, int(size * 0.18))
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [(0, 0), (size - 1, size - 1)], radius=radius, fill=255
        )
        out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        out.paste(canvas, (0, 0), mask)
        return out

    return canvas


def main():
    if not SRC.exists():
        raise SystemExit(f"Source not found: {SRC}")

    # Multi-size ICO at the site root
    sizes = [16, 32, 48, 64]
    images = [make_icon(s, rounded=False) for s in sizes]
    ico_path = ROOT / "favicon.ico"
    images[0].save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:],
    )

    # PNG fallbacks at standard sizes
    (ROOT / "favicon-16.png").write_bytes(b"")  # placeholder so PIL can save
    make_icon(16, rounded=False).save(ROOT / "favicon-16.png", "PNG", optimize=True)
    make_icon(32, rounded=False).save(ROOT / "favicon-32.png", "PNG", optimize=True)

    # Apple touch icon (iOS adds its own corner radius, so we skip rounding)
    make_icon(180, padding_ratio=0.10, rounded=False).save(
        ROOT / "apple-touch-icon.png", "PNG", optimize=True
    )

    # PWA-grade large icon (maskable safe area)
    make_icon(512, padding_ratio=0.18, rounded=False).save(
        ROOT / "assets" / "images" / "logos" / "moemodi-icon-512.png",
        "PNG",
        optimize=True,
    )

    print("Wrote:")
    for p in [ico_path, ROOT / "favicon-16.png", ROOT / "favicon-32.png",
              ROOT / "apple-touch-icon.png",
              ROOT / "assets/images/logos/moemodi-icon-512.png"]:
        print(" ", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
