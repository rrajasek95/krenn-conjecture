#!/usr/bin/env python3
"""Exact second rep5 quotient after guard-pivot; design generation only."""
from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"
PIVOT = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-2026-08-25"
PIVOT_REF = ROOT / "computations/unaudited-codex-n8-x5-rep5-post-timeout-guard-pivot-quotient-design-referee-2026-08-25"
K0_TERM = ROOT / "computations/unaudited-codex-n8-x5-rep5-guard-pivot-k0-modular-terminal-referee-2026-08-25"

PINS = {
    BASE / "MANIFEST.sha256": "33ae759fb235518412c33d36d621ccce09b8a9e05e9ece05b6d1aaf7f2d8c40c",
    BASE / "generate_design.py": "3844eadf4a9e21c2feb012cbd684c22ca7611f4d22f87659e19952d0381614f4",
    PIVOT / "MANIFEST.sha256": "00ac8c2a1bea2b958644b0e6b1851d26535c83cc715d92b28335157b219da3f9",
    PIVOT / "rep5_p00_guardpivot_k0_Q.sing": "d4204428cab5f3b5dd4ac321dd1ae04ce9b79c8f1197b8e1e863c6c186cc74f1",
    PIVOT / "rep5_p00_guardpivot_k1_Q.sing": "cdf782ee92b0a019c2a77d6ccc980828c7d0279ebcc3592cced648306fd95e6c",
    PIVOT / "rep5_p00_guardpivot_k2_Q.sing": "ef6fec2e4ba4baf44c07e9d90e0a1b7fb2624d99c838d901d388e3041bf6aa6d",
    PIVOT_REF / "FINAL_MANIFEST.sha256": "af4bee0ca8db5391aac9f59cb1e52051d32e66fdb2974a126468b054ca3f5a4b",
    PIVOT_REF / "results_referee.json": "940f360ab66ec5071c24181cac2218df6da90ab57901cdba8009d3eeed280c05",
    K0_TERM / "FINAL_MANIFEST.sha256": "a5dcd93bc79154bce1af90557c8496ca5aa38052f9e6b6206266e498c198e9cf",
    K0_TERM / "results_referee.json": "37358baa478e6d220a19cdf955effab940c8b560bc93242e1ed52511c5db31c8",
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
    spec = importlib.util.spec_from_file_location("sealed_rep5_base", BASE / "generate_design.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


for path, expected in PINS.items():
    assert sha(path) == expected, (path, sha(path), expected)
m = load_base()
assert m.orbit_representative(RECORD) == RECORD


def build_context_with_zero_t(record, zero_t: frozenset[int]):
    """Frozen Cramer context with selected free row parameters set to zero."""
    coordinate, p, q, r, kind, s, a, b = record
    c = next(value for value in m.COLORS if value not in (a, b))
    solved = {(0, 6, i, j) for i, j in itertools.product(m.COLORS, repeat=2)}
    partner = (3, 5) if kind == "y" else (3, 7)
    solved |= {(partner[0], partner[1], i, s) for i in m.COLORS}
    source = {
        (edge, i, j): f"a{edge[0]}{edge[1]}_{i}{j}"
        for edge in m.RETAINED
        for i, j in itertools.product(m.COLORS, repeat=2)
        if (edge[0], edge[1], i, j) not in solved
    }
    xn = {j: f"xn{j}" for j in m.COLORS if j != r}
    yn = {j: f"yn{j}" for j in m.COLORS if not (kind == "y" and j == s)}
    zn = {j: f"zn{j}" for j in m.COLORS if not (kind == "z" and j == s)}

    def raw(edge, i, j): return source[edge, i, j]
    def w(j): return "1" if j == r else xn[j]
    def qy(j): return "1" if kind == "y" and j == s else yn[j]
    def qz(j): return "1" if kind == "z" and j == s else zn[j]
    def t(i): return "0" if i in zero_t else f"t{i}"

    def partner_entry(edge, i, j):
        if kind == "y" and edge == (3, 5) and j == s:
            tail = m.summation(
                [m.product(raw((3, 5), i, k), qy(k)) for k in m.COLORS if k != s]
                + [m.product(raw((3, 7), i, k), qz(k)) for k in m.COLORS]
            )
            return m.difference("beta" if i == coordinate else "0", tail)
        if kind == "z" and edge == (3, 7) and j == s:
            tail = m.summation(
                [m.product(raw((3, 5), i, k), qy(k)) for k in m.COLORS]
                + [m.product(raw((3, 7), i, k), qz(k)) for k in m.COLORS if k != s]
            )
            return m.difference("beta" if i == coordinate else "0", tail)
        return raw(edge, i, j)

    def outside(i, j): return partner_entry(m.OUTSIDE, i, j)
    def v(j): return outside(p, j)
    determinant = m.difference(m.product(w(a), v(b)), m.product(w(b), v(a)))

    def entry(edge, i, j):
        if edge in m.FIXED: return "1" if i == j else "0"
        if edge == m.ELIMINATED:
            return f"-({m.summation(m.product(outside(i, k), raw((2, 6), j, k)) for k in m.COLORS)})"
        if edge == (0, 6):
            reduced = m.difference("abar" if i == coordinate else "0", m.product(t(i), w(c)))
            if j == a: return m.summation((m.product(reduced, v(b)), m.product(w(b), t(i), v(c))))
            if j == b: return f"-({m.summation((m.product(w(a), t(i), v(c)), m.product(reduced, v(a))))})"
            assert j == c
            return m.product(determinant, t(i))
        if edge in ((3, 5), (3, 7)): return partner_entry(edge, i, j)
        return raw(edge, i, j)

    variables = (
        list(source.values()) + list(xn.values()) + ["abar"] + list(yn.values())
        + list(zn.values()) + ["beta"] + [f"t{i}" for i in m.COLORS if i not in zero_t] + ["sat"]
    )
    return entry, variables, determinant, outside(p, q)


def program(variables: list[str], equations: list[str]) -> str:
    return "\n".join([
        "// DESIGN INPUT ONLY: zero ideal runs authorized.",
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
        "quit;", "",
    ])


def build(k: int, rank_branch: str, m_index: int | None = None):
    p, q, coordinate = RECORD[1], RECORD[2], RECORD[0]
    if rank_branch == "rank1_closed":
        assert m_index is None
        old_entry, old_variables, determinant, outside = build_context_with_zero_t(RECORD, frozenset((1, 2)))
    else:
        assert rank_branch == "rank2_open" and m_index in (1, 2)
        old_entry, old_variables, determinant, outside = m.build_context(RECORD)
    P = m.product("abar", "beta", outside, determinant)

    def b(h):
        return m.summation(m.product(old_entry((2, 6), h, ell), old_entry((3, 7), p, ell)) for ell in m.COLORS)

    bs = [b(h) for h in m.COLORS]
    saturation_extra = f"t{m_index}" if rank_branch == "rank2_open" else "1"

    def solved_a17(i):
        numerator = m.difference(
            old_entry((3, 7), p, i),
            m.summation(m.product(old_entry((1, 7), i, h), bs[h]) for h in m.COLORS if h != k),
        )
        return m.product(numerator, P, saturation_extra, "sat")

    if rank_branch == "rank2_open":
        inverse_v = m.product("abar", "beta", determinant, bs[k], saturation_extra, "sat")

    def entry(edge, i, j):
        if edge == (1, 7) and j == k:
            return solved_a17(i)
        if rank_branch == "rank2_open" and edge == (3, 7) and i != p and j != q:
            return m.product(old_entry((3, 7), i, q), old_entry((3, 7), p, j), inverse_v)
        return old_entry(edge, i, j)

    removed = {f"a17_{i}{k}" for i in m.COLORS}
    if rank_branch == "rank2_open":
        removed |= {f"a37_{i}{j}" for i in m.COLORS if i != p for j in m.COLORS if j != q}
    variables = [value for value in old_variables if value not in removed]
    equations = []
    for word in itertools.product(m.COLORS, repeat=8):
        value = m.amplitude(entry, word)
        equations.append(m.difference(value, "1") if len(set(word)) == 1 else value)
    if rank_branch == "rank1_closed":
        for j in m.COLORS:
            if j != p:
                equations.append(m.summation(m.product(entry((0, 6), coordinate, ell), entry((3, 7), j, ell)) for ell in m.COLORS))
        for i, j in itertools.product(m.COLORS, repeat=2):
            if j == p: continue
            correction = m.summation(
                m.product(entry((1, 7), i, h), entry((2, 6), h, ell), entry((3, 7), j, ell))
                for h, ell in itertools.product(m.COLORS, repeat=2)
            )
            equations.append(m.difference(entry((3, 7), j, i), correction))
    equations.append(m.product(P, bs[k], saturation_extra, "sat") + "-1")
    expected = (84, 6562) if rank_branch == "rank2_open" else (86, 6570)
    assert (len(variables), len(equations)) == expected
    assert len(variables) == len(set(variables))
    assert len(equations) == len(set(equations))
    assert all(value not in ("0", "1", "-1") for value in equations)
    return program(variables, equations), variables, equations, sorted(removed)


sources = []
for k in m.COLORS:
    for branch, m_index in (("rank2_open", 1), ("rank2_open", 2), ("rank1_closed", None)):
        text, variables, equations, removed = build(k, branch, m_index)
        suffix = f"rank2_t{m_index}" if branch == "rank2_open" else "rank1_closed"
        path = HERE / f"rep5_p00_guardpivot_k{k}_{suffix}_Q.sing"
        atomic(path, text)
        sources.append({
            "pivot_k": k, "rank_branch": branch, "t_open": m_index,
            "path": path.name, "sha256": sha(path), "bytes": path.stat().st_size,
            "variables": len(variables), "generators": len(equations), "removed_variables": removed,
        })

result = {
    "schema": "KRENN_X5_REP5_RANK_STRATIFIED_GUARD_PIVOT_DESIGN_V1",
    "status": "PASS_EXACT_SECOND_QUOTIENT_NINE_STRATA_ZERO_SOLVES",
    "parent_guard_pivot": {"charts": 3, "variables": 88, "generators": 6574, "q_source_sha256": [PINS[PIVOT / f"rep5_p00_guardpivot_k{k}_Q.sing"] for k in m.COLORS]},
    "rank_lemma": {
        "cramer_rows": "u_0 dot v=0, u_0 dot w=d*abar; for m=1,2, u_m=t_m*(w cross v)",
        "minor_identity": "u_0 cross u_m=-t_m*d*abar*v, hence det(rows 0,m; columns 1,2)=-t_m*d*abar*v_0",
        "rank2_consequence": "on t_m!=0 the saturated factors d,abar,v_0 force rank(A06)=2 and ker(A06)=span(v)",
        "outside_row_substitution": "A37[j,l]=A37[j,0]*A37[0,l]*(abar*beta*d*b_k*t_m*sat) for j,l!=0",
        "inverse_identity": "v_0*(abar*beta*d*b_k*t_m*sat)=1",
        "all_first_guards": "each outside A37 row becomes rho_j*v, so A06*A37^T=0",
        "all_second_guards": "c_j=A26*(rho_j*v)^T=rho_j*b, so its guard is rho_j times the removed pivot-row guard",
    },
    "rank2_open_strata": {
        "count": 6, "per_pivot": ["t1!=0", "t2!=0"], "variables": 84, "generators": 6562,
        "generators_breakdown": {"full_x5": 6561, "combined_saturation": 1, "guards": 0},
        "forward": "from the b_k chart and t_m!=0 set sat_new=sat_old/t_m and use the forced proportional-row formulas",
        "reverse": "reconstruct the four eliminated A37 entries and set sat_old=t_m*sat_new",
    },
    "rank1_closed_strata": {
        "count": 3, "condition": "t1=t2=0", "variables": 86, "generators": 6570,
        "generators_breakdown": {"full_x5": 6561, "first_guards": 2, "second_guards": 6, "combined_saturation": 1},
        "map": "exact quotient of each b_k chart by (t1,t2); the four identically-zero first guards are omitted",
    },
    "cover": "for every b_k chart, D(t1) union D(t2) union V(t1,t2) is exhaustive; combined with the three b_k charts these nine strata cover the consumed p00 chart",
    "unit_proof_interface": "unit certificates on both t-open localizations and the (t1,t2) quotient imply the b_k chart is empty; doing this for k=0,1,2 proves the parent chart empty",
    "sources": sources,
    "pins": {str(path.relative_to(ROOT)): expected for path, expected in PINS.items()},
    "scope": {"solver_runs": 0, "consumed_k0_reused": False, "mathematical_coverage": False, "rep5_closed": False, "performance_claim": False},
}
atomic(HERE / "results_design.json", json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({"status": result["status"], "sources": len(sources), "runs": 0}, sort_keys=True))
