#!/usr/bin/env python3
"""Emit the orbit-85 extended-ring Nullstellensatz proof as an arithmetic DAG."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ENCODER = ROOT / "computations/verify_eight_site_diagonal_obstruction.py"
CNF = ROOT / "computations/certificates/n8_diagonal/orbits/n8k4_85.cnf"
DRAT = ROOT / "computations/certificates/n8_diagonal/orbits/n8k4_85.drat"
DRAT_TRIM = (ROOT / "computations/unaudited-hygiene-h1-2026-08-15/tools/"
             "drat-trim/drat-trim")
OUTPUT = Path(__file__).with_name("certificate_dag.json")


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def load_encoder():
    spec = importlib.util.spec_from_file_location("n8diag_certified", ENCODER)
    require(spec is not None and spec.loader is not None, "cannot load encoder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def key_json(key):
    return [key_json(value) if isinstance(value, tuple) else value for value in key]


def sorted_clause(clause):
    return tuple(sorted(clause, key=lambda literal: (abs(literal), literal)))


def even_submasks(mask: int):
    submask = mask
    while True:
        if submask.bit_count() % 2 == 0:
            yield submask
        if submask == 0:
            break
        submask = (submask - 1) & mask


def main() -> None:
    module = load_encoder()
    case, orbit_size = module.orbit_reps(8)[85]
    encoder = module.Enc(8, case, k=4).build()
    require(encoder.dimacs().encode("ascii") == CNF.read_bytes(),
            "orbit-85 CNF does not rebuild byte-for-byte")

    p_vars = sorted((variable, key) for key, variable in encoder.vmap.items()
                    if key[0] == "p")
    g_vars = sorted((variable, key) for key, variable in encoder.vmap.items()
                    if key[0] == "g")
    a2_rows = [(cid, tag) for cid, tag in enumerate(encoder.tags, 1)
               if tag[0] == "A2"]
    fr_rows = [(cid, tag) for cid, tag in enumerate(encoder.tags, 1)
               if tag[0] == "FR"]
    c0_rows = [(cid, tag) for cid, tag in enumerate(encoder.tags, 1)
               if tag[0] == "C0"]

    antecedents = []
    antecedent_ids = set()

    def add_antecedent(identifier, kind, **payload):
        require(identifier not in antecedent_ids, f"duplicate antecedent {identifier}")
        antecedent_ids.add(identifier)
        antecedents.append({"id": identifier, "kind": kind, **payload})

    amp_by_parts = {}
    for _cid, tag in a2_rows:
        parts = tuple(tag[1])
        identifier = "amp:" + ":".join(map(str, parts))
        amp_by_parts[parts] = identifier
        add_antecedent(identifier, "mixed_diagonal_amplitude",
                       colour_class_masks=list(parts), degree=4,
                       tail_first_possible_order=2)

    for variable in range(1, encoder.nv + 1):
        add_antecedent(f"bool:{variable}", "boolean_axiom",
                       variable=variable, variable_key=key_json(encoder.vname[variable]),
                       degree=2)

    for variable, key in p_vars:
        size = key[2].bit_count()
        add_antecedent(f"pz:{variable}", "selector_zero_link",
                       variable=variable, p_key=key_json(key), hafnian_degree=size // 2,
                       degree=size // 2 + 1)
        add_antecedent(f"pr:{variable}", "selector_guarded_inverse",
                       variable=variable, p_key=key_json(key), hafnian_degree=size // 2,
                       degree=size // 2 + 2)

    for variable, key in g_vars:
        c, mask, w, u = key[1:]
        first = encoder.vmap[("p", c, (1 << w) | (1 << u))]
        second = encoder.vmap[("p", c, mask & ~((1 << w) | (1 << u)))]
        add_antecedent(f"gd:{variable}", "laplace_witness_definition",
                       variable=variable, g_key=key_json(key),
                       factor_selectors=[first, second], degree=2)

    for cid, tag in fr_rows:
        add_antecedent(f"fr:{cid}", "inside_free_product_zero",
                       clause_id=cid, tag=key_json(tag), degree=3)

    # Exact complements of the seven outside-free positions.
    full = (1 << 8) - 1
    for cid, tag in c0_rows:
        _, c, y = tag
        star_mask = (1 << 7) | (1 << y)
        residual = full & ~star_mask
        split_rows = []
        d, e = [colour for colour in range(3) if colour != c]
        for split in even_submasks(residual):
            parts = [0, 0, 0]
            parts[c] = star_mask
            parts[d] = split
            parts[e] = residual & ~split
            amp_id = amp_by_parts[tuple(parts)]
            split_rows.append({
                "residual_product_masks": [split, residual & ~split],
                "source_amplitude": amp_id,
                "witness": f"r:C0:{c}:{y}:{len(split_rows)}",
            })
        require(len(split_rows) == 32, "outside-free split count is not 32")
        add_antecedent(f"comp:{c}:{y}", "outside_free_complement_localizer",
                       clause_id=cid, colour=c, site=y, split_rows=split_rows,
                       degree=4)

    # Open equations use the already allocated p-hafnian inverse variable.
    for cid, tag in enumerate(encoder.tags, 1):
        family = tag[0]
        if family not in ("A1", "Cnz", "Ch"):
            continue
        literal = encoder.cls[cid - 1][0]
        require(literal > 0, f"{family} is not a positive unit clause")
        add_antecedent(f"open:{family}:{tag[1]}", "unguarded_open_localizer",
                       clause_id=cid, family=family, colour=tag[1],
                       p_variable=literal,
                       degree=encoder.vname[literal][2].bit_count() // 2 + 1)

    require(len(antecedents) == 13670,
            f"antecedent ledger has {len(antecedents)} rows, expected 13670")

    def p_refs(variable):
        return [f"pz:{variable}", f"pr:{variable}"]

    def c0_source_refs(c, y):
        comp = next(row for row in antecedents if row["id"] == f"comp:{c}:{y}")
        return [comp["id"]] + [item["source_amplitude"]
                               for item in comp["split_rows"]]

    def compiler(cid):
        tag = encoder.tags[cid - 1]
        clause = encoder.cls[cid - 1]
        family = tag[0]
        refs = []
        schema = family
        degree = len(clause)

        if family == "A0":
            refs = [f"pz:{clause[0]}"]
            degree = 1
        elif family in ("A1", "Cnz", "Ch"):
            variable = clause[0]
            refs = [f"pz:{variable}", f"open:{family}:{tag[1]}"]
            size_degree = encoder.vname[variable][2].bit_count() // 2
            degree = size_degree + 2
        elif family == "A2":
            refs = [amp_by_parts[tuple(tag[1])]]
            refs += [f"pr:{abs(literal)}" for literal in clause]
            degree = 2 * len(clause) + 4
        elif family == "A3g":
            g_variable = abs(clause[0])
            p_variable = abs(clause[1])
            refs = [f"gd:{g_variable}", f"bool:{p_variable}"]
            degree = 3
        elif family == "A3":
            p_h = abs(clause[0])
            refs = [f"pr:{p_h}"]
            for literal in clause[1:]:
                g_variable = abs(literal)
                refs.append(f"gd:{g_variable}")
                g_key = encoder.vname[g_variable]
                c, mask, w, u = g_key[1:]
                refs.append(f"pz:{encoder.vmap[('p', c, (1 << w) | (1 << u))]}")
                refs.append(f"pz:{encoder.vmap[('p', c, mask & ~((1 << w) | (1 << u)))]}")
            size = tag[2].bit_count()
            degree = (size - 1) + size // 2 + 2
        elif family == "C0":
            _, c, y = tag
            refs = [f"pr:{abs(clause[0])}"] + c0_source_refs(c, y)
            degree = 7
        elif family == "FR":
            refs = [f"fr:{cid}"] + [f"pr:{abs(literal)}" for literal in clause]
            degree = 2 * len(clause) + 3
        elif family == "XF":
            _, c, mask = tag
            variables = [abs(literal) for literal in clause]
            refs = p_refs(variables[0]) + p_refs(variables[1])
            refs.append(f"open:Cnz:{c}")
            free = {c} | set(case[c])
            yc = c
            for y in module.bits(mask):
                if y != yc:
                    require(y not in free, "XF residual site unexpectedly lies in F_c")
                    refs += c0_source_refs(c, y)
            degree = (mask.bit_count() + 1) // 2 + 4
        else:
            raise RuntimeError(f"unsupported clause family {family}")

        require(all(ref in antecedent_ids for ref in refs),
                f"compiler {cid}/{family} has missing antecedent")
        return {
            "schema": schema,
            "tag": key_json(tag),
            "antecedents": refs,
            "arithmetic_degree_bound": degree,
        }

    # Produce a core LRAT and reconstruct its resolution chains.
    with tempfile.TemporaryDirectory(prefix="n8diag85-compose-") as temporary:
        lrat = Path(temporary) / "core.lrat"
        process = subprocess.run(
            [str(DRAT_TRIM), str(CNF), str(DRAT), "-U", "-L", str(lrat)],
            text=True, capture_output=True, timeout=30, check=False)
        transcript = process.stdout + process.stderr
        require(process.returncode == 0 and "s VERIFIED" in transcript,
                f"RUP-only replay failed:\n{transcript}")
        require("0 RAT lemmas in core" in transcript, "RAT lemma entered core")
        additions = []
        for line in lrat.read_text(encoding="ascii").splitlines():
            words = line.split()
            if not words or words[1] == "d":
                continue
            zero = words.index("0", 1)
            literals = tuple(map(int, words[1:zero]))
            hints = tuple(map(int, words[zero + 1:-1]))
            require(all(hint > 0 for hint in hints), "negative LRAT hint")
            additions.append((int(words[0]), literals, hints))

    core_inputs = sorted({
        hint for _, _, hints in additions for hint in hints
        if hint <= len(encoder.cls)
    })
    require(len(core_inputs) == 502, "core input count changed")

    nodes = []
    clause_node = {}
    node_degree = {}
    core_amplitude_refs = []
    for cid in core_inputs:
        comp = compiler(cid)
        node_id = f"c:{cid}"
        nodes.append({
            "id": node_id,
            "op": "compile_clause",
            "cnf_clause_id": cid,
            "clause": list(encoder.cls[cid - 1]),
            "compiler": comp,
        })
        clause_node[cid] = node_id
        node_degree[node_id] = comp["arithmetic_degree_bound"]
        core_amplitude_refs += [
            ref for ref in comp["antecedents"] if ref.startswith("amp:")]

    database = {cid: tuple(clause) for cid, clause in
                enumerate(encoder.cls, 1)}
    resolution_steps = weakening_steps = 0
    for added_id, target, hints in additions:
        assignment = {}
        reasons = []
        conflict_id = None
        for literal in target:
            assignment[abs(literal)] = literal < 0
        for hint in hints:
            clause = database[hint]
            unassigned = []
            satisfied = False
            for literal in clause:
                variable = abs(literal)
                if variable not in assignment:
                    unassigned.append(literal)
                elif assignment[variable] == (literal > 0):
                    satisfied = True
                    break
            require(not satisfied, f"satisfied LRAT hint {hint}")
            if not unassigned:
                conflict_id = hint
                break
            require(len(unassigned) == 1, f"nonunit LRAT hint {hint}")
            unit = unassigned[0]
            assignment[abs(unit)] = unit > 0
            reasons.append((unit, hint))
        require(conflict_id is not None, f"no conflict for lemma {added_id}")
        current = set(database[conflict_id])
        current_node = clause_node[conflict_id]
        for unit, reason_id in reversed(reasons):
            if -unit not in current:
                continue
            reason = set(database[reason_id])
            require(unit in reason, "unit missing from reason")
            left_without = current - {-unit}
            right_without = reason - {unit}
            left_factors = sorted_clause(right_without - left_without)
            right_factors = sorted_clause(left_without - right_without)
            result_clause = sorted_clause(left_without | right_without)
            resolution_steps += 1
            node_id = f"r:{resolution_steps}"
            right_node = clause_node[reason_id]
            nodes.append({
                "id": node_id,
                "op": "resolve_polynomials",
                "left": current_node,
                "right": right_node,
                "pivot_literal_in_right": unit,
                "left_falsity_factors": list(left_factors),
                "right_falsity_factors": list(right_factors),
                "result_clause": list(result_clause),
            })
            node_degree[node_id] = max(
                node_degree[current_node] + len(left_factors),
                node_degree[right_node] + len(right_factors))
            current = set(result_clause)
            current_node = node_id
        require(current.issubset(set(target)), f"bad RUP resolvent {added_id}")
        if current != set(target):
            added = sorted_clause(set(target) - current)
            weakening_steps += 1
            node_id = f"w:{weakening_steps}"
            nodes.append({
                "id": node_id,
                "op": "weaken_polynomial",
                "input": current_node,
                "added_falsity_factors": list(added),
                "result_clause": list(sorted_clause(target)),
            })
            node_degree[node_id] = node_degree[current_node] + len(added)
            current_node = node_id
        database[added_id] = target
        clause_node[added_id] = current_node

    root = clause_node[additions[-1][0]]
    require(database[additions[-1][0]] == (), "root is not empty clause")
    require((resolution_steps, weakening_steps) == (1652, 5),
            "resolution profile changed")

    unique_tail_amplitudes = sorted(set(core_amplitude_refs))
    def profile(amplitude_id):
        masks = map(int, amplitude_id.split(":")[1:])
        return tuple(sorted((mask.bit_count() for mask in masks), reverse=True))

    distinct_profiles = Counter(profile(item) for item in unique_tail_amplitudes)
    occurrence_profiles = Counter(profile(item) for item in core_amplitude_refs)
    tail2_terms = {(6, 2, 0): 90, (4, 4, 0): 72, (4, 2, 2): 30}
    require(set(distinct_profiles) == set(tail2_terms), "unexpected even profile")
    certificate = {
        "format": "n8diag-orbit85-extended-ns-dag-v1",
        "orbit": 85,
        "case": key_json(case),
        "case_orbit_size": orbit_size,
        "coefficient_ring": "Z",
        "antecedents": antecedents,
        "core_input_clause_ids": core_inputs,
        "proof_nodes": nodes,
        "root": root,
        "root_polynomial": "1",
        "stats": {
            "antecedent_equations": len(antecedents),
            "antecedent_variables": 6284,
            "antecedent_max_degree": 6,
            "antecedent_expanded_monomial_occurrences": 39949,
            "compiled_core_clauses": len(core_inputs),
            "resolution_nodes": resolution_steps,
            "weakening_nodes": weakening_steps,
            "dag_nodes": len(nodes),
            "resolution_primitive_mul_add_gates": 3 * resolution_steps,
            "weakening_primitive_mul_gates": weakening_steps,
            "max_arithmetic_degree_bound": max(node_degree.values()),
        },
        "tail_interface": {
            "substitution": "A_ij^(ab)=delta_(a,b)*d_ij^a+epsilon*T_ij^(ab)",
            "selectors_inverses_branch_witnesses": "epsilon-constant",
            "epsilon_order_1_coefficient": "0",
            "reason_order_1": (
                "every lifted amplitude leaf has three even colour classes; "
                "a matching cannot have exactly one cross-colour edge"
            ),
            "first_possible_order": 2,
            "distinct_amplitude_leaves_in_core_compilation": len(unique_tail_amplitudes),
            "amplitude_leaf_occurrences_in_core_compilation": len(core_amplitude_refs),
            "amplitude_leaf_ids": unique_tail_amplitudes,
            "distinct_leaf_profile_counts": {
                "+".join(map(str, key)): value
                for key, value in sorted(distinct_profiles.items())
            },
            "leaf_occurrence_profile_counts": {
                "+".join(map(str, key)): value
                for key, value in sorted(occurrence_profiles.items())
            },
            "Tail2_terms_per_profile": {
                "+".join(map(str, key)): value
                for key, value in sorted(tail2_terms.items())
            },
            "distinct_leaf_Tail2_monomial_occurrences": sum(
                count * tail2_terms[key] for key, count in distinct_profiles.items()),
            "weighted_leaf_Tail2_monomial_occurrences": sum(
                count * tail2_terms[key] for key, count in occurrence_profiles.items()),
            "order_2_coefficient_circuit": (
                "linearize this proof DAG: replace each mixed_diagonal_amplitude "
                "antecedent by Tail2(colour_class_masks), every other antecedent "
                "by 0, and retain all polynomial multipliers"
            ),
            "lifted_certificate_convention": "C(epsilon)=1+epsilon^2*C2+O(epsilon^3)",
            "tail_remainder_convention": "1-C(epsilon)=-epsilon^2*C2+O(epsilon^3)",
            "Tail2_formula": (
                "sum over perfect matchings M with exactly two cross-colour "
                "edges of product_(same ij in M)d_ij^(w_i) times "
                "product_(cross ij in M)T_ij^(w_i,w_j)"
            ),
        },
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "root": root,
        "stats": certificate["stats"],
        "tail_interface": {
            key: value for key, value in certificate["tail_interface"].items()
            if key not in ("amplitude_leaf_ids",)
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
