#!/usr/bin/env python3
"""Close the 1I+4R+1Z generic-kernel potential frontier below rank 55.

Sites are 0 (invertible), 1,...,4 (nonzero rank one), and 5 (zero).
Write E for the zero-sum graph on sites 1,...,5.  A rank-one site
isolated in E is a fixed root, so rank(dPsi)<=42.  Up to permutation of
the four rank-one sites, exactly fourteen E-orbits have no such isolate.

Three orbits have a coordinate three-shore and inherit rank bounds 49 or
51.  The Z-centred K1,4 orbit has a direct support-slice bound 50, and the
complete graph has a fixed root at site 0.  Exact Singular syzygies close
the remaining nine normalized support families at rank at most 49.  Thus
no 1I+4R+1Z chart reaches differential rank 55; L0, L1, and R2 are unused.

Research evidence only.  Singular is the sole external dependency.
Python checks remain live under -O and -I -S.
"""

from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
from runpy import run_path
from shutil import which
import subprocess


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
PREDECESSOR = run_path(str(
    HERE / "verify_level_two_one_invertible_five_rank_one_potential_reduction.py"
))
SHORE = run_path(str(
    HERE / "verify_level_two_three_invertible_coordinate_shore_rank_drop.py"
))

SITES = tuple(range(6))
RANK_ONE = (1, 2, 3, 4)
COLOURS = (0, 1)
EDGES = tuple(combinations(SITES, 2))
POTENTIAL_EDGES = tuple(combinations(range(1, 6), 2))
WORDS = tuple(product(COLOURS, repeat=6))

# name, (nu_1,...,nu_5), free-05 admissible, root-spoke profile,
# closure method, asserted upper bound, scalar mode.
CHARTS = (
    ("matching2", (-2, -1, 1, 2, 0), True, "four", "syzygy", 35, "variable"),
    ("rstar3", (-2, -2, -2, 2, -1), True, "star", "syzygy", 34, "variable"),
    ("rpath2_z", (-2, -2, -1, 2, 1), True, "three", "path shore", 49, None),
    ("matching2_z", (-2, -1, 1, 2, -2), False, "four", "path shore", 49, None),
    ("redge_z2", (-2, -2, -1, 1, 2), True, "four", "syzygy", 46, "variable"),
    ("rstar3_z", (-2, -2, -2, 2, -2), False, "star", "syzygy", 30, "variable"),
    ("rtriangle_z", (-2, 0, 0, 0, 2), True, "triangle", "constant shore", 51, None),
    ("rk22", (-2, -2, 2, 2, -1), True, "k22", "syzygy", 35, "variable"),
    ("matching2_z2", (-2, 0, 0, 2, 0), False, "four", "syzygy", 46, "variable"),
    ("zstar4", (-2, -2, -2, -2, 2), True, "four", "support slices", 50, None),
    ("rk4", (0, 0, 0, 0, -2), True, "one", "syzygy", 36, "variable"),
    ("k23_zsmall", (-2, -2, -2, 2, 2), False, "star", "syzygy", 49, "unit"),
    ("k23_zlarge", (-2, -2, 2, 2, -2), False, "k22", "syzygy", 43, "variable"),
    ("k5", (0, 0, 0, 0, 0), False, "one", "fixed root", 42, None),
)

CHART = {entry[0]: entry for entry in CHARTS}
CAS_NAMES = tuple(
    name for name, _nu, _free05, _profile, method, _bound, _mode in CHARTS
    if method == "syzygy"
)

ROOT_PROFILES = {
    # Four generic projective lines modulo PGL2; t is their cross-ratio.
    "four": {
        1: ("1", "0"), 2: ("0", "1"),
        3: ("1", "1"), 4: ("1", "t"),
    },
    # A three-leaf orthogonal pencil and its opposite line.
    "star": {
        1: ("1", "0"), 2: ("1", "0"),
        3: ("1", "0"), 4: ("0", "1"),
    },
    # One two-leaf pencil, its opposite, and one independent line.
    "three": {
        1: ("1", "0"), 2: ("1", "0"),
        3: ("1", "1"), 4: ("0", "1"),
    },
    # A zero-potential triangle is one common isotropic line.
    "triangle": {
        1: ("0", "1"), 2: ("1", "0"),
        3: ("1", "0"), 4: ("1", "0"),
    },
    "k22": {
        1: ("1", "0"), 2: ("1", "0"),
        3: ("0", "1"), 4: ("0", "1"),
    },
    "one": {
        1: ("1", "0"), 2: ("1", "0"),
        3: ("1", "0"), 4: ("1", "0"),
    },
}

