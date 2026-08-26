#!/usr/bin/env python3
"""UNAUDITED PROBE (W1) -- exactness push on the P2 all-blocked shadows.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01
Plan: notes/2026-08-15-resolution-master-plan.md (agent W1, probe P3')
Inherited machinery: computations/unaudited-witness-splitting-p2-2026-08-15/
    wsplit_core.py  (sha256 4ce16df70d20bd07334227cf4b48c89ddec0d6ac...)

Nothing here is a proved claim.  Exact rational arithmetic throughout;
witness/blocking decisions are Singular Groebner computations over Q
(P2's `classify_source`, reused verbatim).

THE STAR LINEARISATION (the tool that makes the exactness push exact).
Every perfect matching of the six sites contains EXACTLY ONE edge at a
fixed site z.  Hence for every word w in {0,1,2}^6

    H(A)_w  =  sum_{v != z}  A_{zv}[w_z][w_v] * P_v(w)                (*)

where P_v(w) = sum over the three perfect matchings of B \\ {z,v} of the
product of their two block entries.  So, with the ten blocks off the star
of z held fixed, ALL 729 GHZ equations are LINEAR in the 45 star
coordinates, and they decouple by the colour c = w_z into three systems of
3^5 = 243 equations in 15 unknowns each.

Consequently "impose a subset of the mixed GHZ equations" is exact
rational linear algebra: a consistency test plus an orthogonal projection
of the current star onto the affine solution set.  Cycling z over the six
sites is an exact monotone block-coordinate push toward exactness (already
satisfied equations are carried as hard constraints, so the satisfied set
never shrinks).  By Theorem 1.1 of
proofs/six-site-arbitrary-complex-obstruction.md no six-site source is
exact, so the push must stall; WHERE it stalls and WHAT structure appears
there is the measurement.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd, lcm
import os
import sys

sys.set_int_max_str_digits(2000000)   # exact push solutions get large

P2DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "unaudited-witness-splitting-p2-2026-08-15")
sys.path.insert(0, os.path.abspath(P2DIR))

from wsplit_core import (DIM_W, PAIRS, SITES, PairData, Source,
                         classify_source, decide_pair, in_sym_square,
                         matrix_rank, pair_status, perfect_matchings,
                         random_matrix, random_source, require)

MATCHINGS = perfect_matchings(SITES)          # 15
WORDS = tuple(product(range(3), repeat=6))    # 729
PURE_WORDS = tuple((c,) * 6 for c in range(3))
MIXED_WORDS = tuple(w for w in WORDS if len(set(w)) > 1)   # 726
NMIXED = len(MIXED_WORDS)


# ------------------------------------------------------------ coefficients


def all_coefficients(source):
    """Exact H_6(A)_w for every word (independent of the star linearisation)."""
    out = {}
    oriented = {(u, v): source.oriented(u, v) for u in SITES for v in SITES
                if u != v}
    for word in WORDS:
        total = Fraction(0)
        for matching in MATCHINGS:
            term = Fraction(1)
            for u, v in matching:
                term *= oriented[(u, v)][word[u]][word[v]]
                if term == 0:
                    break
            total += term
        out[word] = total
    return out


def support_fibres(source):
    """Number of matchings whose three entries are all nonzero, per word.

    A mixed word with fibre size 1 has a NONZERO coefficient (one surviving
    monomial), so its GHZ equation cannot be satisfied without changing the
    support: this is exactly the singleton/O2 mechanism of Lemma J.2.
    """
    out = {}
    oriented = {(u, v): source.oriented(u, v) for u in SITES for v in SITES
                if u != v}
    for word in WORDS:
        count = 0
        for matching in MATCHINGS:
            if all(oriented[(u, v)][word[u]][word[v]] != 0
                   for u, v in matching):
                count += 1
        out[word] = count
    return out


# -------------------------------------------------------------- structure


def block_type(matrix):
    """Coordinate-ness classification of one block."""
    rank = matrix_rank(matrix)
    rows = sum(1 for i in range(3) if any(matrix[i][j] for j in range(3)))
    cols = sum(1 for j in range(3) if any(matrix[i][j] for i in range(3)))
    nnz = sum(1 for i in range(3) for j in range(3) if matrix[i][j])
    if rank == 0:
        kind = "zero"
    elif rank == 1:
        # rank one: matrix = x (x) y.  x is a coordinate vector iff exactly one
        # nonzero ROW; y is a coordinate vector iff exactly one nonzero COLUMN.
        if rows == 1 and cols == 1:
            kind = "rank1-monomial"        # both factors coordinate
        elif rows == 1 or cols == 1:
            kind = "rank1-half"            # exactly one factor coordinate
        else:
            kind = "rank1-generic"         # neither factor coordinate
    else:
        kind = f"rank{rank}"
    return {"rank": rank, "rows": rows, "cols": cols, "nnz": nnz, "kind": kind}


def structure_metrics(source):
    types = {pair: block_type(source.blocks[pair]) for pair in PAIRS}
    kinds = Counter(entry["kind"] for entry in types.values())
    rank1 = [pair for pair in PAIRS if types[pair]["rank"] == 1]
    noncoord = [pair for pair in rank1
                if types[pair]["kind"] != "rank1-monomial"]
    fully_generic = [pair for pair in rank1
                     if types[pair]["kind"] == "rank1-generic"]
    return {
        "kinds": dict(kinds),
        "rank1_blocks": len(rank1),
        "noncoordinate_rank1": len(noncoord),
        "generic_rank1": len(fully_generic),
        "noncoordinate_pairs": [list(pair) for pair in noncoord],
        "defect_graph": sorted([list(pair) for pair in PAIRS
                                if types[pair]["rank"] != 1]),
        "support_size": sum(entry["nnz"] for entry in types.values()),
    }


def exactness_metrics(source):
    coefficients = all_coefficients(source)
    fibres = support_fibres(source)
    mixed_defects = [w for w in MIXED_WORDS if coefficients[w] != 0]
    singleton = [w for w in MIXED_WORDS if fibres[w] == 1]
    histogram = Counter(fibres[w] for w in MIXED_WORDS)
    return {
        "pure": [str(coefficients[w]) for w in PURE_WORDS],
        "pure_exact": all(coefficients[w] == 1 for w in PURE_WORDS),
        "mixed_satisfied": NMIXED - len(mixed_defects),
        "mixed_violated": len(mixed_defects),
        "mixed_satisfied_fraction": (NMIXED - len(mixed_defects)) / NMIXED,
        "singleton_mixed_fibres": len(singleton),
        "mixed_fibre_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "supported_mixed_words": sum(1 for w in MIXED_WORDS if fibres[w] > 0),
    }


def primitive(values):
    """Scale a rational vector to primitive integers (0 vector unchanged).

    Used ONLY on the generators handed to Singular: multiplying an ideal
    generator, or the linear form s, by a nonzero rational changes neither
    the ideal, nor the hyperplane {s = 0}, nor membership of any L-monomial,
    so every witness/blocking verdict is unchanged -- while the exact push
    solutions, whose numerators can run to thousands of digits, become small
    integers.  Control W8 checks the verdicts agree.
    """
    values = list(values)
    if all(value == 0 for value in values):
        return values
    multiplier = 1
    for value in values:
        multiplier = lcm(multiplier, value.denominator)
    scaled = [value * multiplier for value in values]
    divisor = 0
    for value in scaled:
        divisor = gcd(divisor, int(value))
    return [Fraction(int(value) // divisor) for value in scaled]


def normalised_pairdata(source, p, q):
    pd = PairData(source, p, q)
    pd.s = primitive(pd.s)
    normalised = []
    for quad in pd.quadrics:
        keys = sorted(quad)
        scaled = primitive([quad[key] for key in keys])
        normalised.append({key: value for key, value in zip(keys, scaled)
                           if value})
    pd.quadrics = normalised
    return pd


def blocking_metrics(source, max_degree=4, timeout=30, pairs=None,
                     normalise=True):
    if not normalise:
        report = classify_source(source, max_degree=max_degree, pairs=pairs,
                                 timeout=timeout)
    else:
        report = classify_normalised(source, max_degree=max_degree,
                                     pairs=pairs, timeout=timeout)
    live = [record for record in report.values() if record["live"]]
    witness = [pair for pair, record in report.items()
               if record["live"] and record["witness"] is True]
    undecided = [pair for pair, record in report.items()
                 if record["live"] and record["witness"] is None]
    degrees = Counter(record["min_block_degree"] for record in live
                      if record["witness"] is False)
    return {
        "live_pairs": len(live),
        "witness_pairs": len(witness),
        "witness_pair_list": [list(pair) for pair in witness],
        "blocked_pairs": sum(1 for record in live
                             if record["witness"] is False),
        "undecided_pairs": [list(pair) for pair in undecided],
        "all_live_blocked": (not witness) and (not undecided),
        "min_block_degrees": {str(k): v for k, v in sorted(
            degrees.items(), key=lambda kv: (kv[0] is None, kv[0]))},
        "status": {str(pair): report[pair]["status"] for pair in report},
        "arithmetic": sorted({record["arithmetic"] for record in report.values()}),
    }


def classify_normalised(source, max_degree=4, pairs=None, timeout=30):
    """P2's classify_source with primitive generators (identical record shape)."""
    pairs = tuple(pairs) if pairs is not None else PAIRS
    report = {}
    for pair in pairs:
        pd = normalised_pairdata(source, *pair)
        patterns, span = pd.split_patterns()
        entry = decide_pair(pd, max_degree, timeout)
        record = {
            "live": pd.is_live(),
            "error_zero": pd.error_identically_zero(),
            "span": span,
            "patterns": patterns,
            "cone_dim": entry["dim"],
            "witness": entry["witness"],
            "mem": entry["mem"],
            "arithmetic": entry.get("arithmetic", "Q"),
        }
        record["variety_empty"] = (entry["dim"] is not None
                                   and entry["dim"] <= 0)
        record["span_is_W"] = span == DIM_W
        record["all_components_in_W"] = all(in_sym_square(quad)
                                            for quad in pd.quadrics)
        record["min_block_degree"] = min(
            (degree for (degree, _name), value in entry["mem"].items() if value),
            default=None)
        record["status"] = pair_status(record)
        report[pair] = record
    return report


