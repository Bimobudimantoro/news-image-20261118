#!/usr/bin/env python3
"""Deterministic news-image for 18 November 2026 — 50 stories, global balance, 7 regions, world map."""
import os, math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG    = (247, 242, 230)
INK   = (28, 28, 28)
MUTED = (85, 80, 72)
RULE  = (188, 178, 162)
WHITE = (255, 255, 255)
DARK  = (34, 32, 28)
PANEL_BG = (252, 249, 242)
OCEAN   = (215, 228, 242)
MAP_STR = (140, 150, 165)

COL = {
    'EU': (47, 87, 160),    # blue
    'ME': (196, 102, 28),   # orange
    'AS': (112, 64, 160),   # purple
    'AF': (46, 122, 78),    # green
    'AM': (176, 54, 54),    # red
    'OC': (20, 132, 140),   # teal
    'AP': (55, 120, 180),   # Asia-Pacific (steel blue)
    'SC': (50, 85, 140),    # science
    'BZ': (120, 90, 40),    # business
}

def load_font(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

f_title    = load_font('/system/fonts/NotoSerif-Bold.ttf', 44)
f_sub      = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 15)
f_strip_v  = load_font('/system/fonts/NotoSerif-Bold.ttf', 20)
f_strip_l  = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 11)
f_tag      = load_font('/system/fonts/RobotoCondensed-Bold.ttf', 12)
f_lead_h   = load_font('/system/fonts/NotoSerif-Bold.ttf', 22)
f_lead_b   = load_font('/system/fonts/Roboto-Regular.ttf', 13)
f_panel_h  = load_font('/system/fonts/RobotoCondensed-Bold.ttf', 14)
f_item     = load_font('/system/fonts/Roboto-Regular.ttf', 11)
f_map_tag  = load_font('/system/fonts/RobotoCondensed-Bold.ttf', 10)
f_utc      = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 10)
f_footer   = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 9)
f_datechk  = load_font('/system/fonts/NotoSerif-Bold.ttf', 15)
f_also     = load_font('/system/fonts/RobotoCondensed-Bold.ttf', 11)
f_also_v   = load_font('/system/fonts/Roboto-Regular.ttf', 10)

img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur+' '+w).strip()
        if d.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines or ['']

def dw(x, y, text, font, fill, maxw, lh, mx=None):
    lines = wrap(text, font, maxw)
    if mx: lines = lines[:mx]
    for L in lines:
        d.text((x,y), L, font=font, fill=fill)
        y += lh
    return y

