#!/usr/bin/env python3
"""Draw entry.png: "The World on Monday" - a front-page poster summing up
the world news of Monday 23 November 2026.

Run with the project venv:  ~/workspace/makefun/.venv/bin/python draw_image.py
Writes entry.png (1024x1024) next to this file. The grader never runs this
script; main.ts copies the finished entry.png to /output/entry.png.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

SS = 2  # supersampling: draw at 2048, shrink to 1024
W = 1024

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

INK = (26, 26, 30)
PAPER = (248, 245, 238)
PANEL = (255, 255, 255)
PANEL_EDGE = (200, 195, 185)
RED = (168, 32, 40)
NAVY = (31, 58, 95)
GOLD = (198, 152, 40)
SLATE = (52, 60, 72)
GREY = (96, 96, 100)
STEEL = (46, 110, 160)
GREEN = (34, 139, 70)
ORANGE = (232, 110, 30)


def font(path, size):
    return ImageFont.truetype(path, size * SS)


def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap_text(d, s, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if text_w(d, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(d, cx, y, s, f, fill, tracking=0):
    """One centered line; tracking adds letter spacing in design units."""
    if tracking:
        total = sum(text_w(d, ch, f) for ch in s) + tracking * SS * (len(s) - 1)
        x = cx - total / 2
        for ch in s:
            d.text((x, y), ch, font=f, fill=fill)
            x += text_w(d, ch, f) + tracking * SS
        return
    w = text_w(d, s, f)
    d.text((cx - w / 2, y), s, font=f, fill=fill)


def star_shape(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ------------------------------------------------------------------ icons
# Every icon draws on its own transparent 240x150 canvas, centered at
# (120, 75) in design units; render() trims and scales it into a panel.


def icon_chip(d, cx, cy):
    """A computer chip with a rising arrow: Nvidia reinstates its CEO."""
    # chip body
    d.rectangle([cx - 42, cy - 34, cx + 42, cy + 34], fill=INK,
                outline=(255, 255, 255), width=3 * SS)
    d.rectangle([cx - 26, cy - 18, cx + 26, cy + 18], fill=(255, 255, 255),
                outline=INK, width=2 * SS)
    # pins on all four sides
    for i in range(4):
        x = cx - 30 + i * 20
        d.rectangle([x, cy - 46, x + 8, cy - 34], fill=INK)
        d.rectangle([x, cy + 34, x + 8, cy + 46], fill=INK)
    for i in range(3):
        y = cy - 20 + i * 20
        d.rectangle([cx - 54, y, cx - 42, y + 8], fill=INK)
        d.rectangle([cx + 42, y, cx + 54, y + 8], fill=INK)
    # green arrow rising out of the chip
    d.line([cx - 6, cy + 6, cx - 6, cy - 52], fill=GREEN, width=6 * SS)
    d.polygon([(cx - 20, cy - 40), (cx - 6, cy - 62), (cx + 8, cy - 40)],
              fill=GREEN)


def icon_tanker(d, cx, cy):
    """An oil tanker on waves under a red warning triangle: the Hormuz
    blockade standoff."""
    # waves
    for wy, amp in [(cy + 46, 7), (cy + 58, 5)]:
        pts = []
        for i in range(25):
            x = cx - 104 + i * 9
            pts.append((x, wy + amp * math.sin(i * 1.1 + wy)))
        d.line(pts, fill=STEEL, width=4 * SS, joint="curve")
    # tanker hull and deck
    d.polygon([(cx - 88, cy + 6), (cx + 84, cy + 6), (cx + 64, cy + 40),
               (cx - 68, cy + 40)], fill=SLATE)
    d.rectangle([cx - 60, cy - 16, cx + 20, cy + 6], fill=(70, 78, 92))
    d.rectangle([cx + 34, cy - 28, cx + 62, cy + 6], fill=NAVY)
    d.line([cx - 40, cy - 28, cx - 40, cy + 6], fill=INK, width=2 * SS)
    # red warning triangle overhead, big enough to read at panel size
    tx, ty = cx + 52, cy - 58
    d.polygon([(tx, ty - 30), (tx - 32, ty + 20), (tx + 32, ty + 20)],
              fill=RED)
    d.rectangle([tx - 3, ty - 15, tx + 3, ty + 4], fill=(255, 255, 255))
    d.ellipse([tx - 3, ty + 8, tx + 3, ty + 14], fill=(255, 255, 255))


def icon_aid(d, cx, cy):
    """Himalayan peaks behind an aid parcel: India's package for Nepal."""
    # two mountain peaks
    d.polygon([(cx - 96, cy + 52), (cx - 44, cy - 48), (cx + 4, cy + 52)],
              fill=SLATE)
    d.polygon([(cx - 60, cy - 48), (cx - 52, cy - 30), (cx - 44, cy - 48),
               (cx - 36, cy - 28), (cx - 28, cy - 48)],
              fill=(255, 255, 255))
    d.polygon([(cx - 30, cy + 52), (cx + 30, cy - 28), (cx + 92, cy + 52)],
              fill=(70, 78, 92))
    d.polygon([(cx + 16, cy - 28), (cx + 24, cy - 12), (cx + 32, cy - 28),
               (cx + 40, cy - 10), (cx + 44, cy - 28)],
              fill=(255, 255, 255))
    # aid parcel in front, ribboned
    bx0, by0, bx1, by1 = cx - 30, cy + 8, cx + 34, cy + 58
    d.rectangle([bx0, by0, bx1, by1], fill=GOLD, outline=INK, width=3 * SS)
    d.rectangle([cx - 4, by0, cx + 8, by1], fill=RED)
    d.rectangle([bx0, cy + 28, bx1, cy + 40], fill=RED)
    d.rectangle([bx0 - 4, by1, bx1 + 4, by1 + 5], fill=INK)


