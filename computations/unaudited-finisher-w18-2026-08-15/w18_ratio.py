#!/usr/bin/env python3
"""UNAUDITED PROBE (W18) -- the monomial-ratio engine, generic form.

Pinned HEAD: see PINNED_HEAD.txt.  Probe output; not a proved project claim.

INPUT.  A monomial system in n variables, ALL REQUIRED NONZERO:
    zeros    {key: [exponent vectors]}   -- each sum of monomials must vanish
    nonzeros {key: [exponent vectors]}   -- each sum of monomials must NOT
Since the variables are nonzero, a two-term vanishing sum m_a + m_b = 0 is the
multiplicative relation x^{e_b - e_a} = -1.  Let LAMBDA be the group generated
by such vectors, chi the induced character to Q^*.

RULES (each is a contradiction, i.e. the system has no solution)
  C0  a `zeros` equation with exactly one term
  C1  chi is inconsistent: an integer combination of generators is the zero
      vector with product of values != 1
  C2  a `zeros` equation whose terms fall into ratio classes of which exactly
      ONE has a nonzero coefficient sum
  C3  a `nonzeros` equation whose ratio classes ALL have coefficient sum 0
A `zeros` equation with exactly two live classes yields a NEW relation, so the
engine is iterated to a fixpoint.

CERTIFICATE.  Generators are listed in derivation order; a derived generator
carries the ratio data that produced it, referring only to EARLIER generators
by index, with an explicit integer coefficient vector.  `verify` re-checks
every claim as exact integer / Fraction arithmetic against the equation tables
supplied by the caller (which must be recomputed from the template).
"""

from __future__ import annotations

from fractions import Fraction


class Relations:
    """Subgroup of Z^n with a character to Q^*, in echelon form."""

    def __init__(self, n):
        self.n = n
        self.rows = {}
        self.ngen = 0
        self.contradiction = None

    def add_generator(self, vec, value):
        gi = self.ngen
        self.ngen += 1
        return self._insert(list(vec), Fraction(value), {gi: 1})

    def _insert(self, vec, value, coeffs):
        p = 0
        while p < self.n:
            if vec[p] == 0:
                p += 1
                continue
            if p not in self.rows:
                self.rows[p] = (list(vec), value, dict(coeffs))
                return "ok"
            bvec, bval, bco = self.rows[p]
            a, b = bvec[p], vec[p]
            g, s, t = _xgcd(a, b)
            nvec = [s * x + t * y for x, y in zip(bvec, vec)]
            nval = _pw(bval, s) * _pw(value, t)
            nco = _lin(bco, s, coeffs, t)
            ka, kb = a // g, b // g
            vec = [ka * y - kb * x for x, y in zip(bvec, vec)]
            value = _pw(value, ka) * _pw(bval, -kb)
            coeffs = _lin(coeffs, ka, bco, -kb)
            self.rows[p] = (nvec, nval, nco)
            p += 1
        if any(vec):
            raise AssertionError("echelon reduction left a nonzero vector")
        if value != 1:
            self.contradiction = {"coeffs": {str(k): int(v)
                                             for k, v in coeffs.items() if v},
                                  "value": [value.numerator, value.denominator]}
            return "contradiction"
        return "redundant"

    def reduce(self, vec):
        vec = list(vec)
        coeffs = {}
        value = Fraction(1)
        for p in range(self.n):
            if vec[p] == 0:
                continue
            if p not in self.rows:
                return None
            bvec, bval, bco = self.rows[p]
            if vec[p] % bvec[p]:
                return None
            k = vec[p] // bvec[p]
            vec = [y - k * x for x, y in zip(bvec, vec)]
            value = value / _pw(bval, k)
            coeffs = _lin(coeffs, 1, bco, -k)
        if any(vec):
            return None
        return (Fraction(1) / value, {k: -v for k, v in coeffs.items() if v})


def _xgcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    if old_r < 0:
        old_r, old_s, old_t = -old_r, -old_s, -old_t
    return old_r, old_s, old_t


def _pw(value, k):
    return value ** k if k >= 0 else Fraction(1) / (value ** (-k))


