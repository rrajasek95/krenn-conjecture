#!/usr/bin/env python3
"""Audit the all-h spectator theorem needed by the collision splitter.

The h=3 collision audits leave four parent-anti-diagonal families

    D*s1, p0*q01, D*s0, p1*q01

over the three perfect matchings of the four-site tail.  Matching repair is
already natural for an arbitrary fixed tail.  This checker asks the stronger
uniform question: when does one physical h=3 PP/AugP2 cylinder determine a
cell on every tail at every h?

Two failures distinguish static tensoring from a chain construction.

* Multiplying an h=3 cell C by r=h-3 disjoint spectator edges T preserves
  its local boundary, but d(C*T)=dC*T+(-1)^|C| C*dT.  The second summand is
  nonzero for r=1 and contains every spectator restriction face.
* Keeping the old four tail sites paired internally covers only
  3*(2h-7)!! of the (2h-3)!! full tail matchings.  Relabelling the h=3
  window covers the rest, but every matching has binomial(h-1,2) window
  presentations, so overlap/descent and divided-power normalization are
  additional data.

The exact conditional positive theorem is a dg-module statement.  A strong
symmetric-monoidal action of the oriented spectator matching/Hasse species,
with chain Leibniz, restriction/reinsertion, shuffle descent, physical
grade/readout covariance, and an H-linear PP/AugP2 comparison, transports
the four local cells and makes d^2=0.  A literal h=3 cell does not supply
these hypotheses; an h=3 *schema* suffices only when it already includes
them, which is precisely the desired all-h naturality theorem.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_hyperbolic_root_collision_tate_cobar_totalization_gate.py":
        "c0c6c075388a2eb2d5dad6d133166a3f211dd268183d3e2a5433d922e2ea8ceb",
    "computations/verify_h3_hyperbolic_collision_fixed_window_matching_routing_gate.py":
        "b8d02d77213bbb21d68dbad0aa4d6d1263625de012e413547723999d8d87fada",
    "computations/verify_h3_jd_hasse_bianchi_totalization_uniform_spectator_gate.py":
        "0a67d93f795600e1f406598fb22a3c0e0de5a29b5120b371a8e42be8f32a5213",
    "computations/verify_pointed_h3_spectator_uniformization_no_go.py":
        "832c4388961f24356cb182888cff89a4bda5ff181204a510baefb55e754323d2",
    "computations/verify_uniform_chart_cross_companion_relative_switch_dga_gate.py":
        "e0a8251128174d50b450b3bf85ce0a6870af00d4ab5565e7849fc3c8644c31c6",
}
EXPECTED_LEDGER_SHA256 = (
    "49c1833414dfafa6fcc145133b5eebcd27472e6b66985d5a36876eac91ed2c8e"
)


Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Basis = tuple[str, Matching]
Chain = Counter[Basis]

# Negative labels reserve the four operation ports.  Tail sites are
# nonnegative and hence disjoint at every order.
P, S, ZERO, ONE = -4, -3, -2, -1
PORTS = (P, S, ZERO, ONE)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def edge(left: int, right: int) -> Edge:
    require(left != right, ("loop", left))
    return tuple(sorted((left, right)))


def matching(*edges: Edge) -> Matching:
    return tuple(sorted(edges))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            yield matching(edge(first, second), *tail)


def odd_double_factorial(value: int) -> int:
    return 1 if value <= 0 else math.prod(range(1, value + 1, 2))


def clean(counter: Counter) -> Counter:
    return Counter({key: value for key, value in counter.items() if value})


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


LOCAL_MATCHINGS = {
    "A": matching(edge(P, S), edge(ZERO, ONE)),
    "B": matching(edge(P, ZERO), edge(S, ONE)),
    "C": matching(edge(P, ONE), edge(S, ZERO)),
}
COLLISIONS = (
    {
        "name": "forward_01=-D*s1",
        "local": matching(edge(P, S), edge(S, ONE)),
        "parents": ("A", "B"),
        "missing_doubled": (ZERO, S),
        "tail_operation": "DSQ",
    },
    {
        "name": "reverse_01=+p0*q01",
        "local": matching(edge(P, ZERO), edge(ZERO, ONE)),
        "parents": ("A", "B"),
        "missing_doubled": (S, ZERO),
        "tail_operation": "PQQ",
    },
    {
        "name": "forward_02=-D*s0",
        "local": matching(edge(P, S), edge(S, ZERO)),
        "parents": ("A", "C"),
        "missing_doubled": (ONE, S),
        "tail_operation": "DSQ",
    },
    {
        "name": "reverse_02=+p1*q01",
        "local": matching(edge(P, ONE), edge(ZERO, ONE)),
        "parents": ("A", "C"),
        "missing_doubled": (S, ONE),
        "tail_operation": "PQQ",
    },
)


def vertex_degree(value: Matching, vertices: tuple[int, ...]) -> tuple[int, ...]:
    counts = Counter(site for item in value for site in item)
    return tuple(counts[site] for site in vertices)


def collision_signature(value: Matching, vertices: tuple[int, ...]):
    degree = vertex_degree(value, vertices)
    missing = tuple(vertices[index] for index, count in enumerate(degree)
                    if count == 0)
    doubled = tuple(vertices[index] for index, count in enumerate(degree)
                    if count == 2)
    require(len(missing) == len(doubled) == 1,
            ("not a simple collision", value, degree))
    return missing[0], doubled[0]


def repair_collision(value: Matching, vertices: tuple[int, ...]):
    missing, doubled = collision_signature(value, vertices)
    arms = tuple(item for item in value if doubled in item)
    require(len(arms) == 2, ("collision arm count", value, arms))
    repairs = []
    for arm in arms:
        freed = arm[1] if arm[0] == doubled else arm[0]
        remainder = list(value)
        remainder.remove(arm)
        repairs.append(matching(*remainder, edge(missing, freed)))
    return tuple(sorted(repairs))


def oriented_boundary(value: Matching) -> Counter[Matching]:
    """Boolean/Hasse boundary of an oriented edge word."""
    answer: Counter[Matching] = Counter()
    for position in range(len(value)):
        face = value[:position] + value[position + 1:]
        answer[face] += Q(-1 if position % 2 else 1)
    return clean(answer)


def boundary_chain(chain: Counter[Matching]) -> Counter[Matching]:
    answer: Counter[Matching] = Counter()
    for value, coefficient in chain.items():
        for face, sign in oriented_boundary(value).items():
            answer[face] += coefficient * sign
    return clean(answer)


def total_differential_basis(local: str, tail: Matching,
                             carrier_parity: int) -> Chain:
    """Tensor differential for dc=b, with parity |c| given."""
    require(local in {"c", "b"} and carrier_parity in {0, 1},
            (local, carrier_parity))
    answer: Chain = Counter()
    if local == "c":
        answer[("b", tail)] += 1
        spectator_sign = Q(-1 if carrier_parity else 1)
    else:
        spectator_sign = Q(1 if carrier_parity else -1)
    for face, coefficient in oriented_boundary(tail).items():
        answer[(local, face)] += spectator_sign * coefficient
    return clean(answer)


def total_differential(chain: Chain, carrier_parity: int) -> Chain:
    answer: Chain = Counter()
    for (local, tail), coefficient in chain.items():
        for basis, value in total_differential_basis(
                local, tail, carrier_parity).items():
            answer[basis] += coefficient * value
    return clean(answer)


def tensor_hasse_and_reinsertion_audit() -> dict[str, object]:
    records = []
    for tail_edges in range(0, 6):
        # One oriented matching is enough for the universal Boolean sign
        # identity; endpoint labels make all its edges distinct.
        value = tuple(edge(2 * index, 2 * index + 1)
                      for index in range(tail_edges))
        require(not boundary_chain(oriented_boundary(value)),
                ("spectator boundary stopped squaring to zero", value))

        for parity in (0, 1):
            start = Counter({("c", value): Q(1)})
            require(not total_differential(
                total_differential(start, parity), parity
            ), ("tensor differential stopped squaring to zero", tail_edges,
                parity))

        # With a new edge placed first, insertion is the standard contracting
        # homotopy: partial I_e + I_e partial = identity.  The shuffle signs
        # transport this formula to insertion at an arbitrary position.
        new_edge = edge(-6, -5)
        require(all(set(new_edge).isdisjoint(item) for item in value),
                "reinsertion edge met a tail endpoint")
        inserted = (new_edge,) + value
        lhs = oriented_boundary(inserted)
        for face, coefficient in oriented_boundary(value).items():
            lhs[(new_edge,) + face] += coefficient
        lhs = clean(lhs)
        require(lhs == Counter({value: Q(1)}),
                ("restriction/reinsertion homotopy changed", value, lhs))
        records.append({
            "tail_edges": tail_edges,
            "first_Hasse_faces": tail_edges,
            "all_nonempty_tail_face_flags": 2 ** tail_edges - 1,
            "tail_boundary_squared": 0,
            "tensor_total_boundary_squared_for_both_parities": 0,
            "restriction_insertion_identity": "partial I + I partial = id",
        })
    return {
        "oriented_tail_records": records,
        "chain_Leibniz_rule":
            "d mu(c,T)=mu(dc,T)+(-1)^|c| mu(c,partial T)",
        "consequence": (
            "a strong dg-module action totalizes every spectator face and "
            "makes d^2=0; the static term mu(dc,T) alone is not a chain "
            "boundary when T has positive edge degree"
        ),
    }


def all_order_collision_family_audit() -> dict[str, object]:
    records = []
    for h in range(3, 8):
        tail_edges = h - 1
        tail_vertices = tuple(range(2 * tail_edges))
        tails = tuple(perfect_matchings(tail_vertices))
        expected_tails = odd_double_factorial(2 * tail_edges - 1)
        require(len(tails) == len(set(tails)) == expected_tails,
                ("tail matching count", h, len(tails), expected_tails))

        restriction_flags = 0
        collision_occurrences = set()
        parent_occurrences = set()
        induced_cover = Counter()
        for tail in tails:
            # Every selection of two tail edges is a relabelled h=3 window;
            # its complement is the extra spectator tail.  This proves the
            # exact overlap multiplicity of h=3 induction.
            for base_positions in combinations(range(tail_edges), 2):
                base = tuple(tail[index] for index in base_positions)
                extra = tuple(tail[index] for index in range(tail_edges)
                              if index not in base_positions)
                require(set(base).isdisjoint(extra), "tail split overlapped")
                induced_cover[tail] += 1

            for removed in tail:
                face = tuple(item for item in tail if item != removed)
                remaining_vertices = tuple(
                    site for site in tail_vertices if site not in removed
                )
                require(vertex_degree(face, remaining_vertices)
                        == (1,) * len(remaining_vertices),
                        ("tail restriction left the matching species", h,
                         tail, removed))
                require(matching(*face, removed) == tail,
                        ("tail reinsertion failed", h, tail, removed))
                restriction_flags += 1

            vertices = PORTS + tail_vertices
            for family_index, family in enumerate(COLLISIONS):
                collision = matching(*family["local"], *tail)
                require(collision_signature(collision, vertices)
                        == family["missing_doubled"],
                        ("collision sector changed", h, family["name"]))
                repairs = repair_collision(collision, vertices)
                expected_repairs = tuple(sorted(
                    matching(*LOCAL_MATCHINGS[parent], *tail)
                    for parent in family["parents"]
                ))
                require(repairs == expected_repairs,
                        ("tail-natural repairs changed", h, family["name"]))
                collision_occurrences.add((family_index, tail))
                for parent_index, _parent in enumerate(family["parents"]):
                    parent_occurrences.add((family_index, tail, parent_index))

                # Restricting any tail edge commutes with both repairs and
                # with the parent anti-diagonal (+1,-1).
                for removed in tail:
                    restricted = tuple(item for item in tail
                                       if item != removed)
                    restricted_collision = matching(
                        *family["local"], *restricted
                    )
                    restricted_vertices = tuple(
                        site for site in vertices if site not in removed
                    )
                    actual = repair_collision(
                        restricted_collision, restricted_vertices
                    )
                    expected = tuple(sorted(
                        matching(*LOCAL_MATCHINGS[parent], *restricted)
                        for parent in family["parents"]
                    ))
                    require(actual == expected,
                            ("parent split lost restriction naturality", h,
                             family["name"], removed))

        overlap = math.comb(tail_edges, 2)
        require(set(induced_cover.values()) == {overlap}
                and len(induced_cover) == len(tails),
                ("h3-window induction multiplicity changed", h,
                 Counter(induced_cover.values())))

        extra_edges = h - 3
        fixed_partition_tails = (
            3 * odd_double_factorial(2 * extra_edges - 1)
        )
        require(fixed_partition_tails <= len(tails)
                and (fixed_partition_tails == len(tails)) == (h == 3),
                ("fixed partition unexpectedly exhausted tails", h,
                 fixed_partition_tails, len(tails)))

        collision_count = 4 * len(tails)
        parent_count = 2 * collision_count
        require(len(collision_occurrences) == collision_count
                and len(parent_occurrences) == parent_count
                and restriction_flags == tail_edges * len(tails),
                ("all-h labelled census changed", h))
        records.append({
            "h": h,
            "tail_edges": tail_edges,
            "all_tail_matchings": len(tails),
            "four_family_collision_occurrences": collision_count,
            "parent_labelled_occurrences": parent_count,
            "parent_collection_rank_kernel": [collision_count,
                                                   collision_count],
            "local_arm_PP_flags": 2 * collision_count,
            "spectator_Leibniz_PP_flags": tail_edges * collision_count,
            "fixed_h3_window_times_extra_tail_matchings":
                fixed_partition_tails,
            "cross_partition_tail_matchings_missing_from_bare_tensor":
                len(tails) - fixed_partition_tails,
            "relabelled_h3_window_cover_multiplicity": overlap,
            "normalized_induction_denominator": overlap,
            "parent_split_restriction_reinsertion_natural": True,
        })

    require(records[0]["four_family_collision_occurrences"] == 12
            and records[0]["local_arm_PP_flags"] == 24
            and records[0]["spectator_Leibniz_PP_flags"] == 24
            and records[1]["cross_partition_tail_matchings_missing_from_bare_tensor"]
            == 12,
            "the h3/h4 frontier changed")
    return {
        "finite_exact_orders": records,
        "uniform_formulas": {
            "tail_matchings": "(2h-3)!!",
            "collision_occurrences": "4*(2h-3)!!",
            "parent_split_kernel_dimension": "4*(2h-3)!!",
            "local_arm_first_PP_flags": "8*(2h-3)!!",
            "tail_Leibniz_first_PP_flags": "4*(h-1)*(2h-3)!!",
            "bare_fixed_window_tail_matchings": "3*(2h-7)!!",
            "h3_window_overlap_multiplicity": "binomial(h-1,2)",
        },
        "formal_tensoring": (
            "for a fixed disjoint tail T, the parent anti-diagonal, its two "
            "A/B or A/C repairs, every local PP/AugP2 face, and every "
            "additive word/fine/repeated grade tensor literally with T"
        ),
        "new_uniform_faces": (
            "removing any tail edge gives the recursive collision carrier "
            "on the restricted tail; all higher nonempty tail subsets give "
            "the remaining cobar faces.  Reinsertion is their oriented "
            "inverse homotopy and requires shuffle/overlap coherence"
        ),
    }


def fixed_h3_tensor_audit() -> dict[str, object]:
    records = []
    for extra_edges in range(0, 6):
        extra_matchings = odd_double_factorial(2 * extra_edges - 1)
        h3_collision_cells = 12
        records.append({
            "h": extra_edges + 3,
            "extra_spectator_edges": extra_edges,
            "extra_tail_matchings": extra_matchings,
            "formal_local_PP_faces": 48 * extra_matchings,
            "new_first_Leibniz_faces":
                h3_collision_cells * extra_edges * extra_matchings,
            "new_nonempty_tail_subset_flags":
                h3_collision_cells * (2 ** extra_edges - 1)
                * extra_matchings,
        })
    require(records[1]["new_first_Leibniz_faces"] == 12
            and records[1]["new_nonempty_tail_subset_flags"] == 12,
            "the first h4 Leibniz packet changed")
    return {
        "records": records,
        "first_failure": (
            "h=4: one added spectator edge contributes twelve labelled "
            "faces (de)*C, one for each h3 collision occurrence"
        ),
        "static_h3_tensor_is_chain_map": False,
    }


def uniform_hypotheses_and_sufficiency() -> dict[str, object]:
    hypotheses = [
        {
            "id": "U1",
            "name": "four-family source seed",
            "requirement": (
                "physical parent-split collision carriers for all four "
                "root-order families, with their complete local PP/AugP2 "
                "boundary and root/chart overlap square"
            ),
        },
        {
            "id": "U2",
            "name": "spectator dg-module",
            "requirement": (
                "a strong symmetric-monoidal action mu of the oriented "
                "matching Hasse/cobar species satisfying the chain Leibniz "
                "identity and all shuffle signs"
            ),
        },
        {
            "id": "U3",
            "name": "restriction/reinsertion descent",
            "requirement": (
                "edge-labelled restriction and insertion satisfy partial "
                "I+I partial=id, Beck-Chevalley for disjoint edges, and "
                "overlap descent among the binomial(h-1,2) relabelled h3 "
                "window presentations"
            ),
        },
        {
            "id": "U4",
            "name": "physical covariance and exhaustivity",
            "requirement": (
                "the PP-to-AugP2 word/fine/repeated map, reduced Eq, target, "
                "q, anchor, W, ordinary residue and shifted ridge are "
                "mu-linear, and normalized induction lands in the complete "
                "source/terminal block rather than only a T-divisible sector"
            ),
        },
    ]
    return {
        "minimal_uniform_hypotheses": hypotheses,
        "conditional_theorem": (
            "Under U1-U4, define C_f(M)=mu(C_f,M).  U2 gives every local "
            "and spectator face with d^2=0; U3 makes restriction and "
            "reinsertion independent of window/shuffle presentation; U4 "
            "transports the physical AugP2 and protected rows and descends "
            "the relabelled cover to the full order-h source.  The four "
            "families therefore form an all-h collision PP/AugP2 splitter"
        ),
        "literal_single_h3_cell_suffices": False,
        "single_h3_schema_suffices_iff": (
            "schema means a U1 seed together with the U2-U4 module, overlap, "
            "and physical descent structure; those clauses are new uniform "
            "data and do not follow from checking h=3"
        ),
        "independent_first_failures": [
            "chain: the h4 (de)*C Leibniz packet",
            "coverage: twelve of fifteen h4 tails cross the fixed partition",
            "descent: the three h4 h3-window presentations need coherence",
            "physical: DSQ is still untyped and PQQ still lacks word/fine transport",
        ],
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": (
            "uniform hyperbolic collision PP/AugP2 spectator naturality gate"
        ),
        "pins": PINS,
        "all_order_collision_and_parent_split":
            all_order_collision_family_audit(),
        "formal_h3_tensor_vs_new_faces": fixed_h3_tensor_audit(),
        "spectator_Hasse_totalization":
            tensor_hasse_and_reinsertion_audit(),
        "uniform_extension_theorem": uniform_hypotheses_and_sufficiency(),
        "verdict": (
            "The h3 parent-split obstruction tensors formally with a fixed "
            "spectator matching, and matching repair remains exactly "
            "tail-natural.  This is not an all-h physical cell.  At h4 the "
            "product differential adds twelve (de)*C faces, while a fixed "
            "h3 tail window covers only three of fifteen tail matchings.  "
            "Relabelling covers all tails with multiplicity three and hence "
            "adds overlap/descent data.  One h3 schema is sufficient only "
            "as a generator in a strong spectator-Hasse dg module whose "
            "restriction/reinsertion, PP/AugP2, physical readouts and full-"
            "source descent satisfy U1-U4; a literal h3 cylinder alone is "
            "insufficient"
        ),
        "shortest_positive_datum": (
            "construct the h4 one-edge structure map mu(C,e) together with "
            "its twelve Leibniz faces and the three-presentation overlap "
            "homotopy, retaining the four parent labels and the DSQ/PQQ "
            "physical AugP2 types.  The oriented Hasse identities then state "
            "the exact recursion required at every higher h"
        ),
        "nonclaims": [
            "static polynomial tensoring is not called a chain suspension",
            "fixed-partition tails are not called the full matching source",
            "normalized relabelled induction is not supplied without overlap descent",
            "coarse P3+K2 topology is not called a physical AugP2 landing",
            "the conditional dg-module theorem is not called constructed",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("fixed-tail parent split: FORMALLY NATURAL AT EVERY h")
    print("h4 product rule: TWELVE NEW (de)*C FACES")
    print("h4 fixed window: 3/15 TAILS; RELABELLED COVER MULTIPLICITY 3")
    print("uniform iff: SPECTATOR-HASSE DG MODULE + OVERLAP/PHYSICAL DESCENT")
    print("literal h3 cell schema: INSUFFICIENT")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()