def full_metrics(source, max_degree=4, timeout=30, with_blocking=True):
    out = {"structure": structure_metrics(source),
           "exactness": exactness_metrics(source)}
    if with_blocking:
        out["blocking"] = blocking_metrics(source, max_degree, timeout)
    return out


# ------------------------------------------------- exact linear algebra


class IncSystem:
    """Incrementally maintained RREF of an exact rational linear system.

    add_row(row, rhs) returns True if the row is consistent with the rows
    accepted so far (and accepts it), False otherwise (and changes nothing).
    """

    def __init__(self, dimension):
        self.dimension = dimension
        self.pivots = []
        self.rows = []
        self.rhs = []

    def _reduce(self, row, rhs):
        row = list(row)
        for pivot, base, target in zip(self.pivots, self.rows, self.rhs):
            if row[pivot]:
                factor = row[pivot] / base[pivot]
                row = [a - factor * b for a, b in zip(row, base)]
                rhs = rhs - factor * target
        return row, rhs

    def consistent(self, row, rhs):
        row, rhs = self._reduce(row, rhs)
        if any(row):
            return True
        return rhs == 0

    def add_row(self, row, rhs):
        row, rhs = self._reduce(row, rhs)
        pivot = next((n for n, value in enumerate(row) if value), None)
        if pivot is None:
            return rhs == 0            # dependent row: consistent iff 0 = 0
        # back-substitute into the stored rows to keep a true RREF
        for index, (p, base, target) in enumerate(
                zip(self.pivots, self.rows, self.rhs)):
            if base[pivot]:
                factor = base[pivot] / row[pivot]
                self.rows[index] = [a - factor * b for a, b in zip(base, row)]
                self.rhs[index] = target - factor * rhs
        self.pivots.append(pivot)
        self.rows.append(row)
        self.rhs.append(rhs)
        return True

    def rank(self):
        return len(self.pivots)

    def particular(self):
        x = [Fraction(0)] * self.dimension
        for pivot, row, rhs in zip(self.pivots, self.rows, self.rhs):
            x[pivot] = rhs / row[pivot]
        return x

    def nullspace(self):
        free = [n for n in range(self.dimension) if n not in set(self.pivots)]
        basis = []
        for f in free:
            vector = [Fraction(0)] * self.dimension
            vector[f] = Fraction(1)
            for pivot, row in zip(self.pivots, self.rows):
                vector[pivot] = -row[f] / row[pivot]
            basis.append(vector)
        return basis

    def project(self, x0):
        """Point of the affine solution set nearest (Euclidean) to x0.

        Exact: solve (N^T N) y = N^T (x0 - x_p) by Gaussian elimination.
        """
        x_p = self.particular()
        basis = self.nullspace()
        if not basis:
            return x_p
        diff = [a - b for a, b in zip(x0, x_p)]
        gram = [[sum(u[k] * v[k] for k in range(self.dimension)) for v in basis]
                for u in basis]
        target = [sum(u[k] * diff[k] for k in range(self.dimension))
                  for u in basis]
        y = solve_square(gram, target)
        out = list(x_p)
        for coefficient, vector in zip(y, basis):
            out = [a + coefficient * b for a, b in zip(out, vector)]
        return out