EXPECTED_PAYLOADS = {
    # (number of syz generators, bad cells in DQ, independent specialized
    # syzygies, exact rank of the displayed integral specialization).
    "matching2": (28, 0, 25, 35),
    "rstar3": (31, 0, 26, 34),
    "redge_z2": (86, 0, 14, 46),
    "rstar3_z": (31, 0, 30, 30),
    "rk22": (30, 0, 25, 35),
    "matching2_z2": (18, 0, 14, 46),
    "rk4": (29, 0, 24, 34),
    "k23_zsmall": (15, 0, 11, 49),
    "k23_zlarge": (42, 0, 17, 43),
}


def zero_sum_edges(values):
    return frozenset(
        edge for edge in POTENTIAL_EDGES
        if values[edge[0] - 1] + values[edge[1] - 1] == 0
    )


def canonical_edges(edges):
    images = []
    for target in permutations(RANK_ONE):
        relabel = dict(zip(RANK_ONE, target))
        relabel[5] = 5
        images.append(tuple(sorted(
            tuple(sorted((relabel[left], relabel[right])))
            for left, right in edges
        )))
    return min(images)


def audit_zero_sum_graph_split():
    representatives = {}
    for chart in CHARTS:
        name, values, free05, _profile, _method, _bound, _mode = chart
        edges = zero_sum_edges(values)
        require(all(any(vertex in edge for edge in edges)
                    for vertex in RANK_ONE),
                ("chart acquired an isolated rank-one site", name, edges))
        key = canonical_edges(edges)
        require(key not in representatives,
                ("two displayed charts entered one orbit", name, key))
        representatives[key] = name
        admissible = all(value != values[4] for value in values[:4])
        require(admissible == free05,
                ("05-admissibility flag changed", name, admissible, free05))

    # Zero, one signed magnitude, and two signed magnitudes realize every
    # opposition/zero component possible on five vertices.  The finite
    # census audits the resulting orbit list exactly.
    census = set()
    labelled = 0
    for values in product((-2, -1, 0, 1, 2), repeat=5):
        edges = zero_sum_edges(values)
        if not all(any(vertex in edge for edge in edges)
                   for vertex in RANK_ONE):
            continue
        labelled += 1
        census.add(canonical_edges(edges))
    require(census == set(representatives),
            ("four-rank-one zero-sum orbit census changed",
             len(census), set(representatives) - census,
             census - set(representatives)))
    require(len(census) == 14,
            ("zero-sum orbit count changed", len(census)))
    return labelled, representatives


def audit_generic_kernel_reduction():
    pair_checks, root_images = PREDECESSOR["audit_rank_one_pair_pencil"]()
    require(pair_checks > 0 and len(root_images) == 5,
            "the predecessor pair-pencil audit changed")

    fixed_cases, fixed_bound, calibration = PREDECESSOR[
        "audit_fixed_root_bound"
    ]()
    require(fixed_bound == calibration == 42,
            ("the fixed-root bound changed", fixed_bound, calibration))
    require("isolated rank-one potential" in fixed_cases,
            "the isolated-potential fixed-root case disappeared")

    # M_05 is arbitrary precisely when nu_0=-nu_5.  At an invertible root,
    # nu_0+nu_i cannot vanish for a nonzero rank-one X_i.  Hence the special
    # 05 chart exists iff no rank-one potential equals nu_5.  Its arbitrary
    # family contains the M_05=0 chart as a specialization.
    admissible = {
        name for name, _values, free05, *_tail in CHARTS if free05
    }
    require(admissible == {
        "matching2", "rstar3", "rpath2_z", "redge_z2",
        "rtriangle_z", "rk22", "zstar4", "rk4",
    }, ("free-05 chart list changed", admissible))
    return pair_checks, fixed_bound, admissible


