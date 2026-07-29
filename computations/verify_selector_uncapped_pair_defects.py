#!/usr/bin/env python3
"""Exact audit of uncapped pair defects invisible to termwise selectors."""

from itertools import combinations, product


P, Q = 0, 1
R = tuple(range(2, 8))
E = tuple(combinations(range(8), 2))


def zero_matrix():
    return [[0 for _ in range(3)] for _ in range(3)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def determinant3(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2]
                        - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2]
                          - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1]
                          - matrix[1][1] * matrix[2][0])
    )


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


MATCHINGS = {vertices: tuple(perfect_matchings(vertices))
             for size in (0, 2, 4, 6, 8)
             for vertices in combinations(range(8), size)}


def edge_matrix(blocks, u, v):
    if u < v:
        return blocks[u, v]
    return transpose(blocks[v, u])


def edge_value(blocks, u, v, color_u, color_v):
    return edge_matrix(blocks, u, v)[color_u][color_v]


def hafnian_coefficient(blocks, vertices, coloring):
    total = 0
    for matching in MATCHINGS[tuple(sorted(vertices))]:
        value = 1
        for u, v in matching:
            value *= edge_value(blocks, u, v, coloring[u], coloring[v])
        total += value
    return total


def outer(left, right):
    return [[left[i] * right[j] for j in range(3)] for i in range(3)]


def add_matrix(left, right, scale=1):
    return [[left[i][j] + scale * right[i][j] for j in range(3)]
            for i in range(3)]


def scale_matrix(scale, matrix):
    return [[scale * value for value in row] for row in matrix]


def direct_pair_slice(blocks, outside_word):
    coloring = dict(zip(R, outside_word))
    return [[hafnian_coefficient(
        blocks, tuple(range(8)), {**coloring, P: i, Q: j})
             for j in range(3)] for i in range(3)]


def pair_formula(blocks, outside_word):
    coloring = dict(zip(R, outside_word))
    h = hafnian_coefficient(blocks, R, coloring)
    answer = scale_matrix(h, edge_matrix(blocks, P, Q))
    for u, v in combinations(R, 2):
        remaining = tuple(w for w in R if w not in (u, v))
        huv = hafnian_coefficient(blocks, remaining, coloring)
        pu = [edge_value(blocks, P, u, i, coloring[u]) for i in range(3)]
        pv = [edge_value(blocks, P, v, i, coloring[v]) for i in range(3)]
        qu = [edge_value(blocks, Q, u, i, coloring[u]) for i in range(3)]
        qv = [edge_value(blocks, Q, v, i, coloring[v]) for i in range(3)]
        answer = add_matrix(answer, outer(pu, qv), huv)
        answer = add_matrix(answer, outer(pv, qu), huv)
    return answer


def dense_blocks():
    blocks = {}
    for u, v in E:
        blocks[u, v] = [[
            ((u + 2) * (i + 1) + (v + 3) * (j + 2)
             + 2 * i * j + i * i - j) % 11 - 5
            for j in range(3)] for i in range(3)]
    return blocks


def balanced_blocks():
    blocks = {edge: zero_matrix() for edge in E}
    conceptual = {label: label + 2 for label in range(6)}
    matchings = (
        ((P, conceptual[0]), (Q, conceptual[1]),
         (conceptual[2], conceptual[3]), (conceptual[4], conceptual[5])),
        ((P, conceptual[2]), (Q, conceptual[3]),
         (conceptual[0], conceptual[4]), (conceptual[1], conceptual[5])),
        ((P, conceptual[4]), (Q, conceptual[5]),
         (conceptual[0], conceptual[2]), (conceptual[1], conceptual[3])),
    )
    for color, matching in enumerate(matchings):
        for u, v in matching:
            blocks[tuple(sorted((u, v)))][color][color] += 1
    blocks[P, Q] = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
    return blocks, matchings


def selector_sector(blocks, s, color, crossing_number, output_word):
    shore = {P, Q, s}
    exposed = tuple(vertex for vertex in range(8) if vertex not in shore)
    coloring = {P: color, Q: color, s: color}
    coloring.update(dict(zip(exposed, output_word)))
    total = 0
    for matching in MATCHINGS[tuple(range(8))]:
        crossing = sum((u in shore) != (v in shore) for u, v in matching)
        if crossing != crossing_number:
            continue
        value = 1
        for u, v in matching:
            value *= edge_value(blocks, u, v, coloring[u], coloring[v])
        total += value
    return total