def solve_square(matrix, rhs):
    """Gaussian elimination for a nonsingular exact rational system."""
    n = len(matrix)
    rows = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for column in range(n):
        pivot = next((r for r in range(column, n) if rows[r][column]), None)
        require(pivot is not None, "singular Gram matrix")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        head = rows[column]
        for r in range(n):
            if r != column and rows[r][column]:
                factor = rows[r][column] / head[column]
                rows[r] = [a - factor * b for a, b in zip(rows[r], head)]
    return [rows[i][n] / rows[i][i] for i in range(n)]


# ------------------------------------------------------ star linearisation


def star_partners(z):
    return tuple(v for v in SITES if v != z)


def star_index(z, v, j):
    """Unknown index inside one colour row: block (z,v), column colour j."""
    return 3 * star_partners(z).index(v) + j


STAR_DIM = 15          # 5 partner blocks x 3 colours, per row colour c


def cofactor_tables(source, z):
    """P_v(w) for every partner v and every word restricted to B \\ {z,v}.

    Returned as {v: {word4: value}} with word4 indexed by the sorted list of
    the four remaining sites.
    """
    tables = {}
    oriented = {(u, v): source.oriented(u, v) for u in SITES for v in SITES
                if u != v}
    for v in star_partners(z):
        rest = tuple(site for site in SITES if site not in (z, v))
        matchings = perfect_matchings(rest)
        require(len(matchings) == 3, "four sites carry three matchings")
        table = {}
        for word4 in product(range(3), repeat=4):
            colour = dict(zip(rest, word4))
            total = Fraction(0)
            for matching in matchings:
                term = Fraction(1)
                for a, b in matching:
                    term *= oriented[(a, b)][colour[a]][colour[b]]
                    if term == 0:
                        break
                total += term
            table[word4] = total
        tables[v] = (rest, table)
    return tables


