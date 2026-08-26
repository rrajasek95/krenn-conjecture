use std::collections::BTreeMap;
use std::env;
use std::fs;
use std::time::Instant;

const N: usize = 8;
const Q: usize = 3;

#[derive(Clone)]
struct Source {
    name: String,
    cells: [u32; 252],
}

fn edge_index(u: usize, v: usize) -> usize {
    assert!(u < v);
    let before = u * (2 * N - u - 1) / 2;
    before + (v - u - 1)
}

fn cell(source: &Source, u: usize, v: usize, a: usize, b: usize) -> u32 {
    if u < v {
        source.cells[9 * edge_index(u, v) + 3 * a + b]
    } else {
        source.cells[9 * edge_index(v, u) + 3 * b + a]
    }
}

fn mod_pow(mut base: u32, mut exponent: u32, prime: u32) -> u32 {
    let mut answer = 1u32;
    while exponent > 0 {
        if exponent & 1 == 1 {
            answer = ((answer as u64 * base as u64) % prime as u64) as u32;
        }
        base = ((base as u64 * base as u64) % prime as u64) as u32;
        exponent >>= 1;
    }
    answer
}

fn rank(columns: &[Vec<u32>], prime: u32) -> usize {
    let height = columns.first().map_or(0, Vec::len);
    let mut basis: Vec<Option<Vec<u32>>> = vec![None; height];
    let mut answer = 0usize;
    for input in columns {
        let mut vector = input.clone();
        loop {
            let pivot = vector.iter().position(|&x| x != 0);
            let Some(pivot) = pivot else { break };
            if let Some(row) = &basis[pivot] {
                let scale = vector[pivot];
                for index in pivot..height {
                    let subtract = (scale as u64 * row[index] as u64) % prime as u64;
                    vector[index] =
                        ((vector[index] as u64 + prime as u64 - subtract) % prime as u64) as u32;
                }
            } else {
                let inverse = mod_pow(vector[pivot], prime - 2, prime);
                for value in &mut vector[pivot..] {
                    *value = ((*value as u64 * inverse as u64) % prime as u64) as u32;
                }
                basis[pivot] = Some(vector);
                answer += 1;
                break;
            }
        }
    }
    answer
}

fn row_nullspace(rows: &[Vec<u32>], width: usize, prime: u32) -> Vec<Vec<u32>> {
    let mut matrix = rows.to_vec();
    assert!(matrix.iter().all(|row| row.len() == width));
    let mut pivot_row = 0usize;
    let mut pivot_columns = Vec::new();
    for column in 0..width {
        let Some(found) = (pivot_row..matrix.len()).find(|&row| matrix[row][column] != 0) else {
            continue;
        };
        matrix.swap(pivot_row, found);
        let inverse = mod_pow(matrix[pivot_row][column], prime - 2, prime);
        for value in &mut matrix[pivot_row][column..] {
            *value = ((*value as u64 * inverse as u64) % prime as u64) as u32;
        }
        for row in 0..matrix.len() {
            if row == pivot_row || matrix[row][column] == 0 {
                continue;
            }
            let scale = matrix[row][column];
            for index in column..width {
                let subtract = (scale as u64 * matrix[pivot_row][index] as u64) % prime as u64;
                matrix[row][index] =
                    ((matrix[row][index] as u64 + prime as u64 - subtract) % prime as u64) as u32;
            }
        }
        pivot_columns.push(column);
        pivot_row += 1;
        if pivot_row == matrix.len() {
            break;
        }
    }
    let free_columns: Vec<usize> = (0..width)
        .filter(|column| !pivot_columns.contains(column))
        .collect();
    free_columns
        .into_iter()
        .map(|free| {
            let mut vector = vec![0u32; width];
            vector[free] = 1;
            for (row, &pivot) in pivot_columns.iter().enumerate().rev() {
                vector[pivot] = if matrix[row][free] == 0 {
                    0
                } else {
                    prime - matrix[row][free]
                };
            }
            assert!(rows.iter().all(|row| {
                row.iter()
                    .zip(&vector)
                    .map(|(&a, &b)| a as u64 * b as u64)
                    .sum::<u64>()
                    % prime as u64
                    == 0
            }));
            vector
        })
        .collect()
}

fn normalized_column_basis(columns: &[Vec<u32>], prime: u32) -> Vec<Option<Vec<u32>>> {
    let height = columns.first().map_or(0, Vec::len);
    let mut basis: Vec<Option<Vec<u32>>> = vec![None; height];
    for input in columns {
        let mut vector = input.clone();
        loop {
            let pivot = vector.iter().position(|&x| x != 0);
            let Some(pivot) = pivot else { break };
            if let Some(row) = &basis[pivot] {
                let scale = vector[pivot];
                for index in pivot..height {
                    let subtract = (scale as u64 * row[index] as u64) % prime as u64;
                    vector[index] =
                        ((vector[index] as u64 + prime as u64 - subtract) % prime as u64) as u32;
                }
            } else {
                let inverse = mod_pow(vector[pivot], prime - 2, prime);
                for value in &mut vector[pivot..] {
                    *value = ((*value as u64 * inverse as u64) % prime as u64) as u32;
                }
                basis[pivot] = Some(vector);
                break;
            }
        }
    }
    basis
}

fn reduce_column(mut vector: Vec<u32>, basis: &[Option<Vec<u32>>], prime: u32) -> Vec<u32> {
    loop {
        let pivot = vector.iter().position(|&x| x != 0);
        let Some(pivot) = pivot else { break };
        let Some(row) = &basis[pivot] else { break };
        let scale = vector[pivot];
        for index in pivot..vector.len() {
            let subtract = (scale as u64 * row[index] as u64) % prime as u64;
            vector[index] =
                ((vector[index] as u64 + prime as u64 - subtract) % prime as u64) as u32;
        }
    }
    vector
}

fn assignments(count: usize) -> Vec<Vec<usize>> {
    let total = Q.pow(count as u32);
    (0..total)
        .map(|mut code| {
            let mut word = vec![0usize; count];
            for slot in (0..count).rev() {
                word[slot] = code % Q;
                code /= Q;
            }
            word
        })
        .collect()
}

fn matchings(vertices: &[usize]) -> Vec<Vec<(usize, usize)>> {
    if vertices.is_empty() {
        return vec![Vec::new()];
    }
    let first = vertices[0];
    let mut answer = Vec::new();
    for position in 1..vertices.len() {
        let second = vertices[position];
        let mut rest = vertices[1..position].to_vec();
        rest.extend_from_slice(&vertices[position + 1..]);
        for mut tail in matchings(&rest) {
            let mut row = vec![(first, second)];
            row.append(&mut tail);
            answer.push(row);
        }
    }
    answer
}

fn hafnian_tensor(source: &Source, vertices: &[usize], prime: u32) -> Vec<u32> {
    let words = assignments(vertices.len());
    let perfect = matchings(vertices);
    words
        .iter()
        .map(|word| {
            let mut sum = 0u64;
            for matching in &perfect {
                let mut product = 1u64;
                for &(u, v) in matching {
                    let iu = vertices.iter().position(|&x| x == u).unwrap();
                    let iv = vertices.iter().position(|&x| x == v).unwrap();
                    product =
                        product * cell(source, u, v, word[iu], word[iv]) as u64 % prime as u64;
                }
                sum = (sum + product) % prime as u64;
            }
            sum as u32
        })
        .collect()
}

fn word_index(word: &[usize]) -> usize {
    word.iter().fold(0usize, |acc, &colour| 3 * acc + colour)
}

