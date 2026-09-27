#!/usr/bin/env python3
"""Build the explainer's vector diagrams and place them in both reading editions.

Uses only Python's standard library. Run from any directory. The HTML embeds
the SVGs so the reading edition remains usable without network dependencies.
"""
from html import escape
from itertools import combinations
from math import cos, sin, pi
from pathlib import Path
import re

ASSETS = Path(__file__).resolve().parent
ROOT = ASSETS.parent
INK = '#202d3a'
MUTED = '#526171'
LINE = '#d8dedf'
COLORS = {'R': '#bd3847', 'B': '#2168af', 'G': '#237953'}
TINTS = {'R': '#fcf0f1', 'B': '#edf4fc', 'G': '#edf7f1'}


class Diagram:
    def __init__(self, key, title, description, height):
        self.key, self.height = key, height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" '
            f'role="img" aria-labelledby="{key}-title {key}-desc">',
            f'<title id="{key}-title">{escape(title)}</title>',
            f'<desc id="{key}-desc">{escape(description)}</desc>',
            '<rect width="1000" height="100%" rx="16" fill="#fff"/>',
        ]
        self.text(30, 31, 'KRENN–GU / ' + key[:2], 12, MUTED, weight=700)
        self.text(30, 66, title, 25, weight=700)

    def text(self, x, y, content, size=18, fill=INK, anchor='start', weight=400):
        self.parts.append(
            f'<text x="{x:g}" y="{y:g}" font-family="system-ui, sans-serif" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}">{escape(str(content))}</text>')

    def box(self, x, y, w, h, fill='#f5f7f8', stroke=LINE, radius=12):
        self.parts.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" '
                          f'rx="{radius}" fill="{fill}" stroke="{stroke}"/>')

    def line(self, a, b, color=INK, width=2, dash='', opacity=1):
        self.parts.append(f'<line x1="{a[0]:g}" y1="{a[1]:g}" x2="{b[0]:g}" y2="{b[1]:g}" '
                          f'stroke="{color}" stroke-width="{width}" stroke-linecap="round" '
                          f'stroke-dasharray="{dash}" opacity="{opacity}"/>')

    def arrow(self, x1, y, x2, label=None):
        self.line((x1, y), (x2, y), MUTED)
        self.line((x2-8, y-5), (x2, y), MUTED)
        self.line((x2-8, y+5), (x2, y), MUTED)
        if label:
            self.text((x1+x2)/2, y-12, label, 14, MUTED, 'middle')

    def node(self, x, y, label, color=INK, faded=False):
        self.parts.append(f'<circle cx="{x:g}" cy="{y:g}" r="17" fill="white" '
                          f'stroke="{LINE if faded else color}" stroke-width="2.5"/>')
        self.text(x, y+6, label, 17, MUTED if faded else INK, 'middle', 650)

    def graph(self, points, edges, selected=None, node_colors=None, labels=None):
        for u, v, c in edges:
            active = selected is None or tuple(sorted((u, v))) in selected
            self.line(points[u], points[v], COLORS.get(c, '#b4bec5'),
                      4 if active and c in COLORS else 1.7,
                      {'B': '9 5', 'G': '2 6'}.get(c, ''), 1 if active else .22)
        for k, (x, y) in points.items():
            self.node(x, y, labels.get(k, k) if labels else k,
                      COLORS.get((node_colors or {}).get(k), INK))

    def word(self, x, y, word, gap=39, size=20):
        for i, c in enumerate(word):
            self.box(x+i*gap, y, 32, 36, TINTS[c], COLORS[c], 6)
            self.text(x+i*gap+16, y+25, c, size, COLORS[c], 'middle', 700)

    def finish(self):
        return '\n'.join(self.parts + ['</svg>'])


def ring(cx, cy, r, n=6):
    return {i+1: (cx+r*cos(-pi/2+2*pi*i/n), cy+r*sin(-pi/2+2*pi*i/n)) for i in range(n)}


def square(x, y, w=150, h=100, labels=(1, 2, 3, 4)):
    return dict(zip(labels, [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]))


K4 = [(u, v, '') for u, v in combinations(range(1, 5), 2)]
CYCLE = [(1, 2, 'R'), (3, 4, 'R'), (5, 6, 'R'),
         (2, 3, 'B'), (4, 5, 'B'), (1, 6, 'B')]
THIRD = CYCLE + [(1, 4, 'G'), (2, 5, 'G'), (3, 6, 'G')]
FIGURES = []


