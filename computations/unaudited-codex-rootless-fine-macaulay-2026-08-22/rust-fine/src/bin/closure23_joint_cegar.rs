use std::collections::{BTreeMap, BTreeSet, HashMap};
use std::env;
use std::fs;
use std::sync::atomic::{AtomicU32, Ordering};
use std::time::Instant;

static MODULUS: AtomicU32 = AtomicU32::new(32003);

fn p() -> u32 { MODULUS.load(Ordering::Relaxed) }
const EXTRA_WORD: &str = "00000200";
const NEXT_WORD: &str = "00202112";
const NEXT_WORD_2: &str = "00020212";
const CLOSURE22: [&str; 22] = [
    "01000000", "02000000", "02020000", "10000000", "11110101",
    "11111010", "11111100", "11111101", "11111110", "12000000",
    "12111111", "12121111", "20000000", "20200000", "21000000",
    "21111110", "21111111", "21112111", "22000000", "22111111",
    "22121111", "22211111",
];
const PROFILE71_MISSING: [&str; 40] = [
    "00000001", "00000002", "00000010", "00000020", "00000100",
    "00000200", "00001000", "00002000", "00010000", "00020000",
    "00100000", "00200000", "01111111", "02222222", "10111111",
    "11011111", "11101111", "11110111", "11111011", "11111112",
    "11111121", "11111211", "11112111", "11121111", "11211111",
    "12222222", "20222222", "21222222", "22022222", "22122222",
    "22202222", "22212222", "22220222", "22221222", "22222022",
    "22222122", "22222202", "22222212", "22222220", "22222221",
];
const SLICES: [[u8; 8]; 3] = [
    [0, 1, 2, 1, 1, 2, 2, 2],
    [0, 1, 2, 0, 0, 0, 0, 0],
    [0, 1, 2, 1, 1, 1, 1, 1],
];
const T_EDGES: [(u8, u8); 3] = [(0, 1), (0, 2), (1, 2)];

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Key([u8; 37]);

