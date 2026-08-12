#!/usr/bin/env python3
"""Identify the rootless bar companion inside the canonical E14 S-pair.

The one-face rootless bar leaves the decorated two-edge matching

    q_(1,23|45) = a23_21*a45_12.

After swapping colours 0 and 2 and relabelling its four vertices, this is
exactly the mixed two-edge factor u05_01*v34_10 in one term of the canonical
E14 unary-times-q S-pair (unary word 000101).  The complete E14 term is

    (p1_0_1*s1_1_1*v24_11) * u05_01*v34_10.

This checker also freezes the important scope guard: the equality is an
equality of the decorated 2K2 core, not of full source-labelled cells.  The
E14 term has three extra factors and repeated physical vertices, while the
rootless marked cube is squarefree.  A source-word-changing promotion is
still required before the rootless bar can fill the E14 first-hit cokernel.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROOTLESS_PATH = (
    "computations/verify_h3_rootless_one_face_third_cofactor_"
    "comparison_vertex_gate.py"
)
E14_PATH = (
    "computations/verify_h3_c6_e14_unary_spair_"
    "first_reduction_boundary.py"
)
PINS = {
    ROOTLESS_PATH:
        "37251145d805861b2d1b15b7bf37cf9f98ba30b03fbcffa1daa4fc35789efe84",
    "notes/h3-rootless-one-face-third-cofactor-comparison-vertex-gate.md":
        "f510e17ea2cfc72452b28e982530a59d60276eb193be6b0fdb7d4e29e4246739",
    E14_PATH:
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "notes/h3-c6-e14-unary-spair-first-reduction-boundary.md":
        "9d3af91f0e97079c8e2bd2dd76db110fdde45e71eed0d21805bdd4575a683c4f",
}
EXPECTED_LEDGER_SHA256 = (
    "4eca64dffe89a87e2a71b2826ff33d3204f3b14c297bba619042db25ebd00446"
)

# Rootless internal sites 2,3,4,5 map to E14 residual sites 0,5,3,4.
ROOT_TO_E14 = {2: 0, 3: 5, 4: 3, 5: 4}
COLOUR_MAP = {0: 2, 1: 1, 2: 0}
E14_UNARY_WORD = (0, 0, 0, 1, 0, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(path, name):
    spec = spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def map_rootless_cell(variable, family):
    require(variable.startswith("a") and "_" in variable,
            f"bad rootless cell {variable}")
    physical, decoration = variable[1:].split("_")
    left, right = map(int, physical)
    a, b = map(int, decoration)
    mapped = [
        (ROOT_TO_E14[left], COLOUR_MAP[a]),
        (ROOT_TO_E14[right], COLOUR_MAP[b]),
    ]
    mapped.sort()
    separator = "_" if family == "u" else ""
    return (f"{family}{mapped[0][0]}{mapped[1][0]}{separator}"
            f"{mapped[0][1]}{mapped[1][1]}")


def site_profile(edges, site_count=8):
    profile = [0] * site_count
    for left, right in edges:
        profile[left] += 1
        profile[right] += 1
    return tuple(profile)


def audit():
    pin_dependencies()
    rootless = load(ROOTLESS_PATH, "rootless_e14_rootless")
    e14_first = load(E14_PATH, "rootless_e14_first")

    root_record = rootless.canonical_cube_and_unit()
    root_q = tuple(root_record["physical_marked_cells"][2:])
    require(root_q == ("a23_21", "a45_12"),
            f"the rootless companion changed: {root_q}")

    mapped_core = (
        map_rootless_cell(root_q[0], "u"),
        map_rootless_cell(root_q[1], "v"),
    )
    require(mapped_core == ("u05_01", "v3410"),
            f"the decorated 2K2 identification changed: {mapped_core}")

    # The mapped decorations agree with the restriction of the canonical
    # E14 unary word to the four vertices of the two-edge core.
    for root_site in (2, 3, 4, 5):
        e14_site = ROOT_TO_E14[root_site]
        require(E14_UNARY_WORD[e14_site]
                == COLOUR_MAP[rootless.PHYSICAL_WORD[root_site]],
                f"source-word restriction failed at root site {root_site}")

    rewrite = e14_first.load(e14_first.REWRITE_PATH,
                             "rootless_e14_rewrite")
    top = rewrite.load(rewrite.TOP_PATH, "rootless_e14_top")
    two = top.load(top.TWO_CELL_PATH, "rootless_e14_two")
    e14 = two.load(two.E14_PATH, "rootless_e14_base")
    b4 = e14.load(e14.B4_PATH, "rootless_e14_b4")
    _candidates, _names, _responses, unary = two.universal(
        e14, b4, 1, 1
    )
    pivot = ("u35_11",)
    factor, remainder = e14_first.factor_unary(
        unary[E14_UNARY_WORD], pivot
    )
    require(factor == {(): -1, ("v0400",): 1},
            f"the canonical unary factor changed: {factor}")
    core_monomial = tuple(sorted(mapped_core))
    require(remainder.get(core_monomial) == 1,
            "the mapped rootless core is absent from the canonical E14 row")

    endpoint = ("p1_0_1", "s1_1_1")
    private_multiplier = ("v2411",)
    promoted_monomial = tuple(sorted(
        endpoint + private_multiplier + core_monomial
    ))
    require(promoted_monomial == tuple(sorted((
        "p1_0_1", "s1_1_1", "u05_01", "v2411", "v3410"
    ))), "the canonical promoted term changed")

    # Full physical profiles cannot be related by a vertex permutation.
    # E14 physical sites are residual 0..5 and external P=6,S=7.
    root_cube_profile = site_profile(((6, 7), (0, 1), (2, 3), (4, 5)))
    e14_promoted_profile = site_profile(
        ((6, 0), (7, 1), (2, 4), (0, 5), (3, 4))
    )
    require(root_cube_profile == (1,) * 8,
            "the rootless marked cube stopped being squarefree")
    require(e14_promoted_profile == (2, 1, 1, 1, 2, 1, 1, 1),
            f"the E14 repeated-site profile changed: {e14_promoted_profile}")
    require(sorted(root_cube_profile) != sorted(e14_promoted_profile),
            "the full source cells unexpectedly became relabellable")

    ledger = {
        "pins": PINS,
        "rootless_companion": list(root_q),
        "site_relabelling_root_to_E14": {
            str(key): value for key, value in sorted(ROOT_TO_E14.items())
        },
        "colour_relabelling_root_to_E14": {
            str(key): value for key, value in sorted(COLOUR_MAP.items())
        },
        "mapped_decorated_2K2_core": list(mapped_core),
        "E14_unary_word": "".join(map(str, E14_UNARY_WORD)),
        "canonical_E14_core_coefficient": "1",
        "canonical_E14_promotion_factor": [*endpoint, *private_multiplier],
        "canonical_E14_promoted_term": list(promoted_monomial),
        "rootless_marked_cube_site_profile": list(root_cube_profile),
        "E14_promoted_term_site_profile": list(e14_promoted_profile),
        "core_identification": (
            "after the displayed site relabelling and colour transposition "
            "0<->2, q_(1,23|45)=a23_21*a45_12 is exactly the mixed "
            "u05_01*v34_10 factor of a canonical word-000101 E14 unary "
            "S-pair tail"
        ),
        "conditional_shared_attachment": (
            "any source-labelled comparison that transports the rootless "
            "bar companion into the E14 endpoint module and permits the "
            "literal multiplier p1_0_1*s1_1_1*v24_11 cancels this canonical "
            "E14 companion with unit coefficient"
        ),
        "scope_guard": (
            "the existing rootless bar supplies only the decorated 2K2 "
            "core.  The full E14 term has the repeated-site profile shown "
            "above and belongs to the unary/G11 endpoint S-pair, whereas "
            "the rootless core is an ordinary-residue companion of source "
            "word 01211222.  Thus no literal full-cell relabelling or source "
            "attachment follows without a grade/word-changing promotion"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"rootless/E14 identification ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 rootless/E14 companion-core identification: PASS (exact)")
    print("rootless=" + "*".join(ledger["rootless_companion"]))
    print("E14_core=" + "*".join(ledger["mapped_decorated_2K2_core"]))
    print("full_cell_relabelling=False")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()
