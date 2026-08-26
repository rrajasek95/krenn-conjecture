#!/usr/bin/env python3
"""Independent, design-only referee for the rep5 guard-minor contraction.

This file deliberately does not import the producer.  It regenerates the
support, matrix orientations, Cramer identities, chart quotient, and the two
canonical Singular inputs from the sealed parents, and compares with the
producer only after those reconstructions have succeeded.  It never invokes
Singular.
"""
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
PRODUCER = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
PARENT = ROOT / "computations/unaudited-codex-n8-x5-seven-block-rep5-diagonal-incidence-gate-2026-08-25"
OBLIGATION = ROOT / "computations/unaudited-codex-n8-x5-seven-block-guard-dual-gate-2026-08-25/results_full_family_obligation.json"

PINS = {
    PRODUCER / "MANIFEST.sha256": "33ae759fb235518412c33d36d621ccce09b8a9e05e9ece05b6d1aaf7f2d8c40c",
    PRODUCER / "results_rep5_contraction_design.json": "b2ba095f4f702ac2138cb40d45b7721a8df9b338900282020e83b791264df59b",
    PARENT / "MANIFEST.sha256": "b73583e0b7a3a9c78003433802571cc7c306807ce311118acbe299c6c9fb7d71",
    PARENT / "generate_rep5.py": "a02d55e4fb9dbc9dfab3044c7900c6fc9b0bd72ca68a78388958b57dd7d177f8",
    PARENT / "gate_metadata.json": "e34d3650a7d60121882c55884b7ded9654089f10bda8a2212ef9c2cc62723712",
    OBLIGATION: "22b471512c6ac6a6ff86bb65fbd4f1fec094208a1c99d338865dfee89c0cb3a0",
}
EXPECTED_PROGRAMS = {
    "y": {"record": (0, 0, 0, 0, "y", 0, 0, 1), "sha256": "33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97", "bytes": 1950700},
    "z": {"record": (0, 0, 0, 0, "z", 0, 0, 1), "sha256": "cf9d4eafc3b25a59f848a3f3be942cd92c1e1758682cd83d3163a9e757ba3ce7", "bytes": 2561588},
}

COLORS = (0, 1, 2)
FIXED = frozenset(((0, 3), (1, 6), (2, 7), (4, 5)))
VARIABLE = frozenset(((0, 4), (1, 2), (3, 5), (6, 7)))
ADDED = frozenset(((0, 6), (1, 5), (1, 7), (2, 4), (2, 6), (3, 6), (3, 7)))
ELIMINATED = (3, 6)
OUTSIDE = (3, 7)
NONFIXED = tuple(sorted(VARIABLE | ADDED))
RETAINED = tuple(edge for edge in NONFIXED if edge != ELIMINATED)
SUPPORT = FIXED | set(NONFIXED)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((first, second),) + tail))


PM8 = tuple(sorted(perfect_matchings(tuple(range(8)))))
SUPPORTED = tuple(matching for matching in PM8 if set(matching) <= SUPPORT)


def independent_parent_digest() -> tuple[str, dict[int, int]]:
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
        census[len(terms)] += 1
        records.append(("".join(map(str, word)), int(len(set(word)) == 1), tuple(terms)))
    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest(), dict(sorted(census.items()))


def star_terms(cap=(0, 3), center=4):
    p, q = cap
    residual = tuple(site for site in range(8) if site not in cap)
    answer = []
    for a, b in itertools.combinations(residual, 2):
        if center in (a, b):
            continue
        pa, qb = tuple(sorted((p, a))), tuple(sorted((q, b)))
        pb, qa = tuple(sorted((p, b))), tuple(sorted((q, a)))
        if pa in SUPPORT and qb in SUPPORT:
            answer.append((a, b, "direct", pa, qb))
        if pb in SUPPORT and qa in SUPPORT:
            answer.append((a, b, "switched", pb, qa))
    return tuple(answer)


def wrapped(value: str) -> str:
    return f"({value})" if "+" in value or "-" in value[1:] or value.startswith("-") else value


def product(*values: str) -> str:
    if "0" in values:
        return "0"
    factors = [wrapped(value) for value in values if value != "1"]
    return "*".join(factors) if factors else "1"


