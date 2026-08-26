use std::collections::{BTreeMap, BTreeSet, HashMap, VecDeque};
use std::fs;

const P: i32 = 32003;
const ROOT_WORD: [u8; 8] = [0, 1, 2, 1, 1, 2, 2, 2];
const SLICE_WORDS: [[u8; 8]; 3] = [
    [0, 1, 2, 1, 1, 2, 2, 2],
    [0, 1, 2, 0, 0, 0, 0, 0],
    [0, 1, 2, 1, 1, 1, 1, 1],
];
const T_EDGES: [(u8, u8); 3] = [(0, 1), (0, 2), (1, 2)];
const FIVE_EDGES: [(u8, u8); 10] = [
    (3, 4),
    (3, 5),
    (3, 6),
    (3, 7),
    (4, 5),
    (4, 6),
    (4, 7),
    (5, 6),
    (5, 7),
    (6, 7),
];

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Monomial([u16; 9]);

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Monomial13([u16; 13]);

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct PhysicalGraph([u8; 28]);

type Poly = BTreeMap<Monomial, i32>;
type Poly13 = BTreeMap<Vec<u16>, i32>;

fn modp(x: i64) -> i32 {
    let mut y = (x % P as i64) as i32;
    if y < 0 {
        y += P;
    }
    y
}

fn cell(mut u: u8, mut v: u8, mut a: u8, mut b: u8) -> u16 {
    if u > v {
        std::mem::swap(&mut u, &mut v);
        std::mem::swap(&mut a, &mut b);
    }
    let mut edge_index = 0u16;
    for x in 0..8u8 {
        for y in x + 1..8u8 {
            if (x, y) == (u, v) {
                return edge_index * 9 + (a as u16) * 3 + b as u16;
            }
            edge_index += 1;
        }
    }
    panic!("bad edge");
}

fn cell_label(id: u16) -> String {
    let edge_index = id / 9;
    let colour = id % 9;
    let mut current = 0u16;
    for u in 0..8u8 {
        for v in u + 1..8u8 {
            if current == edge_index {
                return format!("A_{u}{v}[{},{}]", colour / 3, colour % 3);
            }
            current += 1;
        }
    }
    panic!("bad cell id");
}

fn dense_values(seed: i32) -> [i32; 252] {
    let mut values = [0i32; 252];
    for u in 0..8u8 {
        for v in u + 1..8u8 {
            for a in 0..3u8 {
                for b in 0..3u8 {
                    let flat = (((u as i32 * 8 + v as i32) * 3 + a as i32) * 3 + b as i32) + 1;
                    values[cell(u, v, a, b) as usize] = 1
                        + (seed * flat * flat
                            + 7 * flat
                            + 11 * (u as i32 + 1) * (b as i32 + 1)
                            + 13 * (v as i32 + 1) * (a as i32 + 1))
                            % 23;
                }
            }
        }
    }
    values
}

fn evaluate_cells(cells: &[u16], values: &[i32; 252]) -> i32 {
    cells.iter().fold(1i32, |answer, &id| {
        modp(answer as i64 * values[id as usize] as i64)
    })
}

fn evaluate_poly(poly: &Poly, values: &[i32; 252]) -> i32 {
    poly.iter().fold(0i32, |answer, (term, &coefficient)| {
        modp(answer as i64 + coefficient as i64 * evaluate_cells(&term.0, values) as i64)
    })
}

fn evaluate_vec_poly(poly: &BTreeMap<Vec<u16>, i32>, values: &[i32; 252]) -> i32 {
    poly.iter().fold(0i32, |answer, (term, &coefficient)| {
        modp(answer as i64 + coefficient as i64 * evaluate_cells(term, values) as i64)
    })
}

fn perfect_matchings(vertices: &[u8]) -> Vec<Vec<(u8, u8)>> {
    if vertices.is_empty() {
        return vec![Vec::new()];
    }
    let first = vertices[0];
    let mut out = Vec::new();
    for pos in 1..vertices.len() {
        let second = vertices[pos];
        let mut rest = Vec::with_capacity(vertices.len() - 2);
        rest.extend_from_slice(&vertices[1..pos]);
        rest.extend_from_slice(&vertices[pos + 1..]);
        for mut tail in perfect_matchings(&rest) {
            let mut row = vec![(first.min(second), first.max(second))];
            row.append(&mut tail);
            out.push(row);
        }
    }
    out
}

fn monomial(mut cells: Vec<u16>) -> Monomial {
    assert_eq!(cells.len(), 9);
    cells.sort_unstable();
    Monomial(cells.try_into().unwrap())
}

fn monomial13(mut cells: Vec<u16>) -> Monomial13 {
    assert_eq!(cells.len(), 13);
    cells.sort_unstable();
    Monomial13(cells.try_into().unwrap())
}

fn poly_add_term(poly: &mut Poly, key: Monomial, coefficient: i32) {
    let value = modp(*poly.get(&key).unwrap_or(&0) as i64 + coefficient as i64);
    if value == 0 {
        poly.remove(&key);
    } else {
        poly.insert(key, value);
    }
}

fn matching_cells(word: &[u8; 8], matching: &[(u8, u8)]) -> Vec<u16> {
    matching
        .iter()
        .map(|&(u, v)| cell(u, v, word[u as usize], word[v as usize]))
        .collect()
}

fn multiply_by_pure(poly: &Poly, pm8: &[Vec<(u8, u8)>], colour: u8) -> Poly13 {
    let pure = [colour; 8];
    let mut out = Poly13::new();
    for (left, &coefficient) in poly {
        for matching in pm8 {
            let mut cells = left.0.to_vec();
            cells.extend(matching_cells(&pure, matching));
            cells.sort_unstable();
            let value = modp(*out.get(&cells).unwrap_or(&0) as i64 + coefficient as i64);
            if value == 0 {
                out.remove(&cells);
            } else {
                out.insert(cells, value);
            }
        }
    }
    out
}

fn matching_edge_ids(matching: &[(u8, u8)]) -> Vec<u16> {
    matching
        .iter()
        .map(|&(u, v)| cell(u, v, 0, 0) / 9)
        .collect()
}

fn physical_graph(cells: &[u16]) -> PhysicalGraph {
    let mut graph = [0u8; 28];
    for &id in cells {
        graph[(id / 9) as usize] += 1;
    }
    PhysicalGraph(graph)
}

fn graph_add(left: PhysicalGraph, right: PhysicalGraph) -> PhysicalGraph {
    let mut out = [0u8; 28];
    for i in 0..28 {
        out[i] = left.0[i] + right.0[i];
    }
    PhysicalGraph(out)
}

fn graph_row_add(row: &mut BTreeMap<PhysicalGraph, i32>, graph: PhysicalGraph, coefficient: i32) {
    let value = modp(*row.get(&graph).unwrap_or(&0) as i64 + coefficient as i64);
    if value == 0 {
        row.remove(&graph);
    } else {
        row.insert(graph, value);
    }
}

fn graph_row_reduce(
    mut row: BTreeMap<PhysicalGraph, i32>,
    basis: &BTreeMap<PhysicalGraph, BTreeMap<PhysicalGraph, i32>>,
) -> BTreeMap<PhysicalGraph, i32> {
    while let Some((&pivot, &coefficient)) = row.first_key_value() {
        let Some(base) = basis.get(&pivot) else { break };
        for (&graph, &value) in base {
            graph_row_add(&mut row, graph, -modp(coefficient as i64 * value as i64));
        }
    }
    row
}

fn graph_row_basis(
    rows: impl IntoIterator<Item = BTreeMap<PhysicalGraph, i32>>,
) -> BTreeMap<PhysicalGraph, BTreeMap<PhysicalGraph, i32>> {
    let mut basis = BTreeMap::new();
    for row in rows {
        let mut reduced = graph_row_reduce(row, &basis);
        if let Some((&pivot, &coefficient)) = reduced.first_key_value() {
            let inverse = mod_pow(coefficient, P - 2);
            for value in reduced.values_mut() {
                *value = modp(*value as i64 * inverse as i64);
            }
            basis.insert(pivot, reduced);
        }
    }
    basis
}

