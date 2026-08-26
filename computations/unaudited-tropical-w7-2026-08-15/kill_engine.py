#!/usr/bin/env python3
"""UNAUDITED PROBE (W7 / Route T.1) -- per-cone kill engine for the colour-form
family.

Pinned HEAD: a41949965d41e5c63fb4bc1caf7b20c0df017856

For every face of the g-fan produced by colour_form_fan.py this script decides
whether the MIXED part of the initial system is TORUS-infeasible (no solution
with every cell nonzero), using a small catalogue of exactly-stated lemmas.

--------------------------------------------------------------------------
THE FACTORIZATION.  Fix a face and a mixed content n = (n_0,n_1,n_2) whose
argmin type set is A.  For a word chi of content n with colour classes S_c,

    in_w(Phi_chi) = sum_{m in A} (sum over matchings of type m of the monomial).

Build the COLOUR-BLOCK GRAPH of a type m: vertices = the colours c with n_c>0,
edges = {a,b} with m_ab>0.  The type-m sum factorizes over the connected
components of that graph (the choice of which vertices of a class go to which
block, and the matching inside each block, are independent across components).
A component that is a single colour c with n_c = 2 contributes the single cell
W_c(u,v); a component {a,b} with n_a=n_b=1 contributes the single cell
X_ab(u,v).  These are UNITS on the torus and can be divided out.

If every component of every argmin type is a unit, the initial form is a single
monomial -- the SINGLETON certificate.  If, after dividing out the components
that are units and are isolated in the SAME way in every argmin type, exactly
one nontrivial factor is left, the initial system forces that factor to vanish
for EVERY word of the content, i.e. for every configuration of the underlying
sets.  Those "forced vanishing families" are matched against:

  LEMMA U (unit)        h_c(S)=W_c(u,v) and X_ab(u,v) are nonzero on the torus.
  LEMMA H4              [hand proof, see REPORT section 3] Let W be symmetric,
                        zero-diagonal, N>=6, every off-diagonal entry nonzero,
                        over a field of characteristic not 2 or 3.  Then
                        haf(W[T]) cannot vanish for every 4-subset T.
  LEMMA P2              [hand proof, see REPORT section 3] Let X have all
                        entries nonzero, with >=3 available rows and >=2
                        available columns.  Then per(X[P,Q]) cannot vanish for
                        every pair of disjoint 2-sets (P,Q).
  LEMMA HK (k>=6)       NOT AVAILABLE -- recorded as residue.

Everything is exact integer / Fraction arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from colour_form_fan import build, contents, types_for_content  # noqa: E402

PAIRS = ((0, 1), (0, 2), (1, 2))
PAIR_INDEX = {p: i for i, p in enumerate(PAIRS)}


def components(n, m):
    """Connected components of the colour-block graph of type m on content n.

    m is (m01, m02, m12).  Returns a tuple of frozensets of colours (only
    colours with n_c > 0 appear).
    """
    present = [c for c in range(3) if n[c] > 0]
    parent = {c: c for c in present}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (a, b) in PAIRS:
        if m[PAIR_INDEX[(a, b)]] > 0:
            if a in parent and b in parent:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[ra] = rb
    groups = {}
    for c in present:
        groups.setdefault(find(c), []).append(c)
    return tuple(sorted(frozenset(v) for v in groups.values()))


def block_data(n, m, comp):
    """Description of the factor carried by component comp of type m."""
    cols = sorted(comp)
    mm = {}
    for (a, b) in PAIRS:
        if a in comp and b in comp:
            mm[(a, b)] = m[PAIR_INDEX[(a, b)]]
    sizes = tuple(n[c] for c in cols)
    return (tuple(cols), sizes, tuple(sorted(mm.items())))


def is_unit_component(n, m, comp):
    """Is the component's factor a single cell (hence a torus unit)?"""
    cols = sorted(comp)
    if len(cols) == 1:
        c = cols[0]
        # isolated colour: factor is haf(W_c[S_c]); a unit iff |S_c| = 2
        return n[c] == 2
    if len(cols) == 2:
        a, b = cols
        if n[a] == 1 and n[b] == 1 and m[PAIR_INDEX[(a, b)]] == 1:
            return True
    return False


