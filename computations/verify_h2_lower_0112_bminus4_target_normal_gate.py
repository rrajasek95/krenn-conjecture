#!/usr/bin/env python3
"""Audit the target-normal face of the natural h=2 (B-4I) lift.

The marked lower packet has sites (0,1,4,5), word 0112, and marked
occurrence f=(0,1;45).  An endpoint-adjacency edge replaces one endpoint x
by a residual site t and pairs x with the old mate of t.  The natural
word-returning path is the site swap (x t), followed (when the two site
colours differ) by the simultaneous signed colour Weyl swap at x,t.

On the GHZ target the site swap is invisible, while the two-root Weyl path
has normal (w_xt-1)Delta.  Summing the four endpoint moves from f gives

  N_f = X1010+X0101+X2002+X0220+X1212+X2121-2*Delta_4.

Thus even granting the common H0 target line Q*Delta_4 leaves six mixed
target normals.  The primitive reduced cap has target zero, so it cannot
cancel them.  The same obstruction survives the exact rational preimage
v=-(B+6)c_plus/24 used in c_plus=(B-4)v; after denominator clearing its
primitive target normal is computed below.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_lower_centered_endpoint_parity_terminal_fork.py":
        "47ea1f915429dc7937ef2e81037c0494136d9ae379d76e0584bb22cef8e0d390",
    "notes/h2-lower-centered-endpoint-parity-terminal-fork.md":
        "27d25d400daf8c26ff0da928a21cbfd3116058308799f3080cdcae8ae979ddbd",
    "notes/h3-centered-occurrence-same-grade-physical-gate.md":
        "b183f3b5dab83fa79d17c3f539b9f146e3be176a96bfe52b267529148b64134a",
    "computations/verify_h2_lower_centered_orientation_terminal_fork.py":
        "6758c86ec151834d121e5b41b1dae677592cc4224c3aaad95d6f8321b826d3b2",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "notes/h3-physical-cartan-source-orbit-descent.md":
        "4f0ab9035124319cc491bb2cc9914ef58ced228774f41625699e8c1cb2ca65d1",
    "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py":
        "d5c90e6404670c7b666b6aa2b3448f5f16c2aebc7fac47f749fb269250413a28",
    "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md":
        "48e39dd9e2667208eb2a08d98aa5dc58151daeaa7029437270d92a966c9e2542",
    "notes/uniform-physical-bar-occurrence-splitter-cokernel.md":
        "5aecb6fecbb3dffc720efaeb412d366a4c4c7b4475f61535280cc0df4c2b3007",
    "computations/verify_h2_b4_cplus_shared_interface_gate.py":
        "ee48f2d1446d938fc97cda4e0977472081ee9823d31dc91f3f4c46829f3d8400",
    "notes/h2-b4-cplus-shared-interface-gate.md":
        "4c89253c18f4475371849a78c990e27b7d6af79193522cd5a583af80cc929fb8",
}
EXPECTED_LEDGER_SHA256 = (
    "bb42b0ff6cefa8cecee5338482257b72dc133c1e1bcc6b96f24baac1019eb863"
)

SITES = (0, 1, 4, 5)
SITE_INDEX = {site: index for index, site in enumerate(SITES)}
COLOUR = {0: 0, 1: 1, 4: 1, 5: 2}
TARGET_WORDS = tuple(
    (a, b, c, d)
    for a in range(3) for b in range(3)
    for c in range(3) for d in range(3)
)
ZERO_TARGET = (Q(0),) * len(TARGET_WORDS)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load_parity_module():
    relative = (
        "computations/"
        "verify_h2_lower_centered_endpoint_parity_terminal_fork.py"
    )
    specification = importlib.util.spec_from_file_location(
        "h2_lower_parity", ROOT / relative
    )
    require(specification is not None and specification.loader is not None,
            "cannot load lower parity module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum(entries, Q(0))
                 for entries in zip(*vectors, strict=True))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * entry for entry in vector)


def dot(left, right):
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def target_unit(word):
    require(word in TARGET_WORDS, ("bad target word", word))
    return tuple(Q(word == candidate) for candidate in TARGET_WORDS)


def delta_target():
    return add(*(target_unit((colour,) * 4) for colour in range(3)))


def two_root_weyl(word, left_site, right_site):
    """Apply the even signed Weyl swap for the colours at two sites.

    A signed SL2 Weyl sends a -> -b and b -> a.  Because it acts at two
    sites, every image of a monochromatic GHZ word has positive sign.
    """
    left_colour = COLOUR[left_site]
    right_colour = COLOUR[right_site]
    if left_colour == right_colour:
        return word
    answer = list(word)
    for site in (left_site, right_site):
        index = SITE_INDEX[site]
        if answer[index] == left_colour:
            answer[index] = right_colour
        elif answer[index] == right_colour:
            answer[index] = left_colour
    return tuple(answer)


def target_defect(left_site, right_site):
    if COLOUR[left_site] == COLOUR[right_site]:
        return ZERO_TARGET
    images = add(*(
        target_unit(two_root_weyl((colour,) * 4, left_site, right_site))
        for colour in range(3)
    ))
    return add(images, scale(-1, delta_target()))


def sparse(vector):
    return {
        "".join(map(str, word)): str(coefficient)
        for word, coefficient in zip(TARGET_WORDS, vector, strict=True)
        if coefficient
    }


def reinstate(word):
    """Insert q23:21 and q67:22 into a lower target word."""
    values = {
        0: word[0], 1: word[1], 2: 2, 3: 1,
        4: word[2], 5: word[3], 6: 2, 7: 2,
    }
    return "".join(str(values[site]) for site in range(8))


def marked_local_normal_audit():
    marked = (0, 1, ((4, 5),))
    moves = (
        (0, 4, (4, 1, ((0, 5),))),
        (1, 4, (0, 4, ((1, 5),))),
        (0, 5, (5, 1, ((0, 4),))),
        (1, 5, (0, 5, ((1, 4),))),
    )
    defects = []
    records = []
    for endpoint, selected, neighbor in moves:
        defect = target_defect(endpoint, selected)
        defects.append(defect)
        records.append({
            "endpoint_move": f"{endpoint}->{selected}",
            "neighbour": repr(neighbor),
            "colour_pair": [COLOUR[endpoint], COLOUR[selected]],
            "site_swap": f"({endpoint} {selected})",
            "two_root_Weyl_needed": COLOUR[endpoint] != COLOUR[selected],
            "target_defect": sparse(defect),
        })
    local_normal = add(*defects)
    expected = add(
        target_unit((1, 0, 1, 0)), target_unit((0, 1, 0, 1)),
        target_unit((2, 0, 0, 2)), target_unit((0, 2, 2, 0)),
        target_unit((1, 2, 1, 2)), target_unit((2, 1, 2, 1)),
        scale(-2, delta_target()),
    )
    require(local_normal == expected,
            ("marked B-4 target normal changed", sparse(local_normal)))
    mixed_dual = target_unit((1, 0, 1, 0))
    require(dot(mixed_dual, delta_target()) == 0
            and dot(mixed_dual, local_normal) == 1,
            "primitive mixed target dual changed")
    full_words = {
        reinstate(word): str(coefficient)
        for word, coefficient in zip(TARGET_WORDS, local_normal, strict=True)
        if coefficient
    }
    require(len(full_words) == 9
            and full_words["10211022"] == "1"
            and full_words["00210022"] == "-2",
            ("reinserted target normal changed", full_words))
    return {
        "lower_sites": list(SITES),
        "lower_word": "0112",
        "marked_occurrence": repr(marked),
        "B_neighbours": records,
        "same_colour_target_safe_moves": 1,
        "root_decorated_moves": 3,
        "marked_B_minus_4_target_normal": sparse(local_normal),
        "formula": (
            "1010+0101+2002+0220+1212+2121"
            "-2*(0000+1111+2222)"
        ),
        "reinserted_target_words": full_words,
        "common_H0_granted_target_line": "Q*Delta_4",
        "primitive_cap_target": 0,
        "mixed_dual": "X_1010^*",
        "mixed_dual_on_H0_and_cap": 0,
        "mixed_dual_on_marked_normal": 1,
    }


def hole_normal(hole):
    complement = tuple(site for site in SITES if site not in hole)
    return add(*(target_defect(endpoint, residual)
                 for endpoint in hole for residual in complement))


def centered_preimage_normal_audit():
    parity = load_parity_module()
    occurrence, values, lookup, _swap, b_matrix, _s_matrix = (
        parity.endpoint_data()
    )
    # Relabel the canonical four-site occurrence module to actual sites
    # (0,1,4,5).  Its marked hole remains the first pair.
    relabel = {0: 0, 1: 1, 2: 4, 3: 5}
    size = len(values)
    identity = parity.identity(size)
    marked_index = next(index for index, value in enumerate(values)
                        if value[:2] == (0, 1))
    swapped_index = next(index for index, value in enumerate(values)
                         if value[:2] == (1, 0))
    c_plus = tuple(
        Q(6 if index in (marked_index, swapped_index) else 0) - 1
        for index in range(size)
    )
    preimage = scale(
        Q(-1, 24),
        parity.matvec(
            parity.matrix_add(b_matrix, parity.matrix_scale(6, identity)),
            c_plus,
        ),
    )
    b_minus_four = parity.matrix_add(
        b_matrix, parity.matrix_scale(-4, identity)
    )
    require(parity.matvec(b_minus_four, preimage) == c_plus,
            "the exact B-4 preimage changed")
    require(all((12 * value).denominator == 1 for value in preimage),
            "the denominator-12 preimage changed")

    total_normal = ZERO_TARGET
    hole_weights = {}
    for value, coefficient in zip(values, preimage, strict=True):
        p_site, s_site, _matching = value
        actual_hole = tuple(sorted((relabel[p_site], relabel[s_site])))
        total_normal = add(total_normal,
                           scale(coefficient, hole_normal(actual_hole)))
        hole_weights.setdefault(actual_hole, coefficient)
        require(hole_weights[actual_hole] == coefficient,
                "the even preimage lost orientation symmetry")

    primitive = scale(Q(3, 2), total_normal)
    expected_primitive = add(
        scale(2, target_unit((0, 0, 1, 1))),
        scale(2, target_unit((1, 1, 0, 0))),
        scale(2, target_unit((1, 1, 2, 2))),
        scale(2, target_unit((2, 2, 1, 1))),
        scale(-1, target_unit((0, 1, 0, 1))),
        scale(-1, target_unit((0, 2, 2, 0))),
        scale(-1, target_unit((1, 0, 1, 0))),
        scale(-1, target_unit((1, 2, 1, 2))),
        scale(-1, target_unit((2, 0, 0, 2))),
        scale(-1, target_unit((2, 1, 2, 1))),
        scale(-2, target_unit((1, 1, 1, 1))),
    )
    require(primitive == expected_primitive,
            ("centered B-4 target normal changed", sparse(primitive)))
    mixed_dual = target_unit((0, 0, 1, 1))
    require(dot(mixed_dual, delta_target()) == 0
            and dot(mixed_dual, primitive) == 2,
            "centered primitive target dual changed")
    return {
        "identity": "c_plus=(B-4)*(-(B+6)c_plus/24)",
        "preimage_denominator": 12,
        "even_hole_weights_per_orientation": {
            "".join(map(str, hole)): str(value)
            for hole, value in sorted(hole_weights.items())
        },
        "target_normal": sparse(total_normal),
        "primitive_target_normal_scale": "(3/2)*target_normal",
        "primitive_target_normal": sparse(primitive),
        "primitive_mixed_dual": "X_0011^*",
        "primitive_mixed_dual_on_H0_and_cap": 0,
        "primitive_mixed_dual_value": 2,
        "target_normal_zero": False,
    }


def physical_scope_audit():
    cartan = (ROOT / "notes/h3-physical-cartan-source-orbit-descent.md").read_text()
    cap = (ROOT / (
        "notes/h3-centered-endpoint-projector-primitive-cap-lift-gate.md"
    )).read_text()
    orientation = (ROOT / (
        "computations/verify_h2_lower_centered_orientation_terminal_fork.py"
    )).read_text()
    same_grade = (ROOT / (
        "notes/h3-centered-occurrence-same-grade-physical-gate.md"
    )).read_text()
    shared_cplus = (ROOT / "notes/h2-b4-cplus-shared-interface-gate.md").read_text()
    require("permutations preserve the GHZ target" in
            (ROOT / "notes/uniform-physical-bar-occurrence-splitter-cokernel.md").read_text()
            and "target defect is invariant" in cartan,
            "site/Weyl target scope changed")
    cap_checker = (ROOT / (
                "computations/verify_h3_centered_endpoint_projector_primitive_cap_lift_gate.py"
            )).read_text()
    require("with `Omega`, rootless ridge, `Eq`, `W`, target" in cap
            and 'p = (0, -1, 0, 0, 0, 0, -1, 0, 0, 0)' in cap_checker
            and '("Omega", "rootless_ridge", "Eq", "W", "target"' in
            cap_checker,
            "primitive cap target-zero scope changed")
    require("one-endpoint product-rule face" in orientation,
            "lower one-endpoint Hasse scope changed")
    require("zero target/residue/physical-terminal projection" in same_grade,
            "complete H0 target-zero scope changed")
    require("independent, target-bearing" in shared_cplus
            and "one-endpoint product-rule cross term" in shared_cplus,
            "shared C-plus target interface changed")
    return {
        "natural_edge_path": (
            "g_xt=(x t)*w_xt, where w_xt is the two-site signed Weyl "
            "between the colours at x,t; g_xt fixes the lower word and "
            "sends the occurrence to its B-neighbour"
        ),
        "target_boundary": (
            "(g_xt-1)Delta=(w_xt-1)Delta because the site swap fixes Delta"
        ),
        "product_rule": (
            "d(a_f H_xt)=a_f(g_xt-1)+(d a_f) H_xt; cancellation of the "
            "displayed target normal still leaves the occurrence-local "
            "one-endpoint Hasse cross term"
        ),
        "H0_cap_verdict": (
            "the pinned complete H0 row and p_(v,N) both have target zero. "
            "Even artificially granting H0 the entire Delta line cancels "
            "only the pure part; mixed normal coordinates survive"
        ),
        "minimal_new_column": (
            "an occurrence-local mixed-target cone section for the six "
            "root-decorated endpoint moves, totalized with their first "
            "Hasse faces in word 0112 and the reinserted P3+K2 grade"
        ),
        "relation_to_C_plus": (
            "this is the lower-word target face of the independently "
            "target-bearing rho-even C_plus interface; the coefficient "
            "landing agrees, but the source-labelled restriction map is "
            "still absent"
        ),
        "dual_scope": (
            "the mixed-coordinate dual is exact modulo common H0 and the "
            "primitive cap, but is not a physical Fredholm terminal until "
            "extended across every mixed target-cone/protected/q column"
        ),
    }


def audit():
    pin_dependencies()
    ledger = {
        "theorem": "h2 lower 0112 B-4 target-normal gate",
        "pins": PINS,
        "marked_local_normal": marked_local_normal_audit(),
        "centered_preimage_normal": centered_preimage_normal_audit(),
        "physical_scope": physical_scope_audit(),
        "verdict": (
            "The natural occurrence-local endpoint Cartan/site path does "
            "not give a target-safe B-4 lift in lower word 0112.  Three of "
            "the four marked endpoint moves carry two-root Weyl normal; "
            "their sum is six mixed target words minus 2*Delta_4.  Common "
            "H0 can remove at most the Delta part and the primitive cap has "
            "target zero.  The exact B-4 preimage of c_plus retains a "
            "nonzero eleven-word target normal.  Hence the first missing "
            "physical datum is an occurrence-local mixed-target cone "
            "section with its one-endpoint Hasse cross term, or a dual "
            "extending across that complete augmented cone."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("lower 0112 B-4 target-normal ledger changed", digest))
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("marked B-4 natural target normal: SIX MIXED - 2*DELTA")
    print("common H0 + primitive cap cancellation: INSUFFICIENT")
    print("exact centered B-4 preimage target normal: NONZERO")
    print("first new datum: OCCURRENCE-LOCAL MIXED TARGET CONE + HASSE FACE")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
