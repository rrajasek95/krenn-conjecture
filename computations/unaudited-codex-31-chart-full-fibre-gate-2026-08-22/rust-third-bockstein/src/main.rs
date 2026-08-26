use std::cmp::Ordering;
use std::collections::{HashMap, HashSet, VecDeque};
use std::env;
use std::fs::File;
use std::hash::{Hash, Hasher};
use std::io::{BufReader, BufWriter, Read, Write};
use std::path::PathBuf;
use std::time::Instant;

const PORTS: usize = 24;
const PRIME: u16 = 1009;

#[derive(Copy, Clone, Debug, Eq)]
struct Key([i8; PORTS]);

impl PartialEq for Key {
    fn eq(&self, other: &Self) -> bool { self.0 == other.0 }
}

impl Hash for Key {
    fn hash<H: Hasher>(&self, state: &mut H) { self.0.hash(state); }
}

impl Ord for Key {
    fn cmp(&self, other: &Self) -> Ordering { self.0.cmp(&other.0) }
}

impl PartialOrd for Key {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> { Some(self.cmp(other)) }
}

struct Reader<R: Read> { inner: R }

impl<R: Read> Reader<R> {
    fn bytes<const N: usize>(&mut self) -> [u8; N] {
        let mut answer = [0u8; N];
        self.inner.read_exact(&mut answer).expect("truncated input");
        answer
    }
    fn u16(&mut self) -> u16 { u16::from_le_bytes(self.bytes()) }
    fn u32(&mut self) -> u32 { u32::from_le_bytes(self.bytes()) }
    fn key(&mut self) -> Key {
        let raw = self.bytes::<PORTS>();
        let mut answer = [0i8; PORTS];
        for (target, source) in answer.iter_mut().zip(raw) { *target = source as i8; }
        Key(answer)
    }
    fn keys(&mut self) -> Vec<Key> {
        let n = self.u32() as usize;
        (0..n).map(|_| self.key()).collect()
    }
}

struct Input {
    used: Vec<Key>,
    second: Vec<Key>,
    rows: Vec<Key>,
    old_rows: Vec<Key>,
    kernels: Vec<Vec<(u32, u16)>>,
    tails: Vec<Vec<(Key, u16)>>,
    column_controls: Vec<(Key, Vec<Key>)>,
    row_controls: Vec<(Key, Vec<Key>)>,
}

fn read_input(path: &PathBuf) -> Input {
    let file = File::open(path).expect("cannot open input");
    let mut reader = Reader { inner: BufReader::new(file) };
    assert_eq!(&reader.bytes::<8>(), b"BCK3R002");
    assert_eq!(reader.u32(), PRIME as u32);
    let used = reader.keys();
    let second = reader.keys();
    let rows = reader.keys();
    let old_rows = reader.keys();
    let kernel_count = reader.u32() as usize;
    let mut kernels = Vec::with_capacity(kernel_count);
    for _ in 0..kernel_count {
        let n = reader.u32() as usize;
        kernels.push((0..n).map(|_| (reader.u32(), reader.u16())).collect());
    }
    let tail_count = reader.u32() as usize;
    let mut tails = Vec::with_capacity(tail_count);
    for _ in 0..tail_count {
        let n = reader.u32() as usize;
        tails.push((0..n).map(|_| (reader.key(), reader.u16())).collect());
    }
    let column_control_count = reader.u32() as usize;
    let column_controls = (0..column_control_count)
        .map(|_| (reader.key(), reader.keys())).collect();
    let row_control_count = reader.u32() as usize;
    let row_controls = (0..row_control_count)
        .map(|_| (reader.key(), reader.keys())).collect();
    Input { used, second, rows, old_rows, kernels, tails, column_controls, row_controls }
}

