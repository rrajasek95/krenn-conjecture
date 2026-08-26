#!/usr/bin/env python3
"""Exact factorizing-basis closure of the low-degree C9 branches.

On the frozen B0=0, Kplus!=0, L!=0 residual, the linear-C9 elimination
leaves univariate factors of degrees 2,3,4,34.  This audit proves exactly:

* qplus forces the selected factor p3 to vanish;
* qa and qfour force the solve denominator L to vanish.

It uses Singular's exact characteristic-zero factorizing Groebner basis:
the bare branch has a component, while adding the named nonzero constraint
removes every component.  The degree-34 factor is deliberately out of scope.
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
PROBE = HERE / "probe_branch0_cycle_b0_lnonzero_c9_factor.py"
OUT = HERE / "results_branch0_cycle_b0_lnonzero_c9_low_factors.json"


def load(path):
    spec = importlib.util.spec_from_file_location("root_cycle_c9_low_source", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load(PROBE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def component_count(variables, generators, constraint=None):
    prefix = (f"ring R=0,({','.join(map(str, variables))}),dp;"
              f"ideal I={','.join(P.singular(value) for value in generators)};")
    if constraint is None:
        body = 'list L=facstd(I);print("BEGIN");print(size(L));print("END");quit;'
    else:
        body = (f"ideal C={P.singular(constraint)};list L=facstd(I,C);"
                'print("BEGIN");print(size(L));print("END");quit;')
    completed = subprocess.run(["Singular", "-q", "-c", prefix+body],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "exact facstd subprocess failed")
    lines = completed.stdout.splitlines()
    body_lines = lines[lines.index("BEGIN")+1:lines.index("END")]
    require(len(body_lines) == 1, "unexpected facstd status output")
    return int(body_lines[0])


def digest(value):
    return sha256(str(P.sp.expand(value)).encode("ascii")).hexdigest()


def main():
    variables, f, g, c9, named, unused, live = P.derive()
    live_map = dict(live)
    cases = (("qplus", "p3"), ("qa", "L"), ("qfour", "L"))
    statuses = {}
    for factor_name, constraint_name in cases:
        generators = (f, g, c9, named[factor_name])
        bare = component_count(variables, generators)
        constrained = component_count(variables, generators,
                                      live_map[constraint_name])
        require(bare > 0 and constrained == 0,
                f"{factor_name}/{constraint_name} closure changed")
        statuses[factor_name] = {
            "bare_component_count": bare,
            "killing_constraint": constraint_name,
            "localized_component_count": constrained,
        }

    # Must-fire: p2 is not a valid replacement for p3 on qplus.
    qplus_generators = (f, g, c9, named["qplus"])
    wrong = component_count(variables, qplus_generators, live_map["p2"])
    require(wrong > 0, "wrong-constraint must-fire did not fire")

    result = {
        "status": "UNAUDITED exact closure of C9 degree-2/3/4 factors",
        "assumptions": [
            "B0=0", "Kplus!=0", "L!=0", "Delta!=0", "D0!=0",
            "all Laurent and selected-term factors live"],
        "core_term_counts": [len(P.sp.Poly(value, *variables).terms())
                             for value in (f, g, c9)],
        "core_sha256": {"F": digest(f), "G": digest(g), "C9": digest(c9)},
        "cases": statuses,
        "must_fire_qplus_with_p2_component_count": wrong,
        "algorithm_scope": (
            "Exact characteristic-zero facstd gives a radical-equivalent "
            "component cover; an empty cover after a nonzero constraint "
            "proves that open branch empty.  Degree34 and C35 are excluded."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("branch-0 cycle C9 low factors: PASS")
    print("closures:", [(name, data["killing_constraint"])
                        for name, data in statuses.items()])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
