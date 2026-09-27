#!/usr/bin/env python3
"""Build seven SVG diagrams and the offline all-orders proof reading edition.

Uses only Python's standard library. ALL-ORDERS-PROOF.md is the prose source.
The small renderer supports this document's Markdown subset and supplies
explicit native MathML for its named display equations; it is not a TeX parser.
"""
from html import escape
from math import cos, sin, pi
from pathlib import Path
import re

ASSETS = Path(__file__).resolve().parent
EXPLAINERS = ASSETS.parent
SOURCE = EXPLAINERS / "ALL-ORDERS-PROOF.md"
INK, MUTED, LINE = "#202d3a", "#526171", "#d8dedf"
COLORS = {"R": "#bd3847", "B": "#2168af", "G": "#237953"}
DASH = {"R": "", "B": "9 5", "G": "2 6"}
TINT = {"R": "#fcf0f1", "B": "#edf4fc", "G": "#edf7f1"}


class Diagram:
    def __init__(self, key, title, description, height):
        self.key = key
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" '
            f'role="img" aria-labelledby="{key}-title {key}-desc">',
            f'<title id="{key}-title">{escape(title)}</title>',
            f'<desc id="{key}-desc">{escape(description)}</desc>',
            '<rect width="1000" height="100%" rx="16" fill="white"/>',
        ]
        self.text(30, 30, "KRENN–GU / THE ALL-ORDERS PROOF", 12, MUTED, weight=700)
        self.text(30, 66, title, 25, weight=700)

    def text(self, x, y, text, size=18, color=INK, anchor="start", weight=400):
        self.parts.append(
            f'<text x="{x:g}" y="{y:g}" font-family="system-ui,sans-serif" '
            f'font-size="{size}" fill="{color}" text-anchor="{anchor}" '
            f'font-weight="{weight}">{escape(str(text))}</text>')

    def box(self, x, y, w, h, fill="#f5f7f8"):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                          f'rx="12" fill="{fill}" stroke="{LINE}"/>')

    def line(self, p, q, color=LINE, width=2, dash=""):
        self.parts.append(
            f'<line x1="{p[0]:g}" y1="{p[1]:g}" x2="{q[0]:g}" y2="{q[1]:g}" '
            f'stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}" '
            'stroke-linecap="round"/>')

    def arrow(self, p, q):
        self.line(p, q, MUTED)
        dx, dy = q[0] - p[0], q[1] - p[1]
        length = (dx * dx + dy * dy) ** .5
        ux, uy = dx / length, dy / length
        for sign in (-1, 1):
            self.line((q[0] - 8 * ux + sign * 5 * uy,
                       q[1] - 8 * uy - sign * 5 * ux), q, MUTED)

    def node(self, point, label, color=INK, radius=16):
        self.parts.append(
            f'<circle cx="{point[0]:g}" cy="{point[1]:g}" r="{radius}" '
            f'fill="white" stroke="{color}" stroke-width="2"/>')
        self.text(point[0], point[1] + 5, label, 15, INK, "middle", 650)

    def graph(self, points, edges, selected=None, radius=16):
        for u, v, color in edges:
            active = selected is None or frozenset((u, v)) in selected
            self.line(points[u], points[v], COLORS[color] if active else LINE,
                      4 if active else 1.6, DASH[color] if active else "")
        for key, point in points.items():
            self.node(point, key, radius=radius)

    def finish(self):
        result = "\n".join(self.parts + ["</svg>"]) + "\n"
        (ASSETS / (self.key + ".svg")).write_text(result)
        return result


def ring(x, y, radius, n):
    return {i: (x + radius * cos(-pi / 2 + 2 * pi * i / n),
                y + radius * sin(-pi / 2 + 2 * pi * i / n)) for i in range(n)}


def square(x, y, width, height):
    return {1: (x, y), 2: (x + width, y),
            3: (x + width, y + height), 4: (x, y + height)}


