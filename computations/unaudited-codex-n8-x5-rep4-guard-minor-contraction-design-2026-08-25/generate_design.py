#!/usr/bin/env python3
"""Independent rep4 guard-minor/Cramer contraction; generate only, never solve."""
from __future__ import annotations

import collections
import copy
import hashlib
import itertools
import json
import os
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PARENT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-reps1-4-5-low-rank-carrier-2026-08-25"
OBLIGATION_DIR = ROOT / "computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25"
OBLIGATION = OBLIGATION_DIR / "results_full_family_obligation.json"
PINS = {
    PARENT / "MANIFEST.sha256": "9a3cec1a39422d2c3d7a6b40f6acdec0b04b19b893c0a1fb657c69d3b50bb8fe",
    PARENT / "results_remaining_reps_low_rank_carrier.json": "359aa45545d85378dd9e945eb82be3adb98922648025fe853f930feac2b5f458",
    OBLIGATION_DIR / "MANIFEST.sha256": "21f351085e1650dcf64889103813c869853f47b74a432596a9147d3324536acf",
    OBLIGATION: "22b471512c6ac6a6ff86bb65fbd4f1fec094208a1c99d338865dfee89c0cb3a0",
}
COLORS = tuple(range(3))
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
ADDED = frozenset(((0, 6), (1, 5), (1, 7), (2, 3), (2, 6), (4, 6), (4, 7)))
ELIMINATED = (4, 6)
OUTSIDE = (4, 7)
NONFIXED = tuple(sorted(VARIABLE | ADDED))
RETAINED = tuple(edge for edge in NONFIXED if edge != ELIMINATED)
SUPPORT = FIXED | set(NONFIXED)
TINY_Y = (0, 0, 0, 0, "y", 0, 0, 1)
TINY_Z = (0, 0, 0, 0, "z", 0, 0, 1)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


PM8 = tuple(sorted(matchings(tuple(range(8)))))
SUPPORTED = tuple(value for value in PM8 if set(value) <= SUPPORT)
assert len(PM8) == 105 and len(SUPPORTED) == 12 and len(RETAINED) == 10


def wrapped(value):
    return f"({value})" if "+" in value or ("-" in value[1:]) or value.startswith("-") else value


def product(*values):
    if any(value == "0" for value in values):
        return "0"
    kept = [wrapped(value) for value in values if value != "1"]
    return "*".join(kept) if kept else "1"


def summation(values):
    kept = [value for value in values if value != "0"]
    return "+".join(kept).replace("+-", "-") if kept else "0"


def difference(left, right):
    if right == "0":
        return left
    if left == "0":
        return f"-({right})"
    return f"{left}-({right})"


def orbit_representative(record):
    coordinate, p, q, r, kind, s, a, b = record
    candidates = []
    for permutation in itertools.permutations(COLORS):
        aa, bb = sorted((permutation[a], permutation[b]))
        candidates.append((permutation[coordinate], permutation[p], permutation[q], permutation[r], kind, permutation[s], aa, bb))
    return min(candidates)


def orbit_ledger():
    raw = []
    for coordinate, p, q, r, s in itertools.product(COLORS, repeat=5):
        for kind in ("y", "z"):
            for other in COLORS:
                if other != q:
                    a, b = sorted((q, other))
                    raw.append((coordinate, p, q, r, kind, s, a, b))
    groups = {}
    for value in raw:
        groups.setdefault(orbit_representative(value), []).append(value)
    assert len(raw) == 972 and len(groups) == 162 and set(map(len, groups.values())) == {6}
    return raw, groups


