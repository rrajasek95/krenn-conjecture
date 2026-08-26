#!/usr/bin/env python3
"""Exact finite-field all-nine screen on the minimal diagonal-q stratum.

All six endpoint stars are projective vectors supported on at most two
decorated ports.  Unlike the companion selected-row screen, this checker
imposes all nine normalized rows, reconstructs the direct matrix a with
a_01=1, forms r=-sum_i B_ii literally, and tests r^[3] != 0.
"""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
import importlib.util
from itertools import permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_minimal_q_fullnine.json"
BASE_PATH = HERE / "screen_minimal_q_selected_row.py"


def load_base():
    spec = importlib.util.spec_from_file_location("minimal_q_selected", BASE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


B = load_base()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def canonical_selected_triple(triple):
    """Canonicalize with selected ordered channel 01 held fixed.

    Site permutations are always sound.  Swapping the two endpoints sends
    selected 01 to 10; the simultaneous physical/channel colour swap 0<->1
    restores 01, so it supplies the only nontrivial residual colour action.
    """
    images = []
    for site_permutation in B.S6:
        moved = tuple(B.move_matching(row, site_permutation) for row in triple)
        images.append(moved)
        images.append((moved[1], moved[0], moved[2]))
    return min(images)


def selected_q_orbit_representatives():
    representatives = set()
    # The unordered census contains every matching multiset.  Reinsert all
    # distinct colour orders, then quotient only by the valid selected-pair
    # stabilizer above.
    for multiset in B.q_orbit_representatives():
        for ordered in set(permutations(multiset)):
            representatives.add(canonical_selected_triple(ordered))
    return tuple(sorted(representatives))


def sparse_add(output, source, scale, prime):
    for key, value in source.items():
        new = (output.get(key, 0) + scale * value) % prime
        if new:
            output[key] = new
        elif key in output:
            del output[key]


def star_product(left, right, prime):
    answer = {}
    for (u, cu), left_value in left.items():
        for (v, cv), right_value in right.items():
            if u == v:
                continue
            if u < v:
                key = (u, v, cu, cv)
            else:
                key = (v, u, cv, cu)
            answer[key] = (answer.get(key, 0) + left_value * right_value) % prime
            if not answer[key]:
                del answer[key]
    return answer


def edge_response_table(cofactors, prime):
    table = defaultdict(dict)
    for word_index, (word, row) in enumerate(zip(B.WORDS, cofactors, strict=True)):
        for (u, v), value in row.items():
            table[(u, v, word[u], word[v])][word_index] = value % prime
    return dict(table)


def response(left, right, edge_responses, prime):
    quadratic = star_product(left, right, prime)
    answer = {}
    for cell, coefficient in quadratic.items():
        sparse_add(answer, edge_responses.get(cell, {}), coefficient, prime)
    return answer


def scalar_multiple(vector, base, prime):
    if not vector:
        return 0
    if not base:
        return None
    pivot = next(iter(base))
    coefficient = vector.get(pivot, 0) * pow(base[pivot], prime - 2, prime) % prime
    if not coefficient:
        return None
    keys = set(vector) | set(base)
    if all(vector.get(key, 0) == coefficient * base.get(key, 0) % prime
           for key in keys):
        return coefficient
    return None


def diagonal_coordinates(vector, base, colour, prime):
    pure = B.WORD_INDEX[(colour,) * 6]
    # Minimal q has no pure cube: base[pure]=0.
    require(not base.get(pure, 0), "minimal q unexpectedly has a pure cube")
    diagonal = vector.get(pure, 0)
    if not diagonal:
        return None
    remainder = dict(vector)
    remainder.pop(pure, None)
    if not remainder:
        return diagonal, 0
    coefficient = scalar_multiple(remainder, base, prime)
    if coefficient is None:
        return None
    return diagonal, coefficient


def candidates(prime):
    return tuple(left for left, _support in B.projective_lefts(prime))


def relations(q, cube, cofactors, prime):
    stars = candidates(prime)
    z_response = {index: (-value) % prime for index, value in enumerate(cube) if value}
    edge_responses = edge_response_table(cofactors, prime)
    off = [dict() for _ in stars]
    diagonal = [[dict() for _ in stars] for _ in B.COLOURS]
    for left_index, left in enumerate(stars):
        for right_index, right in enumerate(stars):
            value = response(left, right, edge_responses, prime)
            coefficient = (scalar_multiple(value, z_response, prime)
                           if z_response else (0 if not value else None))
            if coefficient is not None:
                off[left_index][right_index] = coefficient
            for colour in B.COLOURS:
                if z_response:
                    coordinates = diagonal_coordinates(
                        value, z_response, colour, prime
                    )
                else:
                    pure = B.WORD_INDEX[(colour,) * 6]
                    diagonal_value = value.get(pure, 0)
                    coordinates = ((diagonal_value, 0)
                                   if diagonal_value
                                   and set(value) == {pure} else None)
                if coordinates is not None:
                    diagonal[colour][left_index][right_index] = coordinates
    return stars, z_response, off, diagonal


def scale_quadratic(quadratic, scalar, prime):
    return {key: scalar * value % prime for key, value in quadratic.items()
            if scalar * value % prime}


def add_quadratics(*rows, prime):
    answer = {}
    for quadratic, scalar in rows:
        for key, value in quadratic.items():
            new = (answer.get(key, 0) + scalar * value) % prime
            if new:
                answer[key] = new
            elif key in answer:
                del answer[key]
    return answer


def cube(quadratic, prime):
    return tuple(B.hafnian(quadratic, word, B.SITES, prime) for word in B.WORDS)


def serialize_star(star):
    return [[site, colour, value] for (site, colour), value in sorted(star.items())]


def serialize_quadratic(quadratic):
    return [[u, v, cu, cv, value]
            for (u, v, cu, cv), value in sorted(quadratic.items())]


def verify_candidate(q, cube_q, stars, z_response, off, diagonal,
                     indices, prime):
    p0, p1, p2, s0, s1, s2 = indices
    ps = (stars[p0], stars[p1], stars[p2])
    ss = (stars[s0], stars[s1], stars[s2])
    selected_coefficient = off[p0][s1]
    d = []
    c = []
    for colour, (p_index, s_index) in enumerate(zip((p0, p1, p2),
                                                     (s0, s1, s2), strict=True)):
        diagonal_value, z_value = diagonal[colour][p_index][s_index]
        d.append(diagonal_value)
        c.append(z_value)

    if z_response:
        x = [1, selected_coefficient * pow(d[1], prime - 2, prime) % prime, 1]
        y = [pow(d[0], prime - 2, prime),
             pow(selected_coefficient, prime - 2, prime),
             pow(d[2], prime - 2, prime)]
    else:
        x = [1, 1, 1]
        y = [pow(value, prime - 2, prime) for value in d]
    scaled_p = tuple(scale_quadratic(star, x_i, prime)
                     for star, x_i in zip(ps, x, strict=True))
    scaled_s = tuple(scale_quadratic(star, y_i, prime)
                     for star, y_i in zip(ss, y, strict=True))
    z = star_product(scaled_p[0], scaled_s[1], prime)
    a = [[0] * 3 for _ in range(3)]
    edge_responses = edge_response_table(B.q_cube_and_cofactors(q, prime)[1], prime)
    for i in B.COLOURS:
        for j in B.COLOURS:
            value = response(scaled_p[i], scaled_s[j], edge_responses, prime)
            if i == j:
                pure = B.WORD_INDEX[(i,) * 6]
                remainder = dict(value)
                require(remainder.pop(pure, 0) == 1,
                        (i, "diagonal target coefficient changed"))
                a[i][j] = ((scalar_multiple(remainder, z_response, prime) or 0)
                           if z_response else 0)
            else:
                a[i][j] = ((scalar_multiple(value, z_response, prime) or 0)
                           if z_response else 0)
    if not z_response:
        a[0][1] = 1
    require(a[0][1] == 1, a)

    products = [star_product(scaled_p[i], scaled_s[i], prime) for i in B.COLOURS]
    if z_response:
        traces = (sum(a[i][i] for i in B.COLOURS) % prime,)
    else:
        # Every a_ij is response-invisible when z q^[2]=0.  Keep a_01=1
        # and exhaust the free trace, assigning it to a_00.
        traces = tuple(range(prime))
    r = None
    r_cube = None
    chosen_trace = None
    for trace in traces:
        candidate_r = add_quadratics(
            *[(row, -1) for row in products], (z, trace), prime=prime
        )
        candidate_cube = cube(candidate_r, prime)
        if any(candidate_cube):
            r, r_cube, chosen_trace = candidate_r, candidate_cube, trace
            break
    if r is None:
        trace = traces[0]
        r = add_quadratics(
            *[(row, -1) for row in products], (z, trace), prime=prime
        )
        r_cube = cube(r, prime)
        chosen_trace = trace
    if not z_response:
        a[0][0] = chosen_trace

    # Literal replay of the selected row and all nine normalized B rows.
    q_cube_sparse = {index: value for index, value in enumerate(cube_q) if value}
    zq2 = response(scaled_p[0], scaled_s[1], edge_responses, prime)
    require(all((q_cube_sparse.get(key, 0) + zq2.get(key, 0)) % prime == 0
                for key in set(q_cube_sparse) | set(zq2)),
            "selected q^[3]+zq^[2] row failed")
    for i in B.COLOURS:
        for j in B.COLOURS:
            pij = star_product(scaled_p[i], scaled_s[j], prime)
            bij = add_quadratics((pij, 1), (z, -a[i][j]), prime=prime)
            # Evaluate B_ij q^[2].
            value = {}
            for cell, coefficient in bij.items():
                sparse_add(value, edge_responses.get(cell, {}), coefficient, prime)
            target = {B.WORD_INDEX[(i,) * 6]: 1} if i == j else {}
            require(value == target, (i, j, "normalized row failed"))

    return {
        "indices": list(indices),
        "p": [serialize_star(row) for row in scaled_p],
        "s": [serialize_star(row) for row in scaled_s],
        "a": a,
        "trace_a": chosen_trace,
        "q": serialize_quadratic(q),
        "z": serialize_quadratic(z),
        "r": serialize_quadratic(r),
        "r_cube_support": sum(value != 0 for value in r_cube),
        "r_cube_first_nonzero": next((
            [list(B.WORDS[index]), value]
            for index, value in enumerate(r_cube) if value
        ), None),
    }


def screen_orbit(triple, prime):
    q = B.q_from_triple(triple, prime)
    cube_q, cofactors = B.q_cube_and_cofactors(q, prime)
    stars, z_response, off, diagonal = relations(q, cube_q, cofactors, prime)
    off_reverse = [set() for _ in stars]
    diagonal_reverse = [[set() for _ in stars] for _ in B.COLOURS]
    for left, row in enumerate(off):
        for right in row:
            off_reverse[right].add(left)
    for colour in B.COLOURS:
        for left, row in enumerate(diagonal[colour]):
            for right in row:
                diagonal_reverse[colour][right].add(left)

    candidate_sextuples = 0
    for p0 in range(len(stars)):
        for s1, selected_coefficient in off[p0].items():
            if z_response and not selected_coefficient:
                continue
            for s0 in diagonal[0][p0]:
                p1_candidates = diagonal_reverse[1][s1] & off_reverse[s0]
                for p1 in p1_candidates:
                    s2_candidates = set(off[p0]) & set(off[p1])
                    for s2 in s2_candidates:
                        p2_candidates = (diagonal_reverse[2][s2]
                                         & off_reverse[s0] & off_reverse[s1])
                        for p2 in p2_candidates:
                            candidate_sextuples += 1
                            record = verify_candidate(
                                q, cube_q, stars, z_response, off, diagonal,
                                (p0, p1, p2, s0, s1, s2), prime,
                            )
                            if record["r_cube_support"]:
                                return {
                                    "q_cube_zero": not any(cube_q),
                                    "candidate_sextuples_before_witness": candidate_sextuples,
                                    "compatible_sextuple": record,
                                    "relation_counts": {
                                        "off": sum(len(row) for row in off),
                                        "diag": [sum(len(row) for row in rows)
                                                 for rows in diagonal],
                                    },
                                }
    return {
        "q_cube_zero": not any(cube_q),
        "candidate_sextuples": candidate_sextuples,
        "compatible_sextuple": None,
        "relation_counts": {
            "off": sum(len(row) for row in off),
            "diag": [sum(len(row) for row in rows) for rows in diagonal],
        },
    }


def build():
    representatives = selected_q_orbit_representatives()
    prime_records = []
    for prime in (5, 7):
        orbits = []
        witness = None
        for orbit_index, triple in enumerate(representatives):
            record = screen_orbit(triple, prime)
            record["orbit"] = orbit_index
            record["triple"] = [[[u, v] for u, v in matching]
                                for matching in triple]
            orbits.append(record)
            if record["compatible_sextuple"] is not None:
                witness = record
                break
        prime_records.append({
            "prime": prime,
            "orbits_screened": len(orbits),
            "literal_counterexample_found": witness is not None,
            "first_witness": witness,
            "orbits": orbits,
        })
        if witness is not None:
            break
    result = {
        "status": "PASS exact bounded minimal-q full-nine screen",
        "scope": (
            "q has two unit diagonal edges per colour; all six endpoint "
            "stars have at most two decorated ports with arbitrary "
            "projective coefficients over the screened finite field. "
            "Supports are quotiented by S6 and the endpoint-swap plus "
            "physical/channel 0<->1 transport preserving selected 01."
        ),
        "q_support_orbits": len(representatives),
        "prime_records": prime_records,
    }
    logical = sha256(json.dumps(result, sort_keys=True,
                                separators=(",", ":")).encode()).hexdigest()
    result["logical_sha256"] = logical
    return result


def main(write_results=False):
    result = build()
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "q_support_orbits": result["q_support_orbits"],
        "prime_summaries": [{
            "prime": row["prime"],
            "orbits_screened": row["orbits_screened"],
            "literal_counterexample_found": row["literal_counterexample_found"],
        } for row in result["prime_records"]],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)
