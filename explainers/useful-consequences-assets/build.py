#!/usr/bin/env python3
"""Build two vector diagrams and the self-contained interactive browser edition.

Uses Python's standard library. Does not change the other explainers.
"""
from html import escape
import json
from pathlib import Path

ASSETS = Path(__file__).resolve().parent
EXPLAINERS = ASSETS.parent
ROOT = EXPLAINERS.parent
COLORS = {"a": "#bd3847", "b": "#2168af", "c": "#237953"}
DASH = {"a": "", "b": "9 5", "c": "2 5"}
INK, MUTED = "#202d3a", "#526171"


class Diagram:
    def __init__(self, key, title, description, height):
        self.key = key
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {height}" '
                      f'role="img" aria-labelledby="{key}-title {key}-desc">',
                      f'<title id="{key}-title">{escape(title)}</title>',
                      f'<desc id="{key}-desc">{escape(description)}</desc>',
                      '<rect width="1000" height="100%" fill="white" rx="16"/>']
        self.text(30, 30, "KRENN–GU / USEFUL CONSEQUENCES", 12, MUTED, weight=700)
        self.text(30, 66, title, 25, weight=700)

    def text(self, x, y, value, size=18, color=INK, anchor="start", weight=400):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="system-ui,sans-serif" '
                          f'font-size="{size}" fill="{color}" text-anchor="{anchor}" '
                          f'font-weight="{weight}">{escape(str(value))}</text>')

    def box(self, x, y, w, h):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
                          'fill="#f5f7f8" stroke="#d8dedf"/>')

    def line(self, p, q, color="#b9c3ca", width=2, dash=""):
        self.parts.append(f'<line x1="{p[0]}" y1="{p[1]}" x2="{q[0]}" y2="{q[1]}" '
                          f'stroke="{color}" stroke-width="{width}" '
                          f'stroke-dasharray="{dash}" stroke-linecap="round"/>')

    def node(self, p, label, color=INK, radius=15):
        self.parts.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="{radius}" fill="white" '
                          f'stroke="{color}" stroke-width="2"/>')
        self.text(p[0], p[1] + 5, label, 14 if radius == 15 else 11, color, "middle", 650)

    def finish(self):
        value = "\n".join(self.parts + ["</svg>"]) + "\n"
        (ASSETS / (self.key + ".svg")).write_text(value)
        return value


def bipartite_diagram():
    d = Diagram("01-bipartite", "A whole architecture class is excluded at every size",
                'Illustrative equal shores. Exact GHZ forces diagonal edges. Deleting opposite '
                'sites leaves a nonzero two-color cofactor. The unwanted slice factors as the '
                'third-color edge weight times that cofactor, forcing every third-color edge to zero.', 460)
    for x in (30, 350, 670):
        d.box(x, 100, 300, 300)
    d.text(180, 132, "1. Two groups of output sites", 17, anchor="middle", weight=650)
    left = [(80, y) for y in (190, 260, 330)]
    right = [(280, y) for y in (190, 260, 330)]
    for p in left:
        for q in right:
            d.line(p, q, width=1.3)
    d.line(left[0], right[0], COLORS["a"], 4)
    for i, point in enumerate(left):
        d.node(point, "p" if i == 0 else "u" + str(i), COLORS["a"] if i == 0 else INK)
    for i, point in enumerate(right):
        d.node(point, "t" if i == 0 else "v" + str(i), COLORS["a"] if i == 0 else INK)
    d.text(180, 177, "a-colored edge", 15, COLORS["a"], "middle", 600)
    d.text(180, 379, "Every source crosses the partition", 15, MUTED, "middle")
    d.text(500, 132, "2. Delete p,t; keep colors b,c", 17, anchor="middle", weight=650)
    pts = [(400, 210), (400, 305), (600, 210), (600, 305)]
    for i, j, c in ((0, 2, "b"), (1, 3, "b"), (0, 3, "c"), (1, 2, "c")):
        d.line(pts[i], pts[j], COLORS[c], 3, DASH[c])
    for point, label in zip(pts, ("u1", "u2", "v1", "v2")):
        d.node(point, label)
    d.text(500, 379, "Whole remaining tensor: K ≠ 0", 16, MUTED, "middle", 600)
    d.text(820, 132, "3. The mixed slice must vanish", 17, anchor="middle", weight=650)
    d.text(820, 215, "a-edge weight × K = 0", 22, anchor="middle", weight=650)
    d.text(820, 260, "K is nonzero", 20, MUTED, "middle")
    d.text(820, 310, "Every a-edge has weight 0", 19, COLORS["a"], "middle", 700)
    d.text(820, 379, "Contradiction: no all-a output", 16, MUTED, "middle")
    d.text(500, 436, "The proof uses whole cofactors, so complex cancellation is fully retained.", 18, MUTED, "middle")
    return d.finish()


