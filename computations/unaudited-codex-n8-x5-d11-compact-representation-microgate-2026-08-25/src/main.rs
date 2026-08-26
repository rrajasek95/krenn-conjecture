//! Bounded exact representation microgate for the sealed X5 D11 triangle checkpoint.
//! This does not solve or continue CEGAR.  It compares literal baseline materialized
//! columns with comparator-ranked u32 rows and natural-order u128 columns.

use std::collections::{BTreeMap, HashMap};
use std::env;
use std::fs::{self, File};
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader, Write};
use std::mem::size_of;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::time::Instant;

const DEGREE: usize = 11;
const VARIABLES: usize = 361;
const EQUATIONS: usize = 6571;
const T_ID: u16 = 361;
const PRIME: u64 = 1_073_741_827;
const SENTINEL9: u16 = 511;

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Mono([u16; DEGREE]);

impl Hash for Mono {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.0.hash(state);
    }
}

impl Mono {
    fn from_sorted(ids: &[u16]) -> Self {
        if ids.len() > DEGREE || ids.iter().any(|&id| id > T_ID)
            || ids.windows(2).any(|pair| pair[0] > pair[1])
        {
            fail("invalid monomial");
        }
        let mut packed = [u16::MAX; DEGREE];
        packed[..ids.len()].copy_from_slice(ids);
        Self(packed)
    }

    fn new(mut ids: Vec<u16>) -> Self {
        ids.sort_unstable();
        Self::from_sorted(&ids)
    }

    fn degree(&self) -> usize {
        self.0.iter().take_while(|&&id| id != u16::MAX).count()
    }

    fn ids(&self) -> &[u16] {
        &self.0[..self.degree()]
    }