fn permutations(values: &[usize]) -> Vec<Vec<usize>> {
    if values.is_empty() {
        return vec![Vec::new()];
    }
    let mut answer = Vec::new();
    for (index, &first) in values.iter().enumerate() {
        let mut rest = values.to_vec();
        rest.remove(index);
        for tail in permutations(&rest) {
            let mut row = vec![first];
            row.extend_from_slice(&tail);
            answer.push(row);
        }
    }
    answer
}

fn endpoint_linear_form(
    source: &Source,
    endpoint: usize,
    residual: &[usize],
    endpoint_colour: usize,
) -> Vec<[u32; 3]> {
    residual
        .iter()
        .map(|&site| {
            [
                cell(source, endpoint, site, endpoint_colour, 0),
                cell(source, endpoint, site, endpoint_colour, 1),
                cell(source, endpoint, site, endpoint_colour, 2),
            ]
        })
        .collect()
}

fn four_linear_product(forms: [&Vec<[u32; 3]>; 4], prime: u32) -> Vec<u32> {
    let site_subsets = combinations(&(0..6).collect::<Vec<_>>(), 4);
    let words = assignments(4);
    let form_permutations = permutations(&[0, 1, 2, 3]);
    let mut column = vec![0u32; 15 * 81];
    for (subset_index, subset) in site_subsets.iter().enumerate() {
        for (word_row, word) in words.iter().enumerate() {
            let mut sum = 0u64;
            for permutation in &form_permutations {
                let mut product = 1u64;
                for slot in 0..4 {
                    product = product * forms[permutation[slot]][subset[slot]][word[slot]] as u64
                        % prime as u64;
                }
                sum = (sum + product) % prime as u64;
            }
            column[81 * subset_index + word_row] = sum as u32;
        }
    }
    column
}

fn four_port_kernel_dimension(source: &Source, cap: &[usize], prime: u32) -> (usize, usize, usize) {
    assert_eq!(cap.len(), 2);
    let residual: Vec<usize> = (0..8).filter(|site| !cap.contains(site)).collect();
    let p: Vec<Vec<[u32; 3]>> = (0..3)
        .map(|colour| endpoint_linear_form(source, cap[0], &residual, colour))
        .collect();
    let s: Vec<Vec<[u32; 3]>> = (0..3)
        .map(|colour| endpoint_linear_form(source, cap[1], &residual, colour))
        .collect();
    let colour_pairs = combinations(&[0, 1, 2], 2);
    let mut repeated = Vec::with_capacity(18);
    for repeated_p in 0..3 {
        for s_pair in &colour_pairs {
            repeated.push(four_linear_product(
                [&p[repeated_p], &p[repeated_p], &s[s_pair[0]], &s[s_pair[1]]],
                prime,
            ));
        }
    }
    for p_pair in &colour_pairs {
        for repeated_s in 0..3 {
            repeated.push(four_linear_product(
                [&p[p_pair[0]], &p[p_pair[1]], &s[repeated_s], &s[repeated_s]],
                prime,
            ));
        }
    }
    let repeated_rank = rank(&repeated, prime);
    let mut augmented = repeated.clone();
    for p_pair in &colour_pairs {
        for s_pair in &colour_pairs {
            augmented.push(four_linear_product(
                [&p[p_pair[0]], &p[p_pair[1]], &s[s_pair[0]], &s[s_pair[1]]],
                prime,
            ));
        }
    }
    let augmented_rank = rank(&augmented, prime);
    let kernel_dimension = 9 - (augmented_rank - repeated_rank);
    (repeated_rank, augmented_rank, kernel_dimension)
}

fn four_port_clean_equations(source: &Source, cap: &[usize], prime: u32) -> Vec<Vec<u32>> {
    assert_eq!(cap.len(), 2);
    let residual: Vec<usize> = (0..8).filter(|site| !cap.contains(site)).collect();
    let p: Vec<Vec<[u32; 3]>> = (0..3)
        .map(|colour| endpoint_linear_form(source, cap[0], &residual, colour))
        .collect();
    let s: Vec<Vec<[u32; 3]>> = (0..3)
        .map(|colour| endpoint_linear_form(source, cap[1], &residual, colour))
        .collect();
    let colour_pairs = combinations(&[0, 1, 2], 2);
    let mut repeated = Vec::with_capacity(18);
    for repeated_p in 0..3 {
        for s_pair in &colour_pairs {
            repeated.push(four_linear_product(
                [&p[repeated_p], &p[repeated_p], &s[s_pair[0]], &s[s_pair[1]]],
                prime,
            ));
        }
    }
    for p_pair in &colour_pairs {
        for repeated_s in 0..3 {
            repeated.push(four_linear_product(
                [&p[p_pair[0]], &p[p_pair[1]], &s[repeated_s], &s[repeated_s]],
                prime,
            ));
        }
    }
    let base = normalized_column_basis(&repeated, prime);
    let mut residual_columns = Vec::with_capacity(9);
    for p_pair in &colour_pairs {
        for s_pair in &colour_pairs {
            residual_columns.push(reduce_column(
                four_linear_product(
                    [&p[p_pair[0]], &p[p_pair[1]], &s[s_pair[0]], &s[s_pair[1]]],
                    prime,
                ),
                &base,
                prime,
            ));
        }
    }
    let mut equations = Vec::new();
    for coordinate in 0..residual_columns[0].len() {
        let row: Vec<u32> = residual_columns
            .iter()
            .map(|column| column[coordinate])
            .collect();
        if row.iter().all(|&value| value == 0) {
            continue;
        }
        let old_rank = rank(&equations, prime);
        let mut candidate = equations.clone();
        candidate.push(row.clone());
        if rank(&candidate, prime) > old_rank {
            equations.push(row);
        }
    }
    equations
}

fn audit_four_port_equations(source: &Source, prime: u32) {
    let cap = [6usize, 7usize];
    let equations = four_port_clean_equations(source, &cap, prime);
    println!(
        "four_port_equations source={} cap={:?} prime={} rank={} rows={:?}",
        source.name,
        cap,
        prime,
        rank(&equations, prime),
        equations,
    );
}

fn audit_four_port_kernels(source: &Source, prime: u32) {
    let sites: Vec<usize> = (0..8).collect();
    let mut histogram = BTreeMap::new();
    let mut rank_histogram = BTreeMap::new();
    let started = Instant::now();
    for cap in combinations(&sites, 2) {
        let (base, augmented, kernel) = four_port_kernel_dimension(source, &cap, prime);
        *histogram.entry(kernel).or_insert(0usize) += 1;
        *rank_histogram.entry((base, augmented)).or_insert(0usize) += 1;
    }
    println!(
        "four_port_kernel source={} kernel_hist={:?} rank_hist={:?} elapsed={:.3}s",
        source.name,
        histogram,
        rank_histogram,
        started.elapsed().as_secs_f64()
    );
}

fn endpoint_star_rank(source: &Source, endpoint: usize, deleted: usize, prime: u32) -> usize {
    let residual: Vec<usize> = (0..N)
        .filter(|&site| site != endpoint && site != deleted)
        .collect();
    let mut columns = Vec::with_capacity(Q);
    for endpoint_colour in 0..Q {
        let mut column = Vec::with_capacity(Q * residual.len());
        for &site in &residual {
            for site_colour in 0..Q {
                column.push(cell(source, endpoint, site, endpoint_colour, site_colour));
            }
        }
        columns.push(column);
    }
    rank(&columns, prime)
}

