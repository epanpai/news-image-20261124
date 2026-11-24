#!/usr/bin/env python3
"""Draw the front page for news-image-20261124 (Tuesday 24 November 2026).

Pure Pillow, DejaVu fonts. Output: assets/entry.png, 1024x1024, < 1 MiB.
Run: python3 gen_image.py
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
BLUE = (28, 68, 120)
TEAL = (16, 90, 90)
GREY = (90, 88, 80)
LIGHT = (235, 229, 214)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FD}/{name}", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, max_w, fill=INK, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(draw, cx, cy, r):
    """Cracked earth globe."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(126, 180, 210),
                 outline=INK, width=3)
    # continents (simple blobs)
    draw.ellipse([cx - r + 18, cy - r + 30, cx - 10, cy - r + 78],
                 fill=(96, 150, 80))
    draw.ellipse([cx - 6, cy - 8, cx + r - 22, cy + 42], fill=(96, 150, 80))
    draw.ellipse([cx - r + 30, cy + 30, cx + 6, cy + r - 18],
                 fill=(120, 165, 95))
    # crack: jagged line from top to bottom
    pts = [(cx - 8, cy - r + 4), (cx + 12, cy - r + 34), (cx - 14, cy - r + 70),
           (cx + 8, cy - r + 108), (cx - 10, cy - r + 142), (cx + 4, cy + r - 6)]
    draw.line(pts, fill=INK, width=4, joint="curve")
    # small crack branches
    draw.line([(cx - 14, cy - r + 70), (cx - 34, cy - r + 92)], fill=INK, width=3)
    draw.line([(cx + 8, cy - r + 108), (cx + 30, cy - r + 128)], fill=INK, width=3)


def draw_ship_fire(draw, x0, y0, x1, y1):
    """Burning warship silhouette on dark sea."""
    draw.rectangle([x0, y0, x1, y1], fill=(24, 30, 46))
    # sea
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(52, 96, 140))
    for i in range(5):
        wx = x0 + 14 + i * 52
        draw.arc([wx, y1 - 22, wx + 34, y1 - 6], 180, 360, fill=(180, 210, 235),
                 width=2)
    # hull
    hx0, hx1, hy = x0 + 18, x1 - 18, y1 - 34
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 16, hy + 16), (hx0 + 10, hy + 16)],
                 fill=(10, 10, 14))
    # superstructure + mast
    draw.rectangle([hx0 + 34, hy - 26, hx0 + 96, hy], fill=(16, 16, 20))
    draw.line([(hx0 + 66, hy - 26), (hx0 + 66, hy - 52)], fill=(16, 16, 20), width=4)
    # flames
    fx = hx0 + 120
    for (dx, w, h, col) in [(0, 46, 66, (235, 120, 20)), (10, 30, 48, (245, 180, 40)),
                            (18, 16, 30, (250, 230, 120))]:
        draw.ellipse([fx + dx, hy - h, fx + dx + w, hy + 4], fill=col)
    # smoke
    for i, (sx, sy, sr) in enumerate([(fx + 8, hy - 58, 12), (fx + 26, hy - 72, 14),
                                      (fx + 2, hy - 84, 10)]):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 125))
    draw.text((x1 - 196, y0 + 8), "BENGHAZI, LIBYA", font=SANS_B(17),
              fill=(235, 220, 180))