def add(d, anchor, caption):
    FIGURES.append(dict(key=d.key, svg=d.finish(), anchor=anchor, caption=caption))


d = Diagram('01-matching-term', 'A matching is one term in an output amplitude',
            'Six sites are paired as 12 red, 36 green, and 45 blue. With edge weights '
            '2, minus 1, and 3, this matching contributes minus 6 to the output RRGBBG. '
            'The output amplitude adds all matchings producing that same word.', 370)
d.box(30, 95, 280, 242)
pts = ring(170, 218, 87)
d.graph(pts, [(1, 2, 'R'), (3, 6, 'G'), (4, 5, 'B')],
        node_colors=dict(zip(range(1, 7), 'RRGBBG')))
d.text(214, 154, 'R · 2', 15, COLORS['R'], weight=650)
d.text(164, 191, 'G · −1', 15, COLORS['G'], weight=650)
d.text(92, 302, 'B · 3', 15, COLORS['B'], weight=650)
d.arrow(327, 216, 366)
d.text(390, 143, 'Read vertices 1 → 6', 17, MUTED)
for j in range(6):
    d.text(406+j*39, 180, j+1, 14, MUTED, 'middle')
d.word(390, 195, 'RRGBBG')
d.text(390, 270, 'One mixed color list', 17, MUTED)
d.arrow(635, 216, 675)
d.text(705, 144, 'Multiply within a matching', 17, MUTED)
d.text(705, 206, '2 × (−1) × 3 = −6', 23, weight=700)
d.text(705, 254, 'Then add contributions from', 17)
d.text(705, 280, 'all matchings with this list.', 17)
add(d, 'The weight of an event is the product of its edge weights.',
    'Figure 1. Pair first, multiply edge weights, then group by the inherited vertex colors. '
    'The displayed −6 is one matching contribution; other matchings could change the total.')

d = Diagram('02-four-site-exception', 'Four sites: the three pairings are exactly the three targets',
            'The red matching is 12 and 34; the blue matching is 13 and 24; '
            'the green matching is 14 and 23. These are all perfect matchings of K4. '
            'Unit weights give RRRR, BBBB, GGGG, each with amplitude one.', 377)
for x, c, pairs in [(30, 'R', [(1, 2), (3, 4)]),
                    (355, 'B', [(1, 3), (2, 4)]),
                    (680, 'G', [(1, 4), (2, 3)])]:
    d.box(x, 98, 290, 230, TINTS[c])
    d.text(x+145, 126, {'R': 'Red', 'B': 'Blue', 'G': 'Green'}[c], 18, COLORS[c], 'middle', 700)
    pts = square(x+65, 160, 160, 97)
    d.graph(pts, K4+[(u, v, c) for u, v in pairs], node_colors={k:c for k in pts})
    d.text(x+145, 305, c*4+'  ·  amplitude 1', 18, COLORS[c], 'middle', 650)
d.text(500, 357, 'No fourth pairing exists, so there is no unwanted mixed output.', 18, MUTED, 'middle')
add(d, 'These are all three perfect matchings of K₄.',
    'Figure 2. Faint edges show K₄; bold edges show one complete pairing. '
    'Each panel covers every vertex once, and together they exhaust all possibilities.')

d = Diagram('03-third-color-leak', 'Adding a third color creates new mixed pairings',
            'The six-cycle has two pure matchings. Adding green edges 14, 25, 36 gives '
            'six matchings: three pure and three mixed. The highlighted matching '
            '12 red, 36 green, 45 blue gives RRGBBG with amplitude one.', 445)
for x, title in [(30, 'Alternating cycle'), (520, 'Add the green matching')]:
    d.box(x, 98, 450, 294)
    d.text(x+225, 130, title, 20, anchor='middle', weight=650)
d.graph(ring(255, 231, 77), CYCLE)
d.text(255, 361, '2 matchings → 2 pure outputs', 18, MUTED, 'middle')
selected = {(1, 2), (3, 6), (4, 5)}
d.graph(ring(745, 231, 77), THIRD, selected, dict(zip(range(1, 7), 'RRGBBG')))
d.word(631, 340, 'RRGBBG')
d.text(500, 424, 'With unit weights, this mixed output has one contribution and cannot cancel.', 18, MUTED, 'middle')
add(d, 'That output has amplitude 1.',
    'Figure 3. The right panel highlights one of the three unwanted mixed matchings. '
    'Vertex numbers fix the order of the color list. This construction fails; the example alone is not a general impossibility proof.')