fn perfect_matchings(vertices: &[u8]) -> Vec<[(u8, u8); 4]> {
    fn rec(vertices: &[u8], current: &mut Vec<(u8, u8)>, out: &mut Vec<[(u8, u8); 4]>) {
        if vertices.is_empty() {
            out.push(current.as_slice().try_into().unwrap());
            return;
        }
        let first = vertices[0];
        for position in 1..vertices.len() {
            let second = vertices[position];
            let mut remaining = Vec::with_capacity(vertices.len() - 2);
            remaining.extend_from_slice(&vertices[1..position]);
            remaining.extend_from_slice(&vertices[position + 1..]);
            current.push((first, second));
            rec(&remaining, current, out);
            current.pop();
        }
    }
    let mut out = Vec::new();
    rec(vertices, &mut Vec::new(), &mut out);
    out
}

fn colour_transform(mate: &Key, permutation: &[usize; 3]) -> Key {
    let mut answer = [-1i8; PORTS];
    for vertex in 0..8 {
        for colour in 0..3 {
            let target = 3 * vertex + permutation[colour];
            let other = mate.0[3 * vertex + colour];
            if other >= 0 {
                let other = other as usize;
                answer[target] = (3 * (other / 3) + permutation[other % 3]) as i8;
            }
        }
    }
    Key(answer)
}

fn vertex_components(mate: &Key) -> Vec<Vec<usize>> {
    let mut adjacency = [0u8; 8];
    for port in 0..PORTS {
        let other = mate.0[port];
        if other >= 0 {
            let left = port / 3;
            let right = other as usize / 3;
            adjacency[left] |= 1 << right;
            adjacency[right] |= 1 << left;
        }
    }
    let mut unseen: u8 = 0xff;
    let mut answer = Vec::new();
    while unseen != 0 {
        let first = unseen.trailing_zeros() as usize;
        let mut component = Vec::new();
        let mut frontier = vec![first];
        let mut included = 0u8;
        while let Some(vertex) = frontier.pop() {
            if included & (1 << vertex) != 0 { continue; }
            included |= 1 << vertex;
            component.push(vertex);
            let mut neighbours = adjacency[vertex] & !included;
            while neighbours != 0 {
                let other = neighbours.trailing_zeros() as usize;
                neighbours &= !(1 << other);
                frontier.push(other);
            }
        }
        component.sort_unstable();
        unseen &= !included;
        answer.push(component);
    }
    answer
}

fn rooted_component_code(mate: &Key, component: &[usize], root: usize) -> Vec<i8> {
    let mut in_component = [false; 8];
    for &vertex in component { in_component[vertex] = true; }
    let mut order = vec![root];
    let mut label = [usize::MAX; 8];
    label[root] = 0;
    let mut cursor = 0;
    while cursor < order.len() {
        let vertex = order[cursor];
        for colour in 0..3 {
            let other = mate.0[3 * vertex + colour];
            if other >= 0 {
                let other_vertex = other as usize / 3;
                if label[other_vertex] == usize::MAX {
                    label[other_vertex] = order.len();
                    order.push(other_vertex);
                }
            }
        }
        cursor += 1;
    }
    assert_eq!(order.len(), component.len());
    assert!(order.iter().all(|&vertex| in_component[vertex]));
    let mut code = Vec::with_capacity(3 * component.len());
    for vertex in order {
        for colour in 0..3 {
            let other = mate.0[3 * vertex + colour];
            if other < 0 {
                code.push(-1);
            } else {
                let other = other as usize;
                code.push((3 * label[other / 3] + other % 3) as i8);
            }
        }
    }
    code
}

fn vertex_canonical_codes(mate: &Key) -> Vec<Vec<i8>> {
    let mut codes = Vec::new();
    for component in vertex_components(mate) {
        let mut best: Option<Vec<i8>> = None;
        for &root in &component {
            let code = rooted_component_code(mate, &component, root);
            if best.as_ref().is_none_or(|old| code < *old) { best = Some(code); }
        }
        codes.push(best.unwrap());
    }
    codes.sort();
    codes
}

fn decode_codes(codes: &[Vec<i8>]) -> Key {
    let mut answer = [-1i8; PORTS];
    let mut offset = 0usize;
    let mut cursor = 0usize;
    for code in codes {
        let size = code.len() / 3;
        for &value in code {
            answer[cursor] = if value < 0 {
                -1
            } else {
                let value = value as usize;
                (3 * (offset + value / 3) + value % 3) as i8
            };
            cursor += 1;
        }
        offset += size;
    }
    assert_eq!(cursor, PORTS);
    Key(answer)
}

