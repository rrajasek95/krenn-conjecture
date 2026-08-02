#!/usr/bin/env python3
"""Exact finite audit of the augmented homological-perturbation formula.

This is an abstract algebra checker.  It proves neither existence of the
source-labelled hafnian contraction nor the clean-pair bridge.
"""

from fractions import Fraction
from hashlib import sha256
import json


QQ = Fraction
EXPECTED_DIGEST = "93f041e93f1e0b6e1968c709a4215600b60358066c46885cec9bea00b228f6e4"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scalar=QQ(1)):
    for key, value in source.items():
        result = target.get(key, QQ(0)) + scalar * value
        if result:
            target[key] = result
        else:
            target.pop(key, None)
    return target


def apply(linear_map, vector):
    answer = {}
    for key, coefficient in vector.items():
        add(answer, linear_map.get(key, {}), coefficient)
    return answer


def compose(left, right, vector):
    return apply(left, apply(right, vector))


def identity_on(basis):
    return {key: {key: QQ(1)} for key in basis}


def equal_maps(first, second, domain):
    return all(
        apply(first, {key: QQ(1)}) == apply(second, {key: QQ(1)})
        for key in domain
    )


def audit():
    # H has x,A,B,C,D.  C adds one acyclic pair u -> v.
    c_basis = ("x", "A", "B", "C", "D", "u", "v")
    h_basis = ("x", "A", "B", "C", "D")
    d0 = {"u": {"v": QQ(1)}}
    homotopy = {"v": {"u": QQ(1)}}
    inclusion = identity_on(h_basis)
    projection = identity_on(h_basis)

    # Check d0 h + h d0 = 1 - i p and the side conditions.
    for key in c_basis:
        left = compose(d0, homotopy, {key: QQ(1)})
        add(left, compose(homotopy, d0, {key: QQ(1)}))
        right = {key: QQ(1)}
        add(right, compose(inclusion, projection, {key: QQ(1)}), QQ(-1))
        require(left == right, f"contraction identity failed at {key}")
    require(all(not compose(projection, homotopy, {key: QQ(1)})
                for key in c_basis), "ph is nonzero")
    require(all(not compose(homotopy, inclusion, {key: QQ(1)})
                for key in h_basis), "hi is nonzero")
    require(all(not compose(homotopy, homotopy, {key: QQ(1)})
                for key in c_basis), "h^2 is nonzero")

    # This is the exact toy transfer used by the local C4 audit.
    delta = {
        "x": {"A": QQ(-1), "B": QQ(-1), "C": QQ(-1), "v": QQ(1)},
        "u": {"D": QQ(-1)},
    }
    total = dict(d0)
    for key in c_basis:
        image = apply(d0, {key: QQ(1)})
        add(image, apply(delta, {key: QQ(1)}))
        if image:
            total[key] = image
        else:
            total.pop(key, None)
    for key in c_basis:
        require(not compose(total, total, {key: QQ(1)}),
                f"perturbed differential does not square to zero at {key}")

    # I = i - h delta i; higher terms vanish in this toy model.
    perturbed_inclusion = {}
    for key in h_basis:
        image = apply(inclusion, {key: QQ(1)})
        add(image, compose(homotopy, delta,
                           apply(inclusion, {key: QQ(1)})), QQ(-1))
        perturbed_inclusion[key] = image

    # D1=p delta i and D2=-p delta h delta i.
    d1 = {}
    d2 = {}
    transferred = {}
    for key in h_basis:
        source = apply(inclusion, {key: QQ(1)})
        first = compose(projection, delta, source)
        second_source = compose(homotopy, delta, source)
        second = compose(projection, delta, second_source)
        second = {item: -value for item, value in second.items()}
        if first:
            d1[key] = first
        if second:
            d2[key] = second
        combined = dict(first)
        add(combined, second)
        if combined:
            transferred[key] = combined

    require(d1 == {"x": {"A": -1, "B": -1, "C": -1}},
            "first transferred differential changed")
    require(d2 == {"x": {"D": 1}},
            "second transferred differential changed")
    require(transferred == {
        "x": {"A": -1, "B": -1, "C": -1, "D": 1}
    }, "total transferred differential changed")

    for key in h_basis:
        lhs = compose(total, perturbed_inclusion, {key: QQ(1)})
        rhs = compose(perturbed_inclusion, transferred, {key: QQ(1)})
        require(lhs == rhs, f"perturbed inclusion is not a chain map at {key}")
        require(not compose(transferred, transferred, {key: QQ(1)}),
                f"transferred differential does not square to zero at {key}")

    # A second two-generator example isolates the augmented terminal formula.
    # d0(u)=v and delta(x)=v, so the perturbed cycle representing x is x-u.
    terminal_basis = ("x", "u", "v")
    terminal_d0 = {"u": {"v": QQ(1)}}
    terminal_h = {"v": {"u": QQ(1)}}
    terminal_delta = {"x": {"v": QQ(1)}}
    terminal_total = {"x": {"v": QQ(1)}, "u": {"v": QQ(1)}}
    terminal_I = {"x": {"x": QQ(1), "u": QQ(-1)}}
    augmentation = {"u": {"target": QQ(1)}}
    for key in terminal_basis:
        require(not compose(augmentation, terminal_total, {key: QQ(1)}),
                "terminal augmentation does not kill total boundaries")
    naive = compose(augmentation, {"x": {"x": QQ(1)}}, {"x": QQ(1)})
    corrected = compose(augmentation, terminal_I, {"x": QQ(1)})
    require(not naive, "naive terminal readout should miss the correction")
    require(corrected == {"target": QQ(-1)},
            "corrected terminal augmentation changed")
    require(not compose(terminal_total, terminal_I, {"x": QQ(1)}),
            "corrected terminal representative is not a total cycle")

    ledger = {
        "contraction_basis": list(c_basis),
        "first_transfer": {key: int(value) for key, value in d1["x"].items()},
        "second_transfer": {key: int(value) for key, value in d2["x"].items()},
        "total_transfer": {
            key: int(value) for key, value in transferred["x"].items()
        },
        "terminal_naive_readout": {},
        "terminal_corrected_representative": {
            key: int(value) for key, value in terminal_I["x"].items()
        },
        "terminal_corrected_readout": {
            key: int(value) for key, value in corrected.items()
        },
        "conclusion": (
            "the augmented physical readout must use the perturbed inclusion; "
            "the second transfer is canonical on first-page homology"
        ),
        "scope_guard": (
            "abstract exact algebra only; no literal hafnian contraction is built"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FROZEN":
        require(digest == EXPECTED_DIGEST, "ledger digest changed")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("augmented HPL terminal/Bockstein lemma: PASS")
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()