d = Diagram('04-cancellation', 'Two matchings can cancel in the same output',
            'Two all-red matchings on four sites have weights plus one and minus one. '
            'They both produce RRRR, so that amplitude is zero. This is a scalar '
            'cancellation example, not a full GHZ solution.', 360)
for x, pairs, title, product in [(30, [(1,2),(3,4)], 'Matching 12 / 34', '+1 × +1 = +1'),
                                (350, [(1,3),(2,4)], 'Matching 13 / 24', '+1 × −1 = −1')]:
    d.box(x, 95, 275, 222, TINTS['R'])
    d.text(x+137, 127, title, 18, anchor='middle', weight=650)
    pts = square(x+60, 159, 155, 80)
    d.graph(pts, [(u,v,'R') for u,v in pairs], node_colors={k:'R' for k in pts})
    d.text(x+137, 288, product, 19, COLORS['R'], 'middle', 650)
d.text(330, 215, '+', 28, anchor='middle')
d.arrow(645, 207, 698)
d.text(818, 144, 'Same output: RRRR', 20, anchor='middle', weight=650)
d.text(818, 211, '1 + (−1) = 0', 29, COLORS['R'], 'middle', 700)
d.text(818, 262, 'Two terms. Zero amplitude.', 17, MUTED, 'middle')
d.text(500, 343, 'Weights: w₁₂ = w₃₄ = w₁₃ = 1, w₂₄ = −1; the other edges are absent.', 17, MUTED, 'middle')
add(d, 'can vanish with supported matchings present:',
    'Figure 4. Cancellation happens between matchings producing the same color list. '
    'A positive red contribution and a negative red contribution can sum to zero. '
    'Contributions to different lists cannot cancel one another.')

d = Diagram('05-diagonal-reduction', 'The new reduction removes six coefficients per pair',
            'A general 3 by 3 endpoint-color block can have nine entries. '
            'The internally reviewed theorem forces its off-diagonal entries to zero '
            'in the original target basis, leaving RR, BB, GG. Across all site pairs '
            'these form three n by n scalar matrices, one per color.', 399)

def matrix(x, y, diagonal):
    for j,c in enumerate('RBG'):
        d.text(x+26+j*53,y-13,c,17,COLORS[c],'middle',700)
        d.text(x-18,y+32+j*53,c,17,COLORS[c],'middle',700)
    for row,c in enumerate('RBG'):
        for col,k in enumerate('RBG'):
            live = row == col
            d.box(x+53*col,y+53*row,51,51,TINTS[c] if live else '#f5f7f8',LINE,4)
            d.text(x+26+53*col,y+32+53*row,c+k if live or not diagonal else '0',
                   18, COLORS[c] if live else MUTED, 'middle', 650 if live else 400)

d.text(151,112,'General block Aᵤᵥ',19,anchor='middle',weight=650)
d.text(151,141,'Columns: color at v',14,MUTED,'middle')
matrix(74,170,False)
d.text(37,351,'Rows: color at u',14,MUTED)
d.arrow(256,248,365)
d.text(310,198,'Full three-color',15,MUTED,'middle')
d.text(310,220,'source equations',15,MUTED,'middle')
d.text(496,112,'Diagonal in the same basis',19,anchor='middle',weight=650)
d.text(496,141,'Only same-color entries remain',14,MUTED,'middle')
matrix(418,170,True)
d.arrow(598,248,693)
d.text(647,209,'Across all',15,MUTED,'middle')
d.text(647,230,'site pairs',15,MUTED,'middle')
for y,c in [(158,'R'),(221,'B'),(284,'G')]:
    d.box(720,y,247,49,TINTS[c],COLORS[c],8)
    d.text(844,y+32,'M'+{'R':'ᴿ','B':'ᴮ','G':'ᴳ'}[c]+'  ·  n × n site matrix',18,COLORS[c],'middle',650)
d.text(500,379,'Internally reviewed research · complex weights and matching cancellation remain.',17,MUTED,'middle')
add(d, 'To understand the gain, a pair originally has nine possible color coefficients:',
    'Figure 5. The left two arrays index endpoint colors; the three resulting matrices index sites. '
    'RR, RB, and so on denote aggregate coefficients, not fixed numerical values. '
    'The theorem applies to a full exact three-color source and is internally reviewed research.')

d = Diagram('06-cofactor', 'A cofactor sums the matchings left after deleting two sites',
            'Delete sites 1 and 2 from a six-site scalar weighted graph. '
            'The remaining sites 3,4,5,6 have three possible pairings. Their sum is '
            'C[1,2] = w34 w56 + w35 w46 + w36 w45. Only under the full-source '
            'hypotheses does the additional identity MC = tau I follow.', 420)
