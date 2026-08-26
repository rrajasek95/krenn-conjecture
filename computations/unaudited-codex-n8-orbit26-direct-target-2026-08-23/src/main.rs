//! Deterministic exact contraction of the normalized direct F^h residual.
//!
//! Input provenance is exported from literal perfect matchings by
//! audit_orbit26_anchor_and_direct_boundary.py.  Coefficients are scaled by
//! four and remain integral.  We divide the y^6 boundary first by the chosen
//! monic constant-minimum generator through degree eight, then divide the
//! y^9 boundary by the chosen monic linear-minimum generator attached to its
//! smallest cell.  Every non-pivot output has larger y-degree, so this is an
//! acyclic source-labelled correction, not a rank inference.

use std::collections::HashMap;
use std::env;
use std::fs::File;
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::Path;
use std::time::Instant;

#[derive(Clone, Copy, Eq, Ord, PartialEq, PartialOrd)]
struct Mono {
    len: u8,
    data: [u8; 12],
}

impl Hash for Mono {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.len.hash(state);
        self.data[..self.len as usize].hash(state);
    }
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("contract-to-y10: {}", message.as_ref());
    std::process::exit(2);
}

impl Mono {
    fn from_hex(text: &str) -> Self {
        if text == "-" { return Self { len: 0, data: [0; 12] }; }
        if text.len() % 2 != 0 || text.len() > 24 {
            fail("bad monomial hex length");
        }
        let mut data = [0_u8; 12];
        let len = text.len() / 2;
        for index in 0..len {
            data[index] = u8::from_str_radix(&text[2 * index..2 * index + 2], 16)
                .unwrap_or_else(|_| fail("bad monomial hex"));
        }
        if !data[..len].windows(2).all(|window| window[0] <= window[1]) {
            fail("monomial is not sorted");
        }
        Self { len: len as u8, data }
    }

    fn multiply(self, other: Self) -> Self {
        let total = self.len as usize + other.len as usize;
        if total > 12 { fail("monomial product exceeds degree twelve"); }
        let left = &self.data[..self.len as usize];
        let right = &other.data[..other.len as usize];
        let mut data = [0_u8; 12];
        let (mut i, mut j, mut k) = (0, 0, 0);
        while i < left.len() || j < right.len() {
            if j == right.len() || (i < left.len() && left[i] <= right[j]) {
                data[k] = left[i];
                i += 1;
            } else {
                data[k] = right[j];
                j += 1;
            }
            k += 1;
        }
        Self { len: total as u8, data }
    }

    fn remove_first(self) -> (u8, Self) {
        if self.len == 0 { fail("cannot remove from empty monomial"); }
        let variable = self.data[0];
        let mut data = [0_u8; 12];
        data[..self.len as usize - 1]
            .copy_from_slice(&self.data[1..self.len as usize]);
        (variable, Self { len: self.len - 1, data })
    }

    fn hex(self) -> String {
        let mut answer = String::with_capacity(2 * self.len as usize);
        for value in &self.data[..self.len as usize] {
            answer.push_str(&format!("{value:02x}"));
        }
        answer
    }
}

fn add(map: &mut HashMap<Mono, i64>, row: Mono, delta: i64) {
    if delta == 0 { return; }
    let old = map.get(&row).copied().unwrap_or(0);
    let value = old.checked_add(delta).unwrap_or_else(|| fail("i64 coefficient overflow"));
    if value == 0 { map.remove(&row); } else { map.insert(row, value); }
}

fn scaled(value: i64, coefficient: i64, sign: i64) -> i64 {
    value.checked_mul(coefficient)
        .and_then(|item| item.checked_mul(sign))
        .unwrap_or_else(|| fail("i64 product overflow"))
}

struct Provider {
    constant_code: u16,
    constant_terms: [Vec<(Mono, i64)>; 5],
    linear_code: [u16; 252],
    linear_quadratic: Vec<Vec<(Mono, i64)>>,
}