def build_context(record):
    coordinate, p, q, r, kind, s, a, b = record
    c = next(value for value in COLORS if value not in (a, b))
    solved = {(0, 6, i, j) for i, j in itertools.product(COLORS, repeat=2)}
    if kind == "y":
        # A23^T*y: y_s pivots row s of A23.
        solved |= {(2, 3, s, j) for j in COLORS}
    else:
        # A35*z: z_s pivots column s of A35.
        solved |= {(3, 5, i, s) for i in COLORS}
    source = {
        (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
        for edge in RETAINED
        for i, j in itertools.product(COLORS, repeat=2)
        if (edge[0], edge[1], i, j) not in solved
    }
    assert len(source) == 78
    xn = {j: f"xn{j}" for j in COLORS if j != r}
    yn = {j: f"yn{j}" for j in COLORS if not (kind == "y" and j == s)}
    zn = {j: f"zn{j}" for j in COLORS if not (kind == "z" and j == s)}

    def raw(edge, i, j):
        return source[edge, i, j]

    def w(j):
        return "1" if j == r else xn[j]

    def qy(j):
        return "1" if kind == "y" and j == s else yn[j]

    def qz(j):
        return "1" if kind == "z" and j == s else zn[j]

    def partner_entry(edge, i, j):
        if kind == "y" and edge == (2, 3) and i == s:
            # Output coordinate is j in A23^T*y.
            tail = summation(
                [product(raw((2, 3), k, j), qy(k)) for k in COLORS if k != s]
                + [product(raw((3, 5), j, k), qz(k)) for k in COLORS]
            )
            return difference("beta" if j == coordinate else "0", tail)
        if kind == "z" and edge == (3, 5) and j == s:
            # Output coordinate is i in A35*z.
            tail = summation(
                [product(raw((2, 3), k, i), qy(k)) for k in COLORS]
                + [product(raw((3, 5), i, k), qz(k)) for k in COLORS if k != s]
            )
            return difference("beta" if i == coordinate else "0", tail)
        return raw(edge, i, j)

    def outside(i, j):
        return raw(OUTSIDE, i, j)

    def v(j):
        return outside(p, j)

    determinant = difference(product(w(a), v(b)), product(w(b), v(a)))

    def entry(edge, i, j):
        if edge in FIXED:
            return "1" if i == j else "0"
        if edge == ELIMINATED:
            return f"-({summation(product(outside(i, k), raw((2, 6), j, k)) for k in COLORS)})"
        if edge == (0, 6):
            reduced = difference("abar" if i == coordinate else "0", product(f"t{i}", w(c)))
            if j == a:
                return summation((product(reduced, v(b)), product(w(b), f"t{i}", v(c))))
            if j == b:
                return f"-({summation((product(w(a), f't{i}', v(c)), product(reduced, v(a))))})"
            assert j == c
            return product(determinant, f"t{i}")
        if edge in ((2, 3), (3, 5)):
            return partner_entry(edge, i, j)
        return raw(edge, i, j)

    variables = list(source.values()) + list(xn.values()) + ["abar"] + list(yn.values()) + list(zn.values()) + ["beta"] + [f"t{i}" for i in COLORS] + ["sat"]
    assert len(variables) == len(set(variables)) == 91
    return entry, variables, determinant, outside(p, q)


def amplitude(entry, word):
    terms = []
    for matching in SUPPORTED:
        factors = []
        for edge in matching:
            value = entry(edge, word[edge[0]], word[edge[1]])
            if value == "0":
                break
            factors.append(value)
        else:
            terms.append(product(*factors))
    return summation(terms)


def build_program(record):
    entry, variables, determinant, outside_entry = build_context(record)
    equations = []
    for word in itertools.product(COLORS, repeat=8):
        value = amplitude(entry, word)
        equations.append(difference(value, "1") if len(set(word)) == 1 else value)
    p = record[1]
    # A06*A47^T=0: the row-p outside equation is a Cramer identity.
    for i, j in itertools.product(COLORS, repeat=2):
        if j != p:
            equations.append(summation(product(entry((0, 6), i, k), entry((4, 7), j, k)) for k in COLORS))
    # (I-A17*A26)*A47^T=0 remains source-faithful and orientation-sensitive.
    for i, j in itertools.product(COLORS, repeat=2):
        correction = summation(
            product(entry((1, 7), i, k), entry((2, 6), k, ell), entry((4, 7), j, ell))
            for k, ell in itertools.product(COLORS, repeat=2)
        )
        equations.append(difference(entry((4, 7), j, i), correction))
    equations.append(product("abar", "beta", outside_entry, determinant, "sat") + "-1")
    assert len(equations) == 6577 and len(variables) == 91
    assert len(set(equations)) == 6577 and all(value not in ("0", "1", "-1") for value in equations)
    program = "\n".join([
        "// DESIGN INPUT ONLY: zero ideal runs authorized.",
        "option(noredefine);",
        f"ring r=0,({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));',
        'print("INPUT_GENERATORS="+string(size(I)));',
        "quit;",
        "",
    ])
    return program


def parent_digest_and_census():
    records = []
    census = collections.Counter()
    for word in itertools.product(COLORS, repeat=8):
        terms = []
        for matching in SUPPORTED:
            factors = []
            for edge in matching:
                i, j = word[edge[0]], word[edge[1]]
                if edge in FIXED:
                    if i != j:
                        break
                else:
                    factors.append(f"A{edge[0]}{edge[1]}[{i}{j}]")
            else:
                terms.append("*".join(factors) or "1")
        target = 1 if len(set(word)) == 1 else 0
        census[len(terms)] += 1
        records.append(("".join(map(str, word)), target, tuple(terms)))
    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest(), dict(sorted(census.items()))


def cramer_symbolic_replay():
    def var(name):
        return collections.Counter({(name,): 1})

    def add(*polys):
        answer = collections.Counter()
        for polynomial in polys:
            answer.update(polynomial)
        return collections.Counter({monomial: coefficient for monomial, coefficient in answer.items() if coefficient})

    def mul(*polys):
        answer = collections.Counter({(): 1})
        for polynomial in polys:
            following = collections.Counter()
            for left, coefficient in answer.items():
                for right, other in polynomial.items():
                    following[tuple(sorted(left + right))] += coefficient * other
            answer = collections.Counter({monomial: coefficient for monomial, coefficient in following.items() if coefficient})
        return answer

    def neg(poly):
        return collections.Counter({monomial: -coefficient for monomial, coefficient in poly.items()})

    checks = 0
    for a, b in itertools.combinations(COLORS, 2):
        c = next(value for value in COLORS if value not in (a, b))
        w = [var(f"w{j}") for j in COLORS]
        v = [var(f"v{j}") for j in COLORS]
        t = var("t")
        abar = var("abar")
        determinant = add(mul(w[a], v[b]), neg(mul(w[b], v[a])))
        for delta in (0, 1):
            reduced = add(abar if delta else collections.Counter(), neg(mul(t, w[c])))
            row = [None] * 3
            row[a] = add(mul(reduced, v[b]), mul(w[b], t, v[c]))
            row[b] = neg(add(mul(w[a], t, v[c]), mul(reduced, v[a])))
            row[c] = mul(determinant, t)
            guard = add(*(mul(row[j], v[j]) for j in COLORS))
            incidence = add(*(mul(row[j], w[j]) for j in COLORS))
            assert guard == collections.Counter()
            assert incidence == (mul(determinant, abar) if delta else collections.Counter())
            checks += 2
    return checks


def validate(result):
    assert result["schema"] == "KRENN_X5_REP4_GUARD_MINOR_CONTRACTION_DESIGN_V1"
    assert result["status"] == "PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN"
    assert result["counts"] == {"old_variables": 100, "old_generators": 6586, "new_variables": 91, "new_generators": 6577, "full_x5": 6561, "remaining_guard": 15, "combined_saturation": 1}
    assert result["chart_census"] == {"raw": 972, "S3_orbits": 162, "orbit_size": 6, "y_orbits": 81, "z_orbits": 81}
    assert result["scope"] == {"materialized_design_inputs": 2, "ideal_runs": 0, "rep4_closed": False, "transport_claimed": False}


def hostile(result, mutation):
    candidate = copy.deepcopy(result)
    mutation(candidate)
    try:
        validate(candidate)
    except (AssertionError, KeyError, TypeError):
        return True
    return False


def main():
    for path, expected in PINS.items():
        assert sha256(path) == expected, (path, sha256(path), expected)
    obligation = json.loads(OBLIGATION.read_text())["six_full_family_representatives"][4]
    assert obligation["added"] == ["06", "15", "17", "23", "26", "46", "47"]
    assert obligation["guard"]["derived"] == ["A46^T=-A26*A47^T", "(I-A17*A26)*A47^T=0", "A06*A47^T=0"]
    parent = json.loads((PARENT / "results_remaining_reps_low_rank_carrier.json").read_text())
    record = next(item for item in parent["representatives"] if item["representative_id"] == 4)
    assert record["support"]["added_nonzero"] == ["06", "15", "17", "23", "26", "46", "47"]
    assert record["carrier"]["factorization_up_to_output_permutation"] == "A06^T*K*[A23^T|A35]"

    digest, census = parent_digest_and_census()
    assert digest == obligation["full_x5_6561_equation_sha256"] == "db51326bf12bfb970b95eb6dd6e490d3e983c18f303f44eeb8b5d0586c0f0d5a"
    assert {str(key): value for key, value in census.items()} == obligation["full_x5_term_count_census"]
    raw, groups = orbit_ledger()
    assert cramer_symbolic_replay() == 12

    inputs = {}
    for kind, chart in (("y", TINY_Y), ("z", TINY_Z)):
        assert orbit_representative(chart) == chart
        program = build_program(chart)
        path = HERE / f"rep4_guard_minor_tiny_{kind}_Q.sing"
        temporary = path.with_suffix(".sing.tmp")
        temporary.write_text(program)
        os.replace(temporary, path)
        inputs[kind] = {"chart": list(chart), "path": path.name, "sha256": hashlib.sha256(program.encode()).hexdigest(), "bytes": len(program.encode())}

    orbit_records = []
    for representative, members in sorted(groups.items()):
        orbit_records.append({"representative": list(representative), "size": len(members), "members": [list(value) for value in sorted(members)]})
    orbit_path = HERE / "chart_orbit_ledger.json"
    temporary = orbit_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps({"raw": len(raw), "groups": orbit_records}, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, orbit_path)

    result = {
        "schema": "KRENN_X5_REP4_GUARD_MINOR_CONTRACTION_DESIGN_V1",
        "status": "PASS_STRICT_SMALLER_EXACT_DESIGN_NO_IDEAL_RUN",
        "source_reconstruction": {
            "fixed": ["03", "16", "27", "45"], "variable": ["04", "12", "35", "67"],
            "added": ["06", "15", "17", "23", "26", "46", "47"],
            "supported_matchings": ["|".join(f"{a}{b}" for a, b in value) for value in SUPPORTED],
            "elimination": "A46=-A47*A26^T", "guard": ["A06*A47^T=0", "(I-A17*A26)*A47^T=0"],
            "carrier": "A06^T*K*[A23^T|A35]", "incidence": ["A06*x=e_i", "A23^T*y+A35*z=e_i"],
            "full_x5_digest": digest, "term_census": census,
        },
        "orientation_audit": {
            "y_pivot": "y_s=1 solves row s of A23 because (A23^T*y)_i=sum_j A23[j,i]y_j",
            "z_pivot": "z_s=1 solves column s of A35 because (A35*z)_i=sum_j A35[i,j]z_j",
            "outside_row": "v=row_p(A47); A06*v=0 is the row-p equation of A06*A47^T=0",
            "reduced_guard_entry": "A47[j,i]-sum_k,l A17[i,k]A26[k,l]A47[j,l]=0",
        },
        "chart_cover": {
            "outside": "choose A47[p,q]!=0 and v=row_p(A47)",
            "x": "choose x_r!=0; normalize w=x/x_r and write A06*w=abar*e_i",
            "independence": "A06*v=0 and abar!=0 make w,v independent; v_q!=0 yields a nonzero w/v minor d involving q",
            "partner": "choose a nonzero y_s or z_s; normalize and write A23^T*y+A35*z=beta*e_i",
            "saturation": "abar*beta*A47[p,q]*d*sat-1",
            "forward_cover": "every nonzero-outside inactive-diagonal witness selects at least one chart by the four nonzero choices above",
            "reverse": "the saturation makes every Cramer division legal; reconstructed A06 and partner entries satisfy the original guard and both incidences exactly",
        },
        "substitution": {
            "A06": "all nine entries solved by the w/v Cramer formulas, with A06*w=d*abar*e_i and A06*v=0",
            "partner_y": "solve row s of A23", "partner_z": "solve column s of A35",
            "A46": "reconstruct as -A47*A26^T after all substitutions",
            "tautologies_removed": ["six incidence equations", "three row-p A06*A47^T equations"],
        },
        "symbolic_replay": {"generic_cramer_polynomial_identities": 12, "parent_semantic_digest_replayed": True},
        "counts": {"old_variables": 100, "old_generators": 6586, "new_variables": 91, "new_generators": 6577, "full_x5": 6561, "remaining_guard": 15, "combined_saturation": 1},
        "chart_census": {"raw": len(raw), "S3_orbits": len(groups), "orbit_size": 6, "y_orbits": sum(key[4] == "y" for key in groups), "z_orbits": sum(key[4] == "z" for key in groups)},
        "orbit_ledger": {"path": orbit_path.name, "sha256": sha256(orbit_path)},
        "materialized_inputs": inputs,
        "pins": {str(path.relative_to(ROOT)): value for path, value in PINS.items()},
        "scope": {"materialized_design_inputs": 2, "ideal_runs": 0, "rep4_closed": False, "transport_claimed": False},
    }
    validate(result)
    tests = {
        "count_mutation": hostile(result, lambda value: value["counts"].__setitem__("new_variables", 90)),
        "orbit_collapse": hostile(result, lambda value: value["chart_census"].__setitem__("S3_orbits", 161)),
        "launch_injection": hostile(result, lambda value: value["scope"].__setitem__("ideal_runs", 1)),
        "transport_overclaim": hostile(result, lambda value: value["scope"].__setitem__("transport_claimed", True)),
    }
    assert all(tests.values())
    result["hostile_tests"] = tests
    output = HERE / "results_rep4_contraction_design.json"
    temporary = output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, output)
    print(json.dumps({"status": result["status"], "variables": 91, "generators": 6577, "orbits": 162, "runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
