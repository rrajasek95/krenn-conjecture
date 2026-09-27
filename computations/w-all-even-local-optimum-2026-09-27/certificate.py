"""Compare every coefficient of the universal second-variation formulas."""

from fractions import Fraction as Q
from itertools import combinations
from derivatives import require, rational_rank


def linear(*terms):
    result = {}
    for coefficient, form in terms:
        for key, value in form.items():
            result[key] = result.get(key, Q(0))+coefficient*value
    return {k: v for k, v in result.items() if v}


def add_product(poly, coefficient, a, b):
    for i, x in a.items():
        for j, y in b.items():
            key = tuple(sorted((i, j)))
            poly[key] = poly.get(key, Q(0))+coefficient*x*y


def clean(poly):
    return {k: v for k, v in poly.items() if v}


def zero_sum_forms(N, counter):
    result = []
    for _ in range(N-1):
        result.append({counter[0]: Q(1)})
        counter[0] += 1
    result.append(linear(*[(-1, f) for f in result]))
    return result


def tangent(N, cells):
    core = range(1, N+1)
    edges = list(combinations(core, 2))
    counter = [0]
    d = {}
    for edge in edges:
        d[edge] = {counter[0]: Q(1)}
        counter[0] += 1
    v = dict(zip(core, zero_sum_forms(N, counter)))
    z = dict(zip(core, zero_sum_forms(N, counter)))
    K = {}
    for i, j in edges:
        K[i, j] = {counter[0]: Q(1)}
        K[j, i] = {counter[0]: Q(-1)}
        counter[0] += 1
    s = {i: linear(*[(Q(2, 4-N), K[i, j]) for j in core if j != i]) for i in core}
    U = {(i, j): linear((Q(1, 2), s[i]), (Q(1, 2), s[j]), (1, K[i, j]))
         for i in core for j in core if i != j}
    D = linear(*[(1, f) for f in d.values()])
    t = {i: linear(*[(1, f) for edge, f in d.items() if i in edge]) for i in core}
    a = {i: linear((1, D), (-1, t[i])) for i in core}
    x = {i: linear((Q(-N, N-2), a[i])) for i in core}
    y = {i: linear((Q(-1, N), D), (1, v[i])) for i in core}
    source = []
    for i, j, first, second in cells:
        if i == 0:
            source.append(z[j] if (first, second) == (0, 0) else
                          x[j] if (first, second) == (0, 1) else
                          y[j] if (first, second) == (1, 0) else linear((-1, s[j])))
        else:
            source.append(d[i, j] if (first, second) == (0, 0) else
                          U[i, j] if (first, second) == (1, 0) else
                          U[j, i] if (first, second) == (0, 1) else {})
    alpha = linear((Q(2, N*(N-1)), D))
    u = {i: linear((Q(1, N-2), t[i]), (Q(-(N-1), N-2), alpha)) for i in core}
    h = {(i, j): linear((1, d[i, j]), (-1, alpha), (-1, u[i]), (-1, u[j]))
         for i, j in edges}
    K0 = {(i, j): linear((1, K[i, j]), (Q(N-4, 2*N), s[i]), (Q(4-N, 2*N), s[j]))
          for i in core for j in core if i != j}
    require(not linear(*[(1, f) for f in s.values()]), "Excitation row sums have total zero")
    require(not linear(*[(1, f) for f in u.values()]), "Standard core component has sum zero")
    require(all(not linear(*[(1, f) for edge, f in h.items() if i in edge]) for i in core),
            "Residual core component has zero rows")
    require(all(not linear(*[(1, K0[i, j]) for j in core if j != i]) for i in core),
            "Residual antisymmetric component has zero rows")
    return dict(source=source, dimension=counter[0], alpha=alpha, u=u, v=v,
                h=h, z=z, s=s, K0=K0)