def icon_bank_ban(d, cx, cy):
    """A bank under a red prohibition ring: the EU's 22nd sanctions
    package."""
    # pediment and columns
    d.polygon([(cx - 62, cy - 30), (cx, cy - 56), (cx + 62, cy - 30)],
              fill=NAVY)
    d.ellipse([cx - 10, cy - 46, cx + 10, cy - 26], fill=GOLD)
    d.rectangle([cx - 66, cy - 30, cx + 66, cy - 20], fill=NAVY)
    for i in range(4):
        x = cx - 52 + i * 30
        d.rectangle([x, cy - 16, x + 12, cy + 34], fill=SLATE)
    d.rectangle([cx - 72, cy + 34, cx + 72, cy + 44], fill=NAVY)
    d.rectangle([cx - 80, cy + 44, cx + 80, cy + 52], fill=NAVY)
    # prohibition ring over the bank
    d.ellipse([cx - 92, cy - 66, cx + 92, cy + 66], outline=RED,
              width=7 * SS)
    d.line([cx - 62, cy + 50, cx + 62, cy - 52], fill=RED, width=7 * SS)


def icon_constitution(d, cx, cy):
    """A draft constitution page with one line struck out: Armenia drops
    the Karabakh reference."""
    x0, y0, x1, y1 = cx - 52, cy - 58, cx + 52, cy + 58
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=INK,
                width=3 * SS)
    # title bar
    d.rectangle([x0 + 10, y0 + 10, x1 - 10, y0 + 24], fill=NAVY)
    # text lines; the second is struck through in red
    for i in range(4):
        ly = y0 + 36 + i * 16
        d.line([x0 + 10, ly, x1 - 10, ly], fill=(170, 170, 178), width=3 * SS)
    d.line([x0 + 10, y0 + 52, x1 - 10, y0 + 52], fill=RED, width=4 * SS)
    # a pen resting on the page, lower right
    d.line([cx + 18, cy + 66, cx + 66, cy + 24], fill=INK, width=5 * SS)
    d.polygon([(cx + 66, cy + 24), (cx + 78, cy + 12), (cx + 70, cy + 32)],
              fill=GOLD)


def icon_gavel(d, cx, cy):
    """A judge's gavel before prison bars: Bangladesh will arrest the
    ex-PM if she returns."""
    # prison bars behind
    for i in range(5):
        x = cx - 72 + i * 36
        d.rectangle([x, cy - 56, x + 10, cy + 56], fill=SLATE)
    # gavel head and handle
    d.rounded_rectangle([cx - 46, cy - 34, cx + 26, cy - 8], radius=6 * SS,
                        fill=INK)
    d.line([cx - 10, cy - 21, cx + 44, cy + 40], fill=INK, width=7 * SS)
    d.ellipse([cx + 36, cy + 32, cx + 54, cy + 50], fill=INK)
    # sound block, bottom left, clear of the handle
    d.rectangle([cx - 78, cy + 40, cx - 20, cy + 54], fill=GOLD,
                outline=INK, width=2 * SS)


