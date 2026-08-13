#!/usr/bin/env python3
"""Construct one labelled two-direction Hasse/cobar occurrence square.

The shifted P2 placement uses a lower occurrence

    f=(p_0^0,s_1^1,q_45^12)

in word 0112.  Let ``a`` recolour the endpoint site 0 from 0 to 1 and let
``b`` recolour the selected residual site 4 from 1 to 0.  They act on
different literal factors, hence commute while preserving the occurrence
tag.  The four vertices are

    0112 --a--> 1112
      |            |
      b            b
      v            v
    0102 --a--> 1102.

With edge boundaries target minus source and the ordered-bar realization

    [a|b] -> A_0+B_1,        [b|a] -> -(B_0+A_1),

the reduced-cobar boundary ``[a|b]+[b|a]`` is the cubical boundary
``A_0+B_1-A_1-B_0`` and its next boundary is zero.

This constructs the labelled square in the ambient principal-parts source
resolution.  It does not manufacture the occurrence-local physical source
section: committed root covariance is termwise on complete matching rows.
The first missing physical datum is the pointed occurrence/global cap.  If
that one section is granted, root naturality supplies the entire displayed
square.  Its target commutator is zero.  Reinserting q23 forces the separate
``dq23`` face; on the exact P2 private coefficient it has scalar residue zero
but a nonzero labelled detector 35/72.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h2_p2_0112_one_endpoint_hasse_placement_gate.py":
        "8ec18f05034b6483512644c49d0009b4b166b0d6b978f6895195321ca9d8417a",
    "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py":
        "20646d25c248a39d27a8be29332d85b7995e9091e106fc1026fe343847df5eed",
    "computations/verify_h3_selected_lower_excess_orbit_pointed_comparison_gate.py":
        "057ca135e410ccf597a90a034e08868b3c901223981ca68662d6ad72414e4759",
}
EXPECTED_LEDGER_SHA256 = (
    "6006cc5db1e07d60cd2dc724ba5c6c0b7335a2afb64e294bdebb9332736dd490"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


@dataclass(frozen=True)
class Occurrence:
    """Structural tag plus the colours currently carried by its factors."""

    p_site: int
    s_site: int
    residual_sites: tuple[int, int]
    colours: tuple[tuple[int, int], ...]

    def colour(self, site: int) -> int:
        return dict(self.colours)[site]

    @property
    def tag(self) -> tuple[int, int, tuple[int, int]]:
        return self.p_site, self.s_site, self.residual_sites

    def recolour(self, site: int, old: int, new: int) -> "Occurrence":
        require(self.colour(site) == old,
                ("root input colour changed", site, self.colour(site), old))
        colours = dict(self.colours)
        colours[site] = new
        return Occurrence(self.p_site, self.s_site, self.residual_sites,
                          tuple(sorted(colours.items())))

    def word(self, sites: tuple[int, ...]) -> str:
        return "".join(str(self.colour(site)) for site in sites)


@dataclass(frozen=True)
class RootDirection:
    name: str
    site: int
    old: int
    new: int

    def apply(self, occurrence: Occurrence) -> Occurrence:
        return occurrence.recolour(self.site, self.old, self.new)


def add_chains(*chains: Counter[str]) -> Counter[str]:
    answer: Counter[str] = Counter()
    for chain in chains:
        answer.update(chain)
    return Counter({key: value for key, value in answer.items() if value})


def scale(coefficient: int, chain: Counter[str]) -> Counter[str]:
    return Counter({key: coefficient * value for key, value in chain.items()
                    if coefficient * value})


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    sites = (0, 1, 4, 5)
    f00 = Occurrence(
        p_site=0,
        s_site=1,
        residual_sites=(4, 5),
        colours=((0, 0), (1, 1), (4, 1), (5, 2)),
    )
    a = RootDirection("a=E_10 at site 0", 0, 0, 1)
    b = RootDirection("b=E_01 at site 4", 4, 1, 0)
    f10 = a.apply(f00)
    f01 = b.apply(f00)
    f11_ab = b.apply(f10)
    f11_ba = a.apply(f01)
    require(f11_ab == f11_ba,
            "the two site-root directions stopped commuting")
    f11 = f11_ab
    vertices = {"00": f00, "10": f10, "01": f01, "11": f11}
    require([vertices[key].word(sites) for key in ("00", "10", "01", "11")]
            == ["0112", "1112", "0102", "1102"],
            "the literal word square changed")
    require(len({value.tag for value in vertices.values()}) == 1
            and f00.tag == (0, 1, (4, 5)),
            "a root direction changed the occurrence tag")

    # Edge differential is target minus source.  The square is oriented by
    # first a then b minus first b then a.
    edge_boundary = {
        "A0": Counter({"10": 1, "00": -1}),
        "B0": Counter({"01": 1, "00": -1}),
        "A1": Counter({"11": 1, "01": -1}),
        "B1": Counter({"11": 1, "10": -1}),
    }
    square_boundary = Counter({"A0": 1, "B1": 1,
                               "A1": -1, "B0": -1})

    def boundary_edges(chain: Counter[str]) -> Counter[str]:
        return add_chains(*(scale(value, edge_boundary[edge])
                            for edge, value in chain.items()))

    require(not boundary_edges(square_boundary),
            ("cubical boundary stopped squaring to zero",
             boundary_edges(square_boundary)))

    # The Boolean reduced cobar is unsigned on the two ordered splits.  The
    # desuspension/Koszul realization assigns the reversed path a minus sign.
    hasse = load(
        "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py",
        "labelled_occurrence_hasse",
    )
    cobar_first = hasse.cobar_boundary((0b11,))
    cobar_second = hasse.apply_cobar(cobar_first)
    require(cobar_first == Counter({(0b01, 0b10): 1,
                                    (0b10, 0b01): 1})
            and not cobar_second,
            ("the two-direction reduced cobar changed",
             cobar_first, cobar_second))
    ordered_path_realization = {
        (0b01, 0b10): Counter({"A0": 1, "B1": 1}),
        (0b10, 0b01): Counter({"B0": -1, "A1": -1}),
    }
    realized_cobar = add_chains(*(
        scale(coefficient, ordered_path_realization[word])
        for word, coefficient in cobar_first.items()
    ))
    require(realized_cobar == square_boundary
            and not boundary_edges(realized_cobar),
            ("ordered bar signs no longer realize the square",
             realized_cobar))

    # On the GHZ target, the two local site-root operators commute.  Hence
    # the target image of the square commutator ab-ba vanishes.  Individual
    # edges can still have mixed-target normals; their four-face total is the
    # cancellation checked here, not an assertion that every edge is target
    # zero separately.
    target_words = {
        "ab": f11_ab.word(sites),
        "ba": f11_ba.word(sites),
    }
    require(target_words["ab"] == target_words["ba"] == "1102",
            "the target commutator acquired a word defect")

    # Recover the exact private B-4 coefficient which would multiply the
    # occurrence-local sections in the physical P2 repair.  Its scalar
    # augmentation vanishes, but q23 reinsertion forces the same vector in
    # an independent dq23-labelled block.  The old aggregate residue sees
    # zero; the occurrence detector sees 35/72.
    private = load(
        "computations/verify_h2_p2_0102_private_parity_reinsertion_gate.py",
        "labelled_occurrence_private",
    )
    private_ledger, private_digest = private.audit()
    require(private_digest == private.EXPECTED_LEDGER_SHA256,
            "the exact private/reinsertion ledger changed")
    z_private = tuple(map(Q, private_ledger[
        "second_even_Bminus4_debt"]["preimage"]))
    detector = tuple(Q(index in (0, 3)) - Q(index in (1, 6))
                     for index in range(len(z_private)))
    require(sum(z_private, Q(0)) == 0
            and dot(detector, z_private) == Q(35, 72),
            "the labelled dq23/cap obstruction changed")

    # A raw occurrence selector has a nonzero pointed/global zero-face.  The
    # complete response relation gives only the sum of all twelve selectors,
    # so it neither creates a marked section nor kills the private labelled
    # combination.  This is the first physical provenance failure; target
    # cancellation occurs only after such a section has been supplied.
    occurrence_unit = tuple(Q(index == 0) for index in range(len(z_private)))
    complete_response = (Q(1),) * len(z_private)
    pointed_dual = tuple(Q(index == 0) - Q(index == 1)
                         for index in range(len(z_private)))
    require(sum(occurrence_unit, Q(0)) == 1
            and dot(pointed_dual, complete_response) == 0
            and dot(pointed_dual, occurrence_unit) == 1,
            "the marked occurrence/complete-response separation changed")

    ledger = {
        "theorem": "one labelled two-direction occurrence Hasse/cobar square",
        "pins": PINS,
        "marked_occurrence": {
            "tag": "(p_site=0,s_site=1,residual_sites=(4,5))",
            "factor": "p0^0 s1^1 q45^12",
            "base_word": "0112",
            "reinsertion": "q23^21",
        },
        "ordered_roots": {
            "a": a.name,
            "b": b.name,
            "act_on_distinct_factors": True,
            "commute_on_marked_occurrence": True,
        },
        "vertices": {key: value.word(sites)
                     for key, value in vertices.items()},
        "occurrence_tag_preserved_at_all_vertices": True,
        "edge_boundaries": {
            edge: dict(sorted(boundary.items()))
            for edge, boundary in edge_boundary.items()
        },
        "ordered_bar_realization": {
            "[a|b]": "A0+B1",
            "[b|a]": "-(B0+A1)",
            "cobar_boundary": "[a|b]+[b|a]",
            "cubical_boundary": "A0+B1-A1-B0",
            "d_squared": 0,
        },
        "source_provenance": {
            "ambient_complete_PP_square": True,
            "reason": (
                "the pinned physical Cartan theorem makes site-root fields "
                "source-provenant on complete matching rows, and the pinned "
                "Hasse theorem totalizes their commuting product-rule faces"
            ),
            "occurrence_local_section_constructed": False,
            "first_failure": (
                "the complete response row supplies only the sum of the "
                "twelve occurrence coordinates; it does not supply the "
                "marked pointed occurrence/global section"
            ),
            "conditional_positive_statement": (
                "one pointed source-valid occurrence section, functorial for "
                "the two site-root PP operators and q23 reinsertion, supplies "
                "the entire displayed square; no recursive unlabelled cells "
                "are needed for this occurrence"
            ),
        },
        "augmented_faces": {
            "word": "four typed quiver objects 0112,1112,0102,1102",
            "fine_grade": (
                "root-recoloured at the indicated site; the structural "
                "occurrence tag and repeated P3+K2 reinsertion label stay fixed"
            ),
            "target": (
                "individual edges may carry mixed-target normals, but the "
                "two ordered paths have the same target word and their square "
                "commutator is zero"
            ),
            "pointed_cap": (
                "first unconstructed physical face: the marked/global "
                "occurrence conormal (the degree-zero pointed section)"
            ),
            "q23_product_rule": "d(q23*S)=q23*dS+dq23*S",
            "scalar_ordinary_residue_on_z_private": "0",
            "labelled_dq23_residue_on_z_private": [str(value)
                                                     for value in z_private],
            "labelled_detector_value": "35/72",
            "labelled_face_cancelled_by_aggregate_residue": False,
        },
        "verdict": (
            "the labelled Hasse/cobar square is explicit and finite.  One "
            "fully pointed occurrence section would generate it, but no "
            "committed physical map selects that occurrence from a complete "
            "response row.  The first failure is the pointed cap; after it is "
            "granted, target commutator cancels and the next nonzero proper "
            "face is the labelled dq23 conormal, invisible to scalar residue"
        ),
        "scope": (
            "one literal 0112 occurrence and its two ordered site-root "
            "directions.  The result does not assert that one seed spans the "
            "other occurrence/site orbits, nor promote the displayed detector "
            "to a full physical q/Fredholm terminal"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("labelled occurrence square changed", digest,
                 EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("one-occurrence words: 0112 -> {1112,0102} -> 1102")
    print("ordered bar: [a|b]+[b|a] -> A0+B1-A1-B0")
    print("labelled square d^2=0: PASS")
    print("physical occurrence section: NOT CONSTRUCTED")
    print("first physical face: POINTED CAP; next labelled dq23=35/72")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
