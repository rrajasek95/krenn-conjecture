//! Cross-page conservation check for the direct K19 (3+4+4) source.
#![allow(dead_code)]

mod audit {
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    use std::collections::BTreeMap;

    pub fn run() {
        let args: Vec<String> = std::env::args().collect();
        let limit = args
            .windows(2)
            .find(|w| w[0] == "--limit-records")
            .map(|w| w[1].parse::<usize>().unwrap())
            .unwrap_or(1);
        let e = parse();
        let mut cache = HashMap::new();
        let mut rows = 0u64;
        let mut pivotable_rows = 0u64;
        let mut pivot_uses = 0u64;
        let mut failures = 0u64;
        let mut residual_hist = BTreeMap::<i64, u64>::new();
        let mut parent_sum = 0i128;
        let mut tail_sum = 0i128;

        for r in e.records.iter().take(limit) {
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
                            rows += 1;
                            let s = sig(&row, &e);
                            let pivots = avail(s, &e);
                            if pivots.is_empty() {
                                continue;
                            }
                            pivotable_rows += 1;
                            let parent_q = charge(&row, &e);
                            for p in pivots {
                                pivot_uses += 1;
                                let (q2, _, n2, _) = resp(&row, s, p, 2, &e, &mut cache);
                                let (q3, _, n3, _) = resp(&row, s, p, 3, &e, &mut cache);
                                let (q4, _, n4, _) = resp(&row, s, p, 4, &e, &mut cache);
                                assert_eq!((n2, n3, n4), (12, 32, 60));
                                let residual = parent_q + q2 + q3 + q4;
                                *residual_hist.entry(residual).or_default() += 1;
                                if residual != 0 {
                                    failures += 1;
                                }
                                parent_sum += parent_q as i128;
                                tail_sum += (q2 + q3 + q4) as i128;
                            }
                        }
                    }
                }
            }
        }

        println!(
            "records={} rows={} pivotable_rows={} pivot_uses={} cache={} failures={} parent_sum={} tail_sum={} residual_sum={} hist={:?}",
            limit.min(e.records.len()),
            rows,
            pivotable_rows,
            pivot_uses,
            cache.len(),
            failures,
            parent_sum,
            tail_sum,
            parent_sum + tail_sum,
            residual_hist
        );
    }
}

fn main() {
    audit::run();
}