def render_icon(img, icon, ccx, cy, max_w=205, max_h=86):
    """Draw an icon on its own layer, trim transparent margins, and paste
    it scaled to fit a max_w x max_h box, centered at (ccx, cy)."""
    layer = Image.new("RGBA", (240 * SS, 150 * SS), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    icon(ld, 120 * SS, 75 * SS)
    bbox = layer.getbbox()
    if bbox:
        layer = layer.crop(bbox)
    scale = min(max_w * SS / layer.width, max_h * SS / layer.height)
    layer = layer.resize((round(layer.width * scale),
                          round(layer.height * scale)), Image.LANCZOS)
    img.paste(layer,
              (round(ccx * SS - layer.width / 2),
               round(cy * SS - layer.height / 2)), layer)


# ------------------------------------------------------------------ stories
STORIES = [
    ("TECH \u00b7 USA", NAVY, icon_chip,
     "HUANG IS NVIDIA CEO AGAIN",
     "Reinstated 11 days after resigning; shares jump 33% on the news."),
    ("STANDOFF \u00b7 GULF", RED, icon_tanker,
     "IRAN VOWS TO DEFY US BLOCKADE",
     "Tehran says it will use all means; a US drone is shot down."),
    ("AID \u00b7 ASIA", NAVY, icon_aid,
     "$1.62BN PACKAGE FOR NEPAL",
     "Modi announces grants and credit to rebuild after the flood."),
    ("SANCTIONS \u00b7 EUROPE", RED, icon_bank_ban,
     "EU PROPOSES 22ND RUSSIA PACKAGE",
     "60 banks off SWIFT, shadow fleet hit, athletes barred from EU events."),
    ("PEACE \u00b7 CAUCASUS", NAVY, icon_constitution,
     "ARMENIA DROPS KARABAKH CLAIM",
     "Draft constitution rewrites the preamble; Baku welcomes the step."),
    ("JUSTICE \u00b7 ASIA", NAVY, icon_gavel,
     "HASINA TO BE JAILED IF SHE RETURNS",
     "Bangladesh tells Reuters the ex-PM faces arrest on arrival."),
]


def main():
    img = Image.new("RGB", (W * SS, W * SS), PAPER)
    d = ImageDraw.Draw(img)

    def X(v):
        return v * SS

    # masthead
    d.rectangle([X(30), X(24), X(994), X(28)], fill=INK)
    draw_centered(d, X(512), X(36), "THE WORLD ON MONDAY", font(SERIF_B, 54),
                  INK, tracking=2)
    d.rectangle([X(30), X(106), X(994), X(110)], fill=INK)

    # date band
    d.rectangle([X(30), X(120), X(994), X(182)], fill=INK)
    draw_centered(d, X(512), X(129), "MONDAY 23 NOVEMBER 2026",
                  font(SANS_B, 48), (255, 255, 255), tracking=1)

    # panels: 2 cols x 3 rows, y 192..980
    gx, gy = 14, 14
    px0, py0 = 30, 192
    pw = (1024 - 60 - gx) // 2
    ph = (980 - py0 - 2 * gy) // 3
    kick_f = font(SANS_B, 18)
    head_f = font(SANS_B, 30)
    sub_f = font(SANS, 21)
    worst = 0  # deepest panel text bottom, in design units from panel top
    for i, (kicker, accent, icon, head, sub) in enumerate(STORIES):
        cx0 = px0 + (i % 2) * (pw + gx)
        cy0 = py0 + (i // 2) * (ph + gy)
        d.rectangle([X(cx0), X(cy0), X(cx0 + pw), X(cy0 + ph)], fill=PANEL,
                    outline=PANEL_EDGE, width=SS)
        d.rectangle([X(cx0), X(cy0), X(cx0 + pw), X(cy0 + 6)], fill=accent)
        ccx = cx0 + pw // 2
        draw_centered(d, X(ccx), X(cy0 + 11), kicker, kick_f, accent,
                      tracking=2)
        render_icon(img, icon, ccx, cy0 + 71)
        y = cy0 + 116
        for line in wrap_text(d, head, head_f, X(pw - 36)):
            draw_centered(d, X(ccx), X(y), line, head_f, INK)
            y += 36
        y += 4
        for line in wrap_text(d, sub, sub_f, X(pw - 44)):
            draw_centered(d, X(ccx), X(y), line, sub_f, (60, 60, 66))
            y += 24
        text_bottom = y - 3
        worst = max(worst, text_bottom - cy0)
        if text_bottom > cy0 + ph - 12:
            raise SystemExit(
                f"panel {i} text overflows: bottom {text_bottom - cy0} of {ph}")

    # footer
    d.rectangle([X(30), X(988), X(994), X(991)], fill=INK)
    draw_centered(d, X(512), X(995),
                  "SIX STORIES \u00b7 ONE DAY \u00b7 AS REPORTED BY REUTERS AND THE ASSOCIATED PRESS",
                  font(SANS_B, 14), GREY, tracking=1)

    img = img.resize((W, W), Image.LANCZOS)
    print("deepest panel text bottom:", worst, "of panel height", ph)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
