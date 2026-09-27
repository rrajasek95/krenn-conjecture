#!/usr/bin/env python3
"""Exact checks for the written all-even unrestricted local W theorem."""

from fractions import Fraction as Q
from math import comb
from pathlib import Path
import hashlib
import json
import derivatives
import certificate
import four_site
from derivatives import require, double_factorial

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    dependencies = json.loads((HERE/"dependencies.json").read_text())
    for name, digest in dependencies.items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest,
                "Pinned dependency: "+name)
    records, four, negative = [], None, None
    for N in (3, 5, 7, 9, 11):
        data = derivatives.build(N)
        record = certificate.check(data)
        n, m, g = N+1, (N+1)//2, N*N+1
        energy = sum(w*z*z for w, z in zip(data["metric"], data["base"]))
        require(energy == g*N*m, "Physical source strength")
        amplitude_squared = g**(m-1)*double_factorial(N)**2
        rate = Q(n*amplitude_squared, energy**m)
        require(rate == Q(n*double_factorial(N)**2, g*(N*m)**m), "Attained all-even rate")
        record.update(source_strength=str(energy), physical_amplitude_squared=str(amplitude_squared),
                      rate=str(rate))
        records.append(record)
        if N == 3:
            four = four_site.check(data)
        if N == 5:
            corrupt = data | {"hessian": dict(data["hessian"])}
            pair = next(iter(corrupt["hessian"]))
            corrupt["hessian"][pair] += 1
            try:
                certificate.check(corrupt)
            except ValueError as error:
                require(str(error) == "Every real second-variation coefficient",
                        "Mutation rejected at the intended coefficient comparison")
                negative = "REJECTED"
            else:
                raise ValueError("Corrupt Hessian coefficient was accepted")
    # Coefficient identity for N*kappa_N under the shift N=r+5.
    polynomial = [8, -4, 9, -6, 1]
    shifted = [sum(polynomial[i]*comb(i, k)*5**(i-k) for i in range(k, 5))
               for k in range(5)]
    require(shifted == [88, 136, 69, 14, 1] and all(c > 0 for c in shifted),
            "All-size positivity certificate has positive coefficients")
    result = dict(status="PASS",
                  evidence_status="Written proof with exact supporting checks; independent audit pending",
                  finite_derivative_certificates=records, four_site_obstruction=four,
                  all_size_kappa_positive_coefficients=shifted,
                  corrupt_hessian=negative, dependencies=dependencies,
                  theorem="Strict unrestricted local W optimality for every even n >= 4, modulo phases and scaling",
                  unresolved="Global unrestricted W optimality; no explicit neighborhood radius")
    paths = [p for p in HERE.iterdir() if p.suffix in (".py", ".md", ".json")
             and p.name != "results.json"]
    paths += [ROOT/"notes"/name for name in (
        "w-state-all-even-local-optimum-2026-09-27.md",
        "w-state-four-site-local-obstruction-2026-09-27.md")]
    result["sha256"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted(paths)}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
