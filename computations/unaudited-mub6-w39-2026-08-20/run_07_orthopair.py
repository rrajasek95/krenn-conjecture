"""W39-T1 stage 3: an IDEAL-THEORETIC certificate, independent of the
isolation route.

The clique stage (run_05) proves "no two vectors MU to {I,S_6} are orthogonal"
by certified interval exclusion on 4005 pairs.  That is sound but it is an
enumeration argument.  This script asks for the campaign's NATIVE verdict on
the same statement:

    ORTHOPAIR(H):  u_2..u_6, v_2..v_6   (first MU vector  p)
                   U_2..U_6, V_2..V_6   (second MU vector q)
                   fibre equations for p          (11 equations)
                   fibre equations for q          (11 equations)
                   A(p,q) = 3 + sum_{j>=2} (3 u_j U_j + v_j V_j) = 0
                   B(p,q) =     sum_{j>=2} (   u_j V_j - v_j U_j) = 0

    ORTHOPAIR(H) is the UNIT IDEAL   ==>   no two vectors MU to {I,H} are
    orthogonal, over ANY field of characteristic 0 containing the coefficients
    -- hence in particular over R, hence {I,H} extends to no MUB triple.

20 variables, 24 equations, all of total degree 2, integer coefficients.

CALIBRATION.  The same ideal for H = F_6 must NOT be unit: {I,F_6} does have
orthogonal MU pairs (16 second bases exist).  A pipeline reporting UNIT for
F_6 is broken -- this is the must-SAT control, and it lives outside the
asserted locus exactly as ledger 18 requires.

CHARACTERISTIC DISCIPLINE (ledgers 19/24).  A mod-p unit verdict does NOT
prove the char-0 statement: e.g. (3x-1) is not unit over Q but is unit over
F_3 (bad prime, leading coefficient killed).  F_p runs here are SIZING PROBES
ONLY; the verdict must come from the run over Q.
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mub_systems import fibre_system, S6_EXP, F6_EXP          # noqa: E402

P_VARS = [f"u{j}" for j in range(2, 7)] + [f"v{j}" for j in range(2, 7)]
Q_VARS = [f"U{j}" for j in range(2, 7)] + [f"V{j}" for j in range(2, 7)]


def orthopair_system(exp, order):
    gens_p, _ = fibre_system(exp, order)
    gens_q = []
    for g in gens_p:
        s = g
        for j in range(6, 1, -1):
            s = s.replace(f"u{j}", f"U{j}").replace(f"v{j}", f"V{j}")
        gens_q.append(s)
    A = "3+" + "+".join(f"3*u{j}*U{j}+v{j}*V{j}" for j in range(2, 7))
    B = "+".join(f"u{j}*V{j}-v{j}*U{j}" for j in range(2, 7))
    return gens_p + gens_q + [A, B], P_VARS + Q_VARS


def run(gens, vs, char, tag, timeout):
    sc = [f'ring zzR = {char},({",".join(vs)}),dp;',
          "option(redSB);",
          "ideal zzI = " + ",".join(f"({g})" for g in gens) + ";",
          "ideal zzG = std(zzI);",
          '"ZZISUNIT"; string(zzG[1]==1);',
          '"ZZDIM"; string(dim(zzG));',
          '"ZZSIZE"; string(size(zzG));',
          "quit;"]
    path = os.path.join(HERE, f"op_{tag}.sing")
    with open(path, "w") as fh:
        fh.write("\n".join(sc) + "\n")
    t0 = time.time()
    try:
        p = subprocess.run(["Singular", "-q", path], capture_output=True,
                           text=True, timeout=timeout)
        out, rc, to = p.stdout, p.returncode, False
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        rc, to = -1, True
    errs = [l for l in out.splitlines() if l.strip().startswith("?")]
    txt = [l.strip() for l in out.splitlines() if l.strip()]
    rec = {"tag": tag, "char": char, "timeout": to, "returncode": rc,
           "singular_error_lines": errs, "wall_seconds": round(time.time() - t0, 1)}
    if to:
        rec["status"] = "UNCHECKED_TIMEOUT"          # ledger 23
    elif errs:
        rec["status"] = "SINGULAR_ERROR"
    else:
        try:
            rec["is_unit"] = (txt[txt.index("ZZISUNIT") + 1] == "1")
            rec["dim"] = int(txt[txt.index("ZZDIM") + 1])
            rec["gb_size"] = int(txt[txt.index("ZZSIZE") + 1])
            rec["status"] = "UNIT" if rec["is_unit"] else "NONUNIT"
        except Exception:
            rec["status"] = "PARSE_FAIL"
            rec["stdout_tail"] = txt[-6:]
    return rec


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "probe"
    out = {}
    ck = os.path.join(HERE, f"results_t6_orthopair_{which}.json")
    if which == "probe":
        jobs = [("S6", S6_EXP, 3, 32003, 300), ("F6", F6_EXP, 6, 32003, 300),
                ("S6", S6_EXP, 3, 1000003, 300), ("F6", F6_EXP, 6, 1000003, 300)]
    else:
        jobs = [("S6", S6_EXP, 3, 0, 100000), ("F6", F6_EXP, 6, 0, 100000)]
    executed = []
    for name, exp, order, ch, to in jobs:
        gens, vs = orthopair_system(exp, order)
        tag = f"{name}_c{ch}"
        print(f"[run ] ORTHOPAIR {tag}: {len(vs)} vars, {len(gens)} eqs",
              flush=True)
        r = run(gens, vs, ch, tag, to)
        out[tag] = r
        executed.append(tag)
        print(f"[done] {tag}: {r['status']} "
              f"dim={r.get('dim')} gb={r.get('gb_size')} "
              f"({r['wall_seconds']}s)", flush=True)
        with open(ck, "w") as fh:
            json.dump(out, fh, indent=2, default=str)
    print("CONTROL MANIFEST OK:", executed, flush=True)
    if which != "probe":
        s = out.get("S6_c0", {})
        f = out.get("F6_c0", {})
        print("\nVERDICT READ (char 0 only):")
        print("  S6 ORTHOPAIR:", s.get("status"),
              "-> UNIT would prove no orthogonal MU pair, hence no MUB triple")
        print("  F6 ORTHOPAIR:", f.get("status"),
              "-> must be NONUNIT (must-SAT control)")


if __name__ == "__main__":
    main()