def _lin(c1, a, c2, b):
    out = {}
    for k, v in c1.items():
        out[k] = out.get(k, 0) + a * v
    for k, v in c2.items():
        out[k] = out.get(k, 0) + b * v
    return {k: v for k, v in out.items() if v}


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def components(rel, monos):
    k = len(monos)
    comp = [-1] * k
    ratios = [Fraction(0)] * k
    cid = 0
    for a in range(k):
        if comp[a] >= 0:
            continue
        comp[a] = cid
        ratios[a] = Fraction(1)
        for b in range(a + 1, k):
            if comp[b] >= 0:
                continue
            r = rel.reduce(sub(monos[b], monos[a]))
            if r is not None:
                comp[b] = cid
                ratios[b] = r[0]
        cid += 1
    return comp, ratios


def analyse(rel, monos):
    comp, ratios = components(rel, monos)
    base = {}
    cert = []
    for k, c in enumerate(comp):
        if c not in base:
            base[c] = k
            cert.append({"term": k, "base": k, "value": [1, 1], "coeffs": {}})
            continue
        r = rel.reduce(sub(monos[k], monos[base[c]]))
        cert.append({"term": k, "base": base[c],
                     "value": [r[0].numerator, r[0].denominator],
                     "coeffs": {str(a): int(b) for a, b in r[1].items()}})
    sums = {}
    for k, c in enumerate(comp):
        sums[base[c]] = sums.get(base[c], Fraction(0)) + ratios[k]
    return cert, sums


def run(n, zeros, nonzeros, max_rounds=12):
    """Search for a contradiction.  Returns a certificate dict or None."""
    rel = Relations(n)
    gens = []
    for key, monos in zeros.items():
        if len(monos) == 1:
            return {"rule": "C0", "key": key, "generators": []}
    for key, monos in zeros.items():
        if len(monos) == 2:
            st = rel.add_generator(sub(monos[1], monos[0]), -1)
            gens.append({"kind": "binomial", "key": key})
            if st == "contradiction":
                return {"rule": "C1", "generators": gens,
                        "contradiction": rel.contradiction}
    big = [(k, m) for k, m in zeros.items() if len(m) >= 3]
    for _ in range(max_rounds):
        progress = False
        for key, monos in nonzeros.items():
            cert, sums = analyse(rel, monos)
            if not [b for b, s in sums.items() if s != 0]:
                return {"rule": "C3", "key": key, "generators": gens,
                        "ratios": cert}
        for key, monos in big:
            cert, sums = analyse(rel, monos)
            live = [b for b, s in sums.items() if s != 0]
            if len(live) == 1:
                return {"rule": "C2", "key": key, "generators": gens,
                        "ratios": cert}
            if len(live) == 2:
                b1, b2 = live
                vec = sub(monos[b2], monos[b1])
                if rel.reduce(vec) is not None:
                    continue
                val = -Fraction(sums[b1]) / Fraction(sums[b2])
                st = rel.add_generator(vec, val)
                gens.append({"kind": "derived", "key": key, "ratios": cert,
                             "base1": b1, "base2": b2,
                             "sum1": [sums[b1].numerator, sums[b1].denominator],
                             "sum2": [sums[b2].numerator, sums[b2].denominator],
                             "value": [val.numerator, val.denominator]})
                progress = True
                if st == "contradiction":
                    return {"rule": "C1", "generators": gens,
                            "contradiction": rel.contradiction}
        if not progress:
            break
    return None


# ---------------------------------------------------------------- verify

def _check_ratios(monos, ratios, vecs, vals):
    seen = {}
    groups = {}
    for r in ratios:
        k = r["term"]
        if k in seen or not (0 <= k < len(monos)):
            return None
        base = r["base"]
        if not (0 <= base < len(monos)):
            return None
        value = Fraction(r["value"][0], r["value"][1])
        target = sub(monos[k], monos[base])
        acc = [0] * len(target)
        prod = Fraction(1)
        for key, a in r.get("coeffs", {}).items():
            i = int(key)
            if not (0 <= i < len(vecs)):
                return None
            acc = [x + a * y for x, y in zip(acc, vecs[i])]
            prod *= _pw(vals[i], a)
        if tuple(acc) != target or prod != value:
            return None
        seen[k] = base
        groups[base] = groups.get(base, Fraction(0)) + value
    if len(seen) != len(monos):
        return None
    for k, base in seen.items():
        if seen.get(base) != base:
            return None
    return groups


