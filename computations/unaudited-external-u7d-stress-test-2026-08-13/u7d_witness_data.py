"""Verbatim transcription of the external U7D witness data.

UNAUDITED EXTERNAL STRESS TEST.

Source repository: https://github.com/YesterdaysLemon/krenn-gu-research
Pinned commit:     f17afa1c8e72aeba51dafdf1e38afeb903591750  (2026-08-13T14:32:00Z)

Everything in this file is transcribed by hand from the two markdown claim
documents (NOT copied from their python), so that the checkers in this
directory are an independent route:

  claims/arbitrary-order/
    MATRIX_UNIT_COMPLETE_PURE_TARGET_MOMENT_COMPATIBLE_ODD_HOLONOMY_SHARPNESS_THEOREM.md
      = the "U7D sharpness" witness  (sections 1-5)
    MATRIX_UNIT_U7D_COMPLETE_SAME_MULTIDEGREE_TARGET_BLOCK_SATURATION_EXCLUSION_THEOREM.md
      = the complete (4,4,0) census / unit-ideal exclusion

Conventions.  Vertices 0..7.  A physical pair ij (i<j) carries exactly one
matrix unit: TABLE[(i, j)] = (label at i, label at j, amplitude).  This is
the r=1 case of our general bicoloured cell a_uv(i, j).
"""

from __future__ import annotations

from fractions import Fraction

Edge = tuple[int, int]

# --- sharpness theorem, section 1 (complete matrix-unit table) --------------
# 01=(0,0; 1)  02=(0,0; 1)  03=(0,0; 1)  04=(0,0; 1)
# 05=(1,2; 1)  06=(1,1; 1)  07=(2,2; 1)
# 12=(0,1;-1)  13=(0,0; 1)  14=(1,0;-1)  15=(1,1; 1)
# 16=(2,2; 1)  17=(0,0; 1)
# 23=(1,1; 1)  24=(0,1;-1)  25=(2,2; 1)  26=(0,0; 1)
# 27=(2,0; 1)
# 34=(2,2; 1)  35=(0,1; 1)  36=(1,0; 1)  37=(1,1; 1)
# 45=(0,0; 1)  46=(1,1; 1)  47=(1,1; 1)
# 56=(0,1; 1)  57=(1,1; 1)
# 67=(1,1; 1)
TABLE: dict[Edge, tuple[int, int, int]] = {
    (0, 1): (0, 0, 1),
    (0, 2): (0, 0, 1),
    (0, 3): (0, 0, 1),
    (0, 4): (0, 0, 1),
    (0, 5): (1, 2, 1),
    (0, 6): (1, 1, 1),
    (0, 7): (2, 2, 1),
    (1, 2): (0, 1, -1),
    (1, 3): (0, 0, 1),
    (1, 4): (1, 0, -1),
    (1, 5): (1, 1, 1),
    (1, 6): (2, 2, 1),
    (1, 7): (0, 0, 1),
    (2, 3): (1, 1, 1),
    (2, 4): (0, 1, -1),
    (2, 5): (2, 2, 1),
    (2, 6): (0, 0, 1),
    (2, 7): (2, 0, 1),
    (3, 4): (2, 2, 1),
    (3, 5): (0, 1, 1),
    (3, 6): (1, 0, 1),
    (3, 7): (1, 1, 1),
    (4, 5): (0, 0, 1),
    (4, 6): (1, 1, 1),
    (4, 7): (1, 1, 1),
    (5, 6): (0, 1, 1),
    (5, 7): (1, 1, 1),
    (6, 7): (1, 1, 1),
}

# --- sharpness theorem, section 3 (auxiliary incidence-dual weights) -------
AUX_BALANCE: dict[Edge, int] = {
    (0, 1): 1, (0, 2): 1, (0, 3): 4, (0, 4): 1,
    (0, 5): 6, (0, 6): 1, (0, 7): 7,
    (1, 2): 4, (1, 3): 1, (1, 4): 3, (1, 5): 4,
    (1, 6): 7, (1, 7): 1,
    (2, 3): 3, (2, 4): 2, (2, 5): 1, (2, 6): 4,
    (2, 7): 6,
    (3, 4): 7, (3, 5): 2, (3, 6): 3, (3, 7): 1,
    (4, 5): 3, (4, 6): 1, (4, 7): 4,
    (5, 6): 4, (5, 7): 1,
    (6, 7): 1,
}
CLAIMED_COMMON_LOAD = 7

