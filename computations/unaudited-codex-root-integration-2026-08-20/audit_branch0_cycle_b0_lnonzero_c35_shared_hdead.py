#!/usr/bin/env python3
"""Exact closure of the shared-S13 C35 cycle branch by pure-H death.

On the frozen B0=0, Kplus!=0, L!=0 reduction, the cubic C35 branch has a
13-term common resultant factor S13.  Exact characteristic-zero facstd on
F=G=C35=S13, localized at L, has one one-dimensional component.  This
audit proves the literal specialized pure Hafnian H belongs to its ideal.
Thus the whole shared-S13 branch is excluded on the required H!=0 chart.
"""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess
import sys


_SITE = (Path(sys.executable).parent.parent / "lib" /
         f"python{sys.version_info.major}.{sys.version_info.minor}" /
         "site-packages")
if str(_SITE) not in sys.path:
    sys.path.append(str(_SITE))


HERE = Path(__file__).resolve().parent
PROBE = HERE / "probe_branch0_cycle_b0_lnonzero_c35.py"
OUT = HERE / "results_branch0_cycle_b0_lnonzero_c35_shared_hdead.json"


def load(path):
    spec = importlib.util.spec_from_file_location("root_cycle_c35_hdead", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load(PROBE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def main():
    variables, f, g, c35, shared, _, _, unused, live = P.derive()
    live_map = dict(live)
    generators = (f, g, c35, shared)
    lower_map = dict(unused)
    checks = [
        ("H", live_map["H"]),
        ("H_plus_1", live_map["H"] + 1),
        *[(name, lower_map[name]) for name in
          ("cofactor_1_3", "cofactor_2_3", "cofactor_3_3",
           "cofactor_4_3", "cofactor_5_3")],
    ]
    command = (
        f"ring R=0,({','.join(map(str, variables))}),dp;"
        f"ideal I={','.join(P.singular(value) for value in generators)};"
        f"ideal C={P.singular(live_map['L'])};"
        'list F=facstd(I,C);print("BEGIN");print(size(F));'
        'ideal G=std(F[1]);print(size(G));print(dim(G));' +
        "".join(f'print("CHECK {name}");'
                f"print(size(reduce({P.singular(value)},G)));"
                for name, value in checks) +
        'print("END");quit;'
    )
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=120, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "exact facstd subprocess failed")
    lines = completed.stdout.splitlines()
    body = lines[lines.index("BEGIN")+1:lines.index("END")]
    require(body[:3] == ["1", "26", "1"],
            "shared-S13 component census changed")
    status = {}
    index = 3
    while index < len(body):
        require(body[index].startswith("CHECK "), "malformed check ledger")
        status[body[index][6:]] = int(body[index+1])
        index += 2
    require(status["H"] == 0 and status["H_plus_1"] == 1,
            "pure-H closure or must-fire changed")
    require([status[f"cofactor_{edge}_3"] for edge in range(1, 6)]
            == [0, 0, status["cofactor_3_3"],
                status["cofactor_4_3"], 0]
            and status["cofactor_3_3"] > 0
            and status["cofactor_4_3"] > 0,
            "lower-cofactor scope guard changed")

    digest = lambda value: sha256(
        str(P.sp.expand(value)).encode("ascii")).hexdigest()
    result = {
        "status": "UNAUDITED exact H-death of shared-S13 C35 branch",
        "assumptions": [
            "B0=0", "Kplus!=0", "L!=0", "Delta!=0", "D0!=0",
            "H!=0 is required by the pure-live chart"],
        "component_count": 1,
        "component_basis_size": 26,
        "component_dimension": 1,
        "core_term_counts": [len(P.sp.Poly(value, *variables).terms())
                             for value in generators],
        "core_sha256": {name: digest(value) for name, value in zip(
            ("F", "G", "C35", "S13"), generators)},
        "literal_H_remainder_terms": status["H"],
        "H_plus_1_must_fire_terms": status["H_plus_1"],
        "lower_cofactor_remainder_terms": {
            str(edge): status[f"cofactor_{edge}_3"]
            for edge in range(1, 6)},
        "scope": (
            "Exact Q facstd gives the L-open component cover; H has zero "
            "normal form on its sole component. Distinct C35 resultants "
            "and the C9 degree-34 factor remain open."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("branch-0 cycle C35 shared-S13 H-death: PASS")
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