fn canonical_key(mate: &Key) -> Key {
    const PERMS: [[usize; 3]; 6] = [
        [0, 1, 2], [0, 2, 1], [1, 0, 2],
        [1, 2, 0], [2, 0, 1], [2, 1, 0],
    ];
    let mut best: Option<Vec<Vec<i8>>> = None;
    for permutation in PERMS {
        let codes = vertex_canonical_codes(&colour_transform(mate, &permutation));
        if best.as_ref().is_none_or(|old| codes < *old) { best = Some(codes); }
    }
    decode_codes(&best.unwrap())
}

fn column_outputs(column: &Key, matchings: &[[(u8, u8); 4]]) -> Vec<Key> {
    let mut holes = [0usize; 8];
    for vertex in 0..8 {
        let missing: Vec<_> = (0..3)
            .filter(|&colour| column.0[3 * vertex + colour] < 0).collect();
        assert_eq!(missing.len(), 1, "column lacks one hole per vertex");
        holes[vertex] = missing[0];
    }
    let mut answer = Vec::with_capacity(matchings.len());
    for matching in matchings {
        let mut mate = *column;
        for &(left, right) in matching {
            let left = left as usize;
            let right = right as usize;
            let first = 3 * left + holes[left];
            let second = 3 * right + holes[right];
            mate.0[first] = second as i8;
            mate.0[second] = first as i8;
        }
        answer.push(canonical_key(&mate));
    }
    answer
}

fn incident_columns(row: &Key) -> Vec<Key> {
    let mut edges = Vec::new();
    for port in 0..PORTS {
        let other = row.0[port];
        if other >= 0 && port < other as usize { edges.push((port, other as usize)); }
    }
    let mut answer = HashSet::new();
    let n = edges.len();
    for a in 0..n {
        for b in a + 1..n {
            for c in b + 1..n {
                for d in c + 1..n {
                    let selected = [edges[a], edges[b], edges[c], edges[d]];
                    let mut vertices = 0u8;
                    let mut colours = 0u8;
                    let mut valid = true;
                    for &(first, second) in &selected {
                        let fv = first / 3;
                        let sv = second / 3;
                        if vertices & (1 << fv) != 0 || vertices & (1 << sv) != 0 {
                            valid = false;
                            break;
                        }
                        vertices |= (1 << fv) | (1 << sv);
                        colours |= (1 << (first % 3)) | (1 << (second % 3));
                    }
                    if !valid || vertices != 0xff || colours.count_ones() == 1 { continue; }
                    let mut multiplier = *row;
                    for &(first, second) in &selected {
                        multiplier.0[first] = -1;
                        multiplier.0[second] = -1;
                    }
                    answer.insert(canonical_key(&multiplier));
                }
            }
        }
    }
    let mut answer: Vec<_> = answer.into_iter().collect();
    answer.sort();
    answer
}

fn mod_inverse(value: u16) -> u16 {
    let mut base = value as u32;
    let mut exponent = PRIME as u32 - 2;
    let mut answer = 1u32;
    while exponent != 0 {
        if exponent & 1 != 0 { answer = answer * base % PRIME as u32; }
        base = base * base % PRIME as u32;
        exponent >>= 1;
    }
    answer as u16
}

type Sparse = Vec<(u32, u16)>;

fn add_scaled(target: &Sparse, source: &Sparse, scale: u16) -> Sparse {
    let mut answer = Vec::with_capacity(target.len() + source.len());
    let mut i = 0;
    let mut j = 0;
    while i < target.len() || j < source.len() {
        if j == source.len() || (i < target.len() && target[i].0 < source[j].0) {
            answer.push(target[i]);
            i += 1;
        } else if i == target.len() || source[j].0 < target[i].0 {
            let value = source[j].1 as u32 * scale as u32 % PRIME as u32;
            if value != 0 { answer.push((source[j].0, value as u16)); }
            j += 1;
        } else {
            let value = (target[i].1 as u32
                + source[j].1 as u32 * scale as u32) % PRIME as u32;
            if value != 0 { answer.push((target[i].0, value as u16)); }
            i += 1;
            j += 1;
        }
    }
    answer
}