def local_l_vector(blocks, s, color, u):
    return tuple(
        edge_value(blocks, P, Q, color, color)
        * edge_value(blocks, s, u, color, color_u)
        + edge_value(blocks, P, s, color, color)
        * edge_value(blocks, Q, u, color, color_u)
        + edge_value(blocks, Q, s, color, color)
        * edge_value(blocks, P, u, color, color_u)
        for color_u in range(3)
    )


def full_coefficient(blocks, word):
    return hafnian_coefficient(blocks, tuple(range(8)), dict(enumerate(word)))


def nonzero_matching_channels(blocks, word):
    coloring = dict(enumerate(word))
    channels = []
    for matching in MATCHINGS[tuple(range(8))]:
        value = 1
        for u, v in matching:
            value *= edge_value(blocks, u, v, coloring[u], coloring[v])
        if value:
            channels.append((matching, value, (P, Q) in matching))
    return channels


def main():
    # Audit the uncapped pair formula away from the sparse example.
    dense = dense_blocks()
    for outside_word in product(range(3), repeat=6):
        assert direct_pair_slice(dense, outside_word) == pair_formula(
            dense, outside_word)

    blocks, matchings = balanced_blocks()
    assert determinant3(blocks[P, Q]) == 1
    declarations = []
    for color, matching in enumerate(matchings):
        excluded = {next(v for u, v in matching if u == P),
                    next(v for u, v in matching if u == Q)}
        declarations.extend((s, color) for s in R if s not in excluded)
    assert len(declarations) == 12
    assert {s for s, _ in declarations} == set(R)
    assert {color for _, color in declarations} == {0, 1, 2}

    for s, color in declarations:
        exposed = tuple(vertex for vertex in range(8)
                        if vertex not in (P, Q, s))
        for output_word in product(range(3), repeat=5):
            assert selector_sector(blocks, s, color, 1, output_word) == 0
            expected = int(all(entry == color for entry in output_word))
            assert selector_sector(blocks, s, color, 3, output_word) == expected
        for u in exposed:
            assert local_l_vector(blocks, s, color, u) == (0, 0, 0)

    expected_residual = {
        (0, 1, 1, 1, 0, 0, 1, 1),
        (0, 1, 2, 2, 2, 2, 0, 0),
        (1, 2, 1, 1, 0, 0, 1, 1),
        (1, 2, 1, 2, 1, 2, 1, 2),
        (1, 2, 2, 2, 2, 2, 0, 0),
        (2, 0, 1, 1, 0, 0, 1, 1),
        (2, 0, 2, 2, 2, 2, 0, 0),
        (2, 1, 2, 1, 2, 1, 2, 1),
    }
    residual = {}
    for word in product(range(3), repeat=8):
        target = int(len(set(word)) == 1)
        value = full_coefficient(blocks, word) - target
        if value:
            residual[word] = value
    assert set(residual) == expected_residual
    assert set(residual.values()) == {1}

    pair_used = 0
    pair_avoided = 0
    distances = []
    for word in expected_residual:
        channels = nonzero_matching_channels(blocks, word)
        assert len(channels) == 1 and channels[0][1] == 1
        if channels[0][2]:
            pair_used += 1
        else:
            pair_avoided += 1
        distances.append(8 - max(word.count(color) for color in range(3)))
    assert (pair_used, pair_avoided) == (6, 2)
    assert sorted(distances) == [3, 3, 3, 3, 4, 4, 4, 4]

    # The internal C6 has exactly two nonconstant coefficient words.  At
    # each, the avoiding-pq correction X is zero, whereas the actual target
    # identity would require -A_pq, a rank-three matrix.
    internal_words = []
    for outside_word in product(range(3), repeat=6):
        coloring = dict(zip(R, outside_word))
        h = hafnian_coefficient(blocks, R, coloring)
        if h:
            internal_words.append((outside_word, h))
            formula = pair_formula(blocks, outside_word)
            pair_part = scale_matrix(h, edge_matrix(blocks, P, Q))
            correction = add_matrix(formula, pair_part, -1)
            assert correction == zero_matrix()
            assert determinant3(scale_matrix(-h, edge_matrix(blocks, P, Q))) != 0
    assert len(internal_words) == 2
    assert all(len(set(word)) > 1 and h == 1 for word, h in internal_words)

    print("PASS: uncapped pair identity audited on all 729 outside words")
    print("PASS: 12 termwise selectors and exact 8-word residual (6+2) audited")
    print("PASS: two missing word-aligned rank-three extensions certified")


if __name__ == "__main__":
    main()
