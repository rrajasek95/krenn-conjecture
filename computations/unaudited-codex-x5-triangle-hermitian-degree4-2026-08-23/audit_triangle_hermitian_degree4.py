#!/usr/bin/env python3
"""Bounded exact audit of triangle-sensitive Hermitian degree-four identities.

The interpolation is deliberately small and source-faithful.  It tests the
natural S8 x S3 averaged spectral moments of the literal 108 x 9 triangle
response matrices on exactly balanced signed sources.  A modular rank jump
is a characteristic-zero nonmembership certificate for this stated ansatz;
it is not advertised as a census of all Hermitian invariants.
"""

from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RESULT = HERE / "results_triangle_hermitian_degree4.json"
GUARD = (ROOT / "computations/unaudited-codex-allrank9-minnorm-counterguard-2026-08-23"
         / "results_allrank9_minnorm_counterguard.json")
GUARD_SHA = "3a101009ca29397afab7cfe7d2a6ca2c73012bcf2d778323cfc6178ebcbe54e6"
PRIMES = (1009, 1013)
SAMPLES = 21
MIXED_PROFILES = (
    (7, 1, 0), (6, 2, 0), (6, 1, 1), (5, 3, 0), (5, 2, 1),
    (4, 4, 0), (4, 3, 1), (4, 2, 2), (3, 3, 2),
)
PROFILE_SIZES = (48, 168, 168, 336, 1008, 210, 1680, 1260, 1680)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


PM8 = tuple(perfect_matchings(range(8)))
EDGES = tuple(combinations(range(8), 2))
EDGE_INDEX = {edge: i for i, edge in enumerate(EDGES)}


def signed_source(sample):
    """A deterministic dense +/-1 source, exactly moment-balanced.

    Every one of the 24 site-colour ports has squared weighted degree 21,
    and every physical edge block has squared norm 9.
    """
    values = []
    for index in range(252):
        digest = sha256(f"triangle-hermitian-v1:{sample}:{index}".encode()).digest()
        values.append(1 if digest[0] & 1 else -1)
    return values


def cell(source, u, v, a, b, prime):
    if u < v:
        index = 9 * EDGE_INDEX[u, v] + 3 * a + b
    else:
        index = 9 * EDGE_INDEX[v, u] + 3 * b + a
    return source[index] % prime


def output_norms(source, prime):
    pure = 0
    mixed = 0
    profiles = {profile: 0 for profile in MIXED_PROFILES}
    for word in product(range(3), repeat=8):
        amplitude = 0
        for matching in PM8:
            term = 1
            for u, v in matching:
                term = term * cell(source, u, v, word[u], word[v], prime) % prime
            amplitude = (amplitude + term) % prime
        square = amplitude * amplitude % prime
        if all(colour == word[0] for colour in word):
            pure = (pure + square) % prime
        else:
            mixed = (mixed + square) % prime
            profile = tuple(sorted((word.count(0), word.count(1), word.count(2)),
                                   reverse=True))
            profiles[profile] = (profiles[profile] + square) % prime
    return pure, mixed, [profiles[profile] for profile in MIXED_PROFILES]


def response_moments(source, prime):
    q = [0] * 7
    for p, cap_q in EDGES:
        residual = tuple(site for site in range(8) if site not in (p, cap_q))
        avec = [cell(source, p, cap_q, i, j, prime)
                for i in range(3) for j in range(3)]
        anorm = sum(x * x for x in avec) % prime
        for triangle in combinations(residual, 3):
            allowed = set(combinations(triangle, 2))
            outside = tuple(edge for edge in combinations(residual, 2)
                            if edge not in allowed)
            require(len(outside) == 12, (p, cap_q, triangle, len(outside)))
            gram = [[0] * 9 for _ in range(9)]
            for a, b in outside:
                for alpha in range(3):
                    for beta in range(3):
                        row = []
                        for i in range(3):
                            for j in range(3):
                                value = (
                                    cell(source, p, a, i, alpha, prime)
                                    * cell(source, cap_q, b, j, beta, prime)
                                    + cell(source, p, b, i, beta, prime)
                                    * cell(source, cap_q, a, j, alpha, prime)
                                ) % prime
                                row.append(value)
                        for i in range(9):
                            ri = row[i]
                            for j in range(i, 9):
                                gram[i][j] = (gram[i][j] + ri * row[j]) % prime
            for i in range(9):
                for j in range(i):
                    gram[i][j] = gram[j][i]
            trace = sum(gram[i][i] for i in range(9)) % prime
            trace2 = sum(gram[i][j] * gram[j][i]
                         for i in range(9) for j in range(9)) % prime
            diag = (0, 4, 8)
            diag_norms = [gram[i][i] for i in diag]
            q[0] = (q[0] + trace * trace) % prime
            q[1] = (q[1] + trace2) % prime
            q[2] = (q[2] + sum(x * x for x in diag_norms)) % prime
            q[3] = (q[3] + sum(diag_norms[i] * diag_norms[j]
                               for i in range(3) for j in range(i + 1, 3))) % prime
            q[4] = (q[4] + sum(gram[diag[i]][diag[j]] ** 2
                               for i in range(3) for j in range(i + 1, 3))) % prime
            ga = [sum(gram[i][j] * avec[j] for j in range(9)) % prime
                  for i in range(9)]
            response_direct = sum(avec[i] * ga[i] for i in range(9)) % prime
            q[5] = (q[5] + response_direct * anorm) % prime
            q[6] = (q[6] + sum(diag_norms) * anorm * anorm) % prime
    return q


