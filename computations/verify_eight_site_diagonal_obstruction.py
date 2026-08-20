#!/usr/bin/env python3
"""Checker for the eight-site block-diagonal obstruction.

Proof document: `proofs/eight-site-diagonal-obstruction.md` (Theorem 1.2).
Ledger record:  `certification/SUPERSESSIONS.md`, SUPERSESSION-2026-08-20-01,
                dependency ID `N8-DIAGONAL`.

WHAT THIS CHECKS
----------------
The theorem's finite content is: (a) the free-set-triple normal form reduces
`N = 8` to a 4,096-case ledger in 87 orbits; (b) at `N = 8` the level filter
`k = 4` drops nothing, so the level-4 system IS the exactness system; (c) each
of the 87 orbit formulas is unsatisfiable.  This checker discharges (a) and
(b) outright, and reduces (c) to the shipped certificates by rebuilding every
CNF from scratch and requiring it to match the shipped SHA-256 digest byte for
byte -- so the certificates cannot have been produced from some other formula.

  MANDATORY, stdlib only, no external process:
    1. case ledger, TWO independent routes (canonical enumeration and
       Burnside), required to agree, at N = 4, 6, 8 (+ Burnside at 10, 12);
    2. word bookkeeping at N = 8 from the raw 3^8 enumeration, and the
       identity  {A2 rows at k=4} == {A2 rows unfiltered} == {mixed all-even
       words} -- this is Lemma 2.3, the `EXACT = X_4` step;
    3. rebuild all 87 orbit CNFs with the encoder inlined below and require
       every SHA-256 to match `SHA256SUMS.txt`;
    4. structural soundness audits of each rebuilt formula: no empty clause,
       no unconditional positive literal outside the four licensed units
       (A0/A1/Cnz/Ch), and every FREE row a genuine mixed all-even word of
       off-count <= 4;
    5. the shipped DRAT files are present and non-empty, and their digests
       match.

  OPTIONAL, external process, LOUD EITHER WAY:
    6. replay every shipped (CNF, DRAT) pair through `drat-trim`, requiring
       the literal string "s VERIFIED".  drat-trim is a third-party binary
       that does not live in this repository, so this step is SKIPPED -- with
       a clearly labelled line -- when the binary is not found.  Point at it
       with the DRAT_TRIM (or DRATTRIM) environment variable.

The encoder below is a self-contained port of the audit lane's independent
encoder (`a9_enc.py`, audit A9).  Nothing is imported from any
`computations/unaudited-*` directory, and nothing outside the standard library
is imported at all.  The port's fidelity is not taken on trust: step 3 fails
loudly if a single clause or variable number moved.

Usage
-----
    python3 computations/verify_eight_site_diagonal_obstruction.py
    python3 -O computations/verify_eight_site_diagonal_obstruction.py
    python3 -I -S computations/verify_eight_site_diagonal_obstruction.py

    --artifacts DIR   where SHA256SUMS.txt and orbits/ live (auto-detected)
    --quick           skip the per-case structural audit (steps 1-3, 5 only)
    --proofs          require step 6 to run; fail if drat-trim is missing

Exit status 0 iff every mandatory check passes (and step 6, when it runs).
"""
from __future__ import annotations

import argparse
import hashlib
import math
import os
import subprocess
import sys
from itertools import combinations, permutations, product

N_ORBITS_N8 = 87
N_CASES_N8 = 4096


class CheckFailure(AssertionError):
    """Raised by require(); never an unchecked `assert` (must survive -O)."""


def require(cond, detail):
    """House-style check: raises under python3, -O and -I -S alike."""
    if not cond:
        raise CheckFailure(detail)


# ---------------------------------------------------------------- bit helpers
def bits(mask):
    out = []
    i = 0
    while mask:
        if mask & 1:
            out.append(i)
        mask >>= 1
        i += 1
    return tuple(out)


def mask_of(S):
    m = 0
    for x in S:
        m |= 1 << x
    return m


def popcount(m):
    return bin(m).count("1")


# ------------------------------------------------------------- the case ledger
def all_cases(n):
    """Every case (R_0,R_1,R_2) at order n, in the canonical index order."""
    Q = tuple(range(3, n - 1))
    allR = [tuple(S) for k in range(len(Q) + 1) for S in combinations(Q, k)]
    return [(R0, R1, R2) for R0 in allR for R1 in allR for R2 in allR]