def check(data):
    N, g = data["N"], data["N"]**2+1
    t = tangent(N, data["cells"])
    source = t["source"]
    require(t["dimension"] == N*(N+1)-2, "Complete tangent parameter count")
    require(rational_rank(source) == t["dimension"], "Tangent parameterization is injective")
    require(all(not linear(*[(coefficient, source[j]) for j, coefficient in row.items()])
                for row in data["jacobian"].values()), "All tangent directions annihilate every output")
    G, B = {}, {}
    for weight, form in zip(data["metric"], source):
        add_product(G, weight, form, form)
    for (i, j), value in data["hessian"].items():
        add_product(B, 2*value, source[i], source[j])
    A = N*N*(N-1)+N-2
    kappa = Q(g*(N*N-5*N+8), N)-(N*N-1)
    h_real, h_imag = Q(g*(N-3), N-2), Q(g*(N-1), N-2)
    real, imag = {}, {}
    add_product(real, Q(g*N*(N*N-1), 2), t["alpha"], t["alpha"])
    for i in range(1, N+1):
        plus = linear((1, t["u"][i]), (1, t["v"][i]))
        minus = linear((1, t["u"][i]), (-1, t["v"][i]))
        add_product(real, 1, plus, plus)
        add_product(real, 2*A-2, t["u"][i], t["u"][i])
        add_product(imag, 1, minus, minus)
        zp = linear((1, t["z"][i]), (N, t["s"][i]))
        zm = linear((1, t["z"][i]), (-N, t["s"][i]))
        add_product(real, 1, zp, zp)
        add_product(imag, 1, zm, zm)
        add_product(real, kappa, t["s"][i], t["s"][i])
        add_product(imag, kappa, t["s"][i], t["s"][i])
    for form in t["h"].values():
        add_product(real, h_real, form, form)
        add_product(imag, h_imag, form, form)
    for form in t["K0"].values():
        add_product(real, g, form, form)
        add_product(imag, g, form, form)
    require(clean(real) == linear((1, G), (-1, B)), "Every real second-variation coefficient")
    require(clean(imag) == linear((1, G), (1, B)), "Every imaginary second-variation coefficient")
    if N >= 5:
        shift = N-5
        require(kappa == Q(shift**4+14*shift**3+69*shift**2+136*shift+88, N) > 0,
                "Positive all-size coefficient")
        require(h_real > 0 and h_imag > 0 and 2*A-2 > 0, "Other positive coefficients")
    else:
        require(N == 3 and kappa == Q(-4, 3), "Four-site exception is retained")
        require(all(not form for form in t["h"].values()), "No residual core mode at four sites")
    # Verify all independent fixed-output site phases directly in source coordinates.
    gauges = []
    for i in range(1, N+1):
        theta = [-1]+[int(j == i) for j in range(1, N+1)]
        vector = {(j): (theta[u]+theta[v])*z
                  for j, ((u, v, a, b), z) in enumerate(zip(data["cells"], data["base"]))
                  if (theta[u]+theta[v])*z}
        require(all(sum(value*vector.get(j, 0) for j, value in row.items()) == 0
                    for row in data["jacobian"].values()), "Phase tangent preserves output")
        value = sum(weight*vector.get(j, 0)**2 for j, weight in enumerate(data["metric"]))
        value += sum(2*b*vector.get(i, 0)*vector.get(j, 0)
                     for (i, j), b in data["hessian"].items())
        require(value == 0, "Phase tangent is in the imaginary nullspace")
        gauges.append(vector)
    require(rational_rank(gauges) == N, "All phase directions are independent")
    return dict(sites=N+1, binary_cells=len(source), jacobian_rank=data["rank"],
                tangent_complex_dimension=t["dimension"], phase_dimension=N,
                kappa=str(kappa), residual_real_coefficient=str(h_real),
                residual_imaginary_coefficient=str(h_imag),
                compared_quadratic_coefficients=len(set(G)|set(B)),
                second_variation="positive modulo phases" if N >= 5 else
                "indefinite; higher output constraints needed")