def audit_coordinate_shores():
    path_identities, categories = SHORE["audit_path_factorization"]()
    constant_identities = SHORE["audit_constant_cross_factorization"]()
    require(path_identities == 64 and categories == {
        "all_cross": 6, "34": 3, "35": 3, "45": 3,
    }, "the coordinate path-shore theorem changed")
    require(constant_identities == 64,
            "the constant-cross triangle theorem changed")

    shores = {
        # Exceptional paths are 1-4-2 and 1-4-5 respectively.
        "rpath2_z": ((1, 4, 2), 49),
        "matching2_z": ((1, 4, 5), 49),
        # Sites 2,3,4 share one zero-potential isotropic pencil.  Their
        # cross spokes are constant in normalized coordinates.
        "rtriangle_z": ((2, 3, 4), 51),
    }
    require(all(CHART[name][5] == bound
                for name, (_shore, bound) in shores.items()),
            ("coordinate-shore chart bound changed", shores))
    return shores


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    head = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((head, partner),) + tail)
    return tuple(answer)


MATCHINGS4 = {
    vertices: perfect_matchings(vertices)
    for vertices in combinations(SITES, 4)
}


def zstar_support_value(edge, colours):
    left, right = edge
    a, b = colours
    if 5 in edge:
        return True
    if left == 0:
        return b == 0
    return a == b == 0


def zstar_cofactor_may_live(edge, word):
    complement = tuple(site for site in SITES if site not in edge)
    return any(all(
        zstar_support_value(pair, (word[pair[0]], word[pair[1]]))
        for pair in matching
    ) for matching in MATCHINGS4[complement])


def audit_zstar_support_slices():
    cells = tuple(
        (left, right, a, b)
        for left, right in EDGES
        for a, b in product(COLOURS, repeat=2)
    )
    high_cells = set()
    row_counts = {weight: 0 for weight in range(5)}
    for word in WORDS:
        weight = sum(word[site] for site in RANK_ONE)
        row_counts[weight] += 1
        active = {
            cell for cell in cells
            if (word[cell[0]], word[cell[1]]) == cell[2:]
            and zstar_cofactor_may_live(cell[:2], word)
        }
        if weight == 4:
            require(not active,
                    ("the four-one zstar slice became live", word, active))
        if weight == 3:
            require(all(
                left in RANK_ONE and right in RANK_ONE and a == b == 1
                for left, right, a, b in active
            ), ("a three-one zstar row escaped the six RR11 columns",
                word, active))
            high_cells.update(active)

    expected_high = {
        (left, right, 1, 1)
        for left, right in combinations(RANK_ONE, 2)
    }
    require(high_cells == expected_high,
            ("the zstar high-slice column set changed", high_cells))
    require(row_counts == {0: 4, 1: 16, 2: 24, 3: 16, 4: 4},
            ("the zstar row-weight census changed", row_counts))

    # The weight <=2 rows contribute at most 44.  All weight-three rows
    # use only six global columns, and every weight-four row is zero.
    bound = row_counts[0] + row_counts[1] + row_counts[2] + len(high_cells)
    require(bound == 50, ("the zstar support bound changed", bound))
    return row_counts, len(high_cells), bound


def free_edges(chart):
    name, values, free05, _profile, _method, _bound, _mode = chart
    answer = set(zero_sum_edges(values))
    if free05:
        answer.add((0, 5))
    require(all(edge in EDGES for edge in answer),
            ("a free edge left K6", name, answer))
    return frozenset(answer)