fn audit_pair_geometry(source: &Source, prime: u32) {
    let sites: Vec<usize> = (0..N).collect();
    let mut histogram = BTreeMap::new();
    let started = Instant::now();
    for cap in combinations(&sites, 2) {
        let residual: Vec<usize> = sites
            .iter()
            .copied()
            .filter(|site| !cap.contains(site))
            .collect();
        let left_star = endpoint_star_rank(source, cap[0], cap[1], prime);
        let right_star = endpoint_star_rank(source, cap[1], cap[0], prime);
        let hessian = hessian_rank(source, &residual, prime);
        let extra_hessian_corank = 130usize.saturating_sub(hessian);
        let (_, _, four_port_kernel) = four_port_kernel_dimension(source, &cap, prime);

        let mut theta_failures = 0usize;
        let mut cyclic_open = 0usize;
        for triangle in combinations(&residual, 3) {
            let outside: Vec<usize> = residual
                .iter()
                .copied()
                .filter(|site| !triangle.contains(site))
                .collect();
            let mut all_cyclic = true;
            for &t in &triangle {
                let opposite: Vec<usize> =
                    triangle.iter().copied().filter(|&site| site != t).collect();
                let w = [opposite[0], opposite[1], outside[0], outside[1], outside[2]];
                for colour in 0..Q {
                    let (_, theta) =
                        five_set_profile(source, &w, t, opposite[0], opposite[1], colour, prime);
                    if theta != 9 {
                        theta_failures += 1;
                        all_cyclic = false;
                    }
                }
            }
            if all_cyclic {
                cyclic_open += 1;
            }
        }
        let key = (
            left_star,
            right_star,
            extra_hessian_corank,
            four_port_kernel,
            theta_failures,
            cyclic_open,
        );
        *histogram.entry(key).or_insert(0usize) += 1;
        println!(
            "pair_geometry source={} cap={:?} stars={}/{} hessian={} extra={} four_port_kernel={} theta_failures={} cyclic_open={}",
            source.name,
            cap,
            left_star,
            right_star,
            hessian,
            extra_hessian_corank,
            four_port_kernel,
            theta_failures,
            cyclic_open,
        );
    }
    println!(
        "pair_geometry_summary source={} histogram={:?} elapsed={:.3}s",
        source.name,
        histogram,
        started.elapsed().as_secs_f64(),
    );
}

fn five_set_profile(
    source: &Source,
    w: &[usize; 5],
    t: usize,
    x: usize,
    y: usize,
    colour: usize,
    prime: u32,
) -> (usize, usize) {
    let words5 = assignments(5);
    let mut base_columns = Vec::with_capacity(16);

    // S_W: five sites times three inserted colours.
    for exposed_position in 0..5 {
        let remaining: Vec<usize> = (0..5)
            .filter(|&position| position != exposed_position)
            .map(|position| w[position])
            .collect();
        let cofactor = hafnian_tensor(source, &remaining, prime);
        for inserted_colour in 0..3 {
            let mut column = vec![0u32; 243];
            for (row, word) in words5.iter().enumerate() {
                if word[exposed_position] != inserted_colour {
                    continue;
                }
                let subword: Vec<usize> = (0..5)
                    .filter(|&position| position != exposed_position)
                    .map(|position| word[position])
                    .collect();
                column[row] = cofactor[word_index(&subword)];
            }
            base_columns.push(column);
        }
    }

    // Add the pure c^5 column: restricting beta to delta_c=0.
    let mut pure = vec![0u32; 243];
    pure[word_index(&[colour; 5])] = 1;
    base_columns.push(pure);
    let base_rank = rank(&base_columns, prime);

    // g_c is the t=c slice of H_4 on {t} union O, O=W\{x,y}.
    let o: Vec<usize> = w
        .iter()
        .copied()
        .filter(|&site| site != x && site != y)
        .collect();
    assert_eq!(o.len(), 3);
    let mut four = vec![t];
    four.extend_from_slice(&o);
    let h4 = hafnian_tensor(source, &four, prime);
    let x_position = w.iter().position(|&site| site == x).unwrap();
    let y_position = w.iter().position(|&site| site == y).unwrap();
    let o_positions: Vec<usize> = o
        .iter()
        .map(|site| w.iter().position(|x| x == site).unwrap())
        .collect();

    let mut augmented = base_columns;
    for cx in 0..3 {
        for cy in 0..3 {
            let mut column = vec![0u32; 243];
            for (row, word) in words5.iter().enumerate() {
                if word[x_position] != cx || word[y_position] != cy {
                    continue;
                }
                let mut four_word = vec![colour];
                four_word.extend(o_positions.iter().map(|&position| word[position]));
                column[row] = h4[word_index(&four_word)];
            }
            augmented.push(column);
        }
    }
    let augmented_rank = rank(&augmented, prime);
    (base_rank, augmented_rank - base_rank)
}

fn response_row(
    source: &Source,
    cap: &[usize],
    edge: &[usize],
    left_colour: usize,
    right_colour: usize,
    prime: u32,
) -> Vec<u32> {
    assert_eq!(cap.len(), 2);
    assert_eq!(edge.len(), 2);
    let (p, q) = (cap[0], cap[1]);
    let (a, b) = (edge[0], edge[1]);
    let mut row = vec![0u32; 9];
    for i in 0..3 {
        for j in 0..3 {
            let first = cell(source, p, a, i, left_colour) as u64
                * cell(source, q, b, j, right_colour) as u64;
            let second = cell(source, p, b, i, right_colour) as u64
                * cell(source, q, a, j, left_colour) as u64;
            row[3 * i + j] = ((first + second) % prime as u64) as u32;
        }
    }
    row
}

fn pure_hafnian(source: &Source, vertices: &[usize], colour: usize, prime: u32) -> u32 {
    let tensor = hafnian_tensor(source, vertices, prime);
    tensor[word_index(&vec![colour; vertices.len()])]
}

fn pure_pair_response_row(
    source: &Source,
    cap: &[usize],
    residual: &[usize],
    colour: usize,
    prime: u32,
) -> Vec<u32> {
    let mut answer = vec![0u32; 9];
    for edge in combinations(residual, 2) {
        let complement: Vec<usize> = residual
            .iter()
            .copied()
            .filter(|site| !edge.contains(site))
            .collect();
        let cofactor = pure_hafnian(source, &complement, colour, prime);
        let row = response_row(source, cap, &edge, colour, colour, prime);
        for index in 0..9 {
            answer[index] = ((answer[index] as u64 + cofactor as u64 * row[index] as u64)
                % prime as u64) as u32;
        }
    }
    answer
}

fn amplitude_at_word(source: &Source, word: &[usize], prime: u32) -> u32 {
    assert_eq!(word.len(), N);
    let mut answer = 0u64;
    for matching in matchings(&(0..N).collect::<Vec<_>>()) {
        let mut term = 1u64;
        for (u, v) in matching {
            term = term * cell(source, u, v, word[u], word[v]) as u64 % prime as u64;
        }
        answer = (answer + term) % prime as u64;
    }
    answer as u32
}

