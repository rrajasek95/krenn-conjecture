#!/usr/bin/env python3
"""Test the M30/M33 S-pair in tau times the shifted P5 mixed ideal."""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
QQ = Fraction


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


R4 = load_module(
    "n8_p5_r4_for_r5_spair",
    "verify_n8_p5_generic_L_koszul_ward_r4.py",
)
WARD = R4.WARD
NAK = R4.NAK
G = R4.G
F2 = R4.F2
REES = R4.REES


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def polynomial(entries):
    answer = {}
    for monomial, coefficient in entries:
        WARD.add(answer, {tuple(sorted(monomial)): QQ(coefficient)})
    return answer


def shifted_rows(graph, epsilon):
    answer = []
    for row in range(39):
        value = dict(graph["compatibility_orders"][6][row])
        WARD.add(value, {
            tuple(sorted(monomial + (epsilon,))): coefficient
            for monomial, coefficient
            in graph["compatibility_orders"][7][row].items()
        })
        answer.append(value)
    return answer


def singular_test(base, graph, relations, rows, epsilon):
    layout = base["layout"]
    a = layout["a"]
    b = graph["b_variable"]
    q = graph["inverse_b"]
    inverse_z11 = epsilon + 1
    inverse_z16 = epsilon + 2
    inverse_z41 = epsilon + 3
    inverse_u = epsilon + 4
    variable_count = inverse_u + 1
    names = [f"x{index}" for index in range(variable_count)]
    for parameter, variable in a.items():
        names[variable] = f"z{parameter}"
    bend_names = ("r3", "r4", "r5")
    for name, variable in zip(bend_names, graph["bend_variables"]):
        names[variable] = name
    names[base["first_bend"]] = "s"
    names[base["second_bend"]] = "t"
    names[b] = "b"
    names[q] = "q"
    names[epsilon] = "e"
    names[inverse_z11] = "w"
    names[inverse_z16] = "p16"
    names[inverse_z41] = "p41"
    names[inverse_u] = "pu"

    u = polynomial((
        ((a[26],), 1), ((b,), 1), ((a[44],), -1)
    ))
    v = polynomial((((a[26],), 1), ((a[44],), -1)))
    s_minus = REES.multiply(v, rows[29])
    WARD.add(s_minus, REES.multiply(u, rows[32]), -1)
    s_plus = REES.multiply(v, rows[29])
    WARD.add(s_plus, REES.multiply(u, rows[32]))

    tau_rows = []
    tau_row_numbers = []
    for row_number, source in enumerate(rows, 1):
        if not source:
            continue
        tau_rows.append({
            tuple(sorted(monomial + (epsilon,))): coefficient
            for monomial, coefficient in source.items()
            if monomial.count(epsilon) == 0
        })
        tau_row_numbers.append(row_number)
    require(len(tau_rows) == 26,
            "shifted tau*I generator count changed")
    pair_offsets = [tau_row_numbers.index(row) + 1 for row in (30, 33)]

    sources = [*relations, *tau_rows, s_minus, s_plus]
    active = set().union(*(
        {variable for monomial in source for variable in monomial}
        for source in sources
    ))
    special = {
        epsilon, *graph["bend_variables"], base["first_bend"],
        base["second_bend"], inverse_u, q, inverse_z11,
        inverse_z16, inverse_z41, b,
    }
    ring_order = [
        "e", "r5", "r4", "r3", "t", "s", "pu", "q", "w",
        "p16", "p41", "b",
    ] + [names[index] for index in sorted(active - special)]
    require(len(set(ring_order)) == len(ring_order),
            "r5 S-pair Singular names collided")
    encode = REES.AMBIENT.singular_polynomial
    ell, first, second, grow = relations
    lines = [f"ring rr=0,({','.join(ring_order)}),dp;"]
    lines.extend((
        f"poly ell={encode(ell, names)};",
        f"poly first={encode(first, names)};",
        f"poly second={encode(second, names)};",
        f"poly grow={encode(grow, names)};",
        "poly locb=b*q-1;",
        "poly loc11=z11*w-1;",
        "poly loc16=z16*p16-1;",
        "poly loc41=z41*p41-1;",
        "poly locu=(z26+b-z44)*pu-1;",
        "poly e2=e^2;",
        "ideal TI=" + ",".join(encode(source, names) for source in tau_rows)
        + ";",
        "ideal recurrence=ell,first,second,grow,locb,loc11,loc16,"
        "loc41,locu,e2,TI;",
        "ideal gr=std(recurrence);",
        '"UNIT",(reduce(1,gr)==0);',
        f"poly sminus={encode(s_minus, names)};",
        f"poly splus={encode(s_plus, names)};",
        f"poly m30={encode(rows[29], names)};",
        f"poly m33={encode(rows[32], names)};",
        "poly W=s*z0*z30*z52+t*z0*z30+t*z0*z52+t*z30*z52+"
        "r3*z0+r3*z30+r3*z52+r4;",
        "poly C=(1/2)*z11*z16^2*z41;",
        "ideal center=ell,first,second,grow,locb,loc11,loc16,loc41,locu;",
        "ideal gcenter=std(center);",
        '"Q7W30",(reduce(subst(m30,e,0)-C*(z26+b-z44)*W,'
        'gcenter)==0);',
        '"Q7W33",(reduce(subst(m33,e,0)-C*(z26-z44)*W,'
        'gcenter)==0);',
        '"SMINUS",size(reduce(sminus,gr)),(reduce(sminus,gr)==0);',
        '"SPLUS",size(reduce(splus,gr)),(reduce(splus,gr)==0);',
        "ideal pair=ell,first,second,grow,locb,loc11,loc16,loc41,"
        f"locu,e2,TI[{pair_offsets[0]}],TI[{pair_offsets[1]}];",
        "ideal gpair=std(pair);",
        '"PAIR",size(reduce(sminus,gpair)),(reduce(sminus,gpair)==0);',
        "ideal single=ell,first,second,grow,locb,loc11,loc16,loc41,"
        f"locu,e2,TI[{pair_offsets[0]}];",
        "ideal gsingle=std(single);",
        '"SINGLE",size(reduce(sminus,gsingle)),'
        '(reduce(sminus,gsingle)==0);',
        '"EW",(reduce(e*W,gsingle)==0),(reduce(W,gsingle)==0);',
        "quit;",
    ))
    completed = subprocess.run(
        ["/usr/local/bin/Singular", "-q"], input="\n".join(lines),
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=300, check=False,
    )
    print(completed.stdout)
    require(completed.returncode == 0,
            "r5 shifted S-pair Singular reduction failed")
    parsed = {}
    for line in completed.stdout.splitlines():
        fields = line.split()
        if fields and fields[0] in (
            "UNIT", "Q7W30", "Q7W33", "SMINUS", "SPLUS", "PAIR",
            "SINGLE", "EW"
        ):
            parsed[fields[0]] = fields[1:]
    require(set(parsed) == {
        "UNIT", "Q7W30", "Q7W33", "SMINUS", "SPLUS", "PAIR",
        "SINGLE", "EW"
    },
            "r5 S-pair output incomplete")
    return {
        "ideal_is_unit": parsed["UNIT"][0] == "1",
        "minus_size": int(parsed["SMINUS"][0]),
        "minus_zero": parsed["SMINUS"][1] == "1",
        "plus_size": int(parsed["SPLUS"][0]),
        "plus_zero": parsed["SPLUS"][1] == "1",
        "pair_size": int(parsed["PAIR"][0]),
        "pair_zero": parsed["PAIR"][1] == "1",
        "single_size": int(parsed["SINGLE"][0]),
        "single_zero": parsed["SINGLE"][1] == "1",
        "q7_w30": parsed["Q7W30"][0] == "1",
        "q7_w33": parsed["Q7W33"][0] == "1",
        "epsilon_w_zero": parsed["EW"][0] == "1",
        "w_zero": parsed["EW"][1] == "1",
        "s_minus_terms": len(s_minus),
        "s_plus_terms": len(s_plus),
        "tau_I_generators": len(tau_rows),
        "tau_I_source_rows": tau_row_numbers,
        "pair_tau_I_source_rows": [30, 33],
        "single_tau_I_source_rows": [30],
        "stdout_sha256": sha256(completed.stdout.encode()).hexdigest(),
    }