def orbit_reps(n):
    """Route (a): canonical enumeration of the S_Q x S_3 orbits."""
    Q = tuple(range(3, n - 1))
    allR = [tuple(S) for k in range(len(Q) + 1) for S in combinations(Q, k)]
    seen, reps = set(), []
    for trip in product(allR, repeat=3):
        if trip in seen:
            continue
        orb = set()
        for sig in permutations(Q):
            relabel = dict(zip(Q, sig))
            img = tuple(tuple(sorted(relabel[y] for y in R)) for R in trip)
            for pi in permutations(range(3)):
                orb.add(tuple(img[pi[i]] for i in range(3)))
        seen |= orb
        reps.append((trip, len(orb)))
    return reps


def _cycles(perm):
    seen = [False] * len(perm)
    out = []
    for i in range(len(perm)):
        if seen[i]:
            continue
        length, j = 0, i
        while not seen[j]:
            seen[j] = True
            j = perm[j]
            length += 1
        out.append(length)
    return out


def _power(pi, k):
    out = list(range(len(pi)))
    for _ in range(k):
        out = [pi[x] for x in out]
    return tuple(out)


def burnside(q):
    """Route (b): Burnside count of triples of subsets of a q-set."""
    total = 0
    for sigma in permutations(range(q)):
        cyc = _cycles(sigma)
        for pi in permutations(range(3)):
            prod = 1
            for length in cyc:
                prod *= 2 ** len(_cycles(_power(pi, length)))
            total += prod
    denom = math.factorial(q) * 6
    return total // denom, total % denom


# ------------------------------------------------------------------ the encoder
class Enc:
    """CNF for one case (Rs) at order n, level k, solve site z = n - 1.

    Self-contained port of the audit encoder.  `p(c, S)` is the Boolean
    "haf(t^c | S) != 0"; `g(c, S, w, u)` are the Laplace auxiliaries.  Clause
    families, in emission order: A0, A1, A3(+A3g), A2, then per colour
    C0, Cnz, Ch, FR, XF.  Emission order fixes the variable numbering and
    hence the DIMACS bytes -- do not reorder.
    """

    FAMILIES = ("A0", "A1", "A2", "A3", "C0", "Cnz", "Ch", "FR", "XF")

    def __init__(self, n, Rs, k=None, ys=(0, 1, 2), use=None):
        self.n = n
        self.k = k
        self.z = n - 1
        self.ys = ys
        self.use = set(self.FAMILIES if use is None else use)
        self.V = tuple(range(n))
        self.VP = tuple(x for x in self.V if x != self.z)
        self.F = tuple(sorted(set([ys[c]]) | set(Rs[c])) for c in range(3))
        self.Rs = tuple(tuple(sorted(R)) for R in Rs)
        self.nv = 0
        self.vmap = {}
        self.vname = {}
        self.cls = []
        self.tags = []

    def _v(self, key):
        if key not in self.vmap:
            self.nv += 1
            self.vmap[key] = self.nv
            self.vname[self.nv] = key
        return self.vmap[key]

    def p(self, c, S):
        m = S if isinstance(S, int) else mask_of(S)
        return self._v(("p", c, m))

    def g(self, c, m, w, u):
        return self._v(("g", c, m, w, u))

    def add(self, tag, cl):
        self.cls.append(tuple(cl))
        self.tags.append(tag)

    def offcount(self, sizes):
        return self.n - max(sizes)

    def keep(self, sizes):
        return self.k is None or self.offcount(sizes) <= self.k

    def build(self):
        n, z, VP = self.n, self.z, self.VP
        full = (1 << n) - 1
        evens = [m for m in range(1 << n) if popcount(m) % 2 == 0]

        for c in range(3):
            if "A0" in self.use:
                self.add(("A0", c), [self.p(c, 0)])
            if "A1" in self.use:
                self.add(("A1", c), [self.p(c, full)])

        if "A3" in self.use:
            for c in range(3):
                for m in evens:
                    if popcount(m) < 4:
                        continue
                    el = bits(m)
                    for w in el:
                        big = [-self.p(c, m)]
                        for u in el:
                            if u == w:
                                continue
                            gv = self.g(c, m, w, u)
                            self.add(("A3g", c, m, w, u),
                                     [-gv, self.p(c, (1 << w) | (1 << u))])
                            self.add(("A3g", c, m, w, u),
                                     [-gv,
                                      self.p(c, m & ~((1 << w) | (1 << u)))])
                            big.append(gv)
                        self.add(("A3", c, m, w), big)

        if "A2" in self.use:
            for a in evens:
                rest = full & ~a
                s = rest
                while True:
                    if popcount(s) % 2 == 0:
                        b = s
                        cmask = rest & ~b
                        if popcount(cmask) % 2 == 0:
                            parts = (a, b, cmask)
                            sizes = [popcount(x) for x in parts]
                            if max(sizes) != n and self.keep(sizes):
                                cl = [-self.p(cc, parts[cc])
                                      for cc in range(3) if parts[cc]]
                                self.add(("A2", parts), cl)
                    if s == 0:
                        break
                    s = (s - 1) & rest

        for c in range(3):
            yc = self.ys[c]
            Fc = set(self.F[c])
            if "C0" in self.use:
                for y in VP:
                    if y not in Fc:
                        self.add(("C0", c, y),
                                 [-self.p(c, (1 << z) | (1 << y))])
            if "Cnz" in self.use:
                self.add(("Cnz", c), [self.p(c, (1 << z) | (1 << yc))])
            if "Ch" in self.use:
                self.add(("Ch", c),
                         [self.p(c, full & ~((1 << z) | (1 << yc)))])
            if "FR" in self.use:
                d, e = [x for x in range(3) if x != c]
                for y in sorted(Fc):
                    W = tuple(x for x in VP if x != y)
                    wm = mask_of(W)
                    s = wm
                    while True:
                        if popcount(s) % 2 == 0:
                            s1, s2 = s, wm & ~s
                            sizes = [2, popcount(s1), popcount(s2)]
                            if self.keep(sizes):
                                cl = []
                                if s1:
                                    cl.append(-self.p(d, s1))
                                if s2:
                                    cl.append(-self.p(e, s2))
                                require(cl, "empty FREE clause -- would be an "
                                            "unearned kill")
                                self.add(("FR", c, y, s1, s2), cl)
                        if s == 0:
                            break
                        s = (s - 1) & wm
            if "XF" in self.use:
                vpm = mask_of(VP)
                s = vpm
                while True:
                    if popcount(s) % 2 == 1:
                        inF = [y for y in bits(s) if y in Fc]
                        if inF == [yc]:
                            a = self.p(c, s & ~(1 << yc))
                            b = self.p(c, s | (1 << z))
                            self.add(("XF", c, s), [-a, b])
                            self.add(("XF", c, s), [a, -b])
                    if s == 0:
                        break
                    s = (s - 1) & vpm
        return self

    def dimacs(self):
        head = "p cnf %d %d\n" % (self.nv, len(self.cls))
        body = "".join(" ".join(map(str, cl)) + " 0\n" for cl in self.cls)
        return head + body