fn scale_sparse(vector: &mut Sparse, scale: u16) {
    for (_, coefficient) in vector { *coefficient =
        (*coefficient as u32 * scale as u32 % PRIME as u32) as u16; }
}

fn aggregate(entries: impl IntoIterator<Item = (u32, u16)>) -> Sparse {
    let mut map: HashMap<u32, u16> = HashMap::new();
    for (row, coefficient) in entries {
        let value = (map.get(&row).copied().unwrap_or(0) as u32
            + coefficient as u32) % PRIME as u32;
        if value == 0 { map.remove(&row); } else { map.insert(row, value as u16); }
    }
    let mut answer: Vec<_> = map.into_iter().collect();
    answer.sort_unstable_by_key(|item| item.0);
    answer
}

type KeySparse = Vec<(Key, u16)>;

fn add_key_scaled(target: &KeySparse, source: &KeySparse, scale: u16) -> KeySparse {
    let mut answer = Vec::with_capacity(target.len() + source.len());
    let mut i = 0;
    let mut j = 0;
    while i < target.len() || j < source.len() {
        if j == source.len() || (i < target.len() && target[i].0 < source[j].0) {
            answer.push(target[i]);
            i += 1;
        } else if i == target.len() || source[j].0 < target[i].0 {
            let value = source[j].1 as u32 * scale as u32 % PRIME as u32;
            if value != 0 { answer.push((source[j].0, value as u16)); }
            j += 1;
        } else {
            let value = (target[i].1 as u32
                + source[j].1 as u32 * scale as u32) % PRIME as u32;
            if value != 0 { answer.push((target[i].0, value as u16)); }
            i += 1;
            j += 1;
        }
    }
    answer
}

fn next_key_vector(
    column: &Key,
    matchings: &[[(u8, u8); 4]],
    old_rows: &HashSet<Key>,
) -> KeySparse {
    let mut counts = HashMap::<Key, u16>::new();
    for row in column_outputs(column, matchings) {
        if old_rows.contains(&row) { continue; }
        let value = (counts.get(&row).copied().unwrap_or(0) + 1) % PRIME;
        if value == 0 { counts.remove(&row); } else { counts.insert(row, value); }
    }
    let mut answer: Vec<_> = counts.into_iter().collect();
    answer.sort_unstable_by_key(|item| item.0);
    answer
}

fn vector_for_column(
    column: &Key,
    matchings: &[[(u8, u8); 4]],
    row_ids: &HashMap<Key, u32>,
) -> Sparse {
    aggregate(column_outputs(column, matchings).into_iter().filter_map(|row| {
        row_ids.get(&row).copied().map(|id| (id, 1))
    }))
}

fn insert_basis(
    mut work: Sparse,
    origin: u32,
    basis: &mut [Option<Sparse>],
    basis_origin: &mut [u32],
    basis_scale: &mut [u16],
    basis_reductions: &mut [Option<Vec<(u32, u16)>>],
    basis_order: &mut Vec<u32>,
) -> Option<Sparse> {
    let mut reductions = Vec::new();
    while let Some(&(pivot, value)) = work.first() {
        if let Some(existing) = &basis[pivot as usize] {
            reductions.push((pivot, value));
            let scale = if value == 0 { 0 } else { PRIME - value };
            work = add_scaled(&work, existing, scale);
        } else {
            basis_origin[pivot as usize] = origin;
            basis_scale[pivot as usize] = value;
            basis_reductions[pivot as usize] = Some(reductions);
            basis_order.push(pivot);
            let inverse = mod_inverse(value);
            scale_sparse(&mut work, inverse);
            basis[pivot as usize] = Some(work);
            return None;
        }
    }
    Some(reductions)
}

