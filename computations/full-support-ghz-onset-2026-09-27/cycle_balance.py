"""Exact support for the two closing arguments in full-support GHZ onset."""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]
                       / "single-invertible-edge-ghz-2026-09-27"))
import edge_projection as EP
from edge_projection import Poly, T, E, ZERO, ONE, require

CORE = (0, 1, 2, 3)
CYCLE = ((0, 1), (0, 3), (1, 2), (2, 3))


def power(value, n):
    result = ONE
    for _ in range(n):
        result *= value
    return result


def unit_vector(q, site):
    weights = {1: (Q(1),), 2: (Q(3, 5), Q(4, 5)),
               3: (Q(1, 3), Q(2, 3), Q(2, 3))}[q]
    vector = [weights[(j+site) % q]*power(T.OMEGA, (site+2*j) % 3) for j in range(q)]
    require(sum(z.abs2() for z in vector) == 1, "Exact unit local vector")
    return vector


def make_core(q, coefficients):
    local = {i: unit_vector(q, i) for i in CORE}
    return {(i, j, a, b): coefficient*local[i][a]*local[j][b]
            for (i, j), coefficient in coefficients.items()
            for a, b in product(range(q), repeat=2)}


def attachment_matrix(core, q):
    columns = tuple(product(CORE, range(q)))
    result = []
    for triple in combinations(CORE, 3):
        for colors in product(range(q), repeat=3):
            word = dict(zip(triple, colors))
            row = []
            for site, color in columns:
                if site not in triple or word[site] != color:
                    row.append(ZERO)
                else:
                    i, j = tuple(v for v in triple if v != site)
                    row.append(core.get((i, j, word[i], word[j]), ZERO))
            result.append(row)
    return result


def gram(matrix):
    n = len(matrix[0])
    return [[sum((row[i].conjugate()*row[j] for row in matrix), ZERO)
             for j in range(n)] for i in range(n)]


def check_phase_gram():
    # Laurent monomials in three independent unit phases; conjugation negates exponents.
    phase = {(0, 1): (1, (1, 0, 0)), (0, 3): (1, (0, 1, 0)),
             (1, 2): (1, (0, 0, 1)), (2, 3): (-1, (-1, 1, 1))}
    cancellations = 0
    for i, j in combinations(CORE, 2):
        terms = {}
        for k in CORE:
            a, b = tuple(sorted((i, k))), tuple(sorted((j, k)))
            if a not in phase or b not in phase:
                continue
            sign_a, exponent_a = phase[a]
            sign_b, exponent_b = phase[b]
            exponent = tuple(x-y for x, y in zip(exponent_a, exponent_b))
            terms[exponent] = terms.get(exponent, 0)+sign_a*sign_b
        require(not any(terms.values()), "Formal unit-phase cancellation of off-diagonal Gram block")
        cancellations += bool(terms)
    require(cancellations == 2, "Two nontrivial opposite-vertex phase cancellations")
    require(all(sum(i not in edge for edge in CYCLE) == 2 for i in CORE),
            "Each diagonal Gram block is twice the identity")
    return dict(off_diagonal_blocks=6, nontrivial_phase_cancellations=2,
                diagonal_blocks=4, scope="Formal identities in arbitrary unit edge phases")


