#!/usr/bin/env python3
"""Close the 1I+5R K2,3 antipodal-pencil residue at rank at most 51.

After independent local binary changes, every K2,3 residual packet has the
normal form

    M01=M02=M12=E00,
    M03=M04=M05=E10,
    M34=M35=M45=E00,

with the six blocks M_ij, i in {1,2}, j in {3,4,5}, arbitrary.  Over the
rational function field in their 24 entries, exact Singular syzygies give
nine independent differential-kernel directions.  Hence rank(dPsi)<=51
identically, including every specialization.  An integral specialization
has exact rank 51.

Research evidence only.  The Python driver is standard-library; Singular
is the sole external dependency.  Checks stay live under -O and -I -S.
"""

from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
from runpy import run_path
from shutil import which
import subprocess


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = Path(__file__).resolve().parent
REDUCTION = run_path(str(
    HERE / "verify_level_two_one_invertible_five_rank_one_potential_reduction.py"
))
CORE = run_path(str(
    HERE / "verify_level_two_three_invertible_l0_obstruction.py"
))

SITES = tuple(range(6))
COLOURS = (0, 1)
EDGES = tuple(combinations(SITES, 2))
WORDS = tuple(product(COLOURS, repeat=6))
FREE_EDGES = tuple(
    (left, right) for left in (1, 2) for right in (3, 4, 5)
)
VARIABLES = tuple(
    f"x{left}{right}{a}{b}"
    for left, right in FREE_EDGES
    for a, b in product(COLOURS, repeat=2)
)
E00 = ((1, 0), (0, 0))
E10 = ((0, 0), (1, 0))
ZERO = ((0, 0), (0, 0))


def audit_covariant_normal_form():
    normal_forms, r2 = REDUCTION["audit_remaining_connected_normal_forms"]()
    require(normal_forms["K23"] == {
        "potential shores": (2, 3),
        "free blocks": 6,
        "within-shore blocks": "fixed nonzero rank one",
        "0-spokes": "constant on each pencil shore",
    }, ("the predecessor K23 normal form changed", normal_forms["K23"]))
    require(len(r2) == 6, "the predecessor K23 R2 frontier changed")

    b_a = (1, 1)
    b_b = (1, -1)
    require(REDUCTION["pairing"](b_a, b_b) == 0,
            "the K23 pencil lines stopped being orthogonal")
    require(REDUCTION["pairing"](b_a, b_a) != 0
            and REDUCTION["pairing"](b_b, b_b) != 0,
            "a K23 pencil line became isotropic")

    fixed = {
        (0, 1): E00, (0, 2): E00, (1, 2): E00,
        (0, 3): E10, (0, 4): E10, (0, 5): E10,
        (3, 4): E00, (3, 5): E00, (4, 5): E00,
    }
    require(set(fixed) | set(FREE_EDGES) == set(EDGES),
            "the normalized K23 edge partition changed")
    require(len(VARIABLES) == 24 and len(set(VARIABLES)) == 24,
            "the normalized K23 variable count changed")
    return fixed, r2


def symbolic_packet(fixed):
    packet = {}
    for left, right in EDGES:
        for a, b in product(COLOURS, repeat=2):
            if (left, right) in FREE_EDGES:
                value = f"x{left}{right}{a}{b}"
            else:
                value = str(fixed[left, right][a][b])
            packet[left, right, a, b] = value
    return packet


def symbolic_cofactor(packet, word, left, right):
    complement = tuple(
        site for site in SITES if site not in (left, right)
    )
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
    nonzero = 0
    for word in WORDS:
        for left, right in EDGES:
            cofactor = symbolic_cofactor(packet, word, left, right)
            for a, b in product(COLOURS, repeat=2):
                entry = (
                    cofactor if (word[left], word[right]) == (a, b)
                    else "0"
                )
                entries.append(entry)
                nonzero += entry != "0"
    require(len(entries) == 64 * 60,
            "the symbolic differential entry count changed")
    require(nonzero == 512,
            ("the symbolic differential support changed", nonzero))
    return tuple(entries), nonzero