# --- sharpness theorem, section 2 (equations (4), (5), (7)) ----------------
CYCLE_WORDS: tuple[tuple[int, ...], ...] = (
    (0, 0, 0, 0, 1, 1, 1, 1),   # chi_0 = 00001111
    (0, 0, 1, 1, 0, 0, 1, 1),   # chi_1 = 00110011
    (0, 1, 0, 1, 0, 1, 0, 1),   # chi_2 = 01010101
)

# equation (5): the complete compatible fibres of chi_0, chi_1, chi_2
CLAIMED_CYCLE_FIBRES: dict[tuple[int, ...], tuple[tuple[Edge, ...], ...]] = {
    CYCLE_WORDS[0]: (((0, 1), (2, 4), (3, 5), (6, 7)),
                     ((0, 2), (1, 3), (4, 6), (5, 7))),
    CYCLE_WORDS[1]: (((0, 1), (2, 3), (4, 5), (6, 7)),
                     ((0, 4), (1, 2), (3, 7), (5, 6))),
    CYCLE_WORDS[2]: (((0, 2), (1, 4), (3, 6), (5, 7)),
                     ((0, 4), (1, 5), (2, 6), (3, 7))),
}

# equation (7): cross cores E_i, bridges B_i, residual matchings P_i
CROSS: tuple[tuple[Edge, ...], ...] = (((2, 4), (3, 5)),
                                       ((1, 2), (5, 6)),
                                       ((1, 4), (3, 6)))
BRIDGE: tuple[tuple[Edge, ...], ...] = (((2, 3), (4, 5)),
                                        ((1, 5), (2, 6)),
                                        ((4, 6), (1, 3)))
RESIDUAL: tuple[tuple[Edge, ...], ...] = (((0, 1), (6, 7)),
                                          ((0, 4), (3, 7)),
                                          ((0, 2), (5, 7)))
CLAIMED_HOLONOMY = Fraction(-1)

# equation (2): the three pure fibres
CLAIMED_PURE_FIBRES: dict[int, tuple[Edge, ...]] = {
    0: ((0, 3), (1, 7), (2, 6), (4, 5)),
    1: ((0, 6), (1, 5), (2, 3), (4, 7)),
    2: ((0, 7), (1, 6), (2, 5), (3, 4)),
}

# section 5: the exposed mixed word eta = 00000100 and its fibre
EXPOSED_WORD: tuple[int, ...] = (0, 0, 0, 0, 0, 1, 0, 0)
CLAIMED_EXPOSED_FIBRE: tuple[Edge, ...] = ((0, 4), (1, 7), (2, 6), (3, 5))
CLAIMED_NONRIGIDITY = ({1, 2, 3, 4, 5, 6}, {1, 2, 3, 4, 5, 6}, {0, 7})

# --- exclusion theorem, section 2 (complete (4,4,0) census) ----------------
CLAIMED_MULTIDEGREE = (4, 4, 0)
CLAIMED_CENSUS_COUNTS = {"empty": 57, "singleton": 10, "binomial": 3}
CLAIMED_CENSUS_TABLE: dict[str, tuple[str, ...]] = {
    "00001111": ("01|24|35|67", "02|13|46|57"),
    "00011011": ("01|24|37|56",),
    "00011101": ("01|24|36|57",),
    "00100111": ("04|12|35|67",),
    "00101011": ("03|12|47|56",),
    "00110011": ("01|23|45|67", "04|12|37|56"),
    "00110101": ("04|12|36|57",),
    "01000111": ("02|14|35|67",),
    "01001101": ("03|15|26|47",),
    "01010011": ("02|14|37|56",),
    "01010101": ("02|14|36|57", "04|15|26|37"),
    "10001110": ("06|17|24|35",),
    "10110010": ("06|17|23|45",),
}
# equation (1)/(12): the singleton used for the Laurent unit certificate
CLAIMED_UNIT_WORD = "00011011"
CLAIMED_UNIT_MATCHING = "01|24|37|56"


def parse_matching(text: str) -> tuple[Edge, ...]:
    """Turn '01|24|37|56' into ((0,1),(2,4),(3,7),(5,6))."""
    return tuple(sorted((int(part[0]), int(part[1])) for part in text.split("|")))


def parse_word(text: str) -> tuple[int, ...]:
    """Turn '00011011' into (0,0,0,1,1,0,1,1)."""
    return tuple(int(character) for character in text)
