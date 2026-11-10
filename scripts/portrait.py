"""Turns the profile picture into colored ASCII <text> rows for the banner SVG."""
import html, sys
from PIL import Image, ImageEnhance
import numpy as np

RAMP = " .:-=+*%#@@"


def is_bg(r, g, b):
    # navy backdrop with its pattern + speed lines: dark and blue-dominant
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return (b > r + 15 and lum < 95) or lum < 28


def portrait(path, cols=66, cw=5.4, lh=9.0, crop=(300, 0, 2960, 2800)):
    im = Image.open(path).convert("RGB").crop(crop)
    im = ImageEnhance.Color(im).enhance(1.25)
    w, h = im.size
    rows = int(round(cols * (h / w) * cw / lh))
    small = np.asarray(im.resize((cols, rows), Image.LANCZOS)).astype(int)
    lines = []
    for y in range(rows):
        spans, prev, buf = [], None, ""
        for x in range(cols):
            r, g, b = small[y, x]
            if is_bg(r, g, b):
                ch, col = " ", None
            else:
                lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                ch = RAMP[min(len(RAMP) - 1, int(lum * (len(RAMP) - 1) + 0.999))]
                if ch == " ":
                    ch = "."
                col = "#%02x%02x%02x" % (min(255, int(r * 1.1)), min(255, int(g * 1.1)), min(255, int(b * 1.1)))
            if col != prev and buf:
                spans.append((buf, prev)); buf = ""
            buf += ch; prev = col
        if buf:
            spans.append((buf, prev))
        lines.append(spans)
    return lines, rows


def to_svg(lines, x0, y0, lh):
    out = []
    for i, spans in enumerate(lines):
        ts = "".join(
            (f'<tspan fill="{c}">{html.escape(s)}</tspan>' if c else html.escape(s))
            for s, c in spans
        )
        out.append(f'<text class="px" x="{x0}" y="{y0 + i * lh:.1f}">{ts}</text>')
    return out
