#!/usr/bin/env python3
"""Audit the dual polar/forced-diagonal boundary on common-coloop fibres.

The exact response quotient has a polar map D, three anchor-coordinate
rows H, a residual b, and diagonal offsets kappa.  This checker proves by
independent rational row reduction that:

* b misses im(D) exactly when a left annihilator of D detects b;
* on a consistent fibre, diagonal i is forced zero exactly when a covector
  lambda satisfies lambda D=H_i and lambda b=-kappa_i; and
* the fixed nonzero missing diagonal in every one-corner branch can never
  be forced zero.

It exercises every possible missing label, positive, cokernel, nonmissing
forced, and sharp fixed-zero strata.  Standard library only; live under
-O and -I -S.  Research evidence only.
"""

from fractions import Fraction
from hashlib import sha256


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def q(value):
    return value if isinstance(value, Fraction) else Fraction(value)


def matrix(rows):
    result = tuple(tuple(q(value) for value in row) for row in rows)
    if result:
        require(all(len(row) == len(result[0]) for row in result),
                "a ragged matrix was supplied")
    return result


def transpose(source):
    if not source:
        return ()
    return tuple(
        tuple(source[row][column] for row in range(len(source)))
        for column in range(len(source[0]))
    )


def dot(left, right):
    require(len(left) == len(right), "dot-product dimensions disagree")
    return sum(a * b for a, b in zip(left, right))


def matvec(source, vector):
    require(not source or len(source[0]) == len(vector),
            "matrix/vector dimensions disagree")
    return tuple(dot(row, vector) for row in source)


def rref(source):
    work = [list(row) for row in source]
    if not work:
        return (), ()
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    pivots = []
    for pivot_column in range(columns):
        selected = next(
            (row for row in range(pivot_row, rows)
             if work[row][pivot_column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][pivot_column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = work[row][pivot_column]
            if factor:
                work[row] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry
                    in zip(work[row], work[pivot_row])
                ]
        pivots.append(pivot_column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def solve(source, target):
    require(len(source) == len(target),
            "linear-system row count changed")
    if not source:
        return (), ()
    width = len(source[0])
    augmented = tuple(
        tuple(row) + (value,)
        for row, value in zip(source, target)
    )
    reduced, augmented_pivots = rref(augmented)
    if width in augmented_pivots:
        return None
    pivots = tuple(pivot for pivot in augmented_pivots if pivot < width)
    free = tuple(index for index in range(width) if index not in pivots)
    pivot_rows = {pivot: row for row, pivot in enumerate(pivots)}
    particular = [Fraction(0) for _ in range(width)]
    for pivot in pivots:
        particular[pivot] = reduced[pivot_rows[pivot]][-1]
    kernel = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(width)]
        vector[free_column] = 1
        for pivot in pivots:
            vector[pivot] = -reduced[pivot_rows[pivot]][free_column]
        kernel.append(tuple(vector))
    return tuple(particular), tuple(kernel)


def nullspace(source):
    require(source, "nullspace needs an explicit ambient width")
    result = solve(
        source, tuple(Fraction(0) for _ in range(len(source)))
    )
    require(result is not None, "a homogeneous system became inconsistent")
    return result[1]


def one_corner_anchor(missing):
    nonmissing = tuple(label for label in range(3) if label != missing)
    rows = [[0, 0, 0] for _ in range(3)]
    rows[nonmissing[0]][0] = 1
    rows[nonmissing[1]][1] = 1
    return matrix(rows), nonmissing


def coker_witness(polar, residual):
    witnesses = tuple(
        covector for covector in nullspace(transpose(polar))
        if dot(covector, residual)
    )
    return witnesses


def forced_dual_witness(polar, residual, anchor_row, offset):
    result = solve(transpose(polar), anchor_row)
    if result is None:
        return None
    particular, homogeneous = result
    values = {dot(particular, residual)}
    values.update(dot(
        tuple(particular[index] + vector[index]
              for index in range(len(particular))),
        residual,
    ) for vector in homogeneous)
    require(len(values) == 1,
            ("a consistent residual changed a dual affine value", values))
    return particular if dot(particular, residual) == -offset else None


def classify(case):
    polar = case["polar"]
    anchor = case["anchor"]
    residual = case["residual"]
    offsets = case["offsets"]
    require(len(anchor) == len(offsets) == 3,
            ("the diagonal ledger changed", case["name"]))
    primal = solve(polar, residual)
    cokernel = coker_witness(polar, residual)
    require((primal is None) == bool(cokernel),
            ("primal/dual cokernel tests disagree",
             case["name"], primal, cokernel))
    if primal is None:
        for witness in cokernel:
            require(matvec(transpose(polar), witness)
                    == tuple(Fraction(0) for _ in anchor[0]),
                    ("a cokernel witness does not annihilate D",
                     case["name"], witness))
            require(dot(witness, residual),
                    ("a cokernel witness misses b",
                     case["name"], witness))
        return {
            "consistent": False,
            "forced": (),
            "cokernel_dimension": len(nullspace(transpose(polar))),
            "detecting_cokernel": len(cokernel),
        }

    point, kernel = primal
    forced_primal = []
    forced_dual = []
    dual_witnesses = {}
    for label, (anchor_row, offset) in enumerate(zip(anchor, offsets)):
        value = offset + dot(anchor_row, point)
        is_forced = not value and all(
            not dot(anchor_row, direction) for direction in kernel
        )
        if is_forced:
            forced_primal.append(label)
        witness = forced_dual_witness(
            polar, residual, anchor_row, offset
        )
        if witness is not None:
            forced_dual.append(label)
            dual_witnesses[label] = witness
            require(matvec(transpose(polar), witness) == anchor_row,
                    ("a forced witness does not transport A through D",
                     case["name"], label, witness))
            require(dot(witness, residual) == -offset,
                    ("a forced witness has the wrong affine constant",
                     case["name"], label, witness))
    require(tuple(forced_primal) == tuple(forced_dual),
            ("primal/dual forced tests disagree",
             case["name"], forced_primal, forced_dual))
    return {
        "consistent": True,
        "forced": tuple(forced_primal),
        "cokernel_dimension": len(nullspace(transpose(polar))),
        "detecting_cokernel": 0,
        "dual_witnesses": dual_witnesses,
    }


def one_corner_cases():
    cases = []
    for missing in range(3):
        anchor, nonmissing = one_corner_anchor(missing)
        first, second = nonmissing

        offsets = [Fraction(1), Fraction(1), Fraction(1)]
        offsets[first] = -1
        cases.append({
            "name": f"missing-{missing}-nonmissing-forced-{first}",
            "missing": missing,
            "anchor": anchor,
            "polar": matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1))),
            "residual": (Fraction(1), Fraction(2), Fraction(0)),
            "offsets": tuple(offsets),
            "expected": (True, (first,)),
        })

        cases.append({
            "name": f"missing-{missing}-active-kernel",
            "missing": missing,
            "anchor": anchor,
            "polar": matrix(((1, 0, 0),)),
            "residual": (Fraction(1),),
            "offsets": (Fraction(1), Fraction(1), Fraction(1)),
            "expected": (True, ()),
        })

        cases.append({
            "name": f"missing-{missing}-polar-cokernel",
            "missing": missing,
            "anchor": anchor,
            "polar": matrix(((1, 0, 0), (0, 0, 0))),
            "residual": (Fraction(0), Fraction(1)),
            "offsets": (Fraction(1), Fraction(1), Fraction(1)),
            "expected": (False, ()),
        })

        sharp_offsets = [Fraction(1), Fraction(1), Fraction(1)]
        sharp_offsets[missing] = 0
        cases.append({
            "name": f"missing-{missing}-fixed-zero-sharp",
            "missing": missing,
            "anchor": anchor,
            "polar": matrix(((1, 0, 0),)),
            "residual": (Fraction(1),),
            "offsets": tuple(sharp_offsets),
            "expected": (True, (missing,)),
        })
    return tuple(cases)