# ------------------------------------------------------------------- artifacts
def find_artifacts(explicit):
    """Locate the directory holding SHA256SUMS.txt and orbits/."""
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [explicit] if explicit else [
        os.path.join(here, "certified_package"),
        os.path.join(here, "certificates", "n8_diagonal"),
        os.path.join(here, os.pardir, "certified_package"),
        here,
    ]
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "SHA256SUMS.txt")):
            return os.path.normpath(c)
    require(False, "cannot locate the artifact directory (looked in: %s); "
                   "pass --artifacts DIR" % ", ".join(str(c) for c in cands))


def read_manifest(root):
    man = {}
    with open(os.path.join(root, "SHA256SUMS.txt")) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            require(len(parts) == 2, "malformed SHA256SUMS line: %r" % line)
            man[parts[1].strip()] = parts[0].strip()
    require(man, "SHA256SUMS.txt is empty")
    return man


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_drat_trim():
    for name in ("DRAT_TRIM", "DRATTRIM"):
        val = os.environ.get(name)
        if val and os.path.exists(val):
            return val, "environment variable %s" % name
        if val:
            return None, "%s is set to %r but no such file exists" % (name, val)
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [
        os.path.join(here, "unaudited-hygiene-h1-2026-08-15", "tools",
                     "drat-trim", "drat-trim"),
        os.path.join(here, os.pardir, "computations",
                     "unaudited-hygiene-h1-2026-08-15", "tools", "drat-trim",
                     "drat-trim"),
    ]
    for c in cands:
        if os.path.exists(c):
            return os.path.normpath(c), "repository-relative default"
    from shutil import which
    found = which("drat-trim")
    if found:
        return found, "PATH"
    return None, ("not found (set DRAT_TRIM=/path/to/drat-trim; the binary is "
                  "third-party and is not vendored in this repository)")


