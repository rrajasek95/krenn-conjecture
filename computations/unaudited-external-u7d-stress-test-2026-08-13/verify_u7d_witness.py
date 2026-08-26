"""Independent exact re-verification of the external U7D witness.

UNAUDITED EXTERNAL STRESS TEST.  Source repo pinned at
https://github.com/YesterdaysLemon/krenn-gu-research/tree/f17afa1c8e72aeba51dafdf1e38afeb903591750

Nothing here imports the external python.  The witness data is transcribed
from their markdown in ``u7d_witness_data``; every check below is recomputed
from scratch with exact rational arithmetic (plus one 80-digit interval-free
numerical exhibit for the moment-balanced gauge, which is *additionally*
given an exact existence proof).

Checks (task B of the stress test):

  B1  complete r=1 support, amplitudes in {+1,-1}
  B2  105 perfect matchings, two independent enumerations agree
  B3  the three pure target coefficients are 1, each from a unique matching
  B4  the three cycle fibres are exactly the claimed binomials and vanish
  B5  z = sum_i (1_{B_i} - 1_{E_i}) has vanishing endpoint character and
      H = lambda^z = -1, invariant under the full vertex-colour torus
  B6  the odd/binomial structure: cycle length 3 (odd), |support(z)| = 12
  B7  strict positive endpoint balance with common loads (7,7,7)
  B8  the exposed mixed word eta has a one-term fibre of weight 1
  B9  the complete (4,4,0) census 57/10/3 and the 13-row certificate
  B10 the Laurent unit certificate of the exclusion theorem
  B11 moment-balanced representative over C: exact coercivity proof from
      the balance certificate, plus an 80-digit numerical minimiser
"""

from __future__ import annotations

import itertools
from fractions import Fraction

from u7d_witness_data import (
    AUX_BALANCE,
    BRIDGE,
    CLAIMED_CENSUS_COUNTS,
    CLAIMED_CENSUS_TABLE,
    CLAIMED_COMMON_LOAD,
    CLAIMED_CYCLE_FIBRES,
    CLAIMED_EXPOSED_FIBRE,
    CLAIMED_HOLONOMY,
    CLAIMED_MULTIDEGREE,
    CLAIMED_NONRIGIDITY,
    CLAIMED_PURE_FIBRES,
    CLAIMED_UNIT_MATCHING,
    CLAIMED_UNIT_WORD,
    CROSS,
    CYCLE_WORDS,
    EXPOSED_WORD,
    RESIDUAL,
    TABLE,
    parse_matching,
    parse_word,
)

ORDER = 8
COLOURS = 3
Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Word = tuple[int, ...]

RESULTS: list[tuple[str, str]] = []


def record(name: str, detail: str) -> None:
    """Append one passed check to the report ledger."""
    RESULTS.append((name, detail))
    print(f"  PASS  {name}: {detail}")


def require(condition: bool, message: str) -> None:
    """Fail loudly on a violated check."""
    if not condition:
        raise AssertionError(message)


# --------------------------------------------------------------------------
# matchings
# --------------------------------------------------------------------------
def matchings_lowest_first(vertices: tuple[int, ...]) -> list[Matching]:
    """Enumerate perfect matchings by pairing the least unused vertex."""
    if not vertices:
        return [()]
    head, rest = vertices[0], vertices[1:]
    answer = []
    for index, partner in enumerate(rest):
        residue = rest[:index] + rest[index + 1:]
        for tail in matchings_lowest_first(residue):
            answer.append(tuple(sorted(((head, partner),) + tail)))
    return answer