fn audit_triangle_pure_quotient(source: &Source, prime: u32) {
    let sites: Vec<usize> = (0..N).collect();
    let mut groups = 0usize;
    let mut open_groups = 0usize;
    let mut open_hafnian_zero = 0usize;
    let mut open_carrier_corank = 0usize;
    let mut open_full_response_increment = BTreeMap::new();
    let mut quotient_profiles = BTreeMap::new();
    let started = Instant::now();

    for cap in combinations(&sites, 2) {
        let residual: Vec<usize> = sites
            .iter()
            .copied()
            .filter(|site| !cap.contains(site))
            .collect();
        for colour in 0..3 {
            let h6 = pure_hafnian(source, &residual, colour, prime);
            let response = pure_pair_response_row(source, &cap, &residual, colour, prime);

            // Literal 15+90 matching partition, checked in every endpoint
            // colour. This is the source-universal input to the quotient
            // collapse on exact X5.
            for i in 0..3 {
                for j in 0..3 {
                    let mut word = vec![colour; N];
                    word[cap[0]] = i;
                    word[cap[1]] = j;
                    let direct = h6 as u64 * cell(source, cap[0], cap[1], i, j) as u64;
                    let reconstructed =
                        ((direct + response[3 * i + j] as u64) % prime as u64) as u32;
                    assert_eq!(
                        reconstructed,
                        amplitude_at_word(source, &word, prime),
                        "pure pair partition failed: source={} cap={:?} colour={} endpoint=({}, {})",
                        source.name,
                        cap,
                        colour,
                        i,
                        j,
                    );
                }
            }

            for triangle in combinations(&residual, 3) {
                groups += 1;
                let outside: Vec<usize> = residual
                    .iter()
                    .copied()
                    .filter(|site| !triangle.contains(site))
                    .collect();
                let mut simultaneous_open = true;
                for &t in &triangle {
                    let xy: Vec<usize> =
                        triangle.iter().copied().filter(|&site| site != t).collect();
                    let mut w_vec = xy.clone();
                    w_vec.extend_from_slice(&outside);
                    w_vec.sort_unstable();
                    let w: [usize; 5] = w_vec.try_into().unwrap();
                    simultaneous_open &=
                        five_set_profile(source, &w, t, xy[0], xy[1], colour, prime).1 == 9;
                }
                if !simultaneous_open {
                    continue;
                }
                open_groups += 1;
                open_hafnian_zero += usize::from(h6 == 0);

                let outside_edges: Vec<Vec<usize>> = combinations(&residual, 2)
                    .into_iter()
                    .filter(|edge| !(triangle.contains(&edge[0]) && triangle.contains(&edge[1])))
                    .collect();
                assert_eq!(outside_edges.len(), 12);
                let mut carrier_rows = Vec::with_capacity(108);
                for edge in &outside_edges {
                    for a in 0..3 {
                        for b in 0..3 {
                            carrier_rows.push(response_row(source, &cap, edge, a, b, prime));
                        }
                    }
                }
                let carrier_rank = rank(&carrier_rows, prime);
                open_carrier_corank += usize::from(carrier_rank < 9);

                let mut full_rows = carrier_rows.clone();
                for edge in combinations(&triangle, 2) {
                    for a in 0..3 {
                        for b in 0..3 {
                            full_rows.push(response_row(source, &cap, &edge, a, b, prime));
                        }
                    }
                }
                let full_rank = rank(&full_rows, prime);
                let response_in_carrier = {
                    let mut augmented = carrier_rows.clone();
                    augmented.push(response.clone());
                    rank(&augmented, prime) == carrier_rank
                };
                *open_full_response_increment
                    .entry(full_rank - carrier_rank)
                    .or_insert(0usize) += 1;
                *quotient_profiles
                    .entry((h6 == 0, carrier_rank, full_rank, response_in_carrier))
                    .or_insert(0usize) += 1;
            }
        }
    }
    assert_eq!(groups, 28 * 3 * 20);
    println!(
        "pure_quotient source={} groups={} open={} open_h6_zero={} open_carrier_corank={} full_response_increment={:?} profiles={:?} elapsed={:.3}s",
        source.name,
        groups,
        open_groups,
        open_hafnian_zero,
        open_carrier_corank,
        open_full_response_increment,
        quotient_profiles,
        started.elapsed().as_secs_f64(),
    );
}

fn matrix_rank_3(source: &Source, u: usize, v: usize, prime: u32) -> usize {
    let columns: Vec<Vec<u32>> = (0..3)
        .map(|b| (0..3).map(|a| cell(source, u, v, a, b)).collect())
        .collect();
    rank(&columns, prime)
}

fn audit_inactive_kernel_overlap(source: &Source, prime: u32) {
    let sites: Vec<usize> = (0..N).collect();
    let mut corank_one = 0usize;
    let mut inactive_corank_one = 0usize;
    let mut joint_rank_histogram = BTreeMap::new();
    let mut adjacent_rank_histogram = BTreeMap::new();
    let mut common_plane_wedge_matches = 0usize;
    let started = Instant::now();
    for cap in combinations(&sites, 2) {
        let residual: Vec<usize> = sites
            .iter()
            .copied()
            .filter(|site| !cap.contains(site))
            .collect();
        let mut response_rows = Vec::with_capacity(135);
        for edge in combinations(&residual, 2) {
            for a in 0..3 {
                for b in 0..3 {
                    response_rows.push(response_row(source, &cap, &edge, a, b, prime));
                }
            }
        }
        let kernel = row_nullspace(&response_rows, 9, prime);
        if kernel.len() != 1 {
            continue;
        }
        corank_one += 1;
        let k = &kernel[0];
        let diagonal_zero = (0..3).all(|c| k[3 * c + c] == 0);
        let direct = (0..3)
            .flat_map(|i| (0..3).map(move |j| (i, j)))
            .map(|(i, j)| k[3 * i + j] as u64 * cell(source, cap[0], cap[1], i, j) as u64)
            .sum::<u64>()
            % prime as u64;
        let inactive = diagonal_zero && direct == 0;
        inactive_corank_one += usize::from(inactive);

        let mut global_forms = Vec::with_capacity(6);
        for endpoint in cap.iter().copied() {
            for endpoint_colour in 0..3 {
                let mut form = Vec::with_capacity(18);
                for &site in &residual {
                    for colour in 0..3 {
                        form.push(cell(source, endpoint, site, endpoint_colour, colour));
                    }
                }
                global_forms.push(form);
            }
        }
        let global_joint_rank = rank(&global_forms, prime);
        if global_joint_rank == 4 {
            let relation_rows: Vec<Vec<u32>> = (0..18)
                .map(|coordinate| global_forms.iter().map(|form| form[coordinate]).collect())
                .collect();
            let relations = row_nullspace(&relation_rows, 6, prime);
            assert_eq!(relations.len(), 2);
            let mut wedge = vec![0u32; 9];
            for i in 0..3 {
                for j in 0..3 {
                    let positive = relations[0][i] as u64 * relations[1][3 + j] as u64;
                    let negative = relations[1][i] as u64 * relations[0][3 + j] as u64;
                    wedge[3 * i + j] =
                        ((positive + prime as u64 * prime as u64 - negative) % prime as u64) as u32;
                }
            }
            assert!(wedge.iter().any(|&value| value != 0));
            assert!(response_rows.iter().all(|row| {
                row.iter()
                    .zip(&wedge)
                    .map(|(&a, &b)| a as u64 * b as u64)
                    .sum::<u64>()
                    % prime as u64
                    == 0
            }));
            common_plane_wedge_matches += 1;
        }

        let mut site_joint_ranks = Vec::new();
        for &removed in &residual {
            let remainder: Vec<usize> = residual
                .iter()
                .copied()
                .filter(|&site| site != removed)
                .collect();
            let mut forms = Vec::with_capacity(6);
            for endpoint in cap.iter().copied() {
                for endpoint_colour in 0..3 {
                    let mut form = Vec::with_capacity(15);
                    for &site in &remainder {
                        for colour in 0..3 {
                            form.push(cell(source, endpoint, site, endpoint_colour, colour));
                        }
                    }
                    forms.push(form);
                }
            }
            let joint_rank = rank(&forms, prime);
            site_joint_ranks.push(joint_rank);
            let left_rank = matrix_rank_3(source, cap[0], removed, prime);
            let right_rank = matrix_rank_3(source, cap[1], removed, prime);
            *adjacent_rank_histogram
                .entry((inactive, joint_rank, left_rank, right_rank))
                .or_insert(0usize) += 1;

            // Coefficient of the removed site in R_K. This is the literal
            // adjacent-chart overlap equation. A fixed-pair contraction of
            // the full-nine rows cannot see it after R_K=d=kappa=0.
            for colour in 0..3 {
                let mut coefficient = vec![0u32; 15];
                for j in 0..3 {
                    let left = (0..3)
                        .map(|i| {
                            k[3 * i + j] as u64 * cell(source, cap[0], removed, i, colour) as u64
                        })
                        .sum::<u64>()
                        % prime as u64;
                    for (slot, &site) in remainder.iter().enumerate() {
                        for b in 0..3 {
                            let index = 3 * slot + b;
                            coefficient[index] = ((coefficient[index] as u64
                                + left * cell(source, cap[1], site, j, b) as u64)
                                % prime as u64)
                                as u32;
                        }
                    }
                }
                for i in 0..3 {
                    let right = (0..3)
                        .map(|j| {
                            k[3 * i + j] as u64 * cell(source, cap[1], removed, j, colour) as u64
                        })
                        .sum::<u64>()
                        % prime as u64;
                    for (slot, &site) in remainder.iter().enumerate() {
                        for a in 0..3 {
                            let index = 3 * slot + a;
                            coefficient[index] = ((coefficient[index] as u64
                                + right * cell(source, cap[0], site, i, a) as u64)
                                % prime as u64)
                                as u32;
                        }
                    }
                }
                assert!(coefficient.iter().all(|&value| value == 0));
            }
        }
        site_joint_ranks.sort_unstable();
        *joint_rank_histogram
            .entry((inactive, global_joint_rank, site_joint_ranks))
            .or_insert(0usize) += 1;
    }
    println!(
        "inactive_overlap source={} corank_one={} inactive_corank_one={} common_plane_wedge_matches={} joint_rank_hist={:?} adjacent_rank_hist={:?} elapsed={:.3}s",
        source.name,
        corank_one,
        inactive_corank_one,
        common_plane_wedge_matches,
        joint_rank_histogram,
        adjacent_rank_histogram,
        started.elapsed().as_secs_f64(),
    );
}

