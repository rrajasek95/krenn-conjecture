//! Bounded source-faithful degree-nine dual CEGAR for the four canonical X5
//! triangle-blocker branches.  This is deliberately non-orbit-compressed:
//! the frozen 361-variable/6571-equation branch is parsed literally.

use std::collections::{BTreeMap, HashMap, HashSet};
use std::env;
use std::fs::{self, File};
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

const DEGREE: usize = 9;
const EXPECTED_VARIABLES: usize = 361;
const EXPECTED_EQUATIONS: usize = 6571;
const T_ID: u16 = 361;

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct Mono([u16; DEGREE]);

impl Hash for Mono {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.0.hash(state);
    }
}

impl Mono {
    fn from_sorted_slice(ids: &[u16]) -> Self {
        if ids.len() > DEGREE {
            fail("monomial exceeds degree nine");
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
    output: PathBuf,
    selected: PathBuf,
    dual: PathBuf,
    prime: u64,
    column_cap: usize,
    wall_seconds: u64,
}

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
        if values.insert(args[index].clone(), args[index + 1].clone()).is_some() {
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
    let branch = get("--branch");
    if !matches!(
        branch.as_str(),
        "triangle_endpoint_colour" | "cap_endpoint_colour" | "third_colour" | "direct"
    ) {
        fail("unknown branch");
    }
    let prime = get("--prime").parse().unwrap_or_else(|_| fail("bad prime"));
    let column_cap = get("--column-cap")
        .parse()
        .unwrap_or_else(|_| fail("bad column cap"));
    let wall_seconds = get("--wall-seconds")
        .parse()
        .unwrap_or_else(|_| fail("bad wall cap"));
    if !matches!(prime, 1_073_741_827 | 1_000_000_007)
        || column_cap == 0
        || column_cap > 2_000_000
    {
        fail("prime/column cap outside frozen contract");
    }
    if wall_seconds == 0 || wall_seconds > 175 {
        fail("wall cap outside frozen contract");
    }
    Config {
        branch,
        input: PathBuf::from(get("--input")),
        output: PathBuf::from(get("--output")),
        selected: PathBuf::from(get("--selected")),
        dual: PathBuf::from(get("--dual")),
        prime,
        column_cap,
        wall_seconds,
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
        if magnitude == 0 { 0 } else { prime - magnitude }
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

fn pairing(vector: &[(Mono, u64)], candidate: &HashMap<Mono, u64>, prime: u64) -> u64 {
    vector.iter().fold(0u64, |sum, (row, coefficient)| {
        let product = (*coefficient as u128
            * candidate.get(row).copied().unwrap_or(0) as u128
            % prime as u128) as u64;
        let next = sum + product;
        if next >= prime { next - prime } else { next }
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
                rhs = if rhs >= subtract { rhs - subtract } else { rhs + prime - subtract };
                continue;
            }
            let inverse = inverse_mod(value, prime);
            for coefficient in equation.values_mut() {
                *coefficient =
                    (*coefficient as u128 * inverse as u128 % prime as u128) as u64;
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
            let subtract = (coefficient as u128
                * candidate.get(&row).copied().unwrap_or(0) as u128
                % prime as u128) as u64;
            value = if value >= subtract { value - subtract } else { value + prime - subtract };
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
    let mut output = String::from("KRENN_X5_BLOCKER_D9_SELECTED_COLUMNS_V1\n");
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
    let mut rows: Vec<_> = candidate.iter().map(|(&row, &value)| (row, value)).collect();
    rows.sort_unstable_by_key(|item| item.0);
    let mut output = format!(
        "KRENN_X5_BLOCKER_D9_MODULAR_DUAL_V1\t{}\t{}\t1\n",
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
) {
    let temporary = config.output.with_extension("json.tmp");
    let mut output = BufWriter::new(File::create(&temporary).unwrap_or_else(|e| fail(e.to_string())));
    writeln!(output, "{{").unwrap();
    writeln!(output, "  \"schema\": \"KRENN_X5_FOUR_BLOCKER_D9_CEGAR_RESULT_V1\",").unwrap();
    writeln!(output, "  \"status\": \"{}\",", json_escape(status)).unwrap();
    writeln!(output, "  \"incomplete_reason\": \"{}\",", json_escape(reason)).unwrap();
    writeln!(output, "  \"branch\": \"{}\",", json_escape(&config.branch)).unwrap();
    writeln!(output, "  \"variables\": {},", provider.variables.len()).unwrap();
    writeln!(output, "  \"equations\": {},", provider.generators.len()).unwrap();
    writeln!(output, "  \"provider_terms_parsed\": {},", provider.parsed_terms).unwrap();
    writeln!(output, "  \"degree_histogram\": {{\"2\": {}, \"3\": {}, \"4\": {}}},",
        provider.degree_histogram[2], provider.degree_histogram[3], provider.degree_histogram[4]).unwrap();
    writeln!(output, "  \"target\": \"t^9\",").unwrap();
    writeln!(output, "  \"degree\": {},", DEGREE).unwrap();
    writeln!(output, "  \"prime\": {},", config.prime).unwrap();
    writeln!(output, "  \"selected_columns\": {},", columns).unwrap();
    writeln!(output, "  \"dual_support\": {},", support).unwrap();
    writeln!(output, "  \"column_cap\": {},", config.column_cap).unwrap();
    writeln!(output, "  \"wall_limit_seconds\": {},", config.wall_seconds).unwrap();
    writeln!(output, "  \"elapsed_seconds\": {:.6},", started.elapsed().as_secs_f64()).unwrap();
    writeln!(output, "  \"global_modular_dual\": {},",
        global_modular_dual.map(|value| value.to_string()).unwrap_or_else(|| "null".into())).unwrap();
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

fn main() {
    let config = parse_args();
    if config.output.exists() || config.selected.exists() || config.dual.exists() {
        fail("refuse pre-existing output");
    }
    let started = Instant::now();
    let deadline = started + Duration::from_secs(config.wall_seconds);
    let provider = parse_provider(&config.input, config.prime);
    let target = Mono::new(vec![T_ID; DEGREE]);
    let mut selected = HashSet::<Column>::new();
    let mut vectors = HashMap::<Column, Vec<(Mono, u64)>>::new();
    let mut candidate = Some(HashMap::<Mono, u64>::from([(target, 1)]));
    let mut rounds = Vec::<RoundRecord>::new();
    let mut terminal_status = String::new();
    let mut terminal_reason = String::new();
    let mut global_modular_dual = None;

    for round in 0usize.. {
        if Instant::now() >= deadline {
            terminal_status = "INCOMPLETE_WALL_CAP".into();
            terminal_reason = "WALL_CAP".into();
            break;
        }
        let current = candidate.as_ref().unwrap_or_else(|| fail("missing active dual"));
        let remaining = config.column_cap - selected.len();
        let incidence_started = Instant::now();
        let scan = scan_violations(
            &provider,
            current,
            &selected,
            config.prime,
            remaining,
            deadline,
        );
        let incidence_seconds = incidence_started.elapsed().as_secs_f64();
        if scan.wall_hit {
            terminal_status = "INCOMPLETE_WALL_CAP".into();
            terminal_reason = "WALL_CAP_DURING_GLOBAL_INCIDENT_SCAN".into();
            break;
        }
        if scan.violations.is_empty() {
            terminal_status = "COMPLETE_MODULAR_DUAL_DIAGNOSTIC".into();
            terminal_reason = "NO_GLOBAL_VIOLATING_COLUMN_OVER_FROZEN_PRIME".into();
            global_modular_dual = Some(true);
            break;
        }
        if scan.truncated {
            rounds.push(RoundRecord {
                round,
                columns_before: selected.len(),
                incident_columns_checked: scan.incident_checked,
                new_violations: scan.violations.len(),
                columns_after: selected.len(),
                support_after: current.len(),
                incidence_seconds,
                solve_seconds: 0.0,
            });
            terminal_status = "INCOMPLETE_COLUMN_CAP".into();
            terminal_reason = "MORE_VIOLATING_COLUMNS_THAN_REMAINING_CAPACITY".into();
            break;
        }
        let columns_before = selected.len();
        for (column, vector) in scan.violations.iter().cloned() {
            if !selected.insert(column) || vectors.insert(column, vector).is_some() {
                fail("duplicate selected violation");
            }
        }
        let mut sorted_columns: Vec<_> = selected.iter().copied().collect();
        sorted_columns.sort_unstable();
        let solve_started = Instant::now();
        candidate = solve_dual(&sorted_columns, &vectors, target, config.prime);
        let solve_seconds = solve_started.elapsed().as_secs_f64();
        let support_after = candidate.as_ref().map(HashMap::len).unwrap_or(0);
        rounds.push(RoundRecord {
            round,
            columns_before,
            incident_columns_checked: scan.incident_checked,
            new_violations: scan.violations.len(),
            columns_after: selected.len(),
            support_after,
            incidence_seconds,
            solve_seconds,
        });
        if candidate.is_none() {
            terminal_status = "MODULAR_MEMBER_REQUIRES_EXACT_RATIONAL_REPLAY".into();
            terminal_reason = "SELECTED_SPAN_CONTAINS_TARGET_OVER_FROZEN_PRIME_ONLY".into();
            break;
        }
        if selected.len() == config.column_cap {
            terminal_status = "INCOMPLETE_COLUMN_CAP".into();
            terminal_reason = "SELECTED_COLUMN_CAP_REACHED".into();
            break;
        }
    }

    if terminal_status.is_empty() {
        fail("missing terminal status");
    }
    write_selected(&config.selected, &provider, &selected);
    write_dual(&config.dual, config.prime, candidate.as_ref());
    write_result(
        &config,
        &provider,
        &terminal_status,
        &terminal_reason,
        started,
        selected.len(),
        candidate.as_ref().map(HashMap::len).unwrap_or(0),
        &rounds,
        global_modular_dual,
    );
}