fn read_provider(path: &Path) -> Provider {
    let input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut constant_code = None;
    let mut constant_terms: [Vec<(Mono, i64)>; 5] = std::array::from_fn(|_| Vec::new());
    let mut linear_code = [u16::MAX; 252];
    let mut linear_quadratic = vec![Vec::new(); 252];
    for (line_number, line) in input.lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if line_number == 0 {
            if fields != ["KRENN_N8_UNIQUE_MIN_PROVIDER_V1"] { fail("bad provider magic"); }
            continue;
        }
        match fields.first().copied() {
            Some("CONSTANT") if fields.len() == 3 => {
                constant_code = Some(fields[1].parse().unwrap_or_else(|_| fail("bad constant code")));
            },
            Some("CTERM") if fields.len() == 4 => {
                let degree: usize = fields[1].parse().unwrap_or_else(|_| fail("bad constant degree"));
                let term = Mono::from_hex(fields[2]);
                let coefficient = fields[3].parse().unwrap_or_else(|_| fail("bad constant coefficient"));
                if degree != term.len as usize || degree > 4 { fail("constant term degree mismatch"); }
                constant_terms[degree].push((term, coefficient));
            },
            Some("LINEAR") if fields.len() == 4 => {
                let variable: usize = fields[1].parse().unwrap_or_else(|_| fail("bad linear variable"));
                linear_code[variable] = fields[2].parse().unwrap_or_else(|_| fail("bad linear code"));
            },
            Some("L2") if fields.len() == 4 => {
                let variable: usize = fields[1].parse().unwrap_or_else(|_| fail("bad L2 variable"));
                let term = Mono::from_hex(fields[2]);
                if term.len != 2 { fail("L2 term is not quadratic"); }
                let coefficient = fields[3].parse().unwrap_or_else(|_| fail("bad L2 coefficient"));
                linear_quadratic[variable].push((term, coefficient));
            },
            _ => fail(format!("bad provider line {}", line_number + 1)),
        }
    }
    if constant_terms[0].len() != 1 || constant_terms[1].len() != 0
        || constant_terms[2].len() != 12 || constant_terms[3].len() != 32
        || constant_terms[4].len() != 60 {
        fail("constant provider profile changed");
    }
    let live: Vec<_> = (0..252).filter(|&index| linear_code[index] != u16::MAX).collect();
    if live.len() != 240 || live.iter().any(|&index| linear_quadratic[index].len() != 6) {
        fail("linear provider coverage/profile changed");
    }
    Provider {
        constant_code: constant_code.unwrap_or_else(|| fail("missing constant provider")),
        constant_terms,
        linear_code,
        linear_quadratic,
    }
}

fn read_residual(path: &Path) -> HashMap<Mono, i64> {
    let input = BufReader::new(File::open(path).unwrap_or_else(|error| fail(error.to_string())));
    let mut expected = None;
    let mut answer = HashMap::new();
    for (line_number, line) in input.lines().enumerate() {
        let line = line.unwrap_or_else(|error| fail(error.to_string()));
        let fields: Vec<_> = line.split_whitespace().collect();
        if line_number == 0 {
            if fields.len() != 5 || fields[..4] != ["KRENN_N8_DIRECT_FH_Y6_V1", "SCALE", "4", "COUNT"] {
                fail("bad residual magic");
            }
            expected = Some(fields[4].parse::<usize>().unwrap_or_else(|_| fail("bad residual count")));
            continue;
        }
        if fields.len() != 3 || fields[0] != "ROW" { fail("bad residual row"); }
        let row = Mono::from_hex(fields[1]);
        if row.len != 6 { fail("residual row is not y-degree six"); }
        let coefficient = fields[2].parse().unwrap_or_else(|_| fail("bad residual coefficient"));
        if coefficient == 0 || answer.insert(row, coefficient).is_some() { fail("bad duplicate/zero residual row"); }
    }
    if Some(answer.len()) != expected { fail("residual packet count changed"); }
    answer
}

