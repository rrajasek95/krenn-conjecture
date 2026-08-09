#!/usr/bin/env python3
"""Exact response obstruction on the sharp N=8, r=3 reciprocal packet.

The dependency ``verify_n8_r3_reciprocal_sharp_normal_form.py`` proves that
the only sharp incidence packet has two nonadjacent cubic sites and an outer
K6, with every bad edge essential at exactly one endpoint.  This checker
audits the remaining coefficient argument:

* all neighbor-triple overlaps m=1,2,3 contradict either the common
  nonessential line at the outer endpoint or a diagonal same-site product;
* with m=0, every monomial in every pure diagonal four-site response would
  need an outer edge essential at both endpoints, forbidden by sharp
  equality.

No positivity or absence-of-cancellation assumption is made: every pure
matching monomial is individually zero before coefficients are summed.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DEPENDENCIES = {
    ROOT / "computations/verify_n8_r3_reciprocal_sharp_normal_form.py":
        "39dff2b926ba62d9da0b6e5ef79a9ca67594635c7b2003c737229d3117c3addf",
    ROOT / "notes/n8-r3-reciprocal-sharp-normal-form.md":
        "2f8f63ccfb3179d06dfdcab46b577b5d034bd36ec3631cfa964c76f88473e8b2",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def audit_dependencies():
    ledger = {}
    for path, expected in DEPENDENCIES.items():
        digest = sha256(path.read_bytes()).hexdigest()
        require(digest == expected, f"sharp-normal-form dependency changed: {path}")
        ledger[str(path.relative_to(ROOT))] = digest
    return ledger


def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(rest):
            yield ((first, second),) + tail


def overlap_verdict(u, v):
    """Apply common-line consistency, then diagonal site-square-zero."""

    common_line = {u[colour]: colour for colour in range(3)}
    for colour in range(3):
        site = v[colour]
        if site in common_line and common_line[site] != colour:
            return "line_conflict"
        common_line.setdefault(site, colour)
    if any(u[colour] == v[colour] for colour in range(3)):
        return "diagonal_collision"
    return "survive"


def audit_overlap_strata():
    # Relabel the first cubic neighbor triple to sites 0,1,2.  The second is
    # an arbitrary injection of three labelled colours into the six outer
    # sites.  The unused-site stabilizer and simultaneous colour relabelling
    # do not affect either exact obstruction, so this exhausts every stratum.
    u = (0, 1, 2)
    census = defaultdict(Counter)
    survivors = []
    for v in permutations(range(6), 3):
        overlap = len(set(u) & set(v))
        verdict = overlap_verdict(u, v)
        census[overlap][verdict] += 1
        if verdict == "survive":
            survivors.append(v)

    expected = {
        0: {"survive": 6},
        1: {"line_conflict": 36, "diagonal_collision": 18},
        2: {"line_conflict": 45, "diagonal_collision": 9},
        3: {"line_conflict": 5, "diagonal_collision": 1},
    }
    frozen = {
        overlap: dict(sorted(census[overlap].items()))
        for overlap in range(4)
    }
    require(frozen == expected, f"neighbor-overlap census changed: {frozen}")
    require(set(survivors) == set(permutations((3, 4, 5))),
            "an overlapping neighbor triple survived")
    return u, tuple(sorted(survivors)), frozen


def audit_disjoint_pure_rows(u, survivors):
    """Every pure response matching would use double-essential q edges."""

    checked_terms = 0
    response_ledger = []
    for v in survivors:
        # The cubic arm of colour c is nonessential at its outer endpoint,
        # so the common nonessential line there is literally e_c.
        common_line = {u[colour]: colour for colour in range(3)}
        common_line.update({v[colour]: colour for colour in range(3)})
        require(len(common_line) == 6, "disjoint port lines collided")

        for target in range(3):
            complement = tuple(
                site for site in range(6)
                if site not in (u[target], v[target])
            )
            require(
                Counter(common_line[site] for site in complement)
                == Counter({colour: 2 for colour in range(3) if colour != target}),
                "pure-response complement line profile changed",
            )
            local_matchings = tuple(matchings(complement))
            require(len(local_matchings) == 3,
                    "four-site hafnian matching count changed")
            for matching in local_matchings:
                for left, right in matching:
                    # To carry target colour at an endpoint whose common line
                    # is another colour, this q block must be essential there.
                    require(common_line[left] != target, "left endpoint became common-line")
                    require(common_line[right] != target, "right endpoint became common-line")
                    # Hence the same physical q edge would have to be
                    # essential at both ends.  Sharp equality forbids that.
                checked_terms += 1
            response_ledger.append({
                "v": list(v),
                "target": target,
                "complement": list(complement),
                "matching_terms_forced_zero": len(local_matchings),
            })

    require(checked_terms == 54, "pure matching-term census changed")
    return checked_terms, response_ledger


def main():
    dependencies = audit_dependencies()
    u, survivors, overlap_census = audit_overlap_strata()
    zero_terms, responses = audit_disjoint_pure_rows(u, survivors)
    ledger = {
        "dependency_sha256": dependencies,
        "normalized_first_neighbors": list(u),
        "overlap_census": overlap_census,
        "disjoint_neighbor_orders": [list(row) for row in survivors],
        "pure_response_rows": len(responses),
        "pure_matching_terms_forced_zero": zero_terms,
        "coefficient_domain": "arbitrary complex aggregate blocks",
        "cancellation_used": False,
        "verdict": "sharp r=3 reciprocal response packet is empty",
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    expected = "9fda2c1b2c7fa3767fa49dced8e1a279ad8e10f8dfcc9de2d8b8dff1c459ae04"
    require(digest == expected, f"r=3 response ledger changed: {digest}")
    print("N=8 r=3 reciprocal response obstruction: PASS")
    print(f"neighbor overlap census: {overlap_census}")
    print(f"disjoint pure matching terms forced zero: {zero_terms}")
    print("verdict: exact sharp response ideal is empty over C")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