def prism_diagram(model):
    d = Diagram("02-prism", "Four matchings make the fidelity–rate tradeoff explicit",
                'The outer triangle is sites 0,1,2 and the inner triangle 3,4,5. '
                'Triangle edges have amplitude t; connecting edges have amplitude t omega. '
                'Three pure matchings have amplitude t cubed omega and the one mixed '
                'matching has amplitude t cubed omega cubed.', 690)
    d.box(30, 110, 350, 490)
    d.text(205, 145, "Nine pair sources", 20, anchor="middle", weight=650)
    points = {0: (70, 200), 1: (340, 200), 2: (205, 465),
              3: (130, 270), 4: (280, 270), 5: (205, 380)}
    for edge in model["edges"]:
        p, q = edge["ends"]
        c = edge["color"]
        d.line(points[p], points[q], COLORS[c], 4, DASH[c])
    for v, point in points.items():
        d.node(point, str(v))
    d.text(82, 250, "tω", 16, COLORS["b"], "middle", 650)
    d.text(329, 250, "tω", 16, COLORS["c"], "middle", 650)
    d.text(227, 430, "tω", 16, COLORS["a"], "middle", 650)
    d.text(205, 520, "Six triangle edges: t", 18, MUTED, "middle")
    d.text(205, 550, "Three connecting edges: tω", 18, MUTED, "middle")
    d.text(205, 580, "a: red     b: blue     c: green", 15, MUTED, "middle")
    panels = [(410, 110, "a", "aaaaaa · t³ω"), (700, 110, "b", "bbbbbb · t³ω"),
              (410, 365, "c", "cccccc · t³ω"), (700, 365, None, "bcabca · t³ω³")]
    for x, y, color, title in panels:
        d.box(x, y, 270, 235)
        d.text(x + 135, y + 30, title, 20, COLORS.get(color, INK), "middle", 650)
        pts = {0: (x + 50, y + 63), 1: (x + 220, y + 63), 2: (x + 135, y + 207),
               3: (x + 90, y + 100), 4: (x + 180, y + 100), 5: (x + 135, y + 157)}
        for edge in model["edges"]:
            p, q = edge["ends"]
            d.line(pts[p], pts[q], "#d5dce1", 1.2)
        for edge in model["edges"]:
            selected = edge["color"] == color if color else edge["omega_power"] == 1
            if selected:
                p, q = edge["ends"]
                c = edge["color"]
                d.line(pts[p], pts[q], COLORS[c], 4, DASH[c])
        for v, point in pts.items():
            d.node(point, str(v), radius=10)
    d.text(500, 640, "H / t³ = ω(aaaaaa + bbbbbb + cccccc) + ω³(bcabca)", 23, anchor="middle", weight=650)
    d.text(500, 674, "Reducing ω suppresses the unwanted amplitude faster than the desired amplitudes.", 18, MUTED, "middle")
    return d.finish()


HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Useful consequences of the Krenn–Gu results</title>
<style>
:root{color-scheme:light;--ink:#202d3a;--muted:#526171;--blue:#2168af}
*{box-sizing:border-box}body{margin:0;background:#f2f5f7;color:var(--ink);font:18px/1.65 system-ui,sans-serif}
main{max-width:1060px;margin:auto;padding:38px 28px 70px}h1{font-size:clamp(32px,5vw,48px);line-height:1.15;letter-spacing:-.03em}
h2{margin-top:2.4em;line-height:1.3;font-size:28px}p{max-width:850px}a{color:var(--blue)}nav{font-size:15px}
.status{border-left:4px solid #977b3d;background:#fcf7e9;padding:14px 20px;border-radius:6px;font-size:16px}
figure{margin:30px 0}figure .scroll{overflow-x:auto;border:1px solid #d8dedf;border-radius:16px;background:white}
svg{display:block;width:100%;min-width:650px}figcaption{font-size:15px;color:var(--muted);margin:9px 2px}
.formula{padding:18px 22px;background:white;border-radius:10px;overflow-x:auto;font-size:21px;white-space:nowrap}
.calculator{background:white;border:1px solid #d8dedf;border-radius:16px;padding:26px;margin-top:24px}
input[type=range]{width:100%;accent-color:var(--blue);margin:22px 0}.ends{display:flex;justify-content:space-between;font-size:14px;color:var(--muted)}
.metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:25px 0}
.metric{background:#edf4fc;padding:18px;border-radius:12px}.metric span{display:block;font-size:14px}.metric strong{display:block;font-size:26px;line-height:1.3;margin-top:7px}
.settings{display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:16px;color:var(--muted)}
small{font-size:14px;color:var(--muted)}code{background:#e6edf2;padding:3px 6px;border-radius:4px;font-size:14px}
@media(max-width:620px){main{padding:24px 16px}.metrics{grid-template-columns:1fr}.settings{grid-template-columns:1fr}.metric strong{font-size:28px}}
</style></head><body><main>
<nav><a href="README.md">All explainers</a> · <a href="USEFUL-CONSEQUENCES.md">Full written explanation</a> · <a href="../notes/useful-consequences-2026-09-26.md">Proofs and assumptions</a></nav>
<h1>What can we use the results for?</h1>
<p>We can discard a whole family of exact-state designs, bound unwanted output in individual designs, and calculate an achievable fidelity–success tradeoff.</p>
<p class="status"><strong>September 26, 2026 research follow-up.</strong> Written deductions and exact checks are available. These consequences have not received a separate independent audit or admission to the certified spine. The all-size exclusion uses certified inputs.</p>
<h2>1. Exclude bipartite output-pair graphs at every size</h2>
<p>If every pair connects opposite groups of output sites, an exact three-color GHZ state is impossible for every even number of sites at least four. Diagonality and binary cofactor nonvanishing force every edge of a chosen third color to disappear.</p>
<figure><div class="scroll">__BIPARTITE__</div><figcaption>The six drawn sites illustrate an argument that works for any equal shore size of at least two. The middle graph represents the whole remaining two-color tensor.</figcaption></figure>
<p>This excludes exact-state architectures even at sizes where the unrestricted conjecture remains open. It does not exclude approximate states or binary GHZ states.</p>
<h2>2. Measure unavoidable leakage in a candidate design</h2>
<p>For a diagonal bipartite source, let k<sub>pt</sub> be the norm of the blue/green output after deleting sites p,t, and q<sub>pt</sub> the pure red amplitude after that deletion. If every k<sub>pt</sub> is nonzero, set D<sub>p</sub> = Σ<sub>t</sub> |q<sub>pt</sub>|² / k<sub>pt</sub>². For equal phase-aligned pure amplitudes:</p>
<div class="formula">Fidelity F ≤ 3D<sub>p</sub> / (3D<sub>p</sub> + 1).</div>
<p>The bound follows from Cauchy–Schwarz and disjoint unwanted color patterns. It is a source-dependent diagnostic. Approximate sources must satisfy the stated diagonality assumption; exact diagonal reduction alone does not provide that assumption.</p>
<h2>3. A six-site source with an exact tradeoff</h2>
<p>The colored triangular prism has only four perfect matchings. Three give the desired pure-color outputs; one gives a mixed output. Set the six triangle amplitudes to t and the three connecting amplitudes to tω.</p>
<figure><div class="scroll">__PRISM__</div><figcaption>Color and line pattern identify a, b, c. Each small panel shows one complete matching and its amplitude.</figcaption></figure>
<div class="formula">F = 3 / (3 + ω⁴)</div>
<p>Small ω makes the unwanted amplitude small faster than the desired amplitudes. The approach-to-unit-fidelity phenomenon is already known from <a href="https://arxiv.org/html/2005.06443">THESEUS</a>; this page supplies an exact benchmark and optimized source settings.</p>
<section class="calculator" id="calculator" aria-labelledby="calculator-title">
<h2 id="calculator-title" style="margin-top:0">Explore the best balanced prism settings</h2>
<p>Adjust the target fidelity. The calculator chooses the source strengths that maximize the ideal probability among balanced sources on this colored prism.</p>
<label for="precision">Target fidelity, from 90% to 99.9999%</label>
<input id="precision" type="range" min="1" max="6" step="0.01" value="2" aria-describedby="scale-note">
<div class="ends"><span>90%</span><span>99.9999%</span></div>
<small id="scale-note">Logarithmic error scale: each full step divides infidelity by ten.</small>
<div class="metrics" aria-live="polite" aria-atomic="true">
<div class="metric"><span>Target fidelity</span><strong id="fidelity">99%</strong></div>
<div class="metric"><span>Ideal probability per trial</span><strong id="probability">0.143898%</strong></div>
<div class="metric"><span>Mean trials per selected event</span><strong id="trials">695</strong></div>
</div>
<div class="settings"><div>Each triangle source: <strong id="triangle">0.565653</strong></div>
<div>Each connecting source: <strong id="vertical">0.236005</strong></div></div>
<p><small>Source settings are the amplitudes λ in √(1−|λ|²) Σ λᵏ|k,k⟩, not laser powers. The calculator includes all nine vacuum-normalization factors.</small></p>
<noscript><p>The displayed default is for 99% fidelity. Enable JavaScript to vary the target; the written guide includes a static table.</p></noscript>
</section>
<p><strong>Model:</strong> nine phase-coherent pair sources acting on disjoint optical modes; perfect mode matching; no loss; and selection of exactly one photon at each site without resolving away the color superposition. This is ideal postselection, not heralding an undetected usable state or forecasting detector count rates.</p>
<p>With x = ω² and s = t², the probability and optimal setting are:</p>
<div class="formula">P(s,x) = s³x(3+x²)(1−s)⁶(1−sx)³<br>s* = 2 / [3+2x+√(9−4x+4x²)]</div>
<p>The proof permits arbitrary weights on this graph while requiring equal phase-aligned pure amplitudes. Concavity first makes the triangle strengths equal and the connecting strengths equal. A quadratic then determines the unique optimum in s.</p>
<h2>The remaining useful question</h2>
<p>Our exact exclusions imply that perfect fidelity cannot be approached at fixed source-coefficient budget while retaining nonzero output strength at six, eight, or ten sites. The prism provides an achievable rate. A quantitative upper bound across all architectures is still open in this work.</p>
<p>In the balanced prism class, P* is asymptotic to 0.01690√(1−F): reducing error by a factor of 100 costs about a factor of 10 in probability. No claim is made that this exponent or constant is globally optimal.</p>
<p><strong>Universal-rate follow-up:</strong> the <a href="../notes/universal-rate-bound-feasibility-2026-09-26.md">feasibility assessment</a> proves that some power-law bound exists for all complex sources at the excluded sizes. It also establishes an explicit square-root upper bound for all nonnegative six-site sources, with optimal exponent in that class.</p>
<p><strong>Complex-weight progress:</strong> a <a href="../notes/complex-rate-bound-2026-09-26.md">new local stability proof</a> establishes the square-root rate bound in a full neighborhood of the prism limit, allowing all 135 complex source entries. It also rules out a cubic polynomial certificate even with the balance equations included. Other zero-output limits remain to be controlled for a universal complex bound. These results have exact reproducible checks and await independent audit.</p>
<p><strong>Beyond the prism:</strong> the <a href="RATE-BOUNDARIES.md">illustrated boundary investigation</a> excludes two different zero-output limits and supplies rank tests that every possible high-fidelity limit must pass. The remaining singular response cases still need analysis.</p>
<h2>Reproduce the calculation</h2>
<p><code>python3 computations/useful-consequences-2026-09-26/verify.py</code></p>
<p>The standard-library checker reconstructs the matchings, verifies 19,683 occupation vectors and exact polynomial identities, and tests the leakage formula with rational weights. See the <a href="../computations/useful-consequences-2026-09-26/README.md">replay details</a> and <a href="../computations/useful-consequences-2026-09-26/calibration.csv">calibration CSV</a>. These checks support the written proofs; they do not replace independent mathematical review.</p>
</main><script>
function calculate(infidelity) {
  const fidelity = 1 - infidelity;
  const x = Math.sqrt(3 * infidelity / fidelity);
  const s = 2 / (3 + 2*x + Math.sqrt(9 - 4*x + 4*x*x));
  const probability = s**3 * x * (3+x*x) * (1-s)**6 * (1-s*x)**3;
  return {fidelity, probability, trials:1/probability, triangle:Math.sqrt(s), vertical:Math.sqrt(s*x)};
}
function update() {
  const slider = document.getElementById('precision');
  const result = calculate(10 ** -Number(slider.value));
  const digits = Math.max(0, Math.ceil(Number(slider.value))-2);
  const fidelityText = (100*result.fidelity).toFixed(digits+2).replace(/\.?0+$/, '') + '%';
  document.getElementById('fidelity').textContent = fidelityText;
  document.getElementById('probability').textContent = (100*result.probability).toPrecision(6) + '%';
  document.getElementById('trials').textContent = Math.round(result.trials).toLocaleString('en-US');
  document.getElementById('triangle').textContent = result.triangle.toFixed(6);
  document.getElementById('vertical').textContent = result.vertical.toFixed(6);
  slider.setAttribute('aria-valuetext', fidelityText + ' target fidelity');
}
document.getElementById('precision').addEventListener('input', update);
update();
</script></body></html>
'''


def main():
    model = json.loads((ROOT / "computations/useful-consequences-2026-09-26/prism.json").read_text())
    page = HTML.replace("__BIPARTITE__", bipartite_diagram()).replace("__PRISM__", prism_diagram(model))
    (EXPLAINERS / "USEFUL-CONSEQUENCES.html").write_text(page)
    print("Built two SVG diagrams and USEFUL-CONSEQUENCES.html")


if __name__ == "__main__":
    main()
