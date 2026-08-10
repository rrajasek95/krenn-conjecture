#!/usr/bin/env python3
"""Exact h=3 two-chart/H2 tagged-reinsertion cokernel audit.

The audit is source-grade, not a support search.  It verifies:
  * uniqueness of the selected fine multidegree among every full-nine
    row followed by two response insertions;
  * the literal marked-site identities sum rho=4 Q2 and sum sigma=6 Q3;
  * the one-dimensional response two-jet cokernel; and
  * independence of the desired clean row from the complete through-H2 span.
"""

from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json


EXPECTED_DIGEST = "e8cb942e321692152deeb2bc7ed415f57c65d92f2f4a3aea06ae9b7a8d505334"
SITES = tuple(range(6))
LABELS = tuple(range(3))
SELECTED = (0, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    if not a:
        return 0
    nr, nc = len(a), len(a[0])
    r = 0
    for c in range(nc):
        pivot = next((i for i in range(r, nr) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][c]
        a[r] = [x / p for x in a[r]]
        for i in range(nr):
            if i != r and a[i][c]:
                p = a[i][c]
                a[i] = [x - p * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == nr:
            break
    return r


def determinant(rows):
    a = [list(map(F, row)) for row in rows]
    n = len(a)
    require(all(len(row) == n for row in a), "determinant needs square matrix")
    out = F(1)
    for c in range(n):
        pivot = next((i for i in range(c, n) if a[i][c]), None)
        if pivot is None:
            return F(0)
        if pivot != c:
            a[c], a[pivot] = a[pivot], a[c]
            out = -out
        p = a[c][c]
        out *= p
        for i in range(c + 1, n):
            if a[i][c]:
                scale = a[i][c] / p
                for j in range(c, n):
                    a[i][j] -= scale * a[c][j]
    return out


def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), F(0))


def block_diag(left, right):
    zl = [F(0)] * len(right)
    zr = [F(0)] * len(left)
    return [list(row) + zl for row in left] + [zr + list(row) for row in right]


def endpoint_degree(pairs):
    left = [0, 0, 0]
    right = [0, 0, 0]
    for i, j in pairs:
        left[i] += 1
        right[j] += 1
    return tuple(left), tuple(right)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


def selected_edges(u, v):
    return {
        tuple(sorted((x, y))): u[x] * v[y] + v[x] * u[y]
        for x in SITES for y in SITES if x < y
    }


def layer_two_and_three(u, v, q):
    r = selected_edges(u, v)
    q2 = F(0)
    q3 = F(0)
    for matching in matchings(SITES):
        # Exactly two R edges and one q edge.
        for q_position in range(3):
            value = F(1)
            for position, edge in enumerate(matching):
                edge = tuple(sorted(edge))
                value *= q[edge] if position == q_position else r[edge]
            q2 += value
        q3 += product_value(r[tuple(sorted(edge))] for edge in matching)
    return q2, q3


def product_value(values):
    out = F(1)
    for value in values:
        out *= value
    return out


def marked_values(u, v, q):
    """Return the six rho_x(beta_x) and sigma_x(beta_x) values."""
    r = selected_edges(u, v)
    rho = []
    sigma = []
    for x in SITES:
        off = tuple(y for y in SITES if y != x)
        rho_x = F(0)
        sigma_x = F(0)
        for y in off:
            beta = r[tuple(sorted((x, y)))]
            if not beta:
                continue
            rest = tuple(z for z in off if z != y)
            for matching in matchings(rest):
                first, second = (tuple(sorted(edge)) for edge in matching)
                # rho(beta)=beta*(R*q) on the remaining four sites.
                rho_x += beta * (r[first] * q[second] + q[first] * r[second])
                # sigma(beta)=beta*R^[2] on the remaining four sites.
                sigma_x += beta * r[first] * r[second]
        rho.append(rho_x)
        sigma.append(sigma_x)
    return rho, sigma


def scalar(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def main():
    a, b = SELECTED
    selected_triple_degree = endpoint_degree(((a, b),) * 3)

    # A full-nine row of grade (i,j), followed by two literal response tags
    # of grades (k,l),(m,n), can reach 3(a,b) only in the selected row with
    # both tags selected.  This is the nonnegative fine-degree gate.
    routes = []
    for i, j, k, ell, m, n in product(LABELS, repeat=6):
        pairs = ((i, j), (k, ell), (m, n))
        if endpoint_degree(pairs) == selected_triple_degree:
            routes.append(pairs)
    require(routes == [((a, b), (a, b), (a, b))],
            f"selected H2 fine grade acquired extra routes: {routes}")

    # Segre switches preserve the complete left/right count vectors.
    segre_checks = 0
    for i, k, j, ell in product(LABELS, repeat=4):
        require(endpoint_degree(((i, j), (k, ell)))
                == endpoint_degree(((i, ell), (k, j))),
                "Segre switch changed endpoint fine degree")
        segre_checks += 1
    require(segre_checks == 81, "wrong Segre degree census")

    # Literal marking identities on several dense exact six-site packets.
    probes = [
        (
            [F(1), F(2), F(-1), F(3), F(1, 2), F(-2)],
            [F(2), F(-1), F(4), F(1), F(-3), F(2, 3)],
            {tuple(sorted((x, y))): F((3 * x + 5 * y + 7) % 11 - 5)
             for x in SITES for y in SITES if x < y},
        ),
        (
            [F(0), F(1), F(2), F(-2), F(3), F(1)],
            [F(1), F(0), F(-1), F(4), F(2), F(-3)],
            {tuple(sorted((x, y))): F((7 * x + 2 * y + 3) % 13 - 6)
             for x in SITES for y in SITES if x < y},
        ),
    ]
    marking_ledger = []
    for u, v, q in probes:
        q2, q3 = layer_two_and_three(u, v, q)
        rho, sigma = marked_values(u, v, q)
        require(sum(rho, F(0)) == 4 * q2, "rho marking factor is not four")
        require(sum(sigma, F(0)) == 6 * q3, "sigma marking factor is not six")
        require(all(value == q3 for value in sigma),
                "fixed-site sigma value is not Q3")
        marking_ledger.append({
            "Q2": scalar(q2), "Q3": scalar(q3),
            "sum_rho": scalar(sum(rho, F(0))),
            "sum_sigma": scalar(sum(sigma, F(0))),
        })

    # Coordinate-free response jet.  The complete through-H2 rows are
    # e0=alpha Q0+Q1, e1=alpha Q1+2Q2, e2=alpha Q2+3Q3.
    # The clean row c=alpha Q2+Q3 is independent for alpha != 0.
    alpha_records = []
    for alpha in (F(1), F(2), F(-3, 2)):
        through_h2 = [
            [alpha, F(1), F(0), F(0)],
            [F(0), alpha, F(2), F(0)],
            [F(0), F(0), alpha, F(3)],
        ]
        clean = [F(0), F(0), alpha, F(1)]
        terminal = [F(-6), 6 * alpha, -3 * alpha ** 2, alpha ** 3]
        require(rank(through_h2) == 3, "through-H2 jet rank changed")
        require(all(dot(row, terminal) == 0 for row in through_h2),
                "terminal line is not killed by every through-H2 row")
        require(dot(clean, terminal) == -2 * alpha ** 3,
                "clean row lost terminal detection")
        augmented = through_h2 + [clean]
        require(rank(augmented) == 4, "clean row entered through-H2 span")
        require(determinant(augmented) == -2 * alpha ** 3,
                "augmented jet determinant changed")

        # The marked normal plane says the same thing after lower grades are
        # eliminated: H2=(alpha/4,1/2), clean=(alpha/4,1/6).
        marked_h2 = [alpha / 4, F(1, 2)]
        marked_clean = [alpha / 4, F(1, 6)]
        marked_terminal = [F(-12) / alpha, F(6)]
        require(dot(marked_h2, marked_terminal) == 0,
                "marked terminal does not kill H2 row")
        require(dot(marked_clean, marked_terminal) == -2,
                "marked clean value is not -2")
        require(determinant([marked_h2, marked_clean]) == -alpha / 12,
                "marked-plane determinant changed")
        alpha_records.append({
            "alpha": scalar(alpha),
            "jet_augmented_det": scalar(determinant(augmented)),
            "marked_augmented_det": scalar(determinant([marked_h2, marked_clean])),
            "terminal_clean_value": scalar(dot(clean, terminal)),
        })

    # The two-chart static label block is already full.  Direct-summing it
    # with the through-H2 jet leaves precisely the terminal line; adjoining
    # clean has determinant 6*alpha^3 at alpha=1.
    static = [
        [F(1), F(0), F(1), F(0)],
        [F(0), F(0), F(1), F(1)],
        [F(0), F(0), F(1), F(-2)],
        [F(0), F(1), F(2), F(0)],
    ]
    require(determinant(static) == -3, "two-chart static determinant changed")
    jet = [
        [F(1), F(1), F(0), F(0)],
        [F(0), F(1), F(2), F(0)],
        [F(0), F(0), F(1), F(3)],
    ]
    clean = [F(0), F(0), F(1), F(1)]
    combined_h2 = block_diag(static, jet)
    combined_clean = block_diag(static, jet + [clean])
    require(rank(combined_h2) == 7, "combined through-H2 rank changed")
    require(rank(combined_clean) == 8, "clean row did not close terminal line")
    require(determinant(combined_clean) == 6,
            "combined clean Fitting determinant changed")

    ledger = {
        "scope": "literal nonnegative endpoint fine grade; two response tags; h=3",
        "selected_labels": list(SELECTED),
        "selected_triple_routes": [[list(pair) for pair in route] for route in routes],
        "segre_degree_checks": segre_checks,
        "marking": marking_ledger,
        "alpha_records": alpha_records,
        "static_det": scalar(determinant(static)),
        "combined_through_h2_rank": rank(combined_h2),
        "combined_with_clean_rank": rank(combined_clean),
        "combined_clean_det_at_alpha_1": scalar(determinant(combined_clean)),
        "verdict": "H2_supplies_alpha_Q2_plus_3Q3_not_alpha_Q2_plus_Q3",
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger changed: {digest}")

    print("h=3 two-chart H2 tagged-reinsertion cokernel: PASS")
    print("selected fine-grade H2 routes: 1 (the repeated selected response)")
    print("through-H2 terminal cokernel: dimension 1")
    print("clean row detects terminal by -2*alpha^3")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()