def symbolic_packet(chart):
    name, _values, _free05, profile, method, _bound, scalar_mode = chart
    require(method == "syzygy", ("non-CAS chart entered CAS", name))
    roots = ROOT_PROFILES[profile]
    free = free_edges(chart)
    variables = ["t"] if profile == "four" else []
    packet = {}
    for left, right in EDGES:
        for a, b in product(COLOURS, repeat=2):
            edge = (left, right)
            if left == 0 and right < 5:
                value = roots[right][a] if b == 0 else "0"
            elif edge in free:
                value = f"x{left}{right}{a}{b}"
                variables.append(value)
            elif right == 5:
                value = "0"
            elif scalar_mode == "unit":
                value = "1" if (a, b) == (0, 0) else "0"
            else:
                value = f"s{left}{right}" if (a, b) == (0, 0) else "0"
                if value != "0":
                    variables.append(value)
            packet[left, right, a, b] = value
    variables = tuple(dict.fromkeys(variables))
    require(variables and len(variables) == len(set(variables)),
            ("bad symbolic variable list", name, variables))
    return packet, variables


def symbolic_cofactor(packet, word, left, right):
    complement = tuple(site for site in SITES if site not in (left, right))
    a, b, c, d = complement
    matchings = (
        ((a, b), (c, d)),
        ((a, c), (b, d)),
        ((a, d), (b, c)),
    )
    terms = []
    for matching in matchings:
        factors = tuple(
            packet[u, v, word[u], word[v]] for u, v in matching
        )
        if "0" not in factors:
            terms.append("*".join(factors))
    return "(" + "+".join(terms) + ")" if terms else "0"


def symbolic_differential_entries(packet):
    entries = []
    for word in WORDS:
        for left, right in EDGES:
            cofactor = symbolic_cofactor(packet, word, left, right)
            for a, b in product(COLOURS, repeat=2):
                entries.append(
                    cofactor if (word[left], word[right]) == (a, b)
                    else "0"
                )
    require(len(entries) == 64 * 60,
            "the symbolic differential size changed")
    return tuple(entries)


def singular_program():
    lines = []
    metadata = {}
    for name in CAS_NAMES:
        chart = CHART[name]
        packet, variables = symbolic_packet(chart)
        entries = symbolic_differential_entries(packet)
        metadata[name] = (len(variables), sum(entry != "0" for entry in entries))
        suffix = name
        lines.extend((
            f"ring {suffix}_ring=0,({','.join(variables)}),dp;",
            f"matrix D_{suffix}[64][60]={','.join(entries)};",
            f"module relations_{suffix}=syz(D_{suffix});",
            f"matrix Q_{suffix}=relations_{suffix};",
            f"matrix Z_{suffix}=D_{suffix}*Q_{suffix};",
            f"int bad_{suffix}=0;",
            f"int i_{suffix}; int j_{suffix};",
            f"for (i_{suffix}=1;i_{suffix}<=nrows(Z_{suffix});i_{suffix}++) {{",
            f"  for (j_{suffix}=1;j_{suffix}<=ncols(Z_{suffix});j_{suffix}++) {{",
            f"    if (Z_{suffix}[i_{suffix},j_{suffix}]!=0) {{ bad_{suffix}++; }}",
            "  }",
            "}",
            f"matrix E_{suffix}=Q_{suffix};",
            f"matrix DE_{suffix}=D_{suffix};",
        ))
        for index, variable in enumerate(variables):
            value = index + 2
            lines.append(
                f"E_{suffix}=subst(E_{suffix},{variable},{value});"
            )
            lines.append(
                f"DE_{suffix}=subst(DE_{suffix},{variable},{value});"
            )
        lines.extend((
            f'print("BEGIN_{suffix}");',
            f"print(ncols(Q_{suffix}));",
            f"print(bad_{suffix});",
            f"print(rank(E_{suffix}));",
            f"print(rank(DE_{suffix}));",
            f'print("END_{suffix}");',
        ))
    lines.extend(("exit;", ""))
    return "\n".join(lines), metadata