def audit():
    base = F2.audit(return_data=True)
    graph = G.source_graph(base, maximum_order=8, additional_bends=2)
    epsilon = graph["inverse_b"] + 1
    relations = NAK.center_relations(base, graph)
    rows = shifted_rows(graph, epsilon)
    result = singular_test(base, graph, relations, rows, epsilon)
    ledger = {
        "chart": "generic L/F1/F2/G shifted Q7/Q8 dual prefix",
        "graph_terms": {
            "Q7": sum(map(len, graph["compatibility_orders"][6])),
            "Q8": sum(map(len, graph["compatibility_orders"][7])),
        },
        "relation_target": (
            "S=v*M30-u*M33 in epsilon*I modulo epsilon^2, "
            "u=z26+b-z44, v=z26-z44"
        ),
        "tau_I_generators": result["tau_I_generators"],
        "tau_I_source_rows": result["tau_I_source_rows"],
        "recurrence_ideal_is_unit": result["ideal_is_unit"],
        "minus_S": {
            "terms": result["s_minus_terms"],
            "remainder_size": result["minus_size"],
            "zero": result["minus_zero"],
        },
        "plus_S": {
            "terms": result["s_plus_terms"],
            "remainder_size": result["plus_size"],
            "zero": result["plus_zero"],
        },
        "pair_only_minus_S": {
            "tau_I_source_rows": result["pair_tau_I_source_rows"],
            "remainder_size": result["pair_size"],
            "zero": result["pair_zero"],
        },
        "M30_only_minus_S": {
            "tau_I_source_rows": result["single_tau_I_source_rows"],
            "remainder_size": result["single_size"],
            "zero": result["single_zero"],
        },
        "selected_special_fibre": {
            "W": (
                "s*z0*z30*z52+t*z0*z30+t*z0*z52+t*z30*z52+"
                "r3*z0+r3*z30+r3*z52+r4"
            ),
            "Q7_M30": "(1/2)*z11*z16^2*z41*u*W",
            "Q7_M33": "(1/2)*z11*z16^2*z41*v*W",
            "epsilon_W_in_single_ideal": result["epsilon_w_zero"],
            "W_in_unsaturated_single_ideal": result["w_zero"],
        },
        "singular_output_sha256": result["stdout_sha256"],
        "scope_guard": (
            "exact shifted dual S-pair/first-colon test; full complete-local "
            "Nakayama still requires the stable special-fibre calculation"
        ),
    }
    require(not result["ideal_is_unit"],
            "recurrence ideal became the unit ideal")
    require(result["minus_zero"] and result["minus_size"] == 0,
            "minus S-pair no longer reduces to zero")
    require(result["pair_zero"] and result["pair_size"] == 0,
            "minus S-pair no longer lies in the two-row shifted ideal")
    require(result["single_zero"] and result["single_size"] == 0,
            "minus S-pair no longer lies in epsilon*M30")
    require(result["q7_w30"] and result["q7_w33"],
            "Q7 selected special-fibre factorization changed")
    require(result["epsilon_w_zero"] and not result["w_zero"],
            "selected epsilon-colon witness changed")
    require(not result["plus_zero"] and result["plus_size"] == 80,
            "plus-sign counterguard changed")
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