def cycle(n):
    return [(i, (i + 1) % n, "R" if i % 2 == 0 else "B") for i in range(n)]


def diagrams():
    figures = {}

    d = Diagram("01-cancellation", "Finding a mixed matching is not enough",
                "Two different red pairings of four vertices have contributions plus one "
                "and minus one to the same pure output. Their sum is zero. The same "
                "cancellation principle is the obstacle when ruling out mixed outputs.", 390)
    for x, pairs, title, product in [
        (30, [(1, 2, "R"), (3, 4, "R")], "Pair 12 and 34", "+1 × +1 = +1"),
        (350, [(1, 3, "R"), (2, 4, "R")], "Pair 13 and 24", "+1 × −1 = −1"),
    ]:
        d.box(x, 105, 280, 220, TINT["R"])
        d.text(x + 140, 137, title, 19, anchor="middle", weight=650)
        d.graph(square(x + 55, 175, 170, 90), pairs)
        d.text(x + 140, 305, product, 20, COLORS["R"], "middle", 650)
    d.arrow((646, 220), (680, 220))
    d.text(830, 164, "Same color list", 18, MUTED, "middle")
    d.text(830, 207, "RRRR", 26, COLORS["R"], "middle", 700)
    d.text(830, 259, "+1 − 1 = 0", 27, anchor="middle", weight=700)
    d.text(500, 366, "Amplitudes add over matchings; individual products need not survive.",
           18, MUTED, "middle")
    figures[d.key] = d.finish()

    d = Diagram("02-roadmap", "The proof makes cancellation impossible",
                "Six steps in order: exact target, higher-response identities, same-color "
                "edges, the new endpoint identity, one edge per vertex per color, and "
                "a mixed matching with nonzero amplitude. Arrows run across the top "
                "row, down, then back along the bottom row.", 490)
    cards = [
        (30, 110, "1 / ASSUMPTION", "Exact target output",
         ["Three nonzero pure amplitudes", "Every mixed amplitude is zero"]),
        (355, 110, "2 / TWO FORMAL COPIES", "Higher responses vanish",
         ["On every two-color palette", "Including the terminal degree"]),
        (680, 110, "3 / MATRIX INVERSES", "Edges have one color",
         ["Both endpoints agree", "Derived in the original basis"]),
        (680, 305, "4 / NEW CLOSING STEP", "The endpoint identity",
         ["Every supported edge contributes", "the entire pure amplitude β"]),
        (355, 305, "5 / COUNT AT A VERTEX", "One edge per color",
         ["β = kβ, with β nonzero", "Therefore k = 1"]),
        (30, 305, "6 / GRAPH CONTRADICTION", "An unwanted output",
         ["Three matchings force a mixed one", "Its nonzero product cannot cancel"]),
    ]
    for x, y, tag, title, lines in cards:
        d.box(x, y, 290, 145, TINT["G"] if tag.startswith("4") else "#f5f7f8")
        d.text(x + 15, y + 28, tag, 12, MUTED, weight=700)
        d.text(x + 15, y + 63, title, 20, weight=700)
        for j, line in enumerate(lines):
            d.text(x + 15, y + 96 + 25 * j, line, 15)
    for p, q in [((326, 183), (349, 183)), ((651, 183), (674, 183)),
                 ((825, 265), (825, 295)), ((674, 378), (651, 378)),
                 ((349, 378), (326, 378))]:
        d.arrow(p, q)
    figures[d.key] = d.finish()

    d = Diagram("03-replicas", "Two copies give a symmetry of the same calculation",
                "Two formal copies share identical pairing rules. Orthogonal mixing "
                "preserves those rules. A local two-color determinant changes sign "
                "under reflection. With an odd number of sites the total changes "
                "sign and must vanish; with an even number it remains invariant.", 485)
    d.box(30, 108, 300, 175)
    d.text(180, 142, "Identical pairing rules", 20, anchor="middle", weight=650)
    d.text(180, 192, "Copy 1: X, g₁", 24, COLORS["R"], "middle")
    d.text(180, 239, "Copy 2: Y, g₂", 24, COLORS["B"], "middle")
    d.arrow((347, 195), (416, 195))
    d.text(382, 173, "mix", 15, MUTED, "middle")
    d.box(435, 108, 535, 175, TINT["B"])
    d.text(702, 145, "A determinant at each retained site", 20, anchor="middle", weight=650)
    d.text(702, 193, "Xᵣ Yᵦ − Xᵦ Yᵣ", 29, anchor="middle")
    d.text(702, 239, "Rotation: unchanged   ·   Reflection: sign flips", 18, MUTED, "middle")
    for x, title, formula, note in [
        (30, "ODD NUMBER OF SITES", "S = −S  ⇒  S = 0", "Gives higher-response identities"),
        (515, "EVEN NUMBER OF SITES", "S stays unchanged", "Constrains the endpoint matrix"),
    ]:
        d.box(x, 315, 455, 128)
        d.text(x + 227, 343, title, 13, MUTED, "middle", 700)
        d.text(x + 227, 383, formula, 24, anchor="middle", weight=650)
        d.text(x + 227, 417, note, 17, MUTED, "middle")
    figures[d.key] = d.finish()

    d = Diagram("04-endpoint", "Each supported edge accounts for the whole amplitude",
                "Condition on an edge pq of weight d. Its contribution is d times "
                "the retained hafnian alpha. The new identity makes this beta. "
                "Three supported edges at p would therefore give beta equals "
                "three beta, impossible when beta is nonzero.", 515)
    d.box(30, 108, 455, 342)
    d.text(257, 143, "One supported edge pq", 21, anchor="middle", weight=650)
    d.line((130, 199), (380, 199), COLORS["R"], 4)
    d.node((130, 199), "p")
    d.node((380, 199), "q")
    d.text(255, 184, "weight d ≠ 0", 17, COLORS["R"], "middle")
    pts = square(160, 270, 190, 88)
    for i in pts:
        for j in pts:
            if i < j:
                d.line(pts[i], pts[j], LINE, 2)
    for key, point in pts.items():
        d.node(point, str(key), MUTED)
    d.text(257, 395, "Retained matching sum: α", 19, MUTED, "middle")
    d.text(257, 431, "Its contribution: dα = β", 23, COLORS["R"], "middle", 700)
    d.box(515, 108, 455, 342, TINT["R"])
    d.text(742, 143, "Suppose p had three such edges", 20, anchor="middle", weight=650)
    points = {"p": (605, 265), "q₁": (862, 196), "q₂": (862, 265), "q₃": (862, 334)}
    for q in ["q₁", "q₂", "q₃"]:
        d.line(points["p"], points[q], COLORS["R"], 4)
    for key, point in points.items():
        d.node(point, key)
    for y in [205, 259, 315]:
        d.box(715, y - 22, 44, 31, "white")
        d.text(737, y, "β", 21, COLORS["R"], "middle", 700)
    d.text(742, 393, "β = β + β + β is impossible", 22, anchor="middle", weight=650)
    d.text(742, 426, "Exactly one supported edge can remain.", 17, MUTED, "middle")
    d.text(500, 487, "The equality is derived from the exact target assumptions, not from positivity.",
           18, MUTED, "middle")
    figures[d.key] = d.finish()

    d = Diagram("05-polynomial", "A finite polynomial cannot hide its highest power",
                "For b with leading term u z to the k, d b has coefficient d u "
                "at degree k and b prime has coefficient zero there. With d "
                "and u nonzero, the equation b prime plus d b equals zero "
                "is impossible. Nonzero constants fail as well.", 455)
    d.text(500, 120, "Assume b(z) = u zᵏ + lower powers, with u ≠ 0 and k ≥ 1.", 21, anchor="middle")
    columns = [455, 650, 835]
    for x, label in zip(columns, ["coefficient of zᵏ", "coefficient of zᵏ⁻¹", "lower powers"]):
        d.text(x, 170, label, 16, MUTED, "middle", 650)
    for y, name, values in [
        (224, "Differentiate: b′", ["0", "ku", "…"]),
        (291, "Multiply: db", ["du ≠ 0", "∗", "…"]),
        (358, "Add: b′ + db", ["du ≠ 0", "∗", "…"]),
    ]:
        d.box(30, y - 35, 940, 55, TINT["R"] if y == 358 else "#f5f7f8")
        d.text(52, y, name, 22, weight=650)
        for x, value in zip(columns, values):
            d.text(x, y, value, 25, COLORS["R"] if x == 455 else INK, "middle", 650)
    d.text(500, 416, "For k = 0: b′ = 0 and db ≠ 0. Thus the only polynomial solution is b = 0.",
           18, MUTED, "middle")
    figures[d.key] = d.finish()

    d = Diagram("06-chords", "Interlacing chords leave even paths to pair",
                "On an eight-cycle the third-color chords 0–4 and 1–5 interlace. "
                "Removing their endpoints leaves paths 2–3 and 6–7 and two empty "
                "paths. The two chords and two remaining cycle edges form a mixed "
                "perfect matching, producing GGRRGGRR.", 480)
    edges = cycle(8) + [(0, 4, "G"), (1, 5, "G")]
    selected = {frozenset(pair) for pair in [(0, 4), (1, 5), (2, 3), (6, 7)]}
    for x, title, highlight in [(30, "Two opposite-parity chord types", None),
                                (515, "Complete the matching on the paths", selected)]:
        d.box(x, 105, 455, 310)
        d.text(x + 227, 139, title, 19, anchor="middle", weight=650)
        d.graph(ring(x + 227, 264, 93, 8), edges, highlight)
        d.text(x + 227, 393,
               "Green: 0–4 (even) and 1–5 (odd)" if highlight is None else "Green 0–4, 1–5; red 2–3, 6–7",
               17, MUTED, "middle")
    d.text(500, 454, "The resulting color list GGRRGGRR has one nonzero matching contribution.",
           18, MUTED, "middle")
    figures[d.key] = d.finish()

    d = Diagram("07-boundary", "Four sites work; beyond four, mixed outputs intervene",
                "At four sites the red pairing 12,34, blue pairing 13,24 and "
                "green pairing 14,23 exhaust all matchings. The six-site "
                "example has a mixed matching green 0–3, blue 1–2 and red "
                "4–5, with color list GBBGRR. Unit weights give amplitude one.", 510)
    d.box(30, 105, 455, 340)
    d.text(257, 141, "K₄: exactly three matchings", 21, anchor="middle", weight=650)
    for x, color, pairs in [
        (65, "R", [(1, 2, "R"), (3, 4, "R")]),
        (210, "B", [(1, 3, "B"), (2, 4, "B")]),
        (355, "G", [(1, 4, "G"), (2, 3, "G")]),
    ]:
        pts = square(x, 205, 95, 102)
        d.graph(pts, pairs, radius=13)
        d.text(x + 47, 352, color * 4, 20, COLORS[color], "middle", 700)
    d.text(257, 398, "No mixed matching exists.", 20, MUTED, "middle")
    d.text(257, 428, "Unit weights: all three amplitudes are 1.", 17, MUTED, "middle")
    d.box(515, 105, 455, 340)
    d.text(742, 141, "Six sites: one mixed matching", 21, anchor="middle", weight=650)
    edges = cycle(6) + [(0, 3, "G"), (1, 4, "G"), (2, 5, "G")]
    selected = {frozenset(pair) for pair in [(0, 3), (1, 2), (4, 5)]}
    d.graph(ring(742, 266, 95, 6), edges, selected)
    d.text(742, 398, "GBBGRR", 23, anchor="middle", weight=700)
    d.text(742, 428, "Unit weights: its unwanted amplitude is 1.", 17, MUTED, "middle")
    d.text(500, 483, "Color also uses line pattern: red solid, blue dashed, green dotted.",
           18, MUTED, "middle")
    figures[d.key] = d.finish()
    return figures