def verify(n, zeros, nonzeros, cert):
    """Re-check a certificate against equation tables recomputed by the caller."""
    rule = cert.get("rule")
    if rule == "C0":
        key = cert["key"]
        if key not in zeros:
            return False, "C0 key is not a vanishing equation"
        return (len(zeros[key]) == 1,
                "a vanishing equation is a single nonzero monomial")
    vecs, vals = [], []
    for gi, g in enumerate(cert.get("generators", [])):
        key = g["key"]
        if key not in zeros:
            return False, f"generator {gi}: key is not a vanishing equation"
        monos = zeros[key]
        if g["kind"] == "binomial":
            if len(monos) != 2:
                return False, f"generator {gi}: not a two-term equation"
            vecs.append(sub(monos[1], monos[0]))
            vals.append(Fraction(-1))
            continue
        if g["kind"] != "derived":
            return False, f"generator {gi}: unknown kind"
        groups = _check_ratios(monos, g["ratios"], vecs, vals)
        if groups is None:
            return False, f"generator {gi}: ratio certificate invalid"
        b1, b2 = g["base1"], g["base2"]
        s1 = Fraction(g["sum1"][0], g["sum1"][1])
        s2 = Fraction(g["sum2"][0], g["sum2"][1])
        if b1 == b2 or groups.get(b1) != s1 or groups.get(b2) != s2:
            return False, f"generator {gi}: claimed group sums wrong"
        if s1 == 0 or s2 == 0:
            return False, f"generator {gi}: degenerate derivation"
        if set(b for b, s in groups.items() if s != 0) != {b1, b2}:
            return False, f"generator {gi}: other live classes present"
        val = Fraction(g["value"][0], g["value"][1])
        if val != -s1 / s2:
            return False, f"generator {gi}: claimed value wrong"
        vecs.append(sub(monos[b2], monos[b1]))
        vals.append(val)
    if rule == "C1":
        acc = [0] * n
        prod = Fraction(1)
        for key, a in cert["contradiction"]["coeffs"].items():
            i = int(key)
            if not (0 <= i < len(vecs)):
                return False, "contradiction cites an unknown generator"
            acc = [x + a * y for x, y in zip(acc, vecs[i])]
            prod *= _pw(vals[i], a)
        if any(acc):
            return False, "the combination is not the zero vector"
        if prod == 1:
            return False, "the contradiction value is 1"
        return True, f"the relations force 1 = {prod}"
    if rule in ("C2", "C3"):
        key = cert["key"]
        table = zeros if rule == "C2" else nonzeros
        if key not in table:
            return False, f"{rule} key is not in the right equation table"
        monos = table[key]
        if not monos:
            return False, "the cited equation is empty"
        groups = _check_ratios(monos, cert["ratios"], vecs, vals)
        if groups is None:
            return False, "ratio certificate invalid"
        live = [b for b, s in groups.items() if s != 0]
        if rule == "C2":
            return (len(live) == 1,
                    "a vanishing equation reduces to one nonzero monomial")
        return (not live, "a required-nonzero equation cancels to zero")
    return False, f"unknown rule {rule}"


def compress(cert):
    """Keep only the generators the certificate uses (re-indexed)."""
    gens = cert.get("generators", [])
    need = set()
    if cert.get("rule") == "C1":
        need |= {int(k) for k in cert["contradiction"]["coeffs"]}
    for r in cert.get("ratios", []) or []:
        need |= {int(k) for k in r.get("coeffs", {})}
    changed = True
    while changed:
        changed = False
        for i in sorted(need):
            g = gens[i]
            if g["kind"] != "derived":
                continue
            for r in g["ratios"]:
                for k in r.get("coeffs", {}):
                    if int(k) not in need:
                        need.add(int(k))
                        changed = True
    keep = sorted(need)
    remap = {old: new for new, old in enumerate(keep)}

    def fix(refs):
        return {str(remap[int(k)]): v for k, v in refs.items()}

    out = dict(cert)
    newgens = []
    for old in keep:
        g = dict(gens[old])
        if g["kind"] == "derived":
            g["ratios"] = [dict(r, coeffs=fix(r.get("coeffs", {})))
                           for r in g["ratios"]]
        newgens.append(g)
    out["generators"] = newgens
    if cert.get("rule") == "C1":
        out["contradiction"] = dict(cert["contradiction"],
                                    coeffs=fix(cert["contradiction"]["coeffs"]))
    if cert.get("ratios"):
        out["ratios"] = [dict(r, coeffs=fix(r.get("coeffs", {})))
                         for r in cert["ratios"]]
    return out
