//! Resumable source-faithful degree-eleven dual CEGAR for the four canonical X5
//! branches.  The selected-column checkpoint is parsed
//! literally.  A pivot order frozen at resume time permits exact incremental
//! elimination instead of rebuilding the whole selected system every round.

use std::collections::{BTreeMap, HashMap, HashSet};
use std::env;
use std::fs::{self, File};
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

const DEGREE: usize = 11;
const EXPECTED_VARIABLES: usize = 361;
const EXPECTED_EQUATIONS: usize = 6571;
const T_ID: u16 = 361;

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Mono([u16; DEGREE]);

impl Hash for Mono {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.0.hash(state);
    }
}

impl Mono {
    fn from_sorted_slice(ids: &[u16]) -> Self {
        if ids.len() > DEGREE {
            fail("monomial exceeds degree eleven");
        }
        let mut packed = [u16::MAX; DEGREE];
        packed[..ids.len()].copy_from_slice(ids);
        Self(packed)
    }

    fn new(mut ids: Vec<u16>) -> Self {
        ids.sort_unstable();
        Self::from_sorted_slice(&ids)
    }

    fn degree(&self) -> usize {
        self.0.iter().take_while(|&&id| id != u16::MAX).count()
    }

    fn ids(&self) -> &[u16] {
        &self.0[..self.degree()]
    }

    fn concat(&self, other: &Mono) -> Self {
        let mut ids = Vec::with_capacity(self.degree() + other.degree());
        ids.extend_from_slice(self.ids());
        ids.extend_from_slice(other.ids());
        Self::new(ids)
    }

    fn quotient(&self, divisor: &Mono) -> Option<Self> {
        let source = self.ids();
        let divide = divisor.ids();
        let (mut i, mut j) = (0usize, 0usize);
        let mut answer = Vec::with_capacity(source.len().saturating_sub(divide.len()));
        while i < source.len() {
            if j < divide.len() && source[i] == divide[j] {
                i += 1;
                j += 1;
            } else {
                if j < divide.len() && divide[j] < source[i] {
                    return None;
                }
                answer.push(source[i]);
                i += 1;
            }
        }
        if j == divide.len() {
            Some(Self::from_sorted_slice(&answer))
        } else {
            None
        }
    }

    fn text(&self) -> String {
        self.ids()
            .iter()
            .map(u16::to_string)
            .collect::<Vec<_>>()
            .join(",")
    }
}

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column {
    generator: u16,
    multiplier: Mono,
}

struct Generator {
    degree: usize,
    terms: Vec<(Mono, i32)>,
}

struct Provider {
    variables: Vec<String>,
    generators: Vec<Generator>,
    term_index: HashMap<Mono, Vec<u16>>,
    parsed_terms: usize,
    degree_histogram: [usize; DEGREE + 1],
}

struct Config {
    branch: String,
    input: PathBuf,
    source_provider: PathBuf,
    output: PathBuf,
    repair_dual: PathBuf,
    resume_dual: PathBuf,
    prime: u64,
    wall_seconds: u64,
    // Retained only so the sealed parent writer remains type-checkable; the
    // transport-only main never reads or writes these checkpoint fields.
    selected: PathBuf,
    dual: PathBuf,
    resume_selected: PathBuf,
    resume_round_offset: usize,
    column_cap: usize,
}

const MAX_SMALL_REPAIR_COLUMNS: usize = 100_000;

#[derive(Clone)]
struct RoundRecord {
    round: usize,
    columns_before: usize,
    incident_columns_checked: usize,
    new_violations: usize,
    columns_after: usize,
    support_after: usize,
    incidence_seconds: f64,
    solve_seconds: f64,
}

struct Scan {
    violations: Vec<(Column, Vec<(Mono, u64)>)>,
    incident_checked: usize,
    truncated: bool,
    wall_hit: bool,
}

struct TransportScan {
    violation_columns: Vec<Column>,
    violation_rows: HashSet<Mono>,
    incident_checked: usize,
    wall_hit: bool,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("x5-four-blocker-d6-cegar: {}", message.as_ref());
    std::process::exit(2)
}

fn json_escape(text: &str) -> String {
    text.replace('\\', "\\\\").replace('"', "\\\"")
}

fn parse_args() -> Config {
    let args: Vec<String> = env::args().collect();
    let mut values = HashMap::<String, String>::new();
    let mut index = 1usize;
    while index < args.len() {
        if index + 1 >= args.len() || !args[index].starts_with("--") {
            fail("expected --key value arguments");
        }
        if values
            .insert(args[index].clone(), args[index + 1].clone())
            .is_some()
        {
            fail("duplicate argument");
        }
        index += 2;
    }
    let get = |key: &str| {
        values
            .get(key)
            .cloned()
            .unwrap_or_else(|| fail(format!("missing {key}")))
    };
    if values.len() != 8 {
        fail("unknown or missing argument");
    }
    let branch = get("--branch");
    if !matches!(
        branch.as_str(),
        "third_colour" | "cap_endpoint_colour"
    ) {
        fail("transport diagnostic accepts only third_colour/cap_endpoint_colour");
    }
    let prime = get("--prime").parse().unwrap_or_else(|_| fail("bad prime"));
    let wall_seconds = get("--wall-seconds")
        .parse()
        .unwrap_or_else(|_| fail("bad wall cap"));
    if prime != 1_073_741_827 {
        fail("transport diagnostic is frozen to p1073741827");
    }
    if wall_seconds == 0 || wall_seconds > 110 {
        fail("wall cap outside frozen contract");
    }
    Config {
        branch,
        input: PathBuf::from(get("--input")),
        source_provider: PathBuf::from(get("--source-provider")),
        output: PathBuf::from(get("--output")),
        repair_dual: PathBuf::from(get("--repair-dual")),
        resume_dual: PathBuf::from(get("--resume-dual")),
        prime,
        wall_seconds,
        selected: PathBuf::new(),
        dual: PathBuf::new(),
        resume_selected: PathBuf::new(),
        resume_round_offset: 0,
        column_cap: MAX_SMALL_REPAIR_COLUMNS,
    }
}