def mi(x):
    return "<mi>" + escape(x) + "</mi>"


def mo(x):
    return "<mo>" + escape(x) + "</mo>"


def mn(x):
    return "<mn>" + str(x) + "</mn>"


def row(*parts):
    return "<mrow>" + "".join(parts) + "</mrow>"


def sub(base, index):
    return "<msub>" + mi(base) + mi(index) + "</msub>"


def power(base, exponent):
    return "<msup>" + mi(base) + mi(exponent) + "</msup>"


def frac(top, bottom):
    return "<mfrac>" + row(top) + row(bottom) + "</mfrac>"


def haf(argument):
    return '<mi mathvariant="normal">haf</mi>' + mo("(") + row(argument) + mo(")")


def equations():
    beta, eta, alpha, d = map(mi, ["β", "η", "α", "d"])
    retained = mi("B") + mo("[") + mi("V") + mo("∖") + mo("{") + mi("p") + mo(",") + mi("q") + mo("}") + mo("]")
    endpoint = sub("B", "pq") + haf(retained)
    gap = '<mspace width="1.2em"/>'
    pd = lambda x: frac(mo("∂") + mi(x), mo("∂") + mi("z"))
    return {
        "target": (mi("H") + mo("=")
                   + mo("+").join(sub("τ", c) + power(c, "V") for c in ["R", "B", "G"])
                   + gap + sub("τ", "R") + sub("τ", "B") + sub("τ", "G") + mo("≠") + mn(0)),
        "alternating": sub("X", "R") + sub("Y", "B") + mo("−") + sub("X", "B") + sub("Y", "R"),
        "scaling": ("<msup>" + row(mi("g"), mo("("), frac(mi("L"), "<msqrt><mn>2</mn></msqrt>"), mo(")"))
                    + mn(2) + "</msup>" + mo("=") + mi("g") + mo("(") + mi("L") + mo(")")),
        "inverse": (sub("B", "hh") + sub("C", "h") + mo("=") + sub("τ", "h") + mi("I")
                    + gap + sub("B", "ih") + sub("C", "h") + mo("=") + mn(0)
                    + gap + mo("(") + mi("i") + mo("≠") + mi("h") + mo(")")),
        "hafnian": haf(mi("B")) + mo("=") + mo("+").join(
            sub("B", x) + sub("B", y) for x, y in [("12", "34"), ("13", "24"), ("14", "23")]),
        "expansion": beta + mo("=") + "<munder>" + mo("∑") + row(mi("q"), mo("≠"), mi("p")) + "</munder>" + endpoint,
        "endpoint": endpoint + mo("=") + beta,
        "degree": beta + mo("=") + mi("k") + beta,
        "matrix": ("<mtable columnalign=\"left\"><mtr><mtd>" + mi("T") + mo("=") + mi("a") + mi("I") + mo("+")
                   + mi("b") + mi("P") + '<msup><mi>Q</mi><mi mathvariant="normal">T</mi></msup>'
                   + gap + mi("a") + mo(",") + mi("b") + mo("∈")
                   + '<mi mathvariant="double-struck">C</mi><mo>[</mo><mi>σ</mi><mo>,</mo><mi>ρ</mi><mo>,</mo><mi>z</mi><mo>]</mo>'
                   + "</mtd></mtr><mtr><mtd>" + mi("σ") + mo("=") + mi("P") + mo("·") + mi("P")
                   + gap + mi("ρ") + mo("=") + mi("Q") + mo("·") + mi("Q")
                   + gap + mi("z") + mo("=") + mi("P") + mo("·") + mi("Q") + "</mtd></mtr></mtable>"),
        "ode": pd("b") + mo("+") + d + mi("b") + mo("=") + mn(0) + gap
               + pd("a") + mo("+") + d + mi("a") + mo("=") + beta + eta,
        "forced": mi("b") + mo("=") + mn(0) + gap + mi("a") + mo("=") + frac(beta + eta, d),
        "finish": eta + alpha + mo("=") + frac(beta + eta, d) + gap + mo("⟹") + gap + beta + mo("=") + d + alpha,
    }


