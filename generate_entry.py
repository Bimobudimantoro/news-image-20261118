#!/usr/bin/env python3
import os
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 242, 230)
INK = (28, 28, 28)
MUTED = (85, 80, 72)
RULE = (188, 178, 162)
WHITE = (255, 255, 255)
DARK = (34, 32, 28)
PANEL_BG = (252, 249, 242)

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
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

f_title = load_font('/system/fonts/NotoSerif-Bold.ttf', 46)
f_sub = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 16)
f_strip_val = load_font('/system/fonts/NotoSerif-Bold.ttf', 21)
f_strip_lab = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 12)
f_tag = load_font('/system/fonts/RobotoCondensed-Bold.ttf', 13)
f_lead_h = load_font('/system/fonts/NotoSerif-Bold.ttf', 22)
f_lead_b = load_font('/system/fonts/Roboto-Regular.ttf', 13)
f_panel_h = load_font('/system/fonts/RobotoCondensed-Bold.ttf', 14)
f_item = load_font('/system/fonts/Roboto-Regular.ttf', 11)
f_pill = load_font('/system/fonts/RobotoCondensed-Bold.ttf', 11)
f_utc = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 11)
f_footer = load_font('/system/fonts/RobotoCondensed-Regular.ttf', 10)
f_datecheck = load_font('/system/fonts/NotoSerif-Bold.ttf', 17)

img = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if d.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines if lines else ['']

