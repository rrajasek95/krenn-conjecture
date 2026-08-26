"""W39 (UNAUDITED, scoping): the COMPACT MU-vector model -- 5 unimodular
variables + 1 Rabinowitsch saturation variable, i.e. the model used by
Szollosi (arXiv:2405.09991) for order-6 CHM classification.

conj(z_j) = 1/z_j is substituted directly and denominators cleared by
Z = z2*z3*z4*z5*z6; saturation is enforced by u*Z - 1 = 0.
Same soundness caveat as run_02: the complex variety is a RELAXATION of
the torus condition (unit ideal => nonexistence; nonempty => nothing).

Ledger: zzg prefix (13), '?'-parse (6/11), integral coefficients (22),
control manifest at exit (21).
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

S_EXP = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 2, 2],
    [0, 1, 0, 2, 2, 1],
    [0, 1, 2, 0, 1, 2],
    [0, 2, 2, 1, 0, 1],
    [0, 2, 1, 2, 1, 0],
]
F_EXP = [[(i * j) % 6 for j in range(6)] for i in range(6)]


def emit(exp, order, tag, char=0):
    n = 6
    minpoly = {3: "xx^2+xx+1", 6: "xx^2-xx+1"}[order]
    zs = [f"z{j}" for j in range(1, n)]
    var = ",".join(zs + ["u"])
    L = [f'ring zzR = ({char},xx),({var}),dp;', f'minpoly = {minpoly};']
    Zsym = ["1"] + zs
    Zprod = "*".join(zs)
    gens = []
    for k in range(n):
        A = "+".join(f"xx^{(-exp[j][k]) % order}*({Zsym[j]})" for j in range(n))
        # sum_j H_{jk} / z_j  times  Zprod   ->   sum_j H_{jk} * (Zprod/z_j)
        terms = []
        for j in range(n):
            if j == 0:
                terms.append(f"xx^{exp[j][k] % order}*({Zprod})")
            else:
                rest = "*".join(z for z in zs if z != Zsym[j])
                terms.append(f"xx^{exp[j][k] % order}*({rest})")
        B = "+".join(terms)
        gens.append(f"({A})*({B})-6*({Zprod})")
    gens.append(f"u*({Zprod})-1")
    for i, g in enumerate(gens):
        L.append(f"poly zzg{i} = {g};")
    L.append("ideal zzI = " + ",".join(f"zzg{i}" for i in range(len(gens))) + ";")
    L.append("option(redSB);")
    L.append("ideal zzG = std(zzI);")
    L.append(f'"TAG {tag}";')
    L.append('"ngens"; size(zzG);')
    L.append('"dim"; dim(zzG);')
    L.append('"vdim"; vdim(zzG);')
    L.append('"isunit"; (zzG[1]==1);')
    L.append("quit;")
    return "\n".join(L) + "\n"


def run(script, name, timeout=48):
    path = os.path.join(HERE, name)
    with open(path, "w") as fh:
        fh.write(script)
    try:
        p = subprocess.run(["Singular", "-q", path], capture_output=True,
                           text=True, timeout=timeout)
        out, rc, to = p.stdout, p.returncode, False
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        rc, to = -1, True
    q = [l for l in out.splitlines() if l.strip().startswith("?")]
    return {"script": name, "returncode": rc, "timeout": to,
            "singular_error_lines": q, "stdout": out}


if __name__ == "__main__":
    res = {}
    res["F6_charQ"] = run(emit(F_EXP, 6, "F6_charQ"), "c_F6_Q.sing")
    res["S6_charQ"] = run(emit(S_EXP, 3, "S6_charQ"), "c_S6_Q.sing")
    # multi-characteristic sizing probes (ledger 19: NOT verdicts over Q)
    res["F6_char7"] = run(emit(F_EXP, 6, "F6_char7", char=7), "c_F6_7.sing")
    res["S6_char7"] = run(emit(S_EXP, 3, "S6_char7", char=7), "c_S6_7.sing")
    for k, v in res.items():
        print("=" * 16, k, "rc", v["returncode"], "timeout", v["timeout"],
              "err", v["singular_error_lines"])
        print(v["stdout"].strip()[-400:])
    with open(os.path.join(HERE, "results_t3.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    assert set(res) == {"F6_charQ", "S6_charQ", "F6_char7", "S6_char7"}, \
        "control manifest mismatch"
    print("CONTROL MANIFEST OK:", sorted(res))
