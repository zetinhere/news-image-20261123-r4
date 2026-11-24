#!/usr/bin/env python3
"""THE WORLD — a newspaper front page for Monday 23 November 2026.

Concept (different from this competition's earlier entries: no collage
grid, no clock dial): the whole day as one broadsheet front page.
Masthead, dateline, a lead story on the COP31 collapse with a drawn
globe-and-smokestack illustration, six more stories in two rows of
three columns, and an "Also today" footer ticker. Every headline is a
real story first reported on Monday 23 November 2026.

Everything is drawn from scratch with PIL: no network, no downloaded
images, no randomness, no timestamps. Run: python3 draw.py
-> entry.png (1024x1024, under 1 MiB).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 228)
INK = (26, 26, 24)
SOFT = (74, 70, 62)
FAINT = (150, 142, 124)
RED = (172, 32, 28)
BLUE = (28, 58, 96)
GOLD = (176, 128, 34)
TEAL = (18, 110, 96)
RULE = (26, 26, 24)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap into lines fitting `width` pixels."""
    out = []
    for para in text.split("\n"):
        words = para.split()
        line = ""
        for w in words:
            trial = (line + " " + w).strip()
            if d.textlength(trial, font=fnt) <= width:
                line = trial
            elif line:
                out.append(line)
                line = w
            else:
                out.append(w)
                line = ""
        if line:
            out.append(line)
    return out


def para(d, x, y, text, fnt, width, leading, color=INK, align="left"):
    """Draw wrapped paragraph, return y just below the last line."""
    for line in wrap(d, text, fnt, width):
        if align == "center":
            lx = x + (width - d.textlength(line, font=fnt)) / 2
        else:
            lx = x
        d.text((lx, y), line, font=fnt, fill=color)
        y += leading
    return y


def centre(d, cx, y, text, fnt, color=INK):
    d.text((cx - d.textlength(text, font=fnt) / 2, y), text, font=fnt,
           fill=color)
    return y


def rule(d, x0, x1, y, width=2, color=RULE):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def double_rule(d, x0, x1, y):
    rule(d, x0, x1, y, 3)
    rule(d, x0, x1, y + 6, 1)


# ------------------------------------------------------------------ icons
def disc(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color,
              outline=INK, width=2)


def icon_globe(d, cx, cy, r):
    disc(d, cx, cy, r, (52, 110, 168))
    d.ellipse([cx - r * 0.55, cy - r * 0.45, cx - r * 0.05, cy + r * 0.05],
              fill=(96, 168, 92))
    d.ellipse([cx + r * 0.05, cy + r * 0.15, cx + r * 0.6, cy + r * 0.55],
              fill=(96, 168, 92))
    d.line([(cx - r * 0.7, cy - r * 0.6), (cx - r * 0.2, cy - r * 0.1),
            (cx - r * 0.45, cy + r * 0.25), (cx + r * 0.1, cy + r * 0.6)],
           fill=INK, width=4)


def icon_missile(d, cx, cy, r):
    disc(d, cx, cy, r, (96, 96, 100))
    d.polygon([(cx - 12, cy + 16), (cx + 16, cy - 14), (cx + 22, cy - 4),
               (cx - 2, cy + 22)], fill=(240, 240, 235))
    d.polygon([(cx + 16, cy - 14), (cx + 26, cy - 22), (cx + 24, cy - 6)],
              fill=RED)
    d.polygon([(cx - 12, cy + 16), (cx - 22, cy + 12), (cx - 16, cy + 24)],
              fill=(200, 60, 40))


def icon_ship(d, cx, cy, r):
    disc(d, cx, cy, r, (38, 92, 140))
    d.polygon([(cx - 22, cy + 4), (cx + 22, cy + 4), (cx + 14, cy + 18),
               (cx - 14, cy + 18)], fill=(250, 246, 236))
    d.line([(cx, cy + 4), (cx, cy - 16)], fill=(250, 246, 236), width=4)
    d.polygon([(cx, cy - 16), (cx + 12, cy - 8), (cx, cy - 6)], fill=RED)
    for dx, dy in [(-12, -14), (10, -16), (0, -18)]:
        d.line([(cx + dx, cy + dy), (cx + dx + 4, cy + dy - 5)], fill=GOLD,
               width=3)
        d.line([(cx + dx, cy + dy), (cx + dx - 4, cy + dy - 5)], fill=GOLD,
               width=3)


