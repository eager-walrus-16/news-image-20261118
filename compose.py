#!/usr/bin/env python3
"""Compose the news-image-20261118 entry: a front-page newspaper poster
that sums up Wednesday 18 November 2026 in one image.

Reads the four scene images from assets/ and writes entry.png (2400x1600).
Pure PIL, no network, no downloaded assets.
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 2400, 1600
MARGIN = 40
NAVY = (13, 30, 58)
GOLD = (216, 164, 65)
PAPER = (251, 249, 244)
INK = (18, 18, 18)
GREY = (90, 90, 90)
RED = (158, 27, 34)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_text(draw, text, fnt_path, size, max_w, min_size=18):
    """Shrink the font until the text fits max_w on one line."""
    s = size
    while s > min_size:
        f = font(fnt_path, s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 2
    return font(fnt_path, min_size)


def cover(img_path, tw, th):
    im = Image.open(img_path).convert("RGB")
    return ImageOps.fit(im, (tw, th), Image.LANCZOS, centering=(0.5, 0.45))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- Masthead ----------
    d.rectangle([0, 0, W, 208], fill=NAVY)
    d.rectangle([0, 208, W, 214], fill=GOLD)
    title = "THE WORLD IN ONE PICTURE"
    f_title = fit_text(d, title, SERIF_B, 96, W - 2 * MARGIN)
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 26), title, font=f_title, fill=(255, 255, 255))
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    f_date = fit_text(d, date, SANS_B, 46, W - 2 * MARGIN)
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 138), date, font=f_date, fill=GOLD)

    # ---------- Lead story (left, ~55% width) ----------
    lx, ly, lw, lh = MARGIN, 232, 1340, 756
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=(255, 255, 255),
                outline=(200, 196, 186), width=2)
    lead_img = cover("assets/media-generation-news-gulf-tankers-0-a7e52174-f7b7-456a-a117-309771f615ba.webp",
                     lw - 24, 430)
    img.paste(lead_img, (lx + 12, ly + 12))
    # red kicker
    d.text((lx + 24, ly + 462), "WAR IN THE GULF  —  LEAD STORY",
           font=font(SANS_B, 30), fill=RED)
    head = "FIVE TANKERS ABLAZE AS U.S.-IRAN WAR ERUPTS IN THE GULF"
    y = draw_wrapped(d, (lx + 24, ly + 506), head, font(SERIF_B, 56),
                     INK, lw - 48, 66)
    stand = ("U.S. forces sank five Iranian tankers after attacks on a "
             "warship; Iran hit ships near Hormuz and fired on a U.S. "
             "base in Jordan.")
    draw_wrapped(d, (lx + 24, y + 8), stand, font(SANS, 31),
                 (60, 60, 60), lw - 48, 40)

    # ---------- Day in numbers (right of lead) ----------
    rx, ry, rw, rh = 1420, 232, 940, 756
    d.rectangle([rx, ry, rx + rw, ry + rh], fill=NAVY)
    d.text((rx + 36, ry + 28), "THE DAY IN NUMBERS",
           font=font(SERIF_B, 44), fill=GOLD)
    d.line([rx + 36, ry + 96, rx + rw - 36, ry + 96], fill=GOLD, width=3)
    numbers = [
        ("5", "tankers ablaze in the Gulf as war erupts"),
        ("144", "disputed items left in the COP31 draft deal"),
        ("5.3", "magnitude of the earthquake in Romania"),
        ("4", "Quad leaders meeting in Manila"),
    ]
    y = ry + 130
    for num, label in numbers:
        f_num = font(SERIF_B, 64)
        d.text((rx + 36, y), num, font=f_num, fill=(255, 255, 255))
        nw = d.textlength(num, font=f_num)
        draw_wrapped(d, (rx + 36 + nw + 28, y + 12), label,
                     font(SANS, 30), (225, 225, 225), rw - 36 - nw - 64, 40)
        y += 148
    d.text((rx + 36, ry + rh - 52), "All figures as reported on the day.",
           font=font(SANS, 24), fill=(170, 175, 190))

    # ---------- Three secondary panels ----------
    py, ph = 1012, 428
    panels = [
        ("assets/media-generation-news-kerch-bridge-0-fe585026-e5e4-49f7-b74e-b1e0b680b23c.webp",
         "KERCH BRIDGE HIT AGAIN — SPAN DOWN, ROAD CUT",
         "Ukraine struck the Crimea link a second night; Russia hit Kyiv bridges."),
        ("assets/media-generation-news-quad-manila-0-d2e71716-2c85-426a-a2fe-8430b23063ee.webp",
         "QUAD MEETS IN MANILA AHEAD OF SHENZHEN SUMMIT",
         "Trump, Modi, Takaichi and Albanese meet before Thursday's U.S.-Russia-China summit."),
        ("assets/media-generation-news-cop31-antalya-0-8e2f5631-2481-4faf-8ac2-636481e30b68.webp",
         "COP31 ENTERS ENDGAME — 144 ITEMS UNSETTLED",
         "Climate talks in Antalya race a draft deal with 144 disputed points."),
    ]
    pw, gap = 746, 21
    for i, (path, head, cap) in enumerate(panels):
        x = MARGIN + i * (pw + gap)
        d.rectangle([x, py, x + pw, py + ph], fill=(255, 255, 255),
                    outline=(200, 196, 186), width=2)
        im = cover(path, pw - 24, 208)
        img.paste(im, (x + 12, py + 12))
        y = draw_wrapped(d, (x + 20, py + 232), head, font(SERIF_B, 34),
                         INK, pw - 40, 42)
        draw_wrapped(d, (x + 20, y + 6), cap, font(SANS, 26),
                     (60, 60, 60), pw - 40, 33)

    # ---------- Ticker ----------
    ty = 1464
    d.rectangle([0, ty, W, H], fill=NAVY)
    d.rectangle([0, ty, W, ty + 6], fill=GOLD)
    ticker = ("ALSO TODAY:  Romania quake M5.3  ·  UN warns of cold deaths in Gaza  ·  "
              "Prague crowds demand a free press  ·  Estonia to shut its Russia border")
    f_tick = fit_text(d, ticker, SANS_B, 32, W - 2 * MARGIN)
    d.text((MARGIN, ty + 46), ticker, font=f_tick, fill=(255, 255, 255))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
