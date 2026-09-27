"""Integer maps for a singular two-versus-four boundary and its kernel lift."""
from itertools import product, combinations
from fractions import Fraction as Q
import core

WORDS = tuple(product(range(3), repeat=6))
WORD_ID = {w: i for i, w in enumerate(WORDS)}
CELLS = tuple((p, q, i, j) for p, q in combinations(range(2, 6), 2)
              for i, j in product(range(3), repeat=2))


def maps():
    full = [[0]*54 for _ in WORDS]
    for c, (p, q, i, j) in enumerate(CELLS):
        r, s = [v for v in range(2, 6) if v not in (p, q)]
        for h, k in product(range(3), repeat=2):
            for u, v in ((r, s), (s, r)):
                w = [h, k, None, None, None, None]
                w[p], w[q], w[u], w[v] = i, j, h, k
                full[WORD_ID[tuple(w)]][c] += int(v in (2, 3))
    visible = [c for c, cell in enumerate(CELLS) if cell[:2] != (2, 3)]
    linear = [[row[c] for c in visible] for row in full]
    lift = [[0]*162 for _ in WORDS]
    # Ordering is K_(i,j) tensor U_(target,h,k), with 9 x 18 coordinates.
    for i, j, ti, h, k in product(range(3), range(3), range(2), range(3), range(3)):
        target, other = 4+ti, 5-ti
        c = (3*i+j)*18+9*ti+3*h+k
        for g in range(3):
            w = [g, h, i, j, None, None]
            w[target], w[other] = k, g
            lift[WORD_ID[tuple(w)]][c] += 1
    return full, linear, lift


def cross(a, b):
    """A^T B using sparse rows; inputs in this module are real."""
    out = [[Q(0)]*len(b[0]) for _ in range(len(a[0]))]
    for left, right in zip(a, b):
        for i, x in enumerate(left):
            if x:
                for j, y in enumerate(right):
                    if y:
                        out[i][j] += x*y
    return out


def multiply(a, b):
    out = [[Q(0)]*len(b[0]) for _ in a]
    for i, row in enumerate(a):
        for k, x in enumerate(row):
            if x:
                for j, y in enumerate(b[k]):
                    if y:
                        out[i][j] += x*y
    return out


def transpose(a):
    return list(map(list, zip(*a)))


def sparse_decode(rows, cols, entries):
    out = [[Q(0)]*cols for _ in range(rows)]
    for i, j, value in entries:
        core.require(0 <= i < rows and 0 <= j < cols and not out[i][j], 'Sparse matrix entry')
        out[i][j] = Q(value)
    return out


def verify(payload):
    full, linear, lift = maps()
    core.require(all(all(not row[c] for c in range(9)) for row in full), 'D23 kernel')
    gram, coupling, lift_gram = cross(linear, linear), cross(linear, lift), cross(lift, lift)
    core.require(all(lift_gram[i][j] ==
                     (3 if i % 18//9 == j % 18//9 else 1)*int(i//18 == j//18 and i % 9 == j % 9)
                     for i in range(162) for j in range(162)), 'Kernel lift upper norm squared is four')
    shifted = [[core.C(x-(4 if i == j else 0)) for j, x in enumerate(row)]
               for i, row in enumerate(gram)]
    lower = core.psd(shifted)
    X = sparse_decode(45, 162, payload['projection_solve'])
    core.require(multiply(gram, X) == coupling, 'Exact orthogonal projection normal equations')
    correction = multiply(transpose(coupling), X)
    H = [[lift_gram[i][j]-correction[i][j] for j in range(162)] for i in range(162)]
    partial = [[core.C(H[(j//18)*18+i % 18][(i//18)*18+j % 18]-(1 if i == j else 0))
                for j in range(162)] for i in range(162)]
    transversality = core.psd(partial)
    # Verify the target projection using the maps, without a rank computation.
    combined = [a+b for a, b in zip(linear, lift)]
    z = list(map(Q, payload['target_projection_solution']))
    core.require(len(z) == 207, 'Combined projection coefficient count')
    projected = [sum(x*y for x, y in zip(row, z)) for row in combined]
    target = [int(len(set(w)) == 1) for w in WORDS]
    residual = [x-y for x, y in zip(target, projected)]
    core.require(all(sum(row[j]*r for row, r in zip(combined, residual)) == 0 for j in range(207)),
                 'Target projection is orthogonal to the combined span')
    norm2 = sum(x*x for x in projected)
    core.require(norm2 == Q(33, 20), 'Second-order span fidelity ceiling 11/20')
    # Every kernel tensor uses only edge 23; no four-site matching can use it twice.
    core.require(all(any(edge != (2, 3) for edge in m) for m in core.matchings((2, 3, 4, 5))),
                 'Quadratic hafnian vanishes on the whole kernel')
    eta = Q(1, 1000)
    core.require(Q(17, 4)**2 > 18 and Q(5, 2)**2 > 6, 'Crossing norm upper bounds')
    core.require(5*(Q(17, 2)+eta) < 43, 'Crossing perturbation coefficient')
    core.require(Q(11, 20) < Q(3, 4)**2, 'Second-order overlap rounding')
    ceiling = ((Q(3, 4)+70*eta)/(1-70*eta))**2
    core.require(ceiling == Q(82, 93)**2 and ceiling < Q(4, 5), 'Full-neighborhood fidelity gap')
    return dict(linear_map_shape=[729, 54], kernel_dimension=9,
                visible_singular_value_lower='2', shifted_gram_psd=lower,
                lift_shape=[729, 162], partial_transpose_psd=transversality,
                product_transversality_squared_lower='1',
                combined_span_target_projection_squared=str(norm2),
                combined_span_fidelity_ceiling='11/20', crossing_radius=str(eta),
                internal_radius=str(eta), direct_edge_norm_bound='1',
                full_complex_neighborhood_fidelity_ceiling=str(ceiling))