def icon_flame(d, cx, cy, r):
    disc(d, cx, cy, r, (196, 84, 32))
    d.polygon([(cx, cy - 20), (cx + 12, cy - 2), (cx + 16, cy + 10),
               (cx + 6, cy + 20), (cx - 8, cy + 20), (cx - 16, cy + 8),
               (cx - 10, cy - 8)], fill=(245, 178, 44))
    d.polygon([(cx, cy - 8), (cx + 7, cy + 4), (cx + 3, cy + 14),
               (cx - 6, cy + 14), (cx - 8, cy + 2)], fill=(250, 240, 210))


def icon_planet(d, cx, cy, r):
    disc(d, cx, cy, r, (30, 30, 44))
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(196, 148, 96))
    for ox, oy, cr in [(-7, -5, 4), (6, 3, 5), (-2, 9, 3), (8, -8, 3)]:
        d.ellipse([cx + ox - cr, cy + oy - cr, cx + ox + cr, cy + oy + cr],
                  fill=(150, 108, 66))
    d.line([(cx - 24, cy + 10), (cx + 24, cy - 10)], fill=GOLD, width=3)


def icon_chip(d, cx, cy, r):
    disc(d, cx, cy, r, (28, 58, 96))
    d.rectangle([cx - 13, cy - 13, cx + 13, cy + 13], fill=(240, 240, 235),
                outline=INK, width=2)
    d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], fill=TEAL)
    for i in (-8, 0, 8):
        d.line([(cx + i, cy - 19), (cx + i, cy - 13)], fill=(240, 240, 235),
               width=3)
        d.line([(cx + i, cy + 13), (cx + i, cy + 19)], fill=(240, 240, 235),
               width=3)
        d.line([(cx - 19, cy + i), (cx - 13, cy + i)], fill=(240, 240, 235),
               width=3)
        d.line([(cx + 13, cy + i), (cx + 19, cy + i)], fill=(240, 240, 235),
               width=3)


# ------------------------------------------------------------------ page
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 36                      # margin
RX = W - MX                   # right edge

# --- masthead: 24..192 ---------------------------------------------
rule(d, MX, RX, 24, 3)
centre(d, W // 2, 30, "THE WORLD", font(SERIF_B, 84))
centre(d, W // 2, 124, "ONE DAY  •  ONE PLANET  •  ONE PAGE",
       font(SANS_B, 16), color=SOFT)
double_rule(d, MX, RX, 150)
d.text((MX, 164), "MONDAY", font=font(SANS_B, 18), fill=INK)
centre(d, W // 2, 164, "23 NOVEMBER 2026", font(SANS_B, 18), color=RED)
right = "No. 327  •  FREE EDITION"
d.text((RX - d.textlength(right, font=font(SANS_B, 18)), 164), right,
       font=font(SANS_B, 18), fill=INK)
double_rule(d, MX, RX, 190)

# --- lead story: COP31, 202..520 ------------------------------------
y = 202
centre(d, W // 2, y, "CLIMATE  •  ANTALYA, TURKEY", font(SANS_B, 17),
       color=RED)
y += 28
centre(d, W // 2, y, "CLIMATE TALKS COLLAPSE", font(SERIF_B, 56))
y += 66
centre(d, W // 2, y,
       "Record-long summit ends with no deal as nations split over fossil fuels",
       font(SERIF_I, 23), color=SOFT)
y += 38

# lead illustration panel (right) + lead text (left)
panel_x, panel_y, panel_w, panel_h = 636, y, 316, 158
d.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h],
            fill=(232, 222, 196), outline=INK, width=2)
gx, gy, gr = panel_x + 88, panel_y + 76, 52
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(52, 110, 168),
          outline=INK, width=3)
d.ellipse([gx - 28, gy - 23, gx - 3, gy + 2], fill=(96, 168, 92))
d.ellipse([gx + 3, gy + 7, gx + 30, gy + 28], fill=(96, 168, 92))
d.line([(gx - 37, gy - 32), (gx - 10, gy - 5), (gx - 23, gy + 13),
        (gx + 5, gy + 32)], fill=INK, width=4)
