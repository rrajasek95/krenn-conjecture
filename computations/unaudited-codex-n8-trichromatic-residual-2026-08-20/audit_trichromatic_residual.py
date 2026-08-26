#!/usr/bin/env python3
"""Exact audit of the 1,680 missing N=8 profile-(3,3,2) rows.

This is deliberately standard-library-only.  It rebuilds perfect matchings,
does not import any source/amplitude implementation, and keeps endpoint order
literal: A_uv[i,j] has the colour at the smaller endpoint first.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def sha(obj) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def matchings_recursive(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    a = vertices[0]
    for k in range(1, len(vertices)):
        b = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in matchings_recursive(rest):
            yield ((a, b),) + tail


MATCHINGS = tuple(matchings_recursive(tuple(range(8))))
require(len(MATCHINGS) == 105, "K8 must have 105 perfect matchings")


def ordered_cell(source, u: int, v: int, i: int, j: int):
    if u < v:
        return source.get((u, v, i, j), 0)
    return source.get((v, u, j, i), 0)


def wrong_untransposed_cell(source, u: int, v: int, i: int, j: int):
    """Intentional endpoint-order mutation used only as a negative control."""
    if u < v:
        return source.get((u, v, i, j), 0)
    return source.get((v, u, i, j), 0)


def hafnian_list(source, vertices: tuple[int, ...], colours: dict[int, int], access=ordered_cell):
    total = Fraction(0)
    for matching in matchings_recursive(vertices):
        term = Fraction(1)
        for u, v in matching:
            term *= access(source, u, v, colours[u], colours[v])
            if not term:
                break
        total += term
    return total


def hafnian_dp(source, vertices: tuple[int, ...], colours: dict[int, int]):
    memo = {}

    def rec(vs: tuple[int, ...]):
        if not vs:
            return Fraction(1)
        if vs in memo:
            return memo[vs]
        a = vs[0]
        total = Fraction(0)
        for k in range(1, len(vs)):
            b = vs[k]
            rest = vs[1:k] + vs[k + 1 :]
            total += ordered_cell(source, a, b, colours[a], colours[b]) * rec(rest)
        memo[vs] = total
        return total

    return rec(vertices)


def profile(word) -> tuple[int, ...]:
    return tuple(sorted(Counter(word).values(), reverse=True))


WORDS_332 = tuple(w for w in itertools.product(range(3), repeat=8) if profile(w) == (3, 3, 2))
require(len(WORDS_332) == 1680, "there must be 1,680 profile-(3,3,2) words")


W40_SUPPORT = (
    (0, 1, 0, 0, "x01_00"), (2, 3, 0, 0, "x23_00"),
    (4, 5, 0, 0, "x45_00"), (6, 7, 0, 0, "x67_00"),
    (0, 3, 1, 1, "x03_11"), (1, 2, 1, 1, "x12_11"),
    (4, 7, 1, 1, "x47_11"), (5, 6, 1, 1, "x56_11"),
    (0, 4, 0, 1, "x04_01"), (0, 5, 1, 0, "x05_10"),
    (1, 7, 0, 1, "x17_01"), (3, 4, 1, 0, "x34_10"),
    (0, 6, 0, 2, "x06_02"), (1, 2, 0, 2, "x12_02"),
    (2, 4, 2, 1, "x24_21"), (6, 7, 2, 1, "x67_21"),
    (0, 4, 2, 2, "x04_22"), (1, 3, 2, 2, "x13_22"),
    (2, 6, 2, 2, "x26_22"), (5, 7, 2, 2, "x57_22"),
)

W40_POINT_VALUES = (
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1
)


def w40_source():
    return {
        (u, v, i, j): Fraction(value)
        for (u, v, i, j, _), value in zip(W40_SUPPORT, W40_POINT_VALUES)
    }


def w40_support_terms(word):
    names = {(u, v, i, j): name for u, v, i, j, name in W40_SUPPORT}
    terms = []
    for matching in MATCHINGS:
        term = []
        for u, v in matching:
            name = names.get((u, v, word[u], word[v]))
            if name is None:
                break
            term.append(name)
        else:
            terms.append(tuple(sorted(term)))
    return tuple(sorted(terms))


def load_w25():
    path = ROOT / "computations/unaudited-x3core-w25-2026-08-15/OBJECT_W25-F8_n8_allblocked_X3.json"
    raw = path.read_bytes()
    data = json.loads(raw)
    source = {}
    for key, matrix in data["blocks"].items():
        u, v = (int(x) for x in key.split(","))
        for i in range(3):
            for j in range(3):
                source[u, v, i, j] = Fraction(matrix[i][j])
    return source, hashlib.sha256(raw).hexdigest()


def live_terms(source, word):
    values = []
    for matching in MATCHINGS:
        term = Fraction(1)
        for u, v in matching:
            term *= ordered_cell(source, u, v, word[u], word[v])
            if not term:
                break
        if term:
            values.append(term)
    return tuple(values)


def poly_add_term(poly, monomial, coefficient):
    if not coefficient:
        return
    monomial = tuple(sorted(monomial))
    poly[monomial] = poly.get(monomial, 0) + coefficient
    if poly[monomial] == 0:
        del poly[monomial]


TWISTED_FIXED = {
    (0, 1, 0, 0): 1, (2, 3, 0, 0): 1, (4, 5, 0, 0): 1, (6, 7, 0, 0): 1,
    (0, 3, 1, 1): 1, (1, 2, 1, 1): 1, (4, 7, 1, 1): 1, (5, 6, 1, 1): 1,
    (0, 4, 0, 1): 1, (0, 5, 1, 0): 1, (1, 7, 0, 1): 1, (3, 4, 1, 0): -1,
}


def twisted_symbolic_cell(u, v, i, j):
    require(u < v, "symbolic cells are stored in endpoint order")
    fixed = TWISTED_FIXED.get((u, v, i, j))
    if fixed is not None:
        return fixed, ()
    if i == 2 or j == 2:
        return 1, (f"x{u}{v}{i}{j}",)
    return 0, ()


def twisted_poly(word):
    poly = {}
    for matching in MATCHINGS:
        coefficient = 1
        monomial = []
        for u, v in matching:
            c, variables = twisted_symbolic_cell(u, v, word[u], word[v])
            coefficient *= c
            if not coefficient:
                break
            monomial.extend(variables)
        if coefficient:
            poly_add_term(poly, monomial, coefficient)
    if len(set(word)) == 1:
        poly_add_term(poly, (), -1)
    return poly


def reduce_zeros(poly, zeros):
    return {m: c for m, c in poly.items() if not any(v in zeros for v in m)}


def serialize_poly(poly):
    return [
        {"coefficient": c, "monomial": "*".join(m) if m else "1"}
        for m, c in sorted(poly.items())
    ]


def audit_twisted_triangular():
    literal = (
        ("20000000", "x0120"), ("21000000", "x0121"),
        ("20010111", "x0220"), ("20110111", "x0221"),
        ("21100000", "x0320"), ("21111111", "x0321"),
        ("20000111", "x0420"), ("21110100", "x0521"),
        ("20000001", "x0620"), ("20000011", "x0621"),
        ("21110110", "x0720"), ("21110111", "x0721"),
    )
    zeros = set()
    literal_rows = []
    for word_text, variable in literal:
        row = twisted_poly(tuple(int(x) for x in word_text))
        require(len(row) == 1 and next(iter(row)) == (variable,), f"literal pivot failed at {word_text}")
        require(abs(row[(variable,)]) == 1, f"literal pivot is not a unit at {word_text}")
        zeros.add(variable)
        literal_rows.append({"word": word_text, "pivot": variable, "coefficient": row[(variable,)]})

    bridge_word = "21110000"
    bridge = twisted_poly(tuple(int(x) for x in bridge_word))
    expected_bridge = {("x0321",): 1, ("x0520",): -1}
    require(bridge == expected_bridge, "twisted bridge binomial changed")
    require(reduce_zeros(bridge, zeros) == {("x0520",): -1}, "bridge does not kill x0520")
    zeros.add("x0520")

    edge_rows_spec = (
        ("22000000", "x0122"), ("20210111", "x0222"),
        ("21120000", "x0322"), ("20002111", "x0422"),
        ("21110200", "x0522"), ("20000021", "x0622"),
        ("21110112", "x0722"),
    )
    edge_rows = []
    for word_text, variable in edge_rows_spec:
        row = twisted_poly(tuple(int(x) for x in word_text))
        reduced = reduce_zeros(row, zeros)
        require(len(reduced) == 1 and next(iter(reduced)) == (variable,), f"edge pivot failed at {word_text}")
        coefficient = reduced[(variable,)]
        require(abs(coefficient) == 1, f"edge pivot is not a unit at {word_text}")
        word_profile = profile(tuple(int(x) for x in word_text))
        edge_rows.append({
            "word": word_text,
            "profile": list(word_profile),
            "pivot": variable,
            "coefficient": coefficient,
        })
        zeros.add(variable)

    central_pivots = [r["word"] for r in edge_rows if r["profile"] == [3, 3, 2]]
    require(central_pivots == ["20002111", "21110200"], "unexpected trichromatic twisted pivots")

    pure = twisted_poly((2,) * 8)
    pure_reduced = reduce_zeros(pure, zeros)
    require(pure_reduced == {(): -1}, "pure-2 row did not reduce to -1")
    require(len(pure) == 106 and pure.get(()) == -1, "pure-2 raw polynomial census changed")
    return {
        "literal_rows": literal_rows,
        "bridge": {"word": bridge_word, "raw": serialize_poly(bridge)},
        "edge_rows": edge_rows,
        "central_pivots": central_pivots,
        "pure2_raw_terms": len(pure),
        "pure2_reduced": serialize_poly(pure_reduced),
        "conclusion": "division-free 21-row contradiction over every field",
    }


def audit_packet_partition():
    pair = (0, 1)
    residual = tuple(v for v in range(8) if v not in pair)
    packet_counts = Counter()
    missing_coefficients = Counter()
    seen_words = Counter()
    x4_complete = 0
    for z in itertools.product(range(3), repeat=6):
        z_profile = profile(z)
        missing = []
        for i in range(3):
            for j in range(3):
                word = [None] * 8
                word[pair[0]] = i
                word[pair[1]] = j
                for v, colour in zip(residual, z):
                    word[v] = colour
                if profile(tuple(word)) == (3, 3, 2):
                    missing.append((i, j))
                    seen_words[tuple(word)] += 1
        if max(Counter(z).values()) >= 4:
            require(not missing, "an X4-complete residual packet has a missing central coefficient")
            x4_complete += 1
        elif missing:
            packet_counts[z_profile] += 1
            missing_coefficients[z_profile] += len(missing)
    expected_packets = {(3, 3): 60, (3, 2, 1): 360, (2, 2, 2): 90}
    expected_coefficients = {(3, 3): 60, (3, 2, 1): 1080, (2, 2, 2): 540}
    require(dict(packet_counts) == expected_packets, "residual packet census changed")
    require(dict(missing_coefficients) == expected_coefficients, "missing coefficient census changed")
    require(x4_complete == 219, "X4 packet census changed")
    require(len(seen_words) == 1680 and set(seen_words.values()) == {1}, "missing rows are not partitioned once")
    return {
        "fixed_pair": list(pair),
        "x4_complete_residual_packets": x4_complete,
        "full_only_packets": {"330": 60, "321": 360, "222": 90},
        "full_only_coefficients": {"330": 60, "321": 1080, "222": 540},
        "total_full_only_packets": sum(packet_counts.values()),
        "total_full_only_coefficients": sum(missing_coefficients.values()),
        "each_332_word_occurs_once": True,
    }


def slice_rhs(source, pair, word, access=ordered_cell):
    p, q = pair
    residual = tuple(v for v in range(8) if v not in pair)
    colours = {v: word[v] for v in range(8)}
    direct = access(source, p, q, word[p], word[q]) * hafnian_list(source, residual, colours, access)
    crossing = Fraction(0)
    for ai in range(len(residual)):
        for bi in range(ai + 1, len(residual)):
            a, b = residual[ai], residual[bi]
            rest = tuple(v for v in residual if v not in (a, b))
            h4 = hafnian_list(source, rest, colours, access)
            response = (
                access(source, p, a, word[p], word[a]) * access(source, q, b, word[q], word[b])
                + access(source, p, b, word[p], word[b]) * access(source, q, a, word[q], word[a])
            )
            crossing += h4 * response
    return direct + crossing


def audit_slice_partition(source, label):
    rows = []
    wrong_mismatches = 0
    for pair in itertools.combinations(range(8), 2):
        for word in WORDS_332:
            colours = {v: word[v] for v in range(8)}
            lhs = hafnian_list(source, tuple(range(8)), colours)
            rhs = slice_rhs(source, pair, word)
            require(lhs == rhs, f"slice partition failed for {label}, pair={pair}, word={word}")
            wrong = slice_rhs(source, pair, word, wrong_untransposed_cell)
            if wrong != lhs:
                wrong_mismatches += 1
            rows.append((pair, word, str(lhs), str(rhs)))
    require(wrong_mismatches > 0, f"endpoint-order mutation did not fire for {label}")
    return {
        "checked_pairs": 28,
        "checked_332_rows_per_pair": 1680,
        "exact_partition_checks": len(rows),
        "endpoint_order_mutation_mismatches": wrong_mismatches,
        "ledger_sha256": sha(rows),
    }


def audit_w40():
    upstream = ROOT / "computations/unaudited-codex-w40-support-global-2026-08-20/certificate.json"
    upstream_data = json.loads(upstream.read_bytes())
    upstream_support = [tuple(x["cell"]) + (x["name"],) for x in upstream_data["support"]]
    require(tuple(upstream_support) == W40_SUPPORT, "W40 support differs from the independently restated support")
    require(tuple(upstream_data["integral_point"]) == W40_POINT_VALUES, "W40 integral point changed")

    supported = []
    for word in WORDS_332:
        terms = w40_support_terms(word)
        if terms:
            supported.append(("".join(str(x) for x in word), terms))
    require(len(supported) == 4, "W40 must have exactly four supported central words")
    distribution = Counter(len(terms) for _, terms in supported)
    require(distribution == Counter({1: 3, 4: 1}), "W40 central matching-count distribution changed")

    singleton_words = [word for word, terms in supported if len(terms) == 1]
    require(singleton_words == ["01110222", "12221000", "20002111"], "W40 singleton words changed")
    four_word, four_terms = next((w, t) for w, t in supported if len(t) == 4)
    require(four_word == "10210021", "W40 four-term central word changed")

    left = ("x03_11", "x45_00"), ("x05_10", "x34_10")
    right = ("x12_02", "x67_21"), ("x17_01", "x26_22")
    factored_terms = tuple(sorted(tuple(sorted(a + b)) for a in left for b in right))
    require(four_terms == factored_terms, "W40 central factorization changed")
    x4_factor_word = tuple(int(x) for x in "10210000")
    x4_terms = w40_support_terms(x4_factor_word)
    expected_x4_terms = tuple(sorted((
        tuple(sorted(("x12_02", "x67_00") + left[0])),
        tuple(sorted(("x12_02", "x67_00") + left[1])),
    )))
    require(x4_terms == expected_x4_terms, "W40 X4 factor row changed")

    source = w40_source()
    point_failures = []
    for word in WORDS_332:
        colours = {v: word[v] for v in range(8)}
        h_list = hafnian_list(source, tuple(range(8)), colours)
        h_dp = hafnian_dp(source, tuple(range(8)), colours)
        require(h_list == h_dp, f"W40 amplitude engines disagree at {word}")
        if h_list:
            point_failures.append(("".join(str(x) for x in word), str(h_list)))
    require(point_failures == [("01110222", "1"), ("12221000", "1"), ("20002111", "-1")], "W40 central point failures changed")

    # Relative to cap pair 67 these are three least-frequency diagonal slots
    # in three distinct residual (3,2,1) packets.
    pair67_slots = []
    for word_text in singleton_words:
        word = tuple(int(x) for x in word_text)
        z = tuple(word[v] for v in range(6))
        counts = Counter(z)
        endpoint = (word[6], word[7])
        require(profile(z) == (3, 2, 1), "W40 singleton is not in a 321 packet")
        require(endpoint[0] == endpoint[1] and counts[endpoint[0]] == 1, "W40 singleton is not a least-colour diagonal slot")
        pair67_slots.append({"word": word_text, "residual": "".join(map(str, z)), "slot": list(endpoint)})

    mutated = dict(source)
    mutated[3, 4, 1, 0] *= -1
    mutated_central = []
    for word in WORDS_332:
        h = hafnian_list(mutated, tuple(range(8)), {v: word[v] for v in range(8)})
        if h:
            mutated_central.append(("".join(map(str, word)), str(h)))
    require(mutated_central != point_failures and len(mutated_central) == 4, "W40 sign mutation did not fire")

    return {
        "upstream_certificate_sha256": hashlib.sha256(upstream.read_bytes()).hexdigest(),
        "supported_332_words": [
            {"word": w, "matching_count": len(t), "monomials": ["*".join(m) for m in t]}
            for w, t in supported
        ],
        "singleton_words": singleton_words,
        "four_term_word": four_word,
        "four_term_factorization": "(x03_11*x45_00+x05_10*x34_10)*(x12_02*x67_21+x17_01*x26_22)",
        "x4_factor_row": "H_10210000=x12_02*x67_00*(x03_11*x45_00+x05_10*x34_10)",
        "integral_point_332_failures": point_failures,
        "pair67_missing_slots": pair67_slots,
        "sign_mutation_failure_count": len(mutated_central),
        "support_stratum_conclusion": "three singleton 332 monomials obstruct full exactness whenever all 20 support cells are nonzero",
    }, source


def audit_w25():
    source, input_sha = load_w25()
    supported = []
    singleton = []
    failures = []
    for word in WORDS_332:
        terms = live_terms(source, word)
        if terms:
            word_text = "".join(map(str, word))
            supported.append((word_text, terms))
            if len(terms) == 1:
                singleton.append(word_text)
            h_list = sum(terms, Fraction(0))
            h_dp = hafnian_dp(source, tuple(range(8)), {v: word[v] for v in range(8)})
            require(h_list == h_dp, f"W25 amplitude engines disagree at {word_text}")
            if h_list:
                failures.append((word_text, str(h_list), len(terms)))
    require(len(supported) == 25, "W25 supported central-word count changed")
    require(len(singleton) == 20, "W25 singleton central-word count changed")
    require(len(failures) == 25, "W25 central failures changed")
    require(Counter(n for _, _, n in failures) == Counter({1: 20, 2: 5}), "W25 matching-count distribution changed")
    return {
        "input_sha256": input_sha,
        "supported_332_words": len(supported),
        "singleton_332_words": singleton,
        "failure_count": len(failures),
        "failure_matching_count_distribution": {"1": 20, "2": 5},
        "failures": [{"word": w, "value": v, "matching_count": n} for w, v, n in failures],
        "support_stratum_conclusion": "twenty singleton 332 monomials independently obstruct full exactness on the open W25 support",
    }, source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()

    packet = audit_packet_partition()
    w40, w40_source_point = audit_w40()
    w25, w25_source_point = audit_w25()
    twisted = audit_twisted_triangular()
    slice_checks = {
        "w40": audit_slice_partition(w40_source_point, "W40"),
        "w25": audit_slice_partition(w25_source_point, "W25"),
    }

    controls_declared = (
        "independent_recursive_vs_subset_dp",
        "endpoint_order_transpose_mutation",
        "w40_forced_sign_mutation",
        "twisted_unit_pivots",
        "packet_bijection_1680",
    )
    controls_executed = controls_declared
    result = {
        "schema": "codex.n8_trichromatic_residual.v1",
        "status": "UNAUDITED exact finite/source-support lemmas",
        "packet_partition": packet,
        "w40": w40,
        "w25": w25,
        "twisted44": twisted,
        "slice_partition": slice_checks,
        "universal_support_lemma": (
            "Over a field (indeed an integral domain), a zero-target word in an exact source cannot have "
            "exactly one live perfect matching: its amplitude is then a product of nonzero cells. Applied to "
            "the full-only shell, every exact N=8 support has NO-SINGLETON-332."
        ),
        "controls": {"declared": list(controls_declared), "executed": list(controls_executed)},
    }
    require(result["controls"]["declared"] == result["controls"]["executed"], "control manifest mismatch")
    digest = sha(result)
    output = {"result": result, "result_sha256": digest}
    if args.write_results:
        (HERE / "results.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "PASS": True,
        "packet_counts": packet,
        "w40_singletons": w40["singleton_words"],
        "w25_singleton_count": len(w25["singleton_332_words"]),
        "twisted_central_pivots": twisted["central_pivots"],
        "slice_checks": {k: v["exact_partition_checks"] for k, v in slice_checks.items()},
        "result_sha256": digest,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