fn key_fingerprint(key: Key) -> u64 {
    let mut hash = 0xcbf29ce484222325u64;
    for byte in key.0 {
        hash ^= byte as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    hash
}

type Row = Vec<(Key, u16)>;
type InternedRow = Vec<(u32, u16)>;

enum StoredRow {
    Keys(Row),
    Interned(InternedRow),
}

enum InternSlot {
    One(u32),
    Collision(Vec<u32>),
}

#[derive(Clone)]
struct Generator {
    label: String,
    terms: Vec<Key>,
}

struct PoolIndex {
    term_owners: HashMap<Key, Vec<usize>>,
    matching_graphs: Vec<[u8; 28]>,
}

impl PoolIndex {
    fn new(generators: &[Generator], pm8: &[Vec<(u8, u8)>]) -> Self {
        let mut term_owners: HashMap<Key, Vec<usize>> = HashMap::new();
        for (index, generator) in generators.iter().enumerate() {
            for &term in &generator.terms {
                term_owners.entry(term).or_default().push(index);
            }
        }
        let matching_graphs = pm8.iter().map(|matching| {
            let key = matching_key(&[0; 8], matching);
            std::array::from_fn(|i| key.0[i])
        }).collect();
        Self { term_owners, matching_graphs }
    }
}

#[derive(Clone)]
struct Round {
    round: usize,
    rank_before: usize,
    remainder_terms_before: usize,
    dual_support: usize,
    crossing_candidates: usize,
    crossing_rows_selected: usize,
    crossing_words: BTreeMap<String, usize>,
    independent_rows_added: usize,
    rank_after: usize,
    basis_nnz_after: usize,
}

struct AllWordScan {
    mixed_words: usize,
    modular_crossing_words: usize,
    modular_crossing_translations: usize,
    modular_cheapest_word: String,
    modular_cheapest_word_crossings: usize,
    modular_profile71_crossings: BTreeMap<String, usize>,
    integer_crossing_words: usize,
    integer_crossing_translations: usize,
    integer_profile71_crossings: BTreeMap<String, usize>,
}

struct Basis {
    lookup: HashMap<Key, usize>,
    rows: Vec<StoredRow>,
    nnz: usize,
    reverse_pivot: bool,
    intern_columns: bool,
    column_ids: HashMap<u64, InternSlot>,
    column_keys: Vec<Key>,
    column_hash_collisions: usize,
}

impl Basis {
    fn new(reverse_pivot: bool, intern_columns: bool) -> Self {
        Self {
            lookup: HashMap::new(), rows: Vec::new(), nnz: 0, reverse_pivot,
            intern_columns, column_ids: HashMap::new(), column_keys: Vec::new(),
            column_hash_collisions: 0,
        }
    }

    fn len(&self) -> usize { self.rows.len() }
    fn nnz(&self) -> usize { self.nnz }
    fn interned_columns(&self) -> usize { self.column_keys.len() }
    fn column_hash_collisions(&self) -> usize { self.column_hash_collisions }

    fn intern(&mut self, key: Key) -> u32 {
        let fingerprint = key_fingerprint(key);
        if let Some(slot) = self.column_ids.get(&fingerprint) {
            match slot {
                InternSlot::One(id) if self.column_keys[*id as usize] == key => return *id,
                InternSlot::Collision(ids) => {
                    if let Some(&id) = ids.iter().find(|&&id| self.column_keys[id as usize] == key) {
                        return id;
                    }
                }
                InternSlot::One(_) => {}
            }
        }
        let id = u32::try_from(self.column_keys.len()).expect("column id fits u32");
        self.column_keys.push(key);
        match self.column_ids.get_mut(&fingerprint) {
            None => { self.column_ids.insert(fingerprint, InternSlot::One(id)); }
            Some(slot @ InternSlot::One(_)) => {
                let InternSlot::One(first) = *slot else { unreachable!() };
                *slot = InternSlot::Collision(vec![first, id]);
                self.column_hash_collisions += 1;
            }
            Some(InternSlot::Collision(ids)) => {
                ids.push(id);
                self.column_hash_collisions += 1;
            }
        }
        id
    }

    fn reduce(&self, mut row: Row) -> Row {
        loop {
            let pivot_entry = if self.reverse_pivot { row.last() } else { row.first() };
            let Some(&(pivot, coefficient)) = pivot_entry else { break };
            let Some(&index) = self.lookup.get(&pivot) else { break };
            row = match &self.rows[index] {
                StoredRow::Keys(right) => add_scaled(&row, right, p() - coefficient as u32),
                StoredRow::Interned(right) => add_scaled_interned(
                    &row, right, &self.column_keys, p() - coefficient as u32,
                ),
            };
        }
        row
    }

    fn insert(&mut self, row: Row) -> bool {
        let mut reduced = self.reduce(row);
        if reduced.is_empty() { return false; }
        let pivot_index = if self.reverse_pivot { reduced.len() - 1 } else { 0 };
        let pivot = reduced[pivot_index].0;
        let inverse = mod_pow(reduced[pivot_index].1 as u32, p() - 2);
        for (_, coefficient) in &mut reduced {
            *coefficient = ((*coefficient as u32 * inverse) % p()) as u16;
        }
        debug_assert_eq!(reduced[pivot_index].1, 1);
        let index = self.rows.len();
        assert!(self.lookup.insert(pivot, index).is_none());
        self.nnz += reduced.len();
        if self.intern_columns {
            let interned = reduced.into_iter().map(|(key, coefficient)| {
                (self.intern(key), coefficient)
            }).collect();
            self.rows.push(StoredRow::Interned(interned));
        } else {
            self.rows.push(StoredRow::Keys(reduced));
        }
        true
    }

    fn separating_dual(&self, remainder: &Row) -> BTreeMap<Key, u16> {
        assert!(!remainder.is_empty());
        let mut dual = BTreeMap::new();
        let remainder_pivot = if self.reverse_pivot {
            remainder.last().expect("nonempty remainder").0
        } else {
            remainder[0].0
        };
        dual.insert(remainder_pivot, 1u16);
        let mut pivots: Vec<Key> = self.lookup.keys().copied().collect();
        if self.reverse_pivot { pivots.sort_unstable(); }
        else { pivots.sort_unstable_by(|a, b| b.cmp(a)); }
        for pivot in pivots {
            let mut value = 0u64;
            match &self.rows[self.lookup[&pivot]] {
                StoredRow::Keys(row) => {
                    let nonpivots = if self.reverse_pivot {
                        &row[..row.len() - 1]
                    } else {
                        &row[1..]
                    };
                    for &(column, coefficient) in nonpivots {
                        if let Some(&right) = dual.get(&column) {
                            value += coefficient as u64 * right as u64;
                            if value >= (p() as u64) << 32 { value %= p() as u64; }
                        }
                    }
                }
                StoredRow::Interned(row) => {
                    let nonpivots = if self.reverse_pivot {
                        &row[..row.len() - 1]
                    } else {
                        &row[1..]
                    };
                    for &(column_id, coefficient) in nonpivots {
                        let column = self.column_keys[column_id as usize];
                        if let Some(&right) = dual.get(&column) {
                            value += coefficient as u64 * right as u64;
                            if value >= (p() as u64) << 32 { value %= p() as u64; }
                        }
                    }
                }
            }
            let value = (value % p() as u64) as u32;
            if value != 0 {
                dual.insert(pivot, (p() - value) as u16);
            }
        }
        let pairing = dot(remainder, &dual);
        assert_ne!(pairing, 0);
        dual
    }
}

fn mod_pow(mut base: u32, mut exponent: u32) -> u32 {
    let mut out = 1u32;
    while exponent != 0 {
        if exponent & 1 != 0 { out = (out as u64 * base as u64 % p() as u64) as u32; }
        base = (base as u64 * base as u64 % p() as u64) as u32;
        exponent >>= 1;
    }
    out
}

fn add_scaled(left: &Row, right: &Row, scale: u32) -> Row {
    let mut out = Vec::with_capacity(left.len() + right.len());
    let (mut i, mut j) = (0usize, 0usize);
    while i < left.len() || j < right.len() {
        if j == right.len() || (i < left.len() && left[i].0 < right[j].0) {
            out.push(left[i]);
            i += 1;
        } else if i == left.len() || right[j].0 < left[i].0 {
            let value = (right[j].1 as u32 * scale % p()) as u16;
            if value != 0 { out.push((right[j].0, value)); }
            j += 1;
        } else {
            let value = (left[i].1 as u32 + right[j].1 as u32 * scale) % p();
            if value != 0 { out.push((left[i].0, value as u16)); }
            i += 1;
            j += 1;
        }
    }
    out
}

fn add_scaled_interned(
    left: &Row, right: &InternedRow, column_keys: &[Key], scale: u32,
) -> Row {
    let mut out = Vec::with_capacity(left.len() + right.len());
    let (mut i, mut j) = (0usize, 0usize);
    while i < left.len() || j < right.len() {
        let right_key = if j < right.len() {
            Some(column_keys[right[j].0 as usize])
        } else { None };
        if j == right.len() || (i < left.len() && left[i].0 < right_key.unwrap()) {
            out.push(left[i]);
            i += 1;
        } else if i == left.len() || right_key.unwrap() < left[i].0 {
            let value = (right[j].1 as u32 * scale % p()) as u16;
            if value != 0 { out.push((right_key.unwrap(), value)); }
            j += 1;
        } else {
            let value = (left[i].1 as u32 + right[j].1 as u32 * scale) % p();
            if value != 0 { out.push((left[i].0, value as u16)); }
            i += 1;
            j += 1;
        }
    }
    out
}

fn dot(row: &Row, dual: &BTreeMap<Key, u16>) -> u16 {
    let mut value = 0u64;
    for &(column, coefficient) in row {
        if let Some(&right) = dual.get(&column) {
            value += coefficient as u64 * right as u64;
        }
    }
    (value % p() as u64) as u16
}

fn edge_index(u: u8, v: u8) -> usize {
    let mut index = 0usize;
    for a in 0..8u8 {
        for b in a + 1..8u8 {
            if (a, b) == (u, v) { return index; }
            index += 1;
        }
    }
    panic!("bad edge ({u},{v})")
}

fn key_add(left: Key, right: Key) -> Key {
    let mut out = [0u8; 37];
    for (i, value) in out.iter_mut().enumerate() {
        *value = left.0[i] + right.0[i];
    }
    Key(out)
}

fn key_sub(left: Key, right: Key) -> Option<Key> {
    let mut out = [0u8; 37];
    for (i, value) in out.iter_mut().enumerate() {
        if left.0[i] < right.0[i] { return None; }
        *value = left.0[i] - right.0[i];
    }
    Some(Key(out))
}

fn matching_key(word: &[u8; 8], matching: &[(u8, u8)]) -> Key {
    let mut out = [0u8; 37];
    for &(u, v) in matching {
        out[edge_index(u, v)] += 1;
        out[28 + 3 * word[u as usize] as usize + word[v as usize] as usize] += 1;
    }
    Key(out)
}

fn perfect_matchings(vertices: &[u8]) -> Vec<Vec<(u8, u8)>> {
    if vertices.is_empty() { return vec![Vec::new()]; }
    let first = vertices[0];
    let mut out = Vec::new();
    for pos in 1..vertices.len() {
        let second = vertices[pos];
        let mut rest = Vec::with_capacity(vertices.len() - 2);
        rest.extend_from_slice(&vertices[1..pos]);
        rest.extend_from_slice(&vertices[pos + 1..]);
        for tail in perfect_matchings(&rest) {
            let mut row = vec![(first.min(second), first.max(second))];
            row.extend(tail);
            out.push(row);
        }
    }
    out
}

fn parse_word(label: &str) -> [u8; 8] {
    let bytes = label.as_bytes();
    assert_eq!(bytes.len(), 8);
    std::array::from_fn(|i| bytes[i] - b'0')
}

fn make_generator(label: String, pm8: &[Vec<(u8, u8)>]) -> Generator {
    let word = parse_word(&label);
    let mut terms: Vec<Key> = pm8.iter().map(|m| matching_key(&word, m)).collect();
    terms.sort_unstable();
    terms.dedup();
    assert_eq!(terms.len(), 105);
    Generator { label, terms }
}

fn lazy_pool_generators(
    pm8: &[Vec<(u8, u8)>], all_mixed: bool,
) -> (Vec<Generator>, usize) {
    let mut labels: Vec<String> = CLOSURE22.iter().map(|value| value.to_string()).collect();
    let initial_count = labels.len();
    let existing: BTreeSet<String> = labels.iter().cloned().collect();
    for code in 0..3usize.pow(8) {
        let mut cursor = code;
        let mut word = [0u8; 8];
        for i in (0..8).rev() { word[i] = (cursor % 3) as u8; cursor /= 3; }
        if word.iter().all(|&value| value == word[0]) { continue; }
        let include = if all_mixed {
            true
        } else {
            let mut counts = [0usize; 3];
            for value in word { counts[value as usize] += 1; }
            counts.sort_unstable();
            counts == [0, 1, 7]
        };
        if include {
            let label = word_label(&word);
            if !existing.contains(&label) { labels.push(label); }
        }
    }
    let expected = if all_mixed { 6558 } else { 62 };
    require_len(labels.len(), expected, "lazy pool word count");
    (labels.into_iter().map(|label| make_generator(label, pm8)).collect(), initial_count)
}

fn require_len(actual: usize, expected: usize, label: &str) {
    assert_eq!(actual, expected, "{label}");
}

fn generators(
    pm8: &[Vec<(u8, u8)>], complete_profile71: bool,
    add_next_word: bool, add_next_word_2: bool, complete_profile62: bool,
) -> Vec<Generator> {
    let mut labels: Vec<String> = CLOSURE22.iter().map(|value| value.to_string()).collect();
    if complete_profile71 { labels.extend(PROFILE71_MISSING.iter().map(|value| value.to_string())); }
    else { labels.push(EXTRA_WORD.to_string()); }
    if add_next_word { labels.push(NEXT_WORD.to_string()); }
    if add_next_word_2 { labels.push(NEXT_WORD_2.to_string()); }
    if complete_profile62 {
        for code in 0..3usize.pow(8) {
            let mut cursor = code;
            let mut word = [0u8; 8];
            for i in (0..8).rev() { word[i] = (cursor % 3) as u8; cursor /= 3; }
            let mut counts = [0usize; 3];
            for value in word { counts[value as usize] += 1; }
            counts.sort_unstable();
            if counts == [0, 2, 6] { labels.push(word_label(&word)); }
        }
    }
    let unique: BTreeSet<String> = labels.iter().cloned().collect();
    labels = unique.into_iter().collect();
    // Restore the source's fixed order first; only orbit completions are sorted.
    let mut ordered = Vec::new();
    for label in CLOSURE22 {
        if let Some(position) = labels.iter().position(|value| value == label) {
            ordered.push(labels.remove(position));
        }
    }
    for label in PROFILE71_MISSING {
        if let Some(position) = labels.iter().position(|value| value == label) {
            ordered.push(labels.remove(position));
        }
    }
    for label in [EXTRA_WORD, NEXT_WORD, NEXT_WORD_2] {
        if let Some(position) = labels.iter().position(|value| value == label) {
            ordered.push(labels.remove(position));
        }
    }
    ordered.append(&mut labels);
    labels = ordered;
    let base_expected = (if complete_profile71 { 62 } else { 23 })
        + add_next_word as usize + add_next_word_2 as usize;
    assert_eq!(labels.len(), base_expected + if complete_profile62 { 159 } else { 0 });
    labels.into_iter().map(|label| make_generator(label, pm8)).collect()
}

fn word_label(word: &[u8; 8]) -> String {
    word.iter().map(|value| char::from(b'0' + *value)).collect()
}

fn is_profile71(word: &[u8; 8]) -> bool {
    let mut counts = [0usize; 3];
    for &value in word { counts[value as usize] += 1; }
    counts.sort_unstable();
    counts == [0, 1, 7]
}

fn parity(perm: [usize; 3]) -> i32 {
    let mut inversions = 0;
    for i in 0..3 { for j in i + 1..3 { if perm[i] > perm[j] { inversions += 1; } } }
    if inversions % 2 == 0 { 1 } else { -1 }
}

fn cofactor_keys(word: &[u8; 8], selected: (u8, u8), pm8: &[Vec<(u8, u8)>]) -> Vec<Key> {
    let mut out = Vec::new();
    for matching in pm8 {
        if matching.contains(&selected) {
            let rest: Vec<(u8, u8)> = matching.iter().copied().filter(|&e| e != selected).collect();
            out.push(matching_key(word, &rest));
        }
    }
    assert_eq!(out.len(), 15);
    out
}

fn target(pm8: &[Vec<(u8, u8)>]) -> Row {
    let cof: Vec<Vec<Vec<Key>>> = SLICES.iter().map(|word| {
        T_EDGES.iter().map(|&edge| cofactor_keys(word, edge, pm8)).collect()
    }).collect();
    let perms = [
        [0, 1, 2], [0, 2, 1], [1, 0, 2],
        [1, 2, 0], [2, 0, 1], [2, 1, 0],
    ];
    let cone = matching_key(&[0; 8], &pm8[0]);
    let mut map: BTreeMap<Key, u16> = BTreeMap::new();
    for perm in perms {
        let coefficient = if parity(perm) == 1 { 1u16 } else { (p() - 1) as u16 };
        for &a in &cof[0][perm[0]] {
            for &b in &cof[1][perm[1]] {
                for &c in &cof[2][perm[2]] {
                    let key = key_add(cone, key_add(a, key_add(b, c)));
                    let value = (map.get(&key).copied().unwrap_or(0) as u32 + coefficient as u32) % p();
                    if value == 0 { map.remove(&key); } else { map.insert(key, value as u16); }
                }
            }
        }
    }
    assert_eq!(map.len(), 13974);
    map.into_iter().collect()
}

fn translated_row(generator: &Generator, quotient: Key) -> Row {
    // Physical-edge coordinates make the 105 projected terms distinct.
    let mut row: Row = generator.terms.iter().map(|&term| (key_add(quotient, term), 1)).collect();
    row.sort_unstable_by_key(|entry| entry.0);
    row
}

fn initial_quotients(generator: &Generator, target: &Row) -> BTreeSet<Key> {
    let mut out = BTreeSet::new();
    for &(column, _) in target {
        for &term in &generator.terms {
            if let Some(q) = key_sub(column, term) { out.insert(q); }
        }
    }
    out
}

fn crossing_quotients(generator: &Generator, dual: &BTreeMap<Key, u16>) -> Vec<Key> {
    let mut pairings: HashMap<Key, u16> = HashMap::new();
    for (&column, &coefficient) in dual {
        for &term in &generator.terms {
            if let Some(quotient) = key_sub(column, term) {
                let value = (pairings.get(&quotient).copied().unwrap_or(0) as u32 + coefficient as u32) % p();
                if value == 0 { pairings.remove(&quotient); }
                else { pairings.insert(quotient, value as u16); }
            }
        }
    }
    let mut live: Vec<Key> = pairings.into_keys().collect();
    live.sort_unstable();
    live
}

fn histogram_divisors(caps: &[u8], degree: u8) -> Vec<[u8; 9]> {
    fn visit(
        position: usize, remaining: u8, caps: &[u8], current: &mut [u8; 9],
        out: &mut Vec<[u8; 9]>,
    ) {
        if position == 9 {
            if remaining == 0 { out.push(*current); }
            return;
        }
        for value in 0..=caps[position].min(remaining) {
            current[position] = value;
            visit(position + 1, remaining - value, caps, current, out);
        }
        current[position] = 0;
    }
    let mut out = Vec::new();
    visit(0, degree, caps, &mut [0u8; 9], &mut out);
    out
}

fn crossing_candidates_indexed(
    generators: &[Generator], dual: &BTreeMap<Key, u16>, index: &PoolIndex,
) -> (Vec<(usize, Key)>, BTreeMap<String, usize>) {
    let mut pairings: HashMap<(usize, Key), u16> = HashMap::new();
    for (&column, &coefficient) in dual {
        let histograms = histogram_divisors(&column.0[28..], 4);
        for graph in &index.matching_graphs {
            if (0..28).any(|i| column.0[i] < graph[i]) { continue; }
            for histogram in &histograms {
                let mut raw = [0u8; 37];
                raw[..28].copy_from_slice(graph);
                raw[28..].copy_from_slice(histogram);
                let term = Key(raw);
                let Some(owners) = index.term_owners.get(&term) else { continue };
                let quotient = key_sub(column, term).expect("divisor key");
                for &owner in owners {
                    let key = (owner, quotient);
                    let value = (pairings.get(&key).copied().unwrap_or(0) as u32
                        + coefficient as u32) % p();
                    if value == 0 { pairings.remove(&key); }
                    else { pairings.insert(key, value as u16); }
                }
            }
        }
    }
    let mut candidates: Vec<(usize, Key)> = pairings.into_keys().collect();
    candidates.sort_unstable();
    let mut crossing_words = BTreeMap::new();
    for &(generator_index, _) in &candidates {
        *crossing_words.entry(generators[generator_index].label.clone()).or_insert(0) += 1;
    }
    (candidates, crossing_words)
}

fn crossing_candidates_direct(
    generators: &[Generator], dual: &BTreeMap<Key, u16>,
) -> (Vec<(usize, Key)>, BTreeMap<String, usize>) {
    let mut candidates = Vec::new();
    let mut crossing_words = BTreeMap::new();
    for (generator_index, generator) in generators.iter().enumerate() {
        let live = crossing_quotients(generator, dual);
        if !live.is_empty() {
            crossing_words.insert(generator.label.clone(), live.len());
            candidates.extend(live.into_iter().map(|q| (generator_index, q)));
        }
    }
    (candidates, crossing_words)
}

fn balanced(value: u16) -> i32 {
    if value as u32 <= p() / 2 { value as i32 } else { value as i32 - p() as i32 }
}

fn integer_crossings(
    generators: &[Generator], dual: &BTreeMap<Key, u16>, target: &Row,
) -> (usize, BTreeMap<String, usize>, i32, i64) {
    let integer_dual: BTreeMap<Key, i32> = dual.iter().map(|(&k, &v)| (k, balanced(v))).collect();
    let mut total = 0usize;
    let mut by_word = BTreeMap::new();
    let mut max_abs = 0i32;
    for generator in generators {
        let mut pairings: HashMap<Key, i32> = HashMap::new();
        for (&column, &coefficient) in &integer_dual {
            for &term in &generator.terms {
                if let Some(q) = key_sub(column, term) {
                    *pairings.entry(q).or_insert(0) += coefficient;
                }
            }
        }
        let values: Vec<i32> = pairings.into_values().filter(|&v| v != 0).collect();
        if !values.is_empty() {
            total += values.len();
            by_word.insert(generator.label.clone(), values.len());
            max_abs = max_abs.max(values.iter().map(|v| v.abs()).max().unwrap());
        }
    }
    let target_pairing = target.iter().map(|(column, coefficient)| {
        balanced(*coefficient) as i64 * integer_dual.get(column).copied().unwrap_or(0) as i64
    }).sum();
    (total, by_word, max_abs, target_pairing)
}

fn scan_all_words(pm8: &[Vec<(u8, u8)>], dual: &BTreeMap<Key, u16>) -> AllWordScan {
    let integer_dual: BTreeMap<Key, i32> = dual.iter().map(|(&k, &v)| (k, balanced(v))).collect();
    let mut modular_crossing_words = 0usize;
    let mut modular_crossing_translations = 0usize;
    let mut modular_cheapest_word = String::new();
    let mut modular_cheapest_word_crossings = usize::MAX;
    let mut modular_profile71_crossings = BTreeMap::new();
    let mut integer_crossing_words = 0usize;
    let mut integer_crossing_translations = 0usize;
    let mut integer_profile71_crossings = BTreeMap::new();
    let mut mixed_words = 0usize;
    for code in 0..3usize.pow(8) {
        let mut cursor = code;
        let mut word = [0u8; 8];
        for i in (0..8).rev() { word[i] = (cursor % 3) as u8; cursor /= 3; }
        if word.iter().all(|&value| value == word[0]) { continue; }
        mixed_words += 1;
        let terms: Vec<Key> = pm8.iter().map(|matching| matching_key(&word, matching)).collect();
        let mut pairings: HashMap<Key, i32> = HashMap::new();
        for (&column, &coefficient) in &integer_dual {
            for &term in &terms {
                if let Some(q) = key_sub(column, term) {
                    *pairings.entry(q).or_insert(0) += coefficient;
                }
            }
        }
        let values: Vec<i32> = pairings.into_values().collect();
        let integer_live = values.iter().filter(|&&value| value != 0).count();
        let modular_live = values.iter().filter(|&&value| value.rem_euclid(p() as i32) != 0).count();
        if integer_live != 0 {
            integer_crossing_words += 1;
            integer_crossing_translations += integer_live;
            if is_profile71(&word) {
                integer_profile71_crossings.insert(word_label(&word), integer_live);
            }
        }
        if modular_live == 0 { continue; }
        let label = word_label(&word);
        modular_crossing_words += 1;
        modular_crossing_translations += modular_live;
        if (modular_live, &label) < (modular_cheapest_word_crossings, &modular_cheapest_word) {
            modular_cheapest_word_crossings = modular_live;
            modular_cheapest_word = label.clone();
        }
        if is_profile71(&word) { modular_profile71_crossings.insert(label, modular_live); }
    }
    if modular_crossing_words == 0 { modular_cheapest_word_crossings = 0; }
    AllWordScan {
        mixed_words, modular_crossing_words, modular_crossing_translations,
        modular_cheapest_word, modular_cheapest_word_crossings,
        modular_profile71_crossings, integer_crossing_words,
        integer_crossing_translations, integer_profile71_crossings,
    }
}

fn python_repr(row: &Row) -> String {
    let mut out = String::from("[");
    for (entry_index, (key, coefficient)) in row.iter().enumerate() {
        if entry_index != 0 { out.push_str(", "); }
        out.push('(');
        out.push('(');
        for (i, value) in key.0.iter().enumerate() {
            if i != 0 { out.push_str(", "); }
            out.push_str(&value.to_string());
        }
        out.push_str("), ");
        out.push_str(&coefficient.to_string());
        out.push(')');
    }
    out.push(']');
    out
}

// Dependency-free SHA-256 for byte-identical comparison with the Python artifact.
fn sha256(input: &[u8]) -> [u8; 32] {
    const K: [u32; 64] = [
        0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
        0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
        0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
        0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
        0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
        0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
        0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
        0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2,
    ];
    let mut bytes = input.to_vec();
    let bit_len = (bytes.len() as u64) * 8;
    bytes.push(0x80);
    while bytes.len() % 64 != 56 { bytes.push(0); }
    bytes.extend_from_slice(&bit_len.to_be_bytes());
    let mut h = [0x6a09e667u32,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
    for chunk in bytes.chunks_exact(64) {
        let mut w = [0u32; 64];
        for i in 0..16 { w[i] = u32::from_be_bytes(chunk[4*i..4*i+4].try_into().unwrap()); }
        for i in 16..64 {
            let s0 = w[i-15].rotate_right(7) ^ w[i-15].rotate_right(18) ^ (w[i-15] >> 3);
            let s1 = w[i-2].rotate_right(17) ^ w[i-2].rotate_right(19) ^ (w[i-2] >> 10);
            w[i] = w[i-16].wrapping_add(s0).wrapping_add(w[i-7]).wrapping_add(s1);
        }
        let [mut a,mut b,mut c,mut d,mut e,mut f,mut g,mut hh] = h;
        for i in 0..64 {
            let s1 = e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25);
            let ch = (e & f) ^ ((!e) & g);
            let t1 = hh.wrapping_add(s1).wrapping_add(ch).wrapping_add(K[i]).wrapping_add(w[i]);
            let s0 = a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22);
            let maj = (a & b) ^ (a & c) ^ (b & c);
            let t2 = s0.wrapping_add(maj);
            hh=g; g=f; f=e; e=d.wrapping_add(t1); d=c; c=b; b=a; a=t1.wrapping_add(t2);
        }
        let values = [a,b,c,d,e,f,g,hh];
        for i in 0..8 { h[i] = h[i].wrapping_add(values[i]); }
    }
    let mut out = [0u8; 32];
    for i in 0..8 { out[4*i..4*i+4].copy_from_slice(&h[i].to_be_bytes()); }
    out
}