fn audit_common_plane_normal_form(source: &Source, prime: u32) {
    let sites: Vec<usize> = (0..N).collect();
    let mut common_plane_cases = 0usize;
    let mut generic_coordinate_cases = 0usize;
    let mut coordinate_plane_cases = 0usize;
    let mut diagonal_lifts = 0usize;
    let mut rank_one_defects = 0usize;
    let mut direct_symmetry_checks = 0usize;
    let mut exceptional_without_diagonal_lift = 0usize;

    for cap in combinations(&sites, 2) {
        let residual: Vec<usize> = sites
            .iter()
            .copied()
            .filter(|site| !cap.contains(site))
            .collect();
        let mut response_rows = Vec::with_capacity(135);
        for edge in combinations(&residual, 2) {
            for a in 0..3 {
                for b in 0..3 {
                    response_rows.push(response_row(source, &cap, &edge, a, b, prime));
                }
            }
        }
        let kernel = row_nullspace(&response_rows, 9, prime);
        if kernel.len() != 1 {
            continue;
        }
        let k = &kernel[0];
        let diagonal_zero = (0..3).all(|c| k[3 * c + c] == 0);
        let direct = (0..3)
            .flat_map(|i| (0..3).map(move |j| (i, j)))
            .map(|(i, j)| k[3 * i + j] as u64 * cell(source, cap[0], cap[1], i, j) as u64)
            .sum::<u64>()
            % prime as u64;
        if !diagonal_zero || direct != 0 {
            continue;
        }

        let mut forms = Vec::with_capacity(6);
        for endpoint in cap.iter().copied() {
            for endpoint_colour in 0..3 {
                let mut form = Vec::with_capacity(18);
                for &site in &residual {
                    for colour in 0..3 {
                        form.push(cell(source, endpoint, site, endpoint_colour, colour));
                    }
                }
                forms.push(form);
            }
        }
        if rank(&forms, prime) != 4 {
            continue;
        }
        let relation_rows: Vec<Vec<u32>> = (0..18)
            .map(|coordinate| forms.iter().map(|form| form[coordinate]).collect())
            .collect();
        let relations = row_nullspace(&relation_rows, 6, prime);
        assert_eq!(relations.len(), 2);
        assert_eq!(
            rank(
                &[relations[0][0..3].to_vec(), relations[1][0..3].to_vec()],
                prime
            ),
            2
        );
        assert_eq!(
            rank(
                &[relations[0][3..6].to_vec(), relations[1][3..6].to_vec()],
                prime
            ),
            2
        );
        common_plane_cases += 1;

        let coordinate_zero: Vec<usize> = (0..3)
            .filter(|&i| relations[0][i] == 0 && relations[1][i] == 0)
            .collect();
        if coordinate_zero.is_empty() {
            generic_coordinate_cases += 1;
        } else {
            assert_eq!(coordinate_zero.len(), 1);
            coordinate_plane_cases += 1;
        }

        // A relation is P(x)+S(b)=0.  On a non-coordinate common plane,
        // K_ii=0 makes b_i=-lambda_i x_i for one diagonal D.  When the
        // plane is x_i=0, K_ii=0 says nothing about b_i; this is the exact
        // exceptional stratum omitted by the naive diagonal claim.
        let mut lambda = [0u32; 3];
        let mut has_diagonal_lift = true;
        for i in 0..3 {
            let pivot = (0..2).find(|&row| relations[row][i] != 0);
            if let Some(row) = pivot {
                let inverse = mod_pow(relations[row][i], prime - 2, prime);
                lambda[i] = ((prime as u64 - relations[row][3 + i] as u64) * inverse as u64
                    % prime as u64) as u32;
                for relation in &relations {
                    let total = (relation[3 + i] as u64 + lambda[i] as u64 * relation[i] as u64)
                        % prime as u64;
                    assert_eq!(total, 0);
                }
            } else if relations.iter().any(|relation| relation[3 + i] != 0) {
                has_diagonal_lift = false;
            }
        }

        if !has_diagonal_lift {
            exceptional_without_diagonal_lift += 1;
            assert!(!coordinate_zero.is_empty());
            continue;
        }
        diagonal_lifts += 1;

        let defects: Vec<Vec<u32>> = (0..3)
            .map(|i| {
                forms[i]
                    .iter()
                    .zip(&forms[3 + i])
                    .map(|(&p, &s)| {
                        ((p as u64 + prime as u64 - lambda[i] as u64 * s as u64 % prime as u64)
                            % prime as u64) as u32
                    })
                    .collect()
            })
            .collect();
        assert!(rank(&defects, prime) <= 1);
        rank_one_defects += 1;

        let left_plane = vec![relations[0][0..3].to_vec(), relations[1][0..3].to_vec()];
        let normal = row_nullspace(&left_plane, 3, prime);
        assert_eq!(normal.len(), 1);
        for i in 0..3 {
            for j in 0..3 {
                for coordinate in 0..18 {
                    let lhs = normal[0][j] as u64 * defects[i][coordinate] as u64 % prime as u64;
                    let rhs = normal[0][i] as u64 * defects[j][coordinate] as u64 % prime as u64;
                    assert_eq!(lhs, rhs);
                }
            }
        }

        let x = &left_plane[0];
        let y = &left_plane[1];
        let mut xady = 0u64;
        let mut yadx = 0u64;
        for i in 0..3 {
            for j in 0..3 {
                let aij = cell(source, cap[0], cap[1], i, j) as u64;
                xady = (xady
                    + x[i] as u64 * aij % prime as u64 * lambda[j] as u64 % prime as u64
                        * y[j] as u64)
                    % prime as u64;
                yadx = (yadx
                    + y[i] as u64 * aij % prime as u64 * lambda[j] as u64 % prime as u64
                        * x[j] as u64)
                    % prime as u64;
            }
        }
        assert_eq!(xady, yadx);
        direct_symmetry_checks += 1;
    }

    println!(
        "common_plane_normal source={} cases={} generic={} coordinate={} diagonal_lifts={} rank_one_defects={} direct_symmetry={} exceptional_no_lift={}",
        source.name,
        common_plane_cases,
        generic_coordinate_cases,
        coordinate_plane_cases,
        diagonal_lifts,
        rank_one_defects,
        direct_symmetry_checks,
        exceptional_without_diagonal_lift,
    );
}

