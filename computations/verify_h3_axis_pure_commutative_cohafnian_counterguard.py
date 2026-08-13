#!/usr/bin/env python3
"""A sharp counterguard to a commutative cohafnian attack on axis purity.

The three variables record only colour counts.  The checker constructs a
rational 6 by 6 axis-pure edge matrix whose commutative hafnian and selected
cohafnian sandwich have exactly the desired diagonal form, but whose fully
polarized mixed-word coefficients are nonzero.  Thus no identity in the
collapsed polynomial data alone can prove the physical statement.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/curved-scalar-zero-tangent-apolar-hall-alternative.md":
        "fac1ddb2189437bd42d756a06043852a28ea41d60299968f4da19cd8d8eaa1f3",
    "computations/verify_h3_axis_pure_cancellation_support_lower_bound.py":
        "c7c501de4c4646b98e5525d616012bbced15957dcaaa836ebe38341c56385397",
    "notes/h3-axis-pure-cancellation-support-lower-bound.md":
        "b81542ec64eb0667c7c70109d15a0e92932d8e1ffeb124c87992a0abe96a41cc",
}
EXPECTED_LEDGER_SHA256 = "0a2bedd4201feba39c763eea8ddcbeefae2ea8ea114c65a32428c85ace8e38bb"
ZERO = (F(0), F(0), F(0))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))


def edge(colour: int, coefficient: F = F(1)) -> tuple[F, F, F]:
    ans = [F(0), F(0), F(0)]
    ans[colour] = coefficient
    return tuple(ans)


def polynomial_add(*values):
    answer = {}
    for value in values:
        for exponent, coefficient in value.items():
            answer[exponent] = answer.get(exponent, F(0)) + coefficient
    return {exponent: coefficient for exponent, coefficient in answer.items()
            if coefficient}


def polynomial_multiply(left, right):
    answer = {}
    for a, coefficient in left.items():
        for b, scalar in right.items():
            exponent = tuple(a[i]+b[i] for i in range(3))
            answer[exponent] = answer.get(exponent, F(0))+coefficient*scalar
    return {exponent: coefficient for exponent, coefficient in answer.items()
            if coefficient}


def linear_polynomial(value):
    return {(1, 0, 0): value[0],
            (0, 1, 0): value[1],
            (0, 0, 1): value[2]}


def hafnian(vertices, q):
    if not vertices:
        return {(0, 0, 0): F(1)}
    first = vertices[0]
    terms = []
    for mate in vertices[1:]:
        rest = [v for v in vertices[1:] if v != mate]
        terms.append(polynomial_multiply(
            linear_polynomial(q.get(tuple(sorted((first, mate))), ZERO)),
            hafnian(rest, q),
        ))
    return polynomial_add(*terms)


def polarized_hafnian(vertices, q):
    """Return coefficients by literal six-site colour word, not colour count."""
    if not vertices:
        return {(): F(1)}
    first = vertices[0]
    answer = {}
    for mate in vertices[1:]:
        value = q.get(tuple(sorted((first, mate))), ZERO)
        rest = [v for v in vertices[1:] if v != mate]
        for word, coefficient in polarized_hafnian(rest, q).items():
            word_map = dict(word)
            for colour, scalar in enumerate(value):
                if not scalar:
                    continue
                extended = dict(word_map)
                extended[first] = colour
                extended[mate] = colour
                key = tuple(sorted(extended.items()))
                answer[key] = answer.get(key, F(0))+coefficient*scalar
    return {word: coefficient for word, coefficient in answer.items()
            if coefficient}


def word_string(word, vertices=range(6)):
    values = dict(word)
    return "".join(str(values[v]) for v in vertices)


def q_matrix():
    # Three target edges, followed by the two inverse-matrix rectangles.
    q = {
        (0, 1): edge(0), (2, 3): edge(0), (4, 5): edge(0),
        (1, 4): edge(1), (1, 5): edge(1),
        (3, 4): edge(1, F(1, 2)), (3, 5): edge(1, F(1, 2)),
        (0, 4): edge(2, F(-1)), (0, 5): edge(2),
        (2, 4): edge(2, F(1, 2)), (2, 5): edge(2, F(-1, 2)),
    }
    return q


def family_identity_audit():
    # Put U=[[a,f],[h,c]], V=[[b,e],[g,d]].  The selected response
    # cofactors are diag(x1,x2) U V diag(x1,x2).
    a, f, h, c = F(1), F(1), F(-1), F(1)
    determinant = a*c-f*h
    b, e, g, d = c/determinant, -f/determinant, -h/determinant, a/determinant
    uv = (
        (a*b+f*g, a*e+f*d),
        (h*b+c*g, h*e+c*d),
    )
    leakage = a*c+f*h+b*d+e*g
    require(determinant == 2 and uv == ((1, 0), (0, 1)),
            (determinant, uv))
    require(leakage == 0, leakage)
    return {
        "U": [[1, 1], [-1, 1]],
        "V": [["1/2", "-1/2"], ["1/2", "1/2"]],
        "UV": [[1, 0], [0, 1]],
        "det_U": 2,
        "hafnian_leakage_coefficient": 0,
        "general_formula": (
            "if V=U^-1, leakage=(ac+fh)*(1+det(U)^-2)"
        ),
        "meaning": (
            "response normalization does not force commutative cubic leakage"
        ),
    }


def exact_countermodel_audit():
    q = q_matrix()
    vertices = list(range(6))
    total = hafnian(vertices, q)
    expected_total = {(3, 0, 0): F(1)}
    require(total == expected_total, total)

    # p1=e0, p2=e1 and s1=e2, s2=e3.  Hence the selected sandwich is
    # the 2 by 2 cohafnian submatrix on rows (0,1), columns (2,3).
    selected = {}
    for row in (0, 1):
        for column in (2, 3):
            selected[(row, column)] = hafnian(
                [v for v in vertices if v not in (row, column)], q)
    expected = {
        (0, 2): {(0, 2, 0): F(1)},
        (0, 3): {},
        (1, 2): {},
        (1, 3): {(0, 0, 2): F(1)},
    }
    require(selected == expected, selected)

    polarized = polarized_hafnian(vertices, q)
    mixed = {word_string(word): coefficient for word, coefficient in
             polarized.items() if len(set(dict(word).values())) > 1}
    expected_mixed = {
        "002121": F(1, 4),
        "002112": F(-1, 4),
        "210021": F(-1),
        "210012": F(1),
    }
    require(mixed == expected_mixed, mixed)
    require(sum(mixed.values(), F(0)) == 0, mixed)

    # The two aggregate-zero crossed cofactors also cancel only across
    # distinct fully polarized response words.
    cross_words = {}
    endpoint_colours = {(0, 3): (1, 2), (1, 2): (2, 1)}
    for pair, colours in endpoint_colours.items():
        remaining = [v for v in vertices if v not in pair]
        entries = polarized_hafnian(remaining, q)
        expanded = {}
        for word, coefficient in entries.items():
            value = dict(word)
            value[pair[0]], value[pair[1]] = colours
            key = "".join(str(value[v]) for v in vertices)
            expanded[key] = expanded.get(key, F(0))+coefficient
        cross_words[str(pair)] = {key: str(value) for key, value in
                                  expanded.items() if value}
        require(sum(expanded.values(), F(0)) == 0, (pair, expanded))

    return {
        "Q_support_size": len(q),
        "haf_Q": "x0^3",
        "selected_cohafnian_block": [["x1^2", 0], [0, "x2^2"]],
        "p_rows": [0, 1],
        "s_columns": [2, 3],
        "polarized_unary_mixed_coefficients": {
            key: str(value) for key, value in mixed.items()
        },
        "polarized_cross_response_coefficients": cross_words,
        "counterguard": (
            "the commutative identities hold exactly, but cancellation is "
            "between distinct site words and is forbidden in a physical source"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h3 axis-pure commutative cohafnian counterguard",
        "pins": PINS,
        "family_identity": family_identity_audit(),
        "countermodel": exact_countermodel_audit(),
        "verdict": (
            "Haf(Q)=x0^3 and the diagonal selected cohafnian sandwich do not "
            "imply a rank or Plucker contradiction in the commutative colour-"
            "count algebra.  A rational 11-edge Q satisfies both.  Its four "
            "nonzero mixed unary word coefficients and its crossed response "
            "coefficients cancel only after forgetting site words.  Therefore "
            "the sharp missing hypothesis is full wordwise polarization (or an "
            "equivalent physical source lift), which immediately exposes an "
            "active mixed carrier in this minimal inverse-rectangle ansatz."
        ),
        "scope": (
            "support-free algebraic counterguard; no finite support enumeration "
            "and no claim that the displayed Q is a physical exact source"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                (digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main():
    ledger, digest = audit()
    print("commutative hafnian/cohafnian equations: EXACT COUNTERMODEL")
    print("selected response block: diag(x1^2,x2^2)")
    print("fully polarized mixed unary words:",
          ledger["countermodel"]["polarized_unary_mixed_coefficients"])
    print("sharp missing datum: WORDWISE PHYSICAL POLARIZATION")
    print("ledger_sha256="+digest)


if __name__ == "__main__":
    main()