def audit():
    ledger = []
    for case in one_corner_cases():
        result = classify(case)
        observed = result["consistent"], result["forced"]
        require(observed == case["expected"],
                ("a one-corner dual stratum changed",
                 case["name"], observed))
        missing = case["missing"]
        if case["offsets"][missing]:
            require(missing not in result["forced"],
                    ("a fixed nonzero missing diagonal was forced",
                     case["name"], result))
        else:
            require(missing in result["forced"],
                    ("the fixed-zero sharp boundary disappeared",
                     case["name"], result))
        ledger.append(
            f"{case['name']}:{int(result['consistent'])}:"
            + ",".join(str(label) for label in result["forced"])
            + f":{result['cokernel_dimension']}:"
            f"{result['detecting_cokernel']}"
        )
    return tuple(ledger)


EXPECTED_LEDGER_DIGEST = (
    "5384677b2b3f009baff38b05598cdea4271a3df4a34e66306e5b23a37f795a3d"
)


def main():
    ledger = audit()
    digest = sha256("\n".join(ledger).encode("utf-8")).hexdigest()
    require(digest == EXPECTED_LEDGER_DIGEST,
            ("the polar-dual case ledger changed", digest))
    print("common-coloop polar dual forced-diagonal boundary: PASS")
    print(f"  exact branch cases          : {len(ledger)}")
    print(f"  case ledger                : {ledger}")
    print(f"  case-ledger digest         : {digest}")
    print("  closed forced stratum      : fixed nonzero missing diagonal")
    print("  residual                   : cokernel or two labelled overlap covectors")


if __name__ == "__main__":
    main()