def singular_program(entries):
    substitutions = "".join(
        f"E=subst(E,{name},{index + 2});"
        f"DE=subst(DE,{name},{index + 2});"
        for index, name in enumerate(VARIABLES)
    )
    return "\n".join((
        f"ring k23_ring=0,({','.join(VARIABLES)}),dp;",
        f"matrix D[64][60]={','.join(entries)};",
        "module columns=D;",
        "module relations=syz(columns);",
        "matrix Q=relations;",
        "matrix Z=D*Q;",
        "int bad=0;",
        "int i; int j;",
        "for (i=1;i<=nrows(Z);i++) {",
        "  for (j=1;j<=ncols(Z);j++) {",
        "    if (Z[i,j]!=0) { bad=bad+1; }",
        "  }",
        "}",
        "matrix E=Q;",
        "matrix DE=D;",
        substitutions,
        'print("BEGIN_K23");',
        "print(ncols(Q));",
        "print(bad);",
        "print(rank(E));",
        "print(rank(DE));",
        'print("END_K23");',
        "exit;",
        "",
    ))


def audit_symbolic_syzygies(executable, program):
    try:
        completed = subprocess.run(
            (executable, "-q"),
            input=program,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError("Singular K23 syzygy audit timed out") from error
    require(completed.returncode == 0,
            ("Singular K23 audit failed", completed.stderr))
    lines = tuple(line.strip() for line in completed.stdout.splitlines())
    require(lines.count("BEGIN_K23") == lines.count("END_K23") == 1,
            ("Singular K23 markers changed", lines))
    payload = tuple(
        line
        for line in lines[
            lines.index("BEGIN_K23") + 1:lines.index("END_K23")
        ]
        if line
    )
    # syz returns eleven module generators.  Their exact polynomial product
    # with D is zero.  At x_ijab=2,...,25 their constant specialization has
    # rank nine, while D has rank 51.  Thus the function-field kernel has at
    # least nine independent directions and the bound is sharp.
    require(payload == ("11", "0", "9", "51"),
            ("the exact K23 syzygy payload changed", payload))
    return payload


def integral_calibration_packet(fixed):
    blocks = dict(fixed)
    for left, right in FREE_EDGES:
        blocks[left, right] = tuple(
            tuple(
                2 + (
                    17 * left + 31 * right + 7 * a + 11 * b
                    + 3 * left * right
                ) % 19
                for b in COLOURS
            )
            for a in COLOURS
        )
    packet = {
        (left, right, a, b): blocks[left, right][a][b]
        for left, right in EDGES
        for a, b in product(COLOURS, repeat=2)
    }
    return packet, blocks


def audit_sharp_rank_calibration(fixed):
    packet, blocks = integral_calibration_packet(fixed)
    derivative = CORE["differential_matrix"](packet)
    ranks = (
        CORE["rational_rank"](derivative),
        CORE["modular_rank"](derivative, 101),
        CORE["modular_rank"](derivative, 32_003),
        CORE["modular_rank"](derivative, 1_000_003),
    )
    require(ranks == (51, 51, 51, 51),
            ("the sharp K23 calibration rank changed", ranks))
    require(all(
        blocks[edge] == fixed[edge] for edge in fixed
    ), "a fixed normalized K23 block changed in calibration")
    require(all(
        any(blocks[edge][a][b]
            for a, b in product(COLOURS, repeat=2))
        for edge in FREE_EDGES
    ), "a free K23 calibration block vanished")
    return ranks, blocks


def main():
    fixed, r2 = audit_covariant_normal_form()
    packet = symbolic_packet(fixed)
    entries, support = symbolic_differential_entries(packet)
    program = singular_program(entries)
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
    syzygies = audit_symbolic_syzygies(executable, program)
    ranks, _blocks = audit_sharp_rank_calibration(fixed)

    print("one-invertible K23 antipodal-pencil rank closure: all checks passed")
    print(f"  normalized fixed/free edges : {len(fixed)}/{len(FREE_EDGES)}")
    print(f"  arbitrary free entries      : {len(VARIABLES)}")
    print(f"  symbolic differential cells : {support}/512")
    print(f"  syzygy payload              : {syzygies}")
    print(f"  sharp exact ranks           : {ranks}")
    print(f"  predecessor R2 roots        : {len(r2)}/6")
    print(f"  Singular program SHA-256    : {digest}")
    print("  theorem                     : rank dPsi <= 51 on the full K23 residue")


if __name__ == "__main__":
    main()
