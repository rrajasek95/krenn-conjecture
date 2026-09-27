"""Exact examples for the connected-cofactor W reduction and its norm bound."""
from itertools import combinations, product
from shared import *


def fixture(kind, branch):
    # Roots 0,1, core 2..5. The cofactor graph is a connected K2,2.
    D = {(2, 4): ONE, (2, 5): 2*OMEGA,
         (3, 4): 3*OMEGA*OMEGA, (3, 5): E(5)}
    vertices = tuple(range(2, 6))
    C = [[ZERO if i == j else hafnian(D, tuple(v for v in vertices if v not in (i, j)))
          for j in vertices] for i in vertices]
    tau = hafnian(D, vertices)
    require(tau == E(11), 'Exact core hafnian')
    sign = [1, 1, -1, -1]
    require(all((sign[i]+sign[j])*C[i][j] == ZERO for i, j in product(range(4), repeat=2)),
            'C anticommutes with the bipartition signs')
    u = [E(1+i, (i % 2)+1) for i in range(4)]
    target = [ONE/z for z in u]
    z = solve(C, target)
    r = E(Q(3, 4))*OMEGA if kind == 'mixed' else ZERO
    k, root_k = Q(1)+r.abs2(), Q(5, 4) if r else Q(1)
    require(root_k**2 == k, 'Exact norm-balancing square root')
    slack = [E(Q(i+1, 7), Q(1-i, 9)) for i in range(4)]
    if r:
        x = [-r.conjugate()*s*v/k+h for s, v, h in zip(sign, z, slack)]
        y = [v/k+r*s*h for s, v, h in zip(sign, z, slack)]
    else:
        x, y = slack, z
    v = [r*s*a for s, a in zip(sign, u)]
    alpha = E(1, 1) if branch == 'left' and r else ZERO
    beta = E(2, 1) if branch == 'right' else ZERO
    d = [alpha*a for a in u]
    e = [beta*s*a for s, a in zip(sign, u)]
    srow = [alpha*s*a/r for s, a in zip(sign, y)] if r else [ZERO]*4
    trow = [beta*s*a for s, a in zip(sign, x)]
    source = {(i, j, 0, 0): weight for (i, j), weight in D.items()}
    for i, xx, uu, ss, dd, yy, vv, tt, ee in zip(vertices, x, u, srow, d, y, v, trow, e):
        for root, row in ((0, (xx, uu, ss, dd)), (1, (yy, vv, tt, ee))):
            for (a, b), weight in zip(product(range(2), repeat=2), row):
                source[root, i, a, b] = weight
    source[0, 1, 0, 0] = -dot(x, mv(C, y))/tau
    source[0, 1, 1, 0] = source[0, 1, 0, 1] = ONE/tau
    source[0, 1, 1, 1] = ZERO
    expected = {tuple(int(i == j) for j in range(6)): ONE for i in range(6)}
    require(outputs(source) == expected, 'Original source has all six W amplitudes and no other output')
    if r:
        reduced = {(i, j, 0, 0): weight for (i, j), weight in D.items()}
        for i, uu, zz in zip(vertices, u, z):
            reduced[0, i, 0, 1] = root_k*uu
            reduced[1, i, 0, 0] = zz/root_k
        reduced[0, 1, 1, 0] = reduced[0, 1, 0, 1] = ONE/tau
        defect = sum(a.abs2() for a in x+y)-sum(a.abs2() for a in z)/k
        require(defect == k*sum(a.abs2() for a in slack), 'Exact sum-of-squares norm deficit')
    else:
        reduced = {c: weight for c, weight in source.items()
                   if not (c[0] == 1 and c[2] == 1) and c != (0, 1, 1, 1)}
    require(outputs(reduced) == expected, 'Reduced one-root source preserves all 729 outputs')
    require(energy(reduced) < energy(source), 'Source energy strictly decreases in the fixture')
    if r and branch == 'left':
        wrong = dict(reduced)
        # Retaining u while dividing z by sqrt(k) does not preserve the target.
        wrong[0, 2, 0, 1] /= root_k
        require(outputs(wrong) != expected, 'Unbalanced transformation is rejected')
    return dict(branch=kind+'-'+branch, source_energy=str(energy(source)),
                reduced_energy=str(energy(reduced)), output_words_checked=729)


def verify():
    fixtures = [fixture('mixed', 'left'), fixture('mixed', 'right'), fixture('pure', 'right')]
    # Exhaustive four-vertex support classification used for the six-site closure.
    edges = tuple(combinations(range(4), 2))
    disconnected = []
    for mask in range(1 << len(edges)):
        support = {e for i, e in enumerate(edges) if (mask >> i) & 1}
        components = graphs.components(4, support)
        if any(not any(v in e for e in support) for v in range(4)):
            continue
        if len(components) > 1:
            require(len(support) == 2 and all(sum(v in e for e in support) == 1 for v in range(4)),
                    'Every disconnected four-vertex support without isolated vertices is a perfect matching')
            disconnected.append(mask)
    require(len(disconnected) == 3, 'Three labeled disconnected cofactor supports')
    # Scalar inequalities in the written proof: (1+t)^3 >= 27*t^2/4,
    # with equality at t=2, and (x^2+y^2)(1/x+1/y)^2 >= 8.
    # The first difference is (t-2)^2*(4*t+1)/4.
    def multiply(left, right):
        out = {}
        for a, x in left.items():
            for b, y in right.items():
                key = tuple(i+j for i, j in zip(a, b))
                out[key] = out.get(key, Q(0))+x*y
        return {m: z for m, z in out.items() if z}
    scale_left = {(0,): Q(1), (1,): Q(3), (2,): -Q(15, 4), (3,): Q(1)}
    scale_right = multiply({(0,): Q(4), (1,): -Q(4), (2,): Q(1)},
                           {(0,): Q(1, 4), (1,): Q(1)})
    require(scale_left == scale_right, 'Scale optimization checked as a polynomial identity')
    # Numerator of the second difference is (x-y)^2*(x^2+4*x*y+y^2).
    balance_left = multiply({(2, 0): 1, (0, 2): 1}, {(2, 0): 1, (1, 1): 2, (0, 2): 1})
    balance_left[2, 2] -= 8
    balance_right = multiply({(2, 0): 1, (1, 1): -2, (0, 2): 1},
                             {(2, 0): 1, (1, 1): 4, (0, 2): 1})
    require(balance_left == balance_right, 'Core balancing checked as a polynomial identity')
    require(Q(1, 144) < Q(1, 65), 'Disconnected upper bound is strictly below the attained optimum')
    return dict(fixtures=fixtures, four_site_supports=64, disconnected_without_isolates=len(disconnected),
                disconnected_six_site_upper='1/144', all_two_root_six_site_optimum='1/65',
                all_even_connected_optimum='n*B_n/((n-1)^2+1)',
                negative_control='Unbalanced root transformation REJECTED',
                unresolved='Disconnected cofactor graphs at eight or more sites; unrestricted colored cores')