def draw_wrapped(x, y, text, font, fill, max_w, lh, max_lines=None):
    lines = wrap(text, font, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y

def rr(xy, radius, fill, outline=None, width=1):
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_centered_text(y, text, font, fill):
    tw = d.textlength(text, font=font)
    d.text(((W - tw) / 2, y), text, font=font, fill=fill)

# ---------- Lead illustrations ----------
def draw_lead_icon(kind, x, y, w, h):
    rr([x, y, x+w, y+h], 6, (242, 238, 228), outline=RULE)
    if kind == 'bridge':
        d.rectangle([x+2, y+h-18, x+w-2, y+h-2], fill=(150, 195, 225))
        d.rectangle([x+2, y+2, x+w-2, y+h-18], fill=(225, 235, 245))
        for px in [x+18, x+w//2, x+w-18]:
            d.rectangle([px-3, y+14, px+3, y+h-18], fill=(85,85,90))
            d.rectangle([px-5, y+14, px+5, y+18], fill=(70,70,75))
        d.rectangle([x+4, y+h//2+2, x+w-4, y+h//2+7], fill=(70,70,75))
        for p in [x+18, x+w-18]:
            d.line([p, y+16, x+w//2, y+h//2+2], fill=(90,90,95), width=2)
        d.line([x+18, y+16, x+w-18, y+16], fill=(90,90,95), width=2)
        ex, ey = x+w//2+10, y+24
        for ang in range(0, 360, 30):
            r1 = 4 if ang % 60 == 0 else 6
            r2 = 15 if ang % 60 == 0 else 11
            x1 = ex + r1*math.cos(math.radians(ang))
            y1 = ey + r1*math.sin(math.radians(ang))
            x2 = ex + r2*math.cos(math.radians(ang))
            y2 = ey + r2*math.sin(math.radians(ang))
            d.line([x1,y1,x2,y2], fill=(235,130,30), width=2)
        d.ellipse([ex-6,ey-6,ex+6,ey+6], fill=(255,210,70), outline=(220,120,20))
        for sx,sy,sr in [(ex+14,ey-8,5),(ex+18,ey-2,4),(ex+10,ey-12,4)]:
            d.ellipse([sx-sr,sy-sr,sx+sr,sy+sr], fill=(120,120,125))
    elif kind == 'art':
        d.rectangle([x+2, y+2, x+w-2, y+h-2], fill=(245, 236, 220))
        d.rectangle([x+8, y+6, x+w-8, y+h-8], outline=(140, 105, 55), width=3)
        d.rectangle([x+11, y+9, x+w-11, y+h-11], fill=(250, 247, 240))
        d.line([x+18, y+h-12, x+30, y+30], fill=(95, 70, 45), width=3)
        d.line([x+30, y+30, x+48, y+16], fill=(95, 70, 45), width=2)
        d.line([x+30, y+30, x+52, y+34], fill=(95, 70, 45), width=2)
        d.line([x+38, y+22, x+36, y+12], fill=(95, 70, 45), width=2)
        for bx,by,br in [(x+46,y+16,8),(x+58,y+20,7),(x+36,y+12,6),(x+52,y+32,7),(x+40,y+26,6),(x+62,y+30,5),(x+28,y+24,5)]:
            d.ellipse([bx-br,by-br,bx+br,by+br], fill=(255,252,248), outline=(230,218,200))
            d.ellipse([bx-2,by-2,bx+2,by+2], fill=(235,205,120))
        badge = '$190.4M'
        bw = d.textlength(badge, font=f_tag) + 10
        bx0 = x + w - bw - 6
        by0 = y + h - 22
        rr([bx0, by0, bx0+bw, by0+16], 4, (255, 248, 225), outline=(160,120,40))
        d.text((bx0+5, by0+1), badge, font=f_tag, fill=(110,75,20))
    elif kind == 'voyager':
        d.rectangle([x+2, y+2, x+w-2, y+h-2], fill=(18, 28, 55))
        for sx,sy,r in [(x+10,y+10,1),(x+22,y+18,1),(x+w-14,y+12,1),(x+w-24,y+22,1),(x+16,y+h-14,1),(x+w-10,y+h-16,1),(x+w//2,y+8,1),(x+30,y+8,1)]:
            d.ellipse([sx-r,sy-r,sx+r,sy+r], fill=(245,245,255))
        d.arc([x-30, y+h-26, x+42, y+h+46], start=270, end=355, fill=(70,130,200), width=7)
        d.arc([x-24, y+h-20, x+36, y+h+40], start=275, end=350, fill=(90,170,90), width=4)
        for i, (px,py) in enumerate([(x+36,y+h-14),(x+46,y+h-22),(x+56,y+h-30),(x+66,y+h-38),(x+76,y+h-46)]):
            pr = 2
            d.ellipse([px-pr,py-pr,px+pr,py+pr], fill=(170,210,255))
        sx, sy = x+w-34, y+24
        d.rectangle([sx, sy, sx+14, sy+10], fill=(215,215,220), outline=(140,140,150))
        d.line([sx-2, sy+5, sx-10, sy+5], fill=(200,200,210), width=2)
        d.arc([sx-16, sy-4, sx-2, sy+14], start=300, end=60, fill=(235,235,240), width=2)
        d.line([sx+14, sy+5, sx+30, sy-2], fill=(180,180,190), width=2)
        d.line([sx+14, sy+5, sx+28, sy+10], fill=(180,180,190), width=2)
        d.rectangle([sx+18, sy-6, sx+28, sy+2], outline=(170,190,220), width=1)
        d.rectangle([sx+17, sy+7, sx+27, sy+14], outline=(170,190,220), width=1)
        d.text((x+8, y+6), '1 LD', font=f_pill, fill=(180,220,255))

# ---------- Per-item mini icons for panels ----------
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
        d.polygon([(cx, y+1),(x+14,y+4),(x+13,y+10),(cx,y+15),(x+2,y+10),(x+2,y+4)], outline=c, fill=None)
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
        for wy in [y+5,y+9,y+13]:
            d.arc([x+1,wy-3,x+8,wy+1], start=180, end=0, fill=c, width=2)
            d.arc([x+8,wy-3,x+15,wy+1], start=180, end=0, fill=c, width=2)
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
    else:
        d.ellipse([x+4,y+4,x+12,y+12], outline=c, width=2)

# ---------- Header ----------
d.rectangle([0,0,W,86], fill=DARK)
draw_centered_text(8, 'WEDNESDAY 18 NOVEMBER 2026', f_title, (250,246,238))
draw_centered_text(60, 'WORLD NEWS IN ONE IMAGE  \u2022  48 verified stories  \u2022  Events happened or first reported 18 Nov 2026 (any time zone)', f_sub, (210,200,185))

# ---------- Numbers strip (8 items) ----------
sy = 86
sh = 52
d.rectangle([0,sy,W,sy+sh], fill=(235,228,214))
d.line([0,sy+sh,W,sy+sh], fill=RULE, width=1)
nums = [
    ('$190.4M', 'Van Gogh sale'),
    ('1 light-day', 'Voyager 1'),
    ('8 dismissals', 'Litton Das record'),
    ('~300 arrests', 'Bangladesh protests'),
    ('55 factories', 'closed in Gazipur'),
    ('4 days', 'Crimea strikes'),
    ('\u09F330,000', 'wage demanded'),
    ('49 years', 'Voyager travel'),
]
items_w = []
for val, lab in nums:
    tw = d.textlength(val, font=f_strip_val)
    lw = d.textlength(lab, font=f_strip_lab)
    items_w.append(max(tw, lw))
gap_n = 16
total = sum(items_w) + gap_n*(len(nums)-1)
nx = (W - total) / 2
for i, (val, lab) in enumerate(nums):
    iw = items_w[i]
    vw = d.textlength(val, font=f_strip_val)
    lw = d.textlength(lab, font=f_strip_lab)
    d.text((nx + (iw-vw)/2, sy+4), val, font=f_strip_val, fill=COL['EU'])
    d.text((nx + (iw-lw)/2, sy+28), lab, font=f_strip_lab, fill=MUTED)
    nx += iw + gap_n

y0 = sy + sh + 8

# ---------- Leads (3 cards, slightly shorter) ----------
lead_h = 152
gap = 10
margin = 18
lead_w = (W - margin*2 - gap*2) // 3
leads = [
    {'tag':'CONFLICT \u2022 EUROPE','color':COL['EU'],'title':'Crimean Bridge struck again','body':'Ukraine hits Crimean Bridge for the 3rd time in four days; Russia closes it to all traffic.','icon':'bridge'},
    {'tag':'ARTS & CULTURE','color':COL['BZ'],'title':'Van Gogh sells for $190.4M','body':'"Blossoming Chestnut Trees" (1890) sells at Sotheby\'s NY \u2014 a new Van Gogh auction record.','icon':'art'},
    {'tag':'SCIENCE & SPACE','color':COL['SC'],'title':'Voyager 1: one light-day out','body':'NASA\'s Voyager 1 is the first human-made object one light-day from Earth, 49 years after launch.','icon':'voyager'},
]
icon_w, icon_h = 82, 68
for i, L in enumerate(leads):
    lx = margin + i*(lead_w + gap)
    ly = y0
    rr([lx,ly,lx+lead_w,ly+lead_h], 8, WHITE, outline=RULE)
    rr([lx,ly,lx+lead_w,ly+22], 8, L['color'])
    d.rectangle([lx,ly+12,lx+lead_w,ly+22], fill=L['color'])
    d.text((lx+10, ly+3), L['tag'], font=f_tag, fill=WHITE)
    ix = lx + lead_w - icon_w - 6
    iy = ly + 24
    draw_lead_icon(L['icon'], ix, iy, icon_w, icon_h)
    tx = lx + 10
    tmax = ix - tx - 6
    ty = draw_wrapped(tx, ly+26, L['title'], f_lead_h, INK, tmax, 22, max_lines=2)
    body_y = max(ty + 2, iy + icon_h + 4)
    bmax = lead_w - 20
    draw_wrapped(tx, body_y, L['body'], f_lead_b, MUTED, bmax, 14, max_lines=3)

# ---------- Layout arithmetic ----------
py = y0 + lead_h + 8
utc_h = 44
also_h = 44
footer_h = 42
panel_h = H - py - utc_h - also_h - footer_h - 10
col_w = (W - margin*2 - gap*2) // 3

# ---------- 3 Panels (12 items each, 36 total) ----------
panels = [
    ('CONFLICTS & SECURITY', COL['EU'], [
        ('EU','blast','Crimean Bridge hit; Russia closes it to all traffic.'),
        ('AM','shield','Haiti: Salvadoran forces destroy Taliban gang leader Jeff Larose\'s house in Canaan.'),
        ('ME','attack','Gaza: Israel launches first central Gaza operation since Oct 2025 ceasefire.'),
        ('AS','rifle','Kulgam (J&K): Indian forces kill militant commander at a mosque.'),
        ('AS','soldier','Narail (Bangladesh): 2 BNP members killed in attack on motorcycle procession.'),
        ('AS','fire','Narayanganj: Crowd sets fire to ex-MP Shamim Osman\'s residence.'),
        ('AS','blast','Gopalganj: Armed group bombs & burns BNP MP K M Babar\'s clinic; patients flee.'),
        ('AS','shield','Pirojpur: Ex-minister SM Rezaul Karim\'s 2 houses looted and burned.'),
        ('AS','sanction','Sirajganj: AL office and ex-MP Habibe Millat\'s home vandalised.'),
        ('AS','vote','Gopalganj: 5 BNP offices torched; 2 Grameen Bank branches attacked.'),
        ('AS','chart','Crimea: Ukraine\'s 3rd major strike on bridge in just four days.'),
        ('ME','person','Gaza operation amid displacement of families from central Strip.'),
    ]),
    ('PROTESTS, LABOUR & LAW', COL['AM'], [
        ('AS','person','Gazipur, Savar, Ashulia: Garment workers block Dhaka\u2013Mymensingh Highway.'),
        ('AS','sanction','Police fire tear gas & stun grenades across protest zones; ~300 arrested.'),
        ('AS','chart','55 factories close; thousands demand ৳30,000 monthly minimum wage.'),
        ('AS','attack','Kafrul (Dhaka): Stun grenades fired; BNP activists allegedly harass female workers.'),
        ('AS','fire','Chattogram: Muhammad Yunus\'s ancestral home set ablaze by arsonists.'),
        ('AS','gavel','Narail: Banned Awami League attacks BNP motorcycle procession; 2 killed.'),
        ('AS','handshake','Nazirpur: Houses of ex-minister SM Rezaul Karim looted and torched.'),
        ('AS','scales','Sirajganj: Crowd vandalises local Awami League office and ex-MP\'s home.'),
        ('AM','shield','Haiti: Gang Suppression Force states it was not involved in Canaan raid.'),
        ('AS','vote','Gopalganj: Crude bombs detonated at BNP MP\'s clinic; patients evacuated.'),
        ('AS','mineral','24 cases filed in Savar & Ashulia over garment worker protests.'),
        ('AS','flood','Protesters set fire to a police vehicle on Dhaka\u2013Mymensingh Highway.'),
    ]),
    ('ARTS, SCIENCE & SPORT', COL['OC'], [
        ('BZ','mineral','Van Gogh\'s "Blossoming Chestnut Trees" fetches $190.4M at Sotheby\'s New York.'),
        ('SC','anchor','Voyager 1: first human-made object one light-day from Earth (1977 launch).'),
        ('AM','gamepad','PlayStation reports major outage ahead of Grand Theft Auto VI release.'),
        ('AF','cricket','Litton Das sets Test record: 8 dismissals in an innings vs South Africa.'),
        ('AF','trophy','Johannesburg Test: 6 catches and 2 stumpings \u2014 a world record.'),
        ('EU','blast','Crimean Bridge: Russia closes crossing after third strike in 4 days.'),
        ('AS','chart','Bangladesh industrial belt: wage protests spread across Gazipur.'),
        ('AS','soldier','Kulgam: Commander killed after escaping shootout two days earlier.'),
        ('EU','person','Van Gogh sale surpasses $117.2M paid for "Orchard with Cypresses" (2022).'),
        ('SC','flood','Voyager probe launched 1977; now 49 years into deep-space mission.'),
        ('AS','handshake','Gaza: first ground operation since Oct 2025 ceasefire came into effect.'),
        ('AM','shield','Canaan: Taliban gang leader Jeff Larose targeted in Salvadoran operation.'),
    ]),
]

for i, (title, color, items) in enumerate(panels):
    px = margin + i*(col_w + gap)
    rr([px,py,px+col_w,py+panel_h], 8, PANEL_BG, outline=RULE)
    rr([px,py,px+col_w,py+23], 8, color)
    d.rectangle([px,py+11,px+col_w,py+23], fill=color)
    d.text((px+10, py+3), title, font=f_panel_h, fill=WHITE)

    iy = py + 27
    for tag, ik, text in items:
        if iy > py + panel_h - 20:
            break
        tc = COL.get(tag, MUTED)
        badge_x = px + 6
        badge_y = iy + 1
        rr([badge_x, badge_y, badge_x+16, badge_y+16], 3, (255,255,255), outline=tc, width=1)
        draw_item_icon(ik, badge_x, badge_y, tc)
        tag_x = badge_x + 18
        tw = d.textlength(tag, font=f_item)
        rr([tag_x, badge_y, tag_x+tw+5, badge_y+13], 2, tc)
        d.text((tag_x+2, badge_y+1), tag, font=f_item, fill=WHITE)
        tx = tag_x + tw + 8
        maxw = px + col_w - tx - 4
        lines = wrap(text, f_item, maxw)
        if len(lines) > 2:
            lines = lines[:2]
        for li, line in enumerate(lines):
            d.text((tx, badge_y + li*12), line, font=f_item, fill=INK)
        iy += 38

# ---------- UTC timeline strip ----------
uy = py + panel_h + 4
d.rectangle([margin, uy, W-margin, uy+utc_h], fill=(242,238,228), outline=RULE)
rr([margin, uy, margin+210, uy+21], 8, DARK)
d.rectangle([margin, uy+10, margin+210, uy+21], fill=DARK)
d.text((margin+8, uy+3), 'UTC TIMELINE  18 NOV 2026', font=f_tag, fill=WHITE)
utc_events = [
    ('~00:00','Crimean Bridge struck','EU'),
    ('~03:00','Bangladesh protests erupt','AS'),
    ('~06:00','Gaza operation launched','ME'),
    ('~09:00','Kulgam commander killed','AS'),
    ('~14:00','Van Gogh auction NY','BZ'),
    ('~18:00','Voyager 1 milestone','SC'),
    ('~20:00','Litton Das Test record','AF'),
    ('~22:00','Yunus home arson','AS'),
]
ux = margin + 218
uw = (W - margin*2 - ux + margin) // len(utc_events) - 8
for tm, txt, code in utc_events:
    tc = COL.get(code, (120,90,40))
    d.text((ux, uy+23), tm, font=f_item, fill=INK)
    d.text((ux, uy+33), txt, font=f_utc, fill=MUTED)
    tw2 = d.textlength(txt, font=f_utc)
    d.line([ux, uy+utc_h-1, ux+tw2+4, uy+utc_h-1], fill=tc, width=2)
    ux += uw + 8

# ---------- ALSO ON 18 NOVEMBER strip ----------
ay = uy + utc_h + 4
rr([margin, ay, W-margin, ay+also_h], 8, WHITE, outline=RULE)
rr([margin, ay, margin+170, ay+19], 8, DARK)
d.rectangle([margin, ay+9, margin+170, ay+19], fill=DARK)
d.text((margin+10, ay+2), 'ALSO ON 18 NOVEMBER', font=f_tag, fill=WHITE)
also_items = [
    ('EU','blast','Crimean Bridge closed after 3rd strike'),
    ('AS','fire','M. Yunus home burned in Chattogram'),
    ('AM','gamepad','PlayStation outage ahead of GTA VI'),
    ('AF','cricket','Litton Das 8 dismissals (Test record)'),
    ('AS','person','Bangladesh protests: 24 cases, ~300 arrests'),
]
ax = margin + 182
for code, ik, txt in also_items:
    tc = COL.get(code, MUTED)
    tw_tag = d.textlength(code, font=f_item)
    rr([ax, ay+22, ax+18, ay+38], 3, (255,255,255), outline=tc)
    draw_item_icon(ik, ax+1, ay+23, tc)
    ax += 20
    rr([ax, ay+23, ax+tw_tag+6, ay+36], 2, tc)
    d.text((ax+2, ay+24), code, font=f_item, fill=WHITE)
    ax += tw_tag + 8
    maxw_item = 145
    lines = wrap(txt, f_utc, maxw_item)
    if lines:
        d.text((ax, ay+23), lines[0], font=f_utc, fill=INK)
    ax += maxw_item + 8

# ---------- Footer + DATE CHECK ----------
fy = H - footer_h
d.line([margin, fy-4, W-margin, fy-4], fill=RULE, width=1)
d.text((margin+2, fy-1), 'Source: Wikipedia Portal:Current events/2026 November 18', font=f_footer, fill=MUTED)
draw_centered_text(fy+8, 'DATE CHECK: This image covers only events that happened or were first reported on Wed 18 Nov 2026 (any time zone).', f_datecheck, INK)
lx = W - 300
for code in ['EU','ME','AS','AF','AM','OC','SC','BZ']:
    c = COL.get(code, (100,100,100))
    d.rectangle([lx, fy+1, lx+9, fy+10], fill=c)
    d.text((lx+12, fy-1), code, font=f_footer, fill=MUTED)
    lx += 36

out_path = os.path.join(os.path.dirname(__file__), 'entry.png')
img.save(out_path, format='PNG', optimize=True)
print('saved', out_path, os.path.getsize(out_path))