fn has_mixed_matching_divisor(term: &[u16], pm8: &[Vec<(u8, u8)>]) -> bool {
    let mut by_edge: [Vec<u16>; 28] = std::array::from_fn(|_| Vec::new());
    for &id in term {
        by_edge[(id / 9) as usize].push(id % 9);
    }
    'matching: for matching in pm8 {
        let edge_ids = matching_edge_ids(matching);
        if edge_ids
            .iter()
            .any(|&edge| by_edge[edge as usize].is_empty())
        {
            continue;
        }
        let mut only_diagonal_colour: Option<u16> = None;
        for edge in edge_ids {
            for &colour_pair in &by_edge[edge as usize] {
                let left = colour_pair / 3;
                let right = colour_pair % 3;
                if left != right {
                    return true;
                }
                match only_diagonal_colour {
                    None => only_diagonal_colour = Some(left),
                    Some(colour) if colour == left => {}
                    Some(_) => return true,
                }
            }
        }
        // All available divisors on this physical matching are the same pure
        // word, so this matching cannot supply a mixed generator.
        continue 'matching;
    }
    false
}

fn has_mixed_divisor_on_matching(term: &[u16], matching: &[(u8, u8)]) -> bool {
    let mut by_edge: [Vec<u16>; 28] = std::array::from_fn(|_| Vec::new());
    for &id in term {
        by_edge[(id / 9) as usize].push(id % 9);
    }
    let edge_ids = matching_edge_ids(matching);
    if edge_ids
        .iter()
        .any(|&edge| by_edge[edge as usize].is_empty())
    {
        return false;
    }
    let mut diagonal_colour: Option<u16> = None;
    for edge in edge_ids {
        for &colour_pair in &by_edge[edge as usize] {
            let left = colour_pair / 3;
            let right = colour_pair % 3;
            if left != right {
                return true;
            }
            match diagonal_colour {
                None => diagonal_colour = Some(left),
                Some(colour) if colour == left => {}
                Some(_) => return true,
            }
        }
    }
    false
}

fn multiset_divides(divisor: &[u16], term: &[u16]) -> bool {
    let (mut i, mut j) = (0usize, 0usize);
    while i < divisor.len() && j < term.len() {
        if divisor[i] == term[j] {
            i += 1;
            j += 1;
        } else if divisor[i] > term[j] {
            j += 1;
        } else {
            return false;
        }
    }
    i == divisor.len()
}

fn multiset_quotient(term: &[u16], divisor: &[u16]) -> Option<Vec<u16>> {
    let mut quotient = Vec::with_capacity(term.len().saturating_sub(divisor.len()));
    let mut i = 0usize;
    let mut j = 0usize;
    while i < divisor.len() && j < term.len() {
        if divisor[i] == term[j] {
            i += 1;
            j += 1;
        } else if divisor[i] > term[j] {
            quotient.push(term[j]);
            j += 1;
        } else {
            return None;
        }
    }
    if i != divisor.len() {
        return None;
    }
    quotient.extend_from_slice(&term[j..]);
    Some(quotient)
}

fn source_generator_support(
    term: &[u16],
    pm8: &[Vec<(u8, u8)>],
    chi: &BTreeMap<Vec<u16>, i32>,
) -> &'static str {
    if has_mixed_matching_divisor(term, pm8) {
        return "mixed_x5";
    }
    if chi.keys().any(|divisor| multiset_divides(divisor, term)) {
        return "clean_error";
    }
    "absent"
}

fn pure_matching_chart_profile(
    poly: &Poly,
    pure_colour: u8,
    pure_matching: &[(u8, u8)],
    pm8: &[Vec<(u8, u8)>],
    chi: &BTreeMap<Vec<u16>, i32>,
) -> BTreeMap<&'static str, usize> {
    let pure_word = [pure_colour; 8];
    let multiplier = matching_cells(&pure_word, pure_matching);
    let mut profile = BTreeMap::new();
    for term in poly.keys() {
        let mut product = term.0.to_vec();
        product.extend(&multiplier);
        product.sort_unstable();
        let class = source_generator_support(&product, pm8, chi);
        *profile.entry(class).or_insert(0) += 1;
    }
    profile
}

fn matching_label(matching: &[(u8, u8)]) -> String {
    matching
        .iter()
        .map(|&(u, v)| format!("{u}{v}"))
        .collect::<Vec<_>>()
        .join("|")
}

fn word_code(word: &[u8; 8]) -> usize {
    let mut code = 0usize;
    let mut power = 1usize;
    for &colour in word {
        code += colour as usize * power;
        power *= 3;
    }
    code
}

fn decode_word(mut code: usize) -> [u8; 8] {
    let mut word = [0u8; 8];
    for colour in &mut word {
        *colour = (code % 3) as u8;
        code /= 3;
    }
    word
}

fn quotient_monomial(term: &[u16], divisor: &[u16]) -> Monomial {
    let mut quotient = Vec::with_capacity(term.len() - divisor.len());
    let mut remaining = divisor.to_vec();
    remaining.sort_unstable();
    let mut next = 0usize;
    for &id in term {
        if next < remaining.len() && id == remaining[next] {
            next += 1;
        } else {
            quotient.push(id);
        }
    }
    assert_eq!(next, remaining.len());
    monomial(quotient)
}

fn divisor_candidates(term: &[u16], pm8: &[Vec<(u8, u8)>]) -> Vec<(u16, u8)> {
    let mut by_edge: [Vec<u16>; 28] = std::array::from_fn(|_| Vec::new());
    for &id in term {
        let edge = (id / 9) as usize;
        let colour_pair = id % 9;
        if !by_edge[edge].contains(&colour_pair) {
            by_edge[edge].push(colour_pair);
        }
    }
    let mut out = BTreeSet::new();
    for (matching_index, matching) in pm8.iter().enumerate() {
        let edge_ids = matching_edge_ids(matching);
        if edge_ids.iter().any(|&edge| by_edge[edge as usize].is_empty()) {
            continue;
        }
        for &c0 in &by_edge[edge_ids[0] as usize] {
            for &c1 in &by_edge[edge_ids[1] as usize] {
                for &c2 in &by_edge[edge_ids[2] as usize] {
                    for &c3 in &by_edge[edge_ids[3] as usize] {
                        let mut word = [0u8; 8];
                        for (edge, colour_pair) in
                            matching.iter().zip([c0, c1, c2, c3].into_iter())
                        {
                            let (u, v) = *edge;
                            word[u as usize] = (colour_pair / 3) as u8;
                            word[v as usize] = (colour_pair % 3) as u8;
                        }
                        if word.iter().all(|&x| x == word[0]) {
                            continue;
                        }
                        out.insert((word_code(&word) as u16, matching_index as u8));
                    }
                }
            }
        }
    }
    out.into_iter().collect()
}

fn leading_matchings(weights: &[i64; 252], pm8: &[Vec<(u8, u8)>]) -> Vec<u8> {
    let mut leading = vec![0u8; 6561];
    for code in 0..6561usize {
        let mut x = code;
        let mut word = [0u8; 8];
        for colour in &mut word {
            *colour = (x % 3) as u8;
            x /= 3;
        }
        let mut best = (i64::MIN, 0u8);
        for (matching_index, matching) in pm8.iter().enumerate() {
            let score = matching_cells(&word, matching)
                .iter()
                .map(|&id| weights[id as usize])
                .sum::<i64>();
            let candidate = (score, matching_index as u8);
            if candidate > best {
                best = candidate;
            }
        }
        leading[code] = best.1;
    }
    leading
}

fn xorshift64(state: &mut u64) -> u64 {
    let mut x = *state;
    x ^= x << 13;
    x ^= x >> 7;
    x ^= x << 17;
    *state = x;
    x
}

fn mod_pow(mut base: i32, mut exponent: i32) -> i32 {
    let mut answer = 1i32;
    while exponent > 0 {
        if exponent & 1 == 1 {
            answer = modp(answer as i64 * base as i64);
        }
        base = modp(base as i64 * base as i64);
        exponent >>= 1;
    }
    answer
}

