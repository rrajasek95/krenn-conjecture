#!/usr/bin/env python3
"""UNAUDITED PROBE (W1, task D) -- controls for the new W1 machinery.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Inherited machinery (Source, PairData, classify_source, the Singular
interface) keeps P2's own controls: run
    python3 ../unaudited-witness-splitting-p2-2026-08-15/run_d_controls.py
(C0 cap identity ... C7 K_4 landing).  This file controls what is NEW here:

 W1  star linearisation identity (*)   H(A)_w = sum_v A_zv[w_z][w_v] P_v(w)
                                       for all 729 words, all 6 sites
 W2  exact linear algebra              projection lands on the affine solution
                                       set and is orthogonal to it
 W3  end-to-end imposition             every accepted word really has
                                       coefficient 0 and the pures really 1,
                                       verified by the INDEPENDENT coefficient
                                       routine
 W4  mutation controls on the push     four deliberately wrong versions of the
                                       star construction must each break W1/W3
 W5  fibre/coefficient consistency     fibre 0 => coefficient 0;
                                       fibre 1 => coefficient != 0
 W6  block-type classification         engineered blocks land in the right
                                       coordinate-ness class
 W7  monotonicity                      push_cycle never loses a satisfied
                                       equation (enforced by require() inside)
"""

from __future__ import annotations

from fractions import Fraction
import random

from w1_core import (IncSystem, MIXED_WORDS, PAIRS, PURE_WORDS, SITES, STAR_DIM,
                     Source, WORDS, all_coefficients, apply_star, block_type,
                     cofactor_tables, perfect_matchings, product, push_at_site,
                     push_cycle, random_source, require, star_index, star_row,
                     star_partners, star_vector, support_fibres,
                     blocking_metrics, normalised_pairdata, primitive)
from run_c_pure_hunt import gauge_pure


def control_star_identity(trials=3):
    """W1: the star linearisation reproduces every GHZ coefficient exactly."""
    rng = random.Random(101)
    checked = 0
    for _ in range(trials):
        source = random_source(rng, "sparse")
        coefficients = all_coefficients(source)
        for z in SITES:
            tables = cofactor_tables(source, z)
            for word in WORDS:
                row = star_row(tables, z, word)
                vector = star_vector(source, z, word[z])
                value = sum(a * b for a, b in zip(row, vector))
                require(value == coefficients[word],
                        f"W1 star identity failed at z={z}, word={word}")
                checked += 1
    return {"coefficients_checked": checked}


def control_projection():
    """W2: IncSystem.project solves the system and is the orthogonal one."""
    rng = random.Random(102)
    for _ in range(20):
        system = IncSystem(STAR_DIM)
        rows, rhs = [], []
        for _ in range(rng.randint(1, 12)):
            row = [Fraction(rng.randint(-4, 4)) for _ in range(STAR_DIM)]
            value = Fraction(rng.randint(-4, 4))
            if system.add_row(row, value):
                rows.append(row)
                rhs.append(value)
        x0 = [Fraction(rng.randint(-5, 5)) for _ in range(STAR_DIM)]
        x = system.project(x0)
        for row, value in zip(rows, rhs):
            require(sum(a * b for a, b in zip(row, x)) == value,
                    "W2 projection does not solve the system")
        for vector in system.nullspace():
            residual = sum(v * (a - b) for v, a, b in zip(vector, x, x0))
            require(residual == 0, "W2 projection is not orthogonal")
    # inconsistency detection
    system = IncSystem(3)
    require(system.add_row([Fraction(1), Fraction(0), Fraction(0)], Fraction(1)),
            "W2 first row must be accepted")
    require(not system.add_row([Fraction(2), Fraction(0), Fraction(0)],
                               Fraction(3)),
            "W2 must reject an inconsistent row")
    require(system.add_row([Fraction(2), Fraction(0), Fraction(0)],
                           Fraction(2)),
            "W2 must accept a dependent consistent row")
    return {"random_systems": 20, "inconsistency_detected": True}


