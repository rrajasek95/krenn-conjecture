#!/usr/bin/env python3
"""Exact three-branch reduction for the diagonal 6+2 cofactor packet.

If a second colour d has permanent -1 in every 2x2 superedge block and
annihilates the pure cofactor gradient of colour c entrywise, then in every
block one of the two permanent terms of d is nonzero.  Consequently either
the two diagonal or the two off-diagonal cofactors of c vanish.  There are
2^6 choices.  Switching the two clones at any of the four supervertices and
permuting the supervertices reduces these choices to three orbits, detected
by the number 0, 2, or 4 of odd triangle parities.

This checker constructs the three exact Q-ideals for one colour:
  six permanent+1 equations, four triangle-2 equations, and the selected
  twelve pure-cofactor equations.  It asks Singular whether adjoining u*H-1
  gives the unit ideal.  A unit result is a characteristic-zero exclusion of
  that support branch; a nonunit result sharply identifies the residual.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
OUT = HERE / "results_diagonal_cofactor_branch_orbits.json"
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
TRIPLES = tuple(tuple(combination) for combination in (
    (0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        answer.extend((((first, second),) + tail)
                      for tail in perfect_matchings(rest))
    return tuple(answer)


PM8 = perfect_matchings(tuple(range(8)))


def variable_for_sites(u, v):
    if u > v:
        u, v = v, u
    i, x = divmod(u, 2)
    j, y = divmod(v, 2)
    if i == j:
        return None
    return 4 * EDGE_INDEX[(i, j)] + 2 * x + y


def normalize_poly(terms):
    result = Counter()
    for coefficient, monomial in terms:
        result[tuple(sorted(monomial))] += coefficient
    return {monomial: coefficient for monomial, coefficient in result.items()
            if coefficient}


def matching_poly(vertices):
    terms = []
    for matching in perfect_matchings(tuple(vertices)):
        monomial = tuple(variable_for_sites(u, v) for u, v in matching)
        monomial = tuple(index for index in monomial if index is not None)
        terms.append((1, monomial))
    return normalize_poly(terms)


def permanent_poly(edge):
    start = 4 * edge
    return normalize_poly(((1, (start, start + 3)),
                           (1, (start + 1, start + 2)),
                           (1, ())))


def triangle_poly(i, j, k):
    ij = EDGE_INDEX[(i, j)]
    ik = EDGE_INDEX[(i, k)]
    jk = EDGE_INDEX[(j, k)]
    terms = [(-2, ())]
    for x, y, z in product((0, 1), repeat=3):
        terms.append((1, (4 * ij + 2 * x + y,
                          4 * ik + 2 * (1 - x) + z,
                          4 * jk + 2 * (1 - y) + (1 - z))))
    return normalize_poly(terms)


def cofactor_poly(u, v):
    return matching_poly(tuple(site for site in range(8)
                               if site not in (u, v)))


def q_poly(index):
    bits = tuple((index >> (3 - site)) & 1 for site in range(4))
    terms = []
    for (i, j), (k, l) in (((0, 1), (2, 3)),
                           ((0, 2), (1, 3)),
                           ((0, 3), (1, 2))):
        first = 4 * EDGE_INDEX[(i, j)] + 2 * bits[i] + bits[j]
        second = 4 * EDGE_INDEX[(k, l)] + 2 * bits[k] + bits[l]
        terms.append((1, (first, second)))
    return normalize_poly(terms)


def poly_to_singular(poly):
    pieces = []
    for monomial, coefficient in sorted(poly.items(),
                                        key=lambda item: (len(item[0]), item[0])):
        if not monomial:
            body = str(abs(coefficient))
        else:
            counts = Counter(monomial)
            factors = [("u" if index == 24 else f"x{index}")
                       + (f"^{power}" if power != 1 else "")
                       for index, power in sorted(counts.items())]
            body = "*".join(factors)
            if abs(coefficient) != 1:
                body = f"{abs(coefficient)}*{body}"
        if not pieces:
            pieces.append(("-" if coefficient < 0 else "") + body)
        else:
            pieces.append(("-" if coefficient < 0 else "+") + body)
    return "".join(pieces) if pieces else "0"


def transform_mask(mask, switches, permutation):
    answer = 0
    for edge_index, (i, j) in enumerate(EDGES):
        bit = (mask >> edge_index) & 1
        bit ^= switches[i] ^ switches[j]
        pi, pj = sorted((permutation[i], permutation[j]))
        target = EDGE_INDEX[(pi, pj)]
        answer |= bit << target
    return answer


def triangle_weight(mask):
    weight = 0
    for i, j, k in TRIPLES:
        parity = ((mask >> EDGE_INDEX[(i, j)])
                  ^ (mask >> EDGE_INDEX[(i, k)])
                  ^ (mask >> EDGE_INDEX[(j, k)])) & 1
        weight += parity
    return weight


def branch_orbits():
    group = tuple((switches, permutation)
                  for switches in product((0, 1), repeat=4)
                  if switches[0] == 0
                  for permutation in permutations(range(4)))
    require(len(group) == 192, "B4 quotient action size changed")
    unseen = set(range(64))
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {transform_mask(representative, *element)
                 for element in group}
        require(orbit <= unseen | (set(range(64)) - unseen),
                "orbit escaped mask universe")
        unseen -= orbit
        weights = {triangle_weight(mask) for mask in orbit}
        require(len(weights) == 1, "triangle weight is not invariant")
        orbits.append((representative, tuple(sorted(orbit)), weights.pop()))
    orbits.sort(key=lambda row: row[2])
    require([row[2] for row in orbits] == [0, 2, 4],
            "expected exactly the three switching classes")
    return group, tuple(orbits)


def singular_program(mask, characteristic=0):
    variables = ",".join([f"x{index}" for index in range(24)] + ["u"])
    generators = [permanent_poly(edge) for edge in range(6)]
    generators.extend(triangle_poly(*triple) for triple in TRIPLES)
    selected = []
    for edge, (i, j) in enumerate(EDGES):
        offdiagonal = (mask >> edge) & 1
        entries = ((0, 1), (1, 0)) if offdiagonal else ((0, 0), (1, 1))
        for x, y in entries:
            u, v = 2 * i + x, 2 * j + y
            generators.append(cofactor_poly(u, v))
            selected.append((u, v))
    hafnian = matching_poly(tuple(range(8)))
    generators.append(normalize_poly(tuple((coefficient, monomial + (24,))
                                            for monomial, coefficient
                                            in hafnian.items()) + ((-1, ()),)))
    program = (
        f"ring r={characteristic},({variables}),dp;\n"
        "option(redSB);\n"
        "ideal I=" + ",\n".join(poly_to_singular(poly)
                                  for poly in generators) + ";\n"
        "ideal G=std(I);\n"
        'print("MARK_SIZE"); size(G);\n'
        'print("MARK_ONE"); reduce(1,G);\n'
        'print("MARK_HILB"); vdim(G);\n'
    )
    return program, selected, len(generators), len(hafnian)


def run_singular(mask, characteristic, timeout):
    program, selected, generator_count, hafnian_terms = singular_program(
        mask, characteristic)
    started = time.monotonic()
    try:
        completed = subprocess.run(
            ["Singular", "-q"], input=program, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            timeout=timeout, check=False)
        elapsed = time.monotonic() - started
        output = completed.stdout
        markers = {}
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        for marker in ("MARK_SIZE", "MARK_ONE", "MARK_HILB"):
            if marker in lines:
                index = lines.index(marker)
                markers[marker] = lines[index + 1] if index + 1 < len(lines) else None
        return {
            "characteristic": characteristic,
            "timed_out": False,
            "return_code": completed.returncode,
            "elapsed_seconds": elapsed,
            "selected_cofactor_site_edges": [list(edge) for edge in selected],
            "generator_count_including_uH_minus_1": generator_count,
            "hafnian_monomial_count": hafnian_terms,
            "markers": markers,
            "output_tail": lines[-12:],
            "unit_ideal": markers.get("MARK_ONE") == "0",
        }
    except subprocess.TimeoutExpired as error:
        return {
            "characteristic": characteristic,
            "timed_out": True,
            "elapsed_seconds": time.monotonic() - started,
            "selected_cofactor_site_edges": [list(edge) for edge in selected],
            "generator_count_including_uH_minus_1": generator_count,
            "hafnian_monomial_count": hafnian_terms,
            "partial_output_tail": (error.stdout or "")[-1000:],
            "unit_ideal": None,
        }


def main():
    require(len(PM8) == 105, "perfect-matching census changed")
    group, orbits = branch_orbits()
    print("branch orbits:", [(row[0], len(row[1]), row[2]) for row in orbits],
          flush=True)
    records = []
    for representative, orbit, weight in orbits:
        print(f"starting branch weight={weight} mask={representative}", flush=True)
        # A short modular control catches construction errors before the
        # exact-Q run.  The Q computation is the theorem-bearing result.
        mod3 = run_singular(representative, 3, 120)
        print("  mod3:", mod3["unit_ideal"], mod3["elapsed_seconds"], flush=True)
        exact = run_singular(representative, 0, 300)
        print("  exact:", exact["unit_ideal"], exact["elapsed_seconds"], flush=True)
        records.append({
            "representative_mask": representative,
            "representative_edge_bits": [
                (representative >> edge) & 1 for edge in range(6)],
            "triangle_parity_weight": weight,
            "orbit_size": len(orbit),
            "orbit_masks": list(orbit),
            "mod3_singular": mod3,
            "exact_Q_singular": exact,
        })
    result = {
        "status": "UNAUDITED exact cofactor branch-orbit saturation audit",
        "edge_order": [list(edge) for edge in EDGES],
        "switch_permutation_group_size": len(group),
        "branch_count": sum(len(row[1]) for row in orbits),
        "branch_orbit_count": len(orbits),
        "records": records,
        "theorem_scope": (
            "If all three exact-Q runs are unit ideals, no live one-colour "
            "graph satisfying the six permanent and four triangle rows can "
            "be cofactor-compatible with even one second colour. This closes "
            "the same-colour diagonal 78+144 packet before using 4+4 rows."
        ),
        "negative_scope": (
            "A timeout or nonunit branch is not a full-packet counterexample; "
            "it still must be paired with a second graph and satisfy Q-cross "
            "products."
        ),
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["result_sha256"] = sha256(logical.encode("ascii")).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("result sha256:", result["result_sha256"])
    if not all(record["exact_Q_singular"]["unit_ideal"] for record in records):
        sys.exit(2)


if __name__ == "__main__":
    main()
