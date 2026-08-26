#!/usr/bin/env python3
"""W21-M2-SING: harness smoke tests (LEDGER 11 / 13 / 6) + MUTATION controls.
Every test states the answer it must produce; a wrong answer aborts."""
import json
import sys

sys.dont_write_bytecode = True
import m2core as M

out = {"_header": "UNAUDITED W21-M2-SING harness smoke tests"}
fails = []


def expect(name, got, want):
    ok = (got == want)
    print("  %-46s got=%-8s want=%-8s %s" % (name, got, want,
                                             "OK" if ok else "*** FAIL ***"))
    out[name] = {"got": str(got), "want": str(want), "ok": bool(ok)}
    if not ok:
        fails.append(name)


print("SMOKE TESTS")

# S1  LEDGER 11: Singular error on stdout with return code 0 must RAISE.
try:
    M.run_singular("ring zzr = 0,(zzv0),dp;\nthis is not singular;\nquit;\n")
    expect("S1 error-scan raises on bad script", "no-raise", "raise")
except M.SingularError:
    expect("S1 error-scan raises on bad script", "raise", "raise")

# S2  LEDGER 11: undefined sat without elim.lib must RAISE (not silently 0).
try:
    M.run_singular("ring zzr = 0,(zzv0),dp;\nideal zzI = zzv0^2;\n"
                   "list zzL = sat(zzI,zzv0);\nquit;\n")
    expect("S2 sat without elim.lib raises", "no-raise", "raise")
except M.SingularError:
    expect("S2 sat without elim.lib raises", "raise", "raise")

# S3  LEDGER 13: shadowing guard.
try:
    M.check_no_shadowing(["zzv1", "zzg2"], ["zzg1", "zzg2"])
    expect("S3 shadowing guard raises on clash", "no-raise", "raise")
except M.SingularError:
    expect("S3 shadowing guard raises on clash", "raise", "raise")
expect("S3b shadowing guard passes on disjoint prefixes",
       M.check_no_shadowing(["zzv1", "zzv2"], ["zzg1", "zzg2"]), 0)

# S4  unit-ideal detection: (x, x-1) is the unit ideal.
o, st = M.run_singular('LIB "elim.lib";\nring zzr = 0,(zzv0,zzv1),dp;\n'
                       'ideal zzI = zzv0,zzv0-1;\nideal zzS = std(zzI);\n'
                       '"MARK_UNIT0";\nreduce(1,zzS);\nquit;\n')
expect("S4 unit ideal detected", o.split("MARK_UNIT0")[1].strip(), "0")

# S5  NON-unit must NOT be reported as unit  (false-kill control at harness
#     level): (x*y) saturated by x is (y), which is not the unit ideal.
o, st = M.run_singular('LIB "elim.lib";\nring zzr = 0,(zzv0,zzv1),dp;\n'
                       'ideal zzI = zzv0*zzv1;\nideal zzS = std(zzI);\n'
                       'list zzL = sat(zzS,zzv0);\nzzS = std(zzL[1]);\n'
                       '"MARK_UNIT0";\nreduce(1,zzS);\nquit;\n')
# reduce(1,S) prints the REMAINDER: 0 <=> unit ideal, 1 <=> not unit.
expect("S5 sat(xy,x)=(y) is NOT unit",
       o.split("MARK_UNIT0")[1].strip().split()[0], "1")

# S6  saturation really saturates: sat(x^2, x) = (1).
o, st = M.run_singular('LIB "elim.lib";\nring zzr = 0,(zzv0,zzv1),dp;\n'
                       'ideal zzI = zzv0^2;\nideal zzS = std(zzI);\n'
                       'list zzL = sat(zzS,zzv0);\nzzS = std(zzL[1]);\n'
                       '"MARK_UNIT0";\nreduce(1,zzS);\nquit;\n')
expect("S6 sat(x^2,x) IS unit", o.split("MARK_UNIT0")[1].strip(), "0")

# S7  a genuinely nonempty all-nonzero variety must survive saturation:
#     x*y-1 = 0 has solutions with x,y != 0.
o, st = M.run_singular('LIB "elim.lib";\nring zzr = 0,(zzv0,zzv1),dp;\n'
                       'ideal zzI = zzv0*zzv1-1;\nideal zzS = std(zzI);\n'
                       'list zzL = sat(zzS,zzv0);\nzzS = std(zzL[1]);\n'
                       'zzL = sat(zzS,zzv1);\nzzS = std(zzL[1]);\n'
                       '"MARK_UNIT0";\nreduce(1,zzS);\nquit;\n')
expect("S7 feasible xy=1 survives saturation (no false kill)",
       o.split("MARK_UNIT0")[1].strip(), "1")

# S8  LEDGER 6: leading unary + must be rejected by the script scanner.
try:
    M.scan_script("ring zzr = 0,(zzv0),dp;\n+zzv0;\nquit;\n", ["zzv0"], [])
    expect("S8 leading-unary-+ rejected", "no-raise", "raise")
except M.SingularError:
    expect("S8 leading-unary-+ rejected", "raise", "raise")

# S9  sing_poly never emits a leading '+' and encodes coefficients correctly.
nm = {("a",): "zza", ("b",): "zzb"}
p = {(("a",), ("b",)): 3, (("a",),): -1, (): 2}
expect("S9 sing_poly output", M.sing_poly(p, nm), "2-zza+3*zza*zzb")
expect("S9b sing_poly has no leading +",
       M.sing_poly({(("a",),): 1}, nm), "zza")

json.dump(out, open("results_smoke.json", "w"), indent=1)
print("\nSMOKE: %d failures" % len(fails))
if fails:
    sys.exit(1)
