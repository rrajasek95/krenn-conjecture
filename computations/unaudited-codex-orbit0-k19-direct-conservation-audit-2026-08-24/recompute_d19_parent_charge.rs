//! Recompute direct-K19 full/irreducible charge with the three true 3+4+4 permutations.
#![allow(dead_code)]

mod audit {
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    #[derive(Clone, Copy, Default)]
    struct Totals {
        rows: u64,
        irreducible_rows: u64,
        full_charge: i128,
        irreducible_charge: i128,
    }

    impl Totals {
        fn add(&mut self, other: Totals) {
            self.rows += other.rows;
            self.irreducible_rows += other.irreducible_rows;
            self.full_charge += other.full_charge;
            self.irreducible_charge += other.irreducible_charge;
        }
    }

    fn add_row(out: &mut Totals, row: Row, mass: i128, e: &E) {
        let q = charge(&row, e) as i128;
        out.rows += 1;
        out.full_charge -= mass * q;
        if avail(sig(&row, e), e).is_empty() {
            out.irreducible_rows += 1;
            out.irreducible_charge -= mass * q;
        }
    }

    fn worker(e: std::sync::Arc<E>, start: usize, step: usize) -> (Totals, Totals) {
        let mut corrected = Totals::default();
        let mut historical = Totals::default();

        for r in e.records.iter().skip(start).step_by(step) {
            let mass = (r.size as i128) * (r.coefficient as i128);

            // Correct source: choose each of the three factor positions for K3 once.
            for low in 0..3 {
                let other: Vec<_> = (0..3).filter(|&x| x != low).collect();
                for a in &e.factor[low][1] {
                    for b in &e.factor[other[0]][2] {
                        for c in &e.factor[other[1]][2] {
                            let row = match low {
                                0 => make(r, a, b, c),
                                1 => make(r, b, a, c),
                                _ => make(r, b, c, a),
                            };
                            add_row(&mut corrected, row, mass, &e);
                        }
                    }
                }
            }

            // Historical source from merge_and_charge_k19.rs, retained as a hostile control.
            for high in 0..3 {
                let other: Vec<_> = (0..3).filter(|&x| x != high).collect();
                for a in &e.factor[other[0]][1] {
                    for b in &e.factor[other[1]][2] {
                        for c in &e.factor[high][2] {
                            let row = match high {
                                0 => make(r, c, a, b),
                                1 => make(r, a, c, b),
                                _ => make(r, a, b, c),
                            };
                            add_row(&mut historical, row, mass, &e);
                        }
                    }
                }
            }
        }

        (corrected, historical)
    }

    pub fn run() {
        let e = std::sync::Arc::new(parse());
        let mut jobs = Vec::new();
        for t in 0..8 {
            let copy = e.clone();
            jobs.push(std::thread::spawn(move || worker(copy, t, 8)));
        }
        let mut corrected = Totals::default();
        let mut historical = Totals::default();
        for job in jobs {
            let (a, b) = job.join().unwrap();
            corrected.add(a);
            historical.add(b);
        }

        println!(
            concat!(
                "corrected rows={} irreducible_rows={} full={} irreducible={} pivotable={}\n",
                "historical rows={} irreducible_rows={} full={} irreducible={} pivotable={}\n",
                "delta full={} irreducible={} pivotable={}"
            ),
            corrected.rows,
            corrected.irreducible_rows,
            corrected.full_charge,
            corrected.irreducible_charge,
            corrected.full_charge - corrected.irreducible_charge,
            historical.rows,
            historical.irreducible_rows,
            historical.full_charge,
            historical.irreducible_charge,
            historical.full_charge - historical.irreducible_charge,
            corrected.full_charge - historical.full_charge,
            corrected.irreducible_charge - historical.irreducible_charge,
            (corrected.full_charge - corrected.irreducible_charge)
                - (historical.full_charge - historical.irreducible_charge),
        );
    }
}

fn main() {
    audit::run();
}
