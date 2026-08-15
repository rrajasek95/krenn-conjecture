#!/usr/bin/env python3
"""Exact minimum-parent census for the h=3 zero-top common-q branch.

This file is intentionally additive.  It studies the target-coordinate
projection of q on six residual sites.  The theorem and its precise scope
are documented in the companion note.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
from collections import Counter, defaultdict
from fractions import Fraction as Q


SITES = tuple(range(6))
COLORS = tuple(range(3))
EDGES = tuple(itertools.combinations(SITES, 2))
ATOMS = tuple((e, a, b) for e in EDGES for a in COLORS for b in COLORS)
WORDS = tuple(itertools.product(COLORS, repeat=6))
TARGETS = tuple((c,) * 6 for c in COLORS)
MATCH2 = tuple(
    tuple(sorted((e, f)))
    for e, f in itertools.combinations(EDGES, 2)
    if not set(e) & set(f)
)
PERMS6 = tuple(itertools.permutations(SITES))
PERMS3 = tuple(itertools.permutations(COLORS))

HERE = os.path.dirname(os.path.abspath(__file__))
PINS = {
    "verify_h3_degenerate_q3_fullnine_scalarzero_routing.py":
        "a22450f8281f46f04bcbc3943c40077b76bc5955d3c9c29670267d8e1e520d96",
    "../notes/2026-08-15-h3-degenerate-q3-fullnine-scalarzero-routing.md":
        "993bb3142c76e94e934e63fe36296d6321c919e0790dbebd5d597dcbdcf4a37b",
    "verify_h3_unified_dark_annihilator_singular_cap_boundary.py":
        "8cced865640ea93bbe3b72c5a1a9bd34d50eb2eaf2647a5dbbafa165f2cfc34e",
    "../notes/h3-unified-dark-annihilator-singular-cap-boundary.md":
        "1d66839c136fbb71aef349ad96dea4b62257f1e7ea63f7a224abe3af2ed582aa",
    "verify_uniform_pure_lift_private_edge_degeneration.py":
        "6c715abb7a5fb7139eac5c5b62a18e1989fa133fe209b3fe3ada4253e8219433",
    "../notes/uniform-pure-lift-private-edge-degeneration.md":
        "bb8b4f0b5315ca14354b7e7cbcd7d29a87dac7b519704ea3ca9cf8e2ebe94207",
}
EXPECTED_LEDGER_SHA256 = "7ed180d254ac446c06de3b3a9389ee3a593d4e2e4d2b2d3556ba805e3f55e883"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_sources():
    out = {}
    for relative, expected in sorted(PINS.items()):
        path = os.path.normpath(os.path.join(HERE, relative))
        with open(path, "rb") as handle:
            actual = hashlib.sha256(handle.read()).hexdigest()
        require(actual == expected, ("pinned source changed", relative, actual))
        out[relative] = actual
    return out


def atom_word(atom):
    (u, v), a, b = atom
    word = [None] * 6
    word[u] = a
    word[v] = b
    return tuple(word)


def disjoint(left, right):
    return not (set(left[0]) & set(right[0]))


def multiply_words(left, right):
    out = []
    for x, y in zip(left, right, strict=True):
        if x is not None and y is not None:
            return None
        out.append(x if x is not None else y)
    return tuple(out)


def divided_power(atoms, order, weights=None):
    if weights is None:
        weights = (Q(1),) * len(atoms)
    out = defaultdict(Q)
    for chosen in itertools.combinations(range(len(atoms)), order):
        word = (None,) * 6
        value = Q(1)
        for i in chosen:
            word = multiply_words(word, atom_word(atoms[i]))
            if word is None:
                break
            value *= weights[i]
        if word is not None:
            out[word] += value
    return {word: value for word, value in out.items() if value}


def pure_atoms(matching, colour):
    return tuple((edge, colour, colour) for edge in matching)


def skeleton(triple):
    return tuple(atom for c, matching in enumerate(triple)
                 for atom in pure_atoms(matching, c))


def matching_graph_has_pm(atoms):
    edges = {atom[0] for atom in atoms}
    return any(all(edge in edges for edge in matching)
               for matching in itertools.combinations(EDGES, 3)
               if len(set().union(*matching)) == 6)


def q2_profile(atoms, weights=None):
    return divided_power(atoms, 2, weights)


def q3_profile(atoms, weights=None):
    return divided_power(atoms, 3, weights)


def catalecticant_rows(f):
    """Rows of arbitrary r -> rF, indexed by six-site words."""
    rows = defaultdict(dict)
    atom_words = tuple(atom_word(atom) for atom in ATOMS)
    for four_word, value in f.items():
        occupied = {i for i, colour in enumerate(four_word)
                    if colour is not None}
        for atom_i, (atom, aw) in enumerate(zip(ATOMS, atom_words, strict=True)):
            if occupied & set(atom[0]):
                continue
            word = multiply_words(four_word, aw)
            rows[word][atom_i] = rows[word].get(atom_i, Q(0)) + value
    return {word: {i: value for i, value in row.items() if value}
            for word, row in rows.items() if any(row.values())}


def poly_add(left, right):
    out = Counter(left)
    out.update(right)
    return {monomial: value for monomial, value in out.items() if value}


def poly_mul(left, right):
    out = Counter()
    for a, ca in left.items():
        for b, cb in right.items():
            out[tuple(sorted(a + b))] += ca * cb
    return {monomial: value for monomial, value in out.items() if value}


def symbolic_q2(atoms):
    out = defaultdict(dict)
    for i, j in itertools.combinations(range(len(atoms)), 2):
        if not disjoint(atoms[i], atoms[j]):
            continue
        word = multiply_words(atom_word(atoms[i]), atom_word(atoms[j]))
        monomial = (i, j)
        out[word] = poly_add(out[word], {monomial: 1})
    return dict(out)


def symbolic_catalecticant_rows(atoms):
    f = symbolic_q2(atoms)
    rows = defaultdict(dict)
    for four_word, polynomial in f.items():
        occupied = {i for i, colour in enumerate(four_word)
                    if colour is not None}
        for atom_i, atom in enumerate(ATOMS):
            if occupied & set(atom[0]):
                continue
            word = multiply_words(four_word, atom_word(atom))
            rows[word][atom_i] = polynomial
    return dict(rows)


def symbolic_private_unit(atoms):
    """A two-row syzygy whose Delta value is a nonzero monomial.

    If A and B are entries of a mixed and target row and
    B*mixed-A*target=0 coefficientwise, its value on Delta is -A.  Requiring
    A to be a monomial makes the unit valid at every point of the coefficient
    torus, including the one-parameter rank-seven gauge families.
    """
    rows = symbolic_catalecticant_rows(atoms)
    zero = {}
    for target in TARGETS:
        target_row = rows.get(target, {})
        for word, mixed_row in rows.items():
            if word in TARGETS:
                continue
            common = sorted(set(target_row) & set(mixed_row))
            for column in common:
                a = mixed_row[column]
                b = target_row[column]
                if len(a) != 1:
                    continue
                columns = set(target_row) | set(mixed_row)
                if all(poly_mul(mixed_row.get(j, zero), b)
                       == poly_mul(target_row.get(j, zero), a)
                       for j in columns):
                    return {
                        "target": target,
                        "mate": word,
                        "target_multiplier": a,
                        "mate_multiplier": b,
                    }
    return None


def sparse_axpy(left, scale, right):
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, Q(0)) + scale * value
        if not out[key]:
            del out[key]
    return out


def exact_fredholm_unit(f):
    """Return omega with omega*A=0 and omega*Delta=1, if one exists."""
    equations = catalecticant_rows(f)
    basis = {}
    target_set = set(TARGETS)
    for word in WORDS:
        row = dict(equations.get(word, {}))
        rhs = Q(1) if word in target_set else Q(0)
        combo = {word: Q(1)}
        while row:
            pivot = min(row)
            if pivot not in basis:
                value = row[pivot]
                row = {key: coefficient / value
                       for key, coefficient in row.items()}
                rhs /= value
                combo = {key: coefficient / value
                         for key, coefficient in combo.items()}
                basis[pivot] = (row, rhs, combo)
                break
            coefficient = row[pivot]
            old_row, old_rhs, old_combo = basis[pivot]
            row = sparse_axpy(row, -coefficient, old_row)
            rhs -= coefficient * old_rhs
            combo = sparse_axpy(combo, -coefficient, old_combo)
        else:
            if rhs:
                combo = {key: coefficient / rhs
                         for key, coefficient in combo.items()}
                # Replay both sides literally.
                lhs = defaultdict(Q)
                value = Q(0)
                for source_word, coefficient in combo.items():
                    value += coefficient * (Q(1) if source_word in target_set
                                             else Q(0))
                    for column, entry in equations.get(source_word, {}).items():
                        lhs[column] += coefficient * entry
                require(not any(lhs.values()) and value == 1,
                        "Fredholm replay failed")
                return combo
    return None


def rank_fraction(rows):
    rows = [list(map(Q, row)) for row in rows]
    if not rows:
        return 0
    m, n = len(rows), len(rows[0])
    pivot = 0
    for col in range(n):
        hit = next((i for i in range(pivot, m) if rows[i][col]), None)
        if hit is None:
            continue
        rows[pivot], rows[hit] = rows[hit], rows[pivot]
        value = rows[pivot][col]
        rows[pivot] = [x / value for x in rows[pivot]]
        for i in range(m):
            if i != pivot and rows[i][col]:
                value = rows[i][col]
                rows[i] = [x - value * y
                           for x, y in zip(rows[i], rows[pivot], strict=True)]
        pivot += 1
        if pivot == m:
            break
    return pivot


def target_fixed_torus_rank(atoms):
    # Columns are the 18 site/colour diagonal gauges.  Atom weights use the
    # two incident gauges; target preservation imposes sum_site g_site,c=0.
    rows = []
    for edge, a, b in atoms:
        row = [0] * 18
        row[3 * edge[0] + a] += 1
        row[3 * edge[1] + b] += 1
        rows.append(row)
    target_rows = []
    for c in COLORS:
        row = [0] * 18
        for site in SITES:
            row[3 * site + c] = 1
        target_rows.append(row)
    base = rank_fraction(target_rows)
    return rank_fraction(target_rows + rows) - base


def transform_matching(matching, site_perm):
    return tuple(sorted(tuple(sorted((site_perm[u], site_perm[v])))
                        for u, v in matching))


def transform_triple(triple, site_perm, colour_perm):
    out = [None] * 3
    for old_c, matching in enumerate(triple):
        out[colour_perm[old_c]] = transform_matching(matching, site_perm)
    return tuple(out)


def orbit_of_triple(rep):
    return {transform_triple(rep, sp, cp)
            for sp in PERMS6 for cp in PERMS3}


MIN2_A = (
    (((0, 1), (2, 3))),
    (((0, 1), (2, 3))),
    (((0, 2), (1, 3))),
)
MIN2_B = (
    (((0, 1), (2, 3))),
    (((0, 2), (1, 3))),
    (((0, 3), (1, 4))),
)
CONTRACTED_GUARD = (
    (((0, 1), (2, 3))),
    (((0, 2), (1, 4))),
    (((0, 3), (1, 5))),
)
SECOND_CONTRACTED_GUARD = (
    (((0, 1), (2, 3))),
    (((0, 4), (2, 5))),
    (((1, 4), (3, 5))),
)


def mixed_term_count(f):
    return sum(1 for word in f
               if len({colour for colour in word if colour is not None}) > 1)


def full_six_cell_orbit_census():
    candidates = set()
    histogram = Counter()
    for triple in itertools.product(MATCH2, repeat=3):
        atoms = skeleton(triple)
        top = q3_profile(atoms)
        has_pm = matching_graph_has_pm(atoms)
        require(bool(top) == has_pm and all(value == 1 for value in top.values()),
                "a six-cell top acquired a cancellation or missed a matching")
        if has_pm:
            continue
        require(target_fixed_torus_rank(atoms) == 6,
                "a six-cell coefficient torus lost a gauge coordinate")
        mixed = mixed_term_count(q2_profile(atoms))
        histogram[mixed] += 1
        candidates.add(triple)
    require(len(candidates) == 37845, len(candidates))
    require(histogram == Counter({0: 90, 2: 2430, 3: 7200,
                                  4: 14040, 5: 6480, 6: 7605}), histogram)

    records = []
    while candidates:
        rep = min(candidates)
        labelled_orbit = candidates & orbit_of_triple(rep)
        atoms = skeleton(rep)
        f = q2_profile(atoms)
        symbolic = symbolic_private_unit(atoms)
        exact_omega = None if symbolic else exact_fredholm_unit(f)
        records.append({
            "rep": rep,
            "orbit_size": len(labelled_orbit),
            "mixed_terms": mixed_term_count(f),
            "symbolic_two_word_unit": symbolic is not None,
            "exact_fredholm_size": (len(exact_omega)
                                      if exact_omega is not None else None),
            "contracted_survivor": symbolic is None and exact_omega is None,
        })
        candidates -= orbit_of_triple(rep)

    survivors = [record for record in records if record["contracted_survivor"]]
    require(len(records) == 23, len(records))
    require([(record["rep"], record["orbit_size"], record["mixed_terms"])
             for record in survivors]
            == [(CONTRACTED_GUARD, 2160, 4),
                (SECOND_CONTRACTED_GUARD, 360, 6)], survivors)
    minimum = [record for record in records if record["mixed_terms"] == 2]
    require([(record["rep"], record["orbit_size"])
             for record in minimum]
            == [(MIN2_A, 270), (MIN2_B, 2160)], minimum)
    require(all(record["symbolic_two_word_unit"] for record in minimum),
            "a minimum non-pure orbit lost its coefficient-uniform unit")
    return histogram, records


def endpoint_form(entries):
    return {(site, colour): Q(value) for site, colour, value in entries
            if value}


def endpoint_product(left, right):
    out = defaultdict(Q)
    for (u, a), x in left.items():
        for (v, b), y in right.items():
            if u == v:
                continue
            atom = ((u, v), a, b) if u < v else ((v, u), b, a)
            out[atom] += x * y
    return {atom: value for atom, value in out.items() if value}


def add_atom_forms(*forms):
    out = defaultdict(Q)
    for form in forms:
        for atom, value in form.items():
            out[atom] += value
    return {atom: value for atom, value in out.items() if value}


def atom_form_times_f(form, f):
    out = defaultdict(Q)
    for atom, coefficient in form.items():
        aw = atom_word(atom)
        for four_word, value in f.items():
            word = multiply_words(aw, four_word)
            if word is not None:
                out[word] += coefficient * value
    return {word: value for word, value in out.items() if value}


def divided_power_of_atom_form(form, order):
    atoms = tuple(form)
    weights = tuple(form[atom] for atom in atoms)
    return divided_power(atoms, order, weights)


def word_label(word):
    return "".join("." if value is None else str(value) for value in word)


def audit_first_contracted_guard():
    q_atoms = skeleton(CONTRACTED_GUARD)
    f = q2_profile(q_atoms)
    require(not q3_profile(q_atoms), "the first guard acquired a unary top")
    require(mixed_term_count(f) == 4 and len(f) == 7,
            "the first guard profile changed")

    # A rank-two response after the universal dark-plane reduction.  The
    # two invisible same-site terms in its symmetric completion are exactly
    # why ordinary matrix rank is not a valid two-channel obstruction.
    u0 = endpoint_form(((4, 0, 1), (2, 2, 1)))
    v0 = endpoint_form(((5, 0, 1), (4, 2, 1)))
    u1 = endpoint_form(((5, 1, 1), (2, 2, 1)))
    v1 = endpoint_form(((5, 0, -1), (3, 1, 1)))
    rank_two = add_atom_forms(endpoint_product(u0, v0),
                              endpoint_product(u1, v1))
    expected_rank_two = {
        ((4, 5), 0, 0): Q(1),
        ((3, 5), 1, 1): Q(1),
        ((2, 4), 2, 2): Q(1),
        ((2, 3), 2, 1): Q(1),
    }
    require(rank_two == expected_rank_two, rank_two)
    require(atom_form_times_f(rank_two, f)
            == {target: Q(1) for target in TARGETS},
            "the rank-two response stopped contracting to Delta")
    require(not divided_power_of_atom_form(rank_two, 3),
            "the singular response unexpectedly retained a root")

    # Add a third, response-kernel channel.  With K_*=I and direct block
    # a_01=-1 this is precisely an invertible scalar-zero selected packet.
    u2 = endpoint_form(((0, 0, 1),))
    v2 = endpoint_form(((1, 0, 1),))
    rank_three = add_atom_forms(rank_two, endpoint_product(u2, v2))
    require(atom_form_times_f(endpoint_product(u2, v2), f) == {},
            "the root channel stopped being response-dark")
    require(atom_form_times_f(rank_three, f)
            == {target: Q(1) for target in TARGETS},
            "the invertible contracted response changed")
    root = divided_power_of_atom_form(rank_three, 3)
    require(root and root[(0, 0, 2, 1, 2, 1)] == 1,
            "the invertible response lost its literal root")

    p = (u0, u1, u2)
    s = (v0, v1, v2)
    table = {}
    failures = []
    for i, j in itertools.product(COLORS, repeat=2):
        value = atom_form_times_f(endpoint_product(p[i], s[j]), f)
        expected = {TARGETS[i]: Q(1)} if i == j else {}
        table["%d%d" % (i, j)] = {
            word_label(word): str(coefficient)
            for word, coefficient in sorted(value.items(),
                                             key=lambda item: word_label(item[0]))
        }
        if value != expected:
            failures.append((i, j))
    require(failures == [(0, 0), (0, 1), (1, 0), (1, 1),
                         (2, 0), (2, 1), (2, 2)], failures)

    direct = [[Q(0) for _ in COLORS] for _ in COLORS]
    direct[0][1] = Q(-1)
    require(sum(direct[i][i] for i in COLORS) == 0,
            "the direct block is not trace zero")
    # K_*=tr(a)E_01-a_01 I=I and <K_*,a>=tr(a)=0.
    return {
        "q_atoms": q_atoms,
        "q2": {word_label(word): str(value) for word, value in f.items()},
        "q3": {},
        "singular_rank_two_response": {
            "%d%d:%d%d" % (atom[0][0], atom[0][1], atom[1], atom[2]):
                str(value)
            for atom, value in rank_two.items()
        },
        "singular_response_cube": {},
        "invertible_K_star": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        "direct_nonzero": {"a_01": -1},
        "sigma_K_star": 0,
        "root_words": {word_label(word): str(value)
                       for word, value in root.items()},
        "contracted_equation": "r(K_*) q^[2] = Delta_6",
        "displayed_factorization_fullnine_failures": failures,
        "displayed_factorization_rows": table,
        "scope": (
            "literal common-q and contracted scalar-zero/rootful packet; "
            "not a full-nine source because the displayed endpoint rectangle "
            "has seven failed entries"
        ),
    }


def audit(mode):
    pins = pin_sources()
    histogram, orbits = full_six_cell_orbit_census()
    minimum = [record for record in orbits if record["mixed_terms"] == 2]
    survivors = [record for record in orbits if record["contracted_survivor"]]
    guard = audit_first_contracted_guard()
    return {
        "pins": pins,
        "mode": "same exact theorem in all modes",
        "six_cell_no_top_profiles": dict(histogram),
        "six_cell_orbit_count": len(orbits),
        "minimum_nonpure_mixed_terms": 2,
        "minimum_nonpure_orbits": minimum,
        "contracted_survivors": survivors,
        "first_contracted_guard": guard,
        "conclusion": (
            "minimum non-pure profiles are unit-excluded; the first common-q "
            "contracted survivor already has six q cells and survives the "
            "rank-two cap reduction, but the exhibited three-channel lift is "
            "not full-nine"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    args = parser.parse_args()
    result = audit(args.mode)
    payload = json.dumps(result, sort_keys=True, default=str)
    digest = hashlib.sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            ("ledger changed", digest))
    print(payload)
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