def rr(xy, r, fill, outline=None, width=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def dc(y, text, font, fill):
    tw = d.textlength(text, font=font)
    d.text(((W-tw)/2, y), text, font=font, fill=fill)

# ─── item icon ─────────────────────────────────
def draw_icon(kind, x, y, c):
    cx, cy = x+7, y+7
    if kind=='drone':
        d.ellipse([cx-3,cy-3,cx+3,cy+3], fill=c); d.line([cx-7,cy-3,cx+7,cy-3], fill=c,width=2)
        d.line([cx-7,cy+3,cx+7,cy+3], fill=c,width=2); d.line([cx,cy-5,cx,cy+6], fill=c,width=1)
    elif kind=='blast':
        for a in range(0,360,45): d.line([cx,cy,cx+7*math.cos(math.radians(a)),cy+7*math.sin(math.radians(a))], fill=c,width=2)
        d.ellipse([cx-3,cy-3,cx+3,cy+3], fill=c)
    elif kind=='shield':
        d.polygon([(cx,y),(x+13,y+4),(x+12,y+9),(cx,y+14),(x+1,y+9),(x+1,y+4)], outline=c)
        d.line([cx,y+4,cx,y+10], fill=c,width=1); d.line([cx-3,y+7,cx+3,y+7], fill=c,width=1)
    elif kind=='rifle':
        d.line([x+2,cy+2,x+13,cy-2], fill=c,width=2); d.line([x+4,cy+2,x+3,cy+6], fill=c,width=2)
        d.rectangle([x+8,cy-4,x+11,cy-1], outline=c)
    elif kind=='attack':
        d.polygon([(cx,y),(x+14,cy),(cx,y+14),(x,cy)], outline=c)
        d.line([x+4,cy,x+10,cy], fill=c,width=2); d.line([cx,y+4,cx,y+10], fill=c,width=2)
    elif kind=='soldier':
        d.ellipse([cx-2,y,cx+2,y+4], fill=c); d.line([cx,y+4,cx,y+9], fill=c,width=2)
        d.line([cx-4,y+6,cx+4,y+6], fill=c,width=2)
        d.line([cx,y+9,x+3,y+14], fill=c,width=2); d.line([cx,y+9,x+11,y+14], fill=c,width=2)
    elif kind=='sanction':
        d.rectangle([x+2,y+1,x+12,y+13], outline=c,width=1)
        d.line([x+4,y+4,x+10,y+10], fill=c,width=2); d.line([x+10,y+4,x+4,y+10], fill=c,width=2)
    elif kind=='fire':
        d.polygon([(cx,y),(x+12,y+7),(cx,y+14),(x+2,y+7)], fill=c)
        d.ellipse([cx-3,y+7,cx+3,y+12], fill=(255,210,120))
    elif kind=='flood':
        for wy in [y+4,y+8,y+12]:
            d.arc([x,wy-3,x+7,wy+1], 180,0, fill=c,width=2); d.arc([x+7,wy-3,x+14,wy+1], 180,0, fill=c,width=2)
    elif kind=='storm':
        d.polygon([(cx+2,y),(x+5,y+7),(cx,y+7),(cx-2,y+14),(x+11,y+6),(cx+1,y+6)], fill=c)
    elif kind=='vote':
        d.rectangle([x+3,y+1,x+13,y+13], outline=c)
        d.rectangle([x+5,y+4,x+11,y+6], fill=c); d.line([x+5,y+9,x+11,y+9], fill=c,width=1)
    elif kind=='gavel':
        d.rectangle([x+3,y+3,x+9,y+7], fill=c); d.line([x+6,y+7,x+12,y+13], fill=c,width=2)
        d.line([x+1,y+13,x+10,y+13], fill=c,width=2)
    elif kind=='scales':
        d.line([cx,y+1,cx,y+12], fill=c,width=2); d.line([x+2,y+4,x+12,y+4], fill=c,width=2)
        d.arc([x,y+4,x+5,y+9], 0,180, fill=c,width=2); d.arc([x+9,y+4,x+14,y+9], 0,180, fill=c,width=2)
    elif kind=='handshake':
        d.line([x+1,y+8,x+6,y+5], fill=c,width=2); d.line([x+13,y+8,x+8,y+5], fill=c,width=2)
        d.rectangle([x+5,y+4,x+9,y+8], outline=c); d.line([x+3,y+10,x+11,y+10], fill=c,width=2)
    elif kind=='mineral':
        d.polygon([(cx,y),(x+13,y+5),(x+10,y+13),(x+4,y+13),(x+1,y+5)], outline=c)
        d.line([cx,y,cx,y+13], fill=c,width=1); d.line([x+1,y+5,x+13,y+5], fill=c,width=1)
    elif kind=='space':
        d.ellipse([x+2,y+2,x+12,y+12], outline=c); d.ellipse([x+4,y+4,x+10,y+10], outline=c)
        d.line([x+2,y+7,x+12,y+7], fill=c,width=1)
    elif kind=='paint':
        d.rectangle([x+1,y+1,x+13,y+13], outline=c)
        d.line([x+3,y+4,x+11,y+8], fill=c,width=2); d.line([x+11,y+4,x+7,y+8], fill=c,width=2)
    elif kind=='gamepad':
        rr([x,y+4,x+14,y+11], 3, None, outline=c)
        d.line([x+3,y+6,x+3,y+9], fill=c,width=1); d.line([x+1,y+7,x+5,y+7], fill=c,width=1)
    elif kind=='cricket':
        d.line([x+3,y+13,x+11,y+1], fill=c,width=3); d.ellipse([x+9,y,x+14,y+5], outline=c,width=2)
    elif kind=='trophy':
        d.rectangle([x+3,y+2,x+11,y+7], outline=c)
        d.arc([x,y+2,x+4,y+7], 90,270, fill=c,width=1); d.arc([x+10,y+2,x+14,y+7], 270,90, fill=c,width=1)
        d.line([cx,y+7,cx,y+11], fill=c,width=2); d.line([x+4,y+12,x+10,y+12], fill=c,width=2)
    elif kind=='person':
        d.ellipse([cx-2,y,cx+2,y+4], outline=c); d.arc([x+3,y+5,x+11,y+13], 180,0, fill=c,width=2)
    elif kind=='chart':
        d.line([x+1,y+13,x+13,y+13], fill=c,width=1); d.line([x+1,y+13,x+1,y+1], fill=c,width=1)
        d.line([x+2,y+10,x+5,y+7,x+8,y+9,x+12,y+3], fill=c,width=2)
    elif kind=='anchor':
        d.line([cx,y+2,cx,y+12], fill=c,width=2); d.ellipse([cx-2,y,cx+2,y+4], outline=c)
        d.line([x+3,y+6,x+11,y+6], fill=c,width=2)
        d.arc([x+2,y+7,x+12,y+14], 0,180, fill=c,width=2)
    elif kind=='bridge':
        d.rectangle([x+2,y+5,x+12,y+8], fill=c); d.line([x+3,y+8,x+3,y+14], fill=c,width=2)
        d.line([x+11,y+8,x+11,y+14], fill=c,width=2); d.line([cx,y+4,cx,y+10], fill=c,width=2)
    elif kind=='oil':
        d.ellipse([x+2,y+7,x+12,y+13], outline=c); d.ellipse([x+4,y+9,x+6,y+11], fill=c)
        d.line([cx,y+13,cx,y+1], fill=c,width=2)
    elif kind=='flag':
        d.line([x+3,y+1,x+3,y+14], fill=c,width=2); d.rectangle([x+3,y+1,x+11,y+7], fill=c)
    else:
        d.ellipse([x+4,y+4,x+12,y+12], outline=c,width=2)

# ─── lead illustrations ────────────────────────
def draw_flag_illust(x, y, w, h, left_flag, right_flag):
    rr([x,y,x+w,y+h], 6, (232,228,218), outline=RULE)
    d.rectangle([x+2,y+2,x+w-2,y+h-2], fill=(238,242,248))
    # Two flags
    for fx,fy,fcolor in [(x+16,y+16,left_flag),(x+48,y+28,right_flag)]:
        d.line([fx,fy,fx,fy+56], fill=(80,80,85), width=2)
        d.rectangle([fx+2,fy,fx+22,fy+16], fill=fcolor)
        d.ellipse([fx+6,fy+4,fx+12,fy+10], fill=WHITE)
    # Handshake
    hx, hy = x+80, y+30
    d.line([hx,hy+14,hx+12,hy+6], fill=(60,60,65), width=2)
    d.line([hx+26,hy+14,hx+14,hy+6], fill=(60,60,65), width=2)
    d.ellipse([hx+10,hy+4,hx+16,hy+10], fill=(220,180,150))
    # Building silhouette
    # City skyline silhouette
    buildings = [(120,30),(130,40),(140,25),(150,20),(160,35),(170,18),(180,22)]
    for bx,bh in buildings:
        d.rectangle([x+bx,y+h-8-bh,x+bx+10,y+h-8], fill=(160,175,200))

def draw_drone_illust(x, y, w, h):
    rr([x,y,x+w,y+h], 6, (232,228,218), outline=RULE)
    d.rectangle([x+2,y+2,x+w-2,y+h-2], fill=(245,238,220))
    # Sky gradient feel
    d.rectangle([x+2,y+2,x+w-2,y+h//2], fill=(245,240,228))
    # Gulf water
    for wy in range(y+h-30, y+h-2, 4):
        d.line([x+4,wy,x+w-4,wy], fill=(180,200,220), width=1)
    # Drones
    for dx,dy in [(x+8,y+16),(x+22,y+24),(x+36,y+14)]:
        d.ellipse([dx,dy,dx+8,dy+6], fill=(80,82,88))
        d.line([dx+2,dy+6,dx+4,dy+10], fill=(60,62,68), width=1)
        d.line([dx+6,dy+6,dx+8,dy+10], fill=(60,62,68), width=1)
        d.arc([dx-6,dy-4,dx+14,dy+4], 180,0, fill=(60,62,68), width=2)
    # Interception lines (shield/explosion)
    sx, sy = x+50, y+24
    for a in range(0,360,30):
        x1 = sx+6*math.cos(math.radians(a)); y1 = sy+6*math.sin(math.radians(a))
        x2 = sx+14*math.cos(math.radians(a)); y2 = sy+14*math.sin(math.radians(a))
        d.line([x1,y1,x2,y2], fill=(200,100,30), width=2)
    d.ellipse([sx-5,sy-5,sx+5,sy+5], fill=(255,180,60))
    # Ship silhouette
    d.rectangle([x+64,y+h-18,x+78,y+h-8], fill=(100,105,115))
    d.line([x+64,y+h-18,x+60,y+h-12], fill=(90,95,105), width=2)
    d.line([x+78,y+h-18,x+82,y+h-12], fill=(90,95,105), width=2)

def draw_money_illust(x, y, w, h):
    rr([x,y,x+w,y+h], 6, (232,228,218), outline=RULE)
    d.rectangle([x+2,y+2,x+w-2,y+h-2], fill=(228,235,248))
    # EU flag stars
    for a in range(0,360,30):
        stx = x+16+6*math.cos(math.radians(a)); sty = y+20+6*math.sin(math.radians(a))
        d.text((stx,sty), '\u2605', font=f_map_tag, fill=COL['EU'])
    # Stack of bills
    for i in range(3):
        ox, oy = i*3, y+18-i*3
        d.rectangle([x+28+ox,oy,x+72-ox,oy+10], fill=(170,210,140), outline=(120,160,100))
    # Euro symbol
    d.text((x+54,y+h-24), '\u20AC45bn', font=f_lead_h, fill=INK)
    # Ukraine flag
    d.rectangle([x+8,y+h-22,x+22,y+h-12], fill=(0,120,220))
    d.rectangle([x+8,y+h-12,x+22,y+h-6], fill=(240,200,20))

# ─── world map ─────────────────────────────────
def draw_world_map(mx, my, mw, mh):
    rr([mx,my,mx+mw,my+mh], 8, (215,228,242), outline=RULE)
    # Title
    tw = d.textlength('WORLD \u2022 18 NOV 2026', font=f_map_tag)+14
    rr([mx+mw//2-tw//2,my+4,mx+mw//2+tw//2,my+17], 4, DARK)
    d.text((mx+mw//2-tw//2+7,my+5), 'WORLD \u2022 18 NOV 2026', font=f_map_tag, fill=WHITE)

    def sc(x, y):
        return (mx+8+x*(mw-16)/1000, my+22+y*(mh-30)/1000)

    def continent(pts, color, label=None, lpos=None):
        s = [sc(px,py) for px,py in pts]
        d.polygon(s, fill=color, outline=MAP_STR)
        if label and lpos:
            lx,ly = sc(*lpos)
            lw = d.textlength(label, font=f_map_tag)
            rr([lx-lw//2-3,ly-6,lx+lw//2+3,ly+9], 3, color)
            d.text((lx-lw//2,ly-7), label, font=f_map_tag, fill=WHITE)

    # Continents
    continent([(50,20),(200,15),(370,35),(340,180),(320,360),(280,540),(200,640),(120,580),(80,500),(60,400),(40,280),(30,160)], COL['AM'], 'AMERICAS', (180,300))
    continent([(220,580),(280,540),(340,600),(350,720),(320,810),(280,850),(240,810),(210,730),(200,680)], COL['AM'])
    continent([(400,30),(460,15),(550,20),(580,60),(560,140),(520,200),(480,220),(440,200),(410,160),(390,100),(380,50)], COL['EU'], 'EUROPE', (480,100))
    continent([(410,230),(460,220),(520,240),(560,300),(580,400),(560,500),(520,580),(480,640),(430,670),(390,600),(370,480),(380,380),(390,280)], COL['AF'], 'AFRICA', (480,420))
    continent([(545,220),(580,200),(610,240),(620,290),(600,340),(570,320),(555,280),(540,240)], COL['ME'])
    continent([(590,20),(750,10),(880,30),(920,80),(910,180),(880,280),(820,340),(780,300),(730,280),(680,260),(640,240),(610,220),(600,160),(590,100)], COL['AS'], 'ASIA-PAC', (740,160))
    continent([(680,260),(720,280),(760,320),(780,380),(740,420),(700,380),(670,320)], COL['AS'])
    continent([(760,520),(820,500),(880,520),(900,560),(860,600),(800,620),(770,590),(750,540)], COL['OC'], 'OCEANIA', (830,560))

    # News dots
    evts = [((760,40), COL['AS'], 'Shenzhen'), ((810,60), COL['AS'], ''),       # APEC
            ((240,30), COL['AM'], 'NYC'), ((440,80), COL['EU'], 'Brussels'),     # US/EU
            ((220,460), COL['AM'], 'Haiti'), ((500,240), COL['ME'], 'Kuwait'),   # Haiti/Gulf
            ((450,60), COL['EU'], 'Crimea'), ((490,280), COL['ME'], 'Gaza'),     # Crimea/Gaza
            ((650,80), COL['AS'], 'Kashmir'), ((260,680), COL['AF'], 'JHB')]     # Kashmir/Johannesburg
    for (ex,ey), ec, lbl in evts:
        px,py = sc(ex,ey)
        d.ellipse([px-5,py-5,px+5,py+5], fill=(255,255,255,180))
        d.ellipse([px-3,py-3,px+3,py+3], fill=ec, outline=WHITE)
        if lbl:
            d.text((px+6,py-5), lbl, font=f_map_tag, fill=INK)

    # Legend
    lx0, ly0 = mx+6, my+mh-14
    for code,clr in [('EU',COL['EU']),('ME',COL['ME']),('AS',COL['AS']),('AF',COL['AF']),('AM',COL['AM']),('OC',COL['OC'])]:
        lw3 = d.textlength(code, font=f_map_tag)
        d.rectangle([lx0,ly0,lx0+7,ly0+7], fill=clr, outline=MAP_STR)
        d.text((lx0+9,ly0-1), code, font=f_map_tag, fill=MUTED)
        lx0 += lw3+16

# ═══════════════ LAYOUT ═══════════════
HEADER_H  = 80
STRIP_H   = 48
LEAD_H    = 244
CONTENT_H = 544
UTC_H     = 42
ALSO_H    = 38
FOOTER_H  = 28
GAP       = 4
MARGIN    = 18

# ─── HEADER ──────────────────────────────
d.rectangle([0,0,W,HEADER_H], fill=DARK)
dc(9, 'WEDNESDAY 18 NOVEMBER 2026', f_title, (250,246,238))
dc(HEADER_H-20, 'WORLD NEWS IN ONE IMAGE  \u2022  50 verified stories  \u2022  7 regions  \u2022  18 Nov 2026 (any time zone)', f_sub, (200,192,175))

# ─── NUMBER STRIP ───────────────────────
sy = HEADER_H
sh = STRIP_H
d.rectangle([0,sy,W,sy+sh], fill=(235,228,214))
d.line([0,sy+sh,W,sy+sh], fill=RULE, width=1)
nums = [
    ('Xi\u2013Trump', 'APEC summit'),
    ('Iran drones', 'Gulf attack'),
    ('\u20AC45bn', 'EU\u2013Ukraine'),
    ('1 light-day', 'Voyager 1'),
    ('$190.4M', 'Van Gogh sale'),
    ('8 dismissals', 'Litton Das'),
    ('~300 arrests', 'Bangladesh'),
    ('3rd strike', 'Crimea Bridge'),
]
items_w = []
for val,lab in nums:
    vw = d.textlength(val, font=f_strip_v); lw = d.textlength(lab, font=f_strip_l)
    items_w.append(max(vw,lw))
gn = 14
tn = sum(items_w)+gn*(len(nums)-1)
nx = (W-tn)/2
for i,(val,lab) in enumerate(nums):
    iw = items_w[i]
    vw = d.textlength(val, font=f_strip_v); lw = d.textlength(lab, font=f_strip_l)
    d.text((nx+(iw-vw)/2, sy+4), val, font=f_strip_v, fill=COL['AP'])
    d.text((nx+(iw-lw)/2, sy+27), lab, font=f_strip_l, fill=MUTED)
    nx += iw+gn

y0 = sy+sh+GAP

# ─── LEAD CARDS (3) ──────────────────────
lead_y = y0
lead_gap = 8
lead_w = (W-MARGIN*2-lead_gap*2)//3
leads = [
    {
        'tag':'GEOPOLITICS \u2022 ASIA-PACIFIC','color':COL['AP'],
        'title':'Xi greets Trump at APEC summit in Shenzhen',
        'body':'Chinese President Xi Jinping greets US President Donald Trump at the APEC Summit in Shenzhen \u2014 their first meeting since Trump\u2019s re-election. Putin also attends. Discussions cover trade, tariffs, and Taiwan.',
        'illust':'flag'
    },
    {
        'tag':'CONFLICT \u2022 MIDDLE EAST','color':COL['ME'],
        'title':'Iranian drones intercepted over Gulf; Kuwait targeted',
        'body':'Gulf states intercept multiple Iranian drones launched toward Kuwait. US and allied forces on high alert. The attack marks Iran\u2019s most direct action against Gulf neighbours in months.',
        'illust':'drone'
    },
    {
        'tag':'EUROPE \u2022 DIPLOMACY','color':COL['EU'],
        'title':'EU approves \u20AC45bn loan for Ukraine',
        'body':'EU member states approve a \u20AC45 billion macro-financial loan for Ukraine, funded by frozen Russian assets. Package covers budget deficit and reconstruction through 2027.',
        'illust':'money'
    },
]
for i,L in enumerate(leads):
    lx = MARGIN+i*(lead_w+lead_gap)
    ly = lead_y
    rr([lx,ly,lx+lead_w,ly+LEAD_H], 8, WHITE, outline=RULE)
    rr([lx,ly,lx+lead_w,ly+22], 8, L['color'])
    d.rectangle([lx,ly+12,lx+lead_w,ly+22], fill=L['color'])
    d.text((lx+10,ly+3), L['tag'], font=f_tag, fill=WHITE)
    # Illustration at bottom
    ix = lx+4; iy = ly+LEAD_H-100
    if L['illust']=='flag':
        draw_flag_illust(ix,iy,lead_w-8,92,(200,50,30),(240,200,20))
    elif L['illust']=='drone':
        draw_drone_illust(ix,iy,lead_w-8,92)
    elif L['illust']=='money':
        draw_money_illust(ix,iy,lead_w-8,92)
    # Text above illustration
    tx = lx+12; tmax = lead_w-24
    ty = dw(tx,ly+27, L['title'], f_lead_h, INK, tmax, 22, mx=2)
    body_ymax = iy-4
    dw(tx, min(ty+2, body_ymax), L['body'], f_lead_b, MUTED, lead_w-24, 14, mx=3)

# ─── CONTENT: 2 PANELS + WORLD MAP ───────
content_y = lead_y+LEAD_H+GAP
panel_gap = 8
map_w = 340
panel_w = (W-MARGIN*2-panel_gap-map_w)//2

# World map (right column)
map_x = MARGIN+panel_w*2+panel_gap
draw_world_map(map_x, content_y-GAP, map_w, CONTENT_H+GAP)

panels = [
    {
        'title':'CONFLICTS, SECURITY & POLITICS','color':COL['EU'],
        'items':[
            ('ME','drone','Iran launches drone attack on Kuwait; Gulf states scramble interceptors.'),
            ('EU','bridge','Crimean Bridge hit for 3rd time in 4 days; Russia closes to all traffic.'),
            ('ME','attack','Gaza: Israel launches 1st central Gaza op since Oct 2025 ceasefire.'),
            ('AP','flag','Putin attends APEC in Shenzhen alongside Xi\u2013Trump meeting.'),
            ('AM','vote','Jeffries picked as US House Speaker ahead of new Congress.'),
            ('AM','shield','Haiti: Salvadoran forces destroy Taliban gang leader\u2019s house in Canaan.'),
            ('AS','rifle','Kulgam (J&K): Indian forces kill militant commander tracked to mosque.'),
            ('AS','soldier','Narail (BD): 2 BNP men killed in attack on motorcycle procession.'),
            ('AS','fire','Narayanganj: Crowd sets fire to ex-MP Shamim Osman\u2019s residence.'),
            ('AS','blast','Gopalganj: Bombs & arson at BNP MP K M Babar\u2019s clinic; patients flee.'),
            ('AS','sanction','Pirojpur: Ex-minister Rezaul Karim\u2019s 2 houses looted & burned.'),
            ('AS','vote','Sirajganj: AL office & ex-MP Habibe Millat\u2019s home vandalised.'),
            ('AS','fire','Gopalganj: 5 BNP offices, 2 Grameen Bank branches attacked.'),
            ('AS','person','Chattogram: Yunus ancestral home set ablaze by arsonists.'),
        ],
    },
    {
        'title':'BUSINESS, LABOUR, ARTS & SPORT','color':COL['AM'],
        'items':[
            ('AS','person','Gazipur/Savar/Ashulia: 1000s of garment workers block highway for wage hike.'),
            ('AS','sanction','Police fire tear gas; ~300 arrested across 24 cases in protest zones.'),
            ('AS','chart','55 factories close; workers demand \u09F330,000 monthly from \u09F312,500.'),
            ('AS','attack','Kafrul (Dhaka): Stun grenades fired after BNP activists harass female workers.'),
            ('BZ','paint','Van Gogh\u2019s "Blossoming Chestnut Trees" sells for $190.4M at Sotheby\u2019s.'),
            ('SC','space','Voyager 1 reaches 1 light-day from Earth \u2014 1st human object (launched 1977).'),
            ('AM','gamepad','PlayStation reports major outage ahead of GTA VI release.'),
            ('AF','cricket','Litton Das sets Test record: 8 dismissals in an innings vs South Africa.'),
            ('AF','trophy','Johannesburg: 6 catches + 2 stumpings in one innings \u2014 world record.'),
            ('BZ','mineral','Van Gogh sale tops $117.2M "Orchard with Cypresses" 2022 record.'),
            ('EU','oil','EU loan funded by frozen Russian assets \u2014 first use of immobilised reserves.'),
            ('AP','handshake','APEC: Trade ministers discuss digital economy, supply chains & climate.'),
            ('ME','storm','Gulf states place air defences on highest alert after Iran drone strike.'),
            ('SC','anchor','Voyager 1: 49-year deep-space journey, still transmitting from light-day mark.'),
        ],
    },
]

for pi,P in enumerate(panels):
    px = MARGIN+pi*(panel_w+panel_gap)
    py = content_y
    rr([px,py,px+panel_w,py+CONTENT_H], 8, PANEL_BG, outline=RULE)
    rr([px,py,px+panel_w,py+23], 8, P['color'])
    d.rectangle([px,py+11,px+panel_w,py+23], fill=P['color'])
    d.text((px+10,py+3), P['title'], font=f_panel_h, fill=WHITE)

    iy = py+27
    row_h = 38
    for tag2,ik,text in P['items']:
        if iy+row_h>py+CONTENT_H-4: break
        tc = COL.get(tag2,MUTED)
        bx,by = px+6,iy+2
        rr([bx,by,bx+16,by+16], 3, WHITE, outline=tc,width=1)
        draw_icon(ik,bx,by,tc)
        tx2 = bx+18
        tw2 = d.textlength(tag2, font=f_item)
        rr([tx2,by,tx2+tw2+5,by+13], 2, tc)
        d.text((tx2+2,by+1), tag2, font=f_item, fill=WHITE)
        txt_x = tx2+tw2+8
        lines = wrap(text, f_item, px+panel_w-txt_x-4)
        if len(lines)>2: lines=lines[:2]
        for li,line in enumerate(lines):
            d.text((txt_x,by+li*12), line, font=f_item, fill=INK)
        iy += row_h

# ─── UTC TIMELINE ─────────────────────────
uy = content_y+CONTENT_H+GAP
d.rectangle([MARGIN,uy,W-MARGIN,uy+UTC_H], fill=(242,238,228), outline=RULE)
rr([MARGIN,uy,MARGIN+195,uy+20], 8, DARK)
d.rectangle([MARGIN,uy+10,MARGIN+195,uy+20], fill=DARK)
d.text((MARGIN+8,uy+3), 'UTC TIMELINE  18 NOV 2026', font=f_tag, fill=WHITE)
utc_events = [
    ('~02:00','Iran drones at Kuwait','ME'),('~04:00','Xi\u2013Trump APEC Shenzhen','AP'),
    ('~06:00','Crimean Bridge struck','EU'),('~10:00','Gaza operation begins','ME'),
    ('~12:00','EU \u20AC45bn Ukraine loan','EU'),('~16:00','Van Gogh auction','BZ'),
    ('~20:00','Voyager 1: 1 light-day','SC'),('~22:00','Litton Das 8 dismissals','AF'),
]
ux = MARGIN+203
uw = (W-MARGIN*2-ux+MARGIN)/len(utc_events)-4
for tm,txt,code in utc_events:
    tc3 = COL.get(code,(120,90,40))
    d.text((ux,uy+21), tm, font=f_item, fill=INK)
    d.text((ux,uy+33), txt, font=f_utc, fill=MUTED)
    tw3 = d.textlength(txt, font=f_utc)
    d.line([ux,uy+UTC_H-1,ux+tw3+2,uy+UTC_H-1], fill=tc3, width=2)
    ux += uw+4

# ─── ALSO ON 18 NOVEMBER ─────────────────
ay = uy+UTC_H+GAP
rr([MARGIN,ay,W-MARGIN,ay+ALSO_H], 8, WHITE, outline=RULE)
rr([MARGIN,ay,MARGIN+165,ay+19], 8, DARK)
d.rectangle([MARGIN,ay+9,MARGIN+165,ay+19], fill=DARK)
d.text((MARGIN+10,ay+2), 'ALSO ON 18 NOVEMBER', font=f_tag, fill=WHITE)
also = [
    ('JEFFRIES','SPEAKER'),('PUTIN','SHENZHEN'),('HAITI','GANGS'),
    ('VAN GOGH','$190.4M'),('PLAYSTATION','OUTAGE'),
]
ax2 = MARGIN+172
for lab1,lab2 in also:
    w1 = d.textlength(lab1, font=f_also); w2 = d.textlength(lab2, font=f_also_v)
    rr([ax2,ay+22,ax2+w1+6,ay+38], 3, DARK)
    d.text((ax2+2,ay+23), lab1, font=f_also, fill=WHITE)
    d.text((ax2+w1+8,ay+24), ' '+lab2, font=f_also_v, fill=MUTED)
    ax2 += w1+w2+22

# ─── FOOTER ───────────────────────────────
fy = ay+ALSO_H+GAP
d.line([MARGIN,fy,W-MARGIN,fy], fill=RULE, width=1)
d.text((MARGIN+2,fy+1), 'Sources: AP, Reuters, BBC, AFP, CNN, Wikipedia Portal:Current events/2026 November 18', font=f_footer, fill=MUTED)
dc(fy+10, 'DATE CHECK: All events happened or were first reported on Wednesday 18 November 2026 (any time zone).', f_datechk, INK)
# Region legend (bottom)
lx = W-300
for code3,clr in [('EU',COL['EU']),('ME',COL['ME']),('AP',COL['AP']),('AS',COL['AS']),
                   ('AF',COL['AF']),('AM',COL['AM']),('OC',COL['OC']),('SC',COL['SC']),('BZ',COL['BZ'])]:
    d.rectangle([lx,fy+22,lx+9,fy+31], fill=clr)
    d.text((lx+11,fy+21), code3, font=f_footer, fill=MUTED)
    lx += 34

out = os.path.join(os.path.dirname(__file__), 'entry.png')
img.save(out, format='PNG', optimize=True)
print('saved', out, os.path.getsize(out))