pts=ring(151,222,72)
d.graph(pts,[(u,v,'') for u,v in combinations(range(1,7),2)])
for p in [1,2]:
    x,y=pts[p]
    d.line((x-24,y-24),(x+24,y+24),COLORS['R'],3)
    d.line((x-24,y+24),(x+24,y-24),COLORS['R'],3)
d.text(151,112,'Original scalar graph',18,anchor='middle',weight=650)
d.text(151,329,'Delete p = 1 and q = 2',16,MUTED,'middle')
d.arrow(263,218,321)
d.text(439,112,'The surviving subgraph',18,anchor='middle',weight=650)
pts=square(368,167,143,101,labels=(3,4,5,6))
d.graph(pts,[(u,v,'') for u,v in combinations(range(3,7),2)])
d.text(439,329,'All its pairings contribute',16,MUTED,'middle')
d.arrow(544,218,596)
d.text(627,162,'C[1,2] =',24,weight=650)
for y,s in [(202,'w₃₄w₅₆'),(239,'+ w₃₅w₄₆'),(276,'+ w₃₆w₄₅')]:
    d.text(662,y,s,24)
d.box(30,353,940,45,'#edf4f6','#c0d4dd',8)
d.text(500,382,'For a full three-color source:  MC = τ I,  hence C = τ M⁻¹  (internally reviewed).',19,anchor='middle',weight=650)
add(d, 'where τₕ is the nonzero all-h amplitude.',
    'Figure 6. The cofactor definition is an actual matching sum. The inverse identity in the '
    'bottom band is an additional consequence of the full-source equations, not an identity '
    'satisfied by every weighted graph drawn above.')

d = Diagram('07-degree-frontier', 'Why six and eight collapse, ten needs more, and twelve remains',
            'The internally reviewed color-degree bound is one through n/2 minus two. '
            'Degree two is forbidden and degree one lies in an isolated edge. '
            'At six and eight sites only degree one remains. At ten, degrees one and three '
            'remain and a separate theorem excludes cubic components. At twelve, '
            'degrees one, three, and four remain; general exclusion is open.', 355)
cards=[(30,6,'1','{1}','Every color is a matching.','One-matching-color','theorem gives contradiction.'),
       (270,8,'2','{1}','Degree 2 is forbidden.','Again every color','would be a matching.'),
       (510,10,'3','{1, 3}','Cubic components remain.','A separate analytic proof','excludes these too.'),
       (750,12,'4','{1, 3, 4}','More components possible.','No general contradiction','has been established.')]
for x,n,bound,allowed,reason,line1,line2 in cards:
    d.box(x,104,220,203,'#fff8ec' if n==12 else '#f2f6f7', '#d6ac60' if n==12 else LINE)
    d.text(x+110,139,'n = '+str(n),25,anchor='middle',weight=700)
    d.text(x+110,169,'Degree at most '+bound,16,MUTED,'middle')
    d.text(x+110,202,'Allowed: '+allowed,20,anchor='middle',weight=650)
    d.text(x+110,231,reason,14,MUTED,'middle')
    d.text(x+110,267,line1,14,anchor='middle')
    d.text(x+110,289,line2,14,anchor='middle')
d.text(500,332,'These are consequences of the internally reviewed chain; the full conjecture stays open.',17,MUTED,'middle')
add(d, 'At n = 12, degree four becomes possible.',
    'Figure 7. The degree bound alone handles neither ten nor twelve sites. '
    'Ten requires the additional cubic-component argument. At twelve, both cubic and '
    'degree-four behavior remain to be covered by a general proof.')

d = Diagram('08-partition-product', 'After the reduction, every mixed output is a product of sums',
            'For an illustrative eight-site partition, sites 1,2,3,4 are red; 5,6 are blue; '
            '7,8 are green. The red hafnian has three terms, while the blue and green '
            'factors are single edges. Their product is the output amplitude. '
            'Every mixed partition of a full target must have at least one zero factor.', 414)
for x,w,c,title in [(30,411,'R','R = {1, 2, 3, 4}'),(465,234,'B','B = {5, 6}'),(725,245,'G','G = {7, 8}')]:
    d.box(x,105,w,204,TINTS[c],LINE)
    d.text(x+w/2,139,title,20,COLORS[c],'middle',650)