def audit_polynomial_syzygies(executable, program):
    try:
        completed = subprocess.run(
            (executable, "-q"),
            input=program,
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("Singular 1I+4R+1Z audit timed out") from error
    require(completed.returncode == 0,
            ("Singular 1I+4R+1Z audit failed", completed.stderr))
    lines = tuple(line.strip() for line in completed.stdout.splitlines())
    payloads = {}
    for name in CAS_NAMES:
        begin = f"BEGIN_{name}"
        end = f"END_{name}"
        require(lines.count(begin) == lines.count(end) == 1,
                ("Singular chart markers changed", name, lines))
        payload = tuple(int(line) for line in lines[
            lines.index(begin) + 1:lines.index(end)
        ] if line)
        require(payload == EXPECTED_PAYLOADS[name],
                ("Singular chart payload changed", name, payload,
                 EXPECTED_PAYLOADS[name]))
        kernel_rank = payload[2]
        asserted_bound = CHART[name][5]
        require(60 - kernel_rank <= asserted_bound < 55,
                ("polynomial kernel no longer proves chart bound",
                 name, kernel_rank, asserted_bound))
        payloads[name] = payload
    return payloads


def audit_complete_graph_fixed_root():
    values = CHART["k5"][1]
    require(values == (0, 0, 0, 0, 0),
            "the complete potential chart stopped being all-zero")
    require(not CHART["k5"][2],
            "the complete chart unexpectedly admitted a free 05 block")

    # Four nonzero pairwise J-orthogonal b-lines share one isotropic line.
    # Thus all four root spokes M_0i share one left factor.  M_05=0 shares
    # it trivially, so root 0 is fixed and the predecessor bound is 42.
    triples, formula_checks = PREDECESSOR[
        "audit_complete_orthogonal_pencil"
    ]()
    require(triples > 0 and formula_checks > 0,
            "the complete orthogonal-pencil audit changed")
    require(CHART["k5"][5] == 42,
            "the complete-graph fixed-root bound changed")
    return triples, formula_checks, 42


def audit_frontier_map(payloads, shores, zstar, complete):
    frontier = {}
    for name, _values, _free05, _profile, method, bound, _mode in CHARTS:
        if method == "syzygy":
            require(name in payloads,
                    ("syzygy chart missing payload", name))
        elif method == "path shore" or method == "constant shore":
            require(name in shores and shores[name][1] == bound,
                    ("shore chart missing bound", name, shores))
        elif method == "support slices":
            require(name == "zstar4" and zstar[2] == bound,
                    ("support-slice chart changed", name, zstar))
        elif method == "fixed root":
            require(name == "k5" and complete[2] == bound,
                    ("complete fixed-root chart changed", name, complete))
        else:
            raise RuntimeError(("unknown closure method", name, method))
        require(bound < 55, ("a chart reached rank 55", name, bound))
        frontier[name] = (method, bound)
    require(len(frontier) == 14 and max(bound for _method, bound in frontier.values()) == 51,
            ("the final frontier map changed", frontier))
    return frontier


def main():
    graphs = audit_zero_sum_graph_split()
    kernel = audit_generic_kernel_reduction()
    shores = audit_coordinate_shores()
    zstar = audit_zstar_support_slices()
    complete = audit_complete_graph_fixed_root()

    program, metadata = singular_program()
    digest = sha256(program.encode()).hexdigest()
    executable = which("Singular")
    require(executable is not None,
            "external dependency missing: Singular is not on PATH")
    version = subprocess.run(
        (executable, "--version"),
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )
    require(version.returncode == 0
            and "Singular" in version.stdout + version.stderr,
            "could not identify the Singular executable")
    payloads = audit_polynomial_syzygies(executable, program)
    frontier = audit_frontier_map(payloads, shores, zstar, complete)

    print("1I+4R+1Z potential/rank closure: all checks passed")
    print(f"  labelled/no-isolate graph census : {graphs[0]}/14 orbits")
    print(f"  fixed-root preliminary bound     : {kernel[1]}")
    print(f"  free-05 orbit count              : {len(kernel[2])}/14")
    print(f"  coordinate-shore charts         : {shores}")
    print(f"  zstar support bound              : {zstar}")
    print(f"  polynomial-syzygy charts        : {len(payloads)}")
    print(f"  CAS variables/support cells     : {metadata}")
    print(f"  exact syzygy payloads           : {payloads}")
    print(f"  complete-graph bound            : {complete[2]}")
    print(f"  final frontier                  : {frontier}")
    print(f"  Singular program SHA-256        : {digest}")
    print("  theorem                         : rank dPsi <= 51 on every chart")
    print("  L0/L1/R2 use                    : none")


if __name__ == "__main__":
    main()
