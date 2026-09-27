#!/usr/bin/env python3
"""Build the six-site SVGs and offline HTML reading edition.

Usage: python3 explainers/six-site-assets/build_explainer.py --marked /path/to/marked.esm.js
Python uses only the standard library; HTML conversion uses Node and marked.
The eight displayed formulas have explicit, accessible native MathML renderings.
"""
import argparse
from html import escape
import importlib.util
from math import cos, sin, pi
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ASSETS = Path(__file__).resolve().parent
ROOT = ASSETS.parent
spec = importlib.util.spec_from_file_location('explainer_diagrams', ROOT / 'explainer-assets/build_diagrams.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
Diagram, ring = base.Diagram, base.ring
INK, MUTED, LINE, COLORS, TINTS = base.INK, base.MUTED, base.LINE, base.COLORS, base.TINTS
FIGURES = []


def add(d, caption):
    FIGURES.append((d.key, d.finish(), caption))


d = Diagram('01-roadmap', 'The short proof: structure leaves nowhere for cancellation to hide',
            'Two imported structural lemmas imply color degree at most two. The inverse-cofactor '
            'identity excludes degree two, leaving one perfect matching per color. Those matchings '
            'force a mixed output with exactly one nonzero term. An older certificate proof is independent.', 395)
cards = [
    (30, 'INPUTS A + B', ['Diagonal edges', 'Inverse cofactors', 'Zero neighborhood blocks']),
    (275, 'LINEAR ALGEBRA', ['Six rows, six columns', 'Degree ≤ 2', 'Degree 2 is impossible']),
    (520, 'GRAPH THEORY', ['Each color is a matching', 'Colors cannot share pairs', 'Red + blue form a cycle']),
    (765, 'CONTRADICTION', ['Green must cross', 'One mixed output', 'One nonzero product']),
]
for x, title, lines in cards:
    d.box(x, 110, 205, 174, '#edf4fc' if x == 30 else '#f5f7f8')
    d.text(x+15, 140, title, 13, MUTED, weight=700)
    for j, line in enumerate(lines):
        d.text(x+15, 180+j*31, line, 14 if len(line)>24 else 15, weight=600 if j == 2 else 400)
    if x < 765:
        d.arrow(x+214, 200, x+235)
d.text(500, 327, 'The lemmas are the hard inputs; the six-site deduction is worked out below.', 18, MUTED, 'middle')
d.text(500, 365, 'Separate earlier route: rank-one blocks → 19 defect graphs → exact certificates.', 17, MUTED, 'middle')
add(d, 'Figure 1. The newer route separates two substantial structural inputs from an elementary six-site deduction. The earlier certificate proof has its own dependencies.')

d = Diagram('02-zero-block', 'Too many neighbors would make the cofactor matrix singular',
            'If p had three red neighbors u,v,w, its closed neighborhood S would have four vertices. '
            'The four corresponding rows of the blue cofactor would be zero in the four S columns, '
            'leaving only two columns for four independent rows. This contradicts invertibility.', 485)
d.box(30, 102, 260, 290)
d.text(160, 134, 'Suppose red-degree ≥ 3', 18, anchor='middle', weight=650)
pts = {'p':(160,190), 'u':(70,300), 'v':(160,330), 'w':(250,300)}
d.graph(pts, [('p',q,'R') for q in 'uvw'])
d.text(160, 375, 'Choose S = {p,u,v,w}', 17, MUTED, 'middle')
d.arrow(307, 245, 345)
x0, y0, cell = 400, 155, 35
d.text(470, 124, '4 columns in S', 16, COLORS['R'], 'middle', 650)
d.text(605, 124, '2 left', 16, COLORS['B'], 'middle', 650)
for r in range(6):
    for c in range(6):
        fill = TINTS['R'] if r<4 and c<4 else TINTS['B'] if r<4 else '#f5f7f8'
        d.box(x0+c*cell, y0+r*cell, cell, cell, fill, LINE, 0)
        d.text(x0+c*cell+cell/2, y0+r*cell+25, '0' if r==c or (r<4 and c<4) else '∗', 22,
               COLORS['R'] if r<4 and c<4 else MUTED, 'middle')
d.text(375, 228, '4', 20, COLORS['R'], 'middle', 700)
d.text(375, 251, 'rows', 12, MUTED, 'middle')
d.text(505, 399, 'The blue cofactor matrix', 17, MUTED, 'middle')
d.text(675, 182, 'These four rows must', 19)
d.text(675, 212, 'be linearly independent.', 19)
d.text(675, 268, 'But they fit in a space', 19)
d.text(675, 298, 'of dimension only two.', 19)
d.text(675, 353, 'Impossible.', 23, COLORS['R'], weight=700)
d.text(500, 454, 'In general: s independent rows supported in 6 − s columns require s ≤ 6 − s.', 18, MUTED, 'middle')
add(d, 'Figure 2. The displayed four-vertex subset already gives a contradiction if a vertex has three or more same-color neighbors. An asterisk marks an entry not determined by the highlighted zero block; it may also be zero.')

d = Diagram('03-degree-two', 'Two neighbors force the remaining triangle to vanish',
            'In one color, p has precisely neighbors r and s with weights a and b. For q among the '
            'other three vertices, the off-diagonal cofactor identity gives zero equals 2ab times '
            'the edge weight between the other two vertices. Varying q kills every edge in that triangle.', 465)
d.box(30, 104, 430, 303)
pts = {'p':(245,154), 'r':(117,231), 's':(373,231), 'q':(115,347), 'u':(245,298), 'v':(374,347)}
d.graph(pts, [('p','r','R'),('p','s','R')])
d.text(166, 175, 'a ≠ 0', 17, COLORS['R'], 'middle', 650)
d.text(325, 175, 'b ≠ 0', 17, COLORS['R'], 'middle', 650)
for u,v in [('q','u'),('u','v'),('q','v')]:
    d.line(pts[u],pts[v],MUTED,2,'4 5')
    x=(pts[u][0]+pts[v][0])/2; y=(pts[u][1]+pts[v][1])/2
    d.box(x-13,y-15,26,28,'white','white',4)
    d.text(x,y+6,'0',20,COLORS['R'],'middle',700)
for q in 'quv':
    d.node(*pts[q],q)
d.text(245, 390, 'E = {q,u,v}: all internal weights become zero', 16, MUTED, 'middle')
d.text(500, 142, 'Delete r,q:  p must pair with s', 21, weight=650)
d.text(500, 180, 'C[r,q] = b M[u,v]', 23)
d.text(500, 225, 'Delete s,q:  p must pair with r', 21, weight=650)
d.text(500, 263, 'C[s,q] = a M[u,v]', 23)
d.box(490, 292, 480, 101, TINTS['R'])
d.text(730, 333, '0 = a·b M[u,v] + b·a M[u,v]', 22, anchor='middle')
d.text(730, 372, '0 = 2ab M[u,v]   ⇒   M[u,v] = 0', 22, COLORS['R'], 'middle', 650)
d.text(500, 441, 'Every full matching needs an edge inside E, so its product is zero. The pure amplitude vanishes.', 17, MUTED, 'middle')
add(d, 'Figure 3. Only the two displayed edges touch p in this color; other edges incident to r and s may exist. The equations force all three E-edges to vanish, destroying every pure-color perfect matching.')

d = Diagram('04-forced-mixed', 'A green crossing forces one mixed output with no cancellation',
            'Red edges 12,34,56 and blue edges 23,45,61 form an alternating six-cycle. '
            'Its shores are 1,3,5 and 2,4,6. A green perfect matching must cross these odd shores. '
            'After relabeling, choose green 14. Together with blue 23 and red 56 this gives GBBGRR.', 565)
d.box(30, 105, 475, 350)
d.text(267, 137, 'Odd shore', 17, MUTED, 'middle')
d.text(267, 420, 'Even shore', 17, MUTED, 'middle')
pts={1:(107,185),3:(267,185),5:(427,185),2:(107,365),4:(267,365),6:(427,365)}
d.graph(pts,base.CYCLE)
d.line(pts[1],pts[4],COLORS['G'],5,'2 7')
for q in [1,4]: d.node(*pts[q],q,COLORS['G'])
d.text(180, 292, 'G', 26, COLORS['G'], 'middle', 700)
d.arrow(518, 280, 555)
d.box(570, 105, 400, 350)
d.text(770, 141, 'Forced mixed matching', 21, anchor='middle', weight=650)
pts2={1:(637,210),4:(900,210),2:(637,270),3:(900,270),5:(637,330),6:(900,330)}
d.graph(pts2,[(1,4,'G'),(2,3,'B'),(5,6,'R')],node_colors={1:'G',4:'G',2:'B',3:'B',5:'R',6:'R'})
d.text(770, 201, 'green', 17, COLORS['G'], 'middle')
d.text(770, 261, 'blue', 17, COLORS['B'], 'middle')
d.text(770, 321, 'red', 17, COLORS['R'], 'middle')
d.word(654, 390, 'GBBGRR')
d.text(500, 492, 'Three vertices on each shore cannot all pair internally: green must cross.', 20, anchor='middle', weight=650)
d.text(500, 535, 'GBBGRR has exactly two sites of each color → exactly one compatible matching → nonzero amplitude.', 17, MUTED, 'middle')
add(d, 'Figure 4. Only one green edge is needed; its other edges are intentionally omitted. The odd-sized shores force some green crossing, and symmetry lets us label it 14. Red is solid, blue dashed, and green dotted.')

# Each component tuple is (path/cycle, vertex count). Its shape completely
# identifies a maximum-degree-two graph up to isomorphism.
TYPES = [
    [('P',1)]*6,
    [('P',2)]+[('P',1)]*4,
    [('P',2)]*2+[('P',1)]*2,
    [('P',3)]+[('P',1)]*3,
    [('P',2)]*3,
    [('P',3),('P',2),('P',1)],
    [('P',4),('P',1),('P',1)],
    [('C',3)]+[('P',1)]*3,
    [('P',5),('P',1)],
    [('P',4),('P',2)],
    [('P',3)]*2,
    [('C',3),('P',2),('P',1)],
    [('C',4),('P',1),('P',1)],
    [('P',6)],
    [('C',3),('P',3)],
    [('C',4),('P',2)],
    [('C',5),('P',1)],
    [('C',6)],
    [('C',3)]*2,
]


def type_label(parts):
    from collections import Counter
    return ' + '.join((str(n) if n>1 else '')+kind+str(order).translate(str.maketrans('123456','₁₂₃₄₅₆'))
                      for (kind,order),n in Counter(parts).items())


d = Diagram('05-census', 'The earlier certified route: exactly 19 defect-graph types',
            'All graphs on six vertices with maximum degree at most two, up to relabeling. '
            'Each component is a path P or cycle C, with its vertex count in the subscript. '
            'Grouped by edge count, there are 1,1,2,4,5,4,2 types, totaling 19. '
            'A drawn edge marks an aggregate block of rank different from one, including a zero block.', 1240)
d.text(30, 104, 'Draw an edge when its 3 × 3 aggregate block has rank ≠ 1. Every vertex has degree ≤ 2.', 18, MUTED)
for i,parts in enumerate(TYPES):
    x=30+(i%3)*325; y=130+(i//3)*151
    d.box(x,y,310,138)
    d.text(x+16,y+27,type_label(parts),18,weight=650)
    edge_count=sum(n if kind=='C' else n-1 for kind,n in parts)
    d.text(x+294,y+27,f'{edge_count} edges',13,MUTED,'end')
    # Reserve a horizontal span for each component; cycles use two dimensions.
    widths=[(n-1)*34+12 if kind=='P' else 78 for kind,n in parts]
    gap=13; total=sum(widths)+gap*(len(parts)-1)
    scale=min(1,275/total); cursor=x+(310-total*scale)/2
    for (kind,n),width in zip(parts,widths):
        w=width*scale; mid=cursor+w/2
        if kind=='P':
            points=[(cursor+6*scale+j*34*scale,y+91) for j in range(n)]
            edges=[(j,j+1) for j in range(n-1)]
        else:
            radius=32*scale
            points=[(mid+radius*cos(-pi/2+2*pi*j/n),y+88+radius*sin(-pi/2+2*pi*j/n)) for j in range(n)]
            edges=[(j,(j+1)%n) for j in range(n)]
        for a,b in edges: d.line(points[a],points[b],INK,2.2)
        for px,py in points:
            d.parts.append(f'<circle cx="{px:g}" cy="{py:g}" r="4.5" fill="{INK}"/>')
        cursor+=w+gap*scale
d.text(30, 1220, 'Pₖ = path on k vertices (P₁ is isolated). Cₖ = cycle on k vertices. “+” means disjoint components.', 17, MUTED)
add(d, 'Figure 5. The complete finite census used in the older proof. These are defect graphs, not the red/blue/green support graphs from the short proof. Every box contains six vertices; exact certificate arguments exclude every box.')


# Small MathML vocabulary. Explicit rendering keeps the reading edition offline.
def row(*xs): return '<mrow>'+''.join(xs)+'</mrow>'
def mi(x): return '<mi>'+escape(x)+'</mi>'
def mn(x): return '<mn>'+str(x)+'</mn>'
def mo(x): return '<mo>'+escape(x)+'</mo>'
def txt(x): return '<mtext>'+escape(x)+'</mtext>'
def sub(x,y): return '<msub>'+x+y+'</msub>'
def sup(x,y): return '<msup>'+x+y+'</msup>'
def call(f,*args): return row(f,mo('('),*args,mo(')'))
def entry(f,*args): return row(f,mo('['),row(*sum(([a,mo(',')] for a in args[:-1]),[]),args[-1]),mo(']'))
M=mi('M'); C=mi('C'); h=mi('h'); k=mi('k'); p=mi('p'); q=mi('q'); u=mi('u'); v=mi('v'); r=mi('r'); s=mi('s'); a=mi('a'); b=mi('b')
Mh=sub(M,h); Ch=sub(C,h); tau=sub(mi('τ'),h)
haf='<mi mathvariant="normal">haf</mi>'
f1=row(call(sub(mi('H'),mi('A')),mi('c')),mo('='),
       '<munder>'+mo('∑')+row(mi('P'),mo('∈'),call('<mi mathvariant="normal">PM</mi>',mn(6)))+'</munder>',
       '<munder>'+mo('∏')+row(mo('{'),u,mo(','),v,mo('}'),mo('∈'),mi('P'),mo(','),u,mo('<'),v)+'</munder>',
       call(sub(mi('A'),row(u,v)),sub(mi('c'),u),mo(','),sub(mi('c'),v)))
f2=row(call(haf,entry(M,row(mo('{'),mn(1),mo(','),mn(2),mo(','),mn(3),mo(','),mn(4),mo('}')))),mo('='),
       sub(M,mn(12)),sub(M,mn(34)),mo('+'),sub(M,mn(13)),sub(M,mn(24)),mo('+'),sub(M,mn(14)),sub(M,mn(23)))
f3=row(Mh,Ch,mo('='),tau,sub(mi('I'),mn(6)),mo(','),txt('   '),Ch,mo('='),tau,sup(Mh,row(mo('−'),mn(1))))
f4=row(entry(sub(C,k),mi('S'),mi('S')),mo('='),mn(0))
f5=row(s,mo('≤'),mn(6),mo('−'),s,mo(','),txt('   '),s,mo('≤'),mn(3),mo(','),txt('   '),
       call(sub('<mi mathvariant="normal">deg</mi>',h),p),mo('≤'),mn(2))
f6=row(entry(C,r,q),mo('='),b,entry(M,u,v),mo(','),txt('   '),entry(C,s,q),mo('='),a,entry(M,u,v))
f7=row(mn(0),mo('='),entry(row(mo('('),M,C,mo(')')),p,q),mo('='),a,entry(C,r,q),mo('+'),b,entry(C,s,q),mo('='),mn(2),a,b,entry(M,u,v))
f8=row(call(sub(mi('H'),mi('A')),txt('GBBGRR')),mo('='),entry(sub(M,mi('G')),mn(1),mn(4)),
       entry(sub(M,mi('B')),mn(2),mn(3)),entry(sub(M,mi('R')),mn(5),mn(6)),mo('≠'),mn(0))
FORMULAS = [
    (r'H_A(c)=\sum_{P\in\operatorname{PM}(6)}\prod_{\{u,v\}\in P,\ u<v}A_{uv}(c_u,c_v).', f1, 'An output amplitude is the sum, over all perfect matchings, of the three edge weights multiplied together.'),
    (r'\operatorname{haf}(M[\{1,2,3,4\}])=M_{12}M_{34}+M_{13}M_{24}+M_{14}M_{23}.', f2, 'The four-site hafnian is M12 times M34 plus M13 times M24 plus M14 times M23.'),
    (r'M_h C_h=\tau_h I_6,\qquad C_h=\tau_h M_h^{-1}.', f3, 'M h times C h equals tau h times the identity; C h equals tau h times the inverse of M h.'),
    (r'C_k[S,S]=0.', f4, 'The S by S block of the other-color cofactor is zero.'),
    (r's\leq 6-s,\qquad s\leq3,\qquad \deg_h(p)\leq2.', f5, 's is at most six minus s, so s is at most three, and the color degree is at most two.'),
    (r'C[r,q]=bM[u,v],\qquad C[s,q]=aM[u,v].', f6, 'C r q equals b times M u v, and C s q equals a times M u v.'),
    (r'0=(MC)[p,q]=aC[r,q]+bC[s,q]=2abM[u,v].', f7, 'Zero equals the p q entry of M C, equals a C r q plus b C s q, equals two a b M u v.'),
    (r'H_A(GBBGRR)=M_G[1,4]M_B[2,3]M_R[5,6]\ne0.', f8, 'The mixed output GBBGRR has amplitude green 14 times blue 23 times red 56, which is nonzero.'),
]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--marked',required=True,type=Path,help='Path to marked.esm.js')
    args=parser.parse_args()
    md=(ROOT/'SIX-SITE-PROOF.md').read_text()
    # Reset generated blocks so repeated builds preserve the same source text.
    md=re.sub(r'<!-- six-figure:([^:]+):start -->.*?<!-- six-figure:\1:end -->',
              lambda m:f'<!-- six-figure:{m[1]} -->',md,flags=re.S)
    html_input=md
    for key,svg,caption in FIGURES:
        filename=key+'.svg'
        (ASSETS/filename).write_text(svg+'\n')
        marker=f'<!-- six-figure:{key} -->'
        assert md.count(marker)==1,marker
        md=md.replace(marker,f'<!-- six-figure:{key}:start -->\n\n![{caption}](six-site-assets/{filename})\n\n*{caption}*\n\n<!-- six-figure:{key}:end -->')
        figure=(f'<figure class="explainer-diagram" id="figure-{key}"><div class="diagram-scroll" tabindex="0" aria-label="Diagram; scroll horizontally on small screens">{svg}</div>'
                f'<figcaption>{escape(caption)}</figcaption><p class="diagram-hint"><a href="six-site-assets/{filename}">Open full-size diagram</a> · on small screens, scroll sideways</p></figure>')
        html_input=html_input.replace(marker,figure)
    found=re.findall(r'\\\[\s*(.*?)\s*\\\]',html_input,flags=re.S)
    assert found==[f[0] for f in FORMULAS], 'Displayed math changed; update its MathML rendering.'
    for latex,mathml,label in FORMULAS:
        exact='\\[\n'+latex+'\n\\]'
        html_input=html_input.replace(exact,f'<div class="equation"><math xmlns="http://www.w3.org/1998/Math/MathML" display="block" aria-label="{escape(label)}">{mathml}</math></div>')
    js='import {pathToFileURL} from "node:url"; import {readFileSync} from "node:fs"; const {marked}=await import(pathToFileURL(process.argv[1])); process.stdout.write(marked.parse(readFileSync(0,"utf8")));'
    body=subprocess.run(['node','--input-type=module','-e',js,str(args.marked.resolve())],input=html_input,text=True,capture_output=True,check=True).stdout
    body=re.sub(r'<p><strong>([1-9])\. (.*?)</strong></p>',r'<h2 id="part-\1">\1. \2</h2>',body)
    css=re.search(r'<style>(.*?)</style>',(ROOT/'EXPLAINER.html').read_text(),re.S)[1]
    css+='\n.equation math{min-width:max-content} .equation{line-height:1.6} .explainer-diagram{margin-left:0;margin-right:0}\n'
    nav='<nav aria-label="Proof guide"><a href="EXPLAINER.html">Larger explainer</a><a href="#part-2">Structural inputs</a><a href="#part-3">The deduction</a><a href="#part-8">Certified route</a><a href="SIX-SITE-PROOF.md">Markdown source</a></nav>'
    html=f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Why six sites cannot support three colors</title><style>{css}</style></head><body><main>{nav}{body}<footer>Six-site proof guide · September 25, 2026 · Diagrams and equations work offline.</footer></main></body></html>\n'
    (ROOT/'SIX-SITE-PROOF.md').write_text(md)
    (ROOT/'SIX-SITE-PROOF.html').write_text(html)
    print(f'Built {len(FIGURES)} SVG diagrams and {len(FORMULAS)} native MathML equations.')


if __name__=='__main__':
    main()