def draw_flame_icon(draw, cx, cy, s):
    draw.ellipse([cx - s, cy - s * 0.7, cx + s, cy + s * 0.7], fill=(245, 170, 30))
    draw.ellipse([cx - s * 0.55, cy - s * 0.3, cx + s * 0.55, cy + s * 0.7],
                 fill=(235, 110, 20))
    draw.ellipse([cx - s * 0.25, cy + s * 0.1, cx + s * 0.25, cy + s * 0.7],
                 fill=(250, 225, 110))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    X1 = W - M

    # ---------- masthead ----------
    d.text((W // 2, 26), "THE WORLD IN ONE DAY", font=SERIF_B(58),
           fill=INK, anchor="ma")
    d.text((W // 2, 96), "TUESDAY, 24 NOVEMBER 2026", font=SANS_B(26),
           fill=RED, anchor="ma")
    rule(d, M, 136, X1, 3)
    rule(d, M, 142, X1, 1)

    # ---------- lead headline ----------
    d.text((M, 154), "CLIMATE TALKS COLLAPSE", font=SERIF_B(56), fill=INK)
    y = para(d, (M, 222),
             "COP31 ends in Antalya with no deal — the summit draft never "
             "once names fossil fuels, and the talks close empty-handed.",
             SANS(23), X1 - M, leading=30)
    rule(d, M, 292, X1, 1, fill=GREY)

    # ---------- lead row: globe + COP31 text | ship panel ----------
    mid_x = 560
    # globe left
    draw_globe(d, 150, 400, 92)
    # NO DEAL stamp
    stamp = Image.new("RGBA", (200, 58), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([3, 3, 196, 54], outline=RED, width=5)
    sd.text((100, 29), "NO DEAL", font=SANS_B(30), fill=RED, anchor="mm")
    stamp = stamp.rotate(-14, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (44, 448), stamp)
    d = ImageDraw.Draw(img)
    # COP31 body text right of globe
    tx = 268
    d.text((tx, 312), "ANTALYA, TÜRKIYE", font=SANS_B(18), fill=RED)
    y = para(d, (tx, 338),
             "Negotiators leave with nothing. The EU and others reject a "
             "draft that never names fossil fuels.",
             SANS(20), mid_x - tx - 16, leading=26)
    d.text((tx, 470), "“A pact that cannot say the words", font=SERIF(19),
           fill=INK)
    d.text((tx, 494), "‘fossil fuels’ is no pact at all.”", font=SERIF(19),
           fill=INK)
    d.text((tx, 524), "— delegates, as the summit closes", font=SANS(16),
           fill=GREY)

    # ship panel right
    px0, px1 = mid_x + 16, X1
    d.rectangle([px0, 306, px1, 548], outline=INK, width=2)
    d.text((px0 + 12, 314), "WAR AT SEA SPREADS", font=SANS_B(24), fill=INK)
    draw_ship_fire(d, px0 + 2, 348, px1 - 2, 470)
    y = para(d, (px0 + 12, 478),
             "A Russian Navy corvette is destroyed in a blast and fire at "
             "the port of Benghazi, Libya — the war reaching far beyond "
             "Ukraine.",
             SANS(17), px1 - px0 - 24, leading=22)
    rule(d, M, 566, X1, 2)

    # ---------- three panels ----------
    py0, py1 = 584, 836
    cols = [(M, 304), (360, 304), (684, 304)]
    # panel 1: Indonesia factory fire
    x0, w = cols[0]
    d.rectangle([x0, py0, x0 + w, py1], outline=INK, width=2)
    draw_flame_icon(d, x0 + 52, py0 + 46, 26)
    d.text((x0 + 92, py0 + 18), "INDONESIA", font=SANS_B(22), fill=INK)
    d.text((x0 + 92, py0 + 46), "FACTORY FIRE", font=SANS_B(22), fill=RED)
    para(d, (x0 + 14, py0 + 92),
         "At least 24 workers are dead and around 30 still missing after "
         "a fire tears through a factory in Banten. Rescuers keep "
         "searching the ruins.",
         SANS(18), w - 28, leading=23)
    # panel 2: Kyiv
    x0, w = cols[1]
    d.rectangle([x0, py0, x0 + w, py1], outline=INK, width=2)
    d.text((x0 + 14, py0 + 14), "KYIV UNDER FIRE", font=SANS_B(22), fill=INK)
    d.text((x0 + 14, py0 + 44), "— AND THE BALTIC", font=SANS_B(22), fill=BLUE)
    para(d, (x0 + 14, py0 + 92),
         "A Russian drone strike on a building in the Kyiv region leaves "
         "several people missing, Zelenskiy says. The cargo ship Sparta II "
         "burns off Finland after a drone attack.",
         SANS(18), w - 28, leading=23)
    # panel 3: Lisbon
    x0, w = cols[2]
    d.rectangle([x0, py0, x0 + w, py1], outline=INK, width=2)
    d.text((x0 + 14, py0 + 14), "LISBON MARCHES", font=SANS_B(22), fill=INK)
    d.text((x0 + 14, py0 + 44), "COST OF LIVING", font=SANS_B(22), fill=TEAL)
    para(d, (x0 + 14, py0 + 92),
         "Thousands take to the streets of Portugal's capital to protest "
         "rising living costs, as household budgets keep shrinking.",
         SANS(18), w - 28, leading=23)

    # ---------- ticker ----------
    ty0, ty1 = 854, 962
    d.rectangle([M, ty0, X1, ty1], fill=INK)
    d.text((M + 14, ty0 + 12), "ALSO TODAY", font=SANS_B(20), fill=(250, 200, 60))
    ticker = ("World Chess Championship opens in Geneva: Gukesh vs Sindarov "
              "•  Alcaraz wins his first ATP Finals title  •  Verstappen wins "
              "the Las Vegas Grand Prix  •  Modi and Shah flag off the "
              "India–Nepal train  •  Oxfam: Gaza poisoned for decades  •  "
              "Bangladesh vows Hasina arrest")
    para(d, (M + 14, ty0 + 38), ticker, SANS(18), X1 - M - 28,
         fill=(240, 240, 235), leading=22)

    # ---------- footer ----------
    d.text((W // 2, 978), "make.fun — one day's world news, in one image",
           font=SANS(16), fill=GREY, anchor="ma")

    img.save("assets/entry.png", optimize=True)
    print("saved assets/entry.png")


if __name__ == "__main__":
    main()
