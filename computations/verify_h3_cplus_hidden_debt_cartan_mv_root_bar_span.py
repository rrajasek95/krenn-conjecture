#!/usr/bin/env python3
"""Audit the full-row span of Cartan/M_v/root-word bar corrections.

The raw generic-even cell would have to contribute the hidden debt

    H = (lower, Eq, ores) = (-E, 0, +E),
    E = 2 D_root tensor (B1+B4)/2.

This checker grants *more* than the physical inventory: an independent
pure-residue Cartan K_u=(0,0,u) and diagonal M_u=(u,u,0) for every one of
the 24 root-word/pure-label coordinates.  It also adjoins all endpoint
differences made by a representative root-pair/cross-cut sigma action.
The resulting span is exactly {(x,x,z)}.  Hence the lower-minus-Eq
covectors still separate H.  In particular, a sigma-paired bar between
already physical Cartan/M_v endpoints cannot supply the clean Eq-only
comparison hidden in this debt.
"""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_cplus_root_even_koszul_physical_dressing_gate.py":
        "9bd2c9f482dc3277d07bd96a4e2189034e766f97e7800d3864179a75e03cef17",
    "computations/verify_h3_cplus_root_even_labelled_ores_sigma_cartan_gate.py":
        "144d1fd64d8a733f3ec737edd301c540e66d545c9d72adf1abba5f7ed4764ce1",
    "computations/verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py":
        "3397fc0b7d773d97fb26e737eb490136c3062549951b07eca701ee46739ff2bb",
    "computations/verify_h3_gl3_normalized_bar_word_change_obstruction.py":
        "ed3c1baafd7d83819c1b6842857611b5b540c57ef95c8ca8a450de357312670a",
}
EXPECTED_LEDGER_SHA256 = (
    "18faa02b2b5fdab3862a91b62f117e010a12d89afdc1a4a7f15d1cd33bca6df1"
)

ROOTS = 4
PURE = 6
N = ROOTS * PURE
LOWER = slice(0, N)
EQ = slice(LOWER.stop, LOWER.stop + N)
ORES = slice(EQ.stop, EQ.stop + N)
ROWS = ORES.stop

D_ROOT = tuple(map(Q, (-1, 1, -1, 1)))
V = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
CHI = tuple(map(Q, (0, 1, -1, 0, 1, -1)))


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(scalar, vector):
    return tuple(Q(scalar) * Q(entry) for entry in vector)


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def tensor(left, right):
    return tuple(Q(a) * Q(b) for a in left for b in right)


def unit(width, index):
    return tuple(Q(int(position == index)) for position in range(width))


def vector(*, lower=(), eq=(), ores=()):
    answer = [Q(0)] * ROWS
    for section, values in ((LOWER, lower), (EQ, eq), (ORES, ores)):
        if values:
            require(len(values) == N, (section, len(values)))
            answer[section] = values
    return tuple(answer)