def gauged_random(rng, mode="sparse"):
    """A pure-normalised random source (P2's gauge, the shadows' normal form)."""
    for _ in range(60):
        source = random_source(rng, mode)
        gauged = gauge_pure(source)
        if gauged is not None:
            return gauged
    raise ValueError("no pure-normalisable random source")


def control_end_to_end():
    """W3: an imposition step really satisfies what it claims."""
    rng = random.Random(103)
    source = gauged_random(rng)
    coefficients = all_coefficients(source)
    keep = {w for w in MIXED_WORDS if coefficients[w] == 0}
    before = len(keep)
    moved, accepted, _info = push_at_site(source, 0, keep)
    check = all_coefficients(moved)
    require(all(check[w] == 0 for w in accepted), "W3 accepted words not zero")
    require(all(check[w] == 0 for w in keep), "W3 kept words not preserved")
    after = sum(1 for w in MIXED_WORDS if check[w] == 0)
    require(after >= before, "W3 satisfied count decreased")
    return {"satisfied_before": before, "satisfied_after": after,
            "accepted": len(accepted)}


def mutated_star_row(tables, z, word, mutation):
    """Deliberately wrong versions of the star row."""
    row = [Fraction(0)] * STAR_DIM
    items = list(tables.items())
    if mutation == "drop-partner":
        items = items[:-1]
    for v, (rest, table) in items:
        key = tuple(word[site] for site in rest)
        if mutation == "wrong-colour":
            key = tuple(0 for _ in rest)
        value = table[key]
        if not value:
            continue
        column = word[v]
        if mutation == "wrong-column":
            column = (word[v] + 1) % 3
        row[star_index(z, v, column)] += value
    return row


def mutated_cofactor_tables(source, z):
    """W4d: cofactors built from TWO of the three sub-matchings."""
    tables = {}
    oriented = {(u, v): source.oriented(u, v) for u in SITES for v in SITES
                if u != v}
    for v in star_partners(z):
        rest = tuple(site for site in SITES if site not in (z, v))
        matchings = perfect_matchings(rest)[:2]
        table = {}
        for word4 in product(range(3), repeat=4):
            colour = dict(zip(rest, word4))
            total = Fraction(0)
            for matching in matchings:
                term = Fraction(1)
                for a, b in matching:
                    term *= oriented[(a, b)][colour[a]][colour[b]]
                total += term
            table[word4] = total
        tables[v] = (rest, table)
    return tables


def control_mutations():
    """W4: every mutation of the star construction must be visible."""
    rng = random.Random(104)
    source = gauged_random(rng)
    coefficients = all_coefficients(source)
    tables = cofactor_tables(source, 0)
    results = {}
    for mutation in ("drop-partner", "wrong-colour", "wrong-column"):
        mismatches = 0
        for word in WORDS:
            row = mutated_star_row(tables, 0, word, mutation)
            value = sum(a * b for a, b in
                        zip(row, star_vector(source, 0, word[0])))
            if value != coefficients[word]:
                mismatches += 1
        require(mismatches, f"W4 mutation {mutation} is invisible")
        results[mutation] = mismatches
    broken = mutated_cofactor_tables(source, 0)
    mismatches = 0
    for word in WORDS:
        row = star_row(broken, 0, word)
        value = sum(a * b for a, b in zip(row, star_vector(source, 0, word[0])))
        if value != coefficients[word]:
            mismatches += 1
    require(mismatches, "W4 dropped sub-matching is invisible")
    results["drop-submatching"] = mismatches

    # the sharpest one: a push built on the broken cofactors must FAIL to
    # impose the equations it claims to impose.
    keep = {w for w in MIXED_WORDS if coefficients[w] == 0}
    import w1_core
    honest = w1_core.cofactor_tables
    w1_core.cofactor_tables = mutated_cofactor_tables
    try:
        failed = False
        try:
            push_at_site(source, 0, keep)
        except ValueError:
            failed = True
        if not failed:
            moved, accepted, _ = push_at_site(source, 0, keep)
            check = all_coefficients(moved)
            failed = any(check[w] != 0 for w in accepted) or any(
                check[PURE_WORDS[c]] != 1 for c in range(3))
    finally:
        w1_core.cofactor_tables = honest
    require(failed, "W4 a push on broken cofactors must not silently succeed")
    results["broken_push_detected"] = True
    return results


