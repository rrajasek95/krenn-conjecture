#!/usr/bin/env python3
"""Shared-star unit ideals for the rank-one directions E10/E20.

Characteristic-zero programs close the star systems on the two normal
shapes established by the W-structure certificates:

* the line packet keeps all nine A23 entries and t as polynomial
  variables and asks the two-colour {0,1} packet to reach a multiple of
  the direct tensor H; it is split into the x00-invertible and x00 = 0
  cases purely to bound Groebner time;
* on the degenerate locus D_full, where the normal is span{H, D}, a
  single colour pair does NOT obstruct everywhere: the clean-room audit
  exhibits star solutions of the {0,1} packet on {X = a0 E00, t = 0}
  (where H - D = a0*[0^6] puts the colour-0 target inside the normal),
  and the {1,2} packet has solutions at X = E21.  Instead a BRANCH COVER
  certifies the obstruction: every D_full point lies in a branch whose
  packet is a unit ideal, and a full three-colour repair would restrict
  to a solution of every pair packet, so no branch point admits one.

The branches (direction 10 parameterization X = v (x) r0 + m (x) e1,
v = e0 + t e1, m = (0, w, u), so w sits on E11 and u on E21):

  A10: t inverted (Rabinowitsch), colours {0,1};
  B10: t = 0, u inverted, colours {0,1};
  C10: t = 0, u = 0, colours {1,2};
  A20: direction 20, t inverted, colours {0,1}.

At t = 0 both directions' moving blocks equal E00 and both D_full loci
degenerate to the SAME family {X = e0 (x) r0 + x11 E11 + x21 E21} (only
the parameter names swap), so branches B10 and C10 literally cover
direction 20's t = 0 locus as well; verify_t0_identity() checks that
block identity exactly.  A unit Groebner basis over
Q[parameters, scalars, stars] specializes to every complex parameter
point, so the five packets cover both directions' D_full completely,
with no torus normalization and t = 0 included.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import shutil
import subprocess
import time

import sympy as sp

import derive_three_cut_internal_23_adjacent_25_rank_one_w_structure as wstruct
import explore_three_cut_internal_23_adjacent_25_rank_one_directions as rankone
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations


ACTIVE = (0, 1)
T = rankone.T
X9 = wstruct.X9


def singular_text(value):
    value = sp.cancel(value)
    if value == 0:
        return "0"
    return str(value).replace("**", "^")


def beta(word_terms, a, b, word):
    terms = []
    for (left, right), coefficient in word_terms.get(word, ()):
        factor = singular_text(coefficient)
        terms.append(
            f"({factor})*{equations.variable('p', a, left)}*"
            f"{equations.variable('q', b, right)}"
        )
        terms.append(
            f"({factor})*{equations.variable('p', a, right)}*"
            f"{equations.variable('q', b, left)}"
        )
    return "+".join(terms) if terms else "0"


def build_program(blocks, parameter_names, basis, extra_generators=(),
                  colours=ACTIVE):
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    hs = {
        word: sp.expand(value) for word, value in hs.items()
        if sp.expand(value) != 0
    }
    word_terms = equations.reconstruct_word_terms(blocks)
    coordinates = tuple(sorted(
        set(word_terms) | set(hs)
        | set().union(*(set(vector) for vector in basis))
        | {(colour,) * 6 for colour in colours}
    ))
    endpoints = tuple(itertools.product(full.SIX, full.COLOURS))
    star_names = [
        equations.variable(kind, boundary, endpoint)
        for kind in ("p", "q") for boundary in colours for endpoint in endpoints
    ]
    scalar_names = []
    scalars = {}
    for i in range(len(basis)):
        for a, b in itertools.product(colours, repeat=2):
            name = f"s{i}{a}{b}"
            scalars[i, a, b] = name
            scalar_names.append(name)
    generators = list(extra_generators)
    for a, b in itertools.product(colours, repeat=2):
        for word in coordinates:
            terms = [beta(word_terms, a, b, word)]
            if a == b and word == (a,) * 6:
                terms.append("-1")
            for i, vector in enumerate(basis):
                if word in vector:
                    terms.append(
                        f"-({singular_text(vector[word])})*{scalars[i, a, b]}"
                    )
            expression = "+".join(terms)
            if expression != "0":
                generators.append(expression)
    generators = list(dict.fromkeys(generators))
    body = ",".join(generators)
    names = parameter_names + scalar_names + [
        name for name in star_names if name in body
    ]
    program = "ring r=0,(" + ",".join(names) + "),dp;\n"
    program += "option(redSB);\n"
    program += "ideal I=" + body + ";\n"
    program += "ideal G=slimgb(I);\n"
    program += 'print("UNIT"); if(G[1]==1){1;}else{0;}\n'
    program += 'print("GBSIZE"); size(G);\n'
    return program, len(generators), len(names), len(coordinates)


def h_basis(blocks):
    hs = equations.cylinders.matching_tensor(full.SIX, blocks)
    return [{
        word: sp.expand(value) for word, value in hs.items()
        if sp.expand(value) != 0
    }]


def line_jobs(key, split=True):
    spec = rankone.select_direction(key)
    jobs = []
    blocks = wstruct.nine_symbol_blocks(key)
    if split:
        program, generators, variables, coordinates = build_program(
            blocks, [str(symbol) for symbol in X9] + ["t", "yinv"],
            h_basis(blocks), ("1-yinv*x00",),
        )
        jobs.append({
            "name": f"line_{key}_x00_invertible",
            "program": program, "generators": generators,
            "variables": variables, "coordinates": coordinates,
        })
        blocks0 = equations.cylinders.aggregate()
        blocks0[2, 3] = {
            cell: X9[bit] for bit, cell in enumerate(full.CELLS) if bit != 0
        }
        block25 = dict(blocks0[2, 5])
        block25[spec["t_cell"]] = (
            block25.get(spec["t_cell"], sp.Integer(0)) + T
        )
        blocks0[2, 5] = block25
        program, generators, variables, coordinates = build_program(
            blocks0, [str(symbol) for symbol in X9[1:]] + ["t"],
            h_basis(blocks0),
        )
        jobs.append({
            "name": f"line_{key}_x00_zero",
            "program": program, "generators": generators,
            "variables": variables, "coordinates": coordinates,
        })
    else:
        program, generators, variables, coordinates = build_program(
            blocks, [str(symbol) for symbol in X9] + ["t"], h_basis(blocks),
        )
        jobs.append({
            "name": f"line_{key}_full",
            "program": program, "generators": generators,
            "variables": variables, "coordinates": coordinates,
        })
    return jobs


def branch_blocks(key, substitution):
    rankone.select_direction(key)
    blocks = wstruct.d_full_blocks(key)
    if substitution:
        blocks = {
            edge: {
                cell: sp.expand(sp.sympify(value).subs(substitution))
                for cell, value in block.items()
            }
            for edge, block in blocks.items()
        }
        blocks = {
            edge: {cell: value for cell, value in block.items() if value != 0}
            for edge, block in blocks.items()
        }
    return blocks


def branch_basis(key, substitution):
    blocks = branch_blocks(key, substitution)
    d_tensor = {
        word: sp.expand(
            sp.sympify(value).subs(substitution) if substitution else value
        )
        for word, value in rankone.d_plane_tensor(key, T).items()
    }
    d_tensor = {word: value for word, value in d_tensor.items() if value != 0}
    return blocks, h_basis(blocks) + [d_tensor]


U_SYMBOL = sp.Symbol("u")

BRANCHES = (
    ("branch_10_A_t_inverted", "10", (0, 1), None, "1-y*t"),
    ("branch_10_B_t0_u_inverted", "10", (0, 1), {"t": 0}, "1-y*u"),
    ("branch_10_C_t0_u0", "10", (1, 2), {"t": 0, "u": 0}, None),
    ("branch_20_A_t_inverted", "20", (0, 1), None, "1-y*t"),
)


def branch_job(name, key, colours, substitution_spec, rabinowitsch):
    substitution = None
    gone = set()
    if substitution_spec:
        substitution = {}
        for symbol_name, value in substitution_spec.items():
            symbol = T if symbol_name == "t" else U_SYMBOL
            substitution[symbol] = sp.Integer(value)
            gone.add(symbol_name)
    blocks, basis = branch_basis(key, substitution)
    parameters = [p for p in ("a0", "a1", "a2", "w", "u", "t") if p not in gone]
    extra = ("y",) if rabinowitsch else ()
    program, generators, variables, coordinates = build_program(
        blocks, parameters + list(extra), basis,
        (rabinowitsch,) if rabinowitsch else (),
        colours=colours,
    )
    return {
        "name": name,
        "program": program, "generators": generators,
        "variables": variables, "coordinates": coordinates,
    }


def branch_jobs():
    return [branch_job(*spec) for spec in BRANCHES]


def verify_t0_identity():
    """At t = 0 the two directions' D_full blocks coincide exactly and
    both loci are {X = e0 (x) r0 + x11 E11 + x21 E21}: direction 10 uses
    (w, u) = (x11, x21) and direction 20 uses (w, u) = (x21, x11)."""
    substitution = {T: sp.Integer(0)}
    blocks10 = branch_blocks("10", substitution)
    blocks20 = branch_blocks("20", substitution)
    swap = {sp.Symbol("w"): sp.Symbol("u"), sp.Symbol("u"): sp.Symbol("w")}
    swapped20 = {
        edge: {
            cell: sp.expand(sp.sympify(value).subs(swap, simultaneous=True))
            for cell, value in block.items()
        }
        for edge, block in blocks20.items()
    }
    assert blocks10 == swapped20, "t=0 identity failed"
    def monic_set(key):
        polynomials = set()
        for generator in wstruct.d_full_generators(key):
            value = sp.expand(sp.sympify(generator).subs(substitution))
            leading = sp.LC(sp.Poly(value, *sorted(value.free_symbols, key=str)))
            polynomials.add(sp.expand(value / leading))
        return polynomials

    assert monic_set("10") == monic_set("20"), "t=0 locus mismatch"
    return True


def all_jobs(split=True):
    jobs = []
    for key in ("10", "20"):
        jobs.extend(line_jobs(key, split=split))
    jobs.extend(branch_jobs())
    for job in jobs:
        job["sha256"] = hashlib.sha256(job["program"].encode()).hexdigest()
    return jobs


def marker(output, name):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return int(lines[lines.index(name) + 1])


def run_job(job, timeout=14400):
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=job["program"], text=True,
        capture_output=True, check=True, timeout=timeout,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    unit = marker(completed.stdout, "UNIT")
    size = marker(completed.stdout, "GBSIZE")
    assert (unit, size) == (1, 1), (job["name"], unit, size)
    return time.monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=14400)
    parser.add_argument("--no-split", action="store_true")
    arguments = parser.parse_args()
    jobs = all_jobs(split=not arguments.no_split)
    for job in jobs:
        print(
            "JOB", job["name"], f'generators={job["generators"]}',
            f'variables={job["variables"]}',
            f'coordinates={job["coordinates"]}',
            f'sha256={job["sha256"]}', flush=True,
        )
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=arguments.workers
    ) as executor:
        elapsed = list(executor.map(
            lambda job: run_job(job, arguments.timeout), jobs,
        ))
    for job, seconds in zip(jobs, elapsed):
        print("RESULT", job["name"], "unit=1 gbsize=1",
              f"seconds={seconds:.3f}", flush=True)


if __name__ == "__main__":
    main()