fn split_signed_terms(line: &str) -> Vec<(i32, &str)> {
    let bytes = line.as_bytes();
    let mut answer = Vec::new();
    let mut begin = 0usize;
    let mut sign = 1i32;
    if bytes.first() == Some(&b'-') {
        sign = -1;
        begin = 1;
    } else if bytes.first() == Some(&b'+') {
        begin = 1;
    }
    for index in begin..bytes.len() {
        if bytes[index] == b'+' || bytes[index] == b'-' {
            if index == begin {
                fail("empty polynomial term");
            }
            answer.push((sign, &line[begin..index]));
            sign = if bytes[index] == b'+' { 1 } else { -1 };
            begin = index + 1;
        }
    }
    if begin >= bytes.len() {
        fail("trailing polynomial sign");
    }
    answer.push((sign, &line[begin..]));
    answer
}

fn parse_provider(path: &Path, prime: u64) -> Provider {
    let input = File::open(path).unwrap_or_else(|e| fail(e.to_string()));
    let mut lines = BufReader::with_capacity(1 << 20, input).lines();
    let variable_line = lines
        .next()
        .unwrap_or_else(|| fail("missing variable header"))
        .unwrap_or_else(|e| fail(e.to_string()));
    let variables: Vec<String> = variable_line.split(',').map(str::to_owned).collect();
    if variables.len() != EXPECTED_VARIABLES {
        fail("provider variable count is not 361");
    }
    let mut variable_ids = HashMap::with_capacity(variables.len());
    for (id, name) in variables.iter().enumerate() {
        if variable_ids.insert(name.as_str(), id as u16).is_some() {
            fail("duplicate provider variable");
        }
    }
    let characteristic: u64 = lines
        .next()
        .unwrap_or_else(|| fail("missing characteristic"))
        .unwrap_or_else(|e| fail(e.to_string()))
        .parse()
        .unwrap_or_else(|_| fail("bad provider characteristic"));
    if characteristic != prime {
        fail("provider characteristic mismatch");
    }

    let mut generators = Vec::with_capacity(EXPECTED_EQUATIONS);
    let mut parsed_terms = 0usize;
    for raw in lines {
        let mut line = raw.unwrap_or_else(|e| fail(e.to_string()));
        if line.ends_with(',') {
            line.pop();
        }
        if line.is_empty() {
            fail("empty provider equation");
        }
        let signed = split_signed_terms(&line);
        let mut raw_terms = Vec::<(Vec<u16>, i32)>::with_capacity(signed.len());
        let mut generator_degree = 0usize;
        for (sign, token) in signed {
            let mut ids = Vec::new();
            if token != "1" {
                for factor in token.split('*') {
                    let id = variable_ids
                        .get(factor)
                        .copied()
                        .unwrap_or_else(|| fail(format!("unknown variable {factor}")));
                    ids.push(id);
                }
            }
            generator_degree = generator_degree.max(ids.len());
            raw_terms.push((ids, sign));
            parsed_terms += 1;
        }
        if !(2..=4).contains(&generator_degree) {
            fail("provider generator degree outside 2..4");
        }
        let mut combined = BTreeMap::<Mono, i32>::new();
        for (mut ids, coefficient) in raw_terms {
            ids.extend(std::iter::repeat_n(T_ID, generator_degree - ids.len()));
            let term = Mono::new(ids);
            *combined.entry(term).or_default() += coefficient;
        }
        combined.retain(|_, coefficient| *coefficient != 0);
        if combined.is_empty() {
            fail("zero provider generator");
        }
        generators.push(Generator {
            degree: generator_degree,
            terms: combined.into_iter().collect(),
        });
    }
    if generators.len() != EXPECTED_EQUATIONS {
        fail(format!(
            "provider equation count {} is not 6571",
            generators.len()
        ));
    }
    let mut degree_histogram = [0usize; DEGREE + 1];
    let mut term_index = HashMap::<Mono, Vec<u16>>::new();
    for (generator, polynomial) in generators.iter().enumerate() {
        degree_histogram[polynomial.degree] += 1;
        for &(term, _) in &polynomial.terms {
            term_index.entry(term).or_default().push(generator as u16);
        }
    }
    if degree_histogram[2] != 1 || degree_histogram[3] != 9 || degree_histogram[4] != 6561 {
        fail("provider degree histogram is not 1/9/6561");
    }
    Provider {
        variables,
        generators,
        term_index,
        parsed_terms,
        degree_histogram,
    }
}

fn coefficient_mod(value: i32, prime: u64) -> u64 {
    if value >= 0 {
        value as u64 % prime
    } else {
        let magnitude = (-value) as u64 % prime;
        if magnitude == 0 {
            0
        } else {
            prime - magnitude
        }
    }
}

fn materialize(provider: &Provider, column: Column, prime: u64) -> Vec<(Mono, u64)> {
    let generator = provider
        .generators
        .get(column.generator as usize)
        .unwrap_or_else(|| fail("column generator out of range"));
    if column.multiplier.degree() + generator.degree != DEGREE {
        fail("column has wrong multiplier degree");
    }
    let mut values = BTreeMap::<Mono, u64>::new();
    for &(term, signed) in &generator.terms {
        let row = term.concat(&column.multiplier);
        let coefficient = coefficient_mod(signed, prime);
        let old = values.get(&row).copied().unwrap_or(0);
        let sum = old + coefficient;
        let reduced = if sum >= prime { sum - prime } else { sum };
        if reduced == 0 {
            values.remove(&row);
        } else {
            values.insert(row, reduced);
        }
    }
    values.into_iter().collect()
}

