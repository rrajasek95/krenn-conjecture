#!/usr/bin/env python3
"""Find a fixed-core rate certificate numerically; acceptance is exact.

Requires NumPy only for discovery. The core and verify modules use
the standard library. A search failure is not an impossibility certificate.
"""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import numpy as np
import core


def number(z):
    return complex(float(z.re), float(z.im))


def find(payload, floor):
    data = core.matrices(core.read_source(payload['core']), payload['root'])
    maximum = core.fidelity_ceiling(data)
    core.require(0 < floor < maximum, 'Search requires a floor strictly below the exact ceiling')
    K = np.array([[number(z) for z in row] for row in data['K']])
    U = np.array([[number(z) for z in row] for row in data['U']])
    # A small fidelity margin lets rational rounding retain feasibility.
    work_floor = floor + min(Q(1, 10**10), (maximum-floor)/100)
    D = U-float(work_floor)*K
    def top(mu):
        vals, vecs = np.linalg.eigh(K+mu*D)
        return vals, vecs
    def slope(mu):
        _, vecs = top(mu)
        v = vecs[:, -1]
        return (v.conj()@D@v).real
    lo, hi = 0., 1.
    while slope(hi) < 0:
        hi *= 2
        core.require(hi < 1e16, 'Search multiplier limit; no certificate found')
    for _ in range(100):
        mid=(lo+hi)/2
        if slope(mid) < 0: lo=mid
        else: hi=mid
    numeric_mu=hi
    vals, vecs=top(numeric_mu)
    # At a corner, mix within the nearly maximal eigenspace to satisfy the
    # active fidelity constraint. Exact verification below controls rounding.
    tol=1e-10*max(1.,abs(vals[-1]))
    space=vecs[:,vals >= vals[-1]-tol]
    dv,directions=np.linalg.eigh(space.conj().T@D@space)
    directions=space@directions
    if dv[0] < 0 < dv[-1]:
        weight=-dv[0]/(dv[-1]-dv[0])
        vector=np.sqrt(weight)*directions[:,-1]+np.sqrt(1-weight)*directions[:,0]
    else:
        vector=directions[:,-1]
    scale = 10**12
    witness = [core.encode(core.C(Q(round(z.real*scale), scale), Q(round(z.imag*scale), scale)))
               for z in vector]
    mu = Q(round(numeric_mu*10**8), 10**8)
    original = U-float(floor)*K
    top = np.linalg.eigvalsh(K+float(mu)*original)[-1]
    upper = Q(int(np.ceil(top*10**12))+100, 10**12)
    out = {**payload, 'fidelity_floor': str(floor), 'mu': str(mu),
           'upper_eigenvalue': str(upper), 'witness': witness}
    receipt = core.verify_certificate(out)
    return out, receipt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('core', type=Path)
    p.add_argument('--fidelity', required=True, type=Q)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    payload, result = find(json.loads(args.core.read_text()), args.fidelity)
    with args.output.open('x') as handle:
        json.dump(payload, handle, indent=2)
        handle.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