def star_row(tables, z, word):
    """Row of the linear form (*) in the STAR_DIM unknowns of colour w_z."""
    row = [Fraction(0)] * STAR_DIM
    for v, (rest, table) in tables.items():
        value = table[tuple(word[site] for site in rest)]
        if value:
            row[star_index(z, v, word[v])] += value
    return row


def star_vector(source, z, colour):
    """Current values of the STAR_DIM unknowns of one colour row."""
    vector = [Fraction(0)] * STAR_DIM
    for v in star_partners(z):
        block = source.oriented(z, v)
        for j in range(3):
            vector[star_index(z, v, j)] = block[colour][j]
    return vector


def apply_star(source, z, vectors):
    """New source with the star at z replaced by `vectors` (per colour row)."""
    blocks = {pair: [row[:] for row in source.blocks[pair]] for pair in PAIRS}
    for v in star_partners(z):
        table = [[Fraction(0)] * 3 for _ in range(3)]
        for c in range(3):
            for j in range(3):
                table[c][j] = vectors[c][star_index(z, v, j)]
        if z < v:
            blocks[(z, v)] = table
        else:
            blocks[(v, z)] = [[table[i][j] for i in range(3)] for j in range(3)]
    return Source(blocks)


def star_coefficient(tables, z, source, word):
    """The right-hand side of (*): the star model's value of H(A)_w."""
    row = star_row(tables, z, word)
    vector = star_vector(source, z, word[z])
    return sum(a * b for a, b in zip(row, vector))


