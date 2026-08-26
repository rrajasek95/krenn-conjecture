use std::env;
use std::fs;
use std::time::Instant;

use symbolica::prelude::*;


fn main() {
    let path = env::args().nth(1).expect("usage: n8-groebner-bench INPUT.ms");
    let source = fs::read_to_string(&path).expect("cannot read input");
    let mut lines = source.lines();
    let variables = lines.next().expect("missing variable line");
    let characteristic: u32 = lines.next().expect("missing characteristic")
        .parse().expect("bad characteristic");
    assert!(characteristic > 1, "benchmark currently requires a prime field");
    for variable in variables.split(',') {
        symbol!(variable.trim());
    }
    let body = lines.collect::<Vec<_>>().join("\n");
    let polynomials = body.split(',')
        .map(str::trim)
        .filter(|value| !value.is_empty())
        .collect::<Vec<_>>();

    let parse_started = Instant::now();
    let lex_ideal: Vec<MultivariatePolynomial<_, u16>> = polynomials.iter()
        .map(|value| {
            let atom = parse!(value).expand();
            atom.to_polynomial(&Zp::new(characteristic), None)
        })
        .collect();
    let ideal: Vec<_> = lex_ideal.iter()
        .map(|poly| poly.reorder::<GrevLexOrder>())
        .collect();
    eprintln!("parsed {} polynomials in {:.3}s", ideal.len(),
              parse_started.elapsed().as_secs_f64());

    let solve_started = Instant::now();
    let basis = GroebnerBasis::new(&ideal, true);
    let elapsed = solve_started.elapsed().as_secs_f64();
    let unit = basis.system.len() == 1
        && basis.system[0].is_constant()
        && !basis.system[0].is_zero();
    let terms: usize = basis.system.iter().map(|poly| poly.nterms()).sum();
    println!("engine=symbolica-2.2.0");
    println!("characteristic={characteristic}");
    println!("input_polynomials={}", ideal.len());
    println!("basis_polynomials={}", basis.system.len());
    println!("basis_terms={terms}");
    println!("unit={unit}");
    println!("solve_seconds={elapsed:.6}");
}