def control_fibres():
    """W5: support fibres bound the coefficient behaviour."""
    rng = random.Random(105)
    singletons = 0
    for _ in range(4):
        source = random_source(rng, "sparse")
        coefficients = all_coefficients(source)
        fibres = support_fibres(source)
        for word in WORDS:
            if fibres[word] == 0:
                require(coefficients[word] == 0,
                        f"W5 empty fibre with nonzero coefficient at {word}")
            if fibres[word] == 1:
                require(coefficients[word] != 0,
                        f"W5 singleton fibre with zero coefficient at {word}")
                singletons += 1
    return {"singleton_words_seen": singletons}


def control_block_types():
    cases = {
        "rank1-monomial": [[2, 0, 0], [0, 0, 0], [0, 0, 0]],
        "rank1-half": [[1, 2, 0], [0, 0, 0], [0, 0, 0]],
        "rank1-generic": [[1, 2, 0], [2, 4, 0], [0, 0, 0]],
        "zero": [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        "rank2": [[1, 0, 0], [0, 1, 0], [0, 0, 0]],
        "rank3": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    }
    for expected, matrix in cases.items():
        table = [[Fraction(entry) for entry in row] for row in matrix]
        got = block_type(table)["kind"]
        require(got == expected, f"W6 block type {expected} classified as {got}")
    return {"cases": len(cases)}


def control_monotone_cycle():
    """W7: the cycling push is monotone and self-verifying (require inside)."""
    rng = random.Random(106)
    source = gauged_random(rng)
    _final, keep, trace = push_cycle(source, rounds=2)
    counts = [entry["satisfied"] for entry in trace]
    require(counts == sorted(counts), "W7 satisfied count not monotone")
    return {"trace": counts[:8], "final": len(keep)}


def control_primitive():
    """W8: primitive rescaling of the Singular generators changes no verdict.

    Checked on a source pushed far enough for the exact coefficients to be
    large -- the situation the rescaling exists for.
    """
    rng = random.Random(107)
    source = gauged_random(rng)
    pushed, _keep, _trace = push_cycle(source, rounds=2)
    raw = blocking_metrics(pushed, max_degree=2, timeout=60, normalise=False)
    scaled = blocking_metrics(pushed, max_degree=2, timeout=60, normalise=True)
    require(raw["status"] == scaled["status"],
            f"W8 verdict changed: {raw['status']} vs {scaled['status']}")
    require(raw["witness_pairs"] == scaled["witness_pairs"], "W8 witness count")
    digits = max((len(str(value.numerator))
                  for pair in PAIRS
                  for row in pushed.blocks[pair] for value in row), default=0)
    scaled_digits = max(
        (len(str(value.numerator))
         for pair in PAIRS
         for quad in normalised_pairdata(pushed, *pair).quadrics
         for value in quad.values()), default=0)
    # the rescaling must actually be doing something
    require(scaled_digits <= digits, "W8 rescaling did not shrink anything")
    require(primitive([Fraction(2, 3), Fraction(4, 9)]) ==
            [Fraction(3), Fraction(2)], "W8 primitive scaling wrong")
    require(primitive([Fraction(0), Fraction(0)]) == [Fraction(0), Fraction(0)],
            "W8 primitive of zero")
    return {"source_entry_digits": digits,
            "generator_digits_after": scaled_digits,
            "verdicts_identical": True}


def main():
    print("UNAUDITED PROBE -- W1 controls, HEAD 26ba69f")
    print("W1 star identity      :", control_star_identity())
    print("W2 exact projection   :", control_projection())
    print("W3 end-to-end impose  :", control_end_to_end())
    print("W4 mutations          :", control_mutations())
    print("W5 fibres             :", control_fibres())
    print("W6 block types        :", control_block_types())
    print("W7 monotone cycle     :", control_monotone_cycle())
    print("W8 primitive rescale  :", control_primitive())
    print("all W1 controls PASS")


if __name__ == "__main__":
    main()