fn load_selected_checkpoint(path: &Path, provider: &Provider) -> HashSet<Column> {
    let file = File::open(path).unwrap_or_else(|e| fail(format!("resume checkpoint: {e}")));
    let mut lines = BufReader::new(file).lines();
    let header = lines
        .next()
        .unwrap_or_else(|| fail("empty resume checkpoint"))
        .unwrap_or_else(|e| fail(e.to_string()));
    if header != "KRENN_X5_BLOCKER_D11_SELECTED_COLUMNS_V1" {
        fail("bad resume checkpoint header");
    }
    let mut selected = HashSet::<Column>::new();
    let mut previous = None;
    for line in lines {
        let line = line.unwrap_or_else(|e| fail(e.to_string()));
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 4 || fields[0] != "COL" {
            fail("bad resume checkpoint row");
        }
        let generator: usize = fields[1]
            .parse()
            .unwrap_or_else(|_| fail("bad resume generator"));
        let degree: usize = fields[2]
            .parse()
            .unwrap_or_else(|_| fail("bad resume generator degree"));
        if generator >= provider.generators.len()
            || provider.generators[generator].degree != degree
            || degree > DEGREE
        {
            fail("resume generator out of range or wrong degree");
        }
        let ids: Vec<u16> = if fields[3].is_empty() {
            Vec::new()
        } else {
            fields[3]
                .split(',')
                .map(|item| {
                    item.parse()
                        .unwrap_or_else(|_| fail("bad resume multiplier"))
                })
                .collect()
        };
        if ids.len() + degree != DEGREE || ids.windows(2).any(|pair| pair[0] > pair[1]) {
            fail("resume multiplier has wrong degree or ordering");
        }
        let column = Column {
            generator: generator as u16,
            multiplier: Mono::from_sorted_slice(&ids),
        };
        if previous.is_some_and(|old| old >= column) || !selected.insert(column) {
            fail("resume checkpoint is not strictly sorted and unique");
        }
        previous = Some(column);
    }
    // Header-only is exact when the transported seed has no violating column;
    // main still performs a full incident scan before accepting terminality.
    selected
}

fn load_dual_checkpoint(path: &Path, prime: u64) -> HashMap<Mono, u64> {
    let file = File::open(path).unwrap_or_else(|e| fail(format!("resume dual: {e}")));
    let mut lines = BufReader::new(file).lines();
    let header = lines
        .next()
        .unwrap_or_else(|| fail("empty resume dual"))
        .unwrap_or_else(|e| fail(e.to_string()));
    let fields: Vec<_> = header.split('\t').collect();
    if fields.len() != 4
        || fields[0] != "KRENN_X5_BLOCKER_D11_MODULAR_DUAL_V1"
        || fields[1].parse::<u64>().ok() != Some(prime)
        || fields[3] != "1"
    {
        fail("bad resume dual header");
    }
    let expected_support: usize = fields[2]
        .parse()
        .unwrap_or_else(|_| fail("bad resume dual support"));
    let mut dual = HashMap::<Mono, u64>::new();
    let mut previous = None;
    for line in lines {
        let line = line.unwrap_or_else(|e| fail(e.to_string()));
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 3 || fields[0] != "ROW" {
            fail("bad resume dual row");
        }
        let ids: Vec<u16> = fields[1]
            .split(',')
            .map(|item| {
                item.parse()
                    .unwrap_or_else(|_| fail("bad resume dual monomial"))
            })
            .collect();
        if ids.len() != DEGREE || ids.windows(2).any(|pair| pair[0] > pair[1]) {
            fail("resume dual monomial has wrong degree or ordering");
        }
        let row = Mono::from_sorted_slice(&ids);
        let value: u64 = fields[2]
            .parse()
            .unwrap_or_else(|_| fail("bad resume dual coefficient"));
        if value == 0 || value >= prime || previous.is_some_and(|old| old >= row) {
            fail("resume dual coefficient/order invalid");
        }
        if dual.insert(row, value).is_some() {
            fail("duplicate resume dual row");
        }
        previous = Some(row);
    }
    if dual.len() != expected_support {
        fail("resume dual support mismatch");
    }
    dual
}

fn pairing(vector: &[(Mono, u64)], candidate: &HashMap<Mono, u64>, prime: u64) -> u64 {
    vector.iter().fold(0u64, |sum, (row, coefficient)| {
        let product = (*coefficient as u128 * candidate.get(row).copied().unwrap_or(0) as u128
            % prime as u128) as u64;
        let next = sum + product;
        if next >= prime {
            next - prime
        } else {
            next
        }
    })
}

fn divisor_subsets(row: Mono, degree: usize) -> Vec<Mono> {
    fn visit(
        ids: &[u16],
        degree: usize,
        begin: usize,
        current: &mut Vec<u16>,
        output: &mut HashSet<Mono>,
    ) {
        if current.len() == degree {
            output.insert(Mono::from_sorted_slice(current));
            return;
        }
        let needed = degree - current.len();
        if ids.len().saturating_sub(begin) < needed {
            return;
        }
        for index in begin..=ids.len() - needed {
            current.push(ids[index]);
            visit(ids, degree, index + 1, current, output);
            current.pop();
        }
    }
    let mut output = HashSet::new();
    visit(row.ids(), degree, 0, &mut Vec::new(), &mut output);
    let mut answer: Vec<_> = output.into_iter().collect();
    answer.sort_unstable();
    answer
}

