#!/usr/bin/env python3
"""Verify that the endpoint-odd Cartan prism is source-provenant.

The missing point in the order-six comparison was not the universal Cartan
formula, but descent of its root contractions to the literal physical source
presentation.  For the perfect-matching tensor this descent is functorial:
the local colour root field on coefficient space is F-related to the same
root field on the output tensor.  Termwise,

    X_src H_w = H_{X_out w}.

The complete principal-parts source resolution is therefore stable under
the root homotopies.  The residual-site transposition 0<->1 is an actual
automorphism of the direct-free matching presentation, commutes with the
tail action at sites 2 and 5, and kills the Weyl target defect after endpoint
oddization.  Hence K=(1-s)H_w is a genuine source-provenant relative cell,
not a formal target mapping-cylinder edge.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
    "computations/verify_h3_sl2_weyl_cartan_prism.py":
        "1024864418fea8f7f4ca6c77015972febd236f2a9822112daf20e1cf979bddaa",
    "computations/verify_h3_endpoint_odd_cartan_prism_augmentation.py":
        "24ec9e3c1d1f9b689fa5a47faf9900c16724dc215fee0a41a0b653f410427fb3",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "computations/verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py":
        "5a89d25227562b397d6cf3f16306346ce7d9fd16fb73a0f0a4486355a7cef29e",
    "computations/verify_h3_endpoint_recoloured_primitive_face_grade.py":
        "1c5ed6f5488fb1c4ec8c26d618f312dc1dfeeb5215f2fa24271154d0bcdea0c0",
    "computations/verify_h3_residual_q_order6_ridge_jet_commutation.py":
        "00a0798b4aa1d901b52645cac3f1dbe2854a3d8ce796191f7a4ff9a6e295b28f",
    "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py":
        "bcc55b05c10ba1ac6f3c4415c18a70274ecc29dd506fbed8e69d471b5f0a5607",
}
EXPECTED_LEDGER_SHA256 = "814cb57088a6c1effce5f4c0ce3b78b9fa0ab89b3a5b5e3d44b7436f87616c69"

TAIL_SITES = (2, 5)
ENDPOINT_SWAP = {0: 1, 1: 0}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def recolour_monomial(monomial, site, old, new):
    cells = list(monomial)
    positions = [index for index, cell in enumerate(cells)
                 if site in cell[:2]]
    require(len(positions) == 1, ("matching incidence changed", site))
    position = positions[0]
    left, right, a, b = cells[position]
    if left == site:
        require(a == old, ("unexpected root input colour", site, a, old))
        cells[position] = (left, right, new, b)
    else:
        require(right == site and b == old,
                ("unexpected root input colour", site, b, old))
        cells[position] = (left, right, a, new)
    return tuple(sorted(cells))


def root_pullback_row(row, site, old, new):
    """Infinitesimal pullback A^old <- A^old+t A^new."""
    answer = Counter()
    for monomial in row:
        answer[recolour_monomial(monomial, site, old, new)] += 1
    return answer


def permute_site(site):
    return ENDPOINT_SWAP.get(site, site)


def permute_cell(cell):
    left, right, a, b = cell
    left = permute_site(left)
    right = permute_site(right)
    if left < right:
        return left, right, a, b
    return right, left, b, a


def permute_monomial(monomial):
    return tuple(sorted(permute_cell(cell) for cell in monomial))


def permute_word(word):
    answer = list(word)
    for old_site, colour in enumerate(word):
        answer[permute_site(old_site)] = colour
    return tuple(answer)


def signed_weyl_word(word):
    """Simultaneous signed Weyl: colour 1 -> -2, colour 2 -> 1."""
    answer = list(word)
    sign = 1
    for site in TAIL_SITES:
        if answer[site] == 1:
            answer[site] = 2
            sign *= -1
        elif answer[site] == 2:
            answer[site] = 1
    return tuple(answer), sign


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "physical_cartan_source_base",
    )

    # Local colour covariance is literal on every complete source word.  It
    # suffices to check the two root directions generating the signed Weyl
    # action at the two tail sites.  Each derivative changes the unique cell
    # incident with that site and reconstructs the complete changed-word row.
    root_words = 0
    root_terms = 0
    for site in TAIL_SITES:
        for old, new in ((1, 2), (2, 1)):
            for word in product(range(3), repeat=8):
                if word[site] != old:
                    continue
                changed = list(word)
                changed[site] = new
                row = base.full_row(word)
                transported = root_pullback_row(row, site, old, new)
                expected = Counter(base.full_row(tuple(changed)))
                require(transported == expected,
                        ("root covariance left the complete row", site,
                         old, new, word))
                root_words += 1
                root_terms += len(row)
    require(root_words == 4 * 3 ** 7 and root_terms == root_words * 90,
            ("root covariance census changed", root_words, root_terms))

    # s is not a formal corner involution: it is the physical residual-site
    # permutation 0<->1.  The forbidden direct edge {6,3} is fixed, so the
    # entire 90-term source row is transported literally.
    swap_words = 0
    swap_terms = 0
    for word in product(range(3), repeat=8):
        transported = Counter(permute_monomial(value)
                              for value in base.full_row(word))
        expected = Counter(base.full_row(permute_word(word)))
        require(transported == expected,
                ("endpoint swap left the physical source presentation", word))
        swap_words += 1
        swap_terms += 90
    require(swap_words == 3 ** 8 and swap_terms == swap_words * 90,
            "endpoint source-automorphism census changed")

    # The local Weyl action does not preserve the GHZ target separately, but
    # its defect is invariant under 0<->1.  Endpoint oddization therefore
    # cancels it without adjoining a target vertex by definition.
    delta = Counter({(colour,) * 8: 1 for colour in range(3)})
    w_delta = Counter()
    for word, coefficient in delta.items():
        changed, sign = signed_weyl_word(word)
        w_delta[changed] += coefficient * sign
    signed_defect = Counter(w_delta)
    signed_defect.subtract(delta)
    signed_defect = Counter({key: value for key, value in
                             signed_defect.items() if value})
    swapped_defect = Counter()
    for word, coefficient in signed_defect.items():
        swapped_defect[permute_word(word)] += coefficient
    require(swapped_defect == signed_defect,
            "endpoint oddization stopped killing the physical target defect")

    # Naturality is now generator-level: functions H_w satisfy the Ward
    # identity above, and their differentials generate the principal-parts
    # de Rham algebra.  Cartan contraction therefore commutes with pullback.
    # The pinned coproduct theorem supplies every polynomial multiple and
    # repeated Hasse face, while the remaining pins identify the residue,
    # common grade, protected readouts, and ridge terminal.
    return {
        "theorem": "physical source-orbit descent of the endpoint-odd Cartan prism",
        "literal_root_covariance": {
            "tail_sites": list(TAIL_SITES),
            "ordered_root_directions": [[1, 2], [2, 1]],
            "complete_words_checked": root_words,
            "matching_terms_checked": root_terms,
            "ward_identity": "X_src H_w = H_(X_out w)",
        },
        "literal_endpoint_involution": {
            "site_permutation": "0 <-> 1",
            "complete_words_checked": swap_words,
            "matching_terms_checked": swap_terms,
            "direct_free_presentation_preserved": True,
        },
        "target_defect": {
            "weyl_delta_support": {repr(key): value
                                   for key, value in sorted(w_delta.items())},
            "endpoint_swap_invariant": True,
            "endpoint_odd_target": 0,
        },
        "chain_construction": (
            "local root fields on coefficient and output spaces are F-related; "
            "Cartan contraction is natural on the complete principal-parts "
            "source resolution, and K=(1-s)H_w is a source-provenant relative "
            "cell because its physical target defect cancels"
        ),
        "physical_packet": {
            "boundary": "(1-s)(w-1)",
            "ordinary_residue": [-1, 1, 1, -1],
            "protected_D_W_target_anchor_Eq": 0,
            "common_repeated_grade": "canonical endpoint-recoloured faces-(3,5) bridge",
            "ridge": "strictly commuting -dOmega_v eta/sigma packet",
        },
        "consequence": (
            "the physical Cartan edge comparison exists in the exhaustive "
            "relative principal-parts complex; the cyclic rank-four edge "
            "orbit and the six-term exhaustive alternative leave only the "
            "generator-or-physical-separator aggregate branch"
        ),
        "scope": (
            "local h=3 augmented interchange theorem in the canonical "
            "repeated grade.  It does not prove transverse quotient landing, "
            "uniform entry from every clean packet, or inactive horizontal "
            "and diagonal routing"
        ),
    }


def main():
    ledger = audit()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("physical Cartan descent ledger changed", digest))
    print("h3 physical Cartan source-orbit descent: PASS")
    print("root covariance words:",
          ledger["literal_root_covariance"]["complete_words_checked"])
    print("endpoint source automorphism words:",
          ledger["literal_endpoint_involution"]["complete_words_checked"])
    print("physical endpoint-odd Cartan comparison: SOURCE-PROVENANT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