fn hessian_block_columns(
    source: &Source,
    vertices: &[usize],
    prime: u32,
) -> Vec<((usize, usize), Vec<Vec<u32>>)> {
    assert_eq!(vertices.len(), 6);
    let words6 = assignments(6);
    let mut blocks = Vec::with_capacity(15);
    for left_position in 0..6 {
        for right_position in left_position + 1..6 {
            let remaining: Vec<usize> = (0..6)
                .filter(|&position| position != left_position && position != right_position)
                .map(|position| vertices[position])
                .collect();
            let cofactor = hafnian_tensor(source, &remaining, prime);
            let mut block_columns = Vec::with_capacity(9);
            for left_colour in 0..3 {
                for right_colour in 0..3 {
                    let mut column = vec![0u32; 729];
                    for (row, word) in words6.iter().enumerate() {
                        if word[left_position] != left_colour
                            || word[right_position] != right_colour
                        {
                            continue;
                        }
                        let subword: Vec<usize> = (0..6)
                            .filter(|&position| {
                                position != left_position && position != right_position
                            })
                            .map(|position| word[position])
                            .collect();
                        column[row] = cofactor[word_index(&subword)];
                    }
                    block_columns.push(column);
                }
            }
            blocks.push((
                (vertices[left_position], vertices[right_position]),
                block_columns,
            ));
        }
    }
    blocks
}

fn hessian_rank(source: &Source, vertices: &[usize], prime: u32) -> usize {
    let blocks = hessian_block_columns(source, vertices, prime);
    let columns: Vec<Vec<u32>> = blocks.into_iter().flat_map(|(_, block)| block).collect();
    rank(&columns, prime)
}

fn hessian_greedy_ladder(
    source: &Source,
    vertices: &[usize],
    distinguished: usize,
    prime: u32,
) -> (usize, Vec<((usize, usize), usize)>) {
    let blocks = hessian_block_columns(source, vertices, prime);
    let mut selected = Vec::new();
    let mut remaining = Vec::new();
    for (edge, columns) in blocks {
        if edge.0 == distinguished || edge.1 == distinguished {
            selected.extend(columns);
        } else {
            remaining.push((edge, columns));
        }
    }
    assert_eq!(selected.len(), 45);
    assert_eq!(remaining.len(), 10);
    let base_rank = rank(&selected, prime);
    let mut current_rank = base_rank;
    let mut ladder = Vec::new();
    while !remaining.is_empty() {
        let mut best: Option<(usize, usize)> = None;
        for (index, (_, columns)) in remaining.iter().enumerate() {
            let candidate: Vec<Vec<u32>> = selected
                .iter()
                .cloned()
                .chain(columns.iter().cloned())
                .collect();
            let candidate_rank = rank(&candidate, prime);
            if best.map_or(true, |(_, value)| candidate_rank > value) {
                best = Some((index, candidate_rank));
            }
        }
        let (index, next_rank) = best.unwrap();
        let (edge, columns) = remaining.remove(index);
        ladder.push((edge, next_rank - current_rank));
        selected.extend(columns);
        current_rank = next_rank;
    }
    (base_rank, ladder)
}

fn gauge_dimension_for_internal_subset(
    vertices: &[usize],
    distinguished: usize,
    internal_edges: &[(usize, usize)],
    selected_mask: usize,
    prime: u32,
) -> usize {
    // A vertex rescaling alpha gives the Hessian-kernel vector
    // delta A_ij=(alpha_i+alpha_j)A_ij when sum_i alpha_i=0.  If an
    // internal edge is omitted, its coefficient must vanish.  On the
    // full-support controls audited below these are precisely the universal
    // gauge relations supported on the selected star-plus-internal blocks.
    let mut equations = vec![vec![1u32; vertices.len()]];
    for (index, &(u, v)) in internal_edges.iter().enumerate() {
        if selected_mask & (1usize << index) != 0 {
            continue;
        }
        let mut equation = vec![0u32; vertices.len()];
        equation[vertices.iter().position(|&site| site == u).unwrap()] = 1;
        equation[vertices.iter().position(|&site| site == v).unwrap()] = 1;
        equations.push(equation);
    }
    assert!(vertices.contains(&distinguished));
    vertices.len() - rank(&equations, prime)
}

fn hessian_subset_circuit_census(
    source: &Source,
    vertices: &[usize],
    distinguished: usize,
    prime: u32,
) {
    let blocks = hessian_block_columns(source, vertices, prime);
    let mut star_columns = Vec::new();
    let mut internal = Vec::new();
    for (edge, columns) in blocks {
        if edge.0 == distinguished || edge.1 == distinguished {
            star_columns.extend(columns);
        } else {
            internal.push((edge, columns));
        }
    }
    assert_eq!(star_columns.len(), 45);
    assert_eq!(internal.len(), 10);
    let internal_edges: Vec<(usize, usize)> = internal.iter().map(|x| x.0).collect();
    let subset_count = 1usize << internal.len();
    let mut actual = vec![0usize; subset_count];
    let mut expected = vec![0usize; subset_count];
    let mut deficits = vec![0usize; subset_count];
    let mut deficit_histogram = BTreeMap::new();
    let started = Instant::now();

    for mask in 0..subset_count {
        let mut columns = star_columns.clone();
        for (index, (_, block)) in internal.iter().enumerate() {
            if mask & (1usize << index) != 0 {
                columns.extend(block.iter().cloned());
            }
        }
        actual[mask] = rank(&columns, prime);
        let gauge = gauge_dimension_for_internal_subset(
            vertices,
            distinguished,
            &internal_edges,
            mask,
            prime,
        );
        expected[mask] = columns.len() - gauge;
        assert!(
            actual[mask] <= expected[mask],
            "rank exceeds gauge upper bound: source={} t={} mask={:#x} actual={} expected={}",
            source.name,
            distinguished,
            mask,
            actual[mask],
            expected[mask]
        );
        deficits[mask] = expected[mask] - actual[mask];
        *deficit_histogram.entry(deficits[mask]).or_insert(0usize) += 1;
    }

    let mut minimal = Vec::new();
    for mask in 1..subset_count {
        if deficits[mask] == 0 {
            continue;
        }
        let mut proper = (mask - 1) & mask;
        let mut is_minimal = true;
        while proper != 0 {
            if deficits[proper] != 0 {
                is_minimal = false;
                break;
            }
            proper = (proper - 1) & mask;
        }
        if deficits[0] != 0 {
            is_minimal = false;
        }
        if is_minimal {
            let edges: Vec<(usize, usize)> = internal_edges
                .iter()
                .enumerate()
                .filter_map(|(index, &edge)| (mask & (1usize << index) != 0).then_some(edge))
                .collect();
            minimal.push((edges, actual[mask], expected[mask], deficits[mask]));
        }
    }
    println!(
        "hessian_subset_circuits source={} cap_vertices={:?} t={} subsets={} deficit_hist={:?} minimal={:?} elapsed={:.3}s",
        source.name, vertices, distinguished, subset_count, deficit_histogram, minimal,
        started.elapsed().as_secs_f64()
    );
}