def matchings_from_permutations(order: int) -> set[Matching]:
    """Enumerate perfect matchings by de-duplicating permutations."""
    answer = set()
    for permutation in itertools.permutations(range(order)):
        pairs = tuple(sorted(
            (min(permutation[2 * k], permutation[2 * k + 1]),
             max(permutation[2 * k], permutation[2 * k + 1]))
            for k in range(order // 2)
        ))
        answer.add(pairs)
    return answer


def matching_record(matching: Matching) -> tuple[Word, Fraction, bool]:
    """Return the induced word, the exact amplitude product, diagonality."""
    word = [-1] * ORDER
    weight = Fraction(1)
    diagonal = True
    for edge in matching:
        left_label, right_label, amplitude = TABLE[edge]
        word[edge[0]] = left_label
        word[edge[1]] = right_label
        weight *= amplitude
        diagonal = diagonal and left_label == right_label
    require(all(value >= 0 for value in word), "unlabelled vertex")
    return tuple(word), weight, diagonal


def build_fibres() -> dict[Word, list[tuple[Matching, Fraction, bool]]]:
    """Group every perfect matching by its induced word."""
    fibres: dict[Word, list[tuple[Matching, Fraction, bool]]] = {}
    for matching in matchings_lowest_first(tuple(range(ORDER))):
        word, weight, diagonal = matching_record(matching)
        fibres.setdefault(word, []).append((matching, weight, diagonal))
    return fibres


def coefficient(fibres, word: Word) -> Fraction:
    """Exact coefficient c_word = sum over the compatible fibre."""
    return sum((weight for _, weight, _ in fibres.get(word, ())), Fraction(0))


# --------------------------------------------------------------------------
# B1 - B2
# --------------------------------------------------------------------------
def check_support_and_matchings():
    """Complete r=1 support and a two-route matching count."""
    all_pairs = set(itertools.combinations(range(ORDER), 2))
    require(set(TABLE) == all_pairs, "table is not the complete K8")
    require({data[2] for data in TABLE.values()} == {1, -1},
            "amplitudes are not unit signs")
    negatives = {edge for edge, data in TABLE.items() if data[2] == -1}
    require(negatives == {(1, 2), (1, 4), (2, 4)}, f"negatives {negatives}")
    record("B1 complete r=1 unit-phase support",
           f"28 pairs, negatives {sorted(negatives)}")

    lowest = matchings_lowest_first(tuple(range(ORDER)))
    permuted = matchings_from_permutations(ORDER)
    require(len(lowest) == 105, f"{len(lowest)} matchings")
    require(set(lowest) == permuted and len(permuted) == 105,
            "the two enumerations disagree")
    record("B2 perfect matchings", "105 by both routes (7!! = 105)")


# --------------------------------------------------------------------------
# B3 - B4
# --------------------------------------------------------------------------
def check_pure_and_cycle(fibres):
    """Pure coefficients and the three binomial cycle fibres."""
    for colour, claimed in CLAIMED_PURE_FIBRES.items():
        word = (colour,) * ORDER
        terms = fibres.get(word, [])
        require(len(terms) == 1, f"pure fibre {colour} has {len(terms)} terms")
        require(terms[0][0] == tuple(sorted(claimed)),
                f"pure fibre {colour} matching mismatch")
        require(terms[0][1] == 1, f"pure coefficient {colour} != 1")
        require(terms[0][2], f"pure matching {colour} not diagonal")
    record("B3 pure targets",
           "c(0^8)=c(1^8)=c(2^8)=1, each a unique diagonal matching")

    for word in CYCLE_WORDS:
        terms = fibres.get(word, [])
        require(len(terms) == 2, f"fibre {word} has {len(terms)} terms")
        found = {matching for matching, _, _ in terms}
        claimed = {tuple(sorted(m)) for m in CLAIMED_CYCLE_FIBRES[word]}
        require(found == claimed, f"fibre {word} mismatch: {found}")
        weights = sorted(weight for _, weight, _ in terms)
        require(weights == [Fraction(-1), Fraction(1)],
                f"fibre {word} weights {weights}")
        require(coefficient(fibres, word) == 0, f"c({word}) != 0")
        diagonal_flags = {matching: flag for matching, _, flag in terms}
        signs = {matching: weight for matching, weight, _ in terms}
        for matching, flag in diagonal_flags.items():
            require((signs[matching] == 1) == flag,
                    "diagonal/offdiagonal sign convention broken")
    record("B4 binomial cycle fibres",
           "chi_0, chi_1, chi_2 each a two-term (+1, -1) fibre with c = 0")


# --------------------------------------------------------------------------
# B5 - B6
# --------------------------------------------------------------------------
def circulation() -> dict[Edge, int]:
    """z = sum_i (1_{B_i} - 1_{E_i}) as an integer edge vector."""
    exponent: dict[Edge, int] = {}
    for bridge, cross in zip(BRIDGE, CROSS, strict=True):
        for edge in bridge:
            exponent[edge] = exponent.get(edge, 0) + 1
        for edge in cross:
            exponent[edge] = exponent.get(edge, 0) - 1
    return {edge: value for edge, value in exponent.items() if value}


def endpoint_character(exponent: dict[Edge, int]) -> dict[tuple[int, int], int]:
    """Unsigned incidence image in Z^{V x 3} of an edge exponent vector."""
    character: dict[tuple[int, int], int] = {}
    for edge, value in exponent.items():
        left_label, right_label, _ = TABLE[edge]
        for vertex, label in ((edge[0], left_label), (edge[1], right_label)):
            character[(vertex, label)] = character.get((vertex, label), 0) + value
    return {key: value for key, value in character.items() if value}


def laurent(exponent: dict[Edge, int],
            amplitudes: dict[Edge, Fraction]) -> Fraction:
    """Evaluate an integral Laurent monomial in the edge amplitudes."""
    value = Fraction(1)
    for edge, power in exponent.items():
        value *= Fraction(amplitudes[edge]) ** power
    return value


def check_holonomy(fibres):
    """The Laurent holonomy, its gauge invariance and its odd structure."""
    exponent = circulation()
    require(len(exponent) == 12, f"|support(z)| = {len(exponent)}")
    require(set(exponent.values()) == {1, -1}, "z is not a +-1 vector")
    character = endpoint_character(exponent)
    require(character == {}, f"z has nonzero endpoint character {character}")

    amplitudes = {edge: Fraction(data[2]) for edge, data in TABLE.items()}
    value = laurent(exponent, amplitudes)
    require(value == CLAIMED_HOLONOMY, f"H = {value}")
    record("B5 holonomy value",
           "H = prod_i lambda(B_i)/lambda(E_i) = -1, z in ker(unsigned incidence)")

    # gauge invariance under the FULL vertex-colour torus b_{v,c}
    rng_values = [Fraction(p, q) for p, q in
                  ((2, 3), (5, 7), (-3, 4), (11, 2), (1, 5), (7, 9), (-8, 3),
                   (13, 6), (4, 11), (9, 2), (-5, 8), (3, 7), (17, 5), (2, 13),
                   (6, 5), (-7, 11), (10, 3), (1, 2), (5, 4), (8, 7), (-2, 9),
                   (12, 5), (3, 8), (14, 3))]
    gauge = {(vertex, colour): rng_values[3 * vertex + colour]
             for vertex in range(ORDER) for colour in range(COLOURS)}
    gauged = {}
    for edge, (left_label, right_label, amplitude) in TABLE.items():
        gauged[edge] = (Fraction(amplitude)
                        * gauge[(edge[0], left_label)]
                        * gauge[(edge[1], right_label)])
    require(laurent(exponent, gauged) == CLAIMED_HOLONOMY,
            "H is not invariant under the full vertex-colour torus")
    record("B5b gauge invariance",
           "H unchanged by a generic rational (C*)^{V x 3} gauge")

    # Odd structure.  In the r=1 matrix-unit model every compatible matching
    # enters its target coefficient with combinatorial coefficient +1, so a
    # two-term fibre is the pure binomial x^{M_a} + x^{M_b} = 0, i.e. the
    # character requirement epsilon(d) = -1 on d = 1_{M_a} - 1_{M_b}.  Their
    # specialisation must realise that value.
    signs = []
    relations = []
    for word in CYCLE_WORDS:
        # canonical orientation: diagonal term minus offdiagonal term
        terms = sorted(fibres[word], key=lambda item: not item[2])
        (m_a, w_a, _), (m_b, w_b, _) = terms
        vector: dict[Edge, int] = {}
        for edge in m_a:
            vector[edge] = vector.get(edge, 0) + 1
        for edge in m_b:
            vector[edge] = vector.get(edge, 0) - 1
        relations.append({e: v for e, v in vector.items() if v})
        signs.append(Fraction(w_a, w_b))  # = lambda^d, must equal -1
    require(signs == [Fraction(-1)] * 3, f"fibre signs {signs}")
    total: dict[Edge, int] = {}
    for relation in relations:
        for edge, value in relation.items():
            total[edge] = total.get(edge, 0) + value
    total = {edge: value for edge, value in total.items() if value}
    require(total == exponent or {e: -v for e, v in total.items()} == exponent,
            "the three fibre relations do not compose to +-z")
    record("B6 odd three-fibre structure",
           "3 fibre relations, each of sign -1, summing to +-z; "
           "(-1)^3 = -1 = H, and z != 0 so this is a value, not a collision")

    # the residual matchings really do complete E_i and B_i to the fibres
    for index, word in enumerate(CYCLE_WORDS):
        off = tuple(sorted(CROSS[index] + RESIDUAL[index]))
        require(off in {m for m, _, _ in fibres[word]},
                f"E_{index} u P_{index} is not in fibre {word}")
    record("B6b cross/bridge decomposition",
           "E_i u P_i lies in F(chi_i) for i = 0,1,2 as claimed")


# --------------------------------------------------------------------------
# B7
# --------------------------------------------------------------------------
def endpoint_loads(values: dict[Edge, Fraction]):
    """Collect an edge value at each labelled endpoint (v, c)."""
    loads = {(vertex, colour): Fraction(0)
             for vertex in range(ORDER) for colour in range(COLOURS)}
    for edge, (left_label, right_label, _) in TABLE.items():
        loads[(edge[0], left_label)] += values[edge]
        loads[(edge[1], right_label)] += values[edge]
    return loads


def check_balance():
    """Strict positive integral endpoint balance with common load 7."""
    require(set(AUX_BALANCE) == set(TABLE), "balance vector is not complete")
    require(all(isinstance(v, int) and v > 0 for v in AUX_BALANCE.values()),
            "balance weights are not positive integers")
    loads = endpoint_loads({e: Fraction(v) for e, v in AUX_BALANCE.items()})
    require(set(loads.values()) == {Fraction(CLAIMED_COMMON_LOAD)},
            f"loads are not constant: {sorted(set(loads.values()))}")
    record("B7 strict endpoint balance",
           "all 24 labelled endpoint loads equal 7 with p_e positive integers")

    unit_loads = endpoint_loads({e: Fraction(1) for e in TABLE})
    require(len(set(unit_loads.values())) > 1,
            "the unit amplitudes were already balanced (claim says otherwise)")
    record("B7b unit table not itself balanced",
           f"unit loads range over {sorted(set(unit_loads.values()))}")


# --------------------------------------------------------------------------
# B8
# --------------------------------------------------------------------------
def nonrigidity_sets():
    """Their oriented colour-nonrigidity sets, recomputed from the table."""
    answer = []
    for colour in range(COLOURS):
        active = set()
        for edge, (left_label, right_label, _) in TABLE.items():
            if left_label != colour and right_label == colour:
                active.add(edge[0])
            if right_label != colour and left_label == colour:
                active.add(edge[1])
        answer.append(active)
    return tuple(answer)


def check_exposed(fibres):
    """The exposed mixed word and the nonrigidity sets."""
    terms = fibres.get(EXPOSED_WORD, [])
    require(len(terms) == 1, f"eta fibre has {len(terms)} terms")
    require(terms[0][0] == tuple(sorted(CLAIMED_EXPOSED_FIBRE)),
            "eta fibre matching mismatch")
    require(terms[0][1] == 1, "c(eta) != 1")
    require(not terms[0][2], "the eta matching is diagonal")
    record("B8 exposed mixed coefficient",
           "eta = 00000100 has the single offdiagonal term 04|17|26|35, c = 1 "
           "(so the table is NOT a Krenn-Gu witness, as they state)")

    sets = nonrigidity_sets()
    require(sets == CLAIMED_NONRIGIDITY, f"nonrigidity sets {sets}")
    require(all(s and len(s) < ORDER for s in sets),
            "some nonrigidity set is empty or improper")
    record("B8b nonrigidity sets",
           f"S_0 = S_1 = {sorted(sets[0])}, S_2 = {sorted(sets[2])}, "
           "all nonempty and proper")


# --------------------------------------------------------------------------
# B9 - B10
# --------------------------------------------------------------------------
def check_census(fibres):
    """The complete same-multidegree (4,4,0) census of the exclusion claim."""
    words = [word for word in itertools.product(range(COLOURS), repeat=ORDER)
             if tuple(word.count(c) for c in range(COLOURS))
             == CLAIMED_MULTIDEGREE]
    require(len(words) == 70, f"|W_mu| = {len(words)}")

    census = {"empty": 0, "singleton": 0, "binomial": 0, "other": 0}
    observed: dict[str, tuple[Matching, ...]] = {}
    for word in words:
        size = len(fibres.get(word, []))
        key = {0: "empty", 1: "singleton", 2: "binomial"}.get(size, "other")
        census[key] += 1
        if size:
            observed["".join(map(str, word))] = tuple(
                sorted(m for m, _, _ in fibres[word]))
    require(census["other"] == 0, f"unexpected fibre sizes: {census}")
    require({k: census[k] for k in CLAIMED_CENSUS_COUNTS}
            == CLAIMED_CENSUS_COUNTS, f"census {census}")

    claimed = {word: tuple(sorted(parse_matching(m) for m in ms))
               for word, ms in CLAIMED_CENSUS_TABLE.items()}
    require(observed == claimed,
            "the 13-row census certificate does not match")
    record("B9 complete (4,4,0) census",
           "70 words: 57 empty / 10 singleton / 3 binomial; 13-row table "
           "reproduced literally")

    binomial_words = {word for word, ms in observed.items() if len(ms) == 2}
    require(binomial_words == {"".join(map(str, w)) for w in CYCLE_WORDS},
            "the binomial words are not the active cycle")
    record("B9b binomial words",
           "the 3 binomial fibres are exactly the active cycle chi_0/1/2")

    for other in ((4, 0, 4), (0, 4, 4)):
        count = 0
        for word in itertools.product(range(COLOURS), repeat=ORDER):
            if tuple(word.count(c) for c in range(COLOURS)) != other:
                continue
            count += 1
            require(not fibres.get(word), f"multidegree {other} has a fibre")
        require(count == 70, f"{count} words of multidegree {other}")
    record("B9c other balanced binary blocks",
           "multidegrees (4,0,4) and (0,4,4): 70 empty fibres each")

    # B10 Laurent unit certificate
    unit_word = parse_word(CLAIMED_UNIT_WORD)
    terms = fibres[unit_word]
    require(len(terms) == 1, "the certificate word is not a singleton")
    require(terms[0][0] == parse_matching(CLAIMED_UNIT_MATCHING),
            "unit certificate matching mismatch")
    require(terms[0][1] != 0, "the unit certificate monomial vanishes")
    record("B10 Laurent unit certificate",
           f"c({CLAIMED_UNIT_WORD}) = lambda_01 lambda_24 lambda_37 lambda_56, "
           "a unit after Laurent saturation; so the complete (4,4,0) "
           "target-zero block generates the unit ideal")

    singletons = sorted(w for w, ms in observed.items() if len(ms) == 1)
    record("B10b all singleton words of (4,4,0)", ", ".join(singletons))


# --------------------------------------------------------------------------
# B11  moment-balanced representative over C
# --------------------------------------------------------------------------
def exact_coercivity_proof():
    """Exact proof that the moment-balancing minimiser exists.

    Setup.  Put x_{v,c} = 2 log s_{v,c}.  For edge e = (i, j) with labels
    (a, b) let A_e in Z^{V x 3} be the unsigned incidence row e_{i,a}+e_{j,b}.
    Then mu_e = |lambda'_e|^2 = exp(<A_e, x>) * lambda_e^2 and

        F(x) = sum_e mu_e,   dF/dx_{v,c} = load_{v,c}(mu).

    Minimising F over the GHZ subspace D = {x : sum_v x_{v,c} = 0 for all c}
    gives grad F in D^perp = span{u_0, u_1, u_2}, u_c = sum_v e_{v,c}, which
    is exactly the moment condition load_{v,c} = q_c for all v.

    Coercivity.  Let d in D with <A_e, d> <= 0 for every e.  The balance
    certificate p > 0 satisfies sum_e p_e A_e = 7 * 1 (all-ones on V x 3),
    and <1, d> = sum_c sum_v d_{v,c} = 0 because d in D.  Hence

        sum_e p_e <A_e, d> = 7 <1, d> = 0,

    and since every p_e > 0 and every term is <= 0, all <A_e, d> = 0, i.e.
    d lies in ker A.  So F has no direction of non-increase in D other than
    the flat directions ker A n D, along which F is constant.  F is therefore
    coercive and (strictly convex transverse to ker A) attains its minimum.
    This function verifies the two exact ingredients of that argument.
    """
    rows = {}
    for edge, (left_label, right_label, _) in TABLE.items():
        row = {(edge[0], left_label): 1}
        row[(edge[1], right_label)] = row.get((edge[1], right_label), 0) + 1
        rows[edge] = row

    combination: dict[tuple[int, int], int] = {}
    for edge, row in rows.items():
        for key, value in row.items():
            combination[key] = combination.get(key, 0) + AUX_BALANCE[edge] * value
    require(set(combination.values()) == {CLAIMED_COMMON_LOAD},
            f"sum_e p_e A_e is not 7 * all-ones: {sorted(set(combination.values()))}")
    require(all(value > 0 for value in AUX_BALANCE.values()), "p not positive")
    record("B11a exact coercivity ingredients",
           "p > 0 with sum_e p_e A_e = 7 * 1; hence any GHZ direction of "
           "non-increase lies in ker A -> minimiser exists (Kempf-Ness)")

    # amplitudes squared are all 1, so lambda_e^2 drops out of F
    require({data[2] ** 2 for data in TABLE.values()} == {1},
            "squared amplitudes are not all 1")
    return rows


def numerical_moment_gauge(rows, digits: int = 80):
    """Exhibit the minimiser to `digits` precision and bound the residual."""
    from mpmath import mp, exp, matrix, lu_solve, mpf

    mp.dps = digits
    keys = [(vertex, colour) for vertex in range(ORDER)
            for colour in range(COLOURS)]
    index = {key: position for position, key in enumerate(keys)}
    edges = sorted(TABLE)
    incidence = [[rows[edge].get(key, 0) for key in keys] for edge in edges]

    # constraint matrix B: sum_v x_{v,c} = 0 for each colour
    constraints = [[1 if key[1] == colour else 0 for key in keys]
                   for colour in range(COLOURS)]

    x = [mpf(0)] * len(keys)
    for _ in range(400):
        mu = [exp(sum(incidence[e][k] * x[k] for k in range(len(keys))))
              for e in range(len(edges))]
        gradient = [sum(incidence[e][k] * mu[e] for e in range(len(edges)))
                    for k in range(len(keys))]
        # project the gradient onto D^perp complement: subtract the colour means
        residual = list(gradient)
        for colour in range(COLOURS):
            mean = sum(gradient[index[(v, colour)]] for v in range(ORDER)) / ORDER
            for v in range(ORDER):
                residual[index[(v, colour)]] -= mean
        norm = max(abs(value) for value in residual)
        if norm < mpf(10) ** (-(digits - 15)):
            break
        hessian = matrix(len(keys) + COLOURS, len(keys) + COLOURS)
        for k in range(len(keys)):
            for l in range(len(keys)):
                hessian[k, l] = sum(
                    incidence[e][k] * incidence[e][l] * mu[e]
                    for e in range(len(edges)))
            hessian[k, k] += mpf(10) ** (-(digits // 2))  # tame ker A
        for c in range(COLOURS):
            for k in range(len(keys)):
                hessian[len(keys) + c, k] = constraints[c][k]
                hessian[k, len(keys) + c] = constraints[c][k]
        rhs = matrix([-value for value in residual] + [mpf(0)] * COLOURS)
        step = lu_solve(hessian, rhs)
        x = [x[k] + step[k] for k in range(len(keys))]
        for colour in range(COLOURS):
            mean = sum(x[index[(v, colour)]] for v in range(ORDER)) / ORDER
            for v in range(ORDER):
                x[index[(v, colour)]] -= mean

    mu = [exp(sum(incidence[e][k] * x[k] for k in range(len(keys))))
          for e in range(len(edges))]
    loads = {key: sum(incidence[e][index[key]] * mu[e]
                      for e in range(len(edges))) for key in keys}
    q = {colour: sum(loads[(v, colour)] for v in range(ORDER)) / ORDER
         for colour in range(COLOURS)}
    residual = max(abs(loads[(v, colour)] - q[colour])
                   for v in range(ORDER) for colour in range(COLOURS))
    scale = max(abs(q[colour]) for colour in range(COLOURS))
    constraint_error = max(abs(sum(x[index[(v, colour)]] for v in range(ORDER)))
                           for colour in range(COLOURS))
    require(residual / scale < mpf(10) ** (-40),
            f"moment residual too large: {residual}")
    require(constraint_error < mpf(10) ** (-40),
            f"GHZ constraint violated: {constraint_error}")
    require(all(value > 0 for value in mu), "some squared amplitude vanished")
    record("B11b numerical moment-balanced representative",
           f"80-digit minimiser: max_v,c |load - q_c| / max_c q_c "
           f"< 1e-40 (actual {mp.nstr(residual / scale, 3)}); "
           f"q = ({mp.nstr(q[0], 12)}, {mp.nstr(q[1], 12)}, {mp.nstr(q[2], 12)})")
    return x, mu, keys, index, edges


def check_gauge_covariance(fibres, x, keys, index, edges, digits: int = 80):
    """Pure coefficients, cycle zeros and H survive the moment gauge."""
    from mpmath import mp, exp, mpf

    mp.dps = digits
    # kappa_{c^8} = prod_v s_{v,c} = exp(sum_v x_{v,c} / 2) = 1 exactly by
    # the GHZ constraint; check numerically as well.
    for colour in range(COLOURS):
        kappa = exp(sum(x[index[(v, colour)]] for v in range(ORDER)) / 2)
        require(abs(kappa - 1) < mpf(10) ** (-40), f"kappa_{colour} != 1")
    record("B11c pure coefficients preserved",
           "kappa_(c^8) = prod_v s_{v,c} = 1 for c = 0,1,2 (GHZ constraint)")

    # the gauged amplitudes, and the exact-in-structure invariance of H
    gauged = {}
    for edge in edges:
        left_label, right_label, amplitude = TABLE[edge]
        factor = exp((x[index[(edge[0], left_label)]]
                      + x[index[(edge[1], right_label)]]) / 2)
        gauged[edge] = amplitude * factor
    exponent = circulation()
    value = mpf(1)
    for edge, power in exponent.items():
        value *= gauged[edge] ** power
    require(abs(value - CLAIMED_HOLONOMY) < mpf(10) ** (-40),
            f"H drifted under the moment gauge: {value}")
    record("B11d holonomy preserved",
           f"H = {mp.nstr(value, 20)} after the moment gauge "
           "(exact: z has zero endpoint character)")

    for word in CYCLE_WORDS:
        total = mpf(0)
        for matching, _, _ in fibres[word]:
            term = mpf(1)
            for edge in matching:
                term *= gauged[edge]
            total += term
        require(abs(total) < mpf(10) ** (-40), f"c'({word}) = {total}")
    for colour in range(COLOURS):
        word = (colour,) * ORDER
        total = mpf(0)
        for matching, _, _ in fibres[word]:
            term = mpf(1)
            for edge in matching:
                term *= gauged[edge]
            total += term
        require(abs(total - 1) < mpf(10) ** (-40), f"c'({word}) = {total}")
    exposed_total = mpf(0)
    for matching, _, _ in fibres[EXPOSED_WORD]:
        term = mpf(1)
        for edge in matching:
            term *= gauged[edge]
        exposed_total += term
    require(exposed_total > mpf(10) ** (-40), "c'(eta) collapsed to zero")
    record("B11e gauged coefficient ledger",
           "c'(chi_i) = 0 for i = 0,1,2; c'(c^8) = 1; c'(eta) = "
           f"{mp.nstr(exposed_total, 12)} > 0 (still not a witness)")


def main():
    """Run every check and print the ledger."""
    print("UNAUDITED EXTERNAL STRESS TEST -- independent verification of U7D")
    print("external repo pinned at commit "
          "f17afa1c8e72aeba51dafdf1e38afeb903591750\n")
    check_support_and_matchings()
    fibres = build_fibres()
    check_pure_and_cycle(fibres)
    check_holonomy(fibres)
    check_balance()
    check_exposed(fibres)
    check_census(fibres)
    rows = exact_coercivity_proof()
    x, _, keys, index, edges = numerical_moment_gauge(rows)
    check_gauge_covariance(fibres, x, keys, index, edges)
    print(f"\nALL {len(RESULTS)} CHECKS PASS")


if __name__ == "__main__":
    main()