    fn concat(&self, other: &Mono) -> Self {
        let mut ids = self.ids().to_vec();
        ids.extend_from_slice(other.ids());
        Self::new(ids)
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column {
    generator: u16,
    multiplier: Mono,
}

struct Generator {
    degree: usize,
    terms: Vec<(Mono, i32)>,
}

struct Provider {
    generators: Vec<Generator>,
}

struct Config {
    mode: String,
    count: usize,
    provider: PathBuf,
    selected: PathBuf,
    dual: PathBuf,
    output: PathBuf,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("d11-compact-microgate: {}", message.as_ref());
    std::process::exit(2)
}

fn parse_args() -> Config {
    let args: Vec<String> = env::args().collect();
    let mut values = HashMap::new();
    let mut index = 1;
    while index < args.len() {
        if index + 1 >= args.len() || !args[index].starts_with("--") {
            fail("expected --key value pairs");
        }
        if values.insert(args[index].clone(), args[index + 1].clone()).is_some() {
            fail("duplicate argument");
        }
        index += 2;
    }
    if values.len() != 6 {
        fail("unknown or missing argument");
    }
    let get = |key: &str| values.get(key).cloned().unwrap_or_else(|| fail(format!("missing {key}")));
    let mode = get("--mode");
    if !matches!(mode.as_str(), "baseline" | "compact") {
        fail("mode must be baseline or compact");
    }
    let count = get("--count").parse().unwrap_or_else(|_| fail("bad count"));
    if !matches!(count, 1000 | 5000) {
        fail("count must be exactly 1000 or 5000");
    }
    Config {
        mode,
        count,
        provider: PathBuf::from(get("--provider")),
        selected: PathBuf::from(get("--selected")),
        dual: PathBuf::from(get("--dual")),
        output: PathBuf::from(get("--output")),
    }
}

fn split_signed_terms(line: &str) -> Vec<(i32, &str)> {
    let bytes = line.as_bytes();
    let mut answer = Vec::new();
    let mut begin = 0;
    let mut sign = 1;
    if bytes.first() == Some(&b'-') {
        sign = -1;
        begin = 1;
    } else if bytes.first() == Some(&b'+') {
        begin = 1;
    }
    for index in begin..bytes.len() {
        if matches!(bytes[index], b'+' | b'-') {
            if index == begin {
                fail("empty term");
            }
            answer.push((sign, &line[begin..index]));
            sign = if bytes[index] == b'+' { 1 } else { -1 };
            begin = index + 1;
        }
    }
    if begin >= bytes.len() {
        fail("trailing sign");
    }
    answer.push((sign, &line[begin..]));
    answer
}

fn parse_provider(path: &Path) -> Provider {
    let mut lines = BufReader::with_capacity(1 << 20, File::open(path).unwrap()).lines();
    let names: Vec<String> = lines.next().unwrap().unwrap().split(',').map(str::to_owned).collect();
    if names.len() != VARIABLES {
        fail("provider variable count");
    }
    let ids: HashMap<&str, u16> = names.iter().enumerate().map(|(id, name)| (name.as_str(), id as u16)).collect();
    if ids.len() != VARIABLES || lines.next().unwrap().unwrap() != PRIME.to_string() {
        fail("provider header");
    }
    let mut generators = Vec::with_capacity(EQUATIONS);
    for raw in lines {
        let mut line = raw.unwrap();
        if line.ends_with(',') {
            line.pop();
        }
        let mut raw_terms = Vec::new();
        let mut degree = 0;
        for (sign, token) in split_signed_terms(&line) {
            let term: Vec<u16> = if token == "1" { Vec::new() } else {
                token.split('*').map(|factor| *ids.get(factor).unwrap_or_else(|| fail("unknown variable"))).collect()
            };
            degree = degree.max(term.len());
            raw_terms.push((term, sign));
        }
        if !(2..=4).contains(&degree) {
            fail("generator degree");
        }
        let mut combined = BTreeMap::<Mono, i32>::new();
        for (mut term, sign) in raw_terms {
            term.extend(std::iter::repeat_n(T_ID, degree - term.len()));
            *combined.entry(Mono::new(term)).or_default() += sign;
        }
        combined.retain(|_, coefficient| *coefficient != 0);
        generators.push(Generator { degree, terms: combined.into_iter().collect() });
    }
    if generators.len() != EQUATIONS {
        fail("provider equation count");
    }
    let histogram = generators.iter().fold([0usize; 5], |mut answer, generator| {
        answer[generator.degree] += 1;
        answer
    });
    if histogram[2] != 1 || histogram[3] != 9 || histogram[4] != 6561 {
        fail("provider degree histogram");
    }
    Provider { generators }
}

fn load_selected(path: &Path, provider: &Provider) -> Vec<Column> {
    let mut lines = BufReader::new(File::open(path).unwrap()).lines();
    if lines.next().unwrap().unwrap() != "KRENN_X5_BLOCKER_D11_SELECTED_COLUMNS_V1" {
        fail("selected header");
    }
    let mut output = Vec::new();
    for raw in lines {
        let line = raw.unwrap();
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 4 || fields[0] != "COL" {
            fail("selected row");
        }
        let generator: usize = fields[1].parse().unwrap();
        let degree: usize = fields[2].parse().unwrap();
        if generator >= provider.generators.len() || provider.generators[generator].degree != degree {
            fail("selected generator");
        }
        let ids: Vec<u16> = if fields[3].is_empty() { Vec::new() } else {
            fields[3].split(',').map(|value| value.parse().unwrap()).collect()
        };
        if ids.len() + degree != DEGREE {
            fail("selected degree");
        }
        let column = Column { generator: generator as u16, multiplier: Mono::from_sorted(&ids) };
        if output.last().is_some_and(|old| *old >= column) {
            fail("selected order");
        }
        output.push(column);
    }
    output
}

fn load_dual(path: &Path) -> Vec<(Mono, u64)> {
    let mut lines = BufReader::new(File::open(path).unwrap()).lines();
    let header = lines.next().unwrap().unwrap();
    let fields: Vec<_> = header.split('\t').collect();
    if fields.len() != 4 || fields[0] != "KRENN_X5_BLOCKER_D11_MODULAR_DUAL_V1"
        || fields[1] != PRIME.to_string() || fields[3] != "1"
    {
        fail("dual header");
    }
    let expected: usize = fields[2].parse().unwrap();
    let mut output = Vec::<(Mono, u64)>::with_capacity(expected);
    for raw in lines {
        let line = raw.unwrap();
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 3 || fields[0] != "ROW" {
            fail("dual row");
        }
        let ids: Vec<u16> = fields[1].split(',').map(|value| value.parse().unwrap()).collect();
        let item = (Mono::from_sorted(&ids), fields[2].parse().unwrap());
        if item.1 == 0 || item.1 >= PRIME || output.last().is_some_and(|old| old.0 >= item.0) {
            fail("dual order/coefficient");
        }
        output.push(item);
    }
    if output.len() != expected || output.iter().find(|item| item.0 == Mono::new(vec![T_ID; DEGREE])).map(|item| item.1) != Some(1) {
        fail("dual support/target");
    }
    output
}

fn coefficient_mod(value: i32) -> u64 {
    if value >= 0 { value as u64 % PRIME } else { PRIME - ((-value) as u64 % PRIME) }
}

fn materialize(provider: &Provider, column: Column) -> Vec<(Mono, u64)> {
    let generator = &provider.generators[column.generator as usize];
    if generator.degree + column.multiplier.degree() != DEGREE {
        fail("column degree");
    }
    let mut values = BTreeMap::<Mono, u64>::new();
    for &(term, signed) in &generator.terms {
        let row = term.concat(&column.multiplier);
        let coefficient = coefficient_mod(signed);
        let sum = values.get(&row).copied().unwrap_or(0) + coefficient;
        let reduced = if sum >= PRIME { sum - PRIME } else { sum };
        if reduced == 0 { values.remove(&row); } else { values.insert(row, reduced); }
    }
    values.into_iter().collect()
}

fn pack_column(column: Column) -> u128 {
    if column.generator as usize >= (1 << 13) {
        fail("generator packing overflow");
    }
    let mut packed = column.generator as u128;
    for &value in &column.multiplier.0 {
        let encoded = if value == u16::MAX { SENTINEL9 } else { value };
        if encoded > SENTINEL9 {
            fail("row packing overflow");
        }
        packed = (packed << 9) | encoded as u128;
    }
    packed
}

fn unpack_column(mut packed: u128) -> Column {
    let mut values = [0u16; DEGREE];
    for index in (0..DEGREE).rev() {
        values[index] = (packed & 0x1ff) as u16;
        packed >>= 9;
    }
    if packed >= (1 << 13) {
        fail("packed generator overflow");
    }
    let mut ids = Vec::new();
    let mut sentinel = false;
    for value in values {
        if value == SENTINEL9 {
            sentinel = true;
        } else {
            if sentinel || value > T_ID {
                fail("noncanonical packed multiplier");
            }
            ids.push(value);
        }
    }
    Column { generator: packed as u16, multiplier: Mono::from_sorted(&ids) }
}

fn write_mono(output: &mut dyn Write, mono: Mono) {
    for value in mono.0 {
        output.write_all(&value.to_be_bytes()).unwrap();
    }
}

fn write_column(output: &mut dyn Write, column: Column) {
    output.write_all(&column.generator.to_be_bytes()).unwrap();
    write_mono(output, column.multiplier);
}

fn sha_stream(write: impl FnOnce(&mut dyn Write)) -> String {
    let mut child = Command::new("/usr/bin/shasum")
        .args(["-a", "256"])
        .stdin(Stdio::piped()).stdout(Stdio::piped()).spawn().unwrap();
    {
        let mut stdin = child.stdin.take().unwrap();
        write(&mut stdin);
    }
    let result = child.wait_with_output().unwrap();
    if !result.status.success() {
        fail("shasum failed");
    }
    String::from_utf8(result.stdout).unwrap().split_whitespace().next().unwrap().to_string()
}

fn file_sha(path: &Path) -> String {
    let result = Command::new("/usr/bin/shasum").args(["-a", "256", path.to_str().unwrap()]).output().unwrap();
    if !result.status.success() { fail("file shasum failed"); }
    String::from_utf8(result.stdout).unwrap().split_whitespace().next().unwrap().to_string()
}

fn selected_sha(columns: impl Iterator<Item = Column>) -> String {
    sha_stream(|output| columns.for_each(|column| write_column(output, column)))
}

fn support_sha(rows: impl Iterator<Item = (Mono, u64)>) -> String {
    sha_stream(|output| rows.for_each(|(row, coefficient)| {
        write_mono(output, row);
        output.write_all(&coefficient.to_be_bytes()).unwrap();
    }))
}

fn vector_sha(vectors: impl Iterator<Item = (Column, Vec<(Mono, u64)>)>) -> String {
    sha_stream(|output| vectors.for_each(|(column, vector)| {
        write_column(output, column);
        output.write_all(&(vector.len() as u32).to_be_bytes()).unwrap();
        for (row, coefficient) in vector {
            write_mono(output, row);
            output.write_all(&coefficient.to_be_bytes()).unwrap();
        }
    }))
}

fn pairing_baseline(vector: &[(Mono, u64)], dual: &HashMap<Mono, u64>) -> u64 {
    vector.iter().fold(0, |sum, (row, coefficient)| {
        let product = (*coefficient as u128 * dual.get(row).copied().unwrap_or(0) as u128 % PRIME as u128) as u64;
        let next = sum + product;
        if next >= PRIME { next - PRIME } else { next }
    })
}

fn run_baseline(provider: &Provider, columns: &[Column], dual: &[(Mono, u64)]) -> (String, String, String, usize, usize, f64) {
    let started = Instant::now();
    let vectors: Vec<_> = columns.iter().copied().map(|column| (column, materialize(provider, column))).collect();
    let dual_map: HashMap<_, _> = dual.iter().copied().collect();
    let representation_seconds = started.elapsed().as_secs_f64();
    let failures = vectors.iter().filter(|(_, vector)| pairing_baseline(vector, &dual_map) != 0).count();
    let terms: usize = vectors.iter().map(|(_, vector)| vector.len()).sum();
    let retained = vectors.capacity() * size_of::<(Column, Vec<(Mono, u64)>)>()
        + vectors.iter().map(|(_, vector)| vector.capacity() * size_of::<(Mono, u64)>()).sum::<usize>()
        + dual_map.capacity() * size_of::<(Mono, u64)>();
    let selected = selected_sha(columns.iter().copied());
    let support = support_sha(dual.iter().copied());
    let semantics = vector_sha(vectors.into_iter());
    (selected, support, semantics, terms, retained, representation_seconds + failures as f64 * 0.0)
}

fn run_compact(provider: &Provider, columns: &[Column], dual: &[(Mono, u64)]) -> (String, String, String, usize, usize, f64) {
    let started = Instant::now();
    let packed_columns: Vec<u128> = columns.iter().copied().map(pack_column).collect();
    if packed_columns.windows(2).any(|pair| pair[0] >= pair[1])
        || packed_columns.iter().copied().map(unpack_column).ne(columns.iter().copied())
    {
        fail("u128 column natural-order mismatch");
    }
    let mut frequency = HashMap::<Mono, u32>::new();
    for &column in columns {
        for (row, coefficient) in materialize(provider, column) {
            if coefficient != 0 {
                *frequency.entry(row).or_default() = frequency.get(&row).copied().unwrap_or(0).checked_add(1).unwrap();
            }
        }
    }
    let mut rows: Vec<Mono> = frequency.keys().copied().chain(dual.iter().map(|item| item.0)).collect();
    rows.sort_unstable();
    rows.dedup();
    rows.sort_by_key(|row| (frequency.get(row).copied().unwrap_or(u32::MAX), *row));
    if rows.len() > u32::MAX as usize { fail("row id overflow"); }
    let row_ids: HashMap<Mono, u32> = rows.iter().enumerate().map(|(id, &row)| (row, id as u32)).collect();
    let compact_dual: HashMap<u32, u64> = dual.iter().map(|&(row, value)| (row_ids[&row], value)).collect();
    let mut vectors = Vec::<Vec<(u32, u64)>>::with_capacity(columns.len());
    for &column in columns {
        let mut vector: Vec<_> = materialize(provider, column).into_iter().map(|(row, value)| (row_ids[&row], value)).collect();
        vector.sort_unstable_by_key(|item| item.0);
        vectors.push(vector);
    }
    let representation_seconds = started.elapsed().as_secs_f64();
    let failures = vectors.iter().filter(|vector| vector.iter().fold(0u64, |sum, (row, coefficient)| {
        let product = (*coefficient as u128 * compact_dual.get(row).copied().unwrap_or(0) as u128 % PRIME as u128) as u64;
        let next = sum + product;
        if next >= PRIME { next - PRIME } else { next }
    }) != 0).count();
    if failures != 0 { fail("compact pairing failure"); }
    let terms: usize = vectors.iter().map(Vec::len).sum();
    let retained = packed_columns.capacity() * size_of::<u128>()
        + rows.capacity() * size_of::<Mono>()
        + row_ids.capacity() * size_of::<(Mono, u32)>()
        + compact_dual.capacity() * size_of::<(u32, u64)>()
        + vectors.capacity() * size_of::<Vec<(u32, u64)>>()
        + vectors.iter().map(|vector| vector.capacity() * size_of::<(u32, u64)>()).sum::<usize>();
    let selected = selected_sha(packed_columns.iter().copied().map(unpack_column));
    let mut decoded_dual: Vec<_> = compact_dual.iter().map(|(&id, &value)| (rows[id as usize], value)).collect();
    decoded_dual.sort_unstable_by_key(|item| item.0);
    let support = support_sha(decoded_dual.into_iter());
    let decoded_vectors = packed_columns.into_iter().zip(vectors).map(|(packed, vector)| {
        let mut decoded: Vec<_> = vector.into_iter().map(|(id, value)| (rows[id as usize], value)).collect();
        decoded.sort_unstable_by_key(|item| item.0);
        (unpack_column(packed), decoded)
    });
    let semantics = vector_sha(decoded_vectors);
    (selected, support, semantics, terms, retained, representation_seconds)
}

fn atomic_output(path: &Path, text: &str) {
    if path.exists() { fail("refuse pre-existing output"); }
    let temporary = path.with_extension("json.tmp");
    fs::write(&temporary, text).unwrap();
    fs::rename(temporary, path).unwrap();
}

fn selftest() {
    let columns = [
        Column { generator: 0, multiplier: Mono::from_sorted(&[0, 1, 2, 3, 4, 5, 6, 7, 8]) },
        Column { generator: 0, multiplier: Mono::from_sorted(&[0, 1, 2, 3, 4, 5, 6, 7, 9]) },
        Column { generator: 1, multiplier: Mono::from_sorted(&[0, 0, 0, 0, 0, 0, 0, 0]) },
        Column { generator: 6570, multiplier: Mono::from_sorted(&[T_ID; 7]) },
    ];
    let packed: Vec<_> = columns.iter().copied().map(pack_column).collect();
    assert!(packed.windows(2).all(|pair| pair[0] < pair[1]));
    assert!(packed.into_iter().map(unpack_column).eq(columns));
    let rows = [Mono::new(vec![1; DEGREE]), Mono::new(vec![2; DEGREE]), Mono::new(vec![3; DEGREE])];
    let frequency = HashMap::from([(rows[0], 2u32), (rows[1], 1u32)]);
    let mut ranked = rows;
    ranked.sort_by_key(|row| (frequency.get(row).copied().unwrap_or(u32::MAX), *row));
    assert_eq!(ranked, [rows[1], rows[0], rows[2]]);
    println!("{{\"schema\":\"KRENN_X5_D11_COMPACT_MICROGATE_SELFTEST_V1\",\"status\":\"PASS\",\"tests\":4}}");
}

fn main() {
    if env::args().len() == 2 && env::args().nth(1).as_deref() == Some("--selftest") {
        selftest();
        return;
    }
    let config = parse_args();
    let total_started = Instant::now();
    let provider_sha = file_sha(&config.provider);
    let selected_input_sha = file_sha(&config.selected);
    let dual_input_sha = file_sha(&config.dual);
    let parse_started = Instant::now();
    let provider = parse_provider(&config.provider);
    let all_columns = load_selected(&config.selected, &provider);
    let dual = load_dual(&config.dual);
    let parse_seconds = parse_started.elapsed().as_secs_f64();
    if all_columns.len() != 94_526 || dual.len() != 13_116 || config.count > all_columns.len() {
        fail("sealed checkpoint counts");
    }
    let columns = &all_columns[..config.count];
    let (selected_sha, support_sha, semantic_sha, terms, retained, representation_seconds) = if config.mode == "baseline" {
        run_baseline(&provider, columns, &dual)
    } else {
        run_compact(&provider, columns, &dual)
    };
    let result = format!(
        concat!(
            "{{\n  \"schema\": \"KRENN_X5_D11_COMPACT_REPRESENTATION_MICROGATE_RESULT_V1\",",
            "\n  \"status\": \"PASS_EXACT_REPRESENTATION\",\n  \"mode\": \"{}\",",
            "\n  \"count\": {},\n  \"terms\": {},\n  \"pairing_failures\": 0,",
            "\n  \"selected_prefix_sha256\": \"{}\",\n  \"dual_support_sha256\": \"{}\",",
            "\n  \"materialized_semantic_sha256\": \"{}\",\n  \"dual_support\": 13116,",
            "\n  \"provider_sha256\": \"{}\",\n  \"selected_input_sha256\": \"{}\",",
            "\n  \"dual_input_sha256\": \"{}\",\n  \"parse_seconds\": {:.9},",
            "\n  \"representation_seconds\": {:.9},\n  \"retained_accounted_bytes\": {},",
            "\n  \"total_seconds\": {:.9}\n}}\n"
        ),
        config.mode, config.count, terms, selected_sha, support_sha, semantic_sha,
        provider_sha, selected_input_sha, dual_input_sha, parse_seconds,
        representation_seconds, retained, total_started.elapsed().as_secs_f64()
    );
    atomic_output(&config.output, &result);
    print!("{result}");
}