fn combinations(values: &[usize], count: usize) -> Vec<Vec<usize>> {
    fn visit(
        values: &[usize],
        count: usize,
        start: usize,
        current: &mut Vec<usize>,
        out: &mut Vec<Vec<usize>>,
    ) {
        if current.len() == count {
            out.push(current.clone());
            return;
        }
        for index in start..=values.len() - (count - current.len()) {
            current.push(values[index]);
            visit(values, count, index + 1, current, out);
            current.pop();
        }
    }
    let mut out = Vec::new();
    visit(values, count, 0, &mut Vec::new(), &mut out);
    out
}

fn audit_source(source: &Source, prime: u32) {
    let started = Instant::now();
    let mut histogram: BTreeMap<usize, usize> = BTreeMap::new();
    let mut base_histogram: BTreeMap<usize, usize> = BTreeMap::new();
    let mut triangle_min_histogram: BTreeMap<usize, usize> = BTreeMap::new();
    let mut cap_hessian_theta_histogram: BTreeMap<(usize, usize), usize> = BTreeMap::new();
    let mut examples: BTreeMap<usize, String> = BTreeMap::new();
    let sites: Vec<usize> = (0..8).collect();
    let mut profiles = 0usize;
    for cap in combinations(&sites, 2) {
        let residual: Vec<usize> = sites.iter().copied().filter(|x| !cap.contains(x)).collect();
        let residual_hessian_rank = hessian_rank(source, &residual, prime);
        if cap == vec![6, 7] {
            for &distinguished in &residual {
                let (base, ladder) = hessian_greedy_ladder(source, &residual, distinguished, prime);
                println!(
                    "canonical_hessian_ladder source={} cap={:?} t={} base={} ladder={:?} full={}",
                    source.name, cap, distinguished, base, ladder, residual_hessian_rank
                );
            }
        }
        let mut cap_full_triangle_colour_groups = 0usize;
        let mut cap_failed_triangle_colour_groups = Vec::new();
        for triangle in combinations(&residual, 3) {
            let outside: Vec<usize> = residual
                .iter()
                .copied()
                .filter(|x| !triangle.contains(x))
                .collect();
            for colour in 0..3 {
                let mut triangle_ranks = Vec::new();
                for &t in &triangle {
                    let xy: Vec<usize> = triangle.iter().copied().filter(|&x| x != t).collect();
                    let mut w_vec = xy.clone();
                    w_vec.extend_from_slice(&outside);
                    w_vec.sort_unstable();
                    let w: [usize; 5] = w_vec.try_into().unwrap();
                    let (base_rank, increment) =
                        five_set_profile(source, &w, t, xy[0], xy[1], colour, prime);
                    *histogram.entry(increment).or_default() += 1;
                    *base_histogram.entry(base_rank).or_default() += 1;
                    examples.entry(increment).or_insert_with(|| {
                        format!(
                            "cap={:?},T={:?},t={},c={},W={:?},base={}",
                            cap, triangle, t, colour, w, base_rank
                        )
                    });
                    profiles += 1;
                    triangle_ranks.push(increment);
                }
                let triangle_min = *triangle_ranks.iter().min().unwrap();
                *triangle_min_histogram.entry(triangle_min).or_default() += 1;
                if triangle_min == 9 {
                    cap_full_triangle_colour_groups += 1;
                } else {
                    cap_failed_triangle_colour_groups.push((
                        triangle.clone(),
                        colour,
                        triangle_min,
                    ));
                }
            }
        }
        if cap == vec![6, 7] && source.name == "dense_support_E1_block" {
            assert_eq!(cap_failed_triangle_colour_groups.len(), 12);
            assert!(cap_failed_triangle_colour_groups
                .iter()
                .all(|(triangle, _, rank)| triangle.contains(&0)
                    && triangle.contains(&1)
                    && *rank == 0));
            println!(
                "dense_e1_failed_groups cap={:?} groups={:?}",
                cap, cap_failed_triangle_colour_groups
            );
        }
        *cap_hessian_theta_histogram
            .entry((residual_hessian_rank, cap_full_triangle_colour_groups))
            .or_default() += 1;
    }
    assert_eq!(profiles, 28 * 20 * 3 * 3);
    println!(
        "source={} profiles={} theta_rank_hist={:?} triangle_min_rank_hist={:?} base_rank_hist={:?} cap_hessian_theta_hist={:?} examples={:?} elapsed={:.3}s",
        source.name, profiles, histogram, triangle_min_histogram, base_histogram,
        cap_hessian_theta_histogram, examples,
        started.elapsed().as_secs_f64()
    );
}

fn xorshift64(state: &mut u64) -> u64 {
    let mut value = *state;
    value ^= value << 13;
    value ^= value >> 7;
    value ^= value << 17;
    *state = value;
    value
}

fn random_nonzero_vector(state: &mut u64, prime: u32) -> [u32; 3] {
    loop {
        let vector = [
            (xorshift64(state) % prime as u64) as u32,
            (xorshift64(state) % prime as u64) as u32,
            (xorshift64(state) % prime as u64) as u32,
        ];
        if vector.iter().any(|&value| value != 0) {
            return vector;
        }
    }
}

fn random_low_rank_source(state: &mut u64, prime: u32) -> Source {
    let mut cells = [0u32; 252];
    for u in 0..6 {
        for v in u + 1..6 {
            let summand_count = 1 + (xorshift64(state) % 3) as usize;
            for _ in 0..summand_count {
                let left = random_nonzero_vector(state, prime);
                let right = random_nonzero_vector(state, prime);
                for a in 0..3 {
                    for b in 0..3 {
                        let index = 9 * edge_index(u, v) + 3 * a + b;
                        cells[index] = ((cells[index] as u64 + left[a] as u64 * right[b] as u64)
                            % prime as u64) as u32;
                    }
                }
            }
            // Cancellation can exceptionally make a sampled block zero.
            let offset = 9 * edge_index(u, v);
            if cells[offset..offset + 9].iter().all(|&value| value == 0) {
                cells[offset] = 1;
            }
        }
    }
    Source {
        name: "random_low_rank".to_string(),
        cells,
    }
}

fn has_clean_hessian_subdefect(blocks: &[((usize, usize), Vec<Vec<u32>>)], prime: u32) -> bool {
    // On the all-nonzero complete block graph, a gauge vector cannot be
    // supported on a proper star or triangle.  A column dependency on one
    // of these 26 matching-number-one supports is therefore nongauge.
    for centre in 0..6 {
        let columns: Vec<Vec<u32>> = blocks
            .iter()
            .filter(|(edge, _)| edge.0 == centre || edge.1 == centre)
            .flat_map(|(_, block)| block.iter().cloned())
            .collect();
        if rank(&columns, prime) < columns.len() {
            return true;
        }
    }
    let sites: Vec<usize> = (0..6).collect();
    for triangle in combinations(&sites, 3) {
        let columns: Vec<Vec<u32>> = blocks
            .iter()
            .filter(|(edge, _)| triangle.contains(&edge.0) && triangle.contains(&edge.1))
            .flat_map(|(_, block)| block.iter().cloned())
            .collect();
        if rank(&columns, prime) < columns.len() {
            return true;
        }
    }
    false
}

fn search_clean_hessian_circuit() {
    const PRIME: u32 = 5;
    const SAMPLE_COUNT: usize = 10_000;
    let vertices: Vec<usize> = (0..6).collect();
    let mut state = 0x198d_a410_77f2_c53bu64;
    let mut defective = 0usize;
    let mut clean = 0usize;
    let mut hostile = 0usize;
    let mut rank_histogram = BTreeMap::new();
    let started = Instant::now();
    for sample in 0..SAMPLE_COUNT {
        let source = random_low_rank_source(&mut state, PRIME);
        let blocks = hessian_block_columns(&source, &vertices, PRIME);
        let columns: Vec<Vec<u32>> = blocks
            .iter()
            .flat_map(|(_, block)| block.iter().cloned())
            .collect();
        let hessian = rank(&columns, PRIME);
        *rank_histogram.entry(hessian).or_insert(0usize) += 1;
        if hessian >= 130 {
            continue;
        }
        defective += 1;
        if has_clean_hessian_subdefect(&blocks, PRIME) {
            clean += 1;
        } else {
            hostile += 1;
            println!(
                "hostile_hessian_circuit sample={} rank={} cells={:?}",
                sample,
                hessian,
                &source.cells[..135]
            );
            break;
        }
    }
    println!(
        "clean_circuit_search prime={} samples={} defective={} clean={} hostile={} rank_hist={:?} elapsed={:.3}s",
        PRIME,
        SAMPLE_COUNT,
        defective,
        clean,
        hostile,
        rank_histogram,
        started.elapsed().as_secs_f64()
    );
}