fn scan_violations(
    provider: &Provider,
    candidate: &HashMap<Mono, u64>,
    selected: &HashSet<Column>,
    prime: u64,
    limit: usize,
    deadline: Instant,
) -> Scan {
    let mut support: Vec<_> = candidate.keys().copied().collect();
    support.sort_unstable();
    let mut seen = HashSet::<Column>::new();
    let mut violations = Vec::new();
    let mut checked = 0usize;
    for (row_index, row) in support.into_iter().enumerate() {
        if row_index % 64 == 0 && Instant::now() >= deadline {
            return Scan {
                violations,
                incident_checked: checked,
                truncated: false,
                wall_hit: true,
            };
        }
        for degree in 2..=4 {
            for divisor in divisor_subsets(row, degree) {
                let Some(generators) = provider.term_index.get(&divisor) else {
                    continue;
                };
                let multiplier = row.quotient(&divisor).unwrap();
                for &generator in generators {
                    let column = Column {
                        generator,
                        multiplier,
                    };
                    if selected.contains(&column) || !seen.insert(column) {
                        continue;
                    }
                    checked += 1;
                    let vector = materialize(provider, column, prime);
                    if pairing(&vector, candidate, prime) != 0 {
                        violations.push((column, vector));
                        if violations.len() > limit {
                            return Scan {
                                violations,
                                incident_checked: checked,
                                truncated: true,
                                wall_hit: false,
                            };
                        }
                    }
                }
            }
        }
    }
    violations.sort_unstable_by_key(|item| item.0);
    Scan {
        violations,
        incident_checked: checked,
        truncated: false,
        wall_hit: false,
    }
}

/// Enumerate the complete incident set of `candidate` without retaining the
/// materialized columns.  This is the load-bearing memory bound for the
/// cross-branch diagnostic: only violating column keys and their row union
/// survive the scan.
fn scan_transport(
    provider: &Provider,
    candidate: &HashMap<Mono, u64>,
    prime: u64,
    deadline: Instant,
) -> TransportScan {
    let mut support: Vec<_> = candidate.keys().copied().collect();
    support.sort_unstable();
    let mut seen = HashSet::<Column>::new();
    let mut violation_columns = Vec::new();
    let mut violation_rows = HashSet::new();
    let mut checked = 0usize;
    for (row_index, row) in support.into_iter().enumerate() {
        if row_index % 64 == 0 && Instant::now() >= deadline {
            return TransportScan {
                violation_columns,
                violation_rows,
                incident_checked: checked,
                wall_hit: true,
            };
        }
        for degree in 2..=4 {
            for divisor in divisor_subsets(row, degree) {
                let Some(generators) = provider.term_index.get(&divisor) else {
                    continue;
                };
                let multiplier = row.quotient(&divisor).unwrap();
                for &generator in generators {
                    let column = Column {
                        generator,
                        multiplier,
                    };
                    if !seen.insert(column) {
                        continue;
                    }
                    checked += 1;
                    let vector = materialize(provider, column, prime);
                    if pairing(&vector, candidate, prime) != 0 {
                        violation_columns.push(column);
                        violation_rows.extend(vector.iter().map(|item| item.0));
                    }
                }
            }
        }
    }
    violation_columns.sort_unstable();
    TransportScan {
        violation_columns,
        violation_rows,
        incident_checked: checked,
        wall_hit: false,
    }
}

fn inverse_mod(mut base: u64, prime: u64) -> u64 {
    let mut exponent = prime - 2;
    let mut answer = 1u64;
    while exponent != 0 {
        if exponent & 1 == 1 {
            answer = (answer as u128 * base as u128 % prime as u128) as u64;
        }
        base = (base as u128 * base as u128 % prime as u128) as u64;
        exponent >>= 1;
    }
    answer
}

fn subtract_scaled(
    target: &mut BTreeMap<Mono, u64>,
    source: &BTreeMap<Mono, u64>,
    factor: u64,
    prime: u64,
) {
    for (&row, &coefficient) in source {
        let old = target.get(&row).copied().unwrap_or(0);
        let subtract = (factor as u128 * coefficient as u128 % prime as u128) as u64;
        let value = if old >= subtract {
            old - subtract
        } else {
            old + prime - subtract
        };
        if value == 0 {
            target.remove(&row);
        } else {
            target.insert(row, value);
        }
    }
}

struct IncrementalDualSolver {
    prime: u64,
    target: Mono,
    frozen_frequency: HashMap<Mono, usize>,
    basis: HashMap<Mono, (BTreeMap<Mono, u64>, u64)>,
    seed_values: HashMap<Mono, u64>,
    inconsistent: bool,
}

impl IncrementalDualSolver {
    fn from_checkpoint(
        columns: &[Column],
        vectors: &HashMap<Column, Vec<(Mono, u64)>>,
        target: Mono,
        prime: u64,
        seed_values: HashMap<Mono, u64>,
    ) -> Self {
        let mut frozen_frequency = HashMap::<Mono, usize>::new();
        for column in columns {
            for &(row, coefficient) in &vectors[column] {
                if row != target && coefficient != 0 {
                    *frozen_frequency.entry(row).or_default() += 1;
                }
            }
        }
        let mut solver = Self {
            prime,
            target,
            frozen_frequency,
            basis: HashMap::new(),
            seed_values,
            inconsistent: false,
        };
        for column in columns {
            solver.add_vector(&vectors[column]);
        }
        solver
    }

    fn compare_rows(&self, left: &Mono, right: &Mono) -> std::cmp::Ordering {
        (
            self.frozen_frequency
                .get(left)
                .copied()
                .unwrap_or(usize::MAX),
            left,
        )
            .cmp(&(
                self.frozen_frequency
                    .get(right)
                    .copied()
                    .unwrap_or(usize::MAX),
                right,
            ))
    }