def rank(columns):
    if not columns:
        return 0
    height = len(columns[0])
    work = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(height):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right for left, right in
                         zip(work[row], work[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def permute_label_vector(values, root_action, pure_action):
    answer = [Q(0)] * N
    for root in range(ROOTS):
        for pure in range(PURE):
            source = root * PURE + pure
            target = root_action[root] * PURE + pure_action[pure]
            answer[target] += values[source]
    return tuple(answer)


def pin_inputs():
    for relative, expected in PINS.items():
        actual = digest(ROOT / relative)
        require(actual == expected, (relative, actual, expected))


def audit():
    pin_inputs()
    e = scale(2, tensor(D_ROOT, V))
    hidden = vector(lower=scale(-1, e), ores=e)
    require(sum(D_ROOT, Q(0)) == 0 and dot(CHI, V) == 1
            and sum(value != 0 for value in e) == 8,
            "the root-even coefficient changed")

    # This universal grant dominates every physically placed K_alpha/M_v
    # family: K_u is arbitrary pure residue and M_u ties lower to Eq.
    cartan = []
    mv = []
    for index in range(N):
        basis = unit(N, index)
        cartan.append(vector(ores=basis))
        mv.append(vector(lower=basis, eq=basis))
    granted = cartan + mv
    require(rank(granted) == 2 * N,
            "the universal Cartan/M_v grant lost rank")

    # A representative root-pair plus physical cross-cut transition.  Bar
    # boundaries are endpoint differences and hence must lie in the endpoint
    # span.  Checking them explicitly prevents a parity/coarse-label shortcut.
    root_sigma = (1, 0, 3, 2)
    cross_cut = (5, 4, 0, 2, 1, 3)
    bars = []
    for endpoint in cartan + mv:
        moved = vector(
            lower=permute_label_vector(endpoint[LOWER], root_sigma, cross_cut),
            eq=permute_label_vector(endpoint[EQ], root_sigma, cross_cut),
            ores=permute_label_vector(endpoint[ORES], root_sigma, cross_cut),
        )
        bars.append(add(moved, scale(-1, endpoint)))
    require(rank(granted + bars) == rank(granted),
            "a sigma endpoint bar escaped the endpoint span")

    # Four word-local lower-minus-Eq covectors survive the strongest grant.
    # CHI selects the B1/B4 fixed plane while killing the physical Cartan
    # residue plane; it gives an integral pairing on H.
    duals = []
    pairings = []
    for root in range(ROOTS):
        coefficient = tensor(unit(ROOTS, root), CHI)
        covector = vector(lower=coefficient, eq=scale(-1, coefficient))
        require(all(dot(covector, column) == 0
                    for column in granted + bars),
                ("lower-Eq dual sees a granted endpoint/bar", root))
        pairing = dot(covector, hidden)
        require(pairing == -2 * D_ROOT[root] and pairing,
                ("hidden-debt pairing changed", root, pairing))
        duals.append(covector)
        pairings.append(pairing)
    require(rank(granted + [hidden]) == rank(granted) + 1,
            "the hidden debt entered the universal Cartan/M_v span")

    # The formal decomposition identifies the one missing coordinate.  Even
    # after arbitrary K_E is granted, an Eq-only endpoint is indispensable.
    m_e = vector(lower=e, eq=e)
    k_e = vector(ores=e)
    clean_eq = vector(eq=e)
    require(hidden == add(scale(-1, m_e), k_e, clean_eq),
            "the hidden-debt decomposition changed")
    require(rank(granted + [clean_eq]) == rank(granted) + 1,
            "the clean Eq comparison entered the endpoint span")

    ledger = {
        "theorem": "C-plus hidden debt Cartan/M_v/root-bar span",
        "pins": PINS,
        "required_hidden_debt": {
            "E": "2 D_root tensor (B1+B4)/2",
            "signature_lower_Eq_ores": ["-E", "0", "+E"],
            "nonzero_label_coordinates": 8,
        },
        "strong_universal_grant": {
            "Cartan": "K_u=(0,0,u), arbitrary u in Q^24",
            "M_v": "M_u=(u,u,0), arbitrary u in Q^24",
            "span": "{(x,x,z): x,z in Q^24}",
            "rank": rank(granted),
            "sigma_bar_endpoints_adjoined": len(bars),
            "rank_after_sigma_bars": rank(granted + bars),
        },
        "primitive_dual": {
            "formula": "lambda_r=(e_r tensor chi)_lower-(e_r tensor chi)_Eq",
            "chi": [str(value) for value in CHI],
            "pairings_on_hidden_debt": [str(value) for value in pairings],
        },
        "exact_decomposition": (
            "H=-M_E+K_E+C_Eq, where C_Eq=(0,E,0) is the clean "
            "Eq-only comparison"
        ),
        "conclusion": (
            "physical Cartan/M_v cells and any sigma-paired bar between "
            "their endpoints cannot cancel H; K_E reduces the residue "
            "coordinate to the already isolated B1/B4 labelled section, "
            "while C_Eq is the same pointed K_Eq comparison, not a new "
            "bar consequence"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    ledger_digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(ledger_digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", ledger_digest))
    return ledger, ledger_digest


def main():
    _ledger, ledger_digest = audit()
    print("h3 C-plus hidden Cartan/M_v/root-bar span: SHARP NO-GO")
    print("strong endpoint span: {(x,x,z)}")
    print("hidden debt (-E,0,+E): rank +1")
    print("remaining coordinates: d_even residue + clean pointed K_Eq")
    print("ledger sha256:", ledger_digest)


if __name__ == "__main__":
    main()