fn residual_line_source(
    left: &[u32; 135],
    right: &[u32; 135],
    parameter: u32,
    prime: u32,
) -> Source {
    let mut cells = [0u32; 252];
    let mut index = 0usize;
    for u in 0..6 {
        for v in u + 1..6 {
            for a in 0..3 {
                for b in 0..3 {
                    cells[9 * edge_index(u, v) + 3 * a + b] =
                        ((left[index] as u64 + parameter as u64 * right[index] as u64)
                            % prime as u64) as u32;
                    index += 1;
                }
            }
        }
    }
    assert_eq!(index, 135);
    Source {
        name: format!("line_t{}", parameter),
        cells,
    }
}

fn residual_full_triangle_groups(source: &Source, prime: u32) -> usize {
    let residual: Vec<usize> = (0..6).collect();
    let mut full_groups = 0usize;
    for triangle in combinations(&residual, 3) {
        let outside: Vec<usize> = residual
            .iter()
            .copied()
            .filter(|x| !triangle.contains(x))
            .collect();
        for colour in 0..3 {
            let mut full = true;
            for &t in &triangle {
                let xy: Vec<usize> = triangle.iter().copied().filter(|&x| x != t).collect();
                let mut w_vec = xy.clone();
                w_vec.extend_from_slice(&outside);
                w_vec.sort_unstable();
                let w: [usize; 5] = w_vec.try_into().unwrap();
                let (_, increment) = five_set_profile(source, &w, t, xy[0], xy[1], colour, prime);
                full &= increment == 9;
            }
            full_groups += usize::from(full);
        }
    }
    full_groups
}

fn search_hessian_boundary(prime: u32, line_count: usize) {
    let residual: Vec<usize> = (0..6).collect();
    let mut state = 0x7c61_5a23_d49e_108fu64;
    let mut defective = 0usize;
    let mut joint_histogram: BTreeMap<(usize, usize), usize> = BTreeMap::new();
    let started = Instant::now();
    for line in 0..line_count {
        let mut left = [0u32; 135];
        let mut right = [0u32; 135];
        for value in &mut left {
            *value = (xorshift64(&mut state) % prime as u64) as u32;
        }
        for value in &mut right {
            *value = (xorshift64(&mut state) % prime as u64) as u32;
        }
        for parameter in 0..prime {
            let source = residual_line_source(&left, &right, parameter, prime);
            let hessian = hessian_rank(&source, &residual, prime);
            if hessian < 130 {
                defective += 1;
                let full_groups = residual_full_triangle_groups(&source, prime);
                *joint_histogram.entry((hessian, full_groups)).or_default() += 1;
                println!(
                    "boundary_witness line={} parameter={} hessian_rank={} full_triangle_groups={}",
                    line, parameter, hessian, full_groups
                );
            }
        }
    }
    println!(
        "boundary_search prime={} lines={} samples={} defective={} joint_hist={:?} elapsed={:.3}s",
        prime,
        line_count,
        line_count * prime as usize,
        defective,
        joint_histogram,
        started.elapsed().as_secs_f64()
    );
}

fn parse(path: &str) -> (u32, Vec<Source>) {
    let text = fs::read_to_string(path).expect("read source export");
    let mut lines = text.lines();
    let header: Vec<_> = lines.next().expect("header").split_whitespace().collect();
    assert_eq!(header[0], "p");
    let prime: u32 = header[1].parse().unwrap();
    let mut sources = Vec::new();
    for line in lines {
        let mut fields = line.split_whitespace();
        let name = fields.next().unwrap().to_string();
        let values: Vec<u32> = fields.map(|value| value.parse().unwrap()).collect();
        assert_eq!(values.len(), 252);
        sources.push(Source {
            name,
            cells: values.try_into().unwrap(),
        });
    }
    (prime, sources)
}

fn main() {
    let arguments: Vec<String> = env::args().skip(1).collect();
    let path = arguments.first().expect(
        "usage: five-set-response-surjectivity sources.txt [--circuit-census] | --search-boundary",
    );
    if path == "--search-boundary" {
        search_hessian_boundary(101, 64);
        return;
    }
    if path == "--search-boundary-small" {
        search_hessian_boundary(5, 1024);
        return;
    }
    if path == "--search-clean-circuit" {
        search_clean_hessian_circuit();
        return;
    }
    let (prime, sources) = parse(path);
    if arguments.get(1).map(String::as_str) == Some("--circuit-census") {
        let vertices: Vec<usize> = (0..6).collect();
        for source in &sources {
            if source.name == "dense" || source.name == "dense_support_E1_block" {
                for distinguished in 2..6 {
                    hessian_subset_circuit_census(source, &vertices, distinguished, prime);
                }
            }
        }
        return;
    }
    if arguments.get(1).map(String::as_str) == Some("--four-port-kernels") {
        for source in &sources {
            audit_four_port_kernels(source, prime);
        }
        return;
    }
    if arguments.get(1).map(String::as_str) == Some("--pair-geometry") {
        for source in &sources {
            audit_pair_geometry(source, prime);
        }
        return;
    }
    if arguments.get(1).map(String::as_str) == Some("--four-port-equations") {
        for source in &sources {
            if source.name == "good_star_E1_block" {
                audit_four_port_equations(source, prime);
            }
        }
        return;
    }
    if arguments.get(1).map(String::as_str) == Some("--pure-quotient") {
        for source in &sources {
            audit_triangle_pure_quotient(source, prime);
        }
        return;
    }
    if arguments.get(1).map(String::as_str) == Some("--inactive-kernel-overlap") {
        for source in &sources {
            audit_inactive_kernel_overlap(source, prime);
        }
        return;
    }
    if arguments.get(1).map(String::as_str) == Some("--common-plane-normal-form") {
        for source in &sources {
            audit_common_plane_normal_form(source, prime);
        }
        return;
    }
    for source in &sources {
        audit_source(source, prime);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn perfect_matching_counts_are_correct() {
        assert_eq!(matchings(&[]).len(), 1);
        assert_eq!(matchings(&[0, 1, 2, 3]).len(), 3);
        assert_eq!(matchings(&[0, 1, 2, 3, 4, 5]).len(), 15);
        assert_eq!(matchings(&[0, 1, 2, 3, 4, 5, 6, 7]).len(), 105);
    }

    #[test]
    fn oriented_cell_access_transposes() {
        let mut values = [0u32; 252];
        values[9 * edge_index(2, 6) + 3 * 1 + 2] = 37;
        let source = Source {
            name: "test".to_string(),
            cells: values,
        };
        assert_eq!(cell(&source, 2, 6, 1, 2), 37);
        assert_eq!(cell(&source, 6, 2, 2, 1), 37);
        assert_eq!(cell(&source, 6, 2, 1, 2), 0);
    }

    #[test]
    fn modular_rank_is_column_rank() {
        let columns = vec![vec![1, 0, 1], vec![0, 1, 1], vec![1, 1, 2]];
        assert_eq!(rank(&columns, 1009), 2);
    }
}