fn hex(bytes: &[u8]) -> String { bytes.iter().map(|b| format!("{b:02x}")).collect() }

fn is_prime(value: u32) -> bool {
    if value < 2 { return false; }
    let mut divisor = 2u32;
    while divisor * divisor <= value {
        if value % divisor == 0 { return false; }
        divisor += if divisor == 2 { 1 } else { 2 };
    }
    true
}

fn key_json(key: Key) -> String {
    format!("[{}]", key.0.iter().map(u8::to_string).collect::<Vec<_>>().join(","))
}

fn string_array_json(values: &[&str]) -> String {
    format!("[{}]", values.iter().map(|s| format!("\"{s}\"")).collect::<Vec<_>>().join(","))
}

fn usize_map_json(values: &BTreeMap<String, usize>) -> String {
    format!("{{{}}}", values.iter().map(|(k,v)| format!("\"{k}\":{v}")).collect::<Vec<_>>().join(","))
}

fn result_json(
    max_rounds: usize, crossing_cap: usize, elapsed_ms: u128,
    reverse_pivot: bool, intern_columns: bool,
    source_words: &[&str], extra_words: &[&str],
    complete_profile71: bool, initial_source_word_count: usize, lazy_pool_kind: &str,
    initial_rows: usize, initial_independent: usize,
    rounds: &[Round], terminal: &str, basis: &Basis, final_remainder: &Row,
    final_dual: &BTreeMap<Key, u16>, integer_crossing_translations: usize,
    integer_crossing_words: &BTreeMap<String, usize>, integer_max_abs: i32,
    integer_target_pairing: i64, all_word_scan: Option<&AllWordScan>,
) -> String {
    let balanced_max = final_dual.values().map(|&v| balanced(v).abs()).max().unwrap_or(0);
    let remainder_sha = hex(&sha256(python_repr(final_remainder).as_bytes()));
    let mut out = String::from("{\n");
    macro_rules! field { ($name:expr, $value:expr) => {{ out.push_str(&format!("  \"{}\": {},\n", $name, $value)); }} }
    field!("status", if final_remainder.is_empty() { "\"PASS closure22 joint-semigroup exchange reached target\"" } else { "\"INCOMPLETE closure22 joint-semigroup exchange\"" });
    field!("prime", p());
    field!("source_words", string_array_json(source_words));
    field!("initial_source_word_count", initial_source_word_count);
    field!("available_generator_pool_words", source_words.len());
    field!("lazy_pool_kind", format!("\"{lazy_pool_kind}\""));
    field!("indexed_scanner_round1_crosscheck", lazy_pool_kind != "none");
    field!("added_complete_profile71_orbit", complete_profile71);
    field!("extra_words", string_array_json(extra_words));
    field!("max_rounds", max_rounds);
    field!("crossing_cap", if crossing_cap == usize::MAX {
        "null".to_string()
    } else { crossing_cap.to_string() });
    field!("pivot_order", if reverse_pivot { "\"reverse_lex\"" } else { "\"forward_lex\"" });
    field!("column_storage", if intern_columns { "\"global_u32_interner\"" } else { "\"inline_key\"" });
    field!("elapsed_ms", elapsed_ms);
    field!("initial_target_touching_rows", initial_rows);
    field!("initial_independent_rows", initial_independent);
    out.push_str("  \"rounds\": [\n");
    for (i, round) in rounds.iter().enumerate() {
        out.push_str(&format!(concat!(
            "    {{\"round\":{},\"rank_before\":{},\"remainder_terms_before\":{},",
            "\"dual_support\":{},\"crossing_candidates\":{},\"crossing_rows_selected\":{},",
            "\"crossing_words\":{},\"independent_rows_added\":{},\"rank_after\":{},",
            "\"basis_nnz_after\":{}}}{}\n"),
            round.round, round.rank_before, round.remainder_terms_before,
            round.dual_support, round.crossing_candidates, round.crossing_rows_selected,
            usize_map_json(&round.crossing_words),
            round.independent_rows_added, round.rank_after, round.basis_nnz_after,
            if i + 1 == rounds.len() { "" } else { "," }));
    }
    out.push_str("  ],\n");
    field!("terminal", format!("\"{terminal}\""));
    field!("final_rank", basis.len());
    field!("final_basis_nnz", basis.nnz());
    field!("final_interned_columns", basis.interned_columns());
    field!("final_column_hash_collisions", basis.column_hash_collisions());
    field!("final_remainder_terms", final_remainder.len());
    field!("target_reduced_to_zero", final_remainder.is_empty());
    field!("terminal_modular_dual_support", final_dual.len());
    field!("terminal_integer_dual_balanced_max_abs", balanced_max);
    field!("terminal_integer_crossing_translations", integer_crossing_translations);
    field!("terminal_integer_crossing_words", usize_map_json(integer_crossing_words));
    field!("terminal_integer_max_abs_translation_pairing", integer_max_abs);
    field!("terminal_integer_target_pairing", integer_target_pairing);
    field!("terminal_integer_is_full_semigroup_separator", !final_dual.is_empty() && integer_crossing_translations == 0 && integer_target_pairing != 0);
    let dual_json = if final_dual.len() <= 256 {
        format!("[{}]", final_dual.iter().map(|(&column,&coefficient)| {
            format!("{{\"column\":{},\"coefficient\":{}}}", key_json(column), balanced(coefficient))
        }).collect::<Vec<_>>().join(","))
    } else { "[]".to_string() };
    field!("terminal_integer_dual", dual_json);
    field!("final_remainder_sha256", format!("\"{remainder_sha}\""));
    if let Some(scan) = all_word_scan {
        let modular_profile = format!("{{{}}}", scan.modular_profile71_crossings.iter().map(|(k,v)| {
            format!("\"{k}\":{v}")
        }).collect::<Vec<_>>().join(","));
        let integer_profile = format!("{{{}}}", scan.integer_profile71_crossings.iter().map(|(k,v)| {
            format!("\"{k}\":{v}")
        }).collect::<Vec<_>>().join(","));
        field!("all_word_scan", format!(concat!(
            "{{\"mixed_words\":{},\"modular_crossing_words\":{},\"modular_crossing_translations\":{},",
            "\"modular_cheapest_word\":\"{}\",\"modular_cheapest_word_crossings\":{},",
            "\"modular_profile71_crossings\":{},\"integer_crossing_words\":{},",
            "\"integer_crossing_translations\":{},\"integer_profile71_crossings\":{}}}"),
            scan.mixed_words, scan.modular_crossing_words, scan.modular_crossing_translations,
            scan.modular_cheapest_word, scan.modular_cheapest_word_crossings, modular_profile,
            scan.integer_crossing_words, scan.integer_crossing_translations, integer_profile));
    }
    out.push_str("  \"scope\": \"Exact F_32003 closure in the abstract joint edge/colour semigroup; fixed word set closure22 plus 00000200.\"\n");
    out.push_str("}\n");
    out
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut max_rounds = 256usize;
    let mut prime = 32003u32;
    let mut crossing_cap = usize::MAX;
    let mut reverse_pivot = false;
    let mut intern_columns = false;
    let mut output = "results_closure22_plus_00000200_joint_cegar_rust.json".to_string();
    let mut complete_profile71 = false;
    let mut add_next_word = false;
    let mut add_next_word_2 = false;
    let mut complete_profile62 = false;
    let mut scan_all = false;
    let mut lazy_pool_profile71 = false;
    let mut lazy_pool_all = false;
    let mut i = 1usize;
    while i < args.len() {
        match args[i].as_str() {
            "--max-rounds" => { i += 1; max_rounds = args[i].parse().expect("integer max rounds"); }
            "--prime" => { i += 1; prime = args[i].parse().expect("integer prime"); }
            "--crossing-cap" => { i += 1; crossing_cap = args[i].parse().expect("integer crossing cap"); }
            "--reverse-pivot" => { reverse_pivot = true; }
            "--intern-columns" => { intern_columns = true; }
            "--output" => { i += 1; output = args[i].clone(); }
            "--complete-profile71" => { complete_profile71 = true; }
            "--add-next-word" => { add_next_word = true; }
            "--add-next-word-2" => { add_next_word_2 = true; }
            "--complete-profile62" => { complete_profile62 = true; }
            "--scan-all-words" => { scan_all = true; }
            "--lazy-pool-profile71" => { lazy_pool_profile71 = true; }
            "--lazy-pool-all" => { lazy_pool_all = true; }
            other => panic!("unknown argument {other}"),
        }
        i += 1;
    }
    assert!(prime <= u16::MAX as u32 && is_prime(prime), "prime must be prime and fit u16");
    MODULUS.store(prime, Ordering::Relaxed);
    let start = Instant::now();
    let pm8 = perfect_matchings(&(0u8..8).collect::<Vec<_>>());
    assert_eq!(pm8.len(), 105);
    assert!(!add_next_word || complete_profile71, "next word requires full profile71 base");
    assert!(!add_next_word_2 || add_next_word, "second next word requires first next word");
    assert!(!complete_profile62 || complete_profile71,
            "profile62 completion requires full profile71 base");
    assert!(!(lazy_pool_profile71 && lazy_pool_all), "choose one lazy pool");
    assert!(!(lazy_pool_profile71 || lazy_pool_all) ||
            !(complete_profile71 || complete_profile62 || add_next_word || add_next_word_2),
            "lazy pools use the closure22 initial basis and no eager completion flags");
    let (generators, initial_source_word_count, lazy_pool_kind) = if lazy_pool_all {
        let (pool, initial) = lazy_pool_generators(&pm8, true);
        (pool, initial, "all_6558_mixed_X5")
    } else if lazy_pool_profile71 {
        let (pool, initial) = lazy_pool_generators(&pm8, false);
        (pool, initial, "full_profile71")
    } else {
        let eager = generators(
            &pm8, complete_profile71, add_next_word, add_next_word_2,
            complete_profile62,
        );
        let count = eager.len();
        (eager, count, "none")
    };
    let source_words: Vec<&str> = generators.iter().map(|generator| generator.label.as_str()).collect();
    let closure22_set: BTreeSet<&str> = CLOSURE22.into_iter().collect();
    let extra_words: Vec<&str> = source_words.iter().copied()
        .filter(|label| !closure22_set.contains(label)).collect();
    let target = target(&pm8);
    let pool_index = if lazy_pool_kind == "none" {
        None
    } else {
        Some(PoolIndex::new(&generators, &pm8))
    };
    eprintln!("target={} initial_generators={} pool_generators={} lazy_pool={}",
        target.len(), initial_source_word_count, generators.len(), lazy_pool_kind);

    let mut basis = Basis::new(reverse_pivot, intern_columns);
    let mut initial_rows = 0usize;
    let mut initial_independent = 0usize;
    for generator in generators.iter().take(initial_source_word_count) {
        let quotients = initial_quotients(generator, &target);
        initial_rows += quotients.len();
        for quotient in quotients {
            initial_independent += basis.insert(translated_row(generator, quotient)) as usize;
        }
        eprintln!("init {} rank={} rows={} nnz={} columns={} collisions={} elapsed={:.2?}",
            generator.label, basis.len(), initial_rows, basis.nnz(),
            basis.interned_columns(), basis.column_hash_collisions(), start.elapsed());
    }

    let mut rounds = Vec::new();
    let mut terminal = "round cap";
    for round_index in 0..=max_rounds {
        let remainder = basis.reduce(target.clone());
        if remainder.is_empty() { terminal = "target reduced to zero"; break; }
        let dual = basis.separating_dual(&remainder);
        if round_index == max_rounds { break; }
        let (candidates, crossing_words) = if let Some(index) = &pool_index {
            let indexed = crossing_candidates_indexed(&generators, &dual, index);
            if round_index == 0 {
                let direct = crossing_candidates_direct(&generators, &dual);
                assert_eq!(indexed.0, direct.0, "indexed/direct candidate mismatch");
                assert_eq!(indexed.1, direct.1, "indexed/direct word census mismatch");
                eprintln!("indexed scanner round1 crosscheck PASS candidates={}", indexed.0.len());
            }
            indexed
        } else {
            crossing_candidates_direct(&generators, &dual)
        };
        let rank_before = basis.len();
        let candidate_count = candidates.len();
        let mut selected_count = 0usize;
        let mut added = 0usize;
        for (generator_index, quotient) in candidates {
            if added == crossing_cap { break; }
            selected_count += 1;
            added += basis.insert(translated_row(&generators[generator_index], quotient)) as usize;
        }
        rounds.push(Round {
            round: round_index + 1, rank_before,
            remainder_terms_before: remainder.len(), dual_support: dual.len(),
            crossing_candidates: candidate_count, crossing_rows_selected: selected_count,
            crossing_words,
            independent_rows_added: added, rank_after: basis.len(), basis_nnz_after: basis.nnz(),
        });
        eprintln!("round={} candidates={} selected={} added={} rank={} rem={} dual={} nnz={} columns={} collisions={} elapsed={:.2?}",
            round_index + 1, candidate_count, selected_count, added,
            basis.len(), remainder.len(), dual.len(), basis.nnz(),
            basis.interned_columns(), basis.column_hash_collisions(), start.elapsed());
        if round_index == 0 && lazy_pool_all && crossing_cap == 256 {
            assert_eq!(added, 256, "round1 capped rank guard");
        }
        if added == 0 { terminal = "no existing-word exchange row crosses separator"; break; }
    }
    let final_remainder = basis.reduce(target.clone());
    let final_dual = if final_remainder.is_empty() { BTreeMap::new() } else { basis.separating_dual(&final_remainder) };
    let (integer_crossing_translations, integer_crossing_words, integer_max_abs, integer_target_pairing) =
        integer_crossings(&generators, &final_dual, &target);
    let all_word_scan = if scan_all {
        eprintln!("scanning all 6558 mixed words against terminal dual...");
        Some(scan_all_words(&pm8, &final_dual))
    } else { None };
    let text = result_json(
        max_rounds, crossing_cap, start.elapsed().as_millis(), reverse_pivot,
        intern_columns,
        &source_words, &extra_words,
        complete_profile71 || lazy_pool_profile71 || lazy_pool_all,
        initial_source_word_count, lazy_pool_kind, initial_rows, initial_independent,
        &rounds, terminal, &basis, &final_remainder, &final_dual,
        integer_crossing_translations, &integer_crossing_words, integer_max_abs,
        integer_target_pairing, all_word_scan.as_ref(),
    );
    fs::write(&output, text).expect("write result");
    eprintln!("wrote {output}; terminal={terminal}; rank={}; remainder={}; elapsed={:.2?}", basis.len(), final_remainder.len(), start.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sha256_guard() {
        assert_eq!(hex(&sha256(b"abc")), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
    }

    #[test]
    fn matching_and_target_guards() {
        let pm8 = perfect_matchings(&(0u8..8).collect::<Vec<_>>());
        assert_eq!(pm8.len(), 105);
        assert_eq!(target(&pm8).len(), 13974);
    }
}
