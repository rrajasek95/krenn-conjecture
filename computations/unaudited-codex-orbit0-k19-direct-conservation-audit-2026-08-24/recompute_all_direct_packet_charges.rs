//! Recompute the seven direct degree buckets from the literal 27 ordered packets.
//!
//! These packets are the complete expansion of the frozen leading input
//! `P = -R8' E0 E1 E2`; they are not the complete structured `a*T` stream.
#![allow(dead_code)]

mod audit {
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    fn worker(e: std::sync::Arc<E>, start: usize, step: usize) -> ([i128; 7], [u64; 7]) {
        let mut charge_by_degree = [0i128; 7];
        let mut rows_by_degree = [0u64; 7];
        for r in e.records.iter().skip(start).step_by(step) {
            let mass = (r.size as i128) * (r.coefficient as i128);
            for d0 in 0..3 {
                for d1 in 0..3 {
                    for d2 in 0..3 {
                        let bucket = d0 + d1 + d2; // actual degree is 14 + bucket
                        for a in &e.factor[0][d0] {
                            for b in &e.factor[1][d1] {
                                for c in &e.factor[2][d2] {
                                    let row = make(r, a, b, c);
                                    charge_by_degree[bucket] -= mass * (charge(&row, &e) as i128);
                                    rows_by_degree[bucket] += 1;
                                }
                            }
                        }
                    }
                }
            }
        }
        (charge_by_degree, rows_by_degree)
    }

    pub fn run() {
        let e = std::sync::Arc::new(parse());
        let mut jobs = Vec::new();
        for t in 0..8 {
            let copy = e.clone();
            jobs.push(std::thread::spawn(move || worker(copy, t, 8)));
        }
        let mut charges = [0i128; 7];
        let mut rows = [0u64; 7];
        for job in jobs {
            let (c, n) = job.join().unwrap();
            for i in 0..7 {
                charges[i] += c[i];
                rows[i] += n[i];
            }
        }
        let total: i128 = charges.iter().sum();
        for i in 0..7 {
            println!("K{} rows={} charge={}", 14 + i, rows[i], charges[i]);
        }
        println!("total_charge={}", total);
        // The leading input itself has this nonzero charge.  A correct filtered
        // reduction must preserve it; forcing zero here would incorrectly
        // identify this bounded stream with the complete structured target.
        assert_eq!(total, 4_564_224);
    }
}

fn main() {
    audit::run();
}