def check_isometry():
    phases = (ONE, T.OMEGA, E(Q(3, 7), Q(8, 7)))
    require(all(z.abs2() == 1 for z in phases), "Unit edge phases")
    records = []
    entries = 0
    for q in (1, 2, 3):
        for k in range(3):
            g, b, c = phases[k], phases[(k+1) % 3], phases[(k+2) % 3]
            coefficients = {(0, 1): g, (0, 3): b, (1, 2): c, (2, 3): -b*c/g}
            core = make_core(q, coefficients)
            require(not T.outputs(core, n=4, colors=q), "Exactly flat colored four-cycle")
            matrix = attachment_matrix(core, q)
            actual = gram(matrix)
            require(actual == [[E(2) if i == j else ZERO for j in range(4*q)]
                               for i in range(4*q)], "Exact colored response Gram is 2I")
            entries += (4*q)**2
            records.append(dict(palette=q, phase_fixture=k, input_dimension=4*q,
                                response_rows=len(matrix), gram_factor="2"))
    # A plus sign leaves a non-flat cycle and a two-dimensional scalar-sector kernel.
    bad = make_core(2, {edge: ONE for edge in CYCLE})
    bad_matrix = attachment_matrix(bad, 2)
    require(T.outputs(bad, n=4, colors=2) and T.rank(bad_matrix) == 6,
            "Removing the cancellation sign destroys the isometry")
    degeneration = []
    for tau in (Q(1, 2), Q(1, 4), Q(1, 8)):
        core = make_core(1, {(0, 1): ONE, (0, 3): E(tau),
                            (1, 2): ONE, (2, 3): E(-tau)})
        # Express the test vector in the site's local unit phases.
        vector = [unit_vector(1, i)[0]*sign for i, sign in enumerate((1, 0, -1, 0))]
        response = [sum((a*b for a, b in zip(row, vector)), ZERO)
                    for row in attachment_matrix(core, 1)]
        input_squared = sum(x.abs2() for x in vector)
        response_squared = sum(x.abs2() for x in response)
        require(response_squared == 4*tau*tau and input_squared == 2,
                "Unbalanced flat cycles lose a uniform response gap")
        degeneration.append(dict(tau=str(tau), squared_norm_ratio=str(response_squared/input_squared)))
    return dict(fixtures=records, gram_entries=entries,
                wrong_sign_negative_control_rank=6, unbalanced_negative_controls=degeneration)


def check_scaling_and_matching():
    # s=(p,1/p,r,r,1/r,1/r), p=sqrt(c/b), r=g/sqrt(bc).
    weights = ((1, 0), (-1, 0), (0, 1), (0, 1), (0, -1), (0, -1))
    def exponent(vertices):
        return tuple(sum(weights[i][k] for i in vertices) for k in range(2))
    expected = {(0, 1): (0, 0), (0, 3): (1, 1), (1, 2): (-1, 1), (2, 3): (0, 2),
                (0, 2): (1, 1), (1, 3): (-1, 1), (4, 5): (0, -2),
                (0, 4): (1, -1), (1, 4): (-1, -1), (2, 4): (0, 0), (3, 4): (0, 0)}
    require(all(exponent(edge) == value for edge, value in expected.items()), "Every required edge scale")
    quartets = {(0, 1, 2, 4): (0, 0), (0, 1, 3, 4): (0, 0),
                (0, 2, 3, 4): (1, 1), (1, 2, 3, 4): (-1, 1),
                (0, 1, 2, 3): (0, 2)}
    require(all(exponent(quartet) == value for quartet, value in quartets.items()),
            "Exact attachment and core quartet scales")
    for matching in T.matchings(tuple(range(6))):
        require(tuple(sum(exponent(edge)[k] for edge in matching) for k in range(2)) == (0, 0),
                "Product-one site scaling preserves every six-site matching")

    var = lambda *parts: Poly.variable("_".join(map(str, parts)))
    source = {(*edge, a, b): var("t", *edge, a, b)
              for edge in combinations(range(6), 2) for a, b in product(range(2), repeat=2)}
    identities = 0
    for word in product(range(2), repeat=6):
        full, outside_pair, attachments = Poly(), Poly(), Poly()
        first_count = second_count = 0
        for matching in T.matchings(tuple(range(6))):
            term = Poly(1)
            for i, j in matching:
                term *= source[i, j, word[i], word[j]]
            full += term
            if (4, 5) in matching:
                outside_pair += term
                first_count += 1
            else:
                require(sum(i in CORE and j in CORE for i, j in matching) == 1
                        and sum((i in CORE) != (j in CORE) for i, j in matching) == 2,
                        "Each remaining matching has one core edge and two attachments")
                attachments += term
                second_count += 1
        require((first_count, second_count) == (3, 12), "Complete matching split")
        require(full.terms == (outside_pair+attachments).terms, "Formal four-core output identity")
        identities += 1

    dense = {(*edge, a, b): E(edge[0]+2*edge[1]+a-b+1, 1+edge[0]-a+2*b)
             for edge in combinations(range(6), 2) for a, b in product(range(2), repeat=2)}
    original = T.outputs(dense, n=6, colors=2)
    original_four = T.four_outputs(dense, n=6, q=2)
    for tau in (Q(1, 2), Q(1, 3), Q(1, 5)):
        # g=1,b=tau^2,c=tau^4; individual site factors become arbitrarily large.
        sites = (tau, 1/tau, 1/(tau*tau*tau), 1/(tau*tau*tau), tau*tau*tau, tau*tau*tau)
        scaled = {(i, j, a, b): sites[i]*sites[j]*value for (i, j, a, b), value in dense.items()}
        require(T.outputs(scaled, n=6, colors=2) == original, "Exact dense complex output invariance")
        scaled_four = T.four_outputs(scaled, n=6, q=2)
        expected_four = {}
        for (vertices, word), value in original_four.items():
            factor = Q(1)
            for vertex in vertices:
                factor *= sites[vertex]
            expected_four[vertices, word] = factor*value
        require(scaled_four == expected_four, "Every dense quartet obeys its labelled site multiplier")
    return dict(edge_scale_identities=len(expected), quartet_scale_identities=len(quartets),
                invariant_matching_monomials=15, formal_output_splits=identities,
                dense_complex_scaling_fixtures=3)


