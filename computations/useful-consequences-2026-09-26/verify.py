#!/usr/bin/env python3
"""Exact finite checks; the accompanying all-order written proofs are not automated.

Python 3.10+, standard library only. No asserts: checks remain active under -O.
"""

import argparse
import copy
import csv
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from random import Random

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
COLORS = "abc"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    p = vertices[0]
    for j in range(1, len(vertices)):
        t = vertices[j]
        rest = vertices[1:j] + vertices[j + 1:]
        for matching in perfect_matchings(rest):
            yield ((p, t),) + matching


def tensor(vertices, edges):
    """Full coefficient expansion; each edge contains endpoint-colored cells."""
    answer = defaultdict(Q)
    positions = {v: i for i, v in enumerate(vertices)}
    for matching in perfect_matchings(tuple(vertices)):
        cells = [edges.get(tuple(sorted(pair)), ()) for pair in matching]
        for selected in itertools.product(*cells):
            word = [""] * len(vertices)
            value = Q(1)
            for (p, t), (a, b, weight) in zip(matching, selected):
                word[positions[p]], word[positions[t]] = a, b
                value *= weight
            answer[tuple(word)] += value
    return {word: value for word, value in answer.items() if value}


def norm2(coefficients):
    # All finite controls here have real rational coefficients. Written proofs
    # use complex absolute squares and do not depend on that specialization.
    return sum((v * v for v in coefficients.values()), Q(0))


def project(edges, palette):
    return {pair: tuple(cell for cell in cells
                        if cell[0] in palette and cell[1] in palette)
            for pair, cells in edges.items()}


def scalar_permanent(U, T, weights):
    return sum((product(weights[tuple(sorted((u, t)))]
                        for u, t in zip(U, perm))
                for perm in itertools.permutations(T)), Q(0))


def product(values):
    result = Q(1)
    for value in values:
        result *= value
    return result


def bipartite(n, pairs):
    adjacency = [set() for _ in range(n)]
    for a, b in pairs:
        adjacency[a].add(b)
        adjacency[b].add(a)
    labels = {}
    for root in range(n):
        if root in labels:
            continue
        labels[root] = 0
        stack = [root]
        while stack:
            p = stack.pop()
            for t in adjacency[p]:
                if t in labels:
                    if labels[p] == labels[t]:
                        return False
                else:
                    labels[t] = 1 - labels[p]
                    stack.append(t)
    return True


