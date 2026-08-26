#!/usr/bin/env python3
"""H1 / BLOCKER 4 (extension) -- calibrate the ledger's Singular hazards on
THIS build, so the queue's Singular debts can be reported as live or dormant.

UNAUDITED.  Hygiene agent H1, 2026-08-15.  Read-only probes on scratch
scripts; nothing in the repository is touched.

Ledger items exercised:
  6   `e1`, `mult`, `I` are reserved identifiers in Singular 4.4.
  11  Singular reports errors on stdout WITH RETURN CODE 0 -- parse for `?`.
  11  `ideal S = sat(I,J)[1]` coerces and takes the FIRST GENERATOR.
  14  On the W16 build `sat(I,J)` returns an ideal, and `LIB "elim.lib";`
      is required or `sat` is undefined.

Each probe records the stdout, whether any `?` line appeared, and the
return code -- so the "return code 0 is not a success signal" rule is
demonstrated rather than asserted.

Usage:  python3 h1_b4_singular_calib.py
Writes  results_b4_singular_calib.json
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, timeout=120):
    exe = shutil.which("Singular") or shutil.which("singular")
    if exe is None:
        return {"skipped": "no Singular binary on PATH"}
    with tempfile.NamedTemporaryFile("w", suffix=".sing", delete=False) as fh:
        fh.write(script + "\nquit;\n")
        path = fh.name
    try:
        p = subprocess.run([exe, "-q", "--no-warn", path],
                           capture_output=True, text=True, timeout=timeout)
    finally:
        os.unlink(path)
    out = p.stdout + p.stderr
    qlines = [l for l in out.splitlines() if l.strip().startswith("?")]
    return {"returncode": p.returncode,
            "question_lines": qlines,
            "has_error_marker": bool(qlines),
            "stdout": out.strip().splitlines()}


PROBES = {
    # ledger 6: are e1 / mult / I actually reserved on this build?
    "L6_reserved_I": 'ring rr = 0,(x,y,t),dp;\nideal I = x,y;\n"I_size"; size(I);',
    "L6_reserved_e1": 'ring rr = 0,(x,y),dp;\npoly e1 = x+y;\n"e1_ok"; (e1==x+y);',
    "L6_reserved_mult": 'ring rr = 0,(x,y),dp;\npoly mult = x*y;\n"mult_ok"; (mult==x*y);',
    # ledger 14: sat needs elim.lib; what does it return?
    "L14_sat_typeof_with_elim":
        'LIB "elim.lib";\nring rr = 0,(a,b,c),dp;\nideal Jt = a*b, a*c;\n'
        'def L = sat(Jt, b);\n"typeof"; typeof(L);',
    "L11_sat_without_elim":
        'ring rr = 0,(a,b,c),dp;\nideal Jt = a*b, a*c;\n'
        'ideal S = sat(Jt, b);\n"reached"; size(S);',
    # ledger 11: does [1] change the answer when the saturation has >1 gen?
    "L11_sat_bracket1_multigen":
        'LIB "elim.lib";\nring rr = 0,(a,b,c,d),dp;\n'
        'ideal Jt = a*d, b*d, c*d;\n'
        'ideal S1 = sat(Jt, d);\n"plain_size"; size(S1);\n'
        'ideal S2 = sat(Jt, d)[1];\n"bracket1_size"; size(S2);\n'
        '"identical"; (size(S1)==size(S2));',
    # ledger 13: does shadowing a ring variable really pass silently?
    "L13_shadowing_silent":
        'ring rr = 0,(g11,g12),dp;\npoly g11 = g12;\n'
        '"g11_now"; g11;\n"is_it_the_variable"; (g11==var(1));',
}


def main():
    out = {"agent": "H1", "blocker": "4-singular-calibration",
           "pinned_head": open(os.path.join(HERE, "PINNED_HEAD.txt")
                               ).read().split()[0],
           "singular": shutil.which("Singular") or shutil.which("singular"),
           "probes": {}}
    ver = run('"v"; system("version");')
    out["singular_version"] = ver.get("stdout")
    print("Singular:", out["singular"], out["singular_version"])
    for name, script in PROBES.items():
        r = run(script)
        out["probes"][name] = r
        print(f"\n--- {name} ---")
        print(f"    returncode={r.get('returncode')} "
              f"error_marker={r.get('has_error_marker')}")
        for l in r.get("stdout", []):
            print("   ", l)
    # the headline: return code 0 despite errors
    bad = [k for k, r in out["probes"].items()
           if r.get("has_error_marker") and r.get("returncode") == 0]
    out["probes_with_errors_but_returncode_0"] = bad
    print(f"\nPROBES THAT ERRORED WITH RETURN CODE 0: {bad}")
    with open(os.path.join(HERE, "results_b4_singular_calib.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote results_b4_singular_calib.json")


if __name__ == "__main__":
    main()