    fn add_vector(&mut self, raw: &[(Mono, u64)]) {
        if self.inconsistent {
            return;
        }
        let target_coefficient = raw
            .iter()
            .find_map(|(row, coefficient)| (*row == self.target).then_some(*coefficient))
            .unwrap_or(0);
        let mut rhs = if target_coefficient == 0 {
            0
        } else {
            self.prime - target_coefficient
        };
        let mut equation = BTreeMap::<Mono, u64>::new();
        for &(row, coefficient) in raw {
            if row != self.target && coefficient != 0 {
                equation.insert(row, coefficient);
            }
        }
        while !equation.is_empty() {
            let pivot = *equation
                .keys()
                .min_by(|left, right| self.compare_rows(left, right))
                .unwrap();
            let value = equation[&pivot];
            if let Some((record, record_rhs)) = self.basis.get(&pivot) {
                subtract_scaled(&mut equation, record, value, self.prime);
                let subtract = (value as u128 * *record_rhs as u128 % self.prime as u128) as u64;
                rhs = if rhs >= subtract {
                    rhs - subtract
                } else {
                    rhs + self.prime - subtract
                };
                continue;
            }
            let inverse = inverse_mod(value, self.prime);
            for coefficient in equation.values_mut() {
                *coefficient = (*coefficient as u128 * inverse as u128 % self.prime as u128) as u64;
            }
            rhs = (rhs as u128 * inverse as u128 % self.prime as u128) as u64;
            self.basis
                .insert(pivot, (std::mem::take(&mut equation), rhs));
            return;
        }
        if rhs != 0 {
            self.inconsistent = true;
        }
    }

    fn candidate(&self) -> Option<HashMap<Mono, u64>> {
        if self.inconsistent {
            return None;
        }
        let mut pivots: Vec<_> = self.basis.keys().copied().collect();
        pivots.sort_by(|left, right| self.compare_rows(left, right));
        let mut candidate = self.seed_values.clone();
        candidate.insert(self.target, 1);
        for pivot in &pivots {
            candidate.remove(pivot);
        }
        for pivot in pivots.into_iter().rev() {
            let (record, record_rhs) = &self.basis[&pivot];
            let mut value = *record_rhs;
            for (&row, &coefficient) in record {
                if row == pivot {
                    continue;
                }
                let subtract = (coefficient as u128
                    * candidate.get(&row).copied().unwrap_or(0) as u128
                    % self.prime as u128) as u64;
                value = if value >= subtract {
                    value - subtract
                } else {
                    value + self.prime - subtract
                };
            }
            if value != 0 {
                candidate.insert(pivot, value);
            }
        }
        Some(candidate)
    }
}

fn solve_dual(
    columns: &[Column],
    vectors: &HashMap<Column, Vec<(Mono, u64)>>,
    target: Mono,
    prime: u64,
) -> Option<HashMap<Mono, u64>> {
    let mut frequency = HashMap::<Mono, usize>::new();
    for column in columns {
        for &(row, coefficient) in &vectors[column] {
            if row != target && coefficient != 0 {
                *frequency.entry(row).or_default() += 1;
            }
        }
    }
    let order = |left: &Mono, right: &Mono| {
        (frequency.get(left).copied().unwrap_or(usize::MAX), left)
            .cmp(&(frequency.get(right).copied().unwrap_or(usize::MAX), right))
    };
    let mut basis = HashMap::<Mono, (BTreeMap<Mono, u64>, u64)>::new();
    for column in columns {
        let raw = &vectors[column];
        let target_coefficient = raw
            .iter()
            .find_map(|(row, coefficient)| (*row == target).then_some(*coefficient))
            .unwrap_or(0);
        let mut rhs = if target_coefficient == 0 {
            0
        } else {
            prime - target_coefficient
        };
        let mut equation = BTreeMap::<Mono, u64>::new();
        for &(row, coefficient) in raw {
            if row != target && coefficient != 0 {
                equation.insert(row, coefficient);
            }
        }
        let mut inserted = false;
        while !equation.is_empty() {
            let pivot = *equation.keys().min_by(|a, b| order(a, b)).unwrap();
            let value = equation[&pivot];
            if let Some((record, record_rhs)) = basis.get(&pivot) {
                subtract_scaled(&mut equation, record, value, prime);
                let subtract = (value as u128 * *record_rhs as u128 % prime as u128) as u64;
                rhs = if rhs >= subtract {
                    rhs - subtract
                } else {
                    rhs + prime - subtract
                };
                continue;
            }
            let inverse = inverse_mod(value, prime);
            for coefficient in equation.values_mut() {
                *coefficient = (*coefficient as u128 * inverse as u128 % prime as u128) as u64;
            }
            rhs = (rhs as u128 * inverse as u128 % prime as u128) as u64;
            basis.insert(pivot, (std::mem::take(&mut equation), rhs));
            inserted = true;
            break;
        }
        if !inserted && rhs != 0 {
            return None;
        }
    }
    let mut pivots: Vec<_> = basis.keys().copied().collect();
    pivots.sort_by(order);
    let mut candidate = HashMap::<Mono, u64>::from([(target, 1)]);
    for pivot in pivots.into_iter().rev() {
        let (record, record_rhs) = &basis[&pivot];
        let mut value = *record_rhs;
        for (&row, &coefficient) in record {
            if row == pivot {
                continue;
            }
            let subtract = (coefficient as u128 * candidate.get(&row).copied().unwrap_or(0) as u128
                % prime as u128) as u64;
            value = if value >= subtract {
                value - subtract
            } else {
                value + prime - subtract
            };
        }
        if value != 0 {
            candidate.insert(pivot, value);
        }
    }
    if candidate.get(&target).copied() != Some(1)
        || columns
            .iter()
            .any(|column| pairing(&vectors[column], &candidate, prime) != 0)
    {
        fail("internal dual verification failed");
    }
    Some(candidate)
}