fn peel_first_exchange(
    h: &Poly,
    cone_multiplier: &[u16],
    exchange_rows: &BTreeSet<(u16, Monomial)>,
    clean_quotients: &BTreeSet<Vec<u16>>,
    chi: &BTreeMap<Vec<u16>, i32>,
    pm8: &[Vec<(u8, u8)>],
) -> (
    usize,
    usize,
    usize,
    usize,
    bool,
    Option<(Monomial13, i32)>,
    Vec<Monomial13>,
) {
    let mut column_ids: HashMap<Monomial13, u32> = HashMap::new();
    let mut column_keys = Vec::new();
    let mut rows_columns: Vec<Vec<(u32, i32)>> =
        Vec::with_capacity(exchange_rows.len() + clean_quotients.len());
    for &(code, quotient) in exchange_rows {
        let word = decode_word(code as usize);
        let mut row = Vec::with_capacity(105);
        for matching in pm8 {
            let mut product = quotient.0.to_vec();
            product.extend(matching_cells(&word, matching));
            let key = monomial13(product);
            let id = if let Some(&id) = column_ids.get(&key) {
                id
            } else {
                let id = column_ids.len() as u32;
                column_ids.insert(key, id);
                column_keys.push(key);
                id
            };
            row.push((id, 1));
        }
        row.sort_unstable_by_key(|x| x.0);
        row.dedup_by_key(|x| x.0);
        assert_eq!(row.len(), 105);
        rows_columns.push(row);
    }
    for quotient in clean_quotients {
        let mut collected: BTreeMap<u32, i32> = BTreeMap::new();
        for (term, &coefficient) in chi {
            let mut product = quotient.clone();
            product.extend(term);
            let key = monomial13(product);
            let id = if let Some(&id) = column_ids.get(&key) {
                id
            } else {
                let id = column_ids.len() as u32;
                column_ids.insert(key, id);
                column_keys.push(key);
                id
            };
            let value = modp(*collected.get(&id).unwrap_or(&0) as i64 + coefficient as i64);
            if value == 0 {
                collected.remove(&id);
            } else {
                collected.insert(id, value);
            }
        }
        rows_columns.push(collected.into_iter().collect());
    }
    let column_count = column_ids.len();
    let mut rhs = vec![0i32; column_count];
    for (term, &coefficient) in h {
        let mut product = term.0.to_vec();
        product.extend(cone_multiplier);
        let key = monomial13(product);
        let id = *column_ids
            .get(&key)
            .expect("every target term has an exchange-row occurrence") as usize;
        rhs[id] = modp(rhs[id] as i64 + coefficient as i64);
    }
    drop(column_ids);

    let mut degree = vec![0usize; column_count];
    for row in &rows_columns {
        for &(column, _) in row {
            degree[column as usize] += 1;
        }
    }
    let mut offsets = Vec::with_capacity(column_count + 1);
    offsets.push(0usize);
    for &d in &degree {
        offsets.push(offsets.last().copied().unwrap() + d);
    }
    let mut cursor = offsets[..column_count].to_vec();
    let mut incidence = vec![(0u32, 0i32); *offsets.last().unwrap()];
    for (row_id, row) in rows_columns.iter().enumerate() {
        for &(column, coefficient) in row {
            let c = column as usize;
            incidence[cursor[c]] = (row_id as u32, coefficient);
            cursor[c] += 1;
        }
    }
    drop(cursor);

    let mut active = vec![true; rows_columns.len()];
    let mut queue = VecDeque::new();
    for (column, &d) in degree.iter().enumerate() {
        if d <= 1 {
            queue.push_back(column as u32);
        }
    }
    let mut assigned = 0usize;
    let mut inconsistent = false;
    let mut boundary = None;
    let mut pivot_columns = Vec::new();
    while let Some(column) = queue.pop_front() {
        let c = column as usize;
        if degree[c] == 0 {
            if rhs[c] != 0 {
                inconsistent = true;
                boundary = Some((column_keys[c], rhs[c]));
                break;
            }
            continue;
        }
        if degree[c] != 1 {
            continue;
        }
        let (row_id, pivot_coefficient) = incidence[offsets[c]..offsets[c + 1]]
            .iter()
            .copied()
            .find(|&(row, _)| active[row as usize])
            .expect("degree-one column has one active row");
        let row_id = row_id as usize;
        let value = modp(rhs[c] as i64 * mod_pow(pivot_coefficient, P - 2) as i64);
        pivot_columns.push(column_keys[c]);
        active[row_id] = false;
        assigned += 1;
        for &(other_column, coefficient) in &rows_columns[row_id] {
            let d = other_column as usize;
            rhs[d] = modp(rhs[d] as i64 - value as i64 * coefficient as i64);
            degree[d] -= 1;
            if degree[d] <= 1 {
                queue.push_back(other_column);
            }
        }
    }
    let remaining_rows = active.iter().filter(|&&x| x).count();
    let remaining_columns = degree.iter().filter(|&&x| x > 0).count();
    let nonzero_core_rhs = degree
        .iter()
        .zip(rhs.iter())
        .filter(|(degree, rhs)| **degree > 0 && **rhs != 0)
        .count();
    (
        column_count,
        assigned,
        remaining_rows,
        remaining_columns,
        inconsistent || (remaining_rows == 0 && nonzero_core_rhs != 0),
        boundary,
        pivot_columns,
    )
}

fn cofactor_terms(
    word: &[u8; 8],
    selected: (u8, u8),
    pm8: &[Vec<(u8, u8)>],
    avoid_cap_edge: bool,
) -> Vec<Vec<u16>> {
    let mut out = Vec::new();
    for matching in pm8 {
        if !matching.contains(&selected) {
            continue;
        }
        if avoid_cap_edge && matching.contains(&(6, 7)) {
            continue;
        }
        let cells = matching
            .iter()
            .filter(|&&edge| edge != selected)
            .map(|&(u, v)| cell(u, v, word[u as usize], word[v as usize]))
            .collect::<Vec<_>>();
        assert_eq!(cells.len(), 3);
        out.push(cells);
    }
    assert_eq!(out.len(), if avoid_cap_edge { 12 } else { 15 });
    out
}

fn permutations3() -> [[usize; 3]; 6] {
    [
        [0, 1, 2],
        [0, 2, 1],
        [1, 0, 2],
        [1, 2, 0],
        [2, 0, 1],
        [2, 1, 0],
    ]
}

fn permutation_sign(p: &[usize; 3]) -> i32 {
    let mut invs = 0;
    for i in 0..3 {
        for j in i + 1..3 {
            if p[i] > p[j] {
                invs += 1;
            }
        }
    }
    if invs % 2 == 0 { 1 } else { P - 1 }
}

fn holonomy(pm8: &[Vec<(u8, u8)>], avoid_cap_edge: bool) -> Poly {
    let mut cofactors = Vec::new();
    for word in &SLICE_WORDS {
        cofactors.push(T_EDGES.map(|edge| cofactor_terms(word, edge, pm8, avoid_cap_edge)));
    }
    let mut out = Poly::new();
    for permutation in permutations3() {
        let sign = permutation_sign(&permutation);
        for a in &cofactors[0][permutation[0]] {
            for b in &cofactors[1][permutation[1]] {
                for c in &cofactors[2][permutation[2]] {
                    let mut cells = Vec::with_capacity(9);
                    cells.extend(a);
                    cells.extend(b);
                    cells.extend(c);
                    poly_add_term(&mut out, monomial(cells), sign);
                }
            }
        }
    }
    out
}

fn response_terms(edge: (u8, u8), alpha: u8, beta: u8, colour: u8) -> [Vec<u16>; 2] {
    let (a, b) = edge;
    [
        vec![cell(6, a, colour, alpha), cell(7, b, colour, beta)],
        vec![cell(6, b, colour, beta), cell(7, a, colour, alpha)],
    ]
}