# ------------------------------------------------------------- the push


def support_rows(source, z, colour):
    """Hard rows freezing the star coordinates that are currently zero.

    With these the deformation cannot create new support, so it stays inside
    the source's own stratum -- in particular a monomial source stays
    monomial and only its weights move.
    """
    rows = []
    for v in star_partners(z):
        block = source.oriented(z, v)
        for j in range(3):
            if block[colour][j] == 0:
                row = [Fraction(0)] * STAR_DIM
                row[star_index(z, v, j)] = Fraction(1)
                rows.append(row)
    return rows


def push_at_site(source, z, keep, order=None, verbose=False,
                 preserve_support=False):
    """One exact block-coordinate step of the exactness push.

    `keep` is the set of mixed words currently satisfied; they are imposed as
    hard constraints (together with the three pure equations) so the satisfied
    set is monotone.  Remaining mixed words are offered greedily in `order`
    (default: fewest support terms first) and accepted whenever the linear
    system stays consistent.  The new star is the orthogonal projection of the
    old one onto the affine solution set (the minimal deformation).

    Returns (new_source, accepted_words, info).
    """
    coefficients = all_coefficients(source)
    require(all(coefficients[PURE_WORDS[c]] == 1 for c in range(3)),
            "push_at_site expects a pure-normalised source (pure = 1)")
    require(all(coefficients[w] == 0 for w in keep),
            "push_at_site expects `keep` to be satisfied already")
    tables = cofactor_tables(source, z)
    if order is None:
        fibres = support_fibres(source)
        order = sorted(MIXED_WORDS, key=lambda w: (fibres[w], w))
    systems = {c: IncSystem(STAR_DIM) for c in range(3)}
    info = {"pure_infeasible": [], "keep_infeasible": [], "z": z,
            "preserve_support": preserve_support}
    if preserve_support:
        for c in range(3):
            for row in support_rows(source, z, c):
                require(systems[c].add_row(row, Fraction(0)),
                        "support row inconsistent")

    for c in range(3):
        row = star_row(tables, z, PURE_WORDS[c])
        if not systems[c].add_row(row, Fraction(1)):
            info["pure_infeasible"].append(c)
    for word in keep:
        row = star_row(tables, z, word)
        if not systems[word[z]].add_row(row, Fraction(0)):
            info["keep_infeasible"].append(word)
    # The current star solves pure=1 and every kept equation, so both blocks of
    # constraints must be consistent; a rejection would be a machinery bug.
    require(not info["pure_infeasible"] and not info["keep_infeasible"],
            "push_at_site: hard constraints reported inconsistent")

    accepted = []
    for word in order:
        if word in keep:
            continue
        c = word[z]
        row = star_row(tables, z, word)
        if systems[c].add_row(row, Fraction(0)):
            accepted.append(word)
    vectors = {c: systems[c].project(star_vector(source, z, c))
               for c in range(3)}
    info["ranks"] = {c: systems[c].rank() for c in range(3)}
    info["accepted"] = len(accepted)
    return apply_star(source, z, vectors), accepted, info


def push_cycle(source, sites=SITES, rounds=4, checkpoint=None, verbose=False,
               preserve_support=False):
    """Cycle the block-coordinate push over the sites until it stalls.

    Every step is verified against the INDEPENDENT coefficient routine:
    the words carried in `keep` must really have coefficient zero and the
    pure coefficients must really be one.
    """
    current = source
    coefficients = all_coefficients(current)
    keep = {w for w in MIXED_WORDS if coefficients[w] == 0}
    trace = [{"step": 0, "site": None, "satisfied": len(keep),
              "fraction": len(keep) / NMIXED}]
    if checkpoint is not None:
        trace[-1].update(checkpoint(current))
    step = 0
    for round_index in range(rounds):
        improved = False
        for z in sites:
            candidate, accepted, info = push_at_site(
                current, z, keep, preserve_support=preserve_support)
            check = all_coefficients(candidate)
            bad_pure = [c for c in range(3) if check[PURE_WORDS[c]] != 1]
            bad_keep = [w for w in keep if check[w] != 0]
            bad_new = [w for w in accepted if check[w] != 0]
            require(not bad_pure, f"push broke a pure equation at z={z}")
            require(not bad_keep, f"push broke a kept equation at z={z}")
            require(not bad_new, f"push failed to impose {len(bad_new)} words")
            new_keep = {w for w in MIXED_WORDS if check[w] == 0}
            require(keep <= new_keep, "the satisfied set must be monotone")
            step += 1
            if len(new_keep) > len(keep):
                improved = True
            current, keep = candidate, new_keep
            entry = {"step": step, "site": z, "satisfied": len(keep),
                     "fraction": len(keep) / NMIXED,
                     "accepted": info["accepted"],
                     "ranks": info["ranks"]}
            if checkpoint is not None:
                entry.update(checkpoint(current))
            trace.append(entry)
            if verbose:
                print(f"    site {z}: satisfied {len(keep)}/{NMIXED}"
                      f" ({len(keep)/NMIXED:.4f})", flush=True)
        if not improved:
            break
    return current, keep, trace