def check_scalar_absorptions():
    names = ("a", "b", "c", "d", "g", "t", "u", "x", "eps", "eta", "k")
    a, b, c, d, g, t, u, x, eps, eta, k = [Poly.variable(name) for name in names]
    records = []
    def record(name, left, right, assumptions):
        require(left.terms == right.terms, "Polynomial scalar certificate: " + name)
        records.append(dict(name=name, nonnegative_factors=assumptions))
    record("large error dominates the projected output",
           eps-t*d*u, (eps-d*u)+(1-t)*d*u,
           ["eps >= d*u", "t <= 1", "d,u >= 0"])
    record("lower bound for the cancelling core product",
           b*c-Q(1, 2)*g*u,
           (b*c-g*u+k*t*d)+Q(1, 2)*((g-eta*t)*u+t*(eta*u-2*k*d)),
           ["b*c >= g*u-k*t*d", "g >= eta*t", "eta*u >= 2*k*d", "u,t >= 0"])
    record("each attachment edge dominates the outside scale",
           2*t*b-eta*t*u, 2*b*(t-c)+(2*b*c-g*u)+(g-eta*t)*u,
           ["c <= t", "2*b*c >= g*u", "g >= eta*t", "b,u >= 0"])
    record("absorb the rescaled attachment",
           2*a*d*u-x*u, 2*(a*d*u+k*d*x-u*x)+x*(u-2*k*d),
           ["x*u <= a*d*u+k*d*x", "u >= 2*k*d", "x >= 0"])
    record("the opposite outside edge is small",
           3*k*d*u-u*x,
           (k*(eps+d*u+d*d)-u*x)+k*(d*u-eps)+k*d*(u-d),
           ["u*x <= k*(eps+d*u+d^2)", "eps <= d*u", "u >= d", "k,d >= 0"])
    # The unscaled counterpart of h1 can be much larger; only its correct weighted term is small.
    for gv, bv, cv in ((Q(1), Q(1, 4), Q(1, 16)), (Q(1), Q(1, 8), Q(1, 64))):
        uv = bv*cv/gv
        require(gv/(bv*cv) == 1/uv, "Exact hidden-attachment coefficient after quartet scaling")
    return dict(certificates=records, weighted_attachment_coefficients=2)


def check_bridge_choices():
    left, right = {0, 1, 2}, {3, 4, 5}
    bridge = (0, 3)
    opposite_bridge = other_pair = 0
    for i in left-{bridge[0]}:
        for j in right-{bridge[1]}:
            outside_left, outside_right = left-{i}, right-{j}
            outside_edges = [(a, b) for a in outside_left for b in outside_right]
            for chosen in outside_edges:
                if chosen == bridge:
                    continue
                other_left = next(v for v in outside_left if v != chosen[0])
                other_right = next(v for v in outside_right if v != chosen[1])
                complement = (other_left, other_right)
                if complement == bridge:
                    opposite_bridge += 1
                else:
                    other_matching = {(chosen[0], other_right), (other_left, chosen[1])}
                    require(bridge in other_matching, "The other outside matching contains the small bridge")
                    other_pair += 1
    require((opposite_bridge, other_pair) == (4, 8), "All residual root and largest-edge choices")
    return dict(largest_edge_opposite_bridge=opposite_bridge,
                bridge_in_other_matching=other_pair, choices=opposite_bridge+other_pair)


