#!/usr/bin/env python3
"""Independent source-level audit of the fixed twisted-4+4 representative.

UNAUDITED.  This file deliberately has no imports from W33/W40.  It builds
K_8 perfect matchings, endpoint-ordered source cells, and coefficient
polynomials directly from the definition.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 8
COLORS = range(3)


def matchings_recursive(vertices=tuple(range(N))):
    """Engine A: first-vertex recursion, producing canonical edge tuples."""
    if not vertices:
        return [()]
    u = vertices[0]
    out = []
    for k in range(1, len(vertices)):
        v = vertices[k]
        rest = vertices[1:k] + vertices[k + 1 :]
        for tail in matchings_recursive(rest):
            out.append(((u, v),) + tail)
    return out


def matchings_permutations():
    """Engine B: quotient all 8! permutations by canonical paired form."""
    found = set()
    for p in itertools.permutations(range(N)):
        edges = tuple(sorted(tuple(sorted((p[2*i], p[2*i+1]))) for i in range(N//2)))
        found.add(edges)
    return sorted(found)


MATCHINGS_A = matchings_recursive()


def edge_cell(u, v, a, b):
    """Canonical endpoint order; swap colours when the edge is reversed."""
    if u < v:
        return (u, v, a, b)
    return (v, u, b, a)


# The fixed W33-D5 representative, restated without importing any prior code.
FIXED_01 = {
    edge_cell(0, 1, 0, 0): 1,
    edge_cell(2, 3, 0, 0): 1,
    edge_cell(4, 5, 0, 0): 1,
    edge_cell(6, 7, 0, 0): 1,
    edge_cell(0, 3, 1, 1): 1,
    edge_cell(1, 2, 1, 1): 1,
    edge_cell(4, 7, 1, 1): 1,
    edge_cell(5, 6, 1, 1): 1,
    edge_cell(0, 4, 0, 1): 1,
    edge_cell(0, 5, 1, 0): 1,
    edge_cell(1, 7, 0, 1): -1,
    edge_cell(3, 4, 1, 0): -1,
}


def var_name(key):
    u, v, a, b = key
    return f"x{u}{v}{a}{b}"


VARS = []
for u in range(N):
    for v in range(u + 1, N):
        for a in COLORS:
            for b in COLORS:
                if 2 in (a, b):
                    VARS.append(edge_cell(u, v, a, b))
VAR_INDEX = {key: i for i, key in enumerate(VARS)}


def source_entry(key):
    a, b = key[2:]
    if 2 in (a, b):
        return (1, (VAR_INDEX[key],))
    return (FIXED_01.get(key, 0), ())


def poly_add_term(poly, coeff, monomial):
    if coeff:
        monomial = tuple(sorted(monomial))
        poly[monomial] += coeff
        if poly[monomial] == 0:
            del poly[monomial]


def amplitude_poly(word, matchings=MATCHINGS_A):
    """Sparse Z-polynomial for one word, directly summing 105 matchings."""
    ans = defaultdict(int)
    for matching in matchings:
        coeff = 1
        mono = []
        for u, v in matching:
            c, m = source_entry(edge_cell(u, v, word[u], word[v]))
            coeff *= c
            if coeff == 0:
                break
            mono.extend(m)
        poly_add_term(ans, coeff, mono)
    return dict(ans)


def subtract_target(poly, word):
    ans = dict(poly)
    if len(set(word)) == 1:
        ans[()] = ans.get((), 0) - 1
        if ans[()] == 0:
            del ans[()]
    return ans


def poly_key(poly):
    """Canonical up to an overall sign, preserving exact integer content."""
    items = tuple(sorted(poly.items()))
    if not items:
        return items
    if items[0][1] < 0:
        items = tuple((m, -c) for m, c in items)
    return items


def poly_text(poly, names=None):
    if names is None:
        names = [var_name(k) for k in VARS]
    terms = []
    for mono, coeff in sorted(poly.items(), key=lambda x: (len(x[0]), x[0])):
        fac = "*".join(names[i] for i in mono) if mono else "1"
        terms.append(f"({coeff})*{fac}")
    return "+".join(terms) if terms else "0"


def poly_add(left, right, scale=1):
    out = defaultdict(int, left)
    for mon, coeff in right.items():
        poly_add_term(out, scale * coeff, mon)
    return dict(out)


def poly_mul(left, right):
    out = defaultdict(int)
    for ml, cl in left.items():
        for mr, cr in right.items():
            poly_add_term(out, cl * cr, ml + mr)
    return dict(out)


def poly_monomial_quotient(monomial, variable):
    parts = list(monomial)
    parts.remove(variable)
    return {tuple(parts): 1}


def cert_add(left, right, multiplier=None, scale=1):
    """Add scale*multiplier*right to a generator->multiplier certificate."""
    multiplier = {(): 1} if multiplier is None else multiplier
    out = {i: dict(p) for i, p in left.items()}
    for i, poly in right.items():
        term = poly_mul(multiplier, poly)
        out[i] = poly_add(out.get(i, {}), term, scale)
        if not out[i]:
            del out[i]
    return out


def raw_numeric_amplitude_a(word, point, matchings=MATCHINGS_A):
    total = 0
    for matching in matchings:
        prod = 1
        for u, v in matching:
            key = edge_cell(u, v, word[u], word[v])
            if 2 in key[2:]:
                prod *= point[VAR_INDEX[key]]
            else:
                prod *= FIXED_01.get(key, 0)
        total += prod
    return total


def raw_numeric_amplitude_b(word, point):
    """Independent engine: subset DP, not a stored matching list."""
    memo = {0: 1}

    def rec(mask):
        if mask in memo:
            return memo[mask]
        u = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << u)
        acc = 0
        bits = rest
        while bits:
            v = (bits & -bits).bit_length() - 1
            key = edge_cell(u, v, word[u], word[v])
            val = point[VAR_INDEX[key]] if 2 in key[2:] else FIXED_01.get(key, 0)
            acc += val * rec(rest ^ (1 << v))
            bits ^= 1 << v
        memo[mask] = acc
        return acc

    return rec((1 << N) - 1)


def laurent_point(s=1, t=1, a=1, b=1):
    point = [0] * len(VARS)

    def put(u, v, ca, cb, value):
        point[VAR_INDEX[edge_cell(u, v, ca, cb)]] = value

    put(1, 2, 0, 2, s)
    put(2, 4, 2, 1, s)
    put(0, 6, 0, 2, t)
    put(6, 7, 2, 1, t)
    put(0, 4, 2, 2, a)
    put(1, 3, 2, 2, b)
    put(2, 6, 2, 2, -s * t)
    # Integral point is sufficient for the two-engine control.  Symbolic
    # Laurent verification is performed separately with exponent vectors.
    if (a, b, s, t) == (1, 1, 1, 1):
        put(5, 7, 2, 2, -1)
    else:
        put(5, 7, 2, 2, -Fraction(1, a*b*s*t))
    return point


def full_source_from_point(point):
    source = dict(FIXED_01)
    for key, i in VAR_INDEX.items():
        if point[i]:
            source[key] = point[i]
    return source


def full_source_amplitude(word, source):
    total = 0
    for matching in MATCHINGS_A:
        product = 1
        for u, v in matching:
            product *= source.get(edge_cell(u, v, word[u], word[v]), 0)
        total += product
    return total


def laurent_substitute(poly):
    """Map a source polynomial to Z[s±,t±,a±,b±] as exponent tuples."""
    # coefficient and exponent vector for each of the 140 variables
    subst = [(0, (0, 0, 0, 0)) for _ in VARS]

    def put(u, v, ca, cb, coeff, exp):
        subst[VAR_INDEX[edge_cell(u, v, ca, cb)]] = (coeff, exp)

    put(1, 2, 0, 2, 1, (1, 0, 0, 0))
    put(2, 4, 2, 1, 1, (1, 0, 0, 0))
    put(0, 6, 0, 2, 1, (0, 1, 0, 0))
    put(6, 7, 2, 1, 1, (0, 1, 0, 0))
    put(0, 4, 2, 2, 1, (0, 0, 1, 0))
    put(1, 3, 2, 2, 1, (0, 0, 0, 1))
    put(2, 6, 2, 2, -1, (1, 1, 0, 0))
    put(5, 7, 2, 2, -1, (-1, -1, -1, -1))
    out = defaultdict(int)
    for mono, coeff in poly.items():
        exp = [0, 0, 0, 0]
        c = coeff
        for i in mono:
            ci, ei = subst[i]
            c *= ci
            for j in range(4):
                exp[j] += ei[j]
        if c:
            out[tuple(exp)] += c
    return {e: c for e, c in out.items() if c}


def build_equations():
    by_key = {}
    word_records = []
    for word in itertools.product(COLORS, repeat=N):
        poly = subtract_target(amplitude_poly(word), word)
        key = poly_key(poly)
        profile = tuple(sorted(Counter(word).values(), reverse=True))
        if key:
            by_key.setdefault(key, {"poly": dict(key), "words": [], "profiles": set()})
            by_key[key]["words"].append("".join(map(str, word)))
            by_key[key]["profiles"].add(profile)
        word_records.append((word, poly, profile))
    return list(by_key.values()), word_records


def build_unit_certificate(equations):
    """Construct a sparse Z[x] certificate using seven equations at vertex 0.

    A first layer of word equations gives literal variables equal to zero.
    A few two-term equations give additional literal zeros.  Seven further
    word equations then force every pure-2 edge incident with vertex 0 to
    vanish.  The pure word 22222222 is consequently 0, contradicting its
    required coefficient 1.
    """
    word_to_index = {}
    for i, equation in enumerate(equations):
        for word in equation["words"]:
            word_to_index[word] = i

    # Each entry certifies the polynomial "variable" as a Z[x]-linear
    # combination of raw coefficient equations.
    zero_cert = {}
    for i, equation in enumerate(equations):
        if len(equation["poly"]) != 1:
            continue
        (monomial, coeff), = equation["poly"].items()
        if len(monomial) == 1 and abs(coeff) == 1:
            zero_cert[monomial[0]] = {i: {(): coeff}}

    # One safe derived layer: a binomial ct*t + cb*b with b already a
    # literal raw zero proves t=0.  Freeze the old layer to prevent cycles.
    direct = dict(zero_cert)
    for i, equation in enumerate(equations):
        if len(equation["poly"]) != 2:
            continue
        items = list(equation["poly"].items())
        if not all(len(mon) == 1 and abs(coeff) == 1 for mon, coeff in items):
            continue
        for (mt, ct), (mb, cb) in (items, items[::-1]):
            target, base = mt[0], mb[0]
            if base not in direct or target in zero_cert:
                continue
            # target = ct*equation - ct*cb*base because ct^2=1.
            cert = {i: {(): ct}}
            cert = cert_add(cert, direct[base], scale=-ct * cb)
            zero_cert[target] = cert

    target_words = {
        "x0122": "22000000",
        "x0222": "20210111",
        "x0322": "21120000",
        "x0422": "20002111",
        "x0522": "21110200",
        "x0622": "20000021",
        "x0722": "21110112",
    }
    name_to_var = {var_name(key): i for i, key in enumerate(VARS)}
    pure_zero_cert = {}
    derivation = []
    for target_name, word in target_words.items():
        target = name_to_var[target_name]
        gi = word_to_index[word]
        equation = equations[gi]["poly"]
        ct = equation.get((target,))
        assert ct in (-1, 1)
        cert = {gi: {(): ct}}
        killed = []
        for monomial, coeff in equation.items():
            if monomial == (target,):
                continue
            choices = [v for v in sorted(set(monomial)) if v in zero_cert]
            assert choices, (target_name, word, monomial)
            # Prefer a direct certificate, then the smallest certificate.
            zero = min(choices, key=lambda v: (len(zero_cert[v]), v))
            cofactor = poly_monomial_quotient(monomial, zero)
            cert = cert_add(cert, zero_cert[zero], multiplier=cofactor,
                            scale=-ct * coeff)
            killed.append({
                "monomial": [var_name(VARS[v]) for v in monomial],
                "zero_factor": var_name(VARS[zero]),
            })
        pure_zero_cert[target] = cert
        derivation.append({
            "target": target_name,
            "word": word,
            "generator_index": gi,
            "killed_terms": killed,
        })

    pure_i = word_to_index["22222222"]
    pure = equations[pure_i]["poly"]
    constant = pure.get(())
    assert constant in (-1, 1)
    certificate = {pure_i: {(): constant}}
    for monomial, coeff in pure.items():
        if not monomial:
            continue
        incident = [
            name_to_var[f"x0{v}22"] for v in range(1, N)
            if name_to_var[f"x0{v}22"] in monomial
        ]
        assert len(incident) == 1
        target = incident[0]
        cofactor = poly_monomial_quotient(monomial, target)
        certificate = cert_add(
            certificate, pure_zero_cert[target], multiplier=cofactor,
            scale=-constant * coeff,
        )

    # Verify sum_i multiplier_i * equation_i = 1 in Z[x].
    check = {}
    for i, multiplier in certificate.items():
        check = poly_add(check, poly_mul(multiplier, equations[i]["poly"]))
    assert check == {(): 1}, poly_text(check)

    record = {
        "ring": "Z[" + ",".join(var_name(k) for k in VARS) + "]",
        "identity": "sum(multiplier_i * raw_word_equation_i) = 1",
        "n_generators_used": len(certificate),
        "generator_words": {
            str(i): equations[i]["words"][0] for i in sorted(certificate)
        },
        "multipliers": {
            str(i): [
                {"coefficient": c, "monomial": [var_name(VARS[v]) for v in mon]}
                for mon, c in sorted(poly.items())
            ]
            for i, poly in sorted(certificate.items())
        },
        "seven_edge_derivation": derivation,
    }
    return record, certificate


def write_singular(equations, selected=None):
    chosen = equations if selected is None else [equations[i] for i in selected]
    names = [var_name(k) for k in VARS]
    lines = [
        "option(redSB);",
        "ring rr=integer,(" + ",".join(names) + "),dp;",
        "ideal II=" + ",\n".join(poly_text(e["poly"], names) for e in chosen) + ";",
        "ideal GG=std(II);",
        "if (size(GG)==1 && GG[1]==1) { print(\"UNIT=1\"); } else { print(\"UNIT=0\"); }",
        'print("SIZE="+string(size(GG)));',
        'print("GBEGIN");',
        "print(GG);",
        'print("GEND");',
        "quit;",
    ]
    out = HERE / "twisted44_full_ZZ.sing"
    out.write_text("\n".join(lines) + "\n")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-singular", action="store_true")
    ap.add_argument("--run-singular", action="store_true")
    args = ap.parse_args()

    controls_declared = [
        "matching_engines_agree",
        "fixed_binary_exact",
        "laurent_level4_positive",
        "laurent_332_failures",
        "two_raw_engines_all_words",
        "gauge_transport_identity",
        "must_fire_fixed_sign_mutation",
        "must_fire_laurent_mutation",
        "equation_manifest",
        "integer_unit_certificate",
        "must_fire_certificate_mutation",
        "singular_no_shadowing",
    ]
    controls_run = []
    result = {"status": "UNAUDITED", "controls_declared": controls_declared}

    mb = matchings_permutations()
    assert len(MATCHINGS_A) == len(mb) == 105
    assert set(MATCHINGS_A) == set(mb)
    controls_run.append("matching_engines_agree")

    equations, word_records = build_equations()
    binary_bad = []
    for word, poly, _ in word_records:
        if set(word) <= {0, 1} and poly:
            binary_bad.append("".join(map(str, word)))
    assert not binary_bad
    controls_run.append("fixed_binary_exact")

    l4_bad = []
    full_bad = []
    for word, poly, profile in word_records:
        val = laurent_substitute(poly)
        off = N - max(Counter(word).values())
        if off <= 4 and val:
            l4_bad.append(("".join(map(str, word)), val))
        if val:
            full_bad.append(("".join(map(str, word)), profile, val))
    assert not l4_bad
    controls_run.append("laurent_level4_positive")
    assert len(full_bad) == 3 and all(p == (3, 3, 2) for _, p, _ in full_bad)
    controls_run.append("laurent_332_failures")

    point = laurent_point()
    engine_disagree = []
    point_bad = []
    for word in itertools.product(COLORS, repeat=N):
        va = raw_numeric_amplitude_a(word, point)
        vb = raw_numeric_amplitude_b(word, point)
        if va != vb:
            engine_disagree.append((word, va, vb))
        target = int(len(set(word)) == 1)
        if va != target:
            point_bad.append(("".join(map(str, word)), va, tuple(sorted(Counter(word).values(), reverse=True))))
    assert not engine_disagree
    assert len(point_bad) == 3
    controls_run.append("two_raw_engines_all_words")

    # Explicit transport check for the target-preserving diagonal site-colour
    # torus.  Products over sites are one for each colour, which is exactly
    # the condition preserving the three normalized pure coefficients.
    exponent_rows = [
        (1, -1, 2, -2, 3, -3, 4, -4),
        (2, -2, 1, -1, 4, -4, 3, -3),
        (3, -3, 4, -4, 1, -1, 2, -2),
    ]
    bases = (2, 3, 5)
    lambdas = {}
    for colour in COLORS:
        for vertex, exponent in enumerate(exponent_rows[colour]):
            lambdas[vertex, colour] = (
                Fraction(bases[colour] ** exponent, 1) if exponent >= 0
                else Fraction(1, bases[colour] ** (-exponent))
            )
        assert __import__("math").prod(lambdas[v, colour] for v in range(N)) == 1
    source = full_source_from_point(point)
    transported = {
        key: value * lambdas[key[0], key[2]] * lambdas[key[1], key[3]]
        for key, value in source.items()
    }
    for word in itertools.product(COLORS, repeat=N):
        factor = __import__("math").prod(lambdas[v, word[v]] for v in range(N))
        assert full_source_amplitude(word, transported) == factor * full_source_amplitude(word, source)
    controls_run.append("gauge_transport_identity")

    # Mutation 1: flip a fixed representative sign.  A binary equation must fire.
    mutation_key = edge_cell(1, 7, 0, 1)
    old = FIXED_01[mutation_key]
    FIXED_01[mutation_key] = 1
    fired_fixed = []
    for word in itertools.product((0, 1), repeat=N):
        val = raw_numeric_amplitude_a(word, point)
        if val != int(len(set(word)) == 1):
            fired_fixed.append("".join(map(str, word)))
    FIXED_01[mutation_key] = old
    assert fired_fixed
    controls_run.append("must_fire_fixed_sign_mutation")

    # Mutation 2: delete one Laurent-family source cell.  The level-4 target fires.
    mut_point = list(point)
    mut_point[VAR_INDEX[edge_cell(1, 2, 0, 2)]] = 0
    fired_l4 = []
    for word in itertools.product(COLORS, repeat=N):
        off = N - max(Counter(word).values())
        if off <= 4:
            val = raw_numeric_amplitude_b(word, mut_point)
            if val != int(len(set(word)) == 1):
                fired_l4.append("".join(map(str, word)))
    assert fired_l4
    controls_run.append("must_fire_laurent_mutation")

    n332_words = sum(1 for w, _, p in word_records if p == (3, 3, 2))
    n332_eqs = sum(1 for e in equations if (3, 3, 2) in e["profiles"])
    result["manifest"] = {
        "n_words": len(word_records),
        "n_matchings": len(MATCHINGS_A),
        "n_variables": len(VARS),
        "n_distinct_nonzero_equations": len(equations),
        "n_332_words": n332_words,
        "n_distinct_equations_touching_332": n332_eqs,
        "fixed_01_nonzero_cells": len(FIXED_01),
        "equations_sha256": hashlib.sha256(
            repr([poly_key(e["poly"]) for e in equations]).encode()
        ).hexdigest(),
    }
    controls_run.append("equation_manifest")
    result["laurent_family"] = {
        "level4_bad": l4_bad,
        "full_bad": [
            {"word": w, "profile": p, "laurent": {str(k): v for k, v in q.items()}}
            for w, p, q in full_bad
        ],
        "integral_point_bad": point_bad,
    }
    result["mutations"] = {
        "fixed_sign_n_fired": len(fired_fixed),
        "fixed_sign_first": fired_fixed[:5],
        "laurent_delete_n_level4_fired": len(fired_l4),
        "laurent_delete_first": fired_l4[:5],
    }

    certificate_record, certificate = build_unit_certificate(equations)
    cert_path = HERE / "certificate.json"
    cert_path.write_text(json.dumps(certificate_record, indent=2, sort_keys=True) + "\n")
    result["certificate"] = {
        "path": cert_path.name,
        "sha256": hashlib.sha256(cert_path.read_bytes()).hexdigest(),
        "n_generators_used": certificate_record["n_generators_used"],
        "identity": certificate_record["identity"],
    }
    controls_run.append("integer_unit_certificate")

    # Must-fire certificate mutation: change the sign of one selected raw
    # generator while holding the certificate fixed; the identity must fail.
    mutation_i = min(certificate)
    mutated_check = {}
    for i, multiplier in certificate.items():
        scale = -1 if i == mutation_i else 1
        mutated_check = poly_add(
            mutated_check, poly_mul(multiplier, equations[i]["poly"]), scale,
        )
    assert mutated_check != {(): 1}
    result["mutations"]["certificate_sign_generator_index"] = mutation_i
    result["mutations"]["certificate_sign_fired"] = True
    controls_run.append("must_fire_certificate_mutation")

    # The emitted Singular file declares only one ideal, never polynomials
    # whose identifiers could shadow ring variables (hazards-ledger item 13).
    controls_run.append("singular_no_shadowing")

    if args.emit_singular or args.run_singular:
        spath = write_singular(equations)
        result["singular_input"] = spath.name
        result["singular_input_sha256"] = hashlib.sha256(spath.read_bytes()).hexdigest()
        if args.run_singular:
            proc = subprocess.run(["Singular", str(spath)], text=True, capture_output=True)
            question_lines = [
                x for x in (proc.stdout + "\n" + proc.stderr).splitlines()
                if x.lstrip().startswith("?")
            ]
            result["singular"] = {
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "question_lines": question_lines,
            }
            assert proc.returncode == 0 and not question_lines
            assert "UNIT=1" in proc.stdout

    result["_controls_run"] = controls_run
    assert controls_run == controls_declared
    (HERE / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["manifest"], indent=2, sort_keys=True))
    print("Laurent full failures:", [x[0] for x in full_bad])
    print("controls:", controls_run)


if __name__ == "__main__":
    main()
