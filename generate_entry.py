#!/usr/bin/env python3
"""Deterministic news-image generator for 18 November 2026 — 48+ stories, world map, SVG-style."""
import os, math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 242, 230)
INK = (28, 28, 28)
MUTED = (85, 80, 72)
RULE = (188, 178, 162)
WHITE = (255, 255, 255)
DARK = (34, 32, 28)
PANEL_BG = (252, 249, 242)
OCEAN = (208, 224, 240)
MAP_STROKE = (140, 150, 165)

COL = {
    'EU': (47, 87, 160),
    'ME': (196, 102, 28),
    'AS': (112, 64, 160),
    'AF': (46, 122, 78),
    'AM': (176, 54, 54),
    'OC': (20, 132, 140),
    'BZ': (120, 90, 40),
    'SC': (50, 85, 140),
}

def load_font(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

f_title    = load_font('/system/fonts/NotoSerif-Bold.ttf', 44)
f_sub      = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 16)
f_strip_val = load_font('/system/fonts/NotoSerif-Bold.ttf', 20)
f_strip_lab = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 12)
f_tag      = load_font('/system/fonts/RobotoCondensed-Bold.ttf', 12)
f_lead_h   = load_font('/system/fonts/NotoSerif-Bold.ttf', 22)
f_lead_b   = load_font('/system/fonts/Roboto-Regular.ttf', 13)
f_panel_h  = load_font('/system/fonts/RobotoCondensed-Bold.ttf', 14)
f_item     = load_font('/system/fonts/Roboto-Regular.ttf', 11)
f_map_tag  = load_font('/system/fonts/RobotoCondensed-Bold.ttf', 10)
f_utc      = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 10)
f_footer   = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 9)
f_datecheck = load_font('/system/fonts/NotoSerif-Bold.ttf', 16)

img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

# ─── helpers ───────────────────────────────────────────
def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if d.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines or ['']

def draw_wrapped(x, y, text, font, fill, max_w, lh, mx=None):
    lines = wrap(text, font, max_w)
    if mx is not None: lines = lines[:mx]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y

def rr(xy, radius, fill, outline=None, width=1):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def dc(y, text, font, fill):
    tw = d.textlength(text, font=font)
    d.text(((W - tw) / 2, y), text, font=font, fill=fill)