def check_prism(model):
    require(model["sites"] == 6, "prism must have six sites")
    edges = model["edges"]
    pairs = [tuple(e["ends"]) for e in edges]
    require(len(edges) == 9 and len(set(pairs)) == 9, "nine distinct edges")
    require(all(0 <= p < t < 6 for p, t in pairs), "canonical edge endpoints")
    require(all(e["color"] in COLORS and e["omega_power"] in (0, 1)
                for e in edges), "invalid edge data")
    modes = [(v, e["color"]) for e in edges for v in e["ends"]]
    require(len(set(modes)) == 18, "pair sources must use disjoint optical modes")
    require(not bipartite(6, pairs), "prism must not fall under bipartite exclusion")
    lookup = {pair: i for i, pair in enumerate(pairs)}
    recursive = set()
    output = defaultdict(Counter)
    for matching in perfect_matchings(tuple(range(6))):
        if not all(pair in lookup for pair in matching):
            continue
        indices = tuple(sorted(lookup[pair] for pair in matching))
        recursive.add(indices)
        word = [""] * 6
        omega_power = 0
        for i in indices:
            edge = edges[i]
            for v in edge["ends"]:
                word[v] = edge["color"]
            omega_power += edge["omega_power"]
        output["".join(word)][omega_power] += 1
    subsets = {indices for indices in itertools.combinations(range(9), 3)
               if sorted(v for i in indices for v in pairs[i]) == list(range(6))}
    require(recursive == subsets and len(subsets) == 4, "matching enumerations disagree")
    expected = {word: Counter({power: 1})
                for word, power in model["expected_output_omega_powers"].items()}
    require(dict(output) == expected, "matching output differs from the stated formula")

    # Independent Fock occupancy enumeration. A source emitting >=2 pairs
    # necessarily puts >=2 photons at each of its endpoint sites. Checking
    # occupations 0,1,2 verifies the finite boundary; that monotonicity proves
    # that every still higher occupation also fails exact one-per-site selection.
    accepted = set()
    for occupation in itertools.product(range(3), repeat=9):
        counts = [0] * 6
        for i, count in enumerate(occupation):
            for v in pairs[i]:
                counts[v] += count
        if counts == [1] * 6:
            require(max(occupation) == 1, "multipair emission passed selection")
            accepted.add(tuple(i for i, count in enumerate(occupation) if count))
    require(accepted == subsets, "Fock selection differs from matching expansion")

    for t, omega in [(Q(1, 3), Q(1, 2)), (Q(1, 2), Q(2, 3)), (Q(1, 4), Q(3, 2))]:
        amplitudes = [t * omega ** e["omega_power"] for e in edges]
        require(all(0 < a < 1 for a in amplitudes), "invalid squeezing amplitude")
        actual = tensor(tuple(range(6)), {
            tuple(e["ends"]): ((e["color"], e["color"], a),)
            for e, a in zip(edges, amplitudes)})
        strength = norm2(actual)
        pure_sum = sum((actual.get(tuple(c * 6), Q(0)) for c in COLORS), Q(0))
        fidelity = pure_sum ** 2 / (3 * strength)
        s, x = t * t, omega * omega
        require(fidelity == 3 / (3 + x * x), "fidelity normalization")
        vacuum = product(1 - a * a for a in amplitudes)
        fock_probability = sum((product(amplitudes[i] ** 2 for i in indices)
                                for indices in accepted), Q(0)) * vacuum
        formula = s ** 3 * x * (3 + x * x) * (1 - s) ** 6 * (1 - s * x) ** 3
        require(fock_probability == formula == strength * vacuum, "physical probability")
        budget = sum((a * a for a in amplitudes), Q(0))
        require(strength / budget ** 3 == x * (3 + x * x) / (27 * (2 + x) ** 3),
                "fixed-budget generation strength")
        require(strength != fock_probability, "vacuum-normalization fault must be visible")
    return {"perfect_matchings": len(subsets), "fock_occupancies_checked": 3 ** 9,
            "output": {word: dict(terms) for word, terms in sorted(output.items())}}


# Sparse exact polynomials in s,x. This checks the derivative as a polynomial
# identity, not by fitting a finite sample of floating-point values.
def add(*polynomials):
    out = defaultdict(Q)
    for polynomial in polynomials:
        for key, value in polynomial.items():
            out[key] += value
    return {key: value for key, value in out.items() if value}


def scale(polynomial, scalar):
    return {key: value * scalar for key, value in polynomial.items() if value * scalar}


def multiply(*polynomials):
    out = {(0, 0): Q(1)}
    for polynomial in polynomials:
        nxt = defaultdict(Q)
        for (a, b), x in out.items():
            for (c, d), y in polynomial.items():
                nxt[a + c, b + d] += x * y
        out = {key: value for key, value in nxt.items() if value}
    return out


def power(polynomial, n):
    return multiply(*([polynomial] * n))


def derivative(polynomial):
    return {(a - 1, b): a * value for (a, b), value in polynomial.items() if a}