def dense_rank(matrix, prime):
    rows = [list(row) for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows))
                      if rows[i][column] % prime), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column] % prime, prime - 2, prime)
        rows[rank] = [value * inverse % prime for value in rows[rank]]
        for i in range(len(rows)):
            if i == rank or not rows[i][column] % prime:
                continue
            factor = rows[i][column] % prime
            rows[i] = [(a - factor * b) % prime
                       for a, b in zip(rows[i], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def weak_compositions(total, slots, prefix=()):
    if slots == 1:
        yield prefix + (total,)
        return
    for value in range(total + 1):
        yield from weak_compositions(total - value, slots - 1,
                                     prefix + (value,))


S3 = tuple(permutations(range(3)))


def permute_table(table, sigma):
    inverse = {sigma[i]: i for i in range(3)}
    return tuple(table[3 * inverse[i] + inverse[j]]
                 for i in range(3) for j in range(3))


def transpose_table(table):
    return tuple(table[3 * j + i] for i in range(3) for j in range(3))


def orbit_census():
    tables = tuple(weak_compositions(8, 9))
    canonical = {min(permute_table(table, sigma) for sigma in S3)
                 for table in tables}
    hermitian = {min(min(permute_table(table, sigma) for sigma in S3),
                     min(permute_table(transpose_table(table), sigma)
                         for sigma in S3))
                 for table in tables}
    return len(tables), len(canonical), len(hermitian)


def audit(mutate=False):
    require(sha256(GUARD.read_bytes()).hexdigest() == GUARD_SHA,
            "all-rank9 guard drift")
    guard = json.loads(GUARD.read_text())
    require(guard["logical_sha256"] ==
            "f281d19d320993a5408d7dfb97f40953800d0a58abc2f63d8e0bb08d57abfaa1",
            "all-rank9 logical guard drift")
    raw_tables, ordered_orbits, hermitian_orbits = orbit_census()
    require((raw_tables, ordered_orbits, hermitian_orbits) == (12870, 2180, 1188),
            (raw_tables, ordered_orbits, hermitian_orbits))

    feature_names = [
        "sum_triangle_trace_gram_squared",
        "sum_triangle_trace_gram2",
        "sum_diagonal_column_norm4",
        "sum_diagonal_column_norm_products",
        "sum_diagonal_column_innerproduct_abs2",
        "sum_direct_response_norm2_times_cap_norm2",
        "sum_diagonal_response_norm2_times_cap_norm4",
        "pure_output_norm2",
        "source_norm2_power4",
    ]
    interpolation = {}
    for prime in PRIMES:
        rows = []
        for sample in range(SAMPLES):
            source = signed_source(sample)
            require(sum(value * value for value in source) == 252,
                    "signed balance changed")
            pure, mixed, profile_norms = output_norms(source, prime)
            moments = response_moments(source, prime)
            norm8 = pow(252, 4, prime)
            rows.append(profile_norms + moments + [pure, norm8, mixed])
        x5_rank = dense_rank([row[:9] for row in rows], prime)
        triangle_rank = dense_rank([row[9:-1] for row in rows], prime)
        joint_rank = dense_rank([row[:-1] for row in rows], prime)
        feature_rank = triangle_rank
        augmented_rank = dense_rank([row[9:] for row in rows], prime)
        if mutate and prime == PRIMES[0]:
            augmented_rank = feature_rank
        require(augmented_rank == feature_rank + 1,
                (prime, feature_rank, augmented_rank))
        require(joint_rank == x5_rank + triangle_rank,
                (prime, x5_rank, triangle_rank, joint_rank))
        interpolation[str(prime)] = {
            "samples": SAMPLES,
            "literal_X5_profile_norm_rank": x5_rank,
            "feature_rank": feature_rank,
            "joint_rank": joint_rank,
            "X5_triangle_span_intersection_dimension": 0,
            "augmented_with_mixed_norm_rank": augmented_rank,
            "first_three_target_values": [row[-1] for row in rows[:3]],
        }

    result = {
        "format": "n8-x5-triangle-hermitian-degree4-audit-v1",
        "status": "EXACT_SCOPED_NO_LOW_DEGREE_TRIANGLE_HERMITIAN_IDENTITY",
        "degree_census": {
            "mixed_amplitude_norm": [4, 4],
            "triangle_response_entry_holomorphic_degree": 2,
            "triangle_response_quartic_spectral_moments": [4, 4],
            "fixed_K_clean_cap_error_holomorphic_degree": 6,
            "clean_cap_error_norm": [6, 6],
            "rank9_determinant_holomorphic_degree": 18,
            "rank9_determinant_norm": [18, 18],
            "consequence": (
                "Neither a clean-cap error square nor a polynomial rank-drop "
                "detector can occur in a bidegree-(4,4) polynomial identity."
            ),
        },
        "representation_census": {
            "ordered_word_pair_contingency_tables": raw_tables,
            "S8_x_S3_ordered_pair_orbits": ordered_orbits,
            "real_Hermitian_orbits_after_transpose": hermitian_orbits,
            "guard": (
                "This is the complete output-quadratic orbit census, not a "
                "claim that output moments detect source response rank."
            ),
            "literal_X5_mixed_word_profiles": {
                "profiles": [list(profile) for profile in MIXED_PROFILES],
                "orbit_sizes": list(PROFILE_SIZES),
                "sum": sum(PROFILE_SIZES),
            },
        },
        "natural_triangle_moment_ansatz": {
            "features": feature_names,
            "interpolation": interpolation,
            "sources": (
                "deterministic dense +/-1 sources; every site-colour port has "
                "squared weighted degree 21 and every edge block norm2 9, so "
                "they are exactly moment-zero for the site-colour torus"
            ),
            "characteristic_zero_consequence": (
                "At either prime, the augmented rank jump is a nonzero integer "
                "minor, so mixed norm is not in the Q-span of the stated nine "
                "natural S8xS3-averaged bidegree-(4,4) moments. The nine literal "
                "X5 profile norms and the nine triangle/control moments have "
                "zero interpolated intersection, so there is no accidental "
                "constant-coefficient coupling in this ansatz."
            ),
        },
        "positive_identity_counterguard": {
            "pinned_logical_sha256": guard["logical_sha256"],
            "properties": (
                "balanced strict local norm minimum; every one of the 560 "
                "literal triangle matrices L_T has rank9; all 6558 mixed "
                "amplitudes are nonzero"
            ),
            "consequence": (
                "On this source ker(L_T)=0 for every triangle, hence every "
                "nonnegative sum indexed by triangle-response kernels is zero "
                "while P_mixed is positive. Such a universal positive identity "
                "is impossible even before imposing X5."
            ),
        },
        "verdict": (
            "The load-bearing X5 rows cannot be converted into the proposed "
            "low-degree positive Hermitian identity by triangle spectral "
            "moments. X5 may still imply a higher-degree or localized identity; "
            "the first polynomial terms capable of seeing cap error/rank drop "
            "occur in bidegrees (6,6)/(18,18)."
        ),
        "scope": (
            "Exact no-go for kernel-square identities and for the explicitly "
            "listed natural bidegree-(4,4) invariant ansatz. The interpolation "
            "does not rule out all 1188 output Hermitian orbit forms, identities "
            "modulo the X5 ideal, rational identities on a response-minor open, "
            "or higher-degree Positivstellensatz certificates."
        ),
        "source_sha256": {str(GUARD.relative_to(ROOT)): GUARD_SHA},
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(logical.encode()).hexdigest()
    return result


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = audit(args.mutate)
    if args.write_results:
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    if args.check_results:
        require(RESULT.exists() and json.loads(RESULT.read_text()) == result,
                "stored result drift")
    print(result["status"])
    print(result["natural_triangle_moment_ansatz"]["interpolation"])
    print(result["logical_sha256"])


if __name__ == "__main__":
    main()
