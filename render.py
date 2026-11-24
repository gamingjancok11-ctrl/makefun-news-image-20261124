#!/usr/bin/env python3
"""Render the make.fun news-image-20261124 entry.

A one-page newspaper front page summing up the world news of Tuesday
24 November 2026: masthead, 3 lead stories, a 15-story grid, 18 briefs
and a world map with 19 numbered markers.

Deterministic: fixed layout, fixed system fonts, no timestamps, no
randomness, no network. Re-running produces byte-identical output.
Run:  python3 render.py   (writes entry.png next to this file)
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

# --- canvas -----------------------------------------------------------------
W, H = 1024, 1024
MARGIN = 24
CW = W - 2 * MARGIN  # content width: 976

PAPER = (253, 251, 243)
INK = (17, 17, 17)
GREY = (90, 90, 90)
RED = (178, 34, 34)
RULE = (60, 60, 60)
SEA = (214, 232, 244)
LAND = (222, 211, 178)
LAND_EDGE = (150, 138, 105)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = os.path.join(FONT_DIR, "dejavu", "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "dejavu", "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "dejavu", "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "dejavu", "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SERIF_B, 58)
F_DATE = font(SANS_B, 23)
F_SUB = font(SERIF, 13)
F_TOPLINE = font(SANS_B, 11)
F_KICK = font(SANS_B, 13)      # lead kickers
F_HEAD = font(SERIF_B, 20)     # lead headlines
F_BODY = font(SANS, 13)        # lead body
F_GKICK = font(SANS_B, 11)     # grid kickers
F_GBODY = font(SANS, 11)       # grid body
F_SECT = font(SANS_B, 13)      # section headers
F_BRIEF = font(SANS, 11)       # briefs body
F_BRIEF_B = font(SANS_B, 11)   # briefs kicker
F_MAP_H = font(SANS_B, 13)     # map header
F_LEGEND = font(SANS, 10)      # map legend
F_NUM = font(SANS_B, 9)        # marker numbers
F_FOOT = font(SANS, 10)

# --- stories (final list, 24 Nov 2026) --------------------------------------
# Leads: (kicker, headline, body)
LEADS = [
    ("GAZA",
     "Israeli strikes kill Hamas security chief",
     "Airstrikes kill Naeem Abu Nahel and six others in Gaza on Tuesday, "
     "despite the October 2025 ceasefire."),
    ("ZAPORIZHZHIA",
     "Overnight Russian attack kills 2, wounds 40",
     "An apartment block is partially destroyed; 96 drones launched "
     "overnight, 73 shot down."),
    ("INDONESIA",
     "Factory fire kills at least 24 in Cikande",
     "About 30 missing as rescuers search the burnt-out confectionery "
     "plant in Banten."),
]

# Grid: (kicker, body)
GRID = [
    ("AUSTRALIA\u2013SINGAPORE",
     "Leaders meet in Canberra, sign deals on carbon transport, AI and "
     "essential supplies."),
    ("POLAND",
     "Russian drone briefly enters Polish airspace near Dorohusk; NATO "
     "deploys advanced detection aircraft in Poland."),
    ("EU",
     "22nd sanctions package proposed, including a sports ban; seven states "
     "urge limits on Russian visas."),
    ("GERMANY",
     "First country to access Ukraine\u2019s Delta battlefield system; "
     "preliminary deal on more interceptor missiles."),
    ("TRUMP",
     "Signals deals with Democrats on healthcare and a 10% credit-card "
     "rate cap."),
    ("SPACEX",
     "Oregon and Virginia sue SpaceX over alleged Grok-generated child "
     "abuse images."),
    ("CROWDSTRIKE",
     "To buy Zscaler in a $44 billion deal."),
    ("INDIA\u2013NEPAL",
     "India pledges $1.6 billion to Nepal rebuild as Nepal\u2019s PM visits "
     "New Delhi."),
    ("SHENZHOU-24",
     "China to launch first foreign astronaut, Pakistan\u2019s Zeeshan Ali, "
     "to Tiangong station."),
    ("SOUTH KOREA",
     "Scrambles jets as Russian warplanes enter its air-defence zone."),
    ("COLOMBIA",
     "Car bomb wounds at least 23 outside the governor\u2019s office in "
     "Villavicencio."),
    ("MEXICO",
     "To try \u2018Chapo Isidro\u2019 at home despite a US extradition "
     "request."),
    ("COP31",
     "Fallout: talks end with no deal as fossil-fuel language is blocked; "
     "Pacific nations despair, blame game begins."),
    ("BRAZIL",
     "Real weakens as Congress votes on Lula\u2019s fiscal package."),
    ("AUSTRALIA",
     "Labor\u2013Greens deal on online safety bill, fines up to 5% of tech "
     "firms\u2019 global revenue."),
]

# Briefs: (kicker, body)
BRIEFS = [
    ("HORMUZ",
     "Iran says three tankers hit mines in the Strait of Hormuz; Britain "
     "reports a record number of Iranian attacks on shipping there."),
    ("YEMEN",
     "Strikes on buses and trucks kill about 25; Houthis blame a Saudi "
     "strike for 17 dead in Hodeida."),
    ("IRAQ",
     "PM orders takeover of oilfields in Kurdish-controlled areas."),
    ("IRAN",
     "Singer Parastoo Ahmadi flogged 74 lashes."),
    ("NATO",
     "Rutte: alliance will defend against threats in space amid Russian "
     "nuclear-satellite reports."),
    ("ESTONIA",
     "Russia warns its moves are \u2018on verge of triggering open war\u2019."),
    ("SUDAN",
     "UNICEF: drones and drought \u2018closing in\u2019 on Sudan; drone strikes "
     "now hit targets 1,500 km away."),
    ("MEASLES",
     "Pennsylvania outbreak claims a ninth death; 46 counties affected."),
    ("NVIDIA",
     "Slips in Tuesday premarket after Monday\u2019s record 31% surge; Huang "
     "to testify to Congress Dec 3."),
    ("MEGASPEED",
     "US blacklists Singapore cloud firm; Malaysia tells data centres to "
     "cut links with blacklisted firms."),
    ("HANOI",
     "Restaurant blast kills at least 6, injures 10."),
    ("JAPAN",
     "Launches Asian oil task force amid Gulf supply disruptions."),
    ("HASINA",
     "Plans return to Bangladesh Dec 16; she faces a death sentence."),
    ("FIFA",
     "US, Mexico, Costa Rica and Jamaica to co-host the 2031 Women\u2019s "
     "World Cup (48 teams); UK hosts 2035."),
    ("BOLSONARO",
     "In ICU with acute bowel obstruction, stable, hospital says."),
    ("TAIWAN",
     "Votes Saturday; Beijing targets DPP\u2019s Taipei candidate."),
    ("MSF",
     "Suspends work in South Sudan\u2019s Yei River county after an "
     "abduction."),
    ("SOLOMON ISLANDS",
     "To end its China security pact and sign a treaty with Australia."),
]

# Map markers: (number, name, latitude, longitude). Two display nudges keep
# crowded markers apart: Antalya plotted slightly west, Khartoum south.
MARKERS = [
    (1, "Gaza", 31.5, 34.5),
    (2, "Zaporizhzhia", 47.8, 35.1),
    (3, "Cikande", -6.2, 106.4),
    (4, "Canberra", -35.3, 149.1),
    (5, "Dorohusk", 51.2, 23.8),
    (6, "Brussels", 50.8, 4.4),
    (7, "Berlin", 52.5, 13.4),
    (8, "Washington DC", 38.9, -77.0),
    (9, "New Delhi", 28.6, 77.2),
    (10, "Beijing", 39.9, 116.4),
    (11, "Seoul", 37.6, 127.0),
    (12, "Villavicencio", 4.1, -73.6),
    (13, "Mexico City", 19.4, -99.1),
    (14, "Antalya", 39.0, 28.0),
    (15, "Bras\u00edlia", -15.8, -47.9),
    (16, "Strait of Hormuz", 26.6, 56.3),
    (17, "Baghdad", 33.3, 44.4),
    (18, "Khartoum", 13.5, 31.0),
    (19, "Honiara", -9.4, 160.0),
]

# Simplified continent outlines, (lon, lat) pairs, equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-160, 58), (-150, 60), (-140, 60), (-132, 56), (-126, 50),
     (-124, 42), (-120, 34), (-113, 29), (-109, 23), (-105, 20), (-97, 16),
     (-94, 17), (-91, 19), (-87, 21), (-86, 15), (-83, 9), (-79, 8),
     (-79, 9), (-82, 10), (-84, 14), (-87, 16), (-88, 18), (-90, 21),
     (-93, 20), (-96, 19), (-97, 22), (-97, 26), (-94, 29), (-90, 29),
     (-86, 30), (-84, 30), (-82, 28), (-81, 25), (-80, 32), (-79, 34),
     (-76, 35), (-74, 40), (-71, 41), (-69, 44), (-66, 45), (-61, 46),
     (-60, 47), (-64, 50), (-66, 53), (-61, 55), (-65, 58), (-68, 58),
     (-72, 62), (-77, 63), (-82, 66), (-88, 66), (-92, 66), (-95, 69),
     (-105, 68), (-115, 68), (-125, 70), (-135, 69), (-145, 70), (-155, 71),
     (-162, 70)],
    # Greenland
    [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-22, 70),
     (-20, 76), (-28, 80), (-40, 82), (-55, 80), (-62, 77), (-66, 73),
     (-60, 70), (-55, 67)],
    # Iceland
    [(-22, 64), (-18, 63), (-15, 64), (-14, 66), (-18, 66), (-21, 66)],
    # South America
    [(-77, 7), (-75, 10), (-72, 12), (-64, 11), (-60, 8), (-53, 5),
     (-50, 0), (-44, -3), (-35, -8), (-37, -13), (-39, -17), (-40, -22),
     (-46, -24), (-48, -28), (-52, -33), (-57, -38), (-62, -41), (-65, -45),
     (-67, -50), (-68, -54), (-70, -54), (-73, -50), (-73, -44), (-73, -37),
     (-71, -30), (-70, -20), (-75, -15), (-77, -12), (-79, -6), (-81, -1),
     (-80, 2), (-78, 5)],
    # Europe (mainland, full perimeter: Med coast east, Black Sea coast
    # north, eastern edge to the Arctic, Norway coast south, Atlantic
    # coast back to Gibraltar). The old outline cut back across the
    # continent through Denmark/Germany, leaving France, Germany and
    # Poland as sea and stranding the Brussels, Berlin and Dorohusk
    # markers in the ocean.
    [(-6, 36), (-2, 37), (0, 39), (3, 42), (7, 44), (10, 44), (12, 42),
     (14, 41), (16, 40), (18, 40), (19, 42), (21, 41), (23, 40), (26, 40),
     (28, 41), (29, 42), (29, 44), (30, 46), (31, 47), (32, 48), (33, 50),
     (32, 52), (31, 54), (30, 56), (30, 58), (30, 60), (30, 64), (32, 67),
     (31, 70), (27, 71), (22, 70), (18, 69), (14, 67), (12, 64), (6, 62),
     (5, 60), (5, 58), (8, 57), (8, 55), (7, 54), (5, 53), (3, 51),
     (1, 51), (0, 50), (-2, 49), (-4, 48), (-2, 46), (-1, 44), (-2, 44),
     (-9, 43), (-9, 37)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-4, 58), (-2, 57), (0, 53), (1, 51),
     (-1, 50)],
    # Ireland
    [(-10, 52), (-8, 52), (-6, 52), (-6, 54), (-8, 55), (-10, 54)],
    # Italy
    [(7, 44), (10, 44), (12, 42), (14, 41), (16, 40), (16, 38), (15, 40),
     (13, 41), (11, 43), (8, 44)],
    # Greece
    [(20, 40), (23, 40), (26, 40), (28, 41), (26, 39), (23, 37), (21, 37),
     (20, 39)],
    # Middle East / Anatolia (was unmapped sea: Gaza, Antalya and
    # Baghdad all floated in it). North edge meets the Asia polygon,
    # south edge follows Arabia's north edge, west edge the Levant and
    # Aegean coasts. The Persian Gulf itself is filled at this scale.
    [(26, 38), (28, 40), (30, 41), (32, 41), (36, 41), (41, 42), (44, 40),
     (48, 38), (52, 37), (56, 36), (60, 34), (63, 32), (63, 29), (60, 27),
     (57, 26), (55, 27), (52, 26), (50, 29), (48, 30), (45, 30), (42, 29),
     (39, 30), (37, 32), (36, 31), (34, 31), (33, 34), (30, 36), (27, 37)],
    # Africa
    [(-6, 35), (-1, 35), (3, 37), (10, 37), (11, 34), (15, 32), (20, 32),
     (25, 32), (30, 31), (32, 31), (34, 28), (36, 23), (38, 20), (39, 21),
     (43, 12), (48, 11), (51, 12), (51, 10), (46, 5), (42, 0), (40, -5),
     (40, -11), (36, -18), (33, -25), (28, -33), (20, -35), (17, -32),
     (15, -27), (12, -18), (13, -12), (9, -1), (9, 4), (4, 6), (-4, 5),
     (-8, 4), (-13, 8), (-16, 12), (-17, 15), (-16, 20), (-14, 25),
     (-10, 29)],
    # Madagascar
    [(44, -12), (47, -14), (48, -17), (47, -21), (45, -25), (44, -22),
     (43, -17)],
    # Asia (northern landmass; south edge along ~37-42N, southern regions drawn separately)
    [(30, 41), (36, 41), (41, 42), (44, 40), (48, 38), (52, 37), (57, 37),
     (62, 37), (67, 38), (70, 40), (74, 43), (78, 45), (83, 47), (88, 49),
     (93, 50), (98, 51), (103, 52), (108, 53), (113, 53), (118, 54),
     (123, 55), (128, 54), (133, 52), (138, 51), (141, 53), (143, 58),
     (148, 60), (154, 61), (159, 62), (163, 65), (168, 66), (173, 67),
     (178, 66), (178, 69), (170, 70), (162, 70), (155, 71), (148, 72),
     (140, 72), (132, 72), (124, 72), (117, 73), (110, 74), (103, 76),
     (96, 76), (89, 75), (82, 73), (75, 72), (68, 71), (62, 69), (56, 69),
     (50, 68), (45, 68), (40, 67), (35, 66), (33, 63), (31, 60), (30, 57),
     (29, 54), (30, 51), (32, 48), (35, 46), (38, 45), (40, 44), (38, 42),
     (35, 41), (32, 41)],
    # Central Asia + China (was unmapped sea: Beijing and New Delhi
    # floated in it). North edge is the Asia polygon's south edge,
    # traced back west; south edge follows the Himalayas and the China
    # coast, dipping around Korea so Seoul sits on land. The Black and
    # Caspian seas are filled at this scale, as before.
    [(52, 37), (57, 37), (62, 37), (67, 38), (70, 40), (74, 43), (78, 45),
     (83, 47), (88, 49), (93, 50), (98, 51), (103, 52), (108, 53),
     (113, 53), (118, 54), (123, 55), (128, 54), (133, 52), (138, 51),
     (141, 53), (140, 52), (136, 48), (133, 46), (130, 44), (129, 43),
     (128, 40), (127, 37), (126, 35), (124, 36), (122, 37), (121, 34),
     (121, 31), (121, 28), (119, 25), (116, 23), (113, 22), (110, 20),
     (108, 21), (105, 22), (102, 24), (98, 26), (95, 25), (92, 24),
     (88, 25), (84, 26), (80, 27), (76, 28), (72, 29), (68, 30), (64, 32),
     (60, 34), (56, 36)],
    # Arabia
    [(35, 29), (37, 32), (39, 30), (40, 28), (42, 25), (43, 21), (43, 17),
     (43, 13), (45, 12), (48, 14), (52, 15), (55, 17), (57, 20), (59, 23),
     (57, 26), (55, 27), (52, 26), (50, 29), (48, 30), (45, 30), (42, 29),
     (39, 30), (36, 31)],
    # India
    [(68, 23), (70, 21), (72, 19), (74, 14), (76, 9), (77, 8), (80, 8),
     (80, 13), (82, 16), (85, 19), (88, 22), (91, 22), (89, 24), (87, 26),
     (84, 25), (80, 26), (77, 28), (74, 29), (71, 28), (68, 26)],
    # SE Asia
    [(92, 22), (94, 18), (96, 16), (98, 12), (99, 9), (100, 6), (103, 1),
     (104, 2), (103, 6), (101, 8), (100, 10), (101, 13), (103, 12),
     (105, 10), (107, 11), (109, 13), (109, 17), (107, 20), (105, 22),
     (103, 22), (100, 22), (98, 24), (95, 25)],
    # Sumatra
    [(95, 5), (97, 3), (99, 0), (101, -2), (103, -4), (105, -5), (106, -6),
     (104, -5), (102, -3), (100, 0), (98, 3)],
    # Borneo
    [(109, 1), (111, 3), (113, 4), (116, 6), (118, 5), (119, 2), (118, -1),
     (117, -3), (114, -3), (111, -2), (109, 0)],
    # Java (drawn to its real latitude extremes so Cikande sits on
    # land; the old sliver was sub-pixel thin and the marker floated
    # in the sea south of the island)
    [(105, -5.8), (108, -6.0), (111, -6.5), (114, -7.5), (114, -8.5),
     (110, -8.2), (106, -7.8), (105, -6.8)],
    # New Guinea
    [(131, -1), (134, -2), (137, -2), (140, -3), (143, -4), (146, -6),
     (149, -9), (150, -10), (147, -9), (144, -8), (141, -7), (137, -6),
     (134, -4)],
    # Solomon Islands (drawn as the full island chain, 155-166E, so
    # Honiara's marker sits visibly on land; the real chain spans
    # ~155-170E, so this is the chain's true extent, not a fake island)
    [(155, -7), (158, -6), (162, -7.5), (166, -9), (166, -10.5),
     (162, -11.5), (158, -11), (155, -9.5)],
    # Japan
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
     (141, 38), (141, 41), (142, 43), (141, 45), (140, 43), (139, 39),
     (138, 37), (136, 35), (133, 34), (131, 32)],
    # Korea
    [(126, 35), (127, 35), (129, 36), (129, 38), (128, 40), (126, 40),
     (125, 39), (124, 37)],
    # Australia
    [(114, -22), (114, -28), (115, -32), (117, -34), (120, -34), (124, -33),
     (128, -32), (132, -32), (135, -35), (137, -35), (140, -38), (144, -38),
     (147, -38), (150, -37), (153, -32), (153, -28), (151, -24), (148, -20),
     (146, -19), (143, -15), (142, -11), (141, -13), (140, -17), (138, -17),
     (136, -15), (135, -12), (132, -11), (130, -13), (127, -14), (124, -16),
     (121, -18), (118, -20)],
    # Tasmania
    [(145, -41), (147, -41), (148, -42), (147, -43), (146, -43), (145, -42)],
    # New Zealand
    [(167, -46), (169, -44), (171, -42), (173, -40), (174, -38), (176, -37),
     (178, -38), (177, -39), (175, -40), (173, -41), (171, -43), (169, -45)],
]

# --- text helpers -------------------------------------------------------------

WARNINGS = []


def text_w(draw, s, fnt):
    return draw.textlength(s, font=fnt)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, line_h, max_lines=None,
                 label=""):
    lines = wrap(draw, text, fnt, width)
    if max_lines is not None and len(lines) > max_lines:
        WARNINGS.append("%s: %d lines, only %d fit: %r"
                        % (label, len(lines), max_lines, text[:60]))
        lines = lines[:max_lines]
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=fnt, fill=fill)
    return y + len(lines) * line_h


def centre(draw, y, text, fnt, fill, cx=W // 2):
    draw.text((cx - text_w(draw, text, fnt) / 2, y), text, font=fnt, fill=fill)


def hrule(draw, y, x0=MARGIN, x1=W - MARGIN, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# --- sections -----------------------------------------------------------------

def draw_masthead(draw):
    y = 16
    # top line
    draw.text((MARGIN, y), "36 STORIES  \u00b7  6 CONTINENTS  \u00b7  ONE DAY",
              font=F_TOPLINE, fill=GREY)
    right = "WORLD NEWS IN ONE IMAGE"
    draw.text((W - MARGIN - text_w(draw, right, F_TOPLINE), y), right,
              font=F_TOPLINE, fill=GREY)
    y += 22
    centre(draw, y, "THE WORLD TODAY", F_TITLE, INK)
    y += 72
    # black date band
    draw.rectangle([MARGIN, y, W - MARGIN, y + 34], fill=INK)
    centre(draw, y + 5, "TUESDAY  24  NOVEMBER  2026", F_DATE, PAPER)
    y += 42
    centre(draw, y, "The day\u2019s most consequential stories, from Gaza to "
           "Canberra \u2014 what happened, as reported.",
           F_SUB, GREY)
    y += 22
    hrule(draw, y, width=2)
    return y + 8


def draw_leads(draw, y0):
    col_w = (CW - 2 * 20) // 3  # 312
    gap = 20
    top = y0
    bottom = top
    for i, (kicker, head, body) in enumerate(LEADS):
        x = MARGIN + i * (col_w + gap)
        y = top
        draw.text((x, y), kicker, font=F_KICK, fill=RED)
        y += 19
        y = draw_wrapped(draw, x, y, head, F_HEAD, col_w, INK, 24,
                         max_lines=2, label="lead %d headline" % i)
        y += 4
        y = draw_wrapped(draw, x, y, body, F_BODY, col_w, INK, 17,
                         max_lines=4, label="lead %d body" % i)
        bottom = max(bottom, y)
        if i < 2:
            draw.line([(x + col_w + gap // 2, top),
                       (x + col_w + gap // 2, top + 138)],
                      fill=(200, 200, 200), width=1)
    return bottom + 6


def draw_section_header(draw, y, text):
    draw.text((MARGIN, y), text, font=F_SECT, fill=INK)
    tw = text_w(draw, text, F_SECT)
    draw.line([(MARGIN + tw + 10, y + 8), (W - MARGIN, y + 8)],
              fill=RULE, width=1)
    return y + 20


def draw_grid(draw, y0):
    cols, rows = 5, 3
    gap_x, gap_y = 12, 10
    cell_w = (CW - (cols - 1) * gap_x) // cols   # 187
    cell_h = 88
    for idx, (kicker, body) in enumerate(GRID):
        r, c = divmod(idx, cols)
        x = MARGIN + c * (cell_w + gap_x)
        y = y0 + r * (cell_h + gap_y)
        draw.text((x, y), kicker, font=F_GKICK, fill=RED)
        draw_wrapped(draw, x, y + 15, body, F_GBODY, cell_w, INK, 13,
                     max_lines=5, label="grid %d" % idx)
        if c < cols - 1:
            draw.line([(x + cell_w + gap_x // 2, y),
                       (x + cell_w + gap_x // 2, y + cell_h - 6)],
                      fill=(220, 220, 220), width=1)
    return y0 + rows * cell_h + (rows - 1) * gap_y


def draw_briefs(draw, y0):
    cols, rows = 2, 9
    gap_x = 24
    col_w = (CW - gap_x) // 2  # 476
    row_h = 21
    for idx, (kicker, body) in enumerate(BRIEFS):
        r, c = divmod(idx, cols)
        x = MARGIN + c * (col_w + gap_x)
        y = y0 + r * row_h
        head = kicker + " \u2014 "
        hw = text_w(draw, head, F_BRIEF_B)
        draw.text((x, y), head, font=F_BRIEF_B, fill=INK)
        # first line starts after the kicker; continuation lines full width
        first_w = col_w - hw
        lines = wrap(draw, body, F_BRIEF, first_w)
        if len(lines) > 1:
            # re-wrap the overflow at full width
            rest = " ".join(lines[1:])
            rest_lines = wrap(draw, rest, F_BRIEF, col_w)
            lines = [lines[0]] + rest_lines
        if len(lines) > 2:
            WARNINGS.append("brief %d: %d lines: %r"
                            % (idx, len(lines), body[:50]))
            lines = lines[:2]
        draw.text((x + hw, y), lines[0], font=F_BRIEF, fill=INK)
        if len(lines) > 1:
            draw.text((x, y + 11), lines[1], font=F_BRIEF, fill=INK)
    return y0 + rows * row_h


def draw_map(draw, y0, height):
    # header
    draw.text((MARGIN, y0), "WHERE IT HAPPENED", font=F_MAP_H, fill=INK)
    sub = "19 places from today\u2019s stories, numbered"
    draw.text((W - MARGIN - text_w(draw, sub, F_LEGEND), y0 + 2), sub,
              font=F_LEGEND, fill=GREY)
    map_y = y0 + 20
    map_h = height - 20 - 31  # room for 2 legend lines + gap
    map_x0, map_w = MARGIN, CW
    lat_top, lat_bot = 72.0, -55.0

    def project(lat, lon):
        px = map_x0 + (lon + 180.0) / 360.0 * map_w
        py = map_y + (lat_top - lat) / (lat_top - lat_bot) * map_h
        return (px, py)

    draw.rectangle([map_x0, map_y, map_x0 + map_w, map_y + map_h],
                   fill=SEA, outline=RULE, width=1)
    for poly in CONTINENTS:
        pts = [project(lat, lon) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)

    # markers
    for num, _name, lat, lon in MARKERS:
        px, py = project(lat, lon)
        r = 7
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        label = str(num)
        tw = text_w(draw, label, F_NUM)
        th = 9
        draw.text((px - tw / 2, py - th / 2 - 1), label, font=F_NUM,
                  fill=(255, 255, 255))

    # legend, two lines
    ly = map_y + map_h + 5
    line1 = "  \u00b7  ".join("%d %s" % (n, name)
                             for n, name, _la, _lo in MARKERS[:10])
    line2 = "  \u00b7  ".join("%d %s" % (n, name)
                             for n, name, _la, _lo in MARKERS[10:])
    draw.text((MARGIN, ly), line1, font=F_LEGEND, fill=INK)
    draw.text((MARGIN, ly + 13), line2, font=F_LEGEND, fill=INK)
    return ly + 26


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # double outer border
    draw.rectangle([8, 8, W - 9, H - 9], outline=INK, width=2)
    draw.rectangle([12, 12, W - 13, H - 13], outline=INK, width=1)

    y = draw_masthead(draw)
    y = draw_leads(draw, y)
    hrule(draw, y, width=1)
    y = draw_section_header(draw, y + 6, "AROUND THE WORLD")
    y = draw_grid(draw, y)
    hrule(draw, y + 4, width=1)
    y = draw_section_header(draw, y + 10, "IN BRIEF")
    y = draw_briefs(draw, y)
    hrule(draw, y + 2, width=1)
    map_bottom = draw_map(draw, y + 8, H - MARGIN - 8 - (y + 8))
    if map_bottom > H - MARGIN - 6:
        WARNINGS.append("map overflows: bottom %d" % map_bottom)

    # footer
    foot = ("All 36 stories happened or were first reported on Tuesday "
            "24 November 2026.")
    centre(draw, H - 24, foot, F_FOOT, GREY)

    img.save(OUT, format="PNG")
    return OUT


if __name__ == "__main__":
    path = render()
    size = os.path.getsize(path)
    print("wrote %s (%d bytes)" % (path, size))
    for w in WARNINGS:
        print("WARNING:", w)
    if size > 1048576:
        print("WARNING: over the 1 MiB gate")