def check_optimization():
    one, s, x = {(0, 0): Q(1)}, {(1, 0): Q(1)}, {(0, 1): Q(1)}
    one_s = add(one, scale(s, -1))
    one_sx = add(one, scale(multiply(s, x), -1))
    factor = multiply(x, add(scale(one, 3), power(x, 2)))
    probability = multiply(power(s, 3), factor, power(one_s, 6), power(one_sx, 3))
    quadratic = add(one, scale(s, -3), scale(multiply(s, x), -2),
                    scale(multiply(power(s, 2), x), 4))
    expected_derivative = scale(multiply(power(s, 2), factor, power(one_s, 5),
                                        power(one_sx, 2), quadratic), 3)
    require(derivative(probability) == expected_derivative, "pump derivative identity")
    wrong = add(quadratic, multiply(s, x))
    require(derivative(probability) != scale(multiply(power(s, 2), factor,
            power(one_s, 5), power(one_sx, 2), wrong), 3), "derivative mutation undetected")

    # Unequal weights preserve all three pure amplitudes and the mixed ratio.
    # These exact controls supplement, rather than replace, the Jensen proof.
    s0, x0 = Q(1, 4), Q(1, 4)
    symmetric_vacuum = (1 - s0) ** 6 * (1 - s0 * x0) ** 3
    for ratios in [(Q(2), Q(1), Q(1, 2)), (Q(3, 2), Q(2, 3), Q(1))]:
        triangles, verticals = [], []
        for ratio in ratios:
            group = [s0, s0 / ratio, s0 * x0 * ratio]
            require(product(group) == s0 ** 3 * x0, "balanced amplitude not preserved")
            triangles.extend(group[:2])
            verticals.append(group[2])
        require(product(verticals) == (s0 * x0) ** 3, "mixed ratio not preserved")
        require(all(0 < v < 1 for v in triangles + verticals), "invalid Jensen control")
        require(product(1 - v for v in triangles + verticals) < symmetric_vacuum,
                "symmetric vacuum product failed control")
    return {"exact_polynomial_derivative": "PASS", "unequal_weight_controls": 2}


def check_leakage():
    rng = Random(20260926)
    slices = witnesses = 0
    for n in (4, 6):
        r = n // 2
        U, T = tuple(range(r)), tuple(range(r, n))
        for _ in range(6):
            edges = {(p, t): tuple((c, c, Q(rng.choice((-3, -2, -1, 1, 2, 3))))
                                   for c in COLORS) for p in U for t in T}
            full = tensor(tuple(range(n)), edges)
            mixed_norm = norm2({w: v for w, v in full.items() if len(set(w)) > 1})
            for color in COLORS:
                binary = project(edges, set(COLORS) - {color})
                weights = {pair: next(v for a, b, v in cells if a == b == color)
                           for pair, cells in edges.items()}
                for p in U:
                    D = Q(0)
                    L = Q(0)
                    tau_expansion = Q(0)
                    valid = True
                    for t in T:
                        rest = tuple(v for v in range(n) if v not in (p, t))
                        K = tensor(rest, binary)
                        k2 = norm2(K)
                        q = scalar_permanent(tuple(v for v in U if v != p),
                                             tuple(v for v in T if v != t), weights)
                        actual_slice = {tuple(w[v] for v in rest): value
                                        for w, value in full.items()
                                        if w[p] == w[t] == color
                                        and all(w[v] != color for v in rest)}
                        predicted_slice = {w: weights[p, t] * value for w, value in K.items()}
                        require(actual_slice == predicted_slice, "whole binary slice identity")
                        tau_expansion += weights[p, t] * q
                        L += weights[p, t] ** 2 * k2
                        if k2:
                            D += q * q / k2
                        else:
                            valid = False
                        slices += 1
                    tau = full.get(tuple(color * n), Q(0))
                    require(tau == tau_expansion, "independent permanent expansion")
                    require(L <= mixed_norm, "slice supports must be disjoint")
                    if valid and tau:
                        require(D > 0 and tau * tau <= L * D <= mixed_norm * D,
                                "weighted leakage bound")
                        witnesses += 1

    # Dropping diagonality invalidates the factorization: ab on 03 and ba
    # on 12 produces abab with no aa edge on the opposite-shore pair 02.
    heterogeneous = {(0, 3): (("a", "b", Q(1)),), (1, 2): (("b", "a", Q(1)),)}
    require(tensor((0, 1, 2, 3), heterogeneous) == {tuple("abab"): Q(1)},
            "off-color scope control")
    require((0, 2) not in heterogeneous, "scope control must lack the direct aa edge")
    return {"exact_slice_checks": slices, "nonzero_leakage_witnesses": witnesses,
            "off_color_scope_guard": "PASS"}


