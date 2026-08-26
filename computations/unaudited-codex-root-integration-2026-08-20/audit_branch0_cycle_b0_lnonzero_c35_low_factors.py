#!/usr/bin/env python3
"""Exact closure of the three low-degree distinct-C35 factors.

The distinct 140/136-term C35 eliminants have univariate common factors of
degrees 2, 2, 4, 24, and 153 after already-localized linear factors are
removed.  This audit closes the degree-2/2/4 factors exactly:

* d1^2+2*d1-1 is H-dead on the L-open branch;
* d1^2+1 lies on D0=0;
* d1^4+2*d1^3+6*d1^2-2*d1+1 lies on L=0.

The degree-24 and degree-153 factors are deliberately out of scope.
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
OUT = HERE / "results_branch0_cycle_b0_lnonzero_c35_low_factors.json"


def load(path):
    spec = importlib.util.spec_from_file_location("root_cycle_c35_low", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


P = load(PROBE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def component_count(variables, generators, constraints=()):
    command = (f"ring R=0,({','.join(map(str, variables))}),dp;"
               f"ideal I={','.join(P.singular(x) for x in generators)};")
    if constraints:
        command += (f"ideal C={','.join(P.singular(x) for x in constraints)};"
                    "list F=facstd(I,C);")
    else:
        command += "list F=facstd(I);"
    command += 'print("BEGIN");print(size(F));print("END");quit;'
    completed = subprocess.run(["Singular", "-q", "-c", command],
                               text=True, capture_output=True,
                               timeout=60, check=False)
    require(completed.returncode == 0 and not completed.stderr.strip(),
            "exact facstd subprocess failed")
    lines = completed.stdout.splitlines()
    body = lines[lines.index("BEGIN")+1:lines.index("END")]
    require(len(body) == 1, "malformed facstd result")
    return int(body[0])


def main():
    variables, f, g, c35, _, df, dg, _, live = P.derive()
    _, d1, _ = variables
    live_map = dict(live)
    factors = {
        "qplus": d1**2 + 2*d1 - 1,
        "qi": d1**2 + 1,
        "qfour": d1**4 + 2*d1**3 + 6*d1**2 - 2*d1 + 1,
    }
    constraints = {
        "qplus": (live_map["L"], live_map["H"]),
        "qi": (live_map["D0"],),
        "qfour": (live_map["L"],),
    }
    base = (f, g, c35, df, dg)
    statuses = {}
    for name, factor in factors.items():
        generators = (*base, factor)
        bare = component_count(variables, generators)
        localized = component_count(variables, generators,
                                    constraints[name])
        require(bare > 0 and localized == 0,
                f"{name} closure changed")
        statuses[name] = {
            "bare_component_count": bare,
            "killing_constraints": [
                next(label for label, value in live
                     if P.sp.expand(value - constraint) == 0)
                for constraint in constraints[name]],
            "localized_component_count": localized,
        }

    # Must-fire: H alone does not kill the qi branch; D0 is load-bearing.
    wrong = component_count(variables, (*base, factors["qi"]),
                            (live_map["H"],))
    require(wrong > 0, "qi/H wrong-constraint must-fire did not fire")

    digest = lambda value: sha256(
        str(P.sp.expand(value)).encode("ascii")).hexdigest()
    result = {
        "status": "UNAUDITED exact closure of distinct-C35 low factors",
        "assumptions": [
            "B0=0", "Kplus!=0", "L!=0", "Delta!=0", "D0!=0",
            "H!=0 and all selected-term factors are live"],
        "core_term_counts": [len(P.sp.Poly(x, *variables).terms())
                             for x in base],
        "core_sha256": {name: digest(value) for name, value in zip(
            ("F", "G", "C35", "R140", "R136"), base)},
        "factor_sha256": {name: digest(value)
                          for name, value in factors.items()},
        "cases": statuses,
        "must_fire_qi_with_H_component_count": wrong,
        "scope": (
            "Exact Q facstd closes the distinct-resultant factors of "
            "degrees 2,2,4. Factors of degrees 24 and 153 remain open."),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print("branch-0 cycle C35 distinct low factors: PASS")
    print("closures:", [(name, data["killing_constraints"])
                        for name, data in statuses.items()])
    print("result sha256:", result["result_sha256"])


if __name__ == "__main__":
    main()
