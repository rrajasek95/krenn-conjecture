#!/usr/bin/env python3
"""Adversarial builder for the N=8 X4 => active-clean-cap target.

Named target (over C): every endpoint-ordered ternary N=8 source with pure
amplitudes one and all 4,878 mixed off-count <= 4 amplitudes zero has an
active clean cap.

This lane attacks the target on the named W40 integral X4 point and on its
full first-order deformation space.  It also replays the W25-F8 all-blocked
X3 near-falsifier.  Every stored source is evaluated on all 6,561 words by
two independent hafnian engines.  Every live pair is decided over Qbar by a
fresh Rabinowitsch saturation encoding.

The terminal structured result is stronger than a bounded failed search:
the W40 point is a smooth 12-dimensional point of X4, and its entire local
X4 germ is the normalized diagonal-gauge orbit.  Consequently its active
cap cannot be destroyed by any sufficiently local X4 deformation over C.

UNAUDITED.  This file writes only beside itself.
"""

from __future__ import annotations

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
HAZARDS = ROOT / "notes/2026-08-15-conventions-and-hazards.md"
W40_RESULT = (ROOT / "computations/unaudited-x4general-w40-2026-08-20/"
              "results_t3.json")
W25_OBJECT = (ROOT / "computations/unaudited-x3core-w25-2026-08-15/"
              "OBJECT_W25-F8_n8_allblocked_X3.json")
PINS = {
    HAZARDS: "f25e8793587739a3e50fec6dc2c3860e996d94b852d5bce36b4f71c16f069f5d",
    W40_RESULT: "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f",
    W25_OBJECT: "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6",
}

N = 8
SITES = tuple(range(N))
COLOURS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
COORDS = tuple((u, v, a, b) for u, v in EDGES
               for a in COLOURS for b in COLOURS)
K_NAMES = tuple(f"zzk{i}{j}" for i in COLOURS for j in COLOURS)

DECLARED_CONTROLS = {
    "pinned_inputs_and_hazards",
    "matching_counts",
    "w25_two_engine_all_words",
    "w25_all_live_pairs_qbar",
    "w40_positive_through_x4_filter",
    "w40_two_engine_all_words",
    "w40_all_live_pairs_qbar",
    "w40_K_identity_pair67",
    "x4_mutation_must_fire",
    "jacobian_two_views",
    "gauge_kernel_identity",
    "minor_determinants",
}


def require(condition, detail):
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
            yield ((first, second),) + tail


PMS = {m: tuple(perfect_matchings(tuple(range(m)))) for m in (0, 2, 4, 6, 8)}


def cell(source, u, v, a, b):
    if u < v:
        return source[(u, v)][a][b]
    return source[(v, u)][b][a]


def parse_w40():
    record = json.loads(W40_RESULT.read_text())
    raw = record["engine_audit"]["witness_B_integral"]["source"]
    source = {}
    for key, matrix in raw.items():
        u, v = (int(piece.strip()) for piece in key.strip("()").split(","))
        source[(u, v)] = tuple(tuple(Fraction(x) for x in row)
                               for row in matrix)
    require(set(source) == set(EDGES), len(source))
    return source


def parse_w25():
    record = json.loads(W25_OBJECT.read_text())
    source = {}
    for key, matrix in record["blocks"].items():
        u, v = (int(piece) for piece in key.split(","))
        source[(u, v)] = tuple(tuple(Fraction(x) for x in row)
                               for row in matrix)
    require(set(source) == set(EDGES), len(source))
    return source


def haf_pm(source, word, vertices=SITES):
    """Explicit-perfect-matching engine."""
    vertices = tuple(vertices)
    position = {site: i for i, site in enumerate(vertices)}
    total = Fraction(0)
    for matching in PMS[len(vertices)]:
        term = Fraction(1)
        for i, j in matching:
            u, v = vertices[i], vertices[j]
            term *= cell(source, u, v, word[u], word[v])
            if not term:
                break
        total += term
    require(len(position) == len(vertices), vertices)
    return total