fn reduce_basis(mut work: Sparse, basis: &[Option<Sparse>]) -> (Sparse, Sparse) {
    let mut coordinates = Vec::new();
    while let Some(&(pivot, value)) = work.first() {
        let Some(existing) = &basis[pivot as usize] else { break; };
        coordinates.push((pivot, value));
        let scale = if value == 0 { 0 } else { PRIME - value };
        work = add_scaled(&work, existing, scale);
    }
    (work, coordinates)
}

fn add_coordinate(map: &mut HashMap<u32, u16>, index: u32, delta: i32) {
    let old = map.get(&index).copied().unwrap_or(0) as i32;
    let mut value = (old + delta) % PRIME as i32;
    if value < 0 { value += PRIME as i32; }
    if value == 0 { map.remove(&index); } else { map.insert(index, value as u16); }
}

fn back_substitute(
    coordinates: &Sparse,
    basis_order: &[u32],
    basis_origin: &[u32],
    basis_scale: &[u16],
    basis_reductions: &[Option<Vec<(u32, u16)>>],
) -> Sparse {
    let mut pending: HashMap<u32, u16> = coordinates.iter().copied().collect();
    let mut source = HashMap::<u32, u16>::new();
    for &pivot in basis_order.iter().rev() {
        let coefficient = pending.remove(&pivot).unwrap_or(0);
        if coefficient == 0 { continue; }
        let scaled = (coefficient as u32 * mod_inverse(basis_scale[pivot as usize]) as u32
            % PRIME as u32) as u16;
        add_coordinate(&mut source, basis_origin[pivot as usize], scaled as i32);
        for &(earlier, value) in basis_reductions[pivot as usize].as_ref().unwrap() {
            let delta = -((scaled as u32 * value as u32 % PRIME as u32) as i32);
            add_coordinate(&mut pending, earlier, delta);
        }
    }
    assert!(pending.is_empty(), "unexpanded basis coordinates");
    let mut answer: Vec<_> = source.into_iter().collect();
    answer.sort_unstable_by_key(|item| item.0);
    answer
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let input_path = PathBuf::from(args.get(1).expect("usage: third-bockstein INPUT"));
    let started = Instant::now();
    let input = read_input(&input_path);
    eprintln!("loaded rows={} second={} kernels={} in {:?}",
        input.rows.len(), input.second.len(), input.kernels.len(), started.elapsed());

    let matchings = perfect_matchings(&(0u8..8).collect::<Vec<_>>());
    assert_eq!(matchings.len(), 105);

    for (column, expected) in &input.column_controls {
        assert_eq!(&column_outputs(column, &matchings), expected,
            "column-output cross-language control failed");
    }
    for (row, expected) in &input.row_controls {
        assert_eq!(&incident_columns(row), expected,
            "incident-column cross-language control failed");
    }
    eprintln!("cross-language controls passed in {:?}", started.elapsed());

    let row_ids: HashMap<Key, u32> = input.rows.iter().enumerate()
        .map(|(index, &row)| (row, index as u32)).collect();
    let used: HashSet<Key> = input.used.iter().copied().collect();

    let mut second_vectors = Vec::with_capacity(input.second.len());
    for (number, column) in input.second.iter().enumerate() {
        second_vectors.push(vector_for_column(column, &matchings, &row_ids));
        if (number + 1) % 2000 == 0 {
            eprintln!("projected second columns {}/{} in {:?}",
                number + 1, input.second.len(), started.elapsed());
        }
    }

    let mut kernel_tails = Vec::with_capacity(input.kernels.len());
    for kernel in &input.kernels {
        let mut tail = Vec::new();
        for &(correction, coefficient) in kernel {
            if let Some(vector) = second_vectors.get(correction as usize) {
                tail = add_scaled(&tail, vector, coefficient);
            }
        }
        kernel_tails.push(tail);
    }
    let kernel_terms: usize = kernel_tails.iter().map(Vec::len).sum();
    let kernel_nonzero = kernel_tails.iter().filter(|tail| !tail.is_empty()).count();
    eprintln!("projected kernel tails nonzero={} terms={} in {:?}",
        kernel_nonzero, kernel_terms, started.elapsed());

    let mut tails = Vec::with_capacity(input.tails.len());
    for tail in &input.tails {
        tails.push(aggregate(tail.iter().map(|(row, coefficient)| {
            (*row_ids.get(row).expect("tail row absent from third shell"), *coefficient)
        })));
    }

    let mut row_to_kernels = vec![Vec::<u32>::new(); input.rows.len()];
    for (number, tail) in kernel_tails.iter().enumerate() {
        for &(row, _) in tail { row_to_kernels[row as usize].push(number as u32); }
    }

    let mut queue = VecDeque::new();
    let mut reached = vec![false; input.rows.len()];
    for tail in &tails {
        for &(row, _) in tail {
            if !reached[row as usize] {
                reached[row as usize] = true;
                queue.push_back(row);
            }
        }
    }
    let mut reached_count = queue.len();
    let mut seen_columns = HashSet::<Key>::new();
    let mut seen_kernels = vec![false; kernel_tails.len()];
    let mut seen_kernel_count = 0usize;
    let mut literal_vectors = Vec::<Sparse>::new();
    let mut literal_columns = Vec::<Key>::new();

    while let Some(row) = queue.pop_front() {
        for &kernel_number in &row_to_kernels[row as usize] {
            let index = kernel_number as usize;
            if seen_kernels[index] { continue; }
            seen_kernels[index] = true;
            seen_kernel_count += 1;
            let vector = &kernel_tails[index];
            for &(other, _) in vector {
                if !reached[other as usize] {
                    reached[other as usize] = true;
                    reached_count += 1;
                    queue.push_back(other);
                }
            }
        }

        for column in incident_columns(&input.rows[row as usize]) {
            if used.contains(&column) || !seen_columns.insert(column) { continue; }
            let vector = vector_for_column(&column, &matchings, &row_ids);
            assert!(vector.binary_search_by_key(&row, |item| item.0).is_ok(),
                "incident column lost its seed row");
            for &(other, _) in &vector {
                if !reached[other as usize] {
                    reached[other as usize] = true;
                    reached_count += 1;
                    queue.push_back(other);
                }
            }
            literal_columns.push(column);
            literal_vectors.push(vector);
        }

        if reached_count % 10000 == 0 && queue.len() % 101 == 0 {
            eprintln!("closure rows={} queue={} columns={} kernels={} {:?}",
                reached_count, queue.len(), seen_columns.len(), seen_kernel_count,
                started.elapsed());
        }
    }

    eprintln!("closure complete rows={} columns={} kernels={} in {:?}",
        reached_count, literal_vectors.len(), seen_kernel_count, started.elapsed());

    // Pivot the short literal vectors first.  The inherited kernel tails
    // describe the same correction span regardless of insertion order, but
    // inserting their average 2,500+ terms first causes catastrophic fill.
    let mut basis = vec![None::<Sparse>; input.rows.len()];
    let mut basis_origin = vec![u32::MAX; input.rows.len()];
    let mut basis_scale = vec![0u16; input.rows.len()];
    let mut basis_reductions = vec![None::<Vec<(u32, u16)>>; input.rows.len()];
    let mut basis_order = Vec::<u32>::new();
    let mut correction_kernels = Vec::<Sparse>::new();
    let mut rank = 0usize;
    for (number, vector) in literal_vectors.iter().enumerate() {
        let dependent = insert_basis(
            vector.clone(), number as u32, &mut basis, &mut basis_origin,
            &mut basis_scale, &mut basis_reductions, &mut basis_order,
        );
        if let Some(coordinates) = dependent {
            let source = back_substitute(
                &coordinates, &basis_order, &basis_origin, &basis_scale,
                &basis_reductions,
            );
            correction_kernels.push(add_scaled(
                &vec![(number as u32, 1)], &source, PRIME - 1,
            ));
        } else { rank += 1; }
        if (number + 1) % 10000 == 0 {
            eprintln!("literal elimination {}/{} rank={} {:?}",
                number + 1, literal_vectors.len(), rank, started.elapsed());
        }
    }
    let mut inserted_kernels = 0usize;
    let mut kernel_origin_indices = Vec::<usize>::new();
    for (number, (&seen, vector)) in seen_kernels.iter().zip(&kernel_tails).enumerate() {
        if !seen { continue; }
        let origin = literal_vectors.len() as u32 + kernel_origin_indices.len() as u32;
        kernel_origin_indices.push(number);
        let dependent = insert_basis(
            vector.clone(), origin, &mut basis, &mut basis_origin,
            &mut basis_scale, &mut basis_reductions, &mut basis_order,
        );
        if let Some(coordinates) = dependent {
            let source = back_substitute(
                &coordinates, &basis_order, &basis_origin, &basis_scale,
                &basis_reductions,
            );
            correction_kernels.push(add_scaled(
                &vec![(origin, 1)], &source, PRIME - 1,
            ));
        } else { rank += 1; }
        inserted_kernels += 1;
        if inserted_kernels % 100 == 0 {
            eprintln!("kernel elimination {}/{} (source index {}) rank={} {:?}",
                inserted_kernels, seen_kernel_count, number, rank, started.elapsed());
        }
    }

    let mut remainders = Vec::new();
    let mut solutions = Vec::<Option<Sparse>>::new();
    for (target, tail) in tails.iter().enumerate() {
        let (remainder, coordinates) = reduce_basis(tail.clone(), &basis);
        remainders.push(remainder.len());
        if !remainder.is_empty() {
            solutions.push(None);
            continue;
        }
        let source = back_substitute(
            &coordinates, &basis_order, &basis_origin, &basis_scale,
            &basis_reductions,
        );
        let mut replay = Vec::new();
        for &(origin, coefficient) in &source {
            let origin = origin as usize;
            let vector = if origin < literal_vectors.len() {
                &literal_vectors[origin]
            } else {
                &kernel_tails[kernel_origin_indices[origin - literal_vectors.len()]]
            };
            replay = add_scaled(&replay, vector, coefficient);
        }
        assert_eq!(&replay, tail, "target source replay failed at {target}");
        solutions.push(Some(source));
    }

    let solution_path = input_path.with_extension("rsol");
    let mut solution_file = BufWriter::new(File::create(&solution_path)
        .expect("cannot create solution file"));
    solution_file.write_all(b"BCK3S001").unwrap();
    solution_file.write_all(&(PRIME as u32).to_le_bytes()).unwrap();
    solution_file.write_all(&(solutions.len() as u32).to_le_bytes()).unwrap();
    for solution in &solutions {
        let terms = solution.as_ref().map(Vec::as_slice).unwrap_or(&[]);
        solution_file.write_all(&(terms.len() as u32).to_le_bytes()).unwrap();
        for &(origin, coefficient) in terms {
            let origin = origin as usize;
            solution_file.write_all(&coefficient.to_le_bytes()).unwrap();
            if origin < literal_columns.len() {
                solution_file.write_all(&[0]).unwrap();
                let bytes: Vec<u8> = literal_columns[origin].0.iter()
                    .map(|&value| value as u8).collect();
                solution_file.write_all(&bytes).unwrap();
            } else {
                solution_file.write_all(&[1]).unwrap();
                let kernel = kernel_origin_indices[origin - literal_columns.len()] as u32;
                solution_file.write_all(&kernel.to_le_bytes()).unwrap();
            }
        }
    }
    solution_file.flush().unwrap();
    let correction_vectors = literal_vectors.len() + seen_kernel_count;
    let nullity = correction_vectors - rank;
    assert_eq!(correction_kernels.len(), nullity, "third nullity provenance changed");

    for (number, kernel) in correction_kernels.iter().enumerate() {
        let mut replay = Vec::new();
        for &(origin, coefficient) in kernel {
            let origin = origin as usize;
            let vector = if origin < literal_vectors.len() {
                &literal_vectors[origin]
            } else {
                &kernel_tails[kernel_origin_indices[origin - literal_vectors.len()]]
            };
            replay = add_scaled(&replay, vector, coefficient);
        }
        assert!(replay.is_empty(), "third kernel replay failed at {number}");
    }

    let old_rows: HashSet<Key> = input.old_rows.iter().copied().collect();
    let mut next_literal_vectors = Vec::<KeySparse>::with_capacity(literal_columns.len());
    let mut next_global_rows = HashSet::<Key>::new();
    for (number, column) in literal_columns.iter().enumerate() {
        let vector = next_key_vector(column, &matchings, &old_rows);
        next_global_rows.extend(vector.iter().map(|item| item.0));
        next_literal_vectors.push(vector);
        if (number + 1) % 5000 == 0 {
            eprintln!("next-tail projection {}/{} rows={} {:?}", number + 1,
                literal_columns.len(), next_global_rows.len(), started.elapsed());
        }
    }
    let mut next_target_tails = Vec::<KeySparse>::new();
    for solution in &solutions {
        let mut tail = Vec::new();
        for &(origin, coefficient) in solution.as_ref().map(Vec::as_slice).unwrap_or(&[]) {
            if (origin as usize) < literal_columns.len() {
                tail = add_key_scaled(&tail, &next_literal_vectors[origin as usize], coefficient);
            }
        }
        next_target_tails.push(tail);
    }
    let mut next_kernel_tails = Vec::<KeySparse>::new();
    for kernel in &correction_kernels {
        let mut tail = Vec::new();
        for &(origin, coefficient) in kernel {
            if (origin as usize) < literal_columns.len() {
                tail = add_key_scaled(&tail, &next_literal_vectors[origin as usize], coefficient);
            }
        }
        next_kernel_tails.push(tail);
    }
    let next_target_terms: Vec<_> = next_target_tails.iter().map(Vec::len).collect();
    let next_kernel_nonzero = next_kernel_tails.iter().filter(|tail| !tail.is_empty()).count();
    let next_kernel_terms: usize = next_kernel_tails.iter().map(Vec::len).sum();
    eprintln!("next page rows={} target_terms={:?} kernel_nonzero={} kernel_terms={} {:?}",
        next_global_rows.len(), next_target_terms, next_kernel_nonzero,
        next_kernel_terms, started.elapsed());
    println!("{{");
    println!("  \"prime\": {},", PRIME);
    println!("  \"third_global_rows\": {},", input.rows.len());
    println!("  \"reachable_rows\": {},", reached_count);
    println!("  \"reachable_literal_columns\": {},", seen_columns.len());
    println!("  \"reachable_inherited_kernel_tails\": {},", seen_kernel_count);
    println!("  \"correction_vectors\": {},", correction_vectors);
    println!("  \"correction_rank\": {},", rank);
    println!("  \"correction_nullity\": {},", nullity);
    println!("  \"kernel_third_tail_nonzero\": {},", kernel_nonzero);
    println!("  \"kernel_third_tail_terms\": {},", kernel_terms);
    println!("  \"next_global_rows_from_reachable_columns\": {},", next_global_rows.len());
    println!("  \"next_kernel_tail_nonzero\": {},", next_kernel_nonzero);
    println!("  \"next_kernel_tail_terms\": {},", next_kernel_terms);
    print!("  \"target_remainders\": [");
    for (index, value) in remainders.iter().enumerate() {
        if index != 0 { print!(", "); }
        print!("{}", value);
    }
    println!("],");
    print!("  \"next_target_tail_terms\": [");
    for (index, value) in next_target_terms.iter().enumerate() {
        if index != 0 { print!(", "); }
        print!("{}", value);
    }
    println!("],");
    print!("  \"target_solution_terms\": [");
    for (index, solution) in solutions.iter().enumerate() {
        if index != 0 { print!(", "); }
        match solution { Some(value) => print!("{}", value.len()), None => print!("null") }
    }
    println!("],");
    println!("  \"solution_file\": \"{}\",", solution_path.display());
    println!("  \"elapsed_seconds\": {:.3}", started.elapsed().as_secs_f64());
    println!("}}");
}
