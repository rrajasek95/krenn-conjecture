#!/usr/bin/env python3
"""Certify the Koszul-corrected Ward counterguard on the P5 dual prefix.

This is an exact characteristic-zero analyzer.  It adds the dense z9 chart,
corrects the constant site-7 shear successively along z25,s,t,r3 so that it
is tangent to L,F1,F2,G, and tests whether the resulting derivation preserves
the already certified M30-principal dual-number mixed ideal.
"""

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


NAK = load_module(
    "n8_p5_nakayama_for_koszul_ward",
    "verify_n8_p5_schur_generic_L_nakayama_prefix.py",
)
G = NAK.G
F2 = NAK.F2
REES = NAK.REES

EXPECTED_LEDGER_SHA256 = (
    "c8cc428530534cd69916fb173f20a5fafe28ce9d1cc3f0b81e9e5bb15ed3c03a"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add(target, source, scale=QQ(1)):
    REES.add(target, source, scale)


def multiply(left, right):
    return REES.multiply(left, right)


def variable(variable):
    return {(variable,): QQ(1)}


def multiply_many(sources):
    answer = {(): QQ(1)}
    for source in sources:
        answer = multiply(answer, source)
    return answer


def derivation(source, images):
    answer = {}
    for monomial, coefficient in source.items():
        for position, source_variable in enumerate(monomial):
            image = images.get(source_variable)
            if not image:
                continue
            rest = monomial[:position] + monomial[position + 1:]
            add(answer, multiply({rest: coefficient}, image))
    return answer


def polynomial_digest(source):
    return REES.polynomial_digest(source)


def corrected_field(base, graph, relations, inverse_z11, inverse_z9):
    layout = base["layout"]
    a = layout["a"]
    ell, first, second, grow = relations
    b = graph["b_variable"]
    q = graph["inverse_b"]
    first_bend = base["first_bend"]
    second_bend = base["second_bend"]
    third_bend = graph["third_bend"]

    images = {
        a[46]: variable(b),
        a[54]: {
            (a[52],): QQ(1),
            (a[53],): QQ(1),
        },
        # Add (z11*b/z9)*d/dz25, represented on z9*w9=1.
        a[25]: multiply_many((
            variable(a[11]), variable(b), variable(inverse_z9)
        )),
    }
    ell_image = derivation(ell, images)

    first_before = derivation(first, images)
    images[first_bend] = {
        monomial + (inverse_z11,): -coefficient
        for monomial, coefficient in first_before.items()
    }
    first_image = derivation(first, images)

    second_before = derivation(second, images)
    images[second_bend] = {
        tuple(sorted(monomial + (inverse_z11, q))): -coefficient
        for monomial, coefficient in second_before.items()
    }
    second_image = derivation(second, images)

    grow_before = derivation(grow, images)
    # dG/dr3=-1, so adding theta(G)*d/dr3 kills theta(G).
    images[third_bend] = grow_before
    grow_image = derivation(grow, images)
    return images, {
        "L": ell_image,
        "F1": first_image,
        "F2": second_image,
        "G": grow_image,
    }


def singular_test(
    base, graph, relations, rows, pure_windows, epsilon, depth,
    images, center_images, inverse_z11, inverse_z16, inverse_z41,
    inverse_u, inverse_z9,
):
    layout = base["layout"]
    a = layout["a"]
    b = graph["b_variable"]
    q = graph["inverse_b"]
    names = [f"x{index}" for index in range(inverse_z9 + 1)]
    for parameter, chart_variable in a.items():
        names[chart_variable] = f"z{parameter}"
    names[base["first_bend"]] = "s"
    names[base["second_bend"]] = "t"
    names[graph["third_bend"]] = "r3"
    names[b] = "b"
    names[q] = "q"
    names[epsilon] = "e"
    names[inverse_z11] = "w"
    names[inverse_z16] = "p16"
    names[inverse_z41] = "p41"
    names[inverse_u] = "pu"
    names[inverse_z9] = "v9"

    row_images = [derivation(source, images) for source in rows]
    pure_images = [
        (colour, start, derivation(source, images))
        for colour, start, source in pure_windows
    ]
    active_sources = [
        *relations, *rows, *row_images,
        *(source for _colour, _start, source in pure_windows),
        *(source for _colour, _start, source in pure_images),
        *center_images.values(),
    ]
    active = set().union(*(
        {item for monomial in source for item in monomial}
        for source in active_sources
    ))
    special = {
        0, epsilon, graph["third_bend"], base["second_bend"],
        base["first_bend"], q, inverse_z11, inverse_z16,
        inverse_z41, inverse_u, inverse_z9, b,
    }
    ring_order = [
        "e", "r3", "t", "s", "v9", "pu", "q", "w",
        "p16", "p41", "b",
    ] + [names[index] for index in sorted(active - special)]
    require(len(set(ring_order)) == len(ring_order),
            "Koszul-Ward Singular names collided")
    encode = REES.AMBIENT.singular_polynomial
    ell, first, second, grow = relations
    lines = [f"ring rr=0,({','.join(ring_order)}),dp;"]
    lines.extend((
        f"poly ell={encode(ell, names)};",
        f"poly first={encode(first, names)};",
        f"poly second={encode(second, names)};",
        f"poly grow={encode(grow, names)};",
        "poly locb=b*q-1;",
        "poly loc9=z9*v9-1;",
        "poly loc11=z11*w-1;",
        "poly loc16=z16*p16-1;",
        "poly loc41=z41*p41-1;",
        "poly locu=(z26+b-z44)*pu-1;",
        f"poly selected={encode(rows[29], names)};",
        f"ideal prefix=ell,first,second,grow,locb,loc9,loc11,"
        f"loc16,loc41,locu,e{depth},selected;",
        "ideal gp=std(prefix);",
        '"UNIT",(reduce(1,gp)==0);',
    ))
    for label, source in center_images.items():
        lines.append(f"poly d{label}={encode(source, names)};")
        lines.append(
            f'"CENTER","{label}",size(reduce(d{label},gp)),'
            f'(reduce(d{label},gp)==0);'
        )
    for row, source in enumerate(row_images, 1):
        if not rows[row - 1]:
            continue
        lines.append(f"poly dm{row}={encode(source, names)};")
        lines.append(
            f'"ROW",{row},size(reduce(dm{row},gp)),'
            f'(reduce(dm{row},gp)==0);'
        )
    for colour, start, source in pure_images:
        lines.append(f"poly dh{colour}_{start}={encode(source, names)};")
        lines.append(
            f'"PURE",{colour},{start},size(reduce(dh{colour}_{start},gp)),'
            f'(reduce(dh{colour}_{start},gp)==0);'
        )
    lines.append("quit;")
    completed = subprocess.run(
        ["/usr/local/bin/Singular", "-q"],
        input="\n".join(lines), text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=300, check=False,
    )
    print(completed.stdout)
    require(completed.returncode == 0,
            "Koszul-Ward prefix Singular reduction failed")
    require("UNIT 0" in completed.stdout,
            "Koszul-Ward prefix ideal became unit")
    centers = {}
    row_flags = {}
    row_sizes = {}
    pure_flags = {}
    pure_sizes = {}
    for line in completed.stdout.splitlines():
        fields = line.split()
        if not fields:
            continue
        if fields[0] == "CENTER":
            centers[fields[1]] = (int(fields[2]), fields[3] == "1")
        elif fields[0] == "ROW":
            row = int(fields[1])
            row_sizes[row] = int(fields[2])
            row_flags[row] = fields[3] == "1"
        elif fields[0] == "PURE":
            key = int(fields[1]), int(fields[2])
            pure_sizes[key] = int(fields[3])
            pure_flags[key] = fields[4] == "1"
    return {
        "centers": centers,
        "row_flags": row_flags,
        "row_sizes": row_sizes,
        "pure_flags": pure_flags,
        "pure_sizes": pure_sizes,
        "row_image_terms": [len(source) for source in row_images],
        "pure_image_terms": {
            f"H{colour}_{start}": len(source)
            for colour, start, source in pure_images
        },
        "stdout_sha256": sha256(completed.stdout.encode()).hexdigest(),
    }


def audit():
    base = F2.audit(return_data=True)
    depth = 2
    graph = G.source_graph(base, maximum_order=5 + depth)
    epsilon = graph["inverse_b"] + 1
    inverse_z11 = epsilon + 1
    inverse_z16 = epsilon + 2
    inverse_z41 = epsilon + 3
    inverse_u = epsilon + 4
    inverse_z9 = epsilon + 5
    relations = NAK.center_relations(base, graph)
    rows = NAK.truncated_rows(graph, epsilon, depth)
    _pure_coefficients, pure_windows = NAK.pure_prefixes(
        base, graph, epsilon
    )
    images, center_images = corrected_field(
        base, graph, relations, inverse_z11, inverse_z9
    )
    result = singular_test(
        base, graph, relations, rows, pure_windows, epsilon, depth,
        images, center_images, inverse_z11, inverse_z16, inverse_z41,
        inverse_u, inverse_z9,
    )
    require(set(result["centers"]) == {"L", "F1", "F2", "G"},
            "Koszul-Ward center output incomplete")
    require(all(zero for _size, zero in result["centers"].values()),
            "corrected Ward field is not tangent to the four centers")

    failures = [
        row for row, zero in result["row_flags"].items() if not zero
    ]
    pure_failures = [
        key for key, zero in result["pure_flags"].items() if not zero
    ]
    require(failures == [30, 33],
            "Koszul-Ward mixed derivative failure set changed")
    require({row: result["row_sizes"][row] for row in failures}
            == {30: 83, 33: 61},
            "Koszul-Ward mixed derivative remainder sizes changed")
    require(not pure_failures,
            "a pure prefix derivative escaped the selected ideal")
    ledger = {
        "chart": "generic L/F1/F2/G with z9 additionally inverted",
        "field": (
            "delta+(z11*b/z9)d_z25, then unique d_s,d_t,d_r3 "
            "corrections tangent to L,F1,F2,G"
        ),
        "monic_derivatives": {
            "dF1/ds": "z11",
            "dF2/dt": "z11*b",
            "dG/dr3": "-1",
        },
        "center_derivatives": {
            label: {"remainder_terms": size, "zero": zero}
            for label, (size, zero) in result["centers"].items()
        },
        "dual_prefix": f"mod epsilon^{depth}",
        "mixed_derivative_failures": failures,
        "mixed_derivative_remainder_sizes": {
            str(row): result["row_sizes"][row] for row in failures
        },
        "selected_M30_derivative_zero": result["row_flags"].get(30),
        "pure_derivative_failures": [list(key) for key in pure_failures],
        "pure_derivative_remainder_sizes": {
            f"H{colour}_{start}": result["pure_sizes"][colour, start]
            for colour, start in pure_failures
        },
        "mixed_derivative_term_counts": result["row_image_terms"],
        "pure_derivative_term_counts": result["pure_image_terms"],
        "singular_output_sha256": result["stdout_sha256"],
        "scope_guard": (
            "exact corrected-derivation test on the dual-number graph prefix; "
            "not a full-germ or all-order certificate"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "generic-L Koszul-Ward prefix ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()