fn atomic_text(path: &Path, text: &str) {
    let temporary = path.with_extension("tmp");
    fs::write(&temporary, text).unwrap_or_else(|e| fail(e.to_string()));
    fs::rename(temporary, path).unwrap_or_else(|e| fail(e.to_string()));
}

fn write_selected(path: &Path, provider: &Provider, columns: &HashSet<Column>) {
    let mut sorted: Vec<_> = columns.iter().copied().collect();
    sorted.sort_unstable();
    let mut output = String::from("KRENN_X5_BLOCKER_D11_SELECTED_COLUMNS_V1\n");
    for column in sorted {
        let degree = provider.generators[column.generator as usize].degree;
        output.push_str(&format!(
            "COL\t{}\t{}\t{}\n",
            column.generator,
            degree,
            column.multiplier.text()
        ));
    }
    atomic_text(path, &output);
}

fn write_dual(path: &Path, prime: u64, candidate: Option<&HashMap<Mono, u64>>) {
    let Some(candidate) = candidate else {
        if path.exists() {
            fs::remove_file(path).unwrap_or_else(|e| fail(e.to_string()));
        }
        return;
    };
    let mut rows: Vec<_> = candidate
        .iter()
        .map(|(&row, &value)| (row, value))
        .collect();
    rows.sort_unstable_by_key(|item| item.0);
    let mut output = format!(
        "KRENN_X5_BLOCKER_D11_MODULAR_DUAL_V1\t{}\t{}\t1\n",
        prime,
        rows.len()
    );
    for (row, value) in rows {
        output.push_str(&format!("ROW\t{}\t{}\n", row.text(), value));
    }
    atomic_text(path, &output);
}

#[allow(clippy::too_many_arguments)]
fn write_result(
    config: &Config,
    provider: &Provider,
    status: &str,
    reason: &str,
    started: Instant,
    columns: usize,
    support: usize,
    rounds: &[RoundRecord],
    global_modular_dual: Option<bool>,
    resumed_columns: usize,
    startup_solve_seconds: f64,
) {
    let temporary = config.output.with_extension("json.tmp");
    let mut output =
        BufWriter::new(File::create(&temporary).unwrap_or_else(|e| fail(e.to_string())));
    writeln!(output, "{{").unwrap();
    writeln!(
        output,
        "  \"schema\": \"KRENN_X5_FOUR_BLOCKER_D11_RESUMABLE_RESULT_V1\","
    )
    .unwrap();
    writeln!(output, "  \"status\": \"{}\",", json_escape(status)).unwrap();
    writeln!(
        output,
        "  \"incomplete_reason\": \"{}\",",
        json_escape(reason)
    )
    .unwrap();
    writeln!(output, "  \"branch\": \"{}\",", json_escape(&config.branch)).unwrap();
    writeln!(output, "  \"variables\": {},", provider.variables.len()).unwrap();
    writeln!(output, "  \"equations\": {},", provider.generators.len()).unwrap();
    writeln!(
        output,
        "  \"provider_terms_parsed\": {},",
        provider.parsed_terms
    )
    .unwrap();
    writeln!(
        output,
        "  \"degree_histogram\": {{\"2\": {}, \"3\": {}, \"4\": {}}},",
        provider.degree_histogram[2], provider.degree_histogram[3], provider.degree_histogram[4]
    )
    .unwrap();
    writeln!(output, "  \"target\": \"t^11\",").unwrap();
    writeln!(output, "  \"degree\": {},", DEGREE).unwrap();
    writeln!(output, "  \"prime\": {},", config.prime).unwrap();
    writeln!(output, "  \"selected_columns\": {},", columns).unwrap();
    writeln!(output, "  \"dual_support\": {},", support).unwrap();
    writeln!(output, "  \"column_cap\": {},", config.column_cap).unwrap();
    writeln!(output, "  \"wall_limit_seconds\": {},", config.wall_seconds).unwrap();
    writeln!(
        output,
        "  \"solver_mode\": \"FROZEN_CHECKPOINT_FREQUENCY_INCREMENTAL_BASIS\","
    )
    .unwrap();
    writeln!(output, "  \"resumed_columns\": {},", resumed_columns).unwrap();
    writeln!(
        output,
        "  \"resume_round_offset\": {},",
        config.resume_round_offset
    )
    .unwrap();
    writeln!(output, "  \"transported_seed_loaded\": true,").unwrap();
    writeln!(output, "  \"resume_dual_exact_match\": false,").unwrap();
    writeln!(
        output,
        "  \"startup_solve_seconds\": {:.6},",
        startup_solve_seconds
    )
    .unwrap();
    writeln!(
        output,
        "  \"elapsed_seconds\": {:.6},",
        started.elapsed().as_secs_f64()
    )
    .unwrap();
    writeln!(
        output,
        "  \"global_modular_dual\": {},",
        global_modular_dual
            .map(|value| value.to_string())
            .unwrap_or_else(|| "null".into())
    )
    .unwrap();
    writeln!(output, "  \"exact_rational_unit_replay\": false,").unwrap();
    writeln!(output, "  \"mathematical_verdict\": null,").unwrap();
    writeln!(output, "  \"rounds\": [").unwrap();
    for (index, round) in rounds.iter().enumerate() {
        writeln!(output,
            "    {{\"round\":{},\"columns_before\":{},\"incident_columns_checked\":{},\"new_violations\":{},\"columns_after\":{},\"support_after\":{},\"incidence_seconds\":{:.6},\"solve_seconds\":{:.6}}}{}",
            round.round, round.columns_before, round.incident_columns_checked,
            round.new_violations, round.columns_after, round.support_after,
            round.incidence_seconds, round.solve_seconds,
            if index + 1 == rounds.len() { "" } else { "," }).unwrap();
    }
    writeln!(output, "  ]").unwrap();
    writeln!(output, "}}").unwrap();
    output.flush().unwrap();
    drop(output);
    fs::rename(temporary, &config.output).unwrap_or_else(|e| fail(e.to_string()));
}

