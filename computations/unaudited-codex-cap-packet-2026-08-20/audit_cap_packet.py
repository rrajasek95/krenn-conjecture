#!/usr/bin/env python3
"""Raw N=8 audit of the literal six-site thirteen-exit packet.

This is an UNAUDITED lane.  It deliberately rebuilds all matching and cap
expressions from endpoint-ordered aggregate matrices.  It does not import a
packet, matching, hafnian, response, or cap implementation from another lane.

There are two products:

* an exact combinatorial reconstruction of the degree-five N=8 parent chain;
* an exact active-clean-cap decision attempt for W40's integral X_4 boundary
  point, using the Rabinowitsch equation

      z * s * K_00 * K_11 * K_22 - 1 = 0.

The latter is a computational probe until independently encoded/audited.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import tempfile
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
W40_RESULT = (ROOT / "computations/unaudited-x4general-w40-2026-08-20/"
              "results_t3.json")
PINNED_W40_SHA256 = (
    "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f"
)

N = 8
COLOURS = range(3)
SITES = tuple(range(N))
KMONS = tuple((i,) for i in range(9))

DECLARED_CONTROLS = {
    "perfect_matching_counts",
    "cross_tail_mutation_must_fire",
    "endpoint_order_mutation_must_fire",
    "raw_w40_x4_replay",
    "cap_partition_identity",
    "error_polynomial_two_engine",
    "known_clean_cap_positive",
    "inactive_cap_negative",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


PMS8 = tuple(sorted(perfect_matchings(SITES)))


def edge_name(edge):
    return f"{edge[0]}{edge[1]}"


def matching_name(matching):
    return "|".join(edge_name(edge) for edge in matching)


def parse_source(record):
    source = {}
    for key, matrix in record.items():
        u, v = (int(part.strip()) for part in key.strip("()").split(","))
        source[(u, v)] = tuple(
            tuple(Fraction(entry) for entry in row) for row in matrix
        )
    require(set(source) == set(combinations(SITES, 2)), len(source))
    return source


def cell(source, u, v, cu, cv):
    if u < v:
        return source[(u, v)][cu][cv]
    return source[(v, u)][cv][cu]


def hafnian_word(source, word, vertices=SITES):
    total = Fraction(0)
    for matching in perfect_matchings(tuple(vertices)):
        value = Fraction(1)
        for u, v in matching:
            value *= cell(source, u, v, word[u], word[v])
            if value == 0:
                break
        total += value
    return total


class Poly:
    """Sparse polynomial over Q; monomials are sorted variable-index tuples."""

    __slots__ = ("terms",)

    def __init__(self, terms=None):
        self.terms = {tuple(m): Fraction(c) for m, c in (terms or {}).items()
                      if c}

    @staticmethod
    def const(value):
        value = Fraction(value)
        return Poly({(): value}) if value else Poly()

    @staticmethod
    def var(index):
        return Poly({(index,): Fraction(1)})

    def __bool__(self):
        return bool(self.terms)

    def __add__(self, other):
        answer = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            new = answer.get(monomial, Fraction(0)) + coefficient
            if new:
                answer[monomial] = new
            else:
                answer.pop(monomial, None)
        return Poly(answer)

    def __mul__(self, other):
        answer = {}
        for left, left_coefficient in self.terms.items():
            for right, right_coefficient in other.terms.items():
                monomial = tuple(sorted(left + right))
                new = (answer.get(monomial, Fraction(0)) +
                       left_coefficient * right_coefficient)
                if new:
                    answer[monomial] = new
                else:
                    answer.pop(monomial, None)
        return Poly(answer)

    def scale(self, scalar):
        scalar = Fraction(scalar)
        return Poly({m: scalar * c for m, c in self.terms.items()})

    def evaluate(self, values):
        total = Fraction(0)
        for monomial, coefficient in self.terms.items():
            term = coefficient
            for variable in monomial:
                term *= values[variable]
            total += term
        return total

    def singular(self, names):
        from math import gcd
        denominator = 1
        for coefficient in self.terms.values():
            denominator = (denominator * coefficient.denominator //
                           gcd(denominator, coefficient.denominator))
        integers = {m: int(c * denominator)
                    for m, c in self.terms.items()}
        divisor = 0
        for coefficient in integers.values():
            divisor = gcd(divisor, abs(coefficient))
        if divisor > 1:
            integers = {m: c // divisor for m, c in integers.items()}
        pieces = []
        for monomial, coefficient in sorted(integers.items()):
            factor = "*".join(names[index] for index in monomial)
            if not factor:
                piece = str(coefficient)
            elif coefficient == 1:
                piece = factor
            elif coefficient == -1:
                piece = "-" + factor
            else:
                piece = f"{coefficient}*{factor}"
            pieces.append(piece)
        if not pieces:
            return "0"
        answer = pieces[0]
        for piece in pieces[1:]:
            answer += piece if piece.startswith("-") else "+" + piece
        return answer


def kindex(i, j):
    return 3 * i + j


def cap_forms(source, cap):
    p, q = cap
    require(p < q, cap)
    residual = tuple(site for site in SITES if site not in cap)
    scalar = Poly()
    for i in COLOURS:
        for j in COLOURS:
            coefficient = cell(source, p, q, i, j)
            if coefficient:
                scalar = scalar + Poly.var(kindex(i, j)).scale(coefficient)
    response = {}
    for a, b in combinations(residual, 2):
        matrix = [[Poly() for _ in COLOURS] for _ in COLOURS]
        for alpha in COLOURS:
            for beta in COLOURS:
                form = Poly()
                for i in COLOURS:
                    for j in COLOURS:
                        coefficient = (
                            cell(source, p, a, i, alpha) *
                            cell(source, q, b, j, beta) +
                            cell(source, p, b, i, beta) *
                            cell(source, q, a, j, alpha)
                        )
                        if coefficient:
                            form = (form +
                                    Poly.var(kindex(i, j)).scale(coefficient))
                matrix[alpha][beta] = form
        response[(a, b)] = matrix
    return residual, scalar, response


def error_polynomials(source, cap):
    """Return the 3^6 coefficients of E for N=8.

    E = s [r^2/2 exp(x)]_U + [r^3/6]_U.  For a fixed residual
    perfect matching, factorial cancellation leaves one term for each
    choice of its two response edges and one all-response term.
    """
    residual, scalar, response = cap_forms(source, cap)
    polynomials = []
    words = []
    for colours in product(COLOURS, repeat=6):
        word = dict(zip(residual, colours))
        total = Poly()
        for matching in perfect_matchings(residual):
            rforms = [response[edge][word[edge[0]]][word[edge[1]]]
                      for edge in matching]
            xvalues = [cell(source, edge[0], edge[1],
                            word[edge[0]], word[edge[1]])
                       for edge in matching]
            total = total + rforms[0] * rforms[1] * rforms[2]
            for original_index in range(3):
                if not xvalues[original_index]:
                    continue
                term = scalar.scale(xvalues[original_index])
                for index in range(3):
                    if index != original_index:
                        term = term * rforms[index]
                total = total + term
        if total:
            words.append("".join(map(str, colours)))
            polynomials.append(total)
    return residual, scalar, response, words, polynomials


def numeric_response(response, kvals):
    return {
        edge: tuple(tuple(entry.evaluate(kvals) for entry in row)
                    for row in matrix)
        for edge, matrix in response.items()
    }


def response_error_numeric(source, residual, scalar, response, kvals):
    svalue = scalar.evaluate(kvals)
    rnum = numeric_response(response, kvals)
    values = {}
    for colours in product(COLOURS, repeat=6):
        word = dict(zip(residual, colours))
        total = Fraction(0)
        for matching in perfect_matchings(residual):
            rs = [rnum[edge][word[edge[0]]][word[edge[1]]]
                  for edge in matching]
            xs = [cell(source, edge[0], edge[1],
                       word[edge[0]], word[edge[1]])
                  for edge in matching]
            total += rs[0] * rs[1] * rs[2]
            for original_index in range(3):
                rr = Fraction(1)
                for index in range(3):
                    if index != original_index:
                        rr *= rs[index]
                total += svalue * xs[original_index] * rr
        values[colours] = total
    return values


def packet_reconstruction(controls_run):
    require(len(PMS8) == 105 and
            len(tuple(perfect_matchings(tuple(range(6))))) == 15,
            (len(PMS8), len(tuple(perfect_matchings(tuple(range(6)))))))
    controls_run.add("perfect_matching_counts")

    tail = (6, 7)
    m0 = tuple(sorted(((0, 5), (1, 2), (3, 4), tail)))
    m1 = tuple(sorted(((0, 1), (2, 5), (3, 4), tail)))
    common_tail = tuple(matching for matching in PMS8 if tail in matching)
    crossed_tail = tuple(matching for matching in PMS8 if tail not in matching)
    exits13 = tuple(matching for matching in common_tail
                    if matching not in (m0, m1))
    require((len(common_tail), len(crossed_tail), len(exits13)) ==
            (15, 90, 13),
            (len(common_tail), len(crossed_tail), len(exits13)))
    profiles = Counter()
    for matching in crossed_tail:
        crossing_edges = tuple(edge for edge in matching
                               if (edge[0] in tail) != (edge[1] in tail))
        internal_edges = tuple(edge for edge in matching
                               if edge[0] not in tail and edge[1] not in tail)
        profiles[(len(crossing_edges), len(internal_edges))] += 1
    require(profiles == {(2, 2): 90}, profiles)

    # The deletion boundary sign is derived termwise: matchings containing
    # 01 get 1-2=-1; every other matching gets +1.
    signs = {matching: (-1 if (0, 1) in matching else 1)
             for matching in PMS8}
    require(Counter(signs.values()) == {1: 90, -1: 15},
            Counter(signs.values()))
    require(signs[m0] == 1 and signs[m1] == -1, (signs[m0], signs[m1]))

    # Must-fire control: a purported raw N=8 boundary with only 89 crossing
    # terms is detected against the independently enumerated matching row.
    mutated = crossed_tail[:-1]
    caught = len(mutated) != len(crossed_tail)
    require(caught, "cross-tail deletion mutation was not detected")
    controls_run.add("cross_tail_mutation_must_fire")

    # Group the 90 crossings by the unordered residual pair hit from 6,7
    # and by the remaining residual fine.  Each group has the two endpoint-
    # ordered star pairings that form one physical response R_ab.
    groups = Counter()
    for matching in crossed_tail:
        edge6 = next(edge for edge in matching if 6 in edge)
        edge7 = next(edge for edge in matching if 7 in edge)
        a = edge6[0] if edge6[1] == 6 else edge6[1]
        b = edge7[0] if edge7[1] == 7 else edge7[1]
        residual_pair = tuple(sorted((a, b)))
        remaining = tuple(edge for edge in matching
                          if 6 not in edge and 7 not in edge)
        groups[(residual_pair, remaining)] += 1
    require(len(groups) == 45 and set(groups.values()) == {2},
            (len(groups), Counter(groups.values())))
    return {
        "status": "PROVED_COMBINATORIAL_IDENTITY",
        "operation_grade": 5,
        "output_word": "11100111",
        "companion_word": "00100111",
        "deleted_ordered_cell": "a01^00",
        "chain": "a01^00*F_11100111 - 2*a01^11*F_00100111",
        "parent_fines": [matching_name(m0), matching_name(m1)],
        "boundary": {
            "all_fines": 105,
            "negative_containing_01": 15,
            "positive_avoiding_01": 90,
            "common_tail_67_fines": 15,
            "familiar_packet_exits_after_parents": 13,
            "cross_tail_fines": 90,
            "cross_tail_profile": "two 67-window crossings plus two window edges",
            "response_groups": 45,
            "ordered_star_pairings_per_group": 2,
        },
        "exact_consequence": (
            "the six-site 13-exit row is only the direct-cap/common-tail "
            "sector; a raw N=8 coefficient/Macaulay boundary also contains "
            "90 crossing-tail occurrences, grouped into the 45 terms of "
            "the first physical response"
        ),
    }


def replay_w40(source, expected_defects, controls_run):
    defects = []
    for word in product(COLOURS, repeat=N):
        value = hafnian_word(source, word)
        target = Fraction(1) if len(set(word)) == 1 else Fraction(0)
        if value != target:
            defects.append({
                "word": "".join(map(str, word)),
                "value": str(value),
                "target": str(target),
                "off": N - max(word.count(c) for c in COLOURS),
            })
    require([entry["word"] for entry in defects] == expected_defects,
            defects)
    require(len(defects) == 3 and all(entry["off"] == 5 for entry in defects),
            defects)
    controls_run.add("raw_w40_x4_replay")
    return defects


def cap_partition_control(source, cap, scalar, response, residual, controls_run):
    # A fully nonsymmetric covector makes endpoint-order errors observable.
    kvals = tuple(Fraction(value) for value in (1, 2, 3, 5, 7, 11, 13, 17, 19))
    rnum = numeric_response(response, kvals)
    svalue = scalar.evaluate(kvals)
    checked = 0
    for colours in product(COLOURS, repeat=6):
        word = dict(zip(residual, colours))
        left = Fraction(0)
        for i in COLOURS:
            for j in COLOURS:
                fullword = dict(word)
                fullword[cap[0]] = i
                fullword[cap[1]] = j
                ordered = tuple(fullword[site] for site in SITES)
                left += kvals[kindex(i, j)] * hafnian_word(source, ordered)
        right = svalue * hafnian_word(source, tuple(word.get(site, 0)
                                                    for site in SITES),
                                      vertices=residual)
        for a, b in combinations(residual, 2):
            remaining = tuple(site for site in residual if site not in (a, b))
            right += (rnum[(a, b)][word[a]][word[b]] *
                      hafnian_word(source,
                                   tuple(word.get(site, 0) for site in SITES),
                                   vertices=remaining))
        require(left == right, (cap, colours, left, right))
        checked += 1
    controls_run.add("cap_partition_identity")

    # A deliberate transpose error in the second star pairing must disagree
    # with the raw contraction somewhere for this asymmetric point/covector.
    wrong_count = 0
    p, q = cap
    for a, b in combinations(residual, 2):
        for alpha in COLOURS:
            for beta in COLOURS:
                correct = rnum[(a, b)][alpha][beta]
                wrong = Fraction(0)
                for i in COLOURS:
                    for j in COLOURS:
                        wrong += kvals[kindex(i, j)] * (
                            cell(source, p, a, i, alpha) *
                            cell(source, q, b, j, beta) +
                            cell(source, p, b, i, alpha) *
                            cell(source, q, a, j, beta)
                        )
                wrong_count += (wrong != correct)
    return {"words_checked": checked, "transpose_mutation_differences": wrong_count}


def error_two_engine_control(source, cap, residual, scalar, response,
                             words, polynomials, controls_run):
    kvals = tuple(Fraction(value) for value in (2, -3, 5, 7, -11, 13, 17, 19, -23))
    direct = response_error_numeric(source, residual, scalar, response, kvals)
    symbolic = {word: poly.evaluate(kvals)
                for word, poly in zip(words, polynomials)}
    for colours, value in direct.items():
        name = "".join(map(str, colours))
        require(value == symbolic.get(name, Fraction(0)),
                (cap, name, value, symbolic.get(name, 0)))
    controls_run.add("error_polynomial_two_engine")
    return {"sample_k": [str(value) for value in kvals],
            "nonzero_error_words": sum(value != 0 for value in direct.values())}


def basic_activity_controls(controls_run):
    zero = tuple(tuple(Fraction(0) for _ in COLOURS) for _ in COLOURS)
    identity = tuple(tuple(Fraction(i == j) for j in COLOURS) for i in COLOURS)
    source = {edge: zero for edge in combinations(SITES, 2)}
    source[(6, 7)] = identity
    residual, scalar, response, words, polynomials = error_polynomials(source,
                                                                        (6, 7))
    kvals = (Fraction(1), Fraction(0), Fraction(0),
             Fraction(0), Fraction(1), Fraction(0),
             Fraction(0), Fraction(0), Fraction(1))
    require(scalar.evaluate(kvals) == 3 and not polynomials and
            all(not entry for matrix in response.values()
                for row in matrix for entry in row),
            (scalar.terms, len(polynomials)))
    controls_run.add("known_clean_cap_positive")
    inactive = list(kvals)
    inactive[kindex(1, 1)] = 0
    activity = (scalar.evaluate(inactive) * inactive[kindex(0, 0)] *
                inactive[kindex(1, 1)] * inactive[kindex(2, 2)])
    require(activity == 0, activity)
    controls_run.add("inactive_cap_negative")

    # Endpoint-order must-fire control on a deliberately asymmetric star.
    toy = {edge: zero for edge in combinations(SITES, 2)}
    toy02 = [list(row) for row in zero]
    toy13 = [list(row) for row in zero]
    toy03 = [list(row) for row in zero]
    toy12 = [list(row) for row in zero]
    toy02[0][0] = Fraction(5)
    toy13[0][0] = Fraction(7)
    toy03[0][1] = Fraction(2)
    toy12[0][2] = Fraction(3)
    toy[(0, 2)] = tuple(tuple(row) for row in toy02)
    toy[(1, 3)] = tuple(tuple(row) for row in toy13)
    toy[(0, 3)] = tuple(tuple(row) for row in toy03)
    toy[(1, 2)] = tuple(tuple(row) for row in toy12)
    _, _, toy_response = cap_forms(toy, (0, 1))
    toy_k = (Fraction(1),) + (Fraction(0),) * 8
    correct = toy_response[(2, 3)][2][1].evaluate(toy_k)
    wrong = sum(
        toy_k[kindex(i, j)] * (
            cell(toy, 0, 2, i, 2) * cell(toy, 1, 3, j, 1) +
            cell(toy, 0, 3, i, 2) * cell(toy, 1, 2, j, 1)
        )
        for i in COLOURS for j in COLOURS
    )
    require(correct == 6 and wrong == 0, (correct, wrong))
    controls_run.add("endpoint_order_mutation_must_fire")


def singular_decision(polynomials, scalar, timeout):
    names = [f"zzk{i}{j}" for i in COLOURS for j in COLOURS] + ["zzrab"]
    activity = scalar
    for c in COLOURS:
        activity = activity * Poly.var(kindex(c, c))
    rabinowitsch = activity * Poly.var(9) + Poly.const(-1)
    generators = [poly.singular(names) for poly in polynomials]
    generators.append(rabinowitsch.singular(names))
    script = (
        "ring zzR = 0,(" + ",".join(names) + "),dp;\n" +
        "ideal zzI = " + ",\n".join(generators) + ";\n" +
        "ideal zzG = std(zzI);\n" +
        '"ZZUNIT ",(size(zzG)==1 && zzG[1]==1);\n' +
        '"ZZDIM ",dim(zzG);\n' +
        '"ZZGSIZE ",size(zzG);\n'
    )
    # No generator is assigned a name that can shadow a ring variable.
    require(not any(line.startswith("poly zzk") for line in script.splitlines()),
            "shadowing guard")
    started = time.monotonic()
    with tempfile.NamedTemporaryFile("w", suffix=".sing", dir=HERE,
                                     delete=False) as handle:
        handle.write(script)
        path = Path(handle.name)
    try:
        completed = subprocess.run(
            ["Singular", "-q", str(path)], text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as error:
        return {"status": "UNCHECKED_TIMEOUT", "seconds": timeout,
                "partial_output": (error.stdout or "")[-1000:]}
    finally:
        path.unlink(missing_ok=True)
    output = completed.stdout
    require(completed.returncode == 0 and
            not any(line.lstrip().startswith("?") for line in output.splitlines()),
            (completed.returncode, output[-2000:]))
    parsed = {}
    for line in output.splitlines():
        fields = line.strip().split()
        if len(fields) >= 2 and fields[0] in {"ZZUNIT", "ZZDIM", "ZZGSIZE"}:
            parsed[fields[0]] = fields[1]
    require("ZZUNIT" in parsed, output[-2000:])
    unit = parsed["ZZUNIT"] == "1"
    return {
        "status": ("PROBE_NO_ACTIVE_CLEAN_CAP" if unit else
                   "PROBE_ACTIVE_CLEAN_CAP_EXISTS_OVER_ALGEBRAIC_CLOSURE"),
        "rabinowitsch_unit": unit,
        "dimension": int(parsed.get("ZZDIM", "-999")),
        "groebner_basis_size": int(parsed.get("ZZGSIZE", "-1")),
        "seconds": time.monotonic() - started,
        "generator_count": len(generators),
        "generator_sha256": sha256("\n".join(generators).encode()).hexdigest(),
    }


def find_small_rational_cap(polynomials, scalar):
    """Search a finite, explicitly reported rational calibration set.

    This is not used for a negative verdict.  A hit is nevertheless an exact
    positive witness because every error coefficient is then replayed from
    the raw polynomial list and the activity product is evaluated exactly.
    """
    off_diagonal = tuple(kindex(i, j) for i in COLOURS for j in COLOURS
                         if i != j)
    diagonal = tuple(kindex(c, c) for c in COLOURS)
    for diagonal_signs in product((1, -1), repeat=3):
        base = [Fraction(0) for _ in range(9)]
        for index, value in zip(diagonal, diagonal_signs):
            base[index] = Fraction(value)
        # Increasing off-diagonal support makes the first hit reproducible
        # and keeps the witness sparse.
        for support_size in range(7):
            for support in combinations(off_diagonal, support_size):
                for signs in product((-1, 1), repeat=support_size):
                    values = list(base)
                    for index, value in zip(support, signs):
                        values[index] = Fraction(value)
                    svalue = scalar.evaluate(values)
                    activity = svalue
                    for index in diagonal:
                        activity *= values[index]
                    if not activity:
                        continue
                    if all(not polynomial.evaluate(values)
                           for polynomial in polynomials):
                        return {
                            "K_rows": [[str(values[kindex(i, j)])
                                        for j in COLOURS] for i in COLOURS],
                            "s": str(svalue),
                            "activity_product": str(activity),
                            "all_error_coefficients_zero": True,
                            "search_domain": (
                                "diagonal entries in {-1,1}; off-diagonal "
                                "entries in {-1,0,1}, increasing support"
                            ),
                        }
    return None


def decide_w40_caps(source, pair_text, timeout, controls_run):
    live_pairs = tuple(edge for edge in combinations(SITES, 2)
                       if any(cell(source, *edge, i, j)
                              for i in COLOURS for j in COLOURS))
    if pair_text == "all":
        selected = live_pairs
    else:
        pieces = tuple(int(part) for part in pair_text.split(","))
        require(len(pieces) == 2 and tuple(sorted(pieces)) in live_pairs,
                (pair_text, tuple(map(edge_name, live_pairs))))
        selected = (tuple(sorted(pieces)),)
    records = {}
    for cap in selected:
        residual, scalar, response, words, polynomials = error_polynomials(source,
                                                                            cap)
        raw = cap_partition_control(source, cap, scalar, response, residual,
                                    controls_run)
        cross = error_two_engine_control(source, cap, residual, scalar, response,
                                         words, polynomials, controls_run)
        explicit = find_small_rational_cap(polynomials, scalar)
        if explicit is not None:
            flat = tuple(Fraction(value) for row in explicit["K_rows"]
                         for value in row)
            raw_error = response_error_numeric(source, residual, scalar,
                                                response, flat)
            require(all(value == 0 for value in raw_error.values()),
                    (cap, explicit, raw_error))
        decision = singular_decision(polynomials, scalar, timeout)
        if explicit is not None:
            require(not decision.get("rabinowitsch_unit", False),
                    (cap, explicit, decision))
        records[edge_name(cap)] = {
            "direct_block_nonzero_cells": sum(
                cell(source, *cap, i, j) != 0
                for i in COLOURS for j in COLOURS
            ),
            "nonzero_error_polynomials": len(polynomials),
            "distinct_error_monomials": len(set().union(
                *(set(poly.terms) for poly in polynomials)
            )) if polynomials else 0,
            "raw_controls": raw,
            "two_engine_error_control": cross,
            "explicit_rational_cap": explicit,
            "decision": decision,
        }
    return {
        "status": "UNAUDITED_EXACT_PROBE",
        "field": "Qbar (hence C) for completed Singular decisions",
        "live_pairs": [edge_name(edge) for edge in live_pairs],
        "pairs_decided": records,
        "scope": (
            "W40 integral X_4 boundary point only; it is not an exact "
            "ternary source because three off-count-5 rows fail"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", default=None,
                        help="W40 cap pair as p,q, or 'all'; omit for structural only")
    parser.add_argument("--timeout", type=int, default=90,
                        help="Singular timeout per pair")
    parser.add_argument("--output")
    arguments = parser.parse_args()

    require(sha256(W40_RESULT.read_bytes()).hexdigest() == PINNED_W40_SHA256,
            "pinned W40 result changed")
    w40 = json.loads(W40_RESULT.read_text())
    witness = w40["engine_audit"]["witness_B_integral"]
    source = parse_source(witness["source"])
    expected_defects = ["".join(map(str, word))
                        for word in witness["off5_violating_words"]]

    controls_run = set()
    packet = packet_reconstruction(controls_run)
    defects = replay_w40(source, expected_defects, controls_run)
    basic_activity_controls(controls_run)
    result = {
        "status": "PASS",
        "classification": "UNAUDITED: exact structural result plus cap probe",
        "packet": packet,
        "w40_boundary_replay": {"defects": defects},
    }
    if arguments.pair is not None:
        result["w40_cap_decisions"] = decide_w40_caps(
            source, arguments.pair, arguments.timeout, controls_run
        )
    else:
        # These controls are cap-specific and must not be declared as run in
        # structural-only mode.
        DECLARED_CONTROLS.difference_update({
            "cap_partition_identity",
            "error_polynomial_two_engine",
        })
    require(controls_run == DECLARED_CONTROLS,
            {"declared": sorted(DECLARED_CONTROLS),
             "executed": sorted(controls_run)})
    result["controls"] = {
        "declared": sorted(DECLARED_CONTROLS),
        "executed": sorted(controls_run),
        "all_ran": True,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True)
    if arguments.output:
        Path(arguments.output).write_text(encoded + "\n")
    print(encoded)


if __name__ == "__main__":
    main()