fn chi_k000k111k222(pm6: &[Vec<(u8, u8)>], rrr_only: bool) -> BTreeMap<Vec<u16>, i32> {
    // Coefficient of K00*K11*K22 in the six-site cap error at ROOT_WORD[0..6].
    let mut out: BTreeMap<Vec<u16>, i32> = BTreeMap::new();
    for matching in pm6 {
        if !rrr_only {
            // s*R*R*A: choose the ordinary A edge and assign colours 0,1,2
            // bijectively to the three K-linear factors s,R,R.
            for ordinary in 0..3 {
                let response_indices = (0..3).filter(|&x| x != ordinary).collect::<Vec<_>>();
                for colour_perm in permutations3() {
                    let s_colour = colour_perm[0] as u8;
                    let r_colours = [colour_perm[1] as u8, colour_perm[2] as u8];
                    for orientations in 0..4 {
                        let mut cells = vec![cell(6, 7, s_colour, s_colour)];
                        let (u, v) = matching[ordinary];
                        cells.push(cell(u, v, ROOT_WORD[u as usize], ROOT_WORD[v as usize]));
                        for k in 0..2 {
                            let (u, v) = matching[response_indices[k]];
                            let alternatives = response_terms(
                                (u, v),
                                ROOT_WORD[u as usize],
                                ROOT_WORD[v as usize],
                                r_colours[k],
                            );
                            cells.extend(&alternatives[(orientations >> k) & 1]);
                        }
                        cells.sort_unstable();
                        *out.entry(cells).or_insert(0) += 1;
                    }
                }
            }
        }
        // R*R*R with a bijection of the three diagonal K colours.
        for colour_perm in permutations3() {
            for orientations in 0..8 {
                let mut cells = Vec::with_capacity(6);
                for k in 0..3 {
                    let (u, v) = matching[k];
                    let alternatives = response_terms(
                        (u, v),
                        ROOT_WORD[u as usize],
                        ROOT_WORD[v as usize],
                        colour_perm[k] as u8,
                    );
                    cells.extend(&alternatives[(orientations >> k) & 1]);
                }
                cells.sort_unstable();
                *out.entry(cells).or_insert(0) += 1;
            }
        }
    }
    out.retain(|_, coefficient| *coefficient != 0);
    out
}

fn triangle_localizers() -> Vec<Vec<u16>> {
    let edges = [(3u8, 4u8), (3, 5), (4, 5)];
    let mut set = BTreeSet::new();
    for choices in 0..8 {
        let mut colours: HashMap<((u8, u8), u8), u8> = HashMap::new();
        for (offset, site) in [3u8, 4, 5].into_iter().enumerate() {
            let incident = edges
                .into_iter()
                .filter(|&(u, v)| u == site || v == site)
                .collect::<Vec<_>>();
            let choice = (choices >> offset) & 1;
            colours.insert((incident[choice], site), 0);
            colours.insert((incident[1 - choice], site), 1);
        }
        let mut row = edges
            .into_iter()
            .map(|(u, v)| cell(u, v, colours[&((u, v), u)], colours[&((u, v), v)]))
            .collect::<Vec<_>>();
        row.sort_unstable();
        set.insert(row);
    }
    assert_eq!(set.len(), 8);
    set.into_iter().collect()
}

fn two_regular_graphs() -> Vec<Vec<(u8, u8)>> {
    fn rec(
        index: usize,
        remaining: usize,
        counts: &mut [u8; 10],
        degrees: &mut [u8; 5],
        out: &mut Vec<Vec<(u8, u8)>>,
    ) {
        if index == FIVE_EDGES.len() {
            if remaining == 0 && degrees.iter().all(|&d| d == 2) {
                let mut edges = Vec::new();
                for (i, &count) in counts.iter().enumerate() {
                    for _ in 0..count {
                        edges.push(FIVE_EDGES[i]);
                    }
                }
                out.push(edges);
            }
            return;
        }
        let (u, v) = FIVE_EDGES[index];
        let ui = (u - 3) as usize;
        let vi = (v - 3) as usize;
        let maximum = remaining
            .min((2 - degrees[ui]) as usize)
            .min((2 - degrees[vi]) as usize);
        for count in 0..=maximum {
            counts[index] = count as u8;
            degrees[ui] += count as u8;
            degrees[vi] += count as u8;
            rec(index + 1, remaining - count, counts, degrees, out);
            degrees[ui] -= count as u8;
            degrees[vi] -= count as u8;
        }
        counts[index] = 0;
    }
    let mut out = Vec::new();
    rec(0, 5, &mut [0; 10], &mut [0; 5], &mut out);
    assert_eq!(out.len(), 22);
    out
}

fn target_colour_counts() -> [[[u8; 3]; 8]; 1] {
    let mut target = [[[0u8; 3]; 8]; 1];
    for word in SLICE_WORDS {
        for site in 0..8 {
            target[0][site][word[site] as usize] += 1;
        }
    }
    target
}

fn multipliers_for_word(word: &[u8; 8], graphs: &[Vec<(u8, u8)>]) -> Vec<Vec<u16>> {
    let target = target_colour_counts()[0];
    let mut remaining = [[0u8; 2]; 5];
    for site in 3..8 {
        let mut colours = Vec::new();
        for colour in 0..3 {
            let used = if word[site] as usize == colour { 1 } else { 0 };
            for _ in 0..target[site][colour] - used {
                colours.push(colour as u8);
            }
        }
        assert_eq!(colours.len(), 2);
        remaining[site - 3] = [colours[0], colours[1]];
    }
    let mut set = BTreeSet::new();
    for graph in graphs {
        let mut incidences: [Vec<(usize, usize)>; 5] = std::array::from_fn(|_| Vec::new());
        for (edge_index, &(u, v)) in graph.iter().enumerate() {
            incidences[(u - 3) as usize].push((edge_index, 0));
            incidences[(v - 3) as usize].push((edge_index, 1));
        }
        assert!(incidences.iter().all(|x| x.len() == 2));
        for mask in 0..32 {
            let mut endpoint_colours = vec![[0u8; 2]; graph.len()];
            for site in 0..5 {
                let swap = (mask >> site) & 1;
                for slot in 0..2 {
                    let (edge_index, endpoint) = incidences[site][slot];
                    endpoint_colours[edge_index][endpoint] = remaining[site][slot ^ swap];
                }
            }
            let mut cells = graph
                .iter()
                .enumerate()
                .map(|(i, &(u, v))| cell(u, v, endpoint_colours[i][0], endpoint_colours[i][1]))
                .collect::<Vec<_>>();
            cells.sort_unstable();
            set.insert(cells);
        }
    }
    set.into_iter().collect()
}

#[derive(Default)]
struct UnionFind {
    parent: Vec<u32>,
    size: Vec<u32>,
}
impl UnionFind {
    fn add(&mut self) -> u32 {
        let x = self.parent.len() as u32;
        self.parent.push(x);
        self.size.push(1);
        x
    }
    fn find(&mut self, x: u32) -> u32 {
        let p = self.parent[x as usize];
        if p == x {
            x
        } else {
            let r = self.find(p);
            self.parent[x as usize] = r;
            r
        }
    }
    fn union(&mut self, a: u32, b: u32) {
        let mut x = self.find(a);
        let mut y = self.find(b);
        if x == y {
            return;
        }
        if self.size[x as usize] < self.size[y as usize] {
            std::mem::swap(&mut x, &mut y)
        }
        self.parent[y as usize] = x;
        self.size[x as usize] += self.size[y as usize];
    }
}

fn intern(key: Monomial, ids: &mut HashMap<Monomial, u32>, uf: &mut UnionFind) -> u32 {
    if let Some(&id) = ids.get(&key) {
        id
    } else {
        let id = uf.add();
        ids.insert(key, id);
        id
    }
}