BT = chr(96)
TOKEN = re.compile(r"\[[^\]]+\]\([^)]+\)|" + BT + r"[^" + BT + r"]+" + BT + r"|\*\*.+?\*\*|\*[^*]+\*")


def inline(text):
    pieces, end = [], 0
    for match in TOKEN.finditer(text):
        pieces.append(escape(text[end:match.start()]))
        token = match[0]
        if token.startswith("["):
            label, url = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", token).groups()
            pieces.append(f'<a href="{escape(url, quote=True)}">{escape(label)}</a>')
        elif token.startswith(BT):
            pieces.append("<code>" + escape(token[1:-1]) + "</code>")
        elif token.startswith("**"):
            pieces.append("<strong>" + escape(token[2:-2]) + "</strong>")
        else:
            pieces.append("<em>" + escape(token[1:-1]) + "</em>")
        end = match.end()
    pieces.append(escape(text[end:]))
    return "".join(pieces)


def slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def render(markdown, figures):
    math = equations()
    used_math, used_figures = set(), set()
    headings = re.findall(r"^## (.+)$", markdown, re.M)
    contents = '<nav class="contents" aria-label="Guide contents"><strong>In this guide</strong><ol>'
    for title in headings:
        short_title = re.sub(r"^\d+\.\s*", "", title)
        contents += f'<li><a href="#{slug(title)}">{escape(short_title)}</a></li>'
    contents += "</ol></nav>"
    parts, index, contents_added = [], 0, False
    blocks = re.split(r"\n\s*\n", markdown.strip())
    while index < len(blocks):
        block = blocks[index]
        index += 1
        formula = re.fullmatch(r"<!-- math: ([\w-]+) -->\n\$\$\n(.*?)\n\$\$", block, re.S)
        figure = re.fullmatch(r"!\[([^\]]*)\]\(all-orders-assets/([\w-]+)\.svg\)", block)
        if formula:
            key, latex = formula.groups()
            if key in used_math:
                raise ValueError("Duplicate equation: " + key)
            used_math.add(key)
            parts.append('<div class="equation' + (' key-equation' if key == "endpoint" else '') + '">'
                         '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">'
                         '<semantics><mrow>' + math[key] + '</mrow>'
                         '<annotation encoding="application/x-tex">' + escape(latex) +
                         '</annotation></semantics></math></div>')
        elif figure:
            _, key = figure.groups()
            used_figures.add(key)
            caption = blocks[index].replace("\n", " ")
            if not caption.startswith("*Figure ") or not caption.endswith("*"):
                raise ValueError("Missing caption for " + key)
            index += 1
            parts.append('<figure><div class="diagram">' + figures[key] +
                         '</div><figcaption>' + inline(caption[1:-1]) +
                         f' <a href="all-orders-assets/{key}.svg">Full-size diagram</a>'
                         '</figcaption></figure>')
        elif block.startswith("# "):
            parts.append("<h1>" + inline(block[2:]) + "</h1>")
        elif block.startswith("## "):
            if not contents_added:
                parts.append(contents)
                contents_added = True
            title = block[3:]
            parts.append(f'<h2 id="{slug(title)}">' + inline(title) + "</h2>")
        elif block.startswith("- "):
            items = re.split(r"\n(?=- )", block)
            parts.append("<ul>" + "".join("<li>" + inline(" ".join(item[2:].splitlines())) + "</li>"
                                         for item in items) + "</ul>")
        else:
            if "$$" in block or "<!--" in block:
                raise ValueError("Unrendered markup: " + block[:100])
            cls = ' class="status"' if block.startswith("**Status.") else ""
            parts.append("<p" + cls + ">" + inline(" ".join(block.splitlines())) + "</p>")
    if used_math != set(math) or used_figures != set(figures):
        raise ValueError("Equation or figure inventory differs from Markdown")
    return "\n".join(parts)