fn run_selftest() {
    let prime = 1_000_000_007u64;
    let target = Mono::new(vec![T_ID; DEGREE]);
    let row_a = Mono::new(vec![1; DEGREE]);
    let row_b = Mono::new(vec![2; DEGREE]);
    let row_c = Mono::new(vec![3; DEGREE]);
    let empty = Mono::from_sorted_slice(&[]);
    let columns = [
        Column {
            generator: 0,
            multiplier: empty,
        },
        Column {
            generator: 1,
            multiplier: empty,
        },
    ];
    let mut vectors = HashMap::from([
        (columns[0], vec![(target, 1), (row_a, 1)]),
        (columns[1], vec![(row_a, 1), (row_b, 1)]),
    ]);
    let reference = solve_dual(&columns, &vectors, target, prime)
        .unwrap_or_else(|| fail("selftest reference unexpectedly inconsistent"));
    let mut incremental =
        IncrementalDualSolver::from_checkpoint(&columns, &vectors, target, prime, HashMap::new());
    let candidate = incremental
        .candidate()
        .unwrap_or_else(|| fail("selftest incremental unexpectedly inconsistent"));
    assert_eq!(candidate, reference);
    assert_eq!(candidate.get(&target).copied(), Some(1));
    assert!(columns
        .iter()
        .all(|column| pairing(&vectors[column], &candidate, prime) == 0));

    let third = Column {
        generator: 2,
        multiplier: empty,
    };
    let third_vector = vec![(row_b, 1), (row_c, 1)];
    incremental.add_vector(&third_vector);
    vectors.insert(third, third_vector);
    let after_add = incremental
        .candidate()
        .unwrap_or_else(|| fail("selftest incremental add unexpectedly inconsistent"));
    assert!(columns
        .iter()
        .chain(std::iter::once(&third))
        .all(|column| pairing(&vectors[column], &after_add, prime) == 0));

    incremental.add_vector(&[(target, 1), (row_b, 1)]);
    assert!(incremental.candidate().is_none());
    println!(
        "{{\"schema\":\"KRENN_X5_D11_RESUMABLE_SELFTEST_V1\",\"status\":\"PASS\",\"reference_equal\":true,\"incremental_add_replay\":true,\"inconsistency_detected\":true,\"tests\":5}}"
    );
}