def project_pair(output, source, pair):
    i, j = pair
    block = {(a, b): source.get((i, j, a, b), ZERO) for a, b in product(range(2), repeat=2)}
    squared = sum(value.abs2() for value in block.values())
    require(squared > 0, "Nonzero projection line")
    outside = [v for v in range(6) if v not in pair]
    result = {}
    for colors in product(range(2), repeat=4):
        base = dict(zip(outside, colors))
        words = {}
        for a, b in block:
            full = base | {i: a, j: b}
            words[a, b] = tuple(full[v] for v in range(6))
        contraction = sum((value.conjugate()*output.get(words[key], ZERO)
                           for key, value in block.items()), ZERO)/squared
        for key, word in words.items():
            value = output.get(word, ZERO)-block[key]*contraction
            if value:
                result[word] = value
    return result


def check_outside_edge_projection():
    records = []
    wrong_cut_rejected = False
    target = {(0,)*6: ONE, (1,)*6: ONE}
    for fixture in range(4):
        source = {(*edge, a, b): E(1+edge[0]+2*edge[1]+a-b, 2+edge[0]-a+b)
                  for edge in combinations(range(6), 2) for a, b in product(range(2), repeat=2)}
        if fixture == 1:
            for a, b in product(range(2), repeat=2):
                source[0, 1, a, b] = ZERO
        elif fixture == 2:
            for a, b in product(range(2), repeat=2):
                source[2, 3, a, b] = ONE if a == b == 0 else ZERO
        elif fixture == 3:
            left, right = (E(1, 1), E(2)), (E(3, -1), E(1, 2))
            for a, b in product(range(2), repeat=2):
                source[2, 3, a, b] = left[a]*right[b]
        full = T.outputs(source, n=6, colors=2)
        four = T.four_outputs(source, n=6, q=2)
        remaining = {}
        for word in product(range(2), repeat=6):
            cell = lambda i, j: source.get((i, j, word[i], word[j]), ZERO)
            def response(r, s):
                return four.get(((0, 1, r, s), (word[0], word[1], word[r], word[s])), ZERO)
            value = response(2, 3)*cell(4, 5)
            for r, s in ((2, 4), (2, 5), (3, 4), (3, 5)):
                u, v = tuple(k for k in (2, 3, 4, 5) if k not in (r, s))
                value += response(r, s)*cell(u, v)
            value -= cell(0, 1)*(cell(2, 4)*cell(3, 5)+cell(2, 5)*cell(3, 4))
            if value:
                remaining[word] = value
        require(project_pair(full, source, (2, 3)) == project_pair(remaining, source, (2, 3)),
                "Projection at the large outside edge removes its complete product term")
        retained = T.norm2(project_pair(target, source, (2, 3)))
        block_norm = sum(source[2, 3, a, b].abs2() for a, b in product(range(2), repeat=2))
        expected = 2-(source[2, 3, 0, 0].abs2()+source[2, 3, 1, 1].abs2())/block_norm
        require(retained == expected and retained >= 1, "Uniform GHZ gap on the outside pair")
        if fixture == 0:
            wrong_cut_rejected = project_pair(full, source, (0, 1)) != project_pair(remaining, source, (0, 1))
        records.append(dict(fixture=fixture, complementary_edge_zero=(fixture == 1),
                            retained_target_norm_squared=str(retained)))
    require(wrong_cut_rejected, "Projecting at the complementary core need not remove the same term")
    require(records[2]["retained_target_norm_squared"] == "1", "Sharp one-line GHZ gap")
    return dict(fixtures=records, wrong_projection_cut_negative_control=True,
                formal_matching_identities=EP.check_formal_identities())


def check():
    return dict(formal_phase_gram=check_phase_gram(), response_isometry=check_isometry(),
                site_scaling_and_output=check_scaling_and_matching(),
                scalar_absorption=check_scalar_absorptions(), bridge_choices=check_bridge_choices(),
                outside_edge_projection=check_outside_edge_projection())