def impose_words(source, z, words, keep, preserve_support=False,
                 x0_shift=None, rng=None):
    """Least-change star at z imposing pure = 1, `keep`, and as many of `words`.

    Returns (new source, number of words accepted).  With preserve_support the
    zero pattern of the star is frozen, so the deformation stays in the
    source's own stratum.
    """
    tables = cofactor_tables(source, z)
    systems = {c: IncSystem(STAR_DIM) for c in range(3)}
    if preserve_support:
        for c in range(3):
            for row in support_rows(source, z, c):
                require(systems[c].add_row(row, Fraction(0)),
                        "support row inconsistent")
    for c in range(3):
        require(systems[c].add_row(star_row(tables, z, PURE_WORDS[c]),
                                   Fraction(1)), "pure row inconsistent")
    for word in keep:
        require(systems[word[z]].add_row(star_row(tables, z, word),
                                         Fraction(0)), "kept row inconsistent")
    accepted = 0
    for word in words:
        if systems[word[z]].add_row(star_row(tables, z, word), Fraction(0)):
            accepted += 1
    vectors = {}
    for c in range(3):
        base = star_vector(source, z, c)
        if x0_shift is not None and rng is not None:
            base = [value + Fraction(rng.randint(-x0_shift, x0_shift), 4)
                    for value in base]
        vectors[c] = systems[c].project(base)
    return apply_star(source, z, vectors), accepted


def prefix_push(source, z, fractions=(0.1, 0.25, 0.5, 0.75, 1.0)):
    """Incremental single-site imposition: growing prefixes of the mixed list.

    The words are ordered by support-fibre size (fewest live terms first) as
    the plan prescribes; each prefix is imposed by exact projection from the
    ORIGINAL star, so the trajectory is the minimal deformation path.
    """
    tables = cofactor_tables(source, z)
    fibres = support_fibres(source)
    coefficients = all_coefficients(source)
    violated = [w for w in MIXED_WORDS if coefficients[w] != 0]
    violated.sort(key=lambda w: (fibres[w], w))
    already = [w for w in MIXED_WORDS if coefficients[w] == 0]
    out = []
    for fraction in fractions:
        count = max(1, int(round(fraction * len(violated))))
        target = violated[:count]
        systems = {c: IncSystem(STAR_DIM) for c in range(3)}
        for c in range(3):
            systems[c].add_row(star_row(tables, z, PURE_WORDS[c]), Fraction(1))
        for word in already:
            systems[word[z]].add_row(star_row(tables, z, word), Fraction(0))
        accepted, refused = [], []
        for word in target:
            if systems[word[z]].add_row(star_row(tables, z, word), Fraction(0)):
                accepted.append(word)
            else:
                refused.append(word)
        vectors = {c: systems[c].project(star_vector(source, z, c))
                   for c in range(3)}
        candidate = apply_star(source, z, vectors)
        check = all_coefficients(candidate)
        require(all(check[PURE_WORDS[c]] == 1 for c in range(3)),
                "prefix push broke a pure equation")
        require(all(check[w] == 0 for w in accepted),
                "prefix push failed to impose an accepted word")
        out.append({"fraction_requested": fraction, "requested": count,
                    "accepted": len(accepted), "refused": len(refused),
                    "source": candidate})
    return out
