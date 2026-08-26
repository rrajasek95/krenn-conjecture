#!/usr/bin/env python3
"""Freeze Cof(2,3) T4750 and gcd interfaces against Q/R/S."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))
import sympy as sp


HERE = Path(__file__).resolve().parent
TREE = HERE / "audit_branch0_cycle_generic_b3_resultant_tree.py"
FULL = HERE / "export_branch0_cycle_generic_azero_bzero_full_source_exact.py"
GCD = HERE / "export_branch0_cycle_generic_q4098_r4885_gcd.py"
RESULT = HERE / "results_branch0_cycle_generic_t4750_gcd_interface.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


SOURCE = load("t4750_tree", TREE)
FULL_SOURCE = load("t4750_full", FULL)
GCD_SOURCE = load("t4750_gcd", GCD)


def sha(poly, variables):
    primitive = sp.Poly(poly, *variables, domain="QQ").primitive()[1].as_expr()
    return sha256(str(sp.expand(primitive)).encode("ascii")).hexdigest()


def choose(poly, variables, terms):
    primitive = sp.Poly(poly, *variables).primitive()[1].as_expr()
    factors = sp.factor_list(primitive)[1]
    matches = [f for f, e in factors if len(sp.Poly(f, *variables).terms()) == terms]
    require(len(matches) == 1, f"unique {terms}-term factor missing")
    return matches[0], [(len(sp.Poly(f, *variables).terms()),
                         sp.Poly(f, *variables).total_degree(), int(e))
                        for f, e in factors]


def main() -> None:
    rows, _, _ = SOURCE.SOURCE.derive()
    b0, b1, b3, d1, d3, d4 = SOURCE.SOURCE.SOURCE.PARAMETERS
    variables = (b0, b1, d1, d3, d4)
    compact = [sp.cancel(poly/factor) for poly, factor in zip(
        rows, (b1*b3*d1*d3, d4, b3, b1*b3, 1, 1, 1), strict=True)]
    leading = sp.diff(compact[1], b3)
    constant = sp.expand(compact[1].subs(b3, 0))
    gcd_variables, q4098, r4885, _, _, _ = GCD_SOURCE.derive()
    require(gcd_variables == variables, "Q/R variable order changed")
    lower, lower_hashes, *_ = FULL_SOURCE.derive_lower_cofactors()
    s4331, profile13 = choose(
        SOURCE.linear_resultant(lower[1], b3, leading, constant), variables, 4331)
    t4750, profile23 = choose(
        SOURCE.linear_resultant(lower[2], b3, leading, constant), variables, 4750)
    require(profile13 == [(2, 2, 1), (1, 1, 2), (8, 4, 1), (4331, 25, 1)]
            and profile23 == [(2, 2, 1), (1, 1, 2), (8, 4, 1), (4750, 26, 1)],
            "Cof(1/2,3) factor profiles changed")
    programs = []
    for characteristic in (1073741827, 1073741789, 0):
        suffix = "char0" if characteristic == 0 else f"p{characteristic}"
        path = HERE / f"branch0_cycle_generic_t4750_gcd_{suffix}.sing"
        path.write_text(
            f"ring K={characteristic},({','.join(map(str, variables))}),dp;\n"
            f"poly q={str(sp.expand(q4098)).replace('**','^')};\n"
            f"poly r={str(sp.expand(r4885)).replace('**','^')};\n"
            f"poly s={str(sp.expand(s4331)).replace('**','^')};\n"
            f"poly t={str(sp.expand(t4750)).replace('**','^')};\n"
            "poly gq=gcd(q,t);poly gr=gcd(r,t);poly gs=gcd(s,t);\n"
            'print("BEGIN");print(string(gq));print(string(gr));print(string(gs));'
            'print("END");quit;\n')
        programs.append({"characteristic": characteristic, "path": path.name,
                         "sha256": sha256(path.read_bytes()).hexdigest()})
    result = {
        "status": "UNAUDITED exact/two-prime T4750 gcd interface",
        "cofactor23_literal_source_sha256": lower_hashes[2],
        "cofactor23_factor_profile": profile23,
        "q4098_sha256": sha(q4098, variables),
        "r4885_sha256": sha(r4885, variables),
        "s4331_sha256": sha(s4331, variables),
        "t4750_sha256": sha(t4750, variables),
        "programs": programs,
        "scope": (
            "Cof(2,3) contributes b0^2*D0*C8*T4750 after fraction-free b3 "
            "elimination. The frozen live factors are removed and C8 is handled "
            "by its exact empty-branch theorem. Pairwise gcds diagnose shared "
            "hypersurfaces only; they do not decide the Q=R=S=T intersection."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("T4750 gcd interface export: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