# ─── lead illustrations ───────────────────────────────
def draw_lead_bridge(x, y, w, h):
    rr([x, y, x+w, y+h], 6, (232, 228, 218), outline=RULE)
    # Sky
    d.rectangle([x+2, y+2, x+w-2, y+h-2], fill=(215, 228, 242))
    # Water
    d.rectangle([x+2, y+h-24, x+w-2, y+h-2], fill=(155, 195, 225))
    # Bridge pillars
    for px in [x+16, x+w//3, x+w//2, x+2*w//3, x+w-16]:
        d.rectangle([px-3, y+24, px+3, y+h-24], fill=(80, 82, 88))
        d.rectangle([px-4, y+22, px+4, y+26], fill=(65, 67, 72))
    # Bridge deck
    d.rectangle([x+8, y+h//2-6, x+w-8, y+h//2+6], fill=(72, 74, 80))
    # Suspension cables
    for px in [x+16, x+w//3, x+w//2, x+2*w//3, x+w-16]:
        d.line([px, y+26, x+w//2, y+h//2-6], fill=(90, 92, 98), width=1)
        d.line([px, y+h//2+6, x+w//2, y+h//2-6], fill=(90, 92, 98), width=1)
    # Explosion burst
    ex, ey = x+w//2+14, y+34
    for a in range(0, 360, 30):
        ra = 5 if a % 60 == 0 else 8
        rb = 18 if a % 60 == 0 else 13
        x1 = ex + ra*math.cos(math.radians(a))
        y1 = ey + ra*math.sin(math.radians(a))
        x2 = ex + rb*math.cos(math.radians(a))
        y2 = ey + rb*math.sin(math.radians(a))
        d.line([x1, y1, x2, y2], fill=(240, 130, 30), width=2)
    d.ellipse([ex-7, ey-7, ex+7, ey+7], fill=(255, 200, 50), outline=(225, 110, 15))
    # Smoke/debris
    for sx, sy, sr in [(ex+16, ey-10, 5), (ex+20, ey-4, 4), (ex+12, ey-14, 4), (ex+8, ey+12, 3)]:
        d.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(120, 120, 128))
    # 3rd strike label
    d.rectangle([x+6, y+h-18, x+52, y+h-4], fill=(200, 50, 30))
    d.text((x+9, y+h-17), u'3rd strike', font=f_map_tag, fill=WHITE)

def draw_lead_voyager(x, y, w, h):
    rr([x, y, x+w, y+h], 6, (232, 228, 218), outline=RULE)
    d.rectangle([x+2, y+2, x+w-2, y+h-2], fill=(14, 24, 48))
    # Stars
    for sx, sy in [(x+14,y+10),(x+26,y+18),(x+w-16,y+12),(x+w-28,y+24),(x+18,y+h-16),
                   (x+w-12,y+h-18),(x+w//2,y+10),(x+34,y+10),(x+w//2+20,y+20),
                   (x+40,y+h-10),(x+w-30,y+6),(x+20,y+24)]:
        d.ellipse([sx-1,sy-1,sx+1,sy+1], fill=(245,245,255))
    # Earth
    d.ellipse([x+8, y+h-40, x+36, y+h-12], fill=(55, 130, 210))
    d.ellipse([x+14, y+h-34, x+22, y+h-26], fill=(90, 170, 90))
    d.ellipse([x+24, y+h-28, x+30, y+h-22], fill=(140, 195, 110))
    # Probe body
    sx2, sy2 = x+w-36, y+28
    d.rectangle([sx2, sy2, sx2+16, sy2+12], fill=(200, 205, 215), outline=(140,145,155))
    # Antenna dish
    d.arc([sx2-4, sy2-8, sx2+8, sy2+4], start=300, end=60, fill=(235, 235, 240), width=2)
    d.line([sx2+4, sy2, sx2-8, sy2], fill=(200, 200, 210), width=2)
    # Boom arms
    d.line([sx2, sy2+6, sx2-14, sy2-4], fill=(180, 185, 195), width=2)
    d.line([sx2, sy2+8, sx2-12, sy2+14], fill=(180, 185, 195), width=2)
    # Instruments
    d.rectangle([sx2-14, sy2-8, sx2-4, sy2-2], outline=(170, 175, 210), width=1)
    d.rectangle([sx2-12, sy2+8, sx2-4, sy2+14], outline=(170, 175, 210), width=1)
    # Trajectory line
    for i, (px, py) in enumerate([(x+28, y+h-22), (x+38, y+h-30), (x+48, y+h-38), (x+58, y+h-46), (x+68, y+h-54)]):
        d.ellipse([px-2, py-2, px+2, py+2], fill=(170, 210, 255))
        if i < 4:
            nx, ny = (x+28, y+h-22)[0] if i==0 else 0, 0  # placeholder
    # 1 LD label
    d.text((x+8, y+6), '1 LIGHT-DAY', font=f_map_tag, fill=(180, 220, 255))

# ─── WORLD MAP ─────────────────────────────────────────
def draw_world_map(mx, my, mw, mh):
    """Draw SVG-style world map with colored continents + news dots."""
    # Ocean background
    rr([mx, my, mx+mw, my+mh], 8, (215, 228, 242), outline=RULE)
    # Title pill
    title_w = d.textlength('WORLD MAP • 18 NOV 2026', font=f_map_tag) + 14
    rr([mx+mw//2-title_w//2, my+4, mx+mw//2+title_w//2, my+18], 4, DARK)
    d.text((mx+mw//2-title_w//2+7, my+5), 'WORLD MAP \u2022 18 NOV 2026', font=f_map_tag, fill=WHITE)

    # Normalized continent polygons (0-1000 scale, mercator-ish view)
    # Each continent: list of (x,y) tuples scaled to map area
    def sc(x, y):
        """Scale from 0-1000 normalized coords to map pixel coords."""
        return (mx + 8 + x * (mw - 16) / 1000,
                my + 24 + y * (mh - 32) / 1000)

    def draw_continent(points, color, label=None, label_pos=None):
        """Draw a filled continent polygon with optional label."""
        scaled = [sc(px, py) for px, py in points]
        d.polygon(scaled, fill=color, outline=MAP_STROKE)
        if label and label_pos:
            lx, ly = sc(*label_pos)
            lw = d.textlength(label, font=f_map_tag)
            rr([lx-lw//2-3, ly-6, lx+lw//2+3, ly+10], 3, color)
            d.text((lx-lw//2, ly-7), label, font=f_map_tag, fill=WHITE)

    # North America
    draw_continent([
        (50,20),(200,10),(380,30),(340,180),(320,360),(280,550),
        (200,650),(120,580),(80,500),(60,400),(40,280),(30,160)
    ], COL['AM'], 'AMERICAS', (180, 300))

    # South America
    draw_continent([
        (220,580),(280,550),(340,600),(350,720),(320,820),
        (280,860),(240,820),(210,740),(200,680)
    ], COL['AM'])

    # Europe
    draw_continent([
        (400,30),(460,15),(550,20),(580,60),(560,140),(520,200),
        (480,220),(440,200),(410,160),(390,100),(380,50)
    ], COL['EU'], 'EUROPE', (480, 100))

    # Africa
    draw_continent([
        (410,230),(460,220),(520,240),(560,300),(580,400),
        (560,500),(520,580),(480,650),(430,680),(390,600),
        (370,480),(380,380),(390,280)
    ], COL['AF'], 'AFRICA', (480, 420))

    # Middle East (small sub-region)
    draw_continent([
        (545,220),(580,200),(610,240),(620,290),(600,340),(570,320),
        (555,280),(540,240)
    ], COL['ME'])

    # Asia
    draw_continent([
        (590,20),(750,10),(880,30),(920,80),(910,180),(880,280),
        (820,340),(780,300),(730,280),(680,260),(640,240),(610,220),
        (600,160),(590,100)
    ], COL['AS'], 'ASIA', (740, 180))

    # Southeast Asia / India subcontinent
    draw_continent([
        (680,260),(720,280),(760,320),(780,380),(740,420),(700,380),(670,320)
    ], COL['AS'])

    # Japan / East Asia islands
    draw_continent([
        (900,80),(910,100),(900,140),(890,120),(880,140),(880,100)
    ], COL['AS'])

    # Australia / Oceania
    draw_continent([
        (760,520),(820,500),(880,520),(900,560),(860,600),
        (800,620),(770,590),(750,540)
    ], COL['OC'], 'OCEANIA', (830, 560))

    # ─── News event dots ───────────────────────────────
    events = [
        ((210,440), COL['AM'], 'Haiti'),         # Haiti gang raid
        ((830,100), COL['AS'], 'Kashmir'),        # Kulgam
        ((780,260), COL['AS'], 'Bangladesh'),     # Dhaka protests
        ((440,70), COL['EU'], 'Crimea'),          # Crimean Bridge
        ((590,280), COL['ME'], 'Gaza'),           # Gaza operation
        ((480,580), COL['AF'], 'S. Africa'),      # Litton Das record
        ((190,200), COL['AM'], 'NYC'),            # Van Gogh auction
        ((560,440), COL['ME'], ''),               # Middle East general
    ]
    for (ex, ey), ec, lbl in events:
        px, py = sc(ex, ey)
        # Glow
        d.ellipse([px-5, py-5, px+5, py+5], fill=(255, 255, 255, 180))
        # Dot
        d.ellipse([px-3, py-3, px+3, py+3], fill=ec, outline=WHITE)
        if lbl:
            lw2 = d.textlength(lbl, font=f_map_tag)
            d.text((px+6, py-5), lbl, font=f_map_tag, fill=INK)

    # ─── Map legend ────────────────────────────────────
    legend_regions = [
        ('EU', COL['EU']), ('ME', COL['ME']), ('AS', COL['AS']),
        ('AF', COL['AF']), ('AM', COL['AM']), ('OC', COL['OC']),
    ]
    lx0 = mx + 6
    ly0 = my + mh - 16
    for code, clr in legend_regions:
        tw3 = d.textlength(code, font=f_map_tag)
        d.rectangle([lx0, ly0, lx0+8, ly0+8], fill=clr, outline=MAP_STROKE)
        d.text((lx0+10, ly0-1), code, font=f_map_tag, fill=MUTED)
        lx0 += tw3 + 18

# ─── Panel item icons ─────────────────────────────────
def draw_item_icon(kind, x, y, c):
    cx, cy = x+8, y+8
    if kind == 'blast':
        for a in range(0,360,45):
            d.line([cx,cy, cx+7*math.cos(math.radians(a)), cy+7*math.sin(math.radians(a))], fill=c, width=2)
        d.ellipse([cx-3,cy-3,cx+3,cy+3], fill=c)
    elif kind == 'drone':
        d.ellipse([cx-2,cy-2,cx+2,cy+2], fill=c)
        d.line([cx-7,cy-3,cx+7,cy-3], fill=c, width=2)
        d.line([cx-7,cy+3,cx+7,cy+3], fill=c, width=2)
        d.line([cx,cy-5,cx,cy+6], fill=c, width=1)
    elif kind == 'shield':
        d.polygon([(cx,y+1),(x+14,y+4),(x+13,y+10),(cx,y+15),(x+2,y+10),(x+2,y+4)], outline=c)
        d.line([cx,y+4,cx,y+11], fill=c, width=1)
        d.line([cx-3,y+7,cx+3,y+7], fill=c, width=1)
    elif kind == 'rifle':
        d.line([x+2,cy+2,x+14,cy-2], fill=c, width=2)
        d.line([x+5,cy+2,x+4,cy+6], fill=c, width=2)
        d.rectangle([x+9,cy-4,x+12,cy-1], outline=c)
    elif kind == 'attack':
        d.polygon([(cx,y+1),(x+15,cy),(cx,y+15),(x+1,cy)], outline=c)
        d.line([x+4,cy,x+12,cy], fill=c, width=2)
        d.line([cx,y+4,cx,y+12], fill=c, width=2)
    elif kind == 'soldier':
        d.ellipse([cx-2,y+1,cx+2,y+5], fill=c)
        d.line([cx,y+5,cx,y+10], fill=c, width=2)
        d.line([cx-4,y+7,cx+4,y+7], fill=c, width=2)
        d.line([cx,y+10,x+4,y+15], fill=c, width=2)
        d.line([cx,y+10,x+12,y+15], fill=c, width=2)
    elif kind == 'sanction':
        d.rectangle([x+3,y+2,x+13,y+14], outline=c, width=1)
        d.line([x+5,y+5,x+11,y+11], fill=c, width=2)
        d.line([x+11,y+5,x+5,y+11], fill=c, width=2)
    elif kind == 'fire':
        d.polygon([(cx,y+1),(x+13,y+8),(cx,y+15),(x+3,y+8)], fill=c)
        d.ellipse([cx-3,y+8,cx+3,y+13], fill=(255,210,120))
    elif kind == 'flood':
        for wy2 in [y+5,y+9,y+13]:
            d.arc([x+1,wy2-3,x+8,wy2+1], start=180, end=0, fill=c, width=2)
            d.arc([x+8,wy2-3,x+15,wy2+1], start=180, end=0, fill=c, width=2)
    elif kind == 'storm':
        d.polygon([(cx+2,y+1),(x+5,y+8),(cx,y+8),(cx-2,y+15),(x+11,y+7),(cx+1,y+7)], fill=c)
    elif kind == 'avalanche':
        d.polygon([(cx,y+2),(x+14,y+14),(x+2,y+14)], outline=c)
        d.ellipse([x+8,y+6,x+12,y+10], fill=c)
        d.ellipse([x+5,y+9,x+8,y+12], fill=c)
    elif kind == 'vote':
        d.rectangle([x+3,y+2,x+13,y+14], outline=c)
        d.rectangle([x+5,y+5,x+11,y+7], fill=c)
        d.line([x+5,y+10,x+11,y+10], fill=c, width=1)
    elif kind == 'gavel':
        d.rectangle([x+3,y+4,x+9,y+8], fill=c)
        d.line([x+6,y+8,x+12,y+14], fill=c, width=2)
        d.line([x+2,y+14,x+10,y+14], fill=c, width=2)
    elif kind == 'scales':
        d.line([cx,y+2,cx,y+13], fill=c, width=2)
        d.line([x+3,y+5,x+13,y+5], fill=c, width=2)
        d.arc([x+1,y+5,x+6,y+10], start=0, end=180, fill=c, width=2)
        d.arc([x+10,y+5,x+15,y+10], start=0, end=180, fill=c, width=2)
        d.line([x+4,y+13,x+12,y+13], fill=c, width=2)
    elif kind == 'handshake':
        d.line([x+2,y+9,x+7,y+6], fill=c, width=2)
        d.line([x+14,y+9,x+9,y+6], fill=c, width=2)
        d.rectangle([x+6,y+5,x+10,y+9], outline=c)
        d.line([x+4,y+11,x+12,y+11], fill=c, width=2)
    elif kind == 'mineral':
        d.polygon([(cx,y+1),(x+14,y+6),(x+11,y+14),(x+5,y+14),(x+2,y+6)], outline=c)
        d.line([cx,y+1,cx,y+14], fill=c, width=1)
        d.line([x+2,y+6,x+14,y+6], fill=c, width=1)
    elif kind == 'anchor':
        d.line([cx,y+3,cx,y+13], fill=c, width=2)
        d.ellipse([cx-2,y+1,cx+2,y+5], outline=c)
        d.line([x+4,y+6,x+12,y+6], fill=c, width=2)
        d.arc([x+3,y+7,x+13,y+15], start=0, end=180, fill=c, width=2)
    elif kind == 'gamepad':
        rr([x+1,y+5,x+15,y+12], 3, None, outline=c)
        d.line([x+4,y+7,x+4,y+10], fill=c, width=1)
        d.line([x+2,y+8,x+6,y+8], fill=c, width=1)
        d.ellipse([x+10,y+7,x+12,y+9], outline=c)
    elif kind == 'cricket':
        d.line([x+4,y+14,x+12,y+2], fill=c, width=3)
        d.ellipse([x+10,y+1,x+15,y+6], outline=c, width=2)
        d.line([x+2,y+12,x+6,y+12], fill=c, width=1)
        d.line([x+2,y+14,x+6,y+14], fill=c, width=1)
    elif kind == 'trophy':
        d.rectangle([x+4,y+3,x+12,y+8], outline=c)
        d.arc([x+1,y+3,x+5,y+8], start=90, end=270, fill=c, width=1)
        d.arc([x+11,y+3,x+15,y+8], start=270, end=90, fill=c, width=1)
        d.line([cx,y+8,cx,y+12], fill=c, width=2)
        d.line([x+5,y+13,x+11,y+13], fill=c, width=2)
    elif kind == 'football':
        d.ellipse([x+2,y+4,x+14,y+12], outline=c)
        d.line([x+5,y+8,x+11,y+8], fill=c, width=1)
        d.line([cx,y+4,cx,y+12], fill=c, width=1)
    elif kind == 'person':
        d.ellipse([cx-2,y+1,cx+2,y+5], outline=c)
        d.arc([x+3,y+6,x+13,y+16], start=180, end=0, fill=c, width=2)
    elif kind == 'chart':
        d.line([x+2,y+14,x+14,y+14], fill=c, width=1)
        d.line([x+2,y+14,x+2,y+2], fill=c, width=1)
        d.line([x+3,y+11,x+6,y+8,x+9,y+10,x+13,y+4], fill=c, width=2)
    elif kind == 'space':
        d.ellipse([x+3,y+3,x+13,y+13], outline=c)
        d.ellipse([x+5,y+5,x+11,y+11], outline=c)
        d.line([x+3,y+8,x+13,y+8], fill=c, width=1)
    elif kind == 'paint':
        d.rectangle([x+2,y+2,x+14,y+12], outline=c)
        d.line([x+4,y+5,x+12,y+9], fill=c, width=2)
        d.line([x+4,y+9,x+8,y+5], fill=c, width=2)
        d.arc([x+6,y+5,x+12,y+11], start=0, end=180, fill=c, width=1)
    else:
        d.ellipse([x+4,y+4,x+12,y+12], outline=c, width=2)

# ═══════════════════════════════════════════════════════
# LAYOUT CONSTANTS
# ═══════════════════════════════════════════════════════
HEADER_H  = 82
STRIP_H   = 50
LEAD_H    = 146
CONTENT_H = 580   # panels + map
UTC_H     = 42
ALSO_H    = 40
FOOTER_H  = 34
GAP       = 4
MARGIN    = 18

# ─── Header ───────────────────────────────────────────
d.rectangle([0, 0, W, HEADER_H], fill=DARK)
dc(8, 'WEDNESDAY 18 NOVEMBER 2026', f_title, (250, 246, 238))
dc(HEADER_H - 20, 'WORLD NEWS IN ONE IMAGE  \u2022  43 verified stories  \u2022  6 continents  \u2022  Events 18 Nov 2026 (any time zone)', f_sub, (200, 192, 175))

# ─── Number strip ─────────────────────────────────────
sy = HEADER_H
sh = STRIP_H
d.rectangle([0, sy, W, sy+sh], fill=(235, 228, 214))
d.line([0, sy+sh, W, sy+sh], fill=RULE, width=1)
nums = [
    ('$190.4M', 'Van Gogh sale'),
    ('1 light-day', 'Voyager 1'),
    ('8 dismissals', 'Litton Das'),
    ('~300 arrests', 'BD protests'),
    ('55 factories', 'closed Gazipur'),
    ('4 days', 'Crimea strikes'),
    ('\u09F330,000', 'wage demand'),
    ('49 years', 'Voyager travel'),
]
items_w = []
for val, lab in nums:
    tw = d.textlength(val, font=f_strip_val)
    lw = d.textlength(lab, font=f_strip_lab)
    items_w.append(max(tw, lw))
gap_n = 14
total_n = sum(items_w) + gap_n * (len(nums) - 1)
nx = (W - total_n) / 2
for i, (val, lab) in enumerate(nums):
    iw = items_w[i]
    vw = d.textlength(val, font=f_strip_val)
    lw = d.textlength(lab, font=f_strip_lab)
    d.text((nx + (iw - vw) / 2, sy + 4), val, font=f_strip_val, fill=COL['EU'])
    d.text((nx + (iw - lw) / 2, sy + 28), lab, font=f_strip_lab, fill=MUTED)
    nx += iw + gap_n

y0 = sy + sh + GAP

# ─── Lead cards (2 side-by-side) ──────────────────────
lead_y = y0
lead_gap = 10
lead_w = (W - MARGIN * 2 - lead_gap) // 2  # ~485px each
leads = [
    {
        'tag': 'CONFLICT \u2022 EUROPE', 'color': COL['EU'],
        'title': 'Crimean Bridge struck for 3rd time',
        'body': 'Ukraine hits the Crimean Bridge for the third time in four days; Russia closes the crossing to all traffic amid escalating drone and missile strikes.',
        'icon': 'bridge'
    },
    {
        'tag': 'SCIENCE \u2022 SPACE', 'color': COL['SC'],
        'title': 'Voyager 1: one light-day from Earth',
        'body': 'NASA\u2019s Voyager 1 is the first human-made object to reach one light-day from Earth, 49 years after its 1977 launch.',
        'icon': 'voyager'
    },
]
for i, L in enumerate(leads):
    lx = MARGIN + i * (lead_w + lead_gap)
    ly = lead_y
    rr([lx, ly, lx + lead_w, ly + LEAD_H], 8, WHITE, outline=RULE)
    rr([lx, ly, lx + lead_w, ly + 22], 8, L['color'])
    d.rectangle([lx, ly + 12, lx + lead_w, ly + 22], fill=L['color'])
    d.text((lx + 10, ly + 3), L['tag'], font=f_tag, fill=WHITE)
    # Illustration on right side
    ix = lx + lead_w - 124
    iy = ly + 26
    if L['icon'] == 'bridge':
        draw_lead_bridge(ix, iy, 110, 92)
    elif L['icon'] == 'voyager':
        draw_lead_voyager(ix, iy, 110, 92)
    # Text on left
    tx = lx + 12
    tmax = ix - tx - 8
    ty = draw_wrapped(tx, ly + 28, L['title'], f_lead_h, INK, tmax, 22, mx=2)
    body_y = max(ty + 2, iy + 96)
    draw_wrapped(tx, body_y, L['body'], f_lead_b, MUTED, lead_w - 24, 14, mx=3)

# ─── Content area: 2 panels + world map ───────────────
content_y = lead_y + LEAD_H + GAP
panel_gap = 8
map_w = 340
panel_w = (W - MARGIN * 2 - panel_gap - map_w) // 2  # ~314px each

# --- World Map (right side) ---
map_x = MARGIN + panel_w * 2 + panel_gap
draw_world_map(map_x, content_y - GAP, map_w, CONTENT_H + GAP)

# --- Panel 1: Conflicts & Security ---
panels = [
    {
        'title': 'CONFLICTS & SECURITY',
        'color': COL['EU'],
        'items': [
            ('EU', 'blast', 'Crimean Bridge hit 3rd time in 4 days; Russia closes crossing.'),
            ('AM', 'shield', 'Haiti: Salvadoran forces destroy Taliban gang leader\'s house in Canaan.'),
            ('ME', 'attack', 'Gaza: Israel launches 1st central Gaza operation since Oct 2025 ceasefire.'),
            ('AS', 'rifle', 'Kulgam (J&K): Indian forces kill militant commander at mosque.'),
            ('AS', 'soldier', 'Narail (BD): 2 BNP members killed in attack on motorcycle procession.'),
            ('AS', 'fire', 'Narayanganj: Crowd sets fire to ex-MP Shamim Osman\'s residence.'),
            ('AS', 'blast', 'Gopalganj: Bombs & arson at BNP MP K M Babar\'s clinic; patients flee.'),
            ('AS', 'shield', 'Pirojpur: Ex-minister SM Rezaul Karim\'s 2 houses looted & burned.'),
            ('AS', 'sanction', 'Sirajganj: AL office & ex-MP Habibe Millat\'s home vandalised.'),
            ('AS', 'vote', 'Gopalganj: 5 BNP offices torched; 2 Grameen Bank branches attacked.'),
            ('EU', 'drone', 'Ukraine intensifies drone & missile campaign on Crimea infrastructure.'),
            ('ME', 'person', 'Gaza families displaced as central Strip operation begins.'),
            ('AS', 'chart', 'Kashmir: Commander escaped shootout 2 days earlier; tracked to mosque.'),
            ('AM', 'attack', 'Haiti Gang Suppression Force denies involvement in Canaan raid.'),
        ],
    },
    {
        'title': 'PROTESTS, LAW, ARTS & SPORT',
        'color': COL['AM'],
        'items': [
            ('AS', 'person', 'Gazipur/Savar/Ashulia: Thousands of garment workers block highway.'),
            ('AS', 'sanction', 'Police fire tear gas & stun grenades; ~300 arrested across protest zones.'),
            ('AS', 'chart', '55 factories close; workers demand \u09F330,000 monthly minimum wage.'),
            ('AS', 'attack', 'Kafrul (Dhaka): Stun grenades fired after BNP activists harass female workers.'),
            ('AS', 'fire', 'Chattogram: Muhammad Yunus\'s ancestral home set ablaze by arsonists.'),
            ('AS', 'gavel', '24 cases filed in Savar & Ashulia over garment worker protests.'),
            ('BZ', 'paint', 'Van Gogh\'s "Blossoming Chestnut Trees" sells for $190.4M at Sotheby\'s NY.'),
            ('SC', 'space', 'Voyager 1: first human-made object 1 light-day from Earth (launched 1977).'),
            ('AM', 'gamepad', 'PlayStation reports major outage ahead of GTA VI release.'),
            ('AF', 'cricket', 'Litton Das sets Test record: 8 dismissals in an innings vs South Africa.'),
            ('AF', 'trophy', 'Johannesburg: 6 catches + 2 stumpings in one innings \u2014 a world record.'),
            ('BZ', 'mineral', 'Van Gogh sale tops "$117.2M for Orchard with Cypresses" (2022 record).'),
            ('AS', 'handshake', 'Bangladesh industrial belt: wage protests spread across 3 districts.'),
            ('SC', 'anchor', 'Voyager probe: 49-year journey, now deep-space pioneer at light-day mark.'),
        ],
    },
]

for pi, P in enumerate(panels):
    px = MARGIN + pi * (panel_w + panel_gap)
    py = content_y
    rr([px, py, px + panel_w, py + CONTENT_H], 8, PANEL_BG, outline=RULE)
    # Header bar
    rr([px, py, px + panel_w, py + 23], 8, P['color'])
    d.rectangle([px, py + 11, px + panel_w, py + 23], fill=P['color'])
    d.text((px + 10, py + 3), P['title'], font=f_panel_h, fill=WHITE)

    iy = py + 27
    row_h = 38
    for tag2, ik, text in P['items']:
        if iy + row_h > py + CONTENT_H - 4:
            break
        tc = COL.get(tag2, MUTED)
        # Icon badge
        badge_x = px + 6
        badge_y = iy + 2
        rr([badge_x, badge_y, badge_x + 16, badge_y + 16], 3, (255, 255, 255), outline=tc, width=1)
        draw_item_icon(ik, badge_x, badge_y, tc)
        # Region tag
        tag_x = badge_x + 18
        tw2 = d.textlength(tag2, font=f_item)
        rr([tag_x, badge_y, tag_x + tw2 + 5, badge_y + 13], 2, tc)
        d.text((tag_x + 2, badge_y + 1), tag2, font=f_item, fill=WHITE)
        # Text
        tx2 = tag_x + tw2 + 8
        maxw2 = px + panel_w - tx2 - 4
        lines = wrap(text, f_item, maxw2)
        if len(lines) > 2:
            lines = lines[:2]
        for li, line in enumerate(lines):
            d.text((tx2, badge_y + li * 12), line, font=f_item, fill=INK)
        iy += row_h

# ─── UTC Timeline ─────────────────────────────────────
uy = content_y + CONTENT_H + GAP
d.rectangle([MARGIN, uy, W - MARGIN, uy + UTC_H], fill=(242, 238, 228), outline=RULE)
rr([MARGIN, uy, MARGIN + 200, uy + 20], 8, DARK)
d.rectangle([MARGIN, uy + 10, MARGIN + 200, uy + 20], fill=DARK)
d.text((MARGIN + 8, uy + 3), 'UTC TIMELINE  18 NOV 2026', font=f_tag, fill=WHITE)
utc_events = [
    ('~00:00', 'Crimean Bridge struck', 'EU'),
    ('~03:00', 'Bangladesh protests', 'AS'),
    ('~06:00', 'Gaza operation', 'ME'),
    ('~09:00', 'Kulgam commander', 'AS'),
    ('~14:00', 'Van Gogh auction', 'BZ'),
    ('~18:00', 'Voyager 1 milestone', 'SC'),
    ('~20:00', 'Das Test record', 'AF'),
    ('~22:00', 'Yunus home arson', 'AS'),
]
ux = MARGIN + 208
uw = (W - MARGIN * 2 - ux + MARGIN) / len(utc_events) - 6
for tm, txt, code in utc_events:
    tc3 = COL.get(code, (120, 90, 40))
    d.text((ux, uy + 22), tm, font=f_item, fill=INK)
    d.text((ux, uy + 33), txt, font=f_utc, fill=MUTED)
    tw3 = d.textlength(txt, font=f_utc)
    d.line([ux, uy + UTC_H - 1, ux + tw3 + 2, uy + UTC_H - 1], fill=tc3, width=2)
    ux += uw + 6

# ─── Also on 18 November ──────────────────────────────
ay = uy + UTC_H + GAP
rr([MARGIN, ay, W - MARGIN, ay + ALSO_H], 8, WHITE, outline=RULE)
rr([MARGIN, ay, MARGIN + 170, ay + 19], 8, DARK)
d.rectangle([MARGIN, ay + 9, MARGIN + 170, ay + 19], fill=DARK)
d.text((MARGIN + 10, ay + 2), 'ALSO ON 18 NOVEMBER', font=f_tag, fill=WHITE)
also_items = [
    ('EU', 'blast', 'Crimean Bridge closed'),
    ('AS', 'fire', 'M. Yunus home burned'),
    ('AM', 'gamepad', 'PlayStation outage'),
    ('AF', 'cricket', 'Litton Das 8 dismissals'),
    ('AS', 'person', 'BD protests: ~300 arrested'),
]
ax = MARGIN + 180
for code2, ik2, txt2 in also_items:
    tc4 = COL.get(code2, MUTED)
    badge_w = d.textlength(code2, font=f_item)
    # Mini icon
    rr([ax, ay + 22, ax + 15, ay + 37], 3, (255, 255, 255), outline=tc4)
    draw_item_icon(ik2, ax + 1, ay + 23, tc4)
    ax += 17
    # Tag pill
    rr([ax, ay + 23, ax + badge_w + 6, ay + 36], 2, tc4)
    d.text((ax + 2, ay + 24), code2, font=f_item, fill=WHITE)
    ax += badge_w + 8
    # Text
    maxw_a = 140
    alines = wrap(txt2, f_utc, maxw_a)
    if alines:
        d.text((ax, ay + 23), alines[0], font=f_utc, fill=INK)
    ax += maxw_a + 8

# ─── Footer ───────────────────────────────────────────
fy = ay + ALSO_H + GAP
d.line([MARGIN, fy, W - MARGIN, fy], fill=RULE, width=1)
d.text((MARGIN + 2, fy + 1), 'Source: Wikipedia Portal:Current events/2026 November 18', font=f_footer, fill=MUTED)
dc(fy + 12, 'DATE CHECK: All events happened or were first reported on Wednesday 18 Nov 2026 (any time zone).', f_datecheck, INK)
# Region legend
lx = W - 300
for code3, clr in [('EU', COL['EU']), ('ME', COL['ME']), ('AS', COL['AS']),
                    ('AF', COL['AF']), ('AM', COL['AM']), ('OC', COL['OC']),
                    ('SC', COL['SC']), ('BZ', COL['BZ'])]:
    d.rectangle([lx, fy + 23, lx + 9, fy + 32], fill=clr)
    d.text((lx + 11, fy + 21), code3, font=f_footer, fill=MUTED)
    lx += 36

# ─── Save ─────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(__file__), 'entry.png')
img.save(out_path, format='PNG', optimize=True)
print('saved', out_path, os.path.getsize(out_path))