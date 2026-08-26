#!/usr/bin/env python3
"""Exact abstract (K-degree, cycle-partition) completion audit.

The profile retains the multiplier anchor count and the eligible subset of the
four base-pair completion edges.  This first bounded gate uses a structured
14-profile subfamily and proves that the structured a*H0*H1*H2 vector already
lies in the abstract profile span.  It makes no actual mixed-word realization
claim for those abstract profiles.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_kcycle_abstract_refinement.json"
CERT = HERE / "kcycle_abstract_aT_certificate.tsv"
BASE = ((0, 1), (2, 3), (4, 5), (6, 7))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


@lru_cache(None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    u = vertices[0]
    answer = []
    for index, v in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((u, v),) + tail)
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(8)))


def union_cycle_partition(left, right):
    """Edge-count partition of the 2-regular multigraph left union right."""
    adjacency = [[] for _ in range(8)]
    for edge_id, (u, v) in enumerate(left + right):
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))
    require(all(len(row) == 2 for row in adjacency), adjacency)
    used = set()
    parts = []
    for edge_id in range(8):
        if edge_id in used:
            continue
        stack = [edge_id]
        vertices = set()
        while stack:
            current = stack.pop()
            if current in used:
                continue
            used.add(current)
            u, v = (left + right)[current]
            vertices.update((u, v))
            for vertex in (u, v):
                stack.extend(other for _, other in adjacency[vertex]
                             if other not in used)
        parts.append(len(vertices))
    # In a parallel double edge the two edge IDs have two vertices: cycle 2.
    require(sum(parts) == 8, parts)
    return tuple(sorted(parts))


def common_base_edges(matching):
    return len(set(BASE).intersection(matching))


def one_colour_vector():
    answer = Counter()
    types = Counter()
    for matching in PM8:
        partition = union_cycle_partition(BASE, matching)
        common = common_base_edges(matching)
        require(common == partition.count(2), (matching, partition, common))
        answer[(4 - common, partition)] += 1
        types[(partition, common)] += 1
    require(sum(answer.values()) == 105, answer)
    return answer, types


def convolve(left, right):
    answer = Counter()
    for (left_k, left_partition), left_count in left.items():
        for (right_k, right_partition), right_count in right.items():
            answer[(left_k + right_k,
                    tuple(sorted(left_partition + right_partition)))] += (
                        left_count * right_count)
    return answer


def abstract_profile_vector(multiplier_anchor_count, closed_partition):
    """Four base-pair paths of length 1, all four base edges eligible."""
    answer = Counter()
    for completion in PM8:
        selected = common_base_edges(completion)
        k_degree = 24 - multiplier_anchor_count - selected
        partition = tuple(sorted(closed_partition
                                 + union_cycle_partition(BASE, completion)))
        require(0 <= k_degree <= 24, (multiplier_anchor_count, selected))
        answer[(k_degree, partition)] += 1
    require(sum(answer.values()) == 105, answer)
    return answer


def build(mutate=False):
    require(len(PM8) == 105, len(PM8))
    one, types = one_colour_vector()
    direct = convolve(convolve(one, one), one)
    require(sum(direct.values()) == 105 ** 3, sum(direct.values()))

    # Fix the last two pure matchings in the multiplier a*H1*H2, and use H0
    # as the 105 completion edges.  Group the 105^2 ordered choices by the
    # refined abstract profile (m_A, eligible mask=1111, closed cycles).
    profile_multiplicities = Counter()
    for first in PM8:
        first_partition = union_cycle_partition(BASE, first)
        first_common = common_base_edges(first)
        for second in PM8:
            second_partition = union_cycle_partition(BASE, second)
            second_common = common_base_edges(second)
            multiplier_anchor_count = 12 + first_common + second_common
            closed = tuple(sorted(first_partition + second_partition))
            profile_multiplicities[(multiplier_anchor_count, closed)] += 1
    if mutate:
        profile_multiplicities[min(profile_multiplicities)] += 1
    require(sum(profile_multiplicities.values()) == 105 ** 2,
            sum(profile_multiplicities.values()))
    require(len(profile_multiplicities) == 14, len(profile_multiplicities))

    certificate = Counter()
    rows = []
    for (anchor_count, closed), coefficient in sorted(profile_multiplicities.items()):
        vector = abstract_profile_vector(anchor_count, closed)
        for coordinate, value in vector.items():
            certificate[coordinate] += coefficient * value
        rows.append({
            "multiplier_anchor_count": anchor_count,
            "eligible_base_completion_mask": "1111",
            "path_edge_lengths": "1,1,1,1",
            "closed_cycle_partition": ",".join(map(str, closed)),
            "certificate_coefficient": coefficient,
            "profile_support": len(vector),
        })
    require(certificate == direct, "14-profile certificate does not equal structured a*T")

    tsv = ["multiplier_anchor_count\teligible_base_completion_mask\tpath_edge_lengths\tclosed_cycle_partition\tcertificate_coefficient\tprofile_support"]
    for row in rows:
        tsv.append("\t".join(str(row[key]) for key in (
            "multiplier_anchor_count", "eligible_base_completion_mask",
            "path_edge_lengths", "closed_cycle_partition",
            "certificate_coefficient", "profile_support")))
    cert_payload = "\n".join(tsv) + "\n"

    k_histogram = Counter()
    for (k_degree, _), coefficient in direct.items():
        k_histogram[k_degree] += coefficient
    result = {
        "schema": "orbit0-kcycle-abstract-refinement-v1",
        "status": "ABSTRACT_REFINED_QUOTIENT_DOES_NOT_SEPARATE_A_TIMES_T",
        "structured_aT_terms": sum(direct.values()),
        "structured_aT_nonzero_K_partition_coordinates": len(direct),
        "structured_aT_K_degree_histogram": dict(sorted(k_histogram.items())),
        "one_colour_matching_types": [
            {"cycle_partition": list(partition), "common_base_edges": common,
             "matching_count": count}
            for (partition, common), count in sorted(types.items())
        ],
        "abstract_certificate_profiles": len(rows),
        "abstract_certificate_total_profile_multiplicity": sum(profile_multiplicities.values()),
        "abstract_certificate_completion_terms": 105 * sum(profile_multiplicities.values()),
        "certificate_exact_equality": True,
        "certificate_tsv_sha256": sha256(cert_payload.encode()).hexdigest(),
        "scope_guard": (
            "This is exact membership in the sound combinatorial superset of refined completion "
            "profiles. It proves that no separator valid on that entire abstract superset can "
            "separate a*T. It does not prove the 14 profiles are jointly realized by literal "
            "mixed-word columns, so actual mixed-ideal membership remains open."
        ),
    }
    logical = dict(result)
    result["logical_sha256"] = sha256(
        json.dumps(logical, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return result, cert_payload


def main():
    result, cert_payload = build(mutate="--mutate" in sys.argv)
    result_payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if "--verify" in sys.argv:
        require(CERT.read_text() == cert_payload, "stored certificate TSV differs")
        require(OUT.read_text() == result_payload, "stored result differs")
    else:
        CERT.write_text(cert_payload)
        OUT.write_text(result_payload)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