STYLE = """
:root{color-scheme:light;--ink:#202d3a;--muted:#526171;--blue:#2168af}
*{box-sizing:border-box}
body{margin:0;background:#f2f5f7;color:var(--ink);font:18px/1.7 system-ui,sans-serif}
main{max-width:1060px;margin:auto;padding:40px 28px 80px}
h1{font-size:clamp(34px,5vw,50px);line-height:1.12;letter-spacing:-.035em;max-width:900px}
h2{font-size:28px;line-height:1.3;margin:2.7em 0 1em;scroll-margin-top:24px;max-width:900px}
p,ul{max-width:880px}a{color:var(--blue);text-underline-offset:3px}
li{padding-left:4px;margin:10px 0}
code{font:1em/1.5 ui-monospace,monospace;background:#e8eef2;padding:1px 4px;border-radius:4px}
.status{background:#edf7f1;border-left:4px solid #237953;padding:16px 22px;border-radius:6px;font-size:16px}
.contents{background:white;border:1px solid #d8dedf;border-radius:12px;padding:20px 26px;margin-top:32px;font-size:16px}
.contents ol{columns:2;column-gap:38px;margin-bottom:0;padding-left:22px}.contents li{break-inside:avoid}
figure{margin:32px 0}.diagram{overflow-x:auto;border:1px solid #d8dedf;border-radius:16px;background:white}
svg{display:block;width:100%;min-width:720px;height:auto}
figcaption{font-size:15px;line-height:1.6;color:var(--muted);margin:10px 2px;max-width:920px}
.equation{background:white;border:1px solid #d8dedf;border-radius:10px;padding:22px;margin:25px 0;overflow-x:auto}
.equation math{font-size:24px;width:max-content;min-width:100%;margin:0}
.key-equation{background:#edf7f1;border-color:#237953}
footer{margin-top:60px;padding-top:20px;border-top:1px solid #d8dedf;font-size:14px;color:var(--muted)}
@media(max-width:620px){main{padding:24px 16px 50px}.contents ol{columns:1}h2{font-size:25px}.equation math{font-size:22px}}
@media print{body{background:white;font-size:11pt}main{max-width:none;padding:0}.contents{display:none}
h2{break-after:avoid}figure,.equation{break-inside:avoid}svg{min-width:0}.diagram{overflow:visible}
code{background:none}.equation math{font-size:15pt}a{color:inherit}footer{font-size:9pt}}
"""


def main():
    figures = diagrams()
    content = render(SOURCE.read_text(), figures)
    html = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="description" content="An undergraduate guide with seven diagrams '
            'to the internally reviewed all-orders Krenn–Gu proof.">'
            '<title>How the all-orders Krenn–Gu proof works</title><style>' + STYLE +
            '</style></head><body><main><article>' + content +
            '</article><footer>Built from ALL-ORDERS-PROOF.md with Python’s standard library. '
            'Diagrams and native MathML equations are embedded; no network connection or '
            'JavaScript is required for reading. Source links refer to the surrounding repository.'
            '</footer></main></body></html>\n')
    output = EXPLAINERS / "ALL-ORDERS-PROOF.html"
    output.write_text(html)
    print(f"Built {len(figures)} SVGs and {output.name} ({len(html.encode()):,} bytes).")


if __name__ == "__main__":
    main()