# ---------------------------------------------------------------- the checks
def check_ledger(report):
    """Step 1: the case census, two independent routes."""
    table = {}
    for n in (4, 6, 8, 10, 12):
        q = n - 4
        b, rem = burnside(q)
        require(rem == 0,
                "Burnside sum at N=%d is not divisible by the group order "
                "(remainder %d)" % (n, rem))
        rec = {"cases": 8 ** q, "burnside": b}
        if q <= 4:
            reps = orbit_reps(n)
            sizes = sum(s for _, s in reps)
            require(len(reps) == b,
                    "orbit-count routes disagree at N=%d: canonical %d vs "
                    "Burnside %d" % (n, len(reps), b))
            require(sizes == 8 ** q,
                    "orbit sizes at N=%d sum to %d, expected %d"
                    % (n, sizes, 8 ** q))
            rec["canonical"] = len(reps)
        table[n] = rec
    require(table[8]["burnside"] == N_ORBITS_N8,
            "N=8 orbit count is %d, expected %d"
            % (table[8]["burnside"], N_ORBITS_N8))
    require(table[8]["cases"] == N_CASES_N8,
            "N=8 case count is %d, expected %d"
            % (table[8]["cases"], N_CASES_N8))
    require(len(all_cases(8)) == N_CASES_N8, "all_cases(8) has wrong length")
    report("step 1  case ledger: " + ", ".join(
        "N=%d %d cases/%d orbits" % (n, r["cases"], r["burnside"])
        for n, r in sorted(table.items())))
    report("        both routes agree at N = 4, 6, 8; "
           "orbit sizes sum to the case count")
    return table


def check_word_bookkeeping(report):
    """Step 2: EXACT = X_4 at N = 8, from the raw 3^8 word enumeration."""
    n = 8
    V = tuple(range(n))
    const = odd_part = 0
    offs = {}
    needed = set()
    for w in product(range(3), repeat=n):
        parts = tuple(tuple(v for v in V if w[v] == c) for c in range(3))
        sizes = [len(p) for p in parts]
        if max(sizes) == n:
            const += 1
            continue
        if any(s % 2 for s in sizes):
            odd_part += 1
            continue
        offs[n - max(sizes)] = offs.get(n - max(sizes), 0) + 1
        needed.add(tuple(mask_of(p) for p in parts))

    require(const == 3, "expected 3 constant words, got %d" % const)
    require(odd_part == 4920,
            "expected 4920 words with an odd colour class, got %d" % odd_part)
    require(len(needed) == 1638,
            "expected 1638 mixed all-even words, got %d" % len(needed))
    require(offs == {2: 168, 4: 1470},
            "off-count histogram is %r, expected {2: 168, 4: 1470}" % offs)
    require(max(offs) <= 4,
            "some mixed all-even word at N=8 has off-count %d > 4 -- "
            "EXACT would NOT equal X_4" % max(offs))

    base = ((), (), ())
    rows_k4 = {t[1] for t in Enc(n, base, k=4).build().tags if t[0] == "A2"}
    rows_inf = {t[1] for t in Enc(n, base, k=None).build().tags if t[0] == "A2"}
    require(rows_k4 == rows_inf,
            "the k=4 filter drops %d A2 rows -- it is not lossless at N=8"
            % len(rows_inf - rows_k4))
    require(rows_k4 == needed,
            "the A2 clause set does not equal the mixed all-even word set "
            "(%d vs %d rows)" % (len(rows_k4), len(needed)))
    report("step 2  words at N=8: 6561 = 3 constant + 4920 odd-part + 1638 "
           "mixed-even")
    report("        off-counts {2: 168, 4: 1470}; A2 rows at k=4 == "
           "unfiltered == the 1638 words")
    report("        => EXACT = X_4 at N = 8 (Lemma 2.3)")


def audit_formula(enc):
    """Step 4 for one formula: structural soundness, no solver involved."""
    licensed = {"A0", "A1", "Cnz", "Ch"}
    for tag, cl in zip(enc.tags, enc.cls):
        require(cl, "empty clause emitted by family %r" % (tag[0],))
        pos = [l for l in cl if l > 0]
        neg = [l for l in cl if l < 0]
        if pos and not neg and not (tag[0] in licensed and len(cl) == 1):
            require(False,
                    "unconditional positive clause from family %r: the "
                    "encoding would be asserting a hafnian nonzero without a "
                    "hypothesis" % (tag[0],))
    for tag in enc.tags:
        if tag[0] != "FR":
            continue
        _, _, _, s1, s2 = tag
        sizes = [2, popcount(s1), popcount(s2)]
        require(sum(sizes) == enc.n,
                "FREE row %r does not partition the %d sites" % (tag, enc.n))
        require(not any(s % 2 for s in sizes),
                "FREE row %r has an odd part" % (tag,))
        require(max(sizes) != enc.n, "FREE row %r is a constant word" % (tag,))
        require(enc.n - max(sizes) <= 4,
                "FREE row %r has off-count > 4" % (tag,))