fn main() {
    if env::args().len() == 2 && env::args().nth(1).as_deref() == Some("--selftest") {
        run_selftest();
        return;
    }
    let config = parse_args();
    if config.output.exists() || config.repair_dual.exists() {
        fail("refuse pre-existing output");
    }
    let started = Instant::now();
    let deadline = started + Duration::from_secs(config.wall_seconds);
    let source_provider = parse_provider(&config.source_provider, config.prime);
    let provider = parse_provider(&config.input, config.prime);
    if source_provider.variables != provider.variables {
        fail("provider coordinate headers differ; identity transport is invalid");
    }
    let target = Mono::new(vec![T_ID; DEGREE]);
    let mut transported = load_dual_checkpoint(&config.resume_dual, config.prime);
    let raw_target = transported.get(&target).copied().unwrap_or(0);
    if raw_target == 0 {
        fail("transported target coefficient is zero and cannot be normalized");
    }
    let normalization_factor = inverse_mod(raw_target, config.prime);
    for value in transported.values_mut() {
        *value = (*value as u128 * normalization_factor as u128 % config.prime as u128) as u64;
    }
    if transported.get(&target).copied() != Some(1) {
        fail("exact target normalization failed");
    }

    let scan_started = Instant::now();
    let scan = scan_transport(&provider, &transported, config.prime, deadline);
    let scan_seconds = scan_started.elapsed().as_secs_f64();
    let mut allowed_rows: HashSet<_> = transported.keys().copied().collect();
    allowed_rows.extend(scan.violation_rows.iter().copied());
    let new_violation_rows = allowed_rows.len() - transported.len();

    let small_system = !scan.wall_hit
        && scan.violation_columns.len() <= MAX_SMALL_REPAIR_COLUMNS;
    let mut repair_consistent = None;
    let mut repair_basis_rank = None;
    let mut repair_support = None;
    let mut replay_failures = None;
    let mut solve_seconds = 0.0;
    let mut repaired = None;
    if small_system {
        let mut vectors = HashMap::<Column, Vec<(Mono, u64)>>::new();
        for &column in &scan.violation_columns {
            vectors.insert(column, materialize(&provider, column, config.prime));
        }
        let solve_started = Instant::now();
        let solver = IncrementalDualSolver::from_checkpoint(
            &scan.violation_columns,
            &vectors,
            target,
            config.prime,
            transported.clone(),
        );
        let candidate = solver.candidate();
        solve_seconds = solve_started.elapsed().as_secs_f64();
        repair_basis_rank = Some(solver.basis.len());
        repair_consistent = Some(candidate.is_some());
        if let Some(candidate) = candidate {
            let failures = scan
                .violation_columns
                .iter()
                .filter(|column| pairing(&vectors[column], &candidate, config.prime) != 0)
                .count();
            if candidate.get(&target).copied() != Some(1) || failures != 0 {
                fail("support-repair replay or target normalization failed");
            }
            repair_support = Some(candidate.len());
            replay_failures = Some(failures);
            write_dual(&config.repair_dual, config.prime, Some(&candidate));
            repaired = Some(candidate);
        }
    }

    let (status, reason) = if scan.wall_hit {
        ("INCOMPLETE_WALL_CAP", "INCIDENT_SCAN_NOT_EXHAUSTIVE")
    } else if !small_system {
        (
            "PASS_EXACT_TRANSPORT_DIAGNOSTIC_NOT_SMALL",
            "VIOLATION_SYSTEM_EXCEEDS_FROZEN_100000_COLUMN_REPAIR_GATE",
        )
    } else if repair_consistent == Some(true) {
        (
            "PASS_EXACT_TRANSPORT_DIAGNOSTIC_REPAIR_CONSISTENT",
            "VIOLATION_SUBSYSTEM_HAS_EXACT_P107_REPAIR",
        )
    } else {
        (
            "PASS_EXACT_TRANSPORT_DIAGNOSTIC_REPAIR_INCONSISTENT",
            "VIOLATION_SUBSYSTEM_HAS_NO_P107_REPAIR",
        )
    };
    let bool_or_null = |value: Option<bool>| {
        value
            .map(|item| item.to_string())
            .unwrap_or_else(|| "null".into())
    };
    let usize_or_null = |value: Option<usize>| {
        value
            .map(|item| item.to_string())
            .unwrap_or_else(|| "null".into())
    };
    let temporary = config.output.with_extension("json.tmp");
    let mut output = BufWriter::new(File::create(&temporary).unwrap_or_else(|e| fail(e.to_string())));
    writeln!(output, "{{").unwrap();
    writeln!(output, "  \"schema\": \"KRENN_X5_D11_CROSS_BRANCH_TRANSPORT_DIAGNOSTIC_V1\",").unwrap();
    writeln!(output, "  \"status\": \"{}\",", status).unwrap();
    writeln!(output, "  \"reason\": \"{}\",", reason).unwrap();
    writeln!(output, "  \"branch\": \"{}\",", json_escape(&config.branch)).unwrap();
    writeln!(output, "  \"prime\": {},", config.prime).unwrap();
    writeln!(output, "  \"degree\": {},", DEGREE).unwrap();
    writeln!(output, "  \"target\": \"t^11\",").unwrap();
    writeln!(output, "  \"coordinate_transport\": \"IDENTICAL_361_NAME_HEADER\",").unwrap();
    writeln!(output, "  \"provider_variables\": {},", provider.variables.len()).unwrap();
    writeln!(output, "  \"provider_equations\": {},", provider.generators.len()).unwrap();
    writeln!(output, "  \"provider_terms_parsed\": {},", provider.parsed_terms).unwrap();
    writeln!(output, "  \"transported_support\": {},", transported.len()).unwrap();
    writeln!(output, "  \"target_coefficient_before_normalization\": {},", raw_target).unwrap();
    writeln!(output, "  \"normalization_factor\": {},", normalization_factor).unwrap();
    writeln!(output, "  \"target_coefficient_after_normalization\": 1,").unwrap();
    writeln!(output, "  \"incident_scan_exhaustive\": {},", !scan.wall_hit).unwrap();
    writeln!(output, "  \"incident_columns_checked\": {},", scan.incident_checked).unwrap();
    writeln!(output, "  \"violation_columns\": {},", scan.violation_columns.len()).unwrap();
    writeln!(output, "  \"violation_row_union\": {},", scan.violation_rows.len()).unwrap();
    writeln!(output, "  \"new_violation_rows\": {},", new_violation_rows).unwrap();
    writeln!(output, "  \"allowed_rows_support_union_violation_rows\": {},", allowed_rows.len()).unwrap();
    writeln!(output, "  \"small_repair_column_cap\": {},", MAX_SMALL_REPAIR_COLUMNS).unwrap();
    writeln!(output, "  \"small_repair_attempted\": {},", small_system).unwrap();
    writeln!(output, "  \"repair_system_scope\": \"ALL_AND_ONLY_VIOLATING_COLUMNS_INCIDENT_TO_TRANSPORTED_SUPPORT\",").unwrap();
    writeln!(output, "  \"repair_consistent_over_p107\": {},", bool_or_null(repair_consistent)).unwrap();
    writeln!(output, "  \"repair_basis_rank\": {},", usize_or_null(repair_basis_rank)).unwrap();
    writeln!(output, "  \"repair_candidate_support\": {},", usize_or_null(repair_support)).unwrap();
    writeln!(output, "  \"repair_selected_replay_failures\": {},", usize_or_null(replay_failures)).unwrap();
    writeln!(output, "  \"repair_dual_written\": {},", repaired.is_some()).unwrap();
    writeln!(output, "  \"global_dual_claim\": false,").unwrap();
    writeln!(output, "  \"nonviolating_incident_columns_replayed_after_repair\": false,").unwrap();
    writeln!(output, "  \"general_cegar_launched\": false,").unwrap();
    writeln!(output, "  \"second_prime_launched\": false,").unwrap();
    writeln!(output, "  \"degree_twelve_cache_read\": false,").unwrap();
    writeln!(output, "  \"scan_seconds\": {:.6},", scan_seconds).unwrap();
    writeln!(output, "  \"repair_solve_seconds\": {:.6},", solve_seconds).unwrap();
    writeln!(output, "  \"elapsed_seconds\": {:.6},", started.elapsed().as_secs_f64()).unwrap();
    writeln!(output, "  \"native_wall_limit_seconds\": {}", config.wall_seconds).unwrap();
    writeln!(output, "}}").unwrap();
    output.flush().unwrap();
    drop(output);
    fs::rename(temporary, &config.output).unwrap_or_else(|e| fail(e.to_string()));
    if scan.wall_hit {
        std::process::exit(3);
    }
}