fn main() {
    let pm8 = perfect_matchings(&(0..8).collect::<Vec<_>>());
    let pm6 = perfect_matchings(&(0..6).collect::<Vec<_>>());
    assert_eq!(pm8.len(), 105);
    assert_eq!(pm6.len(), 15);
    let h = holonomy(&pm8, false);
    let h_direct_free = holonomy(&pm8, true);
    let chi = chi_k000k111k222(&pm6, false);
    let chi_rrr = chi_k000k111k222(&pm6, true);
    let localizers = triangle_localizers();
    let graphs = two_regular_graphs();
    println!(
        "holonomy_terms={} direct_free_holonomy_terms={} chi_terms={} chi_rrr_terms={} localizers={} graph_types={}",
        h.len(),
        h_direct_free.len(),
        chi.len(),
        chi_rrr.len(),
        localizers.len(),
        graphs.len()
    );
    let dense = dense_values(1);
    let h_dense = evaluate_poly(&h, &dense);
    let chi_dense = evaluate_vec_poly(&chi, &dense);
    // Independent Python/w22_core replay at the same exact dense source gives
    // H=1893145593205 and chi=2578171800.
    assert_eq!(h_dense, 31_446);
    assert_eq!(chi_dense, 10_120);

    let mut pure_augmented_summaries = Vec::new();
    for pure_colour in 0..3u8 {
        let h_times_pure = multiply_by_pure(&h, &pm8, pure_colour);
        let mut support = BTreeMap::new();
        let mut first_absent = None;
        for (term, &coefficient) in &h_times_pure {
            let class = source_generator_support(term, &pm8, &chi);
            *support.entry(class).or_insert(0usize) += 1;
            if class == "absent" && first_absent.is_none() {
                first_absent = Some((
                    term.iter()
                        .map(|&id| cell_label(id))
                        .collect::<Vec<_>>()
                        .join("*"),
                    coefficient,
                ));
            }
        }
        println!(
            "h_times_pure_colour_{}_terms={} support_profile={:?}",
            pure_colour,
            h_times_pure.len(),
            support
        );
        if let Some((term, coefficient)) = &first_absent {
            println!(
                "pure_colour_{}_lex_separator={} coefficient_mod_{}={}",
                pure_colour, term, P, coefficient
            );
        }
        pure_augmented_summaries.push((h_times_pure.len(), support, first_absent));
    }
    let pure_summary_json = pure_augmented_summaries
        .iter()
        .enumerate()
        .map(|(colour, (terms, support, separator))| {
            format!(
                "    {{\"colour\": {colour}, \"terms\": {terms}, \"mixed_x5_divisor\": {mixed}, \"only_clean_error_divisor\": {clean}, \"absent_from_both\": {absent}, \"lex_separator\": \"{separator}\", \"separator_coefficient_mod_prime\": {coefficient}}}",
                mixed = support.get("mixed_x5").copied().unwrap_or(0),
                clean = support.get("clean_error").copied().unwrap_or(0),
                absent = support.get("absent").copied().unwrap_or(0),
                separator = separator.as_ref().map(|x| x.0.as_str()).unwrap_or(""),
                coefficient = separator.as_ref().map(|x| x.1).unwrap_or(0),
            )
        })
        .collect::<Vec<_>>()
        .join(",\n");

    let mut pure_matching_chart_summaries = Vec::new();
    for pure_colour in 0..3u8 {
        let mut absent_histogram = BTreeMap::new();
        let mut best: Option<(usize, usize, usize, usize, String)> = None;
        for (matching_index, matching) in pm8.iter().enumerate() {
            let profile = pure_matching_chart_profile(&h, pure_colour, matching, &pm8, &chi);
            let absent = profile.get("absent").copied().unwrap_or(0);
            let mixed = profile.get("mixed_x5").copied().unwrap_or(0);
            let clean = profile.get("clean_error").copied().unwrap_or(0);
            *absent_histogram.entry(absent).or_insert(0usize) += 1;
            let pure_word = [pure_colour; 8];
            let multiplier = matching_cells(&pure_word, matching);
            let fixed_matching_misses = h
                .keys()
                .filter(|term| {
                    let mut product = term.0.to_vec();
                    product.extend(&multiplier);
                    product.sort_unstable();
                    !has_mixed_divisor_on_matching(&product, matching)
                })
                .count();
            let candidate = (
                absent,
                fixed_matching_misses,
                matching_index,
                mixed,
                matching_label(matching),
            );
            if best.as_ref().map(|old| &candidate < old).unwrap_or(true) {
                best = Some(candidate);
            }
            assert_eq!(absent + mixed + clean, h.len());
        }
        let (best_absent, best_fixed_misses, best_matching_index, best_mixed, best_matching_label) =
            best.unwrap();
        println!(
            "pure_matching_charts_colour_{} best_absent={} best_fixed_matching_misses={} best_matching={} index={} best_mixed={} absent_histogram={:?}",
            pure_colour,
            best_absent,
            best_fixed_misses,
            best_matching_label,
            best_matching_index,
            best_mixed,
            absent_histogram
        );
        pure_matching_chart_summaries.push((
            best_absent,
            best_fixed_misses,
            best_matching_index,
            best_mixed,
            best_matching_label,
            absent_histogram,
        ));
    }
    let pure_matching_chart_json = pure_matching_chart_summaries
        .iter()
        .enumerate()
        .map(|(colour, (absent, fixed_misses, index, mixed, label, histogram))| {
            let histogram_json = histogram
                .iter()
                .map(|(count, multiplicity)| format!("\"{count}\": {multiplicity}"))
                .collect::<Vec<_>>()
                .join(", ");
            format!(
                "    {{\"colour\": {colour}, \"best_absent\": {absent}, \"best_fixed_matching_misses\": {fixed_misses}, \"best_matching_index\": {index}, \"best_matching\": \"{label}\", \"best_mixed_x5_divisor\": {mixed}, \"absent_histogram\": {{{histogram_json}}}}}"
            )
        })
        .collect::<Vec<_>>()
        .join(",\n");

    // Bounded Groebner-cone screen on the common chart M=01|23|45|67,
    // colour zero.  A target term is covered when it contains the leading
    // matching monomial of some mixed X5 word under the sampled cell weight.
    let cone_matching = &pm8[0];
    let cone_multiplier = matching_cells(&[0u8; 8], cone_matching);
    let cone_candidates = h
        .keys()
        .map(|term| {
            let mut product = term.0.to_vec();
            product.extend(&cone_multiplier);
            product.sort_unstable();
            divisor_candidates(&product, &pm8)
        })
        .collect::<Vec<_>>();
    assert!(cone_candidates.iter().all(|candidates| !candidates.is_empty()));
    let candidate_histogram = cone_candidates.iter().fold(BTreeMap::new(), |mut map, row| {
        *map.entry(row.len()).or_insert(0usize) += 1;
        map
    });
    let mut singleton_requirements: BTreeMap<u16, BTreeMap<u8, usize>> = BTreeMap::new();
    for candidates in &cone_candidates {
        if candidates.len() == 1 {
            let (word, matching) = candidates[0];
            *singleton_requirements
                .entry(word)
                .or_default()
                .entry(matching)
                .or_insert(0) += 1;
        }
    }
    let singleton_conflicting_words = singleton_requirements
        .values()
        .filter(|requirements| requirements.len() > 1)
        .count();
    let singleton_forced_misses = singleton_requirements
        .values()
        .map(|requirements| {
            requirements.values().sum::<usize>()
                - requirements.values().copied().max().unwrap_or(0)
        })
        .sum::<usize>();
    let singleton_conflict_example = singleton_requirements
        .iter()
        .find(|(_, requirements)| requirements.len() > 1)
        .map(|(word, requirements)| format!("word_code={word},requirements={requirements:?}"))
        .unwrap_or_default();
    let singleton_conflict_ledger = singleton_requirements
        .iter()
        .filter(|(_, requirements)| requirements.len() > 1)
        .map(|(word, requirements)| {
            format!(
                "{}:{requirements:?}",
                decode_word(*word as usize)
                    .iter()
                    .map(|x| char::from(b'0' + *x))
                    .collect::<String>()
            )
        })
        .collect::<Vec<_>>()
        .join(";");
    let mut first_exchange_rows = BTreeSet::new();
    for ((term, _), candidates) in h.iter().zip(cone_candidates.iter()) {
        let mut product = term.0.to_vec();
        product.extend(&cone_multiplier);
        product.sort_unstable();
        for &(code, matching_index) in candidates {
            let word = decode_word(code as usize);
            let divisor = matching_cells(&word, &pm8[matching_index as usize]);
            let quotient = quotient_monomial(&product, &divisor);
            first_exchange_rows.insert((code, quotient));
        }
    }
    let empty_clean_quotients = BTreeSet::new();
    let (
        first_exchange_columns,
        first_exchange_assigned_rows,
        first_exchange_core_rows,
        first_exchange_core_columns,
        first_exchange_inconsistent,
        first_exchange_boundary,
        first_exchange_pivots,
    ) = peel_first_exchange(
        &h,
        &cone_multiplier,
        &first_exchange_rows,
        &empty_clean_quotients,
        &chi,
        &pm8,
    );
    let first_exchange_boundary_label = first_exchange_boundary
        .as_ref()
        .map(|(term, coefficient)| {
            format!(
                "{};coefficient={coefficient}",
                term.0
                    .iter()
                    .map(|&id| cell_label(id))
                    .collect::<Vec<_>>()
                    .join("*")
            )
        })
        .unwrap_or_default();
    let first_exchange_boundary_candidates = first_exchange_boundary
        .as_ref()
        .map(|(term, _)| divisor_candidates(&term.0, &pm8))
        .unwrap_or_default();
    let first_exchange_new_boundary_rows = first_exchange_boundary_candidates
        .iter()
        .filter(|&&(code, matching_index)| {
            let word = decode_word(code as usize);
            let divisor = matching_cells(&word, &pm8[matching_index as usize]);
            let quotient = quotient_monomial(
                &first_exchange_boundary.as_ref().unwrap().0.0,
                &divisor,
            );
            !first_exchange_rows.contains(&(code, quotient))
        })
        .count();
    let mut first_clean_error_quotients = BTreeSet::new();
    for pivot in first_exchange_pivots
        .iter()
        .chain(first_exchange_boundary.as_ref().map(|x| &x.0))
    {
        for divisor in chi.keys() {
            if let Some(quotient) = multiset_quotient(&pivot.0, divisor) {
                first_clean_error_quotients.insert(quotient);
            }
        }
    }

    // Exact physical-multigraph quotient of the first exchange.  Word and
    // endpoint-colour decorations are forgotten only after the literal row
    // set has been constructed.  Rows with the same quotient graph then
    // become identical, giving a small necessary quotient-membership test.
    let matching_graphs = pm8
        .iter()
        .map(|matching| physical_graph(&matching_cells(&[0u8; 8], matching)))
        .collect::<Vec<_>>();
    let x5_quotient_graphs = first_exchange_rows
        .iter()
        .map(|(_, quotient)| physical_graph(&quotient.0))
        .collect::<BTreeSet<_>>();
    let clean_quotient_graphs = first_clean_error_quotients
        .iter()
        .map(|quotient| physical_graph(quotient))
        .collect::<BTreeSet<_>>();
    let mut projected_rows = Vec::new();
    for quotient in &x5_quotient_graphs {
        let mut row = BTreeMap::new();
        for &matching in &matching_graphs {
            graph_row_add(&mut row, graph_add(*quotient, matching), 1);
        }
        projected_rows.push(row);
    }
    for quotient in &clean_quotient_graphs {
        let mut row = BTreeMap::new();
        for (term, &coefficient) in &chi {
            graph_row_add(
                &mut row,
                graph_add(*quotient, physical_graph(term)),
                coefficient,
            );
        }
        projected_rows.push(row);
    }
    let projected_basis = graph_row_basis(projected_rows);
    let cone_graph = physical_graph(&cone_multiplier);
    let mut projected_target = BTreeMap::new();
    for (term, &coefficient) in &h {
        graph_row_add(
            &mut projected_target,
            graph_add(cone_graph, physical_graph(&term.0)),
            coefficient,
        );
    }
    let projected_target_terms = projected_target.len();
    let projected_remainder = graph_row_reduce(projected_target, &projected_basis);
    println!(
        "physical_graph_exchange_x5_quotients={} clean_quotients={} rank={} target_terms={} remainder_terms={}",
        x5_quotient_graphs.len(),
        clean_quotient_graphs.len(),
        projected_basis.len(),
        projected_target_terms,
        projected_remainder.len(),
    );
    let mut second_exchange_rows = first_exchange_rows.clone();
    let second_clean_quotients = first_clean_error_quotients.clone();
    let mut first_closure_columns = first_exchange_pivots.clone();
    if let Some((boundary, _)) = &first_exchange_boundary {
        first_closure_columns.push(*boundary);
    }
    for boundary in &first_closure_columns {
        for (code, matching_index) in divisor_candidates(&boundary.0, &pm8) {
            let word = decode_word(code as usize);
            let divisor = matching_cells(&word, &pm8[matching_index as usize]);
            second_exchange_rows.insert((code, quotient_monomial(&boundary.0, &divisor)));
        }
    }
    let (
        second_exchange_columns,
        second_exchange_assigned_rows,
        second_exchange_core_rows,
        second_exchange_core_columns,
        second_exchange_inconsistent,
        second_exchange_boundary,
        second_exchange_pivots,
    ) = peel_first_exchange(
        &h,
        &cone_multiplier,
        &second_exchange_rows,
        &second_clean_quotients,
        &chi,
        &pm8,
    );
    let second_exchange_boundary_label = second_exchange_boundary
        .as_ref()
        .map(|(term, coefficient)| {
            format!(
                "{};coefficient={coefficient}",
                term.0
                    .iter()
                    .map(|&id| cell_label(id))
                    .collect::<Vec<_>>()
                    .join("*")
            )
        })
        .unwrap_or_default();
    let second_exchange_boundary_candidates = second_exchange_boundary
        .as_ref()
        .map(|(term, _)| divisor_candidates(&term.0, &pm8))
        .unwrap_or_default();
    let mut iterative_exchange_rows = second_exchange_rows.clone();
    let mut iterative_clean_quotients = second_clean_quotients;
    let mut iterative_boundary = second_exchange_boundary;
    let mut iterative_pivots = second_exchange_pivots;
    let mut iterative_exchange_ledger = Vec::new();
    let exchange_iteration_cap = std::env::var("KRENN_EXCHANGE_CAP")
        .ok()
        .and_then(|value| value.parse::<usize>().ok())
        .unwrap_or(64);
    for iteration in 2..exchange_iteration_cap {
        let mut added = 0usize;
        let mut closure_columns = std::mem::take(&mut iterative_pivots);
        if let Some((boundary, _)) = &iterative_boundary {
            closure_columns.push(*boundary);
        }
        for boundary in &closure_columns {
            for (code, matching_index) in divisor_candidates(&boundary.0, &pm8) {
                let word = decode_word(code as usize);
                let divisor = matching_cells(&word, &pm8[matching_index as usize]);
                if iterative_exchange_rows.insert((
                    code,
                    quotient_monomial(&boundary.0, &divisor),
                )) {
                    added += 1;
                }
            }
            for divisor in chi.keys() {
                if let Some(quotient) = multiset_quotient(&boundary.0, divisor) {
                    if iterative_clean_quotients.insert(quotient) {
                        added += 1;
                    }
                }
            }
        }
        if added == 0 {
            iterative_exchange_ledger.push(format!("{iteration}:no-new-row"));
            break;
        }
        let (columns, assigned, core_rows, core_columns, inconsistent, boundary, pivots) =
            peel_first_exchange(
                &h,
                &cone_multiplier,
                &iterative_exchange_rows,
                &iterative_clean_quotients,
                &chi,
                &pm8,
            );
        let candidates = boundary
            .as_ref()
            .map(|(term, _)| divisor_candidates(&term.0, &pm8).len())
            .unwrap_or(0);
        println!(
            "exchange_iteration={} added={} x5_rows={} clean_rows={} columns={} leaf_assigned={} core_rows={} core_columns={} inconsistent={} next_candidates={}",
            iteration,
            added,
            iterative_exchange_rows.len(),
            iterative_clean_quotients.len(),
            columns,
            assigned,
            core_rows,
            core_columns,
            inconsistent,
            candidates,
        );
        iterative_exchange_ledger.push(format!(
            "{iteration}:added={added},x5_rows={},clean_rows={},columns={columns},assigned={assigned},core_rows={core_rows},core_columns={core_columns},inconsistent={inconsistent},next_candidates={candidates}",
            iterative_exchange_rows.len(),
            iterative_clean_quotients.len()
        ));
        iterative_boundary = boundary;
        iterative_pivots = pivots;
        if !inconsistent {
            break;
        }
    }
    let iterative_exchange_ledger = iterative_exchange_ledger.join(";");
    let mut random_state = 0x9e3779b97f4a7c15u64;
    let mut best_cone_uncovered = h.len();
    let mut best_cone_trial = 0usize;
    for trial in 0..256usize {
        let mut weights = [0i64; 252];
        for weight in &mut weights {
            *weight = (xorshift64(&mut random_state) & 0x7fff_ffff) as i64;
        }
        let leading = leading_matchings(&weights, &pm8);
        let uncovered = cone_candidates
            .iter()
            .filter(|candidates| {
                !candidates
                    .iter()
                    .any(|&(code, matching)| leading[code as usize] == matching)
            })
            .count();
        if uncovered < best_cone_uncovered {
            best_cone_uncovered = uncovered;
            best_cone_trial = trial;
        }
    }
    println!(
        "bounded_groebner_cone_trials=256 best_uncovered={} best_trial={} divisor_candidate_histogram={:?}",
        best_cone_uncovered, best_cone_trial, candidate_histogram
    );
    println!(
        "second_exchange_rows={} columns={} leaf_assigned={} core_rows={} core_columns={} inconsistent={} boundary_candidates={} boundary={}",
        second_exchange_rows.len(),
        second_exchange_columns,
        second_exchange_assigned_rows,
        second_exchange_core_rows,
        second_exchange_core_columns,
        second_exchange_inconsistent,
        second_exchange_boundary_candidates.len(),
        second_exchange_boundary_label,
    );
    println!("iterative_exchange_ledger={}", iterative_exchange_ledger);
    println!(
        "singleton_required_words={} singleton_conflicting_words={} singleton_forced_misses={} conflict_example={}",
        singleton_requirements.len(),
        singleton_conflicting_words,
        singleton_forced_misses,
        singleton_conflict_example
    );
    println!(
        "singleton_conflict_ledger={} first_exchange_rows={} columns={} leaf_assigned={} core_rows={} core_columns={} inconsistent={} boundary_candidates={} new_boundary_rows={} boundary={}",
        singleton_conflict_ledger,
        first_exchange_rows.len(),
        first_exchange_columns,
        first_exchange_assigned_rows,
        first_exchange_core_rows,
        first_exchange_core_columns,
        first_exchange_inconsistent,
        first_exchange_boundary_candidates.len(),
        first_exchange_new_boundary_rows,
        first_exchange_boundary_label,
    );
    println!(
        "first_forced_columns_clean_error_quotients={}",
        first_clean_error_quotients.len()
    );
    println!(
        "first_forced_clean_quotient_labels={}",
        first_clean_error_quotients
            .iter()
            .map(|quotient| quotient.iter().map(|&id| cell_label(id)).collect::<Vec<_>>().join("*"))
            .collect::<Vec<_>>()
            .join(";")
    );

    let target = target_colour_counts()[0];
    let mut words = Vec::new();
    for a3 in 0..3u8 {
        for a4 in 0..3u8 {
            for a5 in 0..3u8 {
                for a6 in 0..3u8 {
                    for a7 in 0..3u8 {
                        let word = [0, 1, 2, a3, a4, a5, a6, a7];
                        if (3..8).all(|site| target[site][word[site] as usize] > 0) {
                            words.push(word)
                        }
                    }
                }
            }
        }
    }
    assert_eq!(words.len(), 108);

    let mut ids = HashMap::new();
    let mut uf = UnionFind::default();
    let mut rows: Vec<Vec<(u32, i32)>> = Vec::new();
    let mut multiplier_count = 0usize;
    for word in &words {
        let multipliers = multipliers_for_word(word, &graphs);
        multiplier_count += multipliers.len();
        for multiplier in multipliers {
            let mut row = Vec::with_capacity(105);
            for matching in &pm8 {
                let mut cells = matching_cells(word, matching);
                cells.extend(&multiplier);
                let id = intern(monomial(cells), &mut ids, &mut uf);
                row.push((id, 1));
            }
            row.sort_unstable_by_key(|x| x.0);
            row.dedup_by(|a, b| {
                if a.0 == b.0 {
                    a.1 = modp(a.1 as i64 + b.1 as i64);
                    true
                } else {
                    false
                }
            });
            let first = row[0].0;
            for &(id, _) in &row[1..] {
                uf.union(first, id)
            }
            rows.push(row);
        }
    }
    let x5_rows = rows.len();
    let mut chi_rows = Vec::new();
    let mut chi_rrr_rows = Vec::new();
    for localizer in &localizers {
        let mut row = Vec::new();
        for (term, &coefficient) in &chi {
            let mut cells = term.clone();
            cells.extend(localizer);
            let id = intern(monomial(cells), &mut ids, &mut uf);
            row.push((id, modp(coefficient as i64)));
        }
        row.sort_unstable_by_key(|x| x.0);
        let first = row[0].0;
        for &(id, _) in &row[1..] {
            uf.union(first, id)
        }
        chi_rows.push(row);

        let mut rrr_row = Vec::new();
        for (term, &coefficient) in &chi_rrr {
            let mut cells = term.clone();
            cells.extend(localizer);
            let id = intern(monomial(cells), &mut ids, &mut uf);
            rrr_row.push((id, modp(coefficient as i64)));
        }
        rrr_row.sort_unstable_by_key(|x| x.0);
        let first = rrr_row[0].0;
        for &(id, _) in &rrr_row[1..] {
            uf.union(first, id)
        }
        chi_rrr_rows.push(rrr_row);
    }
    let mut hrow = Vec::new();
    for (&term, &coefficient) in &h {
        let id = intern(term, &mut ids, &mut uf);
        hrow.push((id, coefficient));
    }
    hrow.sort_unstable_by_key(|x| x.0);
    let first = hrow[0].0;
    for &(id, _) in &hrow[1..] {
        uf.union(first, id)
    }
    let mut h_direct_free_row = Vec::new();
    for (&term, &coefficient) in &h_direct_free {
        let id = intern(term, &mut ids, &mut uf);
        h_direct_free_row.push((id, coefficient));
    }
    h_direct_free_row.sort_unstable_by_key(|x| x.0);
    let first = h_direct_free_row[0].0;
    for &(id, _) in &h_direct_free_row[1..] {
        uf.union(first, id)
    }

    let mut component_columns: HashMap<u32, usize> = HashMap::new();
    for id in 0..uf.parent.len() as u32 {
        let root = uf.find(id);
        *component_columns.entry(root).or_insert(0) += 1;
    }
    let mut component_rows: HashMap<u32, usize> = HashMap::new();
    for row in rows
        .iter()
        .chain(chi_rows.iter())
        .chain(chi_rrr_rows.iter())
    {
        let root = uf.find(row[0].0);
        *component_rows.entry(root).or_insert(0) += 1;
    }
    let mut target_roots = BTreeSet::new();
    for &(id, _) in &hrow {
        target_roots.insert(uf.find(id));
    }
    let mut target_profiles = target_roots
        .iter()
        .map(|root| {
            (
                *component_columns.get(root).unwrap_or(&0),
                *component_rows.get(root).unwrap_or(&0),
            )
        })
        .collect::<Vec<_>>();
    target_profiles.sort_unstable();
    let largest = component_columns.values().copied().max().unwrap_or(0);
    println!(
        "words={} multipliers={} x5_rows={} columns={} components={} largest_component={}",
        words.len(),
        multiplier_count,
        x5_rows,
        ids.len(),
        component_columns.len(),
        largest
    );
    println!(
        "target_components={} target_profiles={:?}",
        target_roots.len(),
        target_profiles
    );

    // Fast exact obstruction: any target component with more columns than rows
    // is not automatically an obstruction, but a singleton target monomial in
    // no source row is a literal separating functional.
    let covered: BTreeSet<u32> = rows
        .iter()
        .chain(chi_rows.iter())
        .flat_map(|row| row.iter().map(|x| x.0))
        .collect();
    let covered_direct_free: BTreeSet<u32> = rows
        .iter()
        .chain(chi_rrr_rows.iter())
        .flat_map(|row| row.iter().map(|x| x.0))
        .collect();
    let chi_only: BTreeSet<u32> = chi_rows
        .iter()
        .flat_map(|row| row.iter().map(|x| x.0))
        .collect();
    let chi_rrr_only: BTreeSet<u32> = chi_rrr_rows
        .iter()
        .flat_map(|row| row.iter().map(|x| x.0))
        .collect();
    let h_chi_overlap = hrow
        .iter()
        .filter(|&&(id, _)| chi_only.contains(&id))
        .count();
    let direct_free_h_rrr_overlap = h_direct_free_row
        .iter()
        .filter(|&&(id, _)| chi_rrr_only.contains(&id))
        .count();
    let uncovered = hrow
        .iter()
        .filter(|&&(id, _)| !covered.contains(&id))
        .count();
    let uncovered_direct_free = h_direct_free_row
        .iter()
        .filter(|&&(id, _)| !covered_direct_free.contains(&id))
        .count();
    let (separator, separator_coefficient) = h
        .iter()
        .find(|(term, _)| !covered.contains(ids.get(term).unwrap()))
        .expect("the frozen separator vanished");
    let (direct_free_separator, direct_free_separator_coefficient) = h_direct_free
        .iter()
        .find(|(term, _)| !covered_direct_free.contains(ids.get(term).unwrap()))
        .expect("the frozen direct-free separator vanished");
    let separator_label = separator
        .0
        .iter()
        .map(|&id| cell_label(id))
        .collect::<Vec<_>>()
        .join("*");
    let direct_free_separator_label = direct_free_separator
        .0
        .iter()
        .map(|&id| cell_label(id))
        .collect::<Vec<_>>()
        .join("*");
    println!(
        "h_terms={} chi_rows={} h_terms_absent_from_all_generators={}",
        hrow.len(),
        chi_rows.len(),
        uncovered
    );
    println!(
        "direct_free_h_terms={} chi_rrr_rows={} direct_free_h_terms_absent_from_all_generators={}",
        h_direct_free_row.len(),
        chi_rrr_rows.len(),
        uncovered_direct_free
    );
    println!(
        "holonomy_terms_in_clean_error_support={} direct_free_holonomy_terms_in_rrr_support={}",
        h_chi_overlap, direct_free_h_rrr_overlap
    );
    println!(
        "direct_free_lex_separator={} coefficient_mod_{}={}",
        direct_free_separator_label, P, direct_free_separator_coefficient
    );
    println!(
        "lex_separator={} coefficient_mod_{}={}",
        separator_label, P, separator_coefficient
    );
    assert_eq!(h.len(), 18_630);
    assert_eq!(chi.len(), 1_800);
    assert_eq!(multiplier_count, 33_156);
    assert_eq!(ids.len(), 2_083_914);
    assert_eq!(uncovered, 11_790);

    let result = format!(
        concat!(
            "{{\n",
            "  \"status\": \"PASS bounded exact source-graded obstruction; iterative closure nonterminal\",\n",
            "  \"prime\": {prime},\n",
            "  \"root_word\": \"01211222\",\n",
            "  \"holonomy_terms\": {h_terms},\n",
            "  \"direct_free_holonomy_terms\": {h_direct_free_terms},\n",
            "  \"polarized_clean_error_terms\": {chi_terms},\n",
            "  \"polarized_rrr_terms\": {chi_rrr_terms},\n",
            "  \"pure_anchor_summaries\": [\n{pure_summary_json}\n  ],\n",
            "  \"pure_matching_chart_summaries\": [\n{pure_matching_chart_json}\n  ],\n",
            "  \"bounded_groebner_cone_trials\": 256,\n",
            "  \"bounded_groebner_cone_best_uncovered\": {best_cone_uncovered},\n",
            "  \"singleton_required_words\": {singleton_required_words},\n",
            "  \"singleton_conflicting_words\": {singleton_conflicting_words},\n",
            "  \"singleton_forced_misses\": {singleton_forced_misses},\n",
            "  \"singleton_conflict_example\": \"{singleton_conflict_example}\",\n",
            "  \"singleton_conflict_ledger\": \"{singleton_conflict_ledger}\",\n",
            "  \"first_exchange_rows\": {first_exchange_rows},\n",
            "  \"first_exchange_columns\": {first_exchange_columns},\n",
            "  \"first_exchange_leaf_assigned_rows\": {first_exchange_assigned_rows},\n",
            "  \"first_exchange_core_rows\": {first_exchange_core_rows},\n",
            "  \"first_exchange_core_columns\": {first_exchange_core_columns},\n",
            "  \"first_exchange_inconsistent\": {first_exchange_inconsistent},\n",
            "  \"first_exchange_boundary_candidates\": {first_exchange_boundary_candidates},\n",
            "  \"first_exchange_new_boundary_rows\": {first_exchange_new_boundary_rows},\n",
            "  \"first_exchange_boundary\": \"{first_exchange_boundary_label}\",\n",
            "  \"first_forced_columns_clean_error_quotients\": {first_clean_error_quotients},\n",
            "  \"physical_graph_exchange_x5_quotients\": {physical_graph_exchange_x5_quotients},\n",
            "  \"physical_graph_exchange_clean_quotients\": {physical_graph_exchange_clean_quotients},\n",
            "  \"physical_graph_exchange_rank\": {physical_graph_exchange_rank},\n",
            "  \"physical_graph_exchange_target_terms\": {physical_graph_exchange_target_terms},\n",
            "  \"physical_graph_exchange_remainder_terms\": {physical_graph_exchange_remainder_terms},\n",
            "  \"iterative_exchange_cap\": {exchange_iteration_cap},\n",
            "  \"iterative_exchange_ledger\": \"{iterative_exchange_ledger}\",\n",
            "  \"triangle_localizers\": 8,\n",
            "  \"compatible_x5_words\": 108,\n",
            "  \"compatible_macaulay_multipliers\": {multipliers},\n",
            "  \"macaulay_rows\": {rows},\n",
            "  \"monomial_columns\": {columns},\n",
            "  \"holonomy_terms_absent_from_all_generators\": {uncovered},\n",
            "  \"direct_free_holonomy_terms_absent_from_mixed_x5_and_rrr_generators\": {uncovered_direct_free},\n",
            "  \"holonomy_terms_in_clean_error_support\": {h_chi_overlap},\n",
            "  \"direct_free_holonomy_terms_in_rrr_support\": {direct_free_h_rrr_overlap},\n",
            "  \"lex_separator\": \"{separator}\",\n",
            "  \"lex_separator_coefficient_mod_prime\": {coefficient},\n",
            "  \"direct_free_lex_separator\": \"{direct_free_separator}\",\n",
            "  \"direct_free_lex_separator_coefficient_mod_prime\": {direct_free_coefficient},\n",
            "  \"dense_control_h_mod_prime\": {h_dense},\n",
            "  \"dense_control_chi_mod_prime\": {chi_dense},\n",
            "  \"scope\": \"Mixed-X5 degree-nine block plus all eight source monomial localizers of the K00*K11*K22 clean-error coefficient. The one-pure-anchor, pure-matching-chart, bounded term-order, and 63-stage source-labelled exchange screens are exact in their stated finite blocks. The exchange closure remains nonterminal: this is neither ideal nonmembership nor a global triangle-branch proof. Multiple pure anchors, unrestricted higher localized degrees, and adjacent full-nine comparison data are not included.\"\n",
            "}}\n"
        ),
        prime = P,
        h_terms = h.len(),
        h_direct_free_terms = h_direct_free.len(),
        chi_terms = chi.len(),
        chi_rrr_terms = chi_rrr.len(),
        pure_summary_json = pure_summary_json,
        pure_matching_chart_json = pure_matching_chart_json,
        best_cone_uncovered = best_cone_uncovered,
        singleton_required_words = singleton_requirements.len(),
        singleton_conflicting_words = singleton_conflicting_words,
        singleton_forced_misses = singleton_forced_misses,
        singleton_conflict_example = singleton_conflict_example,
        singleton_conflict_ledger = singleton_conflict_ledger,
        first_exchange_rows = first_exchange_rows.len(),
        first_exchange_columns = first_exchange_columns,
        first_exchange_assigned_rows = first_exchange_assigned_rows,
        first_exchange_core_rows = first_exchange_core_rows,
        first_exchange_core_columns = first_exchange_core_columns,
        first_exchange_inconsistent = first_exchange_inconsistent,
        first_exchange_boundary_candidates = first_exchange_boundary_candidates.len(),
        first_exchange_new_boundary_rows = first_exchange_new_boundary_rows,
        first_exchange_boundary_label = first_exchange_boundary_label,
        first_clean_error_quotients = first_clean_error_quotients.len(),
        physical_graph_exchange_x5_quotients = x5_quotient_graphs.len(),
        physical_graph_exchange_clean_quotients = clean_quotient_graphs.len(),
        physical_graph_exchange_rank = projected_basis.len(),
        physical_graph_exchange_target_terms = projected_target_terms,
        physical_graph_exchange_remainder_terms = projected_remainder.len(),
        exchange_iteration_cap = exchange_iteration_cap,
        iterative_exchange_ledger = iterative_exchange_ledger,
        multipliers = multiplier_count,
        rows = x5_rows,
        columns = ids.len(),
        uncovered = uncovered,
        uncovered_direct_free = uncovered_direct_free,
        h_chi_overlap = h_chi_overlap,
        direct_free_h_rrr_overlap = direct_free_h_rrr_overlap,
        separator = separator_label,
        coefficient = separator_coefficient,
        direct_free_separator = direct_free_separator_label,
        direct_free_coefficient = direct_free_separator_coefficient,
        h_dense = h_dense,
        chi_dense = chi_dense,
    );
    let result_path = std::env::var("KRENN_RESULT_PATH").unwrap_or_else(|_| {
        "computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/results_rootless_fine_macaulay.json".to_string()
    });
    fs::write(result_path, result)
    .expect("write result");
}