def check_boundaries():
    deletion_checks = 0
    for n in (4, 6, 8):
        edges = {}
        for i in range(n):
            pair = tuple(sorted((i, (i + 1) % n)))
            c = COLORS[i % 2]
            edges[pair] = ((c, c, Q(1)),)
        require(bipartite(n, edges), "even cycle must be bipartite")
        require(tensor(tuple(range(n)), edges) == {tuple("a" * n): Q(1), tuple("b" * n): Q(1)},
                "binary sources remain allowed")
        for p in range(0, n, 2):
            for t in range(1, n, 2):
                require(bool(tensor(tuple(v for v in range(n) if v not in (p, t)), edges)),
                        "binary opposite-shore cofactor control")
                deletion_checks += 1
    two = {(0, 1): tuple((c, c, Q(1)) for c in COLORS)}
    require(tensor((0, 1), two) == {tuple(c * 2): Q(1) for c in COLORS}, "two-site boundary")
    k4 = {}
    for c, matching in zip(COLORS, perfect_matchings((0, 1, 2, 3))):
        for pair in matching:
            k4[pair] = ((c, c, Q(1)),)
    require(tensor((0, 1, 2, 3), k4) == {tuple(c * 4): Q(1) for c in COLORS}, "K4 boundary")
    require(not bipartite(4, k4), "four-site exception is nonbipartite")
    return {"binary_cofactor_controls": deletion_checks, "two_site_and_K4_controls": "PASS"}


def calibration():
    rows = []
    with localcontext() as ctx:
        ctx.prec = 70
        for fs in ("0.9", "0.99", "0.999", "0.9999"):
            f = Decimal(fs)
            x = (3 * (1 - f) / f).sqrt()
            s = 2 / (3 + 2 * x + (9 - 4 * x + 4 * x * x).sqrt())
            p = s ** 3 * x * (3 + x * x) * (1 - s) ** 6 * (1 - s * x) ** 3
            require(0 < s < min(Decimal(1), 1 / x), "optimum outside physical domain")
            require(abs(1 - (3 + 2 * x) * s + 4 * x * s * s) < Decimal("1e-65"),
                    "decimal root residual")
            rows.append({"fidelity": fs, "omega": format(x.sqrt(), ".12g"),
                         "triangle_amplitude": format(s.sqrt(), ".12g"),
                         "vertical_amplitude": format((s * x).sqrt(), ".12g"),
                         "ideal_probability": format(p, ".12g"),
                         "expected_trials": format(1 / p, ".12g")})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a new JSON receipt; refuses overwrite")
    parser.add_argument("--calibration", type=Path, help="Write a new rounded calibration CSV")
    args = parser.parse_args()
    dependencies = json.loads((HERE / "dependencies.json").read_text())
    for entry in dependencies:
        actual = hashlib.sha256((ROOT / entry["path"]).read_bytes()).hexdigest()
        require(actual == entry["sha256"], "dependency bytes changed: " + entry["path"])
    model = json.loads((HERE / "prism.json").read_text())
    report = {"status": "PASS", "certification": "NOT INDEPENDENTLY AUDITED OR ADMITTED",
              "scope": "Exact finite identities and controls, plus rounded benchmark calibration; all-order proofs remain written.",
              "dependency_hashes_checked": len(dependencies), "prism": check_prism(model),
              "optimization": check_optimization(), "leakage": check_leakage(),
              "boundaries": check_boundaries()}
    bad = copy.deepcopy(model)
    bad["edges"][0]["omega_power"] = 1
    try:
        check_prism(bad)
    except ValueError:
        report["edge_weight_mutation"] = "REJECTED"
    else:
        raise ValueError("edge-weight mutation was accepted")
    report["calibration"] = calibration()
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        with args.output.open("x") as handle:
            handle.write(payload)
    if args.calibration:
        with args.calibration.open("x", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(report["calibration"][0]))
            writer.writeheader()
            writer.writerows(report["calibration"])
    print(payload, end="")


if __name__ == "__main__":
    main()
