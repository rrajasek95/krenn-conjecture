#!/usr/bin/env python3
"""Exact audits for the Z/8-translation-invariant n=8 ansatz.

There are two logically separate calculations.

1.  For arbitrary endpoint-colour matrices, the 834 cyclic word-coordinate
    polynomials have full row rank over Q.  Thus no linear output functional
    separates this 33-parameter fourth-power image from the target.
2.  If all four distance matrices are colour diagonal, 39 selected necklace
    equations already generate the unit ideal over Q.  Hence this
    12-parameter subchart has no complex point mapping to ternary GHZ_8.

The second calculation invokes Singular for an exact rational Groebner
basis.  No floating-point arithmetic is used anywhere.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations, product
import shutil
import subprocess


N = 8
Q = 3
PRIME = 1_000_003
VARIABLE_NAMES = tuple(
    f"{colour}{distance}"
    for colour in ("a", "b", "c")
    for distance in range(1, 5)
)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for position in range(1, len(vertices)):
        v = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(rest):
            yield ((u, v),) + tail


MATCHINGS = tuple(perfect_matchings(tuple(range(N))))
assert len(MATCHINGS) == 105


def rotate(word: tuple[int, ...], shift: int) -> tuple[int, ...]:
    return tuple(word[(vertex - shift) % N] for vertex in range(N))


def word_representatives() -> tuple[tuple[int, ...], ...]:
    answer = tuple(
        word
        for word in product(range(Q), repeat=N)
        if word == min(rotate(word, shift) for shift in range(N))
    )
    # Burnside: (3^8 + 4*3 + 2*3^2 + 3^4)/8 = 834.
    assert len(answer) == 834
    return answer


WORDS = word_representatives()


def full_variable(u: int, v: int, left: int, right: int) -> int:
    """Parameter cell for an edge u<v in the unrestricted cyclic chart."""
    assert u < v
    distance = v - u
    if distance <= 3:
        return (distance - 1) * 9 + left * 3 + right
    if distance == 4:
        first, second = sorted((left, right))
        # Upper triangle of the symmetric antipodal matrix, after 27 cells.
        return 27 + sum(3 - row for row in range(first)) + second - first
    # The shorter orientation points from v to u, so use a transposed cell.
    distance = N - distance
    return (distance - 1) * 9 + right * 3 + left


def full_coefficient(word: tuple[int, ...]) -> Counter[tuple[int, ...]]:
    polynomial: Counter[tuple[int, ...]] = Counter()
    for matching in MATCHINGS:
        monomial = tuple(sorted(
            full_variable(u, v, word[u], word[v]) for u, v in matching
        ))
        polynomial[monomial] += 1
    return polynomial


def sparse_rank(rows: list[dict[int, int]], prime: int) -> int:
    """Sparse Gaussian elimination over F_prime."""
    pivots: dict[int, dict[int, int]] = {}
    for source in rows:
        row = {
            column: coefficient % prime
            for column, coefficient in source.items()
            if coefficient % prime
        }
        while row:
            column = min(row)
            if column not in pivots:
                inverse = pow(row[column], -1, prime)
                pivots[column] = {
                    key: value * inverse % prime for key, value in row.items()
                }
                break
            factor = row[column]
            for key, value in pivots[column].items():
                new_value = (row.get(key, 0) - factor * value) % prime
                if new_value:
                    row[key] = new_value
                else:
                    row.pop(key, None)
    return len(pivots)


def audit_unrestricted_linear_span() -> tuple[int, int]:
    polynomials = tuple(full_coefficient(word) for word in WORDS)
    monomials = sorted(set().union(*polynomials))
    assert len(monomials) == 26_370
    monomial_index = {
        monomial: index for index, monomial in enumerate(monomials)
    }
    rows = [
        {
            monomial_index[monomial]: coefficient
            for monomial, coefficient in polynomial.items()
        }
        for polynomial in polynomials
    ]
    rank = sparse_rank(rows, PRIME)
    assert rank == len(WORDS)
    return len(monomials), rank


def diagonal_variable(u: int, v: int, colour: int) -> int:
    distance = v - u
    if distance > N // 2:
        distance = N - distance
    return 4 * colour + distance - 1


def diagonal_coefficient(word: tuple[int, ...]) -> Counter[tuple[int, ...]]:
    """Coefficient after C_d=diag(a_d,b_d,c_d), d=1,...,4."""
    polynomial: Counter[tuple[int, ...]] = Counter()
    for matching in MATCHINGS:
        if all(word[u] == word[v] for u, v in matching):
            monomial = tuple(sorted(
                diagonal_variable(u, v, word[u]) for u, v in matching
            ))
            polynomial[monomial] += 1
    return polynomial


def residual_key(word: tuple[int, ...]):
    constant = -1 if len(set(word)) == 1 else 0
    return tuple(sorted(diagonal_coefficient(word).items())), constant


# One representative from each selected colour-permutation family.  Taking
# all S_3 images, and deleting duplicate polynomials caused by rotations,
# gives 39 equations.  The first family supplies the three pure normalizations.
WORD_FAMILIES = (
    (0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 1, 1, 1),
    (0, 0, 0, 0, 1, 2, 2, 1),
    (0, 0, 0, 1, 2, 0, 1, 2),
    (0, 0, 0, 1, 2, 0, 2, 1),
    (0, 0, 1, 0, 1, 1, 0, 1),
    (0, 0, 1, 1, 0, 0, 1, 1),
    (0, 0, 1, 1, 0, 0, 2, 2),
    (0, 0, 1, 2, 0, 0, 1, 2),
    (0, 0, 1, 2, 0, 0, 2, 1),
    (0, 1, 0, 1, 0, 2, 0, 2),
)


def singular_polynomial(key) -> str:
    terms, constant = key
    pieces: list[str] = []
    for monomial, coefficient in terms:
        variables = "*".join(VARIABLE_NAMES[index] for index in monomial)
        scalar = "" if coefficient == 1 else f"{coefficient}*"
        pieces.append(("+" if pieces else "") + scalar + variables)
    if constant:
        pieces.append(f"{constant:+d}" if pieces else str(constant))
    return "".join(pieces) or "0"


def selected_diagonal_equations():
    selected = {}
    for family in WORD_FAMILIES:
        for permutation in permutations(range(Q)):
            word = tuple(permutation[colour] for colour in family)
            selected.setdefault(residual_key(word), word)
    assert len(selected) == 39
    assert sum(len(set(word)) == 1 for word in selected.values()) == 3
    return selected


def audit_diagonal_unit_ideal() -> tuple[int, str]:
    # Independently enumerate the entire diagonal necklace system and verify
    # that every selected equation really is one of its target residuals.
    all_residuals = {
        residual_key(word)
        for word in WORDS
        if diagonal_coefficient(word) or len(set(word)) == 1
    }
    assert len(all_residuals) == 150
    selected = selected_diagonal_equations()
    assert set(selected) <= all_residuals

    executable = shutil.which("Singular")
    if executable is None:
        raise SystemExit("Singular is required for the rational certificate")
    generators = ",".join(
        singular_polynomial(key) for key in selected
    )
    script = (
        "option(redSB);\n"
        f"ring r=0,({','.join(VARIABLE_NAMES)}),dp;\n"
        f"ideal I={generators};\n"
        "size(I);\n"
        "ideal G=slimgb(I);\n"
        "size(G);\n"
        "G;\n"
        "quit;\n"
    )
    result = subprocess.run(
        [executable, "-q"],
        input=script,
        text=True,
        capture_output=True,
        check=True,
        timeout=120,
    )
    transcript = tuple(line.strip() for line in result.stdout.splitlines()
                       if line.strip())
    assert transcript == ("39", "1", "G[1]=1"), transcript
    return len(all_residuals), " / ".join(transcript)


def main() -> None:
    monomial_count, rank = audit_unrestricted_linear_span()
    residual_count, groebner = audit_diagonal_unit_ideal()
    print(
        "unrestricted cyclic chart: "
        f"parameters=33 word_orbits=834 quartic_monomials={monomial_count} "
        f"rank_mod_{PRIME}={rank}"
    )
    print(
        "colour-diagonal cyclic chart: "
        f"parameters=12 distinct_residuals={residual_count} "
        f"selected_equations=39 rational_Groebner={groebner}"
    )
    print("PASS: exact linear-span audit and exact diagonal no-go")


if __name__ == "__main__":
    main()