def haf_dp(source, word, vertices=SITES):
    """Independent bitmask-peeling engine."""
    vertices = tuple(vertices)
    memo = {0: Fraction(1)}

    def rec(mask):
        if mask in memo:
            return memo[mask]
        lo = (mask & -mask).bit_length() - 1
        rest = mask & ~(1 << lo)
        total = Fraction(0)
        scan = rest
        while scan:
            j = (scan & -scan).bit_length() - 1
            scan &= ~(1 << j)
            u, v = vertices[lo], vertices[j]
            total += cell(source, u, v, word[u], word[v]) * rec(
                rest & ~(1 << j)
            )
        memo[mask] = total
        return total

    return rec((1 << len(vertices)) - 1)


def off_count(word):
    return N - max(word.count(c) for c in COLOURS)


def raw_audit(source):
    defects = []
    engine_hash_rows = []
    for word in product(COLOURS, repeat=N):
        a = haf_pm(source, word)
        b = haf_dp(source, word)
        require(a == b, (word, a, b))
        target = Fraction(1) if len(set(word)) == 1 else Fraction(0)
        engine_hash_rows.append(f"{''.join(map(str, word))}:{a}")
        if a != target:
            defects.append({"word": "".join(map(str, word)),
                            "off": off_count(word), "value": str(a)})
    return {
        "words_checked_each_engine": 3 ** N,
        "engine_agreement": True,
        "amplitude_ledger_sha256": sha256(
            "\n".join(engine_hash_rows).encode()).hexdigest(),
        "pures": [str(haf_dp(source, (c,) * N)) for c in COLOURS],
        "defects_by_off_count": {
            str(k): v for k, v in sorted(Counter(d["off"] for d in defects).items())
        },
        "defect_count": len(defects),
        "first_defects": defects[:12],
    }


class Poly:
    """Sparse Q-polynomial in the nine cap coordinates."""

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
        for left, lc in self.terms.items():
            for right, rc in other.terms.items():
                monomial = tuple(sorted(left + right))
                new = answer.get(monomial, Fraction(0)) + lc * rc
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
        integers = {m: int(c * denominator) for m, c in self.terms.items()}
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


def cap_error_polynomials(source, cap):
    """Build E=s[r^2/2 exp(x)]_U+[r^3/6]_U from raw source blocks."""
    p, q = cap
    residual = tuple(site for site in SITES if site not in cap)
    scalar = Poly()
    for i in COLOURS:
        for j in COLOURS:
            if cell(source, p, q, i, j):
                scalar = scalar + Poly.var(kindex(i, j)).scale(
                    cell(source, p, q, i, j)
                )
    response = {}
    for a, b in combinations(residual, 2):
        matrix = [[Poly() for _ in COLOURS] for _ in COLOURS]
        for alpha in COLOURS:
            for beta in COLOURS:
                entry = Poly()
                for i in COLOURS:
                    for j in COLOURS:
                        coefficient = (
                            cell(source, p, a, i, alpha) *
                            cell(source, q, b, j, beta) +
                            cell(source, p, b, i, beta) *
                            cell(source, q, a, j, alpha)
                        )
                        if coefficient:
                            entry = entry + Poly.var(kindex(i, j)).scale(coefficient)
                matrix[alpha][beta] = entry
        response[(a, b)] = matrix
    polynomials = []
    for colours in product(COLOURS, repeat=6):
        word = dict(zip(residual, colours))
        total = Poly()
        for matching in perfect_matchings(residual):
            rforms = [response[e][word[e[0]]][word[e[1]]] for e in matching]
            xvalues = [cell(source, e[0], e[1], word[e[0]], word[e[1]])
                       for e in matching]
            total = total + rforms[0] * rforms[1] * rforms[2]
            for original in range(3):
                if not xvalues[original]:
                    continue
                term = scalar.scale(xvalues[original])
                for index in range(3):
                    if index != original:
                        term = term * rforms[index]
                total = total + term
        if total:
            polynomials.append(total)
    return scalar, polynomials


