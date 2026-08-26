#!/usr/bin/env python3
"""Superseding literal-safe rep5 rank-stratified quotient; design only."""
from __future__ import annotations

import collections
import hashlib
import importlib.util
import itertools
import json
import os
import re
from pathlib import Path

if not __debug__:
    raise RuntimeError("fail closed: assertions required")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
PIVOT = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-2026-08-25"
PIVOT_REF = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-referee-2026-08-25"
K0_TERM = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-pivot-k0-modular-terminal-referee-2026-08-25"
OLD = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-2026-08-25"
REJECTION = ROOT / "computations/unaudited-codex-n8-x5-rep5-rank-stratified-guard-pivot-design-referee-2026-08-25"

PINS = {
    BASE / "MANIFEST.sha256": "33ae759fb235518412c33d36d621ccce09b8a9e05e9ece05b6d1aaf7f2d8c40c",
    BASE / "generate_design.py": "3844eadf4a9e21c2feb012cbd684c22ca7611f4d22f87659e19952d0381614f4",
    PIVOT / "MANIFEST.sha256": "00ac8c2a1bea2b958644b0e6b1851d26535c83cc715d92b28335157b219da3f9",
    PIVOT / "rep5_p00_guardpivot_k0_Q.sing": "d4204428cab5f3b5dd4ac321dd1ae04ce9b79c8f1197b8e1e863c6c186cc74f1",
    PIVOT / "rep5_p00_guardpivot_k1_Q.sing": "cdf782ee92b0a019c2a77d6ccc980828c7d0279ebcc3592cced648306fd95e6c",
    PIVOT / "rep5_p00_guardpivot_k2_Q.sing": "ef6fec2e4ba4baf44c07e9d90e0a1b7fb2624d99c838d901d388e3041bf6aa6d",
    PIVOT_REF / "FINAL_MANIFEST.sha256": "af4bee0ca8db5391aac9f59cb1e52051d32e66fdb2974a126468b054ca3f5a4b",
    K0_TERM / "FINAL_MANIFEST.sha256": "a5dcd93bc79154bce1af90557c8496ca5aa38052f9e6b6206266e498c198e9cf",
    K0_TERM / "results_referee.json": "37358baa478e6d220a19cdf955effab940c8b560bc93242e1ed52511c5db31c8",
    OLD / "MANIFEST.sha256": "f28dbb2bd003e8ebcfae4eba7945b29507c2a39c417700c17653131cd6674221",
    OLD / "results_design.json": "d2f7bc1d82781d887e5b1cfe8fb31ee32bbd294c64c6b35f40a838d3b6b2b68c",
    REJECTION / "FINAL_MANIFEST.sha256": "8a1c4e5faf9e73cffcfb5a8b52c697aa79fbb15e45aa9cae6d27911dd62ffea7",
    REJECTION / "results_referee.json": "bd13a637305966d993ef4373c3a0f300afae6ee7c269fe097b83552a76a60bd9",
}

VALID_COMPLEMENTS = {
    0: "3dfc97bdcddfe15870e56744101af011e943a0609f98848bfee60c78cac76e79",
    1: "96943ee3f63c84322b65fdf3f44dc46340186807675d2d44a429fe764d9e9115",
    2: "12f08480dc093f3ecb38b6d250f8b8064b64dab2aed9e1e0dea136e287ca7a41",
}
RECORD = (0, 0, 0, 0, "y", 0, 0, 1)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def atomic(path: Path, text: str) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text)
    os.replace(temporary, path)


