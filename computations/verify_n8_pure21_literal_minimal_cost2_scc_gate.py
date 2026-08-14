#!/usr/bin/env python3
"""Literal minimum/cost-two SCC and its first exact full-row cycle.

Scan all thirty cost-two packets over terminal rows R3 and R5 against the
three already constructed rows R0,R3,R5.  Eight packets return to R0: six
from R3 and two from R5.  With the minimum R0->R3/R5 edges, all three rows
form one literal SCC and there are eight inclusion-minimal two-edge cycles.

The first four R3 returns obey the old Laurent determinant cancellation.
The fifth, however, adjoins Z=s_0(0;1) and L=q12^(0,1) and factors
R3=X3*b*K and R0=(X3*q45+X*q35)*K with K=S0*c+Z*L.  Hence K=0 is a genuine
exact full-row cycle.  The normalized exhaustive replay exposes its first
new private row 001100:01; the checker deliberately stops the SCC exclusion
at this first exact cycle.
"""

import argparse
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


PARENT_PATH = Path(__file__).with_name(
    "verify_n8_pure21_private_tail_higher_cost_reset_gate.py"
)
SPEC = spec_from_file_location("higher_cost_parent", PARENT_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load parent audit")
H = module_from_spec(SPEC)
SPEC.loader.exec_module(H)
S = H.S
E = H.E
F = H.F
M = H.M
B = H.B


R0 = ((1, 0, 1, 2, 2, 2), 0, 0)
R3 = ((1, 0, 1, 2, 0, 0), 0, 0)
R5 = ((1, 1, 1, 1, 1, 2), 0, 1)
KNOWN_ROWS = {R0: "R0", R3: "R3", R5: "R5"}


def cost_two_literal_landings():
    answer = []
    for branch, paths in H.PATHS.items():
        H.install_branch(branch)
        base = {
            key: B.residual(key[1], key[2], key[0])
            for key in KNOWN_ROWS
        }
        for index, path in enumerate(paths):
            if len(path[-1]) != 2:
                continue
            H.install_branch(branch)
            H.install_additions(path)
            landed = []
            for key, name in KNOWN_ROWS.items():
                difference = B.subtract(
                    B.residual(key[1], key[2], key[0]), base[key]
                )
                if difference:
                    landed.append((name, difference))
            answer.append((branch, index, path, tuple(landed)))
    M.reset_tables()
    return tuple(answer)


LANDINGS = cost_two_literal_landings()
RETURN_INDICES = {3: (3, 15, 36, 48, 60, 66), 5: (22, 53)}


def audit_literal_landing_classification():
    require(len(LANDINGS) == 30, ("cost-two packet total changed", len(LANDINGS)))
    returns = tuple(
        entry for entry in LANDINGS
        if any(name == "R0" for name, _ in entry[3])
    )
    observed = {
        branch: tuple(index for found_branch, index, _, _ in returns
                      if found_branch == branch)
        for branch in (3, 5)
    }
    require(observed == RETURN_INDICES, ("literal return indices changed", observed))
    require(len(returns) == 8, ("literal return count changed", returns))

    fifth = next(entry for entry in returns if entry[0:2] == (3, 60))
    expected_fifth = (
        "PS", 3, 0, ((1, 2), (4, 5)),
        (("s", (0, 0, 1)), ("q", (1, 2, 0, 1))),
    )
    require(fifth[2] == expected_fifth, ("first exact-cycle packet changed", fifth))
    return returns


def audit_label_symmetry():
    site_markers = (
        ("P0",), ("S0",), ("P2",),
        ("S1", "X3"), ("X",), ("S2", "Y"),
    )
    require(len(set(site_markers)) == 6, ("site marker collision", site_markers))
    # With trivial site stabilizer and retained operation/fine tags, all eight
    # return packets remain separate labelled orbits.
    return {
        "site_stabilizer_order": 1,
        "literal_return_packet_orbits": 8,
        "operation_tags_retained": True,
    }


def strongly_connected_components(vertices, edges):
    reachable = {vertex: {vertex} for vertex in vertices}
    for source, target, _ in edges:
        reachable[source].add(target)
    changed = True
    while changed:
        changed = False
        for source in vertices:
            extension = set().union(*(reachable[target] for target in tuple(reachable[source])))
            new = extension - reachable[source]
            if new:
                reachable[source].update(new)
                changed = True
    component = tuple(sorted(
        vertex for vertex in vertices
        if all(vertex in reachable[other] and other in reachable[vertex]
               for other in vertices)
    ))
    return (component,)


def audit_scc_and_cycles():
    vertices = ("R0", "R3", "R5")
    edges = [
        ("R0", "R3", "X3-minimum-PS"),
        ("R0", "R5", "X5-minimum-PS"),
    ]
    for branch, indices in RETURN_INDICES.items():
        source = "R3" if branch == 3 else "R5"
        edges.extend((source, "R0", f"cost2-{branch}-{index}") for index in indices)
    components = strongly_connected_components(vertices, tuple(edges))
    require(components == (("R0", "R3", "R5"),),
            ("literal SCC changed", components))
    cycles = tuple(
        (("X3-minimum-PS" if branch == 3 else "X5-minimum-PS"),
         f"cost2-{branch}-{index}")
        for branch, indices in RETURN_INDICES.items() for index in indices
    )
    require(len(cycles) == 8, ("minimal cycle count changed", cycles))
    return {
        "components": [list(component) for component in components],
        "inclusion_minimal_directed_cycles": [list(cycle) for cycle in cycles],
        "cycle_count": len(cycles),
    }


def install_first_exact_cycle():
    S.install_symbolic_parent()
    B.FIRST[S.X3_KEY] = S.X3
    z = B.variable("Z")
    ell = B.variable("L")
    B.SECOND[(0, 0, 1)] = z
    B.Q_EDGE[(1, 2, 0, 1)] = ell
    return z, ell


def audit_exact_factorized_cycle():
    z, ell = install_first_exact_cycle()
    r3 = B.residual(0, 0, R3[0])
    r0 = B.residual(0, 0, R0[0])
    kappa = B.add(
        B.multiply(B.variable("S0"), B.variable("c")),
        B.multiply(z, ell),
    )
    expected_r3 = B.product_polynomials((S.X3, B.variable("b"), kappa))
    expected_r0 = B.multiply(
        B.add(
            B.multiply(S.X3, B.variable("q45")),
            B.multiply(E.X, B.variable("q35")),
        ),
        kappa,
    )
    require(r3 == expected_r3, ("factorized R3 changed", r3))
    require(r0 == expected_r0, ("factorized R0 changed", r0))
    # Kappa=0 is available with every inherited factor and both new cells
    # nonzero, e.g. normalized Z=-1,L=1.
    normalized = dict(M.P.NORMALIZATION)
    normalized.update({"X": 2, "X3": 1, "q35": 1, "q45": -2, "Z": -1, "L": 1})
    require(E.N.evaluate_at(kappa, normalized) == 0, "normalized cycle factor did not vanish")
    require(E.N.evaluate_at(r3, normalized) == 0, "normalized R3 cycle did not close")
    require(E.N.evaluate_at(r0, normalized) == 0, "normalized R0 cycle did not close")
    M.reset_tables()
    return {
        "repair_packet": "Z=s0(site0,colour1), L=q12^(0,1)",
        "repair_operation": "PS",
        "repair_fine": "63|70|12|45",
        "factor": "K=S0*c+Z*L",
        "rows": ["R3=X3*b*K", "R0=(X3*q45+X*q35)*K"],
        "normalized_solution": {"Z": -1, "L": 1},
    }


EXPECTED_INCREMENTAL = (
    ("001100", "01", 1, 1),
    ("001200", "01", 1, 1),
    ("001222", "01", -4, -4),
    ("101200", "00", -1, 0),
    ("101221", "10", -1, 0),
    ("110011", "10", -1, -1),
    ("112212", "20", -1, -1),
    ("120021", "10", -1, -1),
    ("120022", "00", -2, -2),
    ("122200", "20", -1, -1),
    ("201121", "11", 1, 1),
    ("201122", "01", 2, 2),
    ("201200", "02", 1, 1),
    ("201221", "11", 4, 4),
    ("201222", "01", 5, 5),
    ("201222", "02", -5, -5),
)


def audit_normalized_cycle_replay():
    S.install_normalized_parent()
    B.FIRST[S.X3_KEY] = B.constant(1)
    before = {key: B.residual(key[1], key[2], key[0]) for key in F.ROWS}
    B.SECOND[(0, 0, 1)] = B.constant(-1)
    B.Q_EDGE[(1, 2, 0, 1)] = B.constant(1)
    after = {key: B.residual(key[1], key[2], key[0]) for key in F.ROWS}
    ledger = tuple(
        ("".join(map(str, key[0])), f"{key[1]}{key[2]}",
         int(increment), int(M.P.evaluate(after[key])))
        for key in F.ROWS
        if (increment := M.P.evaluate(B.subtract(after[key], before[key])))
    )
    require(ledger == EXPECTED_INCREMENTAL, ("exact-cycle replay changed", ledger))
    require(M.P.evaluate(after[R0]) == M.P.evaluate(after[R3]) == 0,
            "the exact SCC rows did not remain closed")
    final_nonzero = sum(bool(M.P.evaluate(after[key])) for key in F.ROWS)
    require(final_nonzero == 44, ("exact-cycle full residual count moved", final_nonzero))
    M.reset_tables()
    return {
        "incremental_rows": len(ledger),
        "full_nonzero_rows": final_nonzero,
        "first_new_private_face": {
            "word_head": "001100:01",
            "operation": "PS",
            "fine": "60|73|12|45",
            "monomial": "P0*S1*L*b",
            "value": 1,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "landings", "symmetry", "scc", "factor", "replay"),
        default="all",
    )
    args = parser.parse_args()

    landings = symmetry = scc = factor = replay = None
    if args.mode in ("all", "landings"):
        landings = audit_literal_landing_classification()
    if args.mode in ("all", "symmetry"):
        symmetry = audit_label_symmetry()
    if args.mode in ("all", "scc"):
        scc = audit_scc_and_cycles()
    if args.mode in ("all", "factor"):
        factor = audit_exact_factorized_cycle()
    if args.mode in ("all", "replay"):
        replay = audit_normalized_cycle_replay()

    report = {
        "mode": args.mode,
        "cost2_packets_examined": len(LANDINGS),
        "literal_returns": None if landings is None else len(landings),
        "label_symmetry": symmetry,
        "scc": scc,
        "first_exact_full_row_cycle": factor,
        "exhaustive_replay": replay,
        "surviving_exact_scc_cycle": factor is not None,
        "scope": "first literal SCC; stop at first exact factorized cycle",
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 pure-21 literal minimum/cost2 SCC gate: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