def summation(values) -> str:
    terms = [value for value in values if value != "0"]
    return "+".join(terms).replace("+-", "-") if terms else "0"


def difference(left: str, right: str) -> str:
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
        candidates.append((permutation[coordinate], permutation[p], permutation[q],
                           permutation[r], kind, permutation[s], aa, bb))
    return min(candidates)


def chart_ledger():
    raw = []
    for coordinate, p, q, r, s in itertools.product(COLORS, repeat=5):
        for kind in ("y", "z"):
            for other in COLORS:
                if other != q:
                    a, b = sorted((q, other))
                    raw.append((coordinate, p, q, r, kind, s, a, b))
    groups = collections.defaultdict(list)
    for record in raw:
        groups[orbit_representative(record)].append(record)
    return raw, dict(groups)


def build_context(record):
    coordinate, p, q, r, kind, s, a, b = record
    c = next(value for value in COLORS if value not in (a, b))
    solved = {(0, 6, i, j) for i, j in itertools.product(COLORS, repeat=2)}
    partner = (3, 5) if kind == "y" else (3, 7)
    solved |= {(partner[0], partner[1], i, s) for i in COLORS}
    source = {(edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
              for edge in RETAINED for i, j in itertools.product(COLORS, repeat=2)
              if (edge[0], edge[1], i, j) not in solved}
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
        if kind == "y" and edge == (3, 5) and j == s:
            tail = summation([product(raw((3, 5), i, k), qy(k)) for k in COLORS if k != s]
                             + [product(raw((3, 7), i, k), qz(k)) for k in COLORS])
            return difference("beta" if i == coordinate else "0", tail)
        if kind == "z" and edge == (3, 7) and j == s:
            tail = summation([product(raw((3, 5), i, k), qy(k)) for k in COLORS]
                             + [product(raw((3, 7), i, k), qz(k)) for k in COLORS if k != s])
            return difference("beta" if i == coordinate else "0", tail)
        return raw(edge, i, j)

    def outside(i, j):
        return partner_entry(OUTSIDE, i, j)

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
        if edge in ((3, 5), (3, 7)):
            return partner_entry(edge, i, j)
        return raw(edge, i, j)

    variables = (list(source.values()) + list(xn.values()) + ["abar"] +
                 list(yn.values()) + list(zn.values()) + ["beta"] +
                 [f"t{i}" for i in COLORS] + ["sat"])
    partner_substitutions = [partner_entry(partner, i, s) for i in COLORS]
    return entry, variables, determinant, outside(p, q), source, partner_substitutions


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


def build_program(record, ring="32003"):
    entry, variables, determinant, outside_entry, source, partner_subs = build_context(record)
    equations = []
    for word in itertools.product(COLORS, repeat=8):
        value = amplitude(entry, word)
        equations.append(difference(value, "1") if len(set(word)) == 1 else value)
    p = record[1]
    for i, j in itertools.product(COLORS, repeat=2):
        if j != p:
            equations.append(summation(product(entry((0, 6), i, k), entry((3, 7), j, k)) for k in COLORS))
    for i, j in itertools.product(COLORS, repeat=2):
        correction = summation(product(entry((1, 7), i, k), entry((2, 6), k, ell),
                                         entry((3, 7), j, ell))
                               for k, ell in itertools.product(COLORS, repeat=2))
        equations.append(difference(entry((3, 7), j, i), correction))
    saturation = product("abar", "beta", outside_entry, determinant, "sat") + "-1"
    equations.append(saturation)
    assert len(variables) == len(set(variables)) == 91
    assert len(equations) == len(set(equations)) == 6577
    assert all(value not in ("0", "1", "-1") for value in equations)
    lines = ["option(noredefine);", f"ring r={ring},({','.join(variables)}),dp;",
             "ideal I=" + ",\n".join(equations) + ";",
             'print("INPUT_VARIABLES="+string(nvars(r)));',
             'print("INPUT_GENERATORS="+string(size(I)));', "ideal G=slimgb(I);",
             'print("GROEBNER_SIZE="+string(size(G)));', "poly remainder=reduce(1,G);",
             'print("UNIT_REMAINDER="+string(remainder));',
             'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
             "quit;", ""]
    return "\n".join(lines), {"variables": len(variables), "equations": len(equations),
                               "saturation": saturation, "source_variables": len(source),
                               "partner_substitutions": partner_subs}


def polynomial_replay() -> int:
    def var(name):
        return collections.Counter({(name,): 1})

    def add(*polys):
        result = collections.Counter()
        for poly in polys:
            result.update(poly)
        return collections.Counter({monomial: coefficient for monomial, coefficient in result.items() if coefficient})

    def mul(*polys):
        result = collections.Counter({(): 1})
        for poly in polys:
            nxt = collections.Counter()
            for left, lc in result.items():
                for right, rc in poly.items():
                    nxt[tuple(sorted(left + right))] += lc * rc
            result = collections.Counter({m: c for m, c in nxt.items() if c})
        return result

    def neg(poly):
        return collections.Counter({m: -c for m, c in poly.items()})

    checks = 0
    for a, b in itertools.combinations(COLORS, 2):
        c = next(value for value in COLORS if value not in (a, b))
        w = [var(f"w{j}") for j in COLORS]
        v = [var(f"v{j}") for j in COLORS]
        t, abar = var("t"), var("abar")
        determinant = add(mul(w[a], v[b]), neg(mul(w[b], v[a])))
        for delta in (0, 1):
            reduced = add(abar if delta else collections.Counter(), neg(mul(t, w[c])))
            row = [None, None, None]
            row[a] = add(mul(reduced, v[b]), mul(w[b], t, v[c]))
            row[b] = neg(add(mul(w[a], t, v[c]), mul(reduced, v[a])))
            row[c] = mul(determinant, t)
            assert add(*(mul(row[j], v[j]) for j in COLORS)) == collections.Counter()
            expected = mul(determinant, abar) if delta else collections.Counter()
            assert add(*(mul(row[j], w[j]) for j in COLORS)) == expected
            checks += 2
    return checks


def validate(result):
    assert result["schema"] == "KRENN_X5_REP5_GUARD_MINOR_CONTRACTION_REFEREE_V1"
    assert result["status"] == "PASS_INDEPENDENT_EXACT_DESIGN_NO_IDEAL_RUN"
    assert result["counts"] == {"old_variables": 100, "old_generators": 6586,
                                 "new_variables": 91, "new_generators": 6577,
                                 "full_x5": 6561, "remaining_guard": 15,
                                 "combined_saturation": 1}
    assert result["charts"] == {"raw": 972, "orbits": 162, "orbit_size": 6,
                                 "y_orbits": 81, "z_orbits": 81}
    assert result["scope"] == {"ideal_runs": 0, "rep5_closed": False,
                                "transport_claimed": False, "pilot_launched": False}


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

    metadata = json.loads((PARENT / "gate_metadata.json").read_text())
    obligation = json.loads(OBLIGATION.read_text())["six_full_family_representatives"][5]
    assert len(PM8) == 105 and len(SUPPORTED) == 12 and len(RETAINED) == 10
    expected_edges = lambda values: {tuple(map(int, value)) for value in values}
    assert expected_edges(metadata["support"]["fixed"]) == FIXED
    assert expected_edges(metadata["support"]["variable"]) == VARIABLE
    assert expected_edges(metadata["support"]["added"]) == ADDED
    assert obligation["added"] == ["06", "15", "17", "24", "26", "36", "37"]

    digest, census = independent_parent_digest()
    assert digest == metadata["parent_full_x5_digest"] == obligation["full_x5_6561_equation_sha256"]
    assert {str(k): v for k, v in census.items()} == obligation["full_x5_term_count_census"]

    # Independent orientation derivation.  Transposing the third fixed-identity
    # equation gives A36=-A37*A26^T; substituting it into the second produces
    # (I-A17*A26)*A37^T.  Index expansions below distinguish all transposes.
    fixed_guard = obligation["guard"]["fixed_identity_substitution"]
    assert fixed_guard == ["A06*A37^T=0", "A37^T+A17*A36^T=0", "A26*A37^T+A36^T=0"]
    orientation = {
        "elimination_entry": "A36[i,j]=-sum_k A37[i,k]*A26[j,k]",
        "first_guard_entry": "sum_k A06[i,k]*A37[j,k]=0",
        "second_guard_entry": "A37[j,i]-sum_k,l A17[i,k]*A26[k,l]*A37[j,l]=0",
        "elimination": "A36=-A37*A26^T",
        "guards": ["A06*A37^T=0", "(I-A17*A26)*A37^T=0"],
    }
    assert star_terms() == ((5, 6, "switched", (0, 6), (3, 5)),
                            (6, 7, "direct", (0, 6), (3, 7)))
    carrier = next(item for item in obligation["two_sandwich_stars"]
                   if item["cap"] == "03" and item["star_center"] == 4
                   and item["common_block"] == "06")
    assert carrier["factorization_up_to_output_permutation"] == "A06^T*K*[A35|A37]"
    assert carrier["P"] == "Row(A06^T)" and carrier["Q"] == "ColSpan(A35,A37)"

    assert polynomial_replay() == 12
    raw, groups = chart_ledger()
    assert len(raw) == 972 and len(groups) == 162
    assert set(map(len, groups.values())) == {6}
    assert sum(key[4] == "y" for key in groups) == 81
    assert sum(key[4] == "z" for key in groups) == 81

    regenerated = {}
    z_acyclic = False
    for kind, expected in EXPECTED_PROGRAMS.items():
        record = expected["record"]
        assert orbit_representative(record) == record
        program, facts = build_program(record)
        digest_program = sha256_text(program)
        assert digest_program == expected["sha256"]
        assert len(program.encode()) == expected["bytes"]
        materialized = PRODUCER / f"rep5_guard_minor_tiny_{kind}_p32003.sing"
        assert sha256(materialized) == digest_program
        assert facts["source_variables"] == 78
        assert facts["saturation"].startswith("abar*beta*") and facts["saturation"].endswith("*sat-1")
        if kind == "z":
            # Solved A37 column s cannot appear as a source variable, and each
            # solved expression refers only to A35 plus the other A37 columns.
            _, _, _, _, source, partner_subs = build_context(record)
            forbidden = {f"a37_{i}{record[5]}" for i in COLORS}
            assert forbidden.isdisjoint(source.values())
            assert all(not any(name in expression for name in forbidden) for expression in partner_subs)
            z_acyclic = True
        regenerated[kind] = {"sha256": digest_program, "bytes": len(program.encode()),
                             "variables": facts["variables"], "generators": facts["equations"],
                             "chart": list(record)}
    assert z_acyclic

    counts = {"old_variables": 10 * 9 + 3 + 3 + 3 + 1,
              "old_generators": 6561 + 18 + 6 + 1,
              "new_variables": 78 + 2 + 1 + 5 + 1 + 3 + 1,
              "new_generators": 6561 + 6 + 9 + 1,
              "full_x5": 6561, "remaining_guard": 6 + 9,
              "combined_saturation": 1}
    assert counts == {"old_variables": 100, "old_generators": 6586,
                      "new_variables": 91, "new_generators": 6577,
                      "full_x5": 6561, "remaining_guard": 15,
                      "combined_saturation": 1}

    # Producer comparison is intentionally last.
    producer = json.loads((PRODUCER / "results_rep5_contraction_design.json").read_text())
    assert producer["counts"] == counts
    assert producer["chart_census"] == {"raw": 972, "S3_orbits": 162,
                                          "orbit_size": 6, "y_orbits": 81, "z_orbits": 81}
    assert producer["source_reconstruction"]["full_x5_digest"] == digest
    assert producer["scope"]["ideal_runs"] == 0
    assert {kind: producer["materialized_inputs"][kind]["sha256"] for kind in ("y", "z")} == {
        kind: regenerated[kind]["sha256"] for kind in ("y", "z")}

    result = {
        "schema": "KRENN_X5_REP5_GUARD_MINOR_CONTRACTION_REFEREE_V1",
        "status": "PASS_INDEPENDENT_EXACT_DESIGN_NO_IDEAL_RUN",
        "pins": {str(path.relative_to(ROOT)): value for path, value in PINS.items()},
        "support": {"fixed": ["03", "16", "27", "45"],
                    "variable": ["04", "12", "35", "67"],
                    "added": ["06", "15", "17", "24", "26", "36", "37"],
                    "perfect_matchings_total": len(PM8), "supported": len(SUPPORTED),
                    "supported_matching_sha256": sha256_text(json.dumps(SUPPORTED, separators=(",", ":")))},
        "orientation": orientation,
        "carrier": {"star_terms": [list(value) for value in star_terms()],
                    "factorization": "A06^T*K*[A35|A37]", "P": "Col(A06)",
                    "Q": "ColSpan(A35,A37)",
                    "incidence": ["A06*x=e_i", "A35*y+A37*z=e_i"]},
        "parent_replay": {"full_x5_digest": digest,
                          "term_count_census": {str(k): v for k, v in census.items()}},
        "cramer": {"identities": 12,
                   "A06_v": "0", "A06_w": "d*abar*e_i",
                   "minor": "d=w[a]*v[b]-w[b]*v[a]",
                   "combined_saturation": "abar*beta*A37[p,q]*d*sat-1",
                   "partner_y": "solve column s of A35",
                   "partner_z": "solve column s of A37 before defining v,d,A36,saturation",
                   "z_dependency_acyclic": z_acyclic,
                   "removed": ["six normalized incidence equations",
                               "three A06*A37^T equations for row p"]},
        "counts": counts,
        "charts": {"raw": len(raw), "orbits": len(groups), "orbit_size": 6,
                   "y_orbits": sum(key[4] == "y" for key in groups),
                   "z_orbits": sum(key[4] == "z" for key in groups)},
        "regenerated_programs": regenerated,
        "comparison": {"performed_after_independent_reconstruction": True,
                       "producer_result_match": True},
        "scope": {"ideal_runs": 0, "rep5_closed": False,
                  "transport_claimed": False, "pilot_launched": False},
    }
    validate(result)
    result["hostile_tests"] = {
        "wrong_count": hostile(result, lambda x: x["counts"].__setitem__("new_generators", 6576)),
        "orbit_loss": hostile(result, lambda x: x["charts"].__setitem__("orbits", 161)),
        "ideal_run_injection": hostile(result, lambda x: x["scope"].__setitem__("ideal_runs", 1)),
        "closure_overclaim": hostile(result, lambda x: x["scope"].__setitem__("rep5_closed", True)),
    }
    assert all(result["hostile_tests"].values())
    atomic_json(HERE / "results_independent_referee.json", result)

    pilot = {
        "schema": "KRENN_X5_REP5_GUARD_MINOR_HELD_MODULAR_PILOT_V1",
        "status": "HELD_NOT_LAUNCHED",
        "source": {"path": str((PRODUCER / "rep5_guard_minor_tiny_y_p32003.sing").relative_to(ROOT)),
                   "sha256": EXPECTED_PROGRAMS["y"]["sha256"], "bytes": EXPECTED_PROGRAMS["y"]["bytes"],
                   "chart": list(EXPECTED_PROGRAMS["y"]["record"]), "prime": 32003,
                   "variables": 91, "generators": 6577},
        "lane": {"maximum_lanes": 1, "native_wall_seconds": 180,
                 "wrapper_wall_seconds": 190, "rss_limit_gib": 8,
                 "rss_observer": "Darwin libproc PROC_PIDTASKINFO summed over process group",
                 "poll_seconds": 0.25, "atomic_logs_and_telemetry": True,
                 "fresh_process_census_required": True,
                 "singular_and_gtimeout_hashes_required_at_launch": True,
                 "manager_clearance_required": True},
        "acceptance": {"returncode_zero": True, "input_variables": 91,
                       "input_generators": 6577, "status": "UNIT_IDEAL",
                       "unit_remainder": "0", "resource_breach": None,
                       "claim_if_pass": "modular p=32003 unit-ideal diagnostic for one chart only"},
        "stops": ["any terminal outcome", "timeout", "RSS breach", "nonunit", "parse mismatch"],
        "forbidden": ["automatic relaunch", "second chart", "Q lane", "rep5 closure claim", "transport claim"],
        "scope": {"launched": False, "ideal_runs": 0},
    }
    atomic_json(HERE / "HELD_MODULAR_PILOT.json", pilot)
    print(json.dumps({"status": result["status"], "counts": counts,
                      "charts": result["charts"], "ideal_runs": 0,
                      "pilot": pilot["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
