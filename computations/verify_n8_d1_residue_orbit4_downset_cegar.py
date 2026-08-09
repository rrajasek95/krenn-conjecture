#!/usr/bin/env python3
"""Exact support-CEGAR frontier below the maximal O4 residue orbit."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib
import itertools
import os
import sys
from time import monotonic

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_CLOSURE_SHA256 = (
    "cffd8ac0c5d54fddd365e4a610f2bed00881683a61733669e2bb41af972ecad1"
)
SOURCE = os.path.join(HERE,
                      "verify_n8_d1_residue_orbit4_four_star_lemma.py")
with open(SOURCE, "rb") as handle:
    source_digest = hashlib.sha256(handle.read()).hexdigest()
if PINNED_CLOSURE_SHA256 != "TO_BE_PINNED":
    require(source_digest == PINNED_CLOSURE_SHA256,
            "the pinned O4 six-site closure changed")
F = importlib.import_module("verify_n8_d1_residue_orbit4_four_star_lemma")
S, C, D, V, O = F.S, F.C, F.D, F.V, F.O

PINNED_ALIGNMENT_SHA256 = (
    "30095da401628a401cbdd2756b6dc3276f3c83cba62538097bd2c70c6481b26d"
)
ALIGNMENT_SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_target_alignment_lemma.py"
)
with open(ALIGNMENT_SOURCE, "rb") as handle:
    alignment_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(alignment_source_digest == PINNED_ALIGNMENT_SHA256,
        "the pinned O4 target-alignment lemma changed")
A = importlib.import_module(
    "verify_n8_d1_residue_orbit4_target_alignment_lemma"
)

PINNED_BOUNDARY_STAR_SHA256 = (
    "db370243f235d1aa5f4315022c54f0d7a8fc8dc318391734f3413438c8c453c3"
)
BOUNDARY_STAR_SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_boundary_star_quotient.py"
)
with open(BOUNDARY_STAR_SOURCE, "rb") as handle:
    boundary_star_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(boundary_star_source_digest == PINNED_BOUNDARY_STAR_SHA256,
        "the pinned O4 boundary-star quotient changed")
BQ = importlib.import_module(
    "verify_n8_d1_residue_orbit4_boundary_star_quotient"
)

PINNED_INCIDENCE_SHA256 = (
    "96bdbf54797b283c7239042ad2b3a9b0d052603aa63d74e491d29527f702337c"
)
INCIDENCE_SOURCE = os.path.join(
    HERE, "verify_n8_d1_one_site_target_incidence.py"
)
with open(INCIDENCE_SOURCE, "rb") as handle:
    incidence_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(incidence_source_digest == PINNED_INCIDENCE_SHA256,
        "the pinned N8 target-incidence theorem changed")
I = importlib.import_module("verify_n8_d1_one_site_target_incidence")

PINNED_ODD_CIRCUIT_SHA256 = (
    "95f75391b40d9e006b4580cf2fa5e34e4930ec87facb7bef5391b419af2c3507"
)
ODD_CIRCUIT_SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_incidence_frontier_odd_circuit.py"
)
with open(ODD_CIRCUIT_SOURCE, "rb") as handle:
    odd_circuit_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(odd_circuit_source_digest == PINNED_ODD_CIRCUIT_SHA256,
        "the pinned O4 incidence-frontier odd circuit changed")
OC = importlib.import_module(
    "verify_n8_d1_residue_orbit4_incidence_frontier_odd_circuit"
)

PINNED_ITERATED_LAURENT_SHA256 = (
    "290195e979282bee0029a4cf02012b79ecba2212bf87daacb2710ff9cf6edf63"
)
ITERATED_LAURENT_SOURCE = os.path.join(
    HERE,
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent.py",
)
with open(ITERATED_LAURENT_SOURCE, "rb") as handle:
    iterated_laurent_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(iterated_laurent_source_digest == PINNED_ITERATED_LAURENT_SHA256,
        "the pinned second O4 incidence-frontier closure changed")
IL = importlib.import_module(
    "verify_n8_d1_residue_orbit4_second_incidence_frontier_iterated_laurent"
)

PINNED_THIRD_SATURATION_SHA256 = (
    "44910ac9885cf58ac34b0f70845918c3e42be1996ef569e92604ec44b4e15b20"
)
THIRD_SATURATION_SOURCE = os.path.join(
    HERE,
    "verify_n8_d1_residue_orbit4_third_incidence_frontier_saturation.py",
)
with open(THIRD_SATURATION_SOURCE, "rb") as handle:
    third_saturation_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(third_saturation_source_digest == PINNED_THIRD_SATURATION_SHA256,
        "the pinned third O4 incidence-frontier closure changed")
TS = importlib.import_module(
    "verify_n8_d1_residue_orbit4_third_incidence_frontier_saturation"
)

PINNED_FOURTH_ODD_SHA256 = (
    "80796a4110facb4c24c403af3edb50f25f650b8a860e02c25022dc868b47927b"
)
FOURTH_ODD_SOURCE = os.path.join(
    HERE,
    "verify_n8_d1_residue_orbit4_fourth_incidence_frontier_odd_circuit.py",
)
with open(FOURTH_ODD_SOURCE, "rb") as handle:
    fourth_odd_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(fourth_odd_source_digest == PINNED_FOURTH_ODD_SHA256,
        "the pinned fourth O4 incidence-frontier closure changed")
FO = importlib.import_module(
    "verify_n8_d1_residue_orbit4_fourth_incidence_frontier_odd_circuit"
)

PINNED_158_BATCH_SHA256 = (
    "8bed466723fe37da34136f4c10f5d49e866984effddcb69b56dbdf0bbde6335e"
)
BATCH_158_SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_158_direct_batch.py"
)
with open(BATCH_158_SOURCE, "rb") as handle:
    batch_158_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(batch_158_source_digest == PINNED_158_BATCH_SHA256,
        "the pinned O4 158-cell direct batch changed")
B158 = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_direct_batch"
)

PINNED_158_SECOND_LAYER_SHA256 = (
    "5c47e1e72874afcc70ae7e4646e9f20acb2ba3a51a6b36c9451cc24ed1a0c4fa"
)
SECOND_LAYER_158_SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_158_second_layer_collision.py"
)
with open(SECOND_LAYER_158_SOURCE, "rb") as handle:
    second_layer_158_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(second_layer_158_source_digest == PINNED_158_SECOND_LAYER_SHA256,
        "the pinned O4 158-cell second-layer collision changed")
SL158 = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_second_layer_collision"
)

PINNED_158_THIRD_FACE_SHA256 = (
    "2374907445dcbb4419b4a0cedf0f6d17981b0bb301d8db7887f3fac24fab6113"
)
THIRD_FACE_158_SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_158_third_face_direct_unit.py"
)
with open(THIRD_FACE_158_SOURCE, "rb") as handle:
    third_face_158_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(third_face_158_source_digest == PINNED_158_THIRD_FACE_SHA256,
        "the pinned O4 third 158-cell direct unit changed")
TF158 = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_third_face_direct_unit"
)

PINNED_158_QUOTIENT_GRAPH_SHA256 = (
    "3f5c6039b502a0b5fa7430c29c5014112e81abd4570201b261b99380cce35939"
)
QUOTIENT_GRAPH_158_SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_158_quotient_character_oracle.py"
)
with open(QUOTIENT_GRAPH_158_SOURCE, "rb") as handle:
    quotient_graph_158_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(quotient_graph_158_source_digest == PINNED_158_QUOTIENT_GRAPH_SHA256,
        "the pinned O4 158-cell quotient-character oracle changed")
QG158 = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_quotient_character_oracle"
)

PINNED_158_CHARACTER_BATCH2_SHA256 = (
    "e31e396c8441bcf08f4bd0f91f8a690fd9315a7c415d1788a8a1c5631b061405"
)
CHARACTER_BATCH2_158_SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_158_character_graph_batch2.py"
)
with open(CHARACTER_BATCH2_158_SOURCE, "rb") as handle:
    character_batch2_158_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(character_batch2_158_source_digest == PINNED_158_CHARACTER_BATCH2_SHA256,
        "the pinned O4 later 158-cell character batch changed")
CB158 = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_character_graph_batch2"
)

PINNED_158_CHARACTER_COLLISION_SHA256 = (
    "4e7cf43e9d372905c00322f1d46248520d98ae975a8f2a716afea64790efca8a"
)
CHARACTER_COLLISION_158_SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_158_character_collision_batch.py"
)
with open(CHARACTER_COLLISION_158_SOURCE, "rb") as handle:
    character_collision_158_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(character_collision_158_source_digest == PINNED_158_CHARACTER_COLLISION_SHA256,
        "the pinned O4 later 158-cell character collision changed")
CC158 = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_character_collision_batch"
)

PINNED_158_INITIAL_ODD_SHA256 = (
    "8f71f339aaf4651ded0c89fa84aa2fd566f71b297cd5f86b1d3aa6a23bf1579e"
)
INITIAL_ODD_158_SOURCE = os.path.join(
    HERE, "verify_n8_d1_residue_orbit4_158_initial_odd_dependency.py"
)
with open(INITIAL_ODD_158_SOURCE, "rb") as handle:
    initial_odd_158_source_digest = hashlib.sha256(handle.read()).hexdigest()
require(initial_odd_158_source_digest == PINNED_158_INITIAL_ODD_SHA256,
        "the pinned O4 158-cell initial odd dependency changed")
IO158 = importlib.import_module(
    "verify_n8_d1_residue_orbit4_158_initial_odd_dependency"
)

EXPECTED_CNF_SHA256 = (
    "c3c9d31ced2d0befc451bae5818c6a1dc671d20c4ec6cfb8a51f80f30ce1d9aa"
)
EXPECTED_LEDGER_SHA256 = (
    "f6e05bdb27569b2f8c997d72db016983200696de45ec996a3bd6578b35d246df"
)
EXPECTED_MINIMUM_OMISSIONS = 36
EXPECTED_FRONTIER_MISSING = [
    [0, 1, 1, 0], [0, 2, 1, 0], [0, 3, 0, 1],
    [0, 6, 0, 0], [0, 6, 0, 1], [0, 6, 1, 0], [0, 6, 1, 1],
    [0, 7, 0, 1], [0, 7, 0, 2], [0, 7, 1, 0],
    [1, 2, 0, 1], [1, 3, 1, 0], [1, 3, 1, 2],
    [1, 4, 0, 1], [1, 4, 1, 0], [1, 5, 0, 1], [1, 5, 1, 0],
    [1, 6, 0, 1], [1, 6, 1, 0],
    [1, 7, 0, 0], [1, 7, 0, 1], [1, 7, 1, 0], [1, 7, 1, 1],
    [2, 6, 0, 0], [2, 6, 0, 1], [2, 6, 1, 0], [2, 6, 1, 1],
    [2, 6, 2, 0], [2, 6, 2, 1], [2, 7, 2, 0],
    [3, 7, 0, 0], [3, 7, 0, 1], [3, 7, 1, 0], [3, 7, 1, 1],
    [3, 7, 2, 0], [3, 7, 2, 1],
]
EXPECTED_FRONTIER_GENERATOR_SHA256 = (
    "45f70f0cb4b3e9e322861b220e2ff4290469ac4bdfe87808f2a0a45df6d8fd27"
)


def allowed_support():
    _state, _extras, _base, admissible, _stats = C.candidate_input()
    allowed = (set(admissible) - set(O.RESIDUE_HOLES)
               - set(S.BOUNDARY_OMISSIONS))
    require(len(allowed) == 193, "the O4 downset universe changed")
    return frozenset(allowed)


def build_cnf():
    cells = tuple(sorted(allowed_support()))
    index = {cell: position + 1 for position, cell in enumerate(cells)}
    next_variable = len(cells)
    clauses = []
    counts = Counter()

    def new_variable():
        nonlocal next_variable
        next_variable += 1
        return next_variable

    # Exact full 8,100-fibre support shadow, specialized before Tseitin.
    for domain in (V.RESIDUE, V.W1, V.W2, V.SITES):
        for values in itertools.product(V.COLORS, repeat=len(domain)):
            word = dict(zip(domain, values))
            terms = []
            for matching in V.MATCHINGS[tuple(domain)]:
                matching_cells = tuple(V.cell(u, v, word[u], word[v])
                                       for u, v in matching)
                if not all(cell in index for cell in matching_cells):
                    continue
                term = new_variable()
                terms.append(term)
                counts["live_matching_auxiliaries"] += 1
                for cell in matching_cells:
                    clauses.append([-term, index[cell]])
                clauses.append([term] + [-index[cell]
                                         for cell in matching_cells])
            pure = (len(set(values)) == 1 if domain == V.SITES
                    else set(values) == {2})
            if pure:
                require(terms, "a pure O4 downset fibre became empty")
                clauses.append(terms)
                counts["pure_fibres"] += 1
            else:
                # Exclude exactly one supported matching.
                for term in terms:
                    clauses.append([-term] + [other for other in terms
                                               if other != term])
                counts["zero_fibres"] += 1

    # Consequences of the checked injective-tripod/six-site proof.  Here P
    # is the boundary-u star and Q is the boundary-v star.
    for u, v in ((0, 2), (1, 3)):
        for a in (0, 1):
            P = [index[V.cell(u, residue, a, colour)]
                 for residue in V.RESIDUE for colour in V.COLORS]
            Pbar = [index[V.cell(u, 7, a, colour)] for colour in (0, 1)]
            Pother = [index[V.cell(u, residue, a, colour)]
                      for residue in (4, 5, 6) for colour in V.COLORS]
            for b in V.COLORS:
                Q = [index[V.cell(v, residue, b, colour)]
                     for residue in V.RESIDUE for colour in V.COLORS]
                Qbar = [index[V.cell(v, 7, b, colour)]
                        for colour in (0, 1)]
                Qother = [index[V.cell(v, residue, b, colour)]
                          for residue in (4, 5, 6)
                          for colour in V.COLORS]
                z = index[V.cell(u, v, a, b)]
                p72 = index[V.cell(u, 7, a, 2)]
                q72 = index[V.cell(v, 7, b, 2)]

                # If both non-target projections are nonzero, independent
                # projections die by injectivity.  Dependent projections
                # reduce to the checked tensor; either non-target P6 slice
                # closes it.
                for pbar in Pbar:
                    for qbar in Qbar:
                        for colour in (0, 1):
                            clauses.append([
                                -z, -index[V.cell(u, 6, a, colour)],
                                -pbar, -qbar,
                            ])
                            counts["balanced_reduced_tensor"] += 1

                        # On the dependent branch Q=-rho*P, so a support
                        # mismatch in any of the nine coordinates closes;
                        # on the independent branch injectivity already does.
                        for residue in (4, 5, 6):
                            for colour in V.COLORS:
                                pcell = index[V.cell(u, residue, a, colour)]
                                qcell = index[V.cell(v, residue, b, colour)]
                                clauses.append([-pbar, -qbar, -pcell, qcell])
                                clauses.append([-pbar, -qbar, pcell, -qcell])
                                counts["dependent_support_equality"] += 2

                # Exactly one non-target projection zero: the other slice
                # puts the corresponding triple in ker(Phi), hence it is zero.
                for pbar in Pbar:
                    for qcell in Qother:
                        clauses.append([-pbar, -qcell] + Qbar)
                        counts["one_zero_projection"] += 1
                for qbar in Qbar:
                    for pcell in Pother:
                        clauses.append([-qbar, -pcell] + Pbar)
                        counts["one_zero_projection"] += 1

                # If Q is target-only at vertex 7 and zero elsewhere, the
                # target slice gives Phi(P)=unit*E222.  Injectivity and the
                # known companion (c,e,e2) force P6 target-supported.
                for colour in (0, 1):
                    clauses.append([
                        -q72, -z, -index[V.cell(u, 6, a, colour)]
                    ] + Qbar + Qother)
                    clauses.append([
                        -p72, -z, -index[V.cell(v, 6, b, colour)]
                    ] + Pbar + Pother)
                    counts["target_only_companion"] += 2

                # If either complete boundary star is zero, the six-site
                # coefficient is z*H_R(2222), an ordinary pure-fibre unit.
                clauses.append([-z] + Q)
                clauses.append([-z] + P)
                counts["zero_star_pure_lift"] += 2

    # The z-optional four-star lemma, transported through every non-target
    # tripod-minor chart by 6414f4d.  These are the exact eight-cell
    # antecedents emitted by its checker.
    for row in F.clause_audit():
        clauses.append([-index[tuple(cell)] for cell in row["support_clause"]])
        counts["z_optional_four_star_6414f4d"] += 1

    # The target-aligned e/c normal forms of 6fd0227.  A clause is active
    # only when both alignment cells and the direct boundary cell are absent.
    for row in A.clause_audit():
        clause = [index[tuple(cell)] for cell in row["alignment_holes"]]
        clause.append(index[tuple(row["direct_edge_hole"])])
        clause.extend(-index[tuple(cell)]
                      for cell in row["localized_witnesses"])
        clauses.append(clause)
        counts["target_alignment_6fd0227"] += 1

    # The all-characteristic full-output double quotient 12d3678.
    for row in BQ.clause_audit():
        clause = [index[tuple(cell)]
                  for cell in row["boundary_star_holes"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["quotient_witnesses"])
        clauses.append(clause)
        counts["boundary_star_quotient_12d3678"] += 1

    # Global one-site target incidence 3cc432c.  Each auxiliary is exactly
    # equivalent to one active target-only incident column.
    for packet in I.incidence_packets():
        alternatives = []
        for row in packet["alternatives"]:
            target = index[tuple(row["target_cell"])]
            off_target = [index[tuple(cell)]
                          for cell in row["off_target_cells"]]
            good = new_variable()
            alternatives.append(good)
            clauses.append([-good, target])
            for cell in off_target:
                clauses.append([-good, -cell])
            clauses.append([good, -target] + off_target)
            counts["one_site_incidence_equivalence_3cc432c"] += (
                2 + len(off_target)
            )
        clauses.append(alternatives)
        counts["one_site_incidence_cover_3cc432c"] += 1

    # Exact coefficient-empty incidence face 5a7d1c5, transported through
    # every site/colour automorphism of the O4 downset universe.
    for row in OC.transported_clause_audit():
        clause = [index[tuple(cell)] for cell in row["positive_cells"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["negative_cells"])
        clauses.append(clause)
        counts["incidence_frontier_odd_circuit_5a7d1c5"] += 1

    # Exact characteristic-zero iterated Laurent closure fe6b2af of the
    # second 159-cell incidence face, including all O4 automorphism transports.
    for row in IL.transported_clause_audit():
        clause = [index[tuple(cell)] for cell in row["positive_cells"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["negative_cells"])
        clauses.append(clause)
        counts["second_incidence_iterated_laurent_fe6b2af"] += 1

    # Exact integral U^2 closure 9531bb8 of the third 159-cell face.
    for row in TS.transported_clause_audit():
        clause = [index[tuple(cell)] for cell in row["positive_cells"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["negative_cells"])
        clauses.append(clause)
        counts["third_incidence_saturation_9531bb8"] += 1

    # Exact odd-circuit U^3 closure 70d7405 of the fourth 159-cell face.
    for row in FO.transported_clause_audit():
        clause = [index[tuple(cell)] for cell in row["positive_cells"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["negative_cells"])
        clauses.append(clause)
        counts["fourth_incidence_odd_circuit_70d7405"] += 1

    # Exact two-face integral U^1 batch 7e50069 on the 158-cell layer.
    for row in B158.transported_clause_audit():
        clause = [index[tuple(cell)] for cell in row["positive_cells"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["negative_cells"])
        clauses.append(clause)
        counts["direct_158_batch_7e50069"] += 1

    # Exact characteristic-not-two U^2 collision 491be48 on the first
    # 158-cell face escaping the direct signed-Laurent layer.
    for row in SL158.transported_clause_audit():
        clause = [index[tuple(cell)] for cell in row["positive_cells"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["negative_cells"])
        clauses.append(clause)
        counts["second_layer_158_collision_491be48"] += 1

    # Exact integral direct U^1 closure c9bd78d of the next 158-cell face.
    for row in TF158.transported_clause_audit():
        clause = [index[tuple(cell)] for cell in row["positive_cells"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["negative_cells"])
        clauses.append(clause)
        counts["third_face_158_direct_unit_c9bd78d"] += 1

    # Exact integral U^2 selected by the quotient-character oracle 8a32870.
    for row in QG158.transported_clause_audit():
        clause = [index[tuple(cell)] for cell in row["positive_cells"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["negative_cells"])
        clauses.append(clause)
        counts["quotient_character_unit_158_8a32870"] += 1

    # Checked direct character units and repair chart from batch 6733ddf.
    for row in CB158.transported_clause_audit():
        clause = [index[tuple(cell)] for cell in row["positive_cells"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["negative_cells"])
        clauses.append(clause)
        counts["character_graph_batch2_158_6733ddf"] += 1

    # Exact length-two character holonomy and repair chart 8179888.
    for row in CC158.transported_clause_audit():
        clause = [index[tuple(cell)] for cell in row["positive_cells"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["negative_cells"])
        clauses.append(clause)
        counts["character_collision_158_8179888"] += 1

    # Exact three-row initial odd-character batch 9b81480.
    for row in IO158.transported_clause_audit():
        clause = [index[tuple(cell)] for cell in row["positive_cells"]]
        clause.extend(-index[tuple(cell)]
                      for cell in row["negative_cells"])
        clauses.append(clause)
        counts["initial_odd_dependency_158_9b81480"] += 1

    # Support-faithful form of D1_harm:
    # (x02_01*x13_01 is live) iff (x01_00*x23_11 is live).
    left = (index[V.cell(0, 2, 0, 1)], index[V.cell(1, 3, 0, 1)])
    right = (index[V.cell(0, 1, 0, 0)], index[V.cell(2, 3, 1, 1)])
    clauses.extend([
        [-left[0], -left[1], right[0]],
        [-left[0], -left[1], right[1]],
        [-right[0], -right[1], left[0]],
        [-right[0], -right[1], left[1]],
    ])
    counts["D1_harm_support_equivalence"] += 4

    require(len(cells) == 193 and next_variable == 225759
            and len(clauses) == 1347198,
            "the specialized O4 downset CNF dimensions changed")
    require(counts == Counter({
        "live_matching_auxiliaries": 225432,
        "zero_fibres": 8094,
        "pure_fibres": 6,
        "balanced_reduced_tensor": 96,
        "dependent_support_equality": 864,
        "one_zero_projection": 432,
        "target_only_companion": 48,
        "zero_star_pure_lift": 24,
        "z_optional_four_star_6414f4d": 576,
        "target_alignment_6fd0227": 384,
        "boundary_star_quotient_12d3678": 8,
        "one_site_incidence_equivalence_3cc432c": 496,
        "one_site_incidence_cover_3cc432c": 24,
        "incidence_frontier_odd_circuit_5a7d1c5": 4,
        "second_incidence_iterated_laurent_fe6b2af": 8,
        "third_incidence_saturation_9531bb8": 8,
        "fourth_incidence_odd_circuit_70d7405": 4,
        "direct_158_batch_7e50069": 16,
        "second_layer_158_collision_491be48": 8,
        "third_face_158_direct_unit_c9bd78d": 8,
        "quotient_character_unit_158_8a32870": 8,
        "character_graph_batch2_158_6733ddf": 40,
        "character_collision_158_8179888": 16,
        "initial_odd_dependency_158_9b81480": 8,
        "D1_harm_support_equivalence": 4,
    }), "the O4 structural clause-family census changed")
    return cells, index, clauses, next_variable, counts


def solve_minimum_omissions(cells, clauses, top_variable):
    # Exact cardinality search.  The first satisfiable bound is the maximum
    # support size under the currently proved structural atoms.
    verdicts = []
    first = None
    model = None
    bounds = (
        (EXPECTED_MINIMUM_OMISSIONS - 1, EXPECTED_MINIMUM_OMISSIONS)
        if EXPECTED_MINIMUM_OMISSIONS is not None
        else range(0, len(cells) + 1)
    )
    for bound in bounds:
        cardinality = CardEnc.atmost(
            lits=[-(position + 1) for position in range(len(cells))],
            bound=bound, top_id=top_variable, encoding=EncType.seqcounter,
        )
        solver = Solver(name="cadical195",
                        bootstrap_with=clauses + cardinality.clauses)
        satisfiable = solver.solve()
        verdicts.append([bound, satisfiable])
        if satisfiable:
            first = bound
            model = {literal for literal in solver.get_model()
                     if 0 < literal <= len(cells)}
            solver.delete()
            break
        solver.delete()
    require(first is not None, "the O4 omission search exceeded its bound")
    missing = tuple(cells[position] for position in range(len(cells))
                    if position + 1 not in model)
    require(len(missing) == first,
            "the cardinality model did not attain its first bound")
    return first, missing, verdicts


def build_ledger(write_frontier=False):
    cells, _index, clauses, top_variable, counts = build_cnf()
    cnf_digest = D.content_hash(clauses)
    minimum, missing, verdicts = solve_minimum_omissions(
        cells, clauses, top_variable
    )
    support = set(cells) - set(missing)
    shadow = C.support_shadow_audit(support)
    records = C.coefficient_generators(support)
    generator_digest = D.content_hash(records)
    residue_cells = {
        V.cell(u, v, i, j)
        for u, v in itertools.combinations(V.RESIDUE, 2)
        for i, j in itertools.product(V.COLORS, repeat=2)
    }
    live_minor_charts = 0
    for row in F.minor_orbit_audit():
        i, j, k = row["indices"]
        ai, aj = row["A_indices"]
        witnesses = {
            V.cell(4, 6, i, k), V.cell(4, 7, i, 2),
            V.cell(5, 7, j, 2), V.cell(4, 5, ai, aj),
        }
        live_minor_charts += int(witnesses <= support)
    boundary_quotient_counts = {}
    for residue in V.RESIDUE:
        boundary_quotient_counts[str(residue)] = sum(
            V.cell(boundary, residue, boundary_colour, residue_colour)
            in support
            for boundary in range(4)
            for boundary_colour in (
                (0, 1) if boundary < 2 else V.COLORS
            )
            for residue_colour in (0, 1)
        )
    active_arcs = []
    for packet in I.incidence_packets():
        for row in packet["alternatives"]:
            target = tuple(row["target_cell"])
            off_target = {tuple(cell) for cell in row["off_target_cells"]}
            if target in support and not (off_target & support):
                active_arcs.append([
                    packet["target_colour"], packet["center"],
                    row["neighbour"],
                ])
    require(all(any(arc[0] == colour and arc[1] == center
                    for arc in active_arcs)
                for center in V.SITES for colour in V.COLORS),
            "the frontier lost a required target-incidence arc")
    mutual_arcs = []
    active_arc_set = {tuple(arc) for arc in active_arcs}
    for colour, source, target in sorted(active_arc_set):
        if source < target and (colour, target, source) in active_arc_set:
            mutual_arcs.append([colour, source, target])
    ledger = {
        "pinned_six_site_closure_sha256": source_digest,
        "pinned_target_alignment_sha256": alignment_source_digest,
        "pinned_boundary_star_sha256": boundary_star_source_digest,
        "pinned_one_site_incidence_sha256": incidence_source_digest,
        "pinned_incidence_frontier_odd_circuit_sha256":
            odd_circuit_source_digest,
        "pinned_second_incidence_iterated_laurent_sha256":
            iterated_laurent_source_digest,
        "pinned_third_incidence_saturation_sha256":
            third_saturation_source_digest,
        "pinned_fourth_incidence_odd_circuit_sha256":
            fourth_odd_source_digest,
        "pinned_158_direct_batch_sha256": batch_158_source_digest,
        "pinned_158_second_layer_sha256": second_layer_158_source_digest,
        "pinned_158_third_face_sha256": third_face_158_source_digest,
        "pinned_158_quotient_graph_sha256": quotient_graph_158_source_digest,
        "pinned_158_character_batch2_sha256": character_batch2_158_source_digest,
        "pinned_158_character_collision_sha256":
            character_collision_158_source_digest,
        "pinned_158_initial_odd_sha256": initial_odd_158_source_digest,
        "allowed_cells": len(cells),
        "cnf_variables": top_variable,
        "cnf_clauses": len(clauses),
        "cnf_sha256": cnf_digest,
        "clause_families": dict(sorted(counts.items())),
        "cardinality_verdicts": verdicts,
        "minimum_additional_omissions": minimum,
        "maximum_surviving_support": len(support),
        "frontier_missing_cells": [list(cell) for cell in missing],
        "frontier_shadow": shadow,
        "frontier_generators": len(records),
        "frontier_generator_sha256": generator_digest,
        "frontier_structure": {
            "additional_residue_holes": [
                list(cell) for cell in missing if cell in residue_cells
            ],
            "live_checked_tripod_minor_charts": live_minor_charts,
            "c_non_target_witnesses": [
                i for i in (0, 1) if V.cell(4, 7, i, 2) in support
            ],
            "e_non_target_witnesses": [
                i for i in (0, 1) if V.cell(5, 7, i, 2) in support
            ],
            "boundary_non_target_cells_by_residue":
                boundary_quotient_counts,
            "active_target_incidence_arcs": active_arcs,
            "mutual_target_incidence_edges": mutual_arcs,
            "invariant_axes": [
                "checked injective-Phi chart count",
                "c/e target-line alignment flags",
                "boundary-star non-target quotient support counts",
            ],
        },
        "status": "exact maximum-support CEGAR frontier; coefficient-open",
    }
    if write_frontier:
        print("frontier support cells:", sorted(support))
    return ledger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-frontier", action="store_true")
    args = parser.parse_args()
    started = monotonic()
    ledger = build_ledger(args.show_frontier)
    if EXPECTED_CNF_SHA256 != "TO_BE_FROZEN":
        require(ledger["cnf_sha256"] == EXPECTED_CNF_SHA256,
                "the O4 downset CNF changed")
    if EXPECTED_MINIMUM_OMISSIONS is not None:
        require(ledger["minimum_additional_omissions"]
                == EXPECTED_MINIMUM_OMISSIONS,
                "the O4 minimum-omission frontier changed")
    if EXPECTED_FRONTIER_MISSING is not None:
        require(ledger["frontier_missing_cells"]
                == EXPECTED_FRONTIER_MISSING,
                "the O4 canonical frontier support changed")
    if EXPECTED_FRONTIER_GENERATOR_SHA256 is not None:
        require(ledger["frontier_generator_sha256"]
                == EXPECTED_FRONTIER_GENERATOR_SHA256,
                "the O4 frontier coefficient input changed")
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256: %s" % digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the O4 downset CEGAR ledger changed")
        print("ledger sha256 (frozen): %s" % digest)
    print("minimum omissions / maximum support: %d / %d"
          % (ledger["minimum_additional_omissions"],
             ledger["maximum_surviving_support"]))
    print("frontier generators:", ledger["frontier_generators"])
    print("elapsed: %.2fs" % (monotonic() - started))


if __name__ == "__main__":
    main()
