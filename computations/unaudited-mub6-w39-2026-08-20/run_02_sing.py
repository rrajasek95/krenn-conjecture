"""W39 (UNAUDITED, scoping): seconds-scale Singular feasibility probe on the
MU-VECTOR system V(H) for H = S_6 (Tao) and H = F_6 (Fourier).

MODEL (sound-for-nonexistence relaxation).  A vector MU to the standard
basis is v = (1/sqrt6)(1, z2,...,z6) with |z_j| = 1.  Unbiasedness to the
basis of H is |sum_j conj(H_{jk}) z_j|^2 = 6 for k = 1..6.  Substituting
conj(z_j) = y_j and imposing z_j y_j = 1 gives BILINEAR equations over the
cyclotomic ring.  On the torus y_j = conj(z_j) this is EXACTLY the MU
condition; off the torus the complex variety is strictly larger.  Hence:

    unit ideal  =>  NO MU vector exists         (SOUND)
    nonempty V  =>  says nothing by itself      (hazard 18)

Ledger compliance: generators are prefixed zzg (hazard 13, no shadowing);
stdout is parsed for '?' lines (hazards 6/11/22); coefficients are integral
so no rational-printing hazard (22).
"""
import json
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

S_EXP = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 2, 2],
    [0, 1, 0, 2, 2, 1],
    [0, 1, 2, 0, 1, 2],
    [0, 2, 2, 1, 0, 1],
    [0, 2, 1, 2, 1, 0],
]
# F_6 exponent matrix in 6th roots of unity
F_EXP = [[(i * j) % 6 for j in range(6)] for i in range(6)]


def emit(exp, order, tag):
    """Emit a Singular script for the MU-vector ideal of the Butson matrix
    with exponent matrix `exp` in `order`-th roots of unity."""
    n = 6
    # minimal polynomial of a primitive `order` root of unity
    minpoly = {3: "xx^2+xx+1", 6: "xx^2-xx+1"}[order]
    zs = [f"z{j}" for j in range(1, n)]      # z1..z5  <->  entries 2..6
    ys = [f"y{j}" for j in range(1, n)]
    var = ",".join(zs + ys)
    L = []
    L.append(f'ring zzR = (0,xx),({var}),dp;')
    L.append(f'minpoly = {minpoly};')
    Zsym = ["1"] + zs
    Ysym = ["1"] + ys
    gens = []
    for k in range(n):
        A = "+".join(f"xx^{(-exp[j][k]) % order}*({Zsym[j]})" for j in range(n))
        B = "+".join(f"xx^{exp[j][k] % order}*({Ysym[j]})" for j in range(n))
        gens.append(f"({A})*({B})-6")
    for j in range(1, n):
        gens.append(f"{Zsym[j]}*{Ysym[j]}-1")
    for i, g in enumerate(gens):
        L.append(f"poly zzg{i} = {g};")
    L.append("ideal zzI = " + ",".join(f"zzg{i}" for i in range(len(gens))) + ";")
    L.append("option(redSB);")
    L.append("ideal zzG = std(zzI);")
    L.append('"TAG %s";' % tag)
    L.append('"ngens"; size(zzG);')
    L.append('"dim"; dim(zzG);')
    L.append('"vdim"; vdim(zzG);')
    L.append('"isunit"; (zzG[1]==1);')
    L.append("quit;")
    return "\n".join(L) + "\n"


def run(script, name, timeout=50):
    path = os.path.join(HERE, name)
    with open(path, "w") as fh:
        fh.write(script)
    try:
        p = subprocess.run(["Singular", "-q", path], capture_output=True,
                           text=True, timeout=timeout)
        out, err, rc, to = p.stdout, p.stderr, p.returncode, False
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        err, rc, to = "TIMEOUT", -1, True
    qlines = [l for l in out.splitlines() if l.strip().startswith("?")]
    return {"script": name, "returncode": rc, "timeout": to,
            "singular_error_lines": qlines, "stdout": out, "stderr": err}


if __name__ == "__main__":
    res = {}
    res["S6"] = run(emit(S_EXP, 3, "S6"), "sing_S6.sing")
    res["F6"] = run(emit(F_EXP, 6, "F6"), "sing_F6.sing")
    for k, v in res.items():
        print("=" * 20, k, "=" * 20)
        print("rc", v["returncode"], "timeout", v["timeout"],
              "errlines", v["singular_error_lines"])
        print(v["stdout"][-1500:])
    with open(os.path.join(HERE, "results_t2.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    # control manifest (hazard 21): assert both probes actually ran
    assert set(res) == {"S6", "F6"}, "control manifest mismatch"
    print("CONTROL MANIFEST OK: ran", sorted(res))
