"""Integer exponent certificates for product-one vertex scaling from edge ratios."""

from collections import deque


def characters(n, edges):
    assert n >= 3 and n % 2 == 1
    edges = [tuple(sorted(edge)) for edge in edges]
    assert len(set(edges)) == len(edges)
    adjacency = [[] for _ in range(n)]
    for k, (i, j) in enumerate(edges):
        assert 0 <= i < j < n
        adjacency[i].append((j, k))
        adjacency[j].append((i, k))
    width = len(edges)
    signs = [0] * n
    signs[0] = 1
    kappa = [[0] * width for _ in range(n)]
    queue = deque([0])
    while queue:
        i = queue.popleft()
        for j, edge in adjacency[i]:
            if not signs[j]:
                signs[j] = -signs[i]
                kappa[j] = [-x for x in kappa[i]]
                kappa[j][edge] += 1
                queue.append(j)
    assert all(signs), "The alignment graph must be connected"
    imbalance = sum(signs)
    total = [sum(row[j] for row in kappa) for j in range(width)]
    chord = next((k for k, (i, j) in enumerate(edges) if signs[i] == signs[j]), None)
    if chord is None:
        if abs(imbalance) != 1:
            return {
                "unique_over_complex": False,
                "stabilizer_order": abs(imbalance),
                "bipartition_signs": signs,
            }
        root = [-imbalance * x for x in total]
    else:
        i, j = edges[chord]
        square = [
            signs[i] * (-a - b + int(k == chord))
            for k, (a, b) in enumerate(zip(kappa[i], kappa[j]))
        ]
        root = [-a + ((1 - imbalance) // 2) * b for a, b in zip(total, square)]
    exponents = [[signs[i] * a + b for a, b in zip(root, kappa[i])] for i in range(n)]
    offsets = []
    for i, row in enumerate(exponents):
        reconstructed = [0] * n
        for power, edge in zip(row, edges):
            for j in edge:
                reconstructed[j] += power
        reconstructed[i] -= 1
        assert len(set(reconstructed)) == 1
        offsets.append(reconstructed[0])
    return {
        "unique_over_complex": True,
        "edge_order": [list(edge) for edge in edges],
        "exponent_rows": exponents,
        "product_one_offsets": offsets,
        "all_integer_character_identities_checked": True,
    }


def exact_examples():
    result = []
    for n in range(3, 20, 2):
        path = [(i, i + 1) for i in range(n - 1)]
        star = [(0, i) for i in range(1, n)]
        for name, edges in [
            ("odd_path", path),
            ("star_with_triangle", star + [(1, 2)]),
        ]:
            report = characters(n, edges)
            assert report["unique_over_complex"]
            result.append({"sites": n, "graph": name, **report})
    rejected = characters(7, [(0, i) for i in range(1, 7)])
    assert not rejected["unique_over_complex"] and rejected["stabilizer_order"] == 5
    powers = rejected["bipartition_signs"]
    assert sum(powers) % 5 == 0
    assert all((powers[0] + powers[i]) % 5 == 0 for i in range(1, 7))
    assert (powers[0] - powers[1]) % 5 != 0
    return {
        "positive_examples": result,
        "seven_site_star": rejected,
        "star_fifth_root_stabilizer_checked_by_integer_exponents": True,
        "scope": "Checks the monomial identities and a complex ambiguity. The all-graph classification is proved in the note; finite graph checks do not establish it alone.",
    }