pts=square(129,178,200,65)
d.graph(pts,[(u,v,'R') for u,v in combinations(range(1,5),2)],node_colors={k:'R' for k in pts})
d.graph({5:(513,206),6:(651,206)},[(5,6,'B')],node_colors={5:'B',6:'B'})
d.graph({7:(776,206),8:(921,206)},[(7,8,'G')],node_colors={7:'G',8:'G'})
d.text(235,291,'R₁₂R₃₄ + R₁₃R₂₄ + R₁₄R₂₃',19,COLORS['R'],'middle',650)
d.text(582,291,'B₅₆',23,COLORS['B'],'middle',650)
d.text(847,291,'G₇₈',23,COLORS['G'],'middle',650)
d.text(453,292,'×',23,anchor='middle')
d.text(711,292,'×',23,anchor='middle')
d.text(500,354,'Amplitude = haf(Mᴿ[R]) × haf(Mᴮ[B]) × haf(Mᴳ[G])',22,anchor='middle',weight=650)
d.text(500,392,'At least one factor must vanish for every mixed partition. Cancellation can occur inside a factor.',16,MUTED,'middle')
add(d, 'Every contributing matching pairs red sites internally,',
    'Figure 8. An illustrative partition with four red, two blue, and two green sites. '
    'Only edges within the chosen color classes contribute to this word. The open task is '
    'to force some mixed partition whose factors are all nonzero, while allowing cancellation inside each sum.')


CSS = """
/* explainer-diagrams:start */
.explainer-diagram{margin:30px 0 36px;break-inside:avoid}
.diagram-scroll{overflow-x:auto;border:1px solid #d8dedf;border-radius:16px;background:white}
.explainer-diagram svg{display:block;width:100%;height:auto;min-width:720px}
.explainer-diagram figcaption{font-size:15px;line-height:1.6;color:#526171;margin:10px 4px 0;max-width:95ch}
.diagram-hint{font-size:12px;color:#526171;text-align:right;margin:5px 4px 0}
@media(max-width:760px){.explainer-diagram svg{min-width:820px}.diagram-scroll{overscroll-behavior-x:contain}}
@media print{.explainer-diagram svg{min-width:0}.diagram-scroll{overflow:visible}.diagram-hint{display:none}}
/* explainer-diagrams:end */
"""


def main():
    md = (ROOT / 'EXPLAINER.md').read_text()
    html = (ROOT / 'EXPLAINER.html').read_text()
    # Each block is replaced on repeat runs, so the builder is idempotent.
    block = r'\n?<!-- explainer-figure:.*?:start -->.*?<!-- explainer-figure:.*?:end -->\n?'
    md = re.sub(r'\n*<!-- explainer-figure:.*?:start -->.*?<!-- explainer-figure:.*?:end -->\n*',
                '\n\n', md, flags=re.S)
    html = re.sub(block, '', html, flags=re.S)
    html = re.sub(r'\n?/\* explainer-diagrams:start \*/.*?/\* explainer-diagrams:end \*/\n?', '', html, flags=re.S)
    for fig in FIGURES:
        filename = fig['key'] + '.svg'
        (ASSETS / filename).write_text(fig['svg'] + '\n')
        start = f"<!-- explainer-figure:{fig['key']}:start -->"
        end = f"<!-- explainer-figure:{fig['key']}:end -->"
        caption = fig['caption']
        md_block = f"\n\n{start}\n\n![{caption}](explainer-assets/{filename})\n\n*{caption}*\n\n{end}"
        a = md.index(fig['anchor'])
        paragraph_end = md.index('\n\n', a)
        md = md[:paragraph_end] + md_block + md[paragraph_end:]
        a = html.index(escape(fig['anchor']))
        paragraph_end = html.index('</p>', a) + len('</p>')
        html_block = (f'\n{start}\n<figure class="explainer-diagram" id="figure-{fig["key"]}">'
                      f'<div class="diagram-scroll" tabindex="0" aria-label="Diagram; scroll horizontally on small screens">{fig["svg"]}</div>'
                      f'<figcaption>{escape(caption)}</figcaption>'
                      f'<p class="diagram-hint"><a href="explainer-assets/{filename}">Open full-size diagram</a> · on small screens, scroll sideways</p>'
                      f'</figure>\n{end}\n')
        html = html[:paragraph_end] + html_block + html[paragraph_end:]
    html = html.replace('</style>', CSS + '</style>', 1)
    (ROOT / 'EXPLAINER.md').write_text(md)
    (ROOT / 'EXPLAINER.html').write_text(html)
    print(f'Built and embedded {len(FIGURES)} diagrams in EXPLAINER.md and EXPLAINER.html.')


if __name__ == '__main__':
    main()