def singular_cap_decision(polynomials, scalar, tag, timeout=120):
    names = K_NAMES + ("zzrab",)
    activity = scalar
    for c in COLOURS:
        activity = activity * Poly.var(kindex(c, c))
    rabinowitsch = activity * Poly.var(9) + Poly.const(-1)
    generators = [p.singular(names) for p in polynomials]
    generators.append(rabinowitsch.singular(names))
    script = (
        "ring zzR=0,(" + ",".join(names) + "),dp;\n" +
        "ideal zzI=" + ",\n".join(generators) + ";\n" +
        "ideal zzG=std(zzI);\n" +
        '"ZZUNIT ",(size(zzG)==1 && zzG[1]==1);\n' +
        '"ZZDIM ",dim(zzG);\n'
    )
    require(not any(line.startswith("poly zzk") for line in script.splitlines()),
            "variable-shadowing guard")
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
    finally:
        path.unlink(missing_ok=True)
    require(completed.returncode == 0, (tag, completed.stdout[-2000:]))
    require(not any(line.lstrip().startswith("?")
                    for line in completed.stdout.splitlines()),
            (tag, completed.stdout[-2000:]))
    parsed = {}
    for line in completed.stdout.splitlines():
        fields = line.strip().split()
        if len(fields) >= 2 and fields[0] in {"ZZUNIT", "ZZDIM"}:
            parsed[fields[0]] = fields[1]
    require(set(parsed) == {"ZZUNIT", "ZZDIM"}, (tag, completed.stdout))
    unit = parsed["ZZUNIT"] == "1"
    return {
        "verdict": "BLOCKED" if unit else "ACTIVE_CAP_EXISTS_OVER_QBAR",
        "rabinowitsch_unit": unit,
        "dimension": int(parsed["ZZDIM"]),
        "nonzero_error_polynomials": len(polynomials),
        "generator_sha256": sha256("\n".join(generators).encode()).hexdigest(),
        "seconds": time.monotonic() - started,
    }


def decide_all_live_pairs(source, prefix):
    live = [edge for edge in EDGES if any(cell(source, *edge, i, j)
                                          for i in COLOURS for j in COLOURS)]
    records = {}
    for p, q in live:
        scalar, polynomials = cap_error_polynomials(source, (p, q))
        records[f"{p}{q}"] = singular_cap_decision(
            polynomials, scalar, f"{prefix}_{p}{q}"
        )
    return {"live_pairs": len(live),
            "active_pairs": sum(not row["rabinowitsch_unit"]
                                for row in records.values()),
            "blocked_pairs": sum(row["rabinowitsch_unit"]
                                 for row in records.values()),
            "records": records}


def x4_jacobian(source, cofactor_engine):
    """Raw Jacobian of all X4 coefficient equations at `source`."""
    coordinate_index = {coordinate: i for i, coordinate in enumerate(COORDS)}
    rows, words = [], []
    for word in product(COLOURS, repeat=N):
        if off_count(word) > 4:
            continue
        row = {}
        for u, v in EDGES:
            residual = tuple(site for site in SITES if site not in (u, v))
            coefficient = cofactor_engine(source, word, residual)
            if coefficient:
                row[coordinate_index[(u, v, word[u], word[v])]] = coefficient
        if row:
            rows.append(row)
            words.append("".join(map(str, word)))
    return rows, words


def rank_mod_with_minor(rows, ncols, prime=1000003):
    pivots = {}
    selected_rows = []
    for row_index, original in enumerate(rows):
        row = {column: int(value) % prime for column, value in original.items()
               if int(value) % prime}
        while row:
            column = min(row)
            if column not in pivots:
                inverse = pow(row[column], prime - 2, prime)
                pivots[column] = {c: v * inverse % prime
                                  for c, v in row.items() if v % prime}
                selected_rows.append(row_index)
                break
            factor = row[column]
            for c, value in pivots[column].items():
                new = (row.get(c, 0) - factor * value) % prime
                if new:
                    row[c] = new
                else:
                    row.pop(c, None)
    return len(pivots), selected_rows, sorted(pivots)