def check_cnfs(root, manifest, report, quick):
    """Steps 3-5: rebuild every CNF, match digests, audit, check the proofs."""
    reps = [trip for trip, _ in orbit_reps(8)]
    require(len(reps) == N_ORBITS_N8, "expected %d orbits" % N_ORBITS_N8)
    matched = audited = proofs_ok = 0
    for i, Rs in enumerate(reps):
        enc = Enc(8, Rs, k=4).build()
        rel = "orbits/n8k4_%d.cnf" % i
        require(rel in manifest, "%s is missing from SHA256SUMS.txt" % rel)
        got = sha256_bytes(enc.dimacs().encode("ascii"))
        require(got == manifest[rel],
                "REBUILD MISMATCH for orbit %d (case %r): the formula this "
                "checker derives is not the one the shipped certificate "
                "refutes\n  rebuilt : %s\n  shipped : %s"
                % (i, [list(R) for R in Rs], got, manifest[rel]))
        matched += 1
        if not quick:
            audit_formula(enc)
            audited += 1
        drat_rel = "orbits/n8k4_%d.drat" % i
        require(drat_rel in manifest,
                "%s is missing from SHA256SUMS.txt" % drat_rel)
        drat_path = os.path.join(root, drat_rel)
        require(os.path.isfile(drat_path), "missing proof file %s" % drat_rel)
        require(os.path.getsize(drat_path) > 0, "empty proof %s" % drat_rel)
        require(sha256_file(drat_path) == manifest[drat_rel],
                "digest mismatch for the shipped proof %s" % drat_rel)
        proofs_ok += 1
    report("step 3  rebuilt %d/%d orbit CNFs; every SHA-256 matches the "
           "shipped digest" % (matched, N_ORBITS_N8))
    if quick:
        report("step 4  structural audit SKIPPED (--quick)")
    else:
        report("step 4  structural audit passed on %d/%d formulas: no empty "
               "clause, no" % (audited, N_ORBITS_N8))
        report("        unconditional positive literal outside A0/A1/Cnz/Ch, "
               "all FREE rows well-formed")
    report("step 5  %d/%d shipped DRAT proofs present, non-empty, digests "
           "match" % (proofs_ok, N_ORBITS_N8))
    return reps


def check_proofs(root, reps, report, required):
    """Step 6: optional third-party proof replay."""
    binary, how = resolve_drat_trim()
    if binary is None:
        line = ("step 6  PROOF REPLAY SKIPPED -- drat-trim %s.\n"
                "        The 87 shipped proofs were checked at staging time "
                "(see the proof\n"
                "        document, section 6.3); this run did NOT re-verify "
                "them." % how)
        if required:
            require(False, line.replace("SKIPPED", "REQUIRED BUT UNAVAILABLE"))
        report(line)
        return None
    verified = 0
    for i in range(len(reps)):
        cnf = os.path.join(root, "orbits/n8k4_%d.cnf" % i)
        drat = os.path.join(root, "orbits/n8k4_%d.drat" % i)
        proc = subprocess.run([binary, cnf, drat, "-f"], capture_output=True,
                              text=True, timeout=1800)
        require("s VERIFIED" in proc.stdout,
                "drat-trim did NOT verify orbit %d (exit %d); last output:\n%s"
                % (i, proc.returncode, proc.stdout.strip()[-400:]))
        verified += 1
    report("step 6  drat-trim (%s, via %s): %d/%d proofs 's VERIFIED'"
           % (os.path.basename(binary), how, verified, len(reps)))
    return verified


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--artifacts", default=None)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--proofs", action="store_true",
                    help="fail instead of skipping if drat-trim is missing")
    args = ap.parse_args(argv)

    lines = []

    def report(msg):
        lines.append(msg)
        print(msg, flush=True)

    print("verify_eight_site_diagonal_obstruction  "
          "(proofs/eight-site-diagonal-obstruction.md, Theorem 1.2)")
    print("python %s   optimized=%s   isolated=%s"
          % (sys.version.split()[0], not __debug__,
             getattr(sys.flags, "isolated", 0) == 1))
    root = find_artifacts(args.artifacts)
    print("artifacts: %s" % root)
    print("")

    manifest = read_manifest(root)
    check_ledger(report)
    check_word_bookkeeping(report)
    reps = check_cnfs(root, manifest, report, args.quick)
    check_proofs(root, reps, report, args.proofs)

    print("")
    print("ALL MANDATORY CHECKS PASSED")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except CheckFailure as exc:
        print("\nCHECK FAILED: %s" % exc, file=sys.stderr)
        sys.exit(1)