for sx in (panel_x + 186, panel_x + 222, panel_x + 258):
    d.polygon([(sx, panel_y + panel_h - 46), (sx + 26, panel_y + panel_h - 46),
               (sx + 21, panel_y + 52), (sx + 5, panel_y + 52)],
              fill=(90, 84, 76))
    d.ellipse([sx - 2, panel_y + 34, sx + 24, panel_y + 56],
              fill=(168, 160, 144))
    d.ellipse([sx + 4, panel_y + 22, sx + 22, panel_y + 40],
              fill=(190, 182, 166))
d.line([(panel_x + 8, panel_y + panel_h - 12),
        (panel_x + panel_w - 8, panel_y + panel_h - 12)], fill=INK, width=3)
d.text((panel_x + 10, panel_y + panel_h + 6),
       "The longest climate summit on record ends empty-handed.",
       font=font(SERIF_I, 14), fill=SOFT)

lead = ("The longest UN climate conference ever held ended on Monday "
        "with no agreement. After record-long talks in Turkey, countries "
        "split over phasing out fossil fuels and over adaptation finance "
        "for the nations hit hardest by warming — and walked away with "
        "neither.")
y = para(d, MX, y, lead, font(SERIF, 20), 576, 27)
y += 8
para(d, MX, y,
     "“We came for a deal and leave with a warning,” one negotiator said.",
     font(SERIF_I, 19), 576, 26, color=SOFT)

# --- section header: 540..592 ---------------------------------------
sy = 540
double_rule(d, MX, RX, sy)
centre(d, W // 2, sy + 12, "—  THE DAY IN BRIEF  —", font(SANS_B, 17),
       color=BLUE)
rule(d, MX, RX, sy + 40, 1, color=FAINT)

stories = [
    ("THE GULF", "TRUMP WARNS OF NEW IRAN STRIKES", RED,
     "Strikes on Iran resume in the new year, the US president warns, "
     "as Iranian strikes wound two in Bahrain.", icon_missile),
    ("THE MEDITERRANEAN", "RUSSIAN WARSHIP SUNK OFF LIBYA", BLUE,
     "A Russian vessel exploded at Benghazi in a suspected Ukrainian "
     "drone strike, carrying the war into the Mediterranean.", icon_ship),
    ("UKRAINE", "15 KILLED AS RUSSIA HITS KYIV", INK,
     "Russian bombardment around Kyiv killed at least 15 people; a boy "
     "was pulled alive from the rubble.", icon_flame),
    ("INDONESIA", "FACTORY FIRE KILLS AT LEAST 24", RED,
     "A blaze at a sweets factory killed at least 24 people, with about "
     "30 more missing.", icon_flame),
    ("SPACE", "BEPICOLOMBO REACHES MERCURY", TEAL,
     "After an eight-year journey, BepiColombo entered orbit around "
     "Mercury — a first for the joint European-Japanese mission.",
     icon_planet),
    ("MARKETS", "NVIDIA SOARS AS HUANG RETURNS", GOLD,
     "Nvidia shares jumped 31.5% as Jensen Huang returned as chief "
     "executive, while Asian tech shares slid in an AI sell-off.",
     icon_chip),
]

col_w = (RX - MX - 2 * 28) // 3
row_h = 168
for row in range(2):
    top = 600 + row * row_h
    for col in range(3):
        kicker, head, accent, body, icon = stories[row * 3 + col]
        x = MX + col * (col_w + 28)
        icon(d, x + 21, top + 21, 21)
        d.text((x + 50, top + 11), kicker, font=font(SANS_B, 14),
               fill=accent)
        yy = para(d, x, top + 46, head, font(SERIF_B, 21), col_w, 24)
        para(d, x, top + 98, body, font(SERIF, 14), col_w, 19)
        if col < 2:
            d.line([(x + col_w + 14, top + 4), (x + col_w + 14,
                    top + row_h - 14)], fill=FAINT, width=1)
    if row == 0:
        rule(d, MX, RX, top + row_h - 6, 1, color=FAINT)

# --- footer ticker: 940..1006 ---------------------------------------
fy = 940
double_rule(d, MX, RX, fy)
ticker = ("ALSO TODAY:  12,000 evacuated from a Manchester concert  •  "
          "Anthropic says AI helped prove the Riemann hypothesis  •  "
          "Seoul's education minister resigns over exam cheating")
para(d, MX, fy + 14, ticker, font(SANS_B, 15), RX - MX, 20, color=SOFT)
rule(d, MX, RX, 1006, 3)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size, len(open("entry.png", "rb").read()),
      "bytes")
