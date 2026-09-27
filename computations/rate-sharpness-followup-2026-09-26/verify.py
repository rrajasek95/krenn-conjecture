#!/usr/bin/env python3
"""Supporting exact checks, not an independent audit of the analytic proofs.

Python standard library. All pass/fail checks use integers or Q(i).
The optional calibration table uses floating point only for display.
"""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, permutations, product
from math import ceil, cos, factorial, pi, sqrt
from pathlib import Path
import argparse
import csv
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(value, message):
    if not value:
        raise AssertionError(message)


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


general = module('followup_general', 'computations/general-complex-rate-2026-09-26/verify.py')
gate = module('followup_positive', 'computations/universal-rate-gate-2026-09-26/verify.py')
C, ZERO, ONE, Source = general.C, general.ZERO, general.ONE, general.Source


def conjugate(z):
    return C(z.re, -z.im)


def multiply(values):
    result = ONE
    for value in values:
        result *= value
    return result


def even(word):
    return all(word.count(h) % 2 == 0 for h in range(3))


def parity_checks():
    structural = []
    for n in (4, 6):
        count = linear = 0
        for matching in gate.matchings(tuple(range(n))):
            for colors in product(tuple(product(range(3), repeat=2)), repeat=n//2):
                word = [None]*n
                off = 0
                for (p, q), (i, j) in zip(matching, colors):
                    word[p], word[q] = i, j
                    off += i != j
                require(off != 0 or even(word), 'Diagonal term has even color counts')
                if off == 1:
                    require(not even(word), 'Exactly one off-color edge has odd counts')
                    linear += 1
                count += 1
        structural.append(dict(sites=n, assignments=count, linear_terms_removed=linear))

    examples = []
    for name, source, _ in general.sources():
        n, m = source.n, source.n//2
        source_norm = sum(z.abs2() for z in source.cells.values())
        eta2 = sum(z.abs2() for (_, _, i, j), z in source.cells.items() if i != j)
        require(source_norm <= 1, 'Example source normalization')
        residual2 = Q(0)
        matching_list = list(gate.matchings(tuple(range(n))))
        for word in product(range(3), repeat=n):
            coefficients = [ZERO]*(m+1)
            for matching in matching_list:
                off = sum(word[p] != word[q] for p, q in matching)
                coefficients[off] += multiply(source.edge(p, q, word[p], word[q])
                                              for p, q in matching)
            require(sum(coefficients, ZERO) == source.output(word), 'Literal expansion in z')
            if even(word):
                require(not coefficients[1], 'Projected derivative is zero')
                residual2 += sum(coefficients[2:], ZERO).abs2()
            if len(set(word)) == 1:
                require(not any(coefficients[1:]), 'Pure amplitudes preserved')
        if n == 6:
            require(residual2 <= Q(9, 16)*eta2**2, 'Quadratic remainder bound on example')
        examples.append(dict(case=name, off_color_norm_squared=str(eta2),
                             projected_remainder_squared=str(residual2)))
    return dict(structural=structural, literal_examples=examples)


def constants_checks():
    # Rational majorants for every radical used in the written norm budgets.
    require(Q(1, 3) < Q(29, 50)**2, 'Root P1 < .58')
    require(Q(27**2*2, 80**2) < Q(12, 25)**2, 'Root P3 < .48')
    require(Q(3, 5)**5 < Q(7, 25)**2, 'Root P5 < .28')
    require(Q(29, 50)+Q(12, 25)+Q(7, 25) < Q(3, 2), 'Root bound M')
    require(Q(54, 6400) < Q(23, 250)**2, 'Diagonal P3 < .092')
    require(Q(1, 3125) < Q(9, 500)**2, 'Diagonal P5 < .018')
    require(Q(23, 250)+Q(9, 500) == Q(11, 100), 'Diagonal higher bound')
    require(Q(8, 27) < Q(11, 20)**2, 'Eu linear part')
    require(Q(54, 1024) < Q(1, 4)**2, 'Eu cubic part')
    require(Q(4, 27) < Q(2, 5)**2, 'Euv linear and eE constant parts')
    require(Q(3, 64) < Q(9, 40)**2, 'Euv quadratic and eE quadratic parts')
    require(Q(16, 3125) < Q(3, 40)**2, 'eE quartic part')
    require(Q(31, 60) < Q(3, 4)**2, 'Quadratic projection constant')
    require(Q(1, 135) < Q(1, 10)**2, 'Pure mean Lambda bound')
    require(8 < 3**2, 'Binary E2 coefficient norm')

    M, lam, P = Q(3, 2), Q(1, 10), 15
    U, V = 32*M, 2*(lam+M)
    T = 9*33*(lam+U)*(U+V)
    Z = T/(4*M*M)
    require(165**3 >= Q(64, 7)*factorial(3)*Z, 'Cubic root bound')
    K3 = 32*M*(1+12*165)
    G = 6*(2*(2*K3+3*lam)+lam**2)
    B = Q(4, 5)+Q(53, 40)+28*Q(8, 5)
    Kd = 27*B*(lam+Q(88, 25))
    endpoint = 4*Kd+lam
    cd = 1/(80*P*endpoint)
    K = 432*G**2
    require((T, Z, K3, G, B, Kd, endpoint, cd) ==
            (Q(18285696, 25), Q(2031744, 25), 95088, Q(114105783, 50),
             Q(1877, 40), Q(9172899, 2000), Q(9172949, 500), Q(5, 110075388)),
            'Refined constants independently recomputed')
    require(Q(25, 4)*lam/(16*P) <= Q(1, 256), 'Light vertex contribution')
    require(16*P*endpoint*cd == Q(1, 5), 'Heavy endpoint defect')
    for j in range(2, 6):
        require(Q(j-1, 2) > Q(j, 5)+Q(1, 16), 'Heavy degree excludes j >= 2')
    require(Q(1, 2)-lam**2/16 >= Q(49, 100), 'Pure heavy product')
    require(Q(49, 100)**3-Q(1, 16) > Q(1, 20), 'Mixed heavy survivor')
    require(cd*lam**3 < Q(1, 20), 'Mixed survivor exceeds assumed error')
    require(cd*lam**5 <= Q(1, 2), 'Large error case and fidelity budget')
    candidates = [1/(27**2*lam**30), (1/(6*G*lam**3))**6,
                  (cd/(4*lam**10))**2, (cd/(4*K))**3]
    gamma = min(candidates)
    require(candidates.index(gamma) == 3, 'Last refined gamma term is active')
    require(gamma*27**2*lam**30 <= 1, 'Small relative error')
    require(gamma*(6*G*lam**3)**6 <= 1, 'Inverse condition')
    require(gamma*16*lam**20 <= cd**2, 'Original projected error')
    require(gamma*(4*K)**3 <= cd**3, 'Quadratic projected error')

    previous = json.loads((ROOT / 'computations/quantitative-proof-identities-2026-09-26/results.json').read_text())
    all_sizes = []
    for row in previous['global_diagonal_rate_constants']:
        n = row['sites']
        cs = general.constants(n)
        m, Pn, Gn = cs['m'], cs['P'], cs['G']
        k = Q(3)+Q(3*(m-1), 2)
        b = min(Q(row['amplitude_lower_bound_c']), Q(1, 2*Pn**ceil(k-1)))
        q = 1+Q(m, 2)*(k+4)
        Kn = 576*(2**m*Pn)*Gn**2
        terms = [Q(1, 3**(2*m)*Pn**(2*ceil(q-1))),
                 (1/(6*Gn*Pn**ceil(k/2)))**(2*m),
                 (b/(4*Pn**ceil(q-k)))**2, (b/(4*Kn))**m]
        gn = min(terms)
        require(1/(q-1) == Q(16, n*(3*n+22)), 'All-size exponent')
        require((q-1)/m-1 == k/2+1, 'Inverse exponent accounting')
        require(2*q/m-4-Q(2, m) == k, 'Quadratic exponent accounting')
        require(gn*3**(2*m)*Pn**(2*ceil(q-1)) <= 1, 'All-size relative error')
        require(gn*(6*Gn*Pn**ceil(k/2))**(2*m) <= 1, 'All-size inverse')
        require(16*gn*Pn**(2*ceil(q-k)) <= b**2, 'All-size original error')
        require(gn*(4*Kn)**m <= b**m, 'All-size quadratic projection')
        require(2*b*Pn**ceil(k-1) <= 1, 'All-size fidelity budget')
        all_sizes.append(dict(sites=n, q=str(q), alpha=str(1/(q-1)),
                              gamma=str(gn), minimum_selected_term=terms.index(gn)+1))
    return dict(six_site={k: str(v) for k, v in dict(M=M, Lambda=lam, K3=K3, G=G,
                B=B, Kd=Kd, Q=endpoint, diagonal_c=cd, quadratic_K=K, gamma=gamma).items()},
                all_sizes=all_sizes)


def rainbow_checks(ms):
    counts = Counter()
    sets = list(map(set, ms))
    for row in product(range(15), repeat=3):
        found = any(len({v for e in selected for v in e}) == 6
                    for selected in product(*(ms[i] for i in row)))
        if not found:
            intersections = tuple(sorted(len(sets[row[i]] & sets[row[j]])
                                         for i, j in combinations(range(3), 2)))
            counts[intersections] += 1
    require(counts == Counter({(0, 0, 1): 1080, (0, 0, 3): 360, (1, 1, 1): 90}),
            'Refutation of rainbow-free classification')
    example = [((0, 1), (2, 3), (4, 5))]*2 + [((0, 2), (1, 4), (3, 5))]
    require(not any(len({v for e in selected for v in e}) == 6
                    for selected in product(*example)), 'Explicit no-rainbow counterexample')
    require(not set.intersection(*map(set, example)), 'Counterexample has no common edge')
    return dict(no_rainbow_triples=sum(counts.values()),
                intersection_counts={str(k): v for k, v in sorted(counts.items())},
                proposed_classification='REFUTED', counterexample=example)


def phase_checks(ms):
    source = Source(6)
    phase, gauge = C(Q(99, 101), Q(20, 101)), C(Q(3, 5), Q(4, 5))
    require(phase.abs2() == gauge.abs2() == 1, 'Exact rational unit phases')
    kappa = (phase**3).re
    require(kappa == Q(851499, 1030301) and kappa > 0, 'Three-edge phase margin')
    for p, q in combinations(range(6), 2):
        for i, j in product(range(3), repeat=2):
            residual = phase if (p+q+i+j) % 2 else conjugate(phase)
            source.put(p, q, i, j, gauge**(p+2*i+q+2*j)*residual/50)
    require(len(source.cells) == 135, 'All endpoint-color cells present')
    require(sum(c.abs2() for c in source.cells.values()) < 1, 'Phase example source norm')
    mixed_count = 0
    # Every term has magnitude 50^-3, so this envelope is exact, not a norm surrogate.
    envelope = Q(15, 50**3)
    for word in product(range(3), repeat=6):
        require(source.output(word).abs2() >= kappa**2*envelope**2, 'Phase-cone guarantee')
        mixed_count += even(word) and len(set(word)) > 1
    require(mixed_count == 180, 'Even mixed receiving words')
    bad = Source(6)
    for p, q, h, weight in [(0, 1, 0, 1), (2, 3, 1, 1), (4, 5, 1, 1),
                             (2, 4, 1, 1), (3, 5, 1, -1)]:
        bad.put(p, q, h, h, Q(weight, 3))
    word = (0, 0, 1, 1, 1, 1)
    terms = [multiply(bad.edge(p, q, word[p], word[q]) for p, q in matching) for matching in ms]
    require(not bad.output(word) and sum(abs(c.re) for c in terms) == Q(2, 27),
            'Full cancellation guard must have kappa zero')
    require(Q(27)*Q(41, 1440) == Q(123, 160), 'Rate constant conversion')
    return dict(all_cells=135, words_verified=729, certificate_words=mixed_count,
                phase_cone_margin=str(kappa), zero_margin_guard='REJECTED AS REQUIRED')


def haf(matrix, indices=None):
    if indices is None:
        indices = tuple(range(len(matrix)))
    @lru_cache(None)
    def rec(vs):
        if not vs:
            return ONE
        p, rest = vs[0], vs[1:]
        return sum((matrix[p][q]*rec(tuple(v for v in rest if v != q)) for q in rest), ZERO)
    return rec(tuple(indices))


def permanent(matrix, rows, cols):
    return sum((multiply(matrix[i][j] for i, j in zip(rows, perm))
                for perm in permutations(cols)), ZERO)


def paired_checks():
    out = []
    for r in range(2, 6):
        for equality in (False, True):
            b = Q(3, 2)
            t = [[C(Q((i+2*j) % 3-1, 7), Q((2*i+j) % 3-1, 11))
                  for j in range(2)] for i in range(r)]
            B = [[C(b if i == j else 0) +
                  (ZERO if equality else sum((t[i][a]*conjugate(t[j][a]) for a in range(2)), ZERO))
                  for j in range(r)] for i in range(r)]
            Y = [[ZERO]*r for _ in range(r)]
            for i, j in combinations(range(r), 2):
                Y[i][j] = Y[j][i] = (C(Q(1, 5), Q(2, 7)) if equality and (i, j) == (0, 1)
                    else ZERO if equality else C(Q(i+j+1, 13), Q(i-j, 17)))
            S = [[Y[i][j] if i < r and j < r else B[i][j-r] if i < r else
                  B[j][i-r] if j < r else conjugate(Y[i-r][j-r])
                  for j in range(2*r)] for i in range(2*r)]
            total = haf(S)
            sectors = []
            sector_floor = Q(0)
            for k in range(r//2+1):
                subsets = list(combinations(range(r), 2*k))
                hs = {I: haf(Y, I) for I in subsets}
                complements = {I: tuple(i for i in range(r) if i not in I) for I in subsets}
                sector = sum((hs[I]*permanent(B, complements[I], complements[J])*conjugate(hs[J])
                              for I, J in product(subsets, repeat=2)), ZERO)
                floor = b**(r-2*k)*sum(h.abs2() for h in hs.values())
                require(not sector.im and sector.re >= floor, 'Positive sector and spectral floor')
                if k:
                    sector_floor += floor
                sectors.append(sector)
            perB = permanent(B, tuple(range(r)), tuple(range(r)))
            require(total == sum(sectors, ZERO) and perB == sectors[0], 'Paired sector expansion')
            edge_floor = b**(r-2)*sum(Y[i][j].abs2() for i, j in combinations(range(r), 2))
            require(total.re-perB.re >= sector_floor >= edge_floor, 'Quantitative paired bound')
            if equality:
                require(total.re-perB.re == edge_floor, 'Sharp constant-one equality case')
            diagonal_product = multiply(B[i][i] for i in range(r))
            require(not perB.im and perB.re >= diagonal_product.re, 'Permanent diagonal bound on examples')
            changed = [row[:] for row in S]
            for i in range(r):
                changed[i][i] = C(1000, 2000)
                changed[i+r][i+r] = conjugate(changed[i][i])
            require(haf(changed) == total, 'No control of diagonal Y entries')
            out.append(dict(block_size=r, equality_case=equality, hafnian=str(total),
                            excess=str(total-perB), certified_example_floor=str(edge_floor)))
    return out


def dependencies():
    # Check preceding receipts before using any of their formulas or constants.
    for folder in ('quantitative-proof-identities-2026-09-26', 'general-complex-rate-2026-09-26'):
        directory = ROOT / 'computations' / folder
        old = json.loads((directory / 'results.json').read_text())
        for relative, expected in old['sha256'].items():
            path = (directory / relative if relative == 'verify.py' else ROOT / 'notes' / relative
                    if '/' not in relative else ROOT / relative)
            require(hashlib.sha256(path.read_bytes()).hexdigest() == expected, 'Prior pinned dependency: '+relative)
    proof = ROOT / 'proofs/krenn-gu-all-orders-two-replica-proof.md'
    require(hashlib.sha256(proof.read_bytes()).hexdigest() ==
            'fb0fa1e9447d8044981692d6e9bbbeff8e6a2cfc90119b6a296cbf506b9a3c9d', 'Frozen proof unchanged')
    paths = [HERE / 'verify.py', proof,
             ROOT / 'notes/rate-sharpness-followup-2026-09-26.md',
             ROOT / 'notes/paired-hafnian-application-2026-09-26.md']
    for folder in ('quantitative-proof-identities-2026-09-26', 'general-complex-rate-2026-09-26'):
        paths.extend(ROOT / 'computations' / folder / f for f in ('verify.py', 'results.json'))
    paths.extend([ROOT / 'computations/universal-rate-gate-2026-09-26/verify.py',
                  ROOT / 'computations/useful-consequences-2026-09-26/prism.json'])
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def calibration(path):
    """Display only: no floating-point assertion contributes to the receipt."""
    K6 = (243/256)**3
    with path.open('w', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['fidelity', 'cell_phase_tolerance_degrees', 'kappa_lower_bound',
                         'phase_rate_upper_bound', 'probability_upper_bound',
                         'probability_upper_bound_with_norm_cap'])
        for fidelity in (.99, .999, .9999, .99999, .999999):
            shape = sqrt(1-fidelity)/(sqrt(fidelity)-sqrt(2*(1-fidelity)))**3
            for degrees in (0, 10, 20):
                kappa = cos(3*degrees*pi/180)
                rate = sqrt(123/160)*shape/kappa
                probability = .75*shape/kappa
                writer.writerow([fidelity, degrees, f'{kappa:.12g}', f'{rate:.12g}',
                                 f'{probability:.12g}', f'{min(K6/15, probability):.12g}'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--calibration', type=Path)
    args = parser.parse_args()
    pins = dependencies()
    vertices, edges, ms, _ = gate.setup()
    result = dict(status='PASS', evidence_status='RESEARCH; NOT INDEPENDENTLY AUDITED',
                  scope='Exact finite checks and examples support the separate analytic proofs; not a formal proof.',
                  parity_projection=parity_checks(), constants=constants_checks(),
                  positive_cover=gate.check_positive_cover(vertices, edges, ms),
                  phase_condition=phase_checks(ms),
                  prism=gate.check_prism_tangent(ms),
                  probability_conversion=gate.check_conversion(),
                  discarded_shortcut=rainbow_checks(ms),
                  paired_hafnian=paired_checks(), sha256=pins)
    if args.calibration:
        calibration(args.calibration)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