def analyse_content(n, argmin, nsites):
    """Return (verdict, detail) for one mixed content in one cone.

    verdict in {"singleton", "fact", "residue"}.
    """
    comp_sets = [components(n, m) for m in argmin]
    # units that are identical across every argmin type can be divided out
    common_units = None
    for m, comps in zip(argmin, comp_sets):
        units = frozenset(comp for comp in comps if is_unit_component(n, m, comp))
        common_units = units if common_units is None else (common_units & units)
    # if every component of every type is a unit, the form is a single monomial
    if all(all(is_unit_component(n, m, comp) for comp in comps)
           for m, comps in zip(argmin, comp_sets)):
        return "singleton", {"n": n, "types": argmin}
    # after dividing out the common units, what is left?
    leftovers = []
    for m, comps in zip(argmin, comp_sets):
        rest = [comp for comp in comps if comp not in common_units]
        leftovers.append((m, tuple(rest)))
    # a single nontrivial factor, the same shape in every type?
    shapes = set()
    for m, rest in leftovers:
        if len(rest) != 1:
            shapes.add(("multi", len(rest)))
        else:
            shapes.add(block_data(n, m, rest[0]))
    if len(shapes) != 1:
        return "residue", {"n": n, "types": argmin, "reason": "no common single factor",
                           "shapes": sorted(str(s) for s in shapes)}
    shape = shapes.pop()
    if shape[0] == "multi":
        return "residue", {"n": n, "types": argmin,
                           "reason": "product of %d nonunit factors" % shape[1]}
    cols, sizes, mm = shape
    if len(cols) == 1:
        c, k = cols[0], sizes[0]
        if k == 2:
            return "kill", {"n": n, "lemma": "U", "fact": "W_%d(u,v)=0" % c}
        if k == 4 and nsites >= 6:
            return "kill", {"n": n, "lemma": "H4",
                            "fact": "haf(W_%d[T])=0 for every 4-subset T" % c}
        return "residue", {"n": n, "types": argmin,
                           "reason": "haf(W_%d[S])=0 for every %d-subset"
                                     % (c, k)}
    if len(cols) == 2:
        a, b = cols
        ka, kb = sizes
        cross = dict(mm).get((a, b), 0)
        if ka == kb == cross:
            if cross == 1:
                return "kill", {"n": n, "lemma": "U", "fact": "X_%d%d(u,v)=0" % (a, b)}
            if cross == 2 and nsites >= 5:
                return "kill", {"n": n, "lemma": "P2",
                                "fact": "per(X_%d%d[P,Q])=0 for every disjoint"
                                        " 2+2" % (a, b)}
            return "residue", {"n": n, "types": argmin,
                               "reason": "per(X_%d%d[P,Q])=0 for every disjoint"
                                         " %d+%d" % (a, b, cross, cross)}
        return "residue", {"n": n, "types": argmin,
                           "reason": "mixed 2-colour block %s sizes %s cross %s"
                                     % (cols, sizes, mm)}
    return "residue", {"n": n, "types": argmin, "reason": "3-colour connected block"}


def run(nsites):
    data = build(nsites, verbose=False)
    mixed = data["mixed"]
    out = []
    for rec in data["faces"]:
        kills = []
        singletons = []
        residues = []
        for n in mixed:
            verdict, detail = analyse_content(n, rec["argmin"][n], nsites)
            if verdict == "singleton":
                singletons.append(detail)
            elif verdict == "kill":
                kills.append(detail)
            else:
                residues.append(detail)
        out.append({"dim": rec["dim"], "point": rec["point"],
                    "sign": rec["sign"],
                    "singletons": singletons, "kills": kills,
                    "residues": residues})
    return data, out


def main():
    summary = {}
    for nsites in (6, 8):
        data, table = run(nsites)
        killed = [r for r in table if r["singletons"] or r["kills"]]
        alive = [r for r in table if not (r["singletons"] or r["kills"])]
        print("N = %d : %d faces of the g-fan" % (nsites, len(table)))
        print("   killed by the MIXED initial system alone : %d" % len(killed))
        by_lemma = {}
        for r in killed:
            if r["singletons"]:
                by_lemma["singleton"] = by_lemma.get("singleton", 0) + 1
            else:
                names = sorted({k["lemma"] for k in r["kills"]})
                key = "+".join(names)
                by_lemma[key] = by_lemma.get(key, 0) + 1
        print("      first available certificate: %s" % by_lemma)
        print("   NOT killed by the mixed system  : %d  (by dim %s)"
              % (len(alive), {d: sum(1 for r in alive if r["dim"] == d)
                              for d in (0, 1, 2, 3)}))
        for r in sorted(alive, key=lambda r: (-r["dim"],))[:40]:
            reasons = sorted({d["reason"] for d in r["residues"]})
            print("      dim %d  g=(%s,%s,%s)  residual shapes: %s"
                  % (r["dim"], r["point"][0], r["point"][1], r["point"][2],
                     "; ".join(reasons[:4])))
        summary[nsites] = {
            "faces": len(table), "killed_mixed": len(killed),
            "alive": [{"dim": r["dim"],
                       "point": [str(c) for c in r["point"]],
                       "reasons": sorted({d["reason"] for d in r["residues"]})}
                      for r in alive],
            "by_lemma": by_lemma,
        }
        print()
    with open("results_kill.json", "w") as handle:
        json.dump(summary, handle, indent=1, default=str)
    print("wrote results_kill.json")


if __name__ == "__main__":
    main()