def exact_minor_det(rows, selected_rows, selected_columns):
    import sympy
    position = {column: j for j, column in enumerate(selected_columns)}
    entries = {}
    for i, row_index in enumerate(selected_rows):
        for column, value in rows[row_index].items():
            if column in position and value:
                entries[(i, position[column])] = int(value)
    matrix = sympy.MutableSparseMatrix(len(selected_rows),
                                       len(selected_columns), entries)
    return int(matrix.det(method="domain-ge"))


def gauge_derivatives(source):
    """Normalized diagonal-gauge tangent map: eta_7c=-sum_{u<7} eta_uc."""
    rows = []
    for u, v, a, b in COORDS:
        value = cell(source, u, v, a, b)
        row = {}
        if value:
            if u < 7:
                row[3 * u + a] = row.get(3 * u + a, 0) + value
            else:
                for site in range(7):
                    row[3 * site + a] = row.get(3 * site + a, 0) - value
            if v < 7:
                row[3 * v + b] = row.get(3 * v + b, 0) + value
            else:
                for site in range(7):
                    row[3 * site + b] = row.get(3 * site + b, 0) - value
        rows.append(row)
    return rows


def compose_jacobian_gauge(jacobian, gauge):
    nonzero = 0
    for row in jacobian:
        image = {}
        for coordinate, coefficient in row.items():
            for variable, value in gauge[coordinate].items():
                image[variable] = image.get(variable, 0) + coefficient * value
        nonzero += any(value for value in image.values())
    return nonzero


def tangent_audit(source):
    jacobian, words = x4_jacobian(source, haf_dp)
    jacobian_pm, words_pm = x4_jacobian(source, haf_pm)
    require(words_pm == words and jacobian_pm == jacobian,
            "independent Jacobian engines disagree")
    rank13, _, _ = rank_mod_with_minor(jacobian, len(COORDS), 13)
    rank31, _, _ = rank_mod_with_minor(jacobian, len(COORDS), 31)
    rank, selected_rows, selected_columns = rank_mod_with_minor(
        jacobian, len(COORDS)
    )
    determinant = exact_minor_det(jacobian, selected_rows, selected_columns)

    gauge = gauge_derivatives(source)
    gauge_rank, gauge_rows, gauge_columns = rank_mod_with_minor(gauge, 21)
    gauge_determinant = exact_minor_det(gauge, gauge_rows, gauge_columns)
    composed_nonzero = compose_jacobian_gauge(jacobian, gauge)

    zero_columns = [i for i, (u, v, a, b) in enumerate(COORDS)
                    if not cell(source, u, v, a, b)]
    zero_position = {column: i for i, column in enumerate(zero_columns)}
    zero_rows = [{zero_position[c]: value for c, value in row.items()
                  if c in zero_position} for row in jacobian]
    zero_rank, zero_selected_rows, zero_selected_columns = rank_mod_with_minor(
        zero_rows, len(zero_columns)
    )
    zero_determinant = exact_minor_det(
        zero_rows, zero_selected_rows, zero_selected_columns
    )
    one_coordinate_nonzero_rows = [0] * len(zero_columns)
    for row in zero_rows:
        for column, value in row.items():
            if value:
                one_coordinate_nonzero_rows[column] += 1

    require((rank13, rank31, rank) == (240, 240, 240),
            (rank13, rank31, rank))
    require(abs(determinant) == 2 ** 33, determinant)
    require(gauge_rank == 12 and abs(gauge_determinant) == 1,
            (gauge_rank, gauge_determinant))
    require(composed_nonzero == 0, composed_nonzero)
    require(zero_rank == 232 and abs(zero_determinant) == 2 ** 33,
            (zero_rank, zero_determinant))
    require(min(one_coordinate_nonzero_rows) > 0,
            min(one_coordinate_nonzero_rows))

    omitted = [str(COORDS[i]) for i in range(len(COORDS))
               if i not in selected_columns]
    minor_words = [words[i] for i in selected_rows]
    return {
        "x4_rows_total": 4881,
        "nonzero_jacobian_rows": len(jacobian),
        "ambient_coordinates": len(COORDS),
        "jacobian_nonzero_entries": sum(len(row) for row in jacobian),
        "independent_jacobian_engines_agree": True,
        "rank_over_F13": rank13,
        "rank_over_F31": rank31,
        "rank_over_Q": rank,
        "tangent_dimension_over_Q": len(COORDS) - rank,
        "rank_minor_determinant": str(determinant),
        "rank_minor_factorization": "2^33",
        "rank_minor_words_sha256": sha256(
            "\n".join(minor_words).encode()).hexdigest(),
        "rank_minor_omitted_coordinates": omitted,
        "normalized_gauge_parameter_count": 21,
        "gauge_orbit_tangent_rank": gauge_rank,
        "gauge_rank_minor_determinant": str(gauge_determinant),
        "jacobian_times_gauge_nonzero_rows": composed_nonzero,
        "zero_coordinates": len(zero_columns),
        "zero_coordinate_jacobian_rank": zero_rank,
        "zero_coordinate_minor_determinant": str(zero_determinant),
        "one_coordinate_extensions_tested": len(zero_columns),
        "one_coordinate_extensions_surviving": sum(
            count == 0 for count in one_coordinate_nonzero_rows
        ),
        "minimum_detecting_X4_rows_per_zero_coordinate": min(
            one_coordinate_nonzero_rows
        ),
        "field_scope": (
            "rank minor is nonzero in characteristic 0 and every odd "
            "characteristic; characteristic 2 is not decided"
        ),
        "proved_structured_sublemma": (
            "Over characteristic 0, the W40 integral point is smooth of "
            "dimension 12 on X4 and its X4 tangent space equals its "
            "normalized diagonal-gauge orbit tangent. Hence the local X4 "
            "germ is the gauge orbit; no local X4 deformation can destroy "
            "the active-cap property. Holding its 20 nonzero cells fixed, "
            "the other 232 coordinates already have full Jacobian rank."
        ),
    }