def load_base():
    spec = importlib.util.spec_from_file_location("sealed_rep5_base_v2", BASE / "generate_design.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_program(text: str) -> tuple[list[str], list[str]]:
    ring = next(line for line in text.splitlines() if line.startswith("ring r="))
    variables = ring.split(",(", 1)[1].rsplit("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    equations: list[str] = []
    depth = 0
    start = 0
    for position, character in enumerate(body):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            assert depth >= 0
        elif character == "," and depth == 0:
            equations.append(body[start:position].strip())
            start = position + 1
    equations.append(body[start:].strip())
    assert depth == 0
    return variables, equations


def program(variables: list[str], equations: list[str]) -> str:
    return "\n".join([
        "// DESIGN INPUT ONLY: zero Singular or ideal runs authorized.",
        "option(noredefine);",
        f"ring r=0,({','.join(variables)}),dp;",
        "ideal I=" + ",\n".join(equations) + ";",
        'print("INPUT_VARIABLES="+string(nvars(r)));',
        'print("INPUT_GENERATORS="+string(size(I)));',
        "ideal G=slimgb(I);",
        'print("GROEBNER_SIZE="+string(size(G)));',
        "poly remainder=reduce(1,G);",
        'print("UNIT_REMAINDER="+string(remainder));',
        'if (remainder==0) { print("STATUS=UNIT_IDEAL"); } else { print("STATUS=NONUNIT_OR_UNRESOLVED"); }',
        "quit;",
        "",
    ])


def literal_census(text: str, variables: list[str], equations: list[str], removed: set[str]) -> dict:
    declared = set(variables)
    tokens = set(re.findall(r"\b(?:a\d\d_\d\d|xn\d|yn\d|zn\d|abar|beta|t\d|sat)\b", "\n".join(equations)))
    undeclared = sorted(tokens - declared)
    removed_counts = {name: len(re.findall(rf"\b{re.escape(name)}\b", text)) for name in sorted(removed)}
    assert not undeclared, undeclared
    assert not any(removed_counts.values()), removed_counts
    assert set(equations) and len(equations) == len(set(equations))
    assert all(value not in ("0", "1", "-1") for value in equations)
    return {
        "declared_variables": len(variables),
        "identifier_tokens_used": len(tokens),
        "undeclared_identifiers": undeclared,
        "removed_symbol_occurrences": removed_counts,
        "all_removed_symbols_absent": True,
    }


def build_open(m, pivot_k: int, m_index: int):
    """Build one open source from raw entries in strict dependency order."""
    assert pivot_k in m.COLORS and m_index in (1, 2)
    coordinate, p, q, r, kind, s, a, b = RECORD
    c = next(value for value in m.COLORS if value not in (a, b))
    assert (coordinate, p, q, r, kind, s, a, b, c) == (0, 0, 0, 0, "y", 0, 0, 1, 2)

    solved = {(0, 6, i, j) for i, j in itertools.product(m.COLORS, repeat=2)}
    solved |= {(3, 5, i, s) for i in m.COLORS}
    solved |= {(1, 7, i, pivot_k) for i in m.COLORS}
    solved |= {(3, 7, i, j) for i in m.COLORS if i != p for j in m.COLORS if j != q}
    source = {
        (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
        for edge in m.RETAINED
        for i, j in itertools.product(m.COLORS, repeat=2)
        if (edge[0], edge[1], i, j) not in solved
    }
    assert len(source) == 71
    xn = {j: f"xn{j}" for j in m.COLORS if j != r}
    yn = {j: f"yn{j}" for j in m.COLORS if not (kind == "y" and j == s)}
    zn = {j: f"zn{j}" for j in m.COLORS if not (kind == "z" and j == s)}

    def raw(edge, i, j):
        return source[edge, i, j]

    def w(j):
        return "1" if j == r else xn[j]

    def qy(j):
        return "1" if kind == "y" and j == s else yn[j]

    def qz(j):
        return "1" if kind == "z" and j == s else zn[j]

    # Load-bearing repair: define the A37 quotient before every dependent
    # expression.  d and b_h only read the retained pivot row, so this is
    # acyclic even though inverse_v is bound after those expressions.
    def pivot_v(j):
        return raw((3, 7), p, j)

    determinant = m.difference(m.product(w(a), pivot_v(b)), m.product(w(b), pivot_v(a)))

    def b_value(h):
        return m.summation(m.product(raw((2, 6), h, ell), pivot_v(ell)) for ell in m.COLORS)

    b_values = [b_value(h) for h in m.COLORS]
    P = m.product("abar", "beta", pivot_v(q), determinant)
    inverse_v = m.product("abar", "beta", determinant, b_values[pivot_k], f"t{m_index}", "sat")

    def a37(i, j):
        if i == p or j == q:
            return raw((3, 7), i, j)
        return m.product(raw((3, 7), i, q), pivot_v(j), inverse_v)

    # A35 is expanded only after the corrected A37 accessor exists.
    def partner_entry(i, j):
        if j != s:
            return raw((3, 5), i, j)
        tail = m.summation(
            [m.product(raw((3, 5), i, ell), qy(ell)) for ell in m.COLORS if ell != s]
            + [m.product(a37(i, ell), qz(ell)) for ell in m.COLORS]
        )
        return m.difference("beta" if i == coordinate else "0", tail)

    # A36 is likewise reconstructed only from the corrected A37 accessor.
    def a36(i, j):
        return f"-({m.summation(m.product(a37(i, ell), raw((2, 6), j, ell)) for ell in m.COLORS)})"

    def a06(i, j):
        reduced = m.difference("abar" if i == coordinate else "0", m.product(f"t{i}", w(c)))
        if j == a:
            return m.summation((m.product(reduced, pivot_v(b)), m.product(w(b), f"t{i}", pivot_v(c))))
        if j == b:
            return f"-({m.summation((m.product(w(a), f't{i}', pivot_v(c)), m.product(reduced, pivot_v(a))))})"
        assert j == c
        return m.product(determinant, f"t{i}")

    def a17(i, j):
        if j != pivot_k:
            return raw((1, 7), i, j)
        numerator = m.difference(
            pivot_v(i),
            m.summation(m.product(raw((1, 7), i, h), b_values[h]) for h in m.COLORS if h != pivot_k),
        )
        return m.product(numerator, P, f"t{m_index}", "sat")

    def entry(edge, i, j):
        if edge in m.FIXED:
            return "1" if i == j else "0"
        if edge == m.ELIMINATED:
            return a36(i, j)
        if edge == (0, 6):
            return a06(i, j)
        if edge == (1, 7):
            return a17(i, j)
        if edge == (3, 5):
            return partner_entry(i, j)
        if edge == (3, 7):
            return a37(i, j)
        return raw(edge, i, j)

    variables = (
        list(source.values()) + list(xn.values()) + ["abar"] + list(yn.values())
        + list(zn.values()) + ["beta", "t0", "t1", "t2", "sat"]
    )
    assert len(variables) == len(set(variables)) == 84
    equations = []
    for word in itertools.product(m.COLORS, repeat=8):
        value = m.amplitude(entry, word)
        equations.append(m.difference(value, "1") if len(set(word)) == 1 else value)
    equations.append(m.product(P, b_values[pivot_k], f"t{m_index}", "sat") + "-1")
    assert len(equations) == 6562
    removed = {f"a17_{i}{pivot_k}" for i in m.COLORS}
    removed |= {f"a37_{i}{j}" for i in m.COLORS if i != p for j in m.COLORS if j != q}
    text = program(variables, equations)
    census = literal_census(text, variables, equations, removed)
    dependency_probe = {
        "a35_partner_uses_corrected_a37": all(
            name not in partner_entry(i, s)
            for i in m.COLORS
            for name in ("a37_11", "a37_12", "a37_21", "a37_22")
        ),
        "a36_reconstruction_uses_corrected_a37": all(
            name not in a36(i, j)
            for i, j in itertools.product(m.COLORS, repeat=2)
            for name in ("a37_11", "a37_12", "a37_21", "a37_22")
        ),
        "amplitudes_literal_closed": census["all_removed_symbols_absent"],
    }
    assert all(dependency_probe.values())
    return text, variables, equations, sorted(removed), census, dependency_probe


# Sparse exact polynomial arithmetic, deliberately independent of source strings.
def C(value: int):
    return collections.Counter({(): value}) if value else collections.Counter()


def V(name: str):
    return collections.Counter({(name,): 1})


def add(*polys):
    out = collections.Counter()
    for poly in polys:
        out.update(poly)
    return collections.Counter({monomial: coefficient for monomial, coefficient in out.items() if coefficient})


def neg(poly):
    return collections.Counter({monomial: -coefficient for monomial, coefficient in poly.items()})


def mul(*polys):
    out = C(1)
    for poly in polys:
        nxt = collections.Counter()
        for left, left_coefficient in out.items():
            for right, right_coefficient in poly.items():
                nxt[tuple(sorted(left + right))] += left_coefficient * right_coefficient
        out = collections.Counter({monomial: coefficient for monomial, coefficient in nxt.items() if coefficient})
    return out


def dot(left, right):
    return add(*(mul(a, b) for a, b in zip(left, right)))


def cross(left, right):
    return [
        add(mul(left[1], right[2]), neg(mul(left[2], right[1]))),
        add(mul(left[2], right[0]), neg(mul(left[0], right[2]))),
        add(mul(left[0], right[1]), neg(mul(left[1], right[0]))),
    ]


def identity_replay() -> dict:
    w = [C(1), V("xn1"), V("xn2")]
    v = [V("v0"), V("v1"), V("v2")]
    abar = V("abar")
    t0 = V("t0")
    d = add(v[1], neg(mul(w[1], v[0])))
    reduced = add(abar, neg(mul(t0, w[2])))
    u0 = [
        add(mul(reduced, v[1]), mul(w[1], t0, v[2])),
        neg(add(mul(t0, v[2]), mul(reduced, v[0]))),
        mul(d, t0),
    ]
    assert dot(u0, v) == C(0)
    assert dot(u0, w) == mul(d, abar)
    cross_checks = 0
    for m_index in (1, 2):
        tm = V(f"t{m_index}")
        um = [mul(tm, value) for value in cross(w, v)]
        assert dot(um, v) == C(0) and dot(um, w) == C(0)
        assert cross(u0, um) == [neg(mul(tm, d, abar, value)) for value in v]
        cross_checks += 4

    # Cleared-denominator forward/reverse identities.  S-1 is exactly the
    # combined saturation equation; each reconstructed relation is a
    # multiple of it and therefore vanishes in the localized quotient.
    n, rho, vj, p, b, tm, sat = (V(name) for name in ("N", "rho", "vj", "P", "b", "tm", "sat"))
    saturation = add(mul(p, b, tm, sat), C(-1))
    solved_a17 = mul(n, p, tm, sat)
    assert add(mul(b, solved_a17), neg(n)) == mul(n, saturation)
    inverse_v0 = mul(V("abar"), V("beta"), V("d"), b, tm, sat)
    saturation_v0 = add(mul(V("v0"), inverse_v0), C(-1))
    reconstructed = mul(rho, vj, inverse_v0)
    assert add(mul(V("v0"), reconstructed), neg(mul(rho, vj))) == mul(rho, vj, saturation_v0)

    classifications = {}
    for t1_nonzero, t2_nonzero in itertools.product((False, True), repeat=2):
        branch = "D(t1)" if t1_nonzero else ("D(t2)" if t2_nonzero else "V(t1,t2)")
        classifications[f"{int(t1_nonzero)}{int(t2_nonzero)}"] = branch
    assert set(classifications.values()) == {"D(t1)", "D(t2)", "V(t1,t2)"}
    nine = [(k, branch) for k in range(3) for branch in ("D(t1)", "D(t2)", "V(t1,t2)")]
    assert len(nine) == len(set(nine)) == 9
    return {
        "cramer_dot_identities": 6,
        "cross_product_component_identities": cross_checks,
        "a17_forward_reverse_cleared_identity": True,
        "a37_forward_reverse_cleared_identity": True,
        "saturation_forward": "sat_new=sat_old/t_m",
        "saturation_reverse": "sat_old=t_m*sat_new",
        "boolean_cover_cases": classifications,
        "nine_strata": [[k, branch] for k, branch in nine],
    }


def main() -> None:
    for path, expected in PINS.items():
        assert sha(path) == expected, (path, sha(path), expected)
    m = load_base()
    assert m.orbit_representative(RECORD) == RECORD
    rejection = json.loads((REJECTION / "results_referee.json").read_text())
    assert rejection["status"] == "REJECT_LITERAL_RANK2_SOURCES_REFERENCE_UNDECLARED_ELIMINATED_A37"
    assert rejection["repair_required"].startswith("regenerate the full dependency graph")

    sources = []
    for pivot_k in m.COLORS:
        for m_index in (1, 2):
            text, variables, equations, removed, census, dependency_probe = build_open(m, pivot_k, m_index)
            path = HERE / f"rep5_p00_guardpivot_k{pivot_k}_rank2_t{m_index}_Q.sing"
            atomic(path, text)
            parsed_variables, parsed_equations = parse_program(path.read_text())
            assert parsed_variables == variables and parsed_equations == equations
            sources.append({
                "pivot_k": pivot_k,
                "rank_branch": "rank2_open",
                "t_open": m_index,
                "path": path.name,
                "sha256": sha(path),
                "bytes": path.stat().st_size,
                "variables": len(variables),
                "generators": len(equations),
                "removed_variables": removed,
                "literal_census": census,
                "dependency_probe": dependency_probe,
                "origin": "regenerated_from_raw_entries_v2",
            })

        # Preserve the three sources independently shown literal-valid by the
        # rejection referee; copy exact bytes and revalidate them in v2.
        name = f"rep5_p00_guardpivot_k{pivot_k}_rank1_closed_Q.sing"
        old_path = OLD / name
        assert sha(old_path) == VALID_COMPLEMENTS[pivot_k]
        atomic(HERE / name, old_path.read_text())
        path = HERE / name
        variables, equations = parse_program(path.read_text())
        removed = {f"a17_{i}{pivot_k}" for i in m.COLORS}
        census = literal_census(path.read_text(), variables, equations, removed)
        assert len(variables) == 86 and len(equations) == 6570
        assert "t1" not in variables and "t2" not in variables
        assert sha(path) == VALID_COMPLEMENTS[pivot_k]
        sources.append({
            "pivot_k": pivot_k,
            "rank_branch": "rank1_closed",
            "t_open": None,
            "path": path.name,
            "sha256": sha(path),
            "bytes": path.stat().st_size,
            "variables": len(variables),
            "generators": len(equations),
            "removed_variables": sorted(removed),
            "literal_census": census,
            "origin": "byte_preserved_rejection_referee_literal_valid_complement",
        })

    assert len(sources) == 9
    assert sum(record["rank_branch"] == "rank2_open" for record in sources) == 6
    assert sum(record["rank_branch"] == "rank1_closed" for record in sources) == 3
    assert all(record["literal_census"]["all_removed_symbols_absent"] for record in sources)
    identities = identity_replay()
    result = {
        "schema": "KRENN_X5_REP5_RANK_STRATIFIED_GUARD_PIVOT_DESIGN_V2",
        "status": "PASS_SUPERSEDING_CORRECTED_NINE_STRATA_ZERO_SOLVES",
        "supersedes": {
            "rejected_producer_manifest_sha256": PINS[OLD / "MANIFEST.sha256"],
            "rejection_manifest_sha256": PINS[REJECTION / "FINAL_MANIFEST.sha256"],
            "rejection_result_sha256": PINS[REJECTION / "results_referee.json"],
            "rejection_status": rejection["status"],
        },
        "repair": {
            "defect": rejection["materialization_defect"],
            "load_bearing_order": [
                "raw retained entries excluding solved A06/A35/A17 and four A37 off-pivot symbols",
                "pivot-row v, d, b_h, P, and inverse-v0 localization expression",
                "proportional A37 accessor",
                "A35 partner-column expansion using corrected A37",
                "A36 reconstruction using corrected A37",
                "A06 and A17 reconstructions",
                "all 6561 amplitudes",
            ],
            "six_open_sources_regenerated_from_scratch": True,
            "three_complement_sources_byte_preserved_and_revalidated": True,
            "undeclared_removed_symbol_occurrences": 0,
        },
        "parent_guard_pivot": {
            "charts": 3,
            "variables": 88,
            "generators": 6574,
            "q_source_sha256": [PINS[PIVOT / f"rep5_p00_guardpivot_k{k}_Q.sing"] for k in m.COLORS],
        },
        "rank_lemma": {
            "cramer_rows": "u_0 dot v=0, u_0 dot w=d*abar; for m=1,2, u_m=t_m*(w cross v)",
            "minor_identity": "u_0 cross u_m=-t_m*d*abar*v",
            "rank2_kernel_implication": "on D(t_m), saturation makes t_m,d,abar,v_0 units, so rank(A06)=2 and ker(A06)=span(v)",
            "proportional_rows": "A37[j,l]=A37[j,0]*A37[0,l]/A37[0,0]",
            "all_first_guards": "A06*A37[j]^T=rho_j*A06*v^T=0",
            "all_second_guards": "A37[j]^T-A17*A26*A37[j]^T=rho_j*(v^T-A17*b)",
        },
        "rank2_open_strata": {
            "count": 6,
            "variables": 84,
            "generators": 6562,
            "breakdown": {"full_x5": 6561, "combined_saturation": 1, "explicit_guards": 0},
        },
        "rank1_closed_strata": {
            "count": 3,
            "variables": 86,
            "generators": 6570,
            "breakdown": {"full_x5": 6561, "first_guards": 2, "second_guards": 6, "combined_saturation": 1},
        },
        "identity_replay": identities,
        "cover": "for each k, D(t1) union D(t2) union V(t1,t2) is exhaustive; three k charts give exactly nine strata",
        "sources": sources,
        "pins": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
        "scope": {
            "design_only": True,
            "singular_runs": 0,
            "ideal_runs": 0,
            "consumed_k0_reused": False,
            "mathematical_coverage": False,
            "rep5_closed": False,
            "performance_claim": False,
        },
    }
    atomic(HERE / "results_design_v2.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "sources": len(sources), "open_literal_valid": 6, "runs": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