fn convolve(input: &HashMap<Mono, i64>, terms: &[(Mono, i64)], sign: i64, label: &str, started: Instant) -> HashMap<Mono, i64> {
    let mut answer = HashMap::with_capacity(input.len().saturating_mul(terms.len()).min(50_000_000));
    for (position, (&row, &coefficient)) in input.iter().enumerate() {
        for &(term, term_coefficient) in terms {
            add(&mut answer, row.multiply(term), scaled(coefficient, term_coefficient, sign));
        }
        if (position + 1) % 250_000 == 0 {
            eprintln!("{label} inputs={} support={} elapsed={:.1}s", position + 1, answer.len(), started.elapsed().as_secs_f64());
        }
    }
    answer
}

fn main() {
    let arguments: Vec<_> = env::args().collect();
    if arguments.len() != 4 { fail("usage: contract-to-y10 RESIDUAL PROVIDER OUTPUT"); }
    let started = Instant::now();
    let residual6 = read_residual(Path::new(&arguments[1]));
    let provider = read_provider(Path::new(&arguments[2]));
    eprintln!("validated residual6={} constant_code={} elapsed={:.1}s", residual6.len(), provider.constant_code, started.elapsed().as_secs_f64());

    let mut core10 = convolve(&residual6, &provider.constant_terms[4], -1, "R6*h4", started);
    eprintln!("initial core10={} elapsed={:.1}s", core10.len(), started.elapsed().as_secs_f64());

    let residual8 = convolve(&residual6, &provider.constant_terms[2], -1, "R6*h2", started);
    let residual8_count = residual8.len();
    for (position, (&row, &coefficient)) in residual8.iter().enumerate() {
        for &(term, term_coefficient) in &provider.constant_terms[2] {
            add(&mut core10, row.multiply(term), scaled(coefficient, term_coefficient, -1));
        }
        if (position + 1) % 500_000 == 0 {
            eprintln!("R8*h2 inputs={} core10={} elapsed={:.1}s", position + 1, core10.len(), started.elapsed().as_secs_f64());
        }
    }
    drop(residual8);
    eprintln!("after degree8 pivots core10={} elapsed={:.1}s", core10.len(), started.elapsed().as_secs_f64());

    let residual9 = convolve(&residual6, &provider.constant_terms[3], -1, "R6*h3", started);
    let residual9_count = residual9.len();
    for (position, (&row, &coefficient)) in residual9.iter().enumerate() {
        let (variable, multiplier) = row.remove_first();
        if provider.linear_code[variable as usize] == u16::MAX { fail("degree-nine row chose a support variable"); }
        for &(term, term_coefficient) in &provider.linear_quadratic[variable as usize] {
            add(&mut core10, multiplier.multiply(term), scaled(coefficient, term_coefficient, -1));
        }
        if (position + 1) % 500_000 == 0 {
            eprintln!("R9*linear2 inputs={} core10={} elapsed={:.1}s", position + 1, core10.len(), started.elapsed().as_secs_f64());
        }
    }
    drop(residual9);
    eprintln!("terminal core10={} elapsed={:.1}s", core10.len(), started.elapsed().as_secs_f64());

    let mut rows: Vec<_> = core10.into_iter().collect();
    rows.sort_unstable_by_key(|item| item.0);
    let output = File::create(&arguments[3]).unwrap_or_else(|error| fail(error.to_string()));
    let mut output = BufWriter::new(output);
    writeln!(output, "KRENN_N8_DIRECT_FH_Y10_V1 SCALE 4 COUNT {}", rows.len()).unwrap();
    writeln!(output, "PIVOTS degree6_constant={} degree8_constant={} degree9_linear={}", residual6.len(), residual8_count, residual9_count).unwrap();
    writeln!(output, "PROVIDER constant_code={} deterministic_linear=smallest_cell_then_smallest_code", provider.constant_code).unwrap();
    for (row, coefficient) in rows {
        if row.len != 10 || coefficient == 0 { fail("bad terminal core row"); }
        writeln!(output, "ROW {} {}", row.hex(), coefficient).unwrap();
    }
    output.flush().unwrap();
    eprintln!("PASS output={} elapsed={:.1}s", arguments[3], started.elapsed().as_secs_f64());
}