def mutate_q26(source):
    mutated = {edge: tuple(tuple(x for x in row) for row in matrix)
               for edge, matrix in source.items()}
    matrix = [list(row) for row in mutated[(2, 6)]]
    require(matrix[2][2] == -1, matrix)
    matrix[2][2] = Fraction(1)
    mutated[(2, 6)] = tuple(tuple(row) for row in matrix)
    failures = []
    for word in product(COLOURS, repeat=N):
        if off_count(word) > 4:
            continue
        target = Fraction(1) if len(set(word)) == 1 else Fraction(0)
        a = haf_pm(mutated, word)
        b = haf_dp(mutated, word)
        require(a == b, (word, a, b))
        if a != target:
            failures.append("".join(map(str, word)))
    require(failures, "q26 sign mutation did not break X4 over Q")
    return failures


def main():
    controls_run = set()
    for path, expected in PINS.items():
        require(sha256(path.read_bytes()).hexdigest() == expected,
                (str(path), "pin changed"))
    require(HAZARDS.read_text().count("\n") + 1 == 313,
            "hazards ledger line count changed")
    controls_run.add("pinned_inputs_and_hazards")

    require({m: len(PMS[m]) for m in PMS} ==
            {0: 1, 2: 1, 4: 3, 6: 15, 8: 105},
            {m: len(PMS[m]) for m in PMS})
    controls_run.add("matching_counts")

    w25 = parse_w25()
    w25_raw = raw_audit(w25)
    require(w25_raw["pures"] == ["1", "1", "1"], w25_raw)
    require(w25_raw["defects_by_off_count"] == {"4": 78, "5": 25},
            w25_raw)
    controls_run.add("w25_two_engine_all_words")
    w25_caps = decide_all_live_pairs(w25, "W25")
    require((w25_caps["live_pairs"], w25_caps["active_pairs"],
             w25_caps["blocked_pairs"]) == (21, 0, 21), w25_caps)
    controls_run.add("w25_all_live_pairs_qbar")

    w40 = parse_w40()
    w40_raw = raw_audit(w40)
    require(w40_raw["pures"] == ["1", "1", "1"], w40_raw)
    require(w40_raw["defects_by_off_count"] == {"5": 3}, w40_raw)
    controls_run.add("w40_positive_through_x4_filter")
    controls_run.add("w40_two_engine_all_words")
    w40_caps = decide_all_live_pairs(w40, "W40")
    require((w40_caps["live_pairs"], w40_caps["active_pairs"],
             w40_caps["blocked_pairs"]) == (17, 7, 10), w40_caps)
    controls_run.add("w40_all_live_pairs_qbar")

    scalar67, polynomials67 = cap_error_polynomials(w40, (6, 7))
    identity = tuple(Fraction(int(i == j))
                     for i in COLOURS for j in COLOURS)
    activity = scalar67.evaluate(identity)
    for c in COLOURS:
        activity *= identity[kindex(c, c)]
    require(activity == 1 and all(p.evaluate(identity) == 0
                                  for p in polynomials67),
            (activity, len(polynomials67)))
    controls_run.add("w40_K_identity_pair67")

    mutation_failures = mutate_q26(w40)
    controls_run.add("x4_mutation_must_fire")

    tangent = tangent_audit(w40)
    controls_run.add("jacobian_two_views")
    controls_run.add("gauge_kernel_identity")
    controls_run.add("minor_determinants")

    require(controls_run == DECLARED_CONTROLS,
            {"declared": sorted(DECLARED_CONTROLS),
             "executed": sorted(controls_run)})
    result = {
        "status": "PASS",
        "classification": "UNAUDITED EXACT ADVERSARIAL BUILDER",
        "target": (
            "Every endpoint-ordered ternary N=8 source with pure amplitudes "
            "1 and all 4,878 mixed off-count<=4 amplitudes zero has some "
            "active clean cap"
        ),
        "terminal": "PROVED_STRUCTURED_LOCAL_SUBLEMMA_NO_FALSIFIER",
        "w25_calibration": {
            "stage_X3": "PASS",
            "stage_X4": "REJECT (78 level-4 defects)",
            "all_blocked_Qbar": True,
            "raw": w25_raw,
            "cap_census": w25_caps,
        },
        "w40_candidate": {
            "stage_X4": "PASS",
            "raw": w40_raw,
            "cap_census": w40_caps,
            "pair67_explicit_cap": {
                "K": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                "activity_product": str(activity),
                "all_error_polynomials_zero": True,
            },
        },
        "named_deformation_stratum": {
            "name": "full first-order X4 deformation germ at W40-B",
            **tangent,
        },
        "negative_control": {
            "mutation": "change q26=-1 to q26=+1",
            "field": "Q (mutation collapses in characteristic 2)",
            "level4_failures": mutation_failures,
        },
        "verdict": (
            "No all-blocked X4 source was constructed. This is not search "
            "evidence for the universal target. The exact terminal is the "
            "local rigidity sublemma: the known W40 X4 component has only "
            "gauge directions at its integral point and therefore cannot "
            "supply a nearby all-blocked falsifier over C. A falsifier must "
            "lie on a different component or at a singular/remote locus."
        ),
        "controls": {
            "declared": sorted(DECLARED_CONTROLS),
            "executed": sorted(controls_run),
            "all_ran": True,
        },
    }
    output = HERE / "results_builder.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "terminal": result["terminal"],
        "w25": [w25_caps["active_pairs"], w25_caps["blocked_pairs"]],
        "w40": [w40_caps["active_pairs"], w40_caps["blocked_pairs"]],
        "tangent_rank": tangent["rank_over_Q"],
        "tangent_dimension": tangent["tangent_dimension_over_Q"],
        "gauge_rank": tangent["gauge_orbit_tangent_rank"],
        "controls": result["controls"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
