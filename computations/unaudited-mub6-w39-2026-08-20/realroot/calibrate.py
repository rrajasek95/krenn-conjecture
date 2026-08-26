"""realroot calibration suite -- systems with KNOWN real-root counts.

Ledger 21/29/31: every control is declared here, executed, and the manifest of
executed controls is asserted against the declared list at exit; the file exits
NONZERO if any control is skipped or disagrees.  Ledger 26: VIEW A (our own
trace form) and VIEW B (Singular rootsmr.lib) must AGREE on every case.

Cases deliberately span: multiplicity (rank < vdim), irrational real roots,
empty real locus with nonempty complex locus, and the unit ideal.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from realroot import real_root_count, real_root_count_view_b   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

# name: (generators, variables, expected distinct complex, expected real, note)
CASES = {
    "univariate_x5_minus_x": (
        ["x^5-x", "y-1"], ["x", "y"], 5, 3,
        "roots 0,1,-1 real; +-i complex"),
    "circle_meets_hyperbola": (
        ["x^2+y^2-1", "x*y-1/4"], ["x", "y"], 4, 4,
        "x^2=(2+-sqrt3)/4, all four real"),
    "no_real_points": (
        ["x^2+1", "y^2+1"], ["x", "y"], 4, 0,
        "complex nonempty, real empty -- the case the unit-ideal test misses"),
    "circle_meets_line": (
        ["x^2+y^2-1", "x-y"], ["x", "y"], 2, 2, "two real points"),
    "imaginary_circle_line": (
        ["x^2+y^2+1", "x-y"], ["x", "y"], 2, 0, "two complex, no real"),
    "double_point_multiplicity": (
        ["x^2", "y-1"], ["x", "y"], 1, 1,
        "vdim 2 but ONE distinct point: rank must be 1, not 2"),
    "tangent_circles": (
        ["(x-1)^2+y^2-1", "(x+1)^2+y^2-1"], ["x", "y"], 1, 1,
        "vdim 2, single real tangency point"),
    "irrational_real_root": (
        ["x^3-2", "y-1"], ["x", "y"], 3, 1, "cbrt(2) real, two complex"),
    "cube_roots_grid": (
        ["x^3-1", "y^3-1"], ["x", "y"], 9, 1, "only (1,1) is real"),
    "unit_ideal": (
        ["x^2+y^2-1", "x^2+y^2-4"], ["x", "y"], 0, 0, "empty over C"),
}


def main():
    executed = []
    results = {}
    failures = []
    for name, (gens, vs, exp_c, exp_r, note) in CASES.items():
        a = real_root_count(gens, vs, workdir=HERE, tag="cal_" + name, timeout=120)
        b = real_root_count_view_b(gens, vs, workdir=HERE, tag="calB_" + name,
                                   timeout=120)
        executed.append(name)
        rec = {"note": note, "expected_distinct_complex": exp_c,
               "expected_real": exp_r, "view_a": a, "view_b": b}
        results[name] = rec
        if not a.get("ok"):
            failures.append((name, "VIEW A not ok: " + str(a.get("status"))))
            continue
        if a["status"] == "UNIT":
            got_c, got_r = 0, 0
        else:
            got_c, got_r = a["n_distinct_complex"], a["n_real"]
        if (got_c, got_r) != (exp_c, exp_r):
            failures.append((name, f"VIEW A got (C={got_c},R={got_r}) "
                                   f"expected (C={exp_c},R={exp_r})"))
        if not b.get("ok"):
            failures.append((name, "VIEW B not ok: " + str(b.get("status"))))
        elif b.get("n_real") != got_r:
            failures.append((name, f"VIEW A/B DISAGREE: A={got_r} B={b.get('n_real')}"))
        print(f"{name:28s} C={got_c:3d} (exp {exp_c:3d})  "
              f"R={got_r:3d} (exp {exp_r:3d})  viewB={b.get('n_real')}")

    with open(os.path.join(HERE, "calibration_results.json"), "w") as fh:
        json.dump(results, fh, indent=2, default=str)

    # ledger 21/31: manifest assertion, loud failure
    declared = sorted(CASES)
    if sorted(executed) != declared:
        print("CONTROL MANIFEST MISMATCH:", sorted(executed), "!=", declared)
        sys.exit(2)
    if failures:
        print("CALIBRATION FAILURES:")
        for n, m in failures:
            print("  ", n, m)
        sys.exit(1)
    print(f"CONTROL MANIFEST OK: {len(declared)} declared, {len(executed)} "
          f"executed, 0 failures; VIEW A and VIEW B agree on all cases.")


if __name__ == "__main__":
    main()
