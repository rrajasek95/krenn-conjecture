mod charge_eval {
    #![allow(dead_code)]
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    use std::fs::File;
    use std::io::{BufReader, Read, Seek, SeekFrom};

    const PATH: &str = "computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/k14_k4_enriched_profiles.bin";
    const OUT: &str = "computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/results_k14_k4_k2_charge.json";
    const U2: i128 = 400_591_699_200;
    const HEADER: u64 = 256;
    const REC: u64 = 104;

    #[derive(Clone, Copy, Default)]
    struct EvalStat {
        profiles: u64, tail_evals: u64, irr_tail_evals: u64,
        retained_occ_tails: u64, retained_irr_occ_tails: u64,
        full_q: i128, irr_q: i128, profile_replays: u64,
    }
    impl EvalStat { fn add(&mut self, x: EvalStat) {
        self.profiles += x.profiles; self.tail_evals += x.tail_evals;
        self.irr_tail_evals += x.irr_tail_evals;
        self.retained_occ_tails += x.retained_occ_tails;
        self.retained_irr_occ_tails += x.retained_irr_occ_tails;
        self.full_q += x.full_q; self.irr_q += x.irr_q;
        self.profile_replays += x.profile_replays;
    }}

    fn worker(e: Arc<E>, start: u64, end: u64) -> EvalStat {
        let mut f = BufReader::with_capacity(8 << 20, File::open(PATH).unwrap());
        f.seek(SeekFrom::Start(HEADER + REC * start)).unwrap();
        let mut out = EvalStat::default();
        let mut b = [0u8; REC as usize];
        for index in start..end {
            f.read_exact(&mut b).unwrap();
            let mut stored_profile = [0u8; 29]; stored_profile.copy_from_slice(&b[..29]);
            let mut s = [0u8; 12]; s.copy_from_slice(&b[29..41]);
            let p = b[41] as usize;
            let weight = i128::from_le_bytes(b[42..58].try_into().unwrap());
            let uses = u64::from_le_bytes(b[58..66].try_into().unwrap());
            let mut cells = [0u8; 24]; cells.copy_from_slice(&b[66..90]);
            let row = Row(cells);
            assert_ne!(weight, 0); assert!(uses > 0); assert!(p < e.anchors.len());
            assert_eq!(sig(&row, &e), s); assert!(avail(s, &e).contains(&p));
            // Replay every 1024th literal witness plus both endpoints per worker.
            if index == start || index + 1 == end || index % 1024 == 0 {
                assert_eq!(profile(&row, p, &e), stored_profile); out.profile_replays += 1;
            }
            for t in &e.tails[p][0] {
                let child = replace(&row, &e.anchors[p], t);
                let q = charge(&child, &e) as i128;
                out.full_q += weight * q;
                out.tail_evals += 1; out.retained_occ_tails += uses;
                if avail(child_sig(s, p, t, &e), &e).is_empty() {
                    out.irr_q += weight * q; out.irr_tail_evals += 1;
                    out.retained_irr_occ_tails += uses;
                }
            }
            out.profiles += 1;
        }
        out
    }

    pub fn run() {
        let begun = Instant::now();
        let mut f = File::open(PATH).unwrap(); let mut h = [0u8; HEADER as usize]; f.read_exact(&mut h).unwrap();
        assert_eq!(&h[..8], b"K14MRG1\0"); assert_eq!(u64::from_le_bytes(h[8..16].try_into().unwrap()), U2 as u64);
        let n = u64::from_le_bytes(h[56..64].try_into().unwrap());
        let e = Arc::new(parse()); let workers = 8u64; let mut jobs = Vec::new();
        for t in 0..workers { let x=e.clone(); let lo=n*t/workers; let hi=n*(t+1)/workers; jobs.push(thread::spawn(move || worker(x,lo,hi))); }
        let mut total = EvalStat::default(); for j in jobs { total.add(j.join().unwrap()); }
        assert_eq!(total.profiles,n); assert_eq!(total.tail_evals,12*n);
        let text=format!(concat!("{{\n  \"status\":\"PASS_OCCURRENCEWISE_SIGNED_K2_CHARGE\",\n",
            "  \"scale_U\":{},\n  \"merged_profiles\":{},\n  \"literal_tail_evaluations\":{},\n",
            "  \"irreducible_tail_evaluations\":{},\n  \"retained_profile_occurrence_tails\":{},\n",
            "  \"retained_irreducible_occurrence_tails\":{},\n  \"full_charge_scaled\":\"{}\",\n",
            "  \"irreducible_charge_scaled\":\"{}\",\n  \"literal_witness_profile_replays\":{},\n",
            "  \"scope_guard\":\"one K14/K4-derived K18-to-K20 path; exact signed profile charge, no row collection and no K21 tails\",\n",
            "  \"elapsed_seconds\":{:.6}\n}}\n"),U2,n,total.tail_evals,total.irr_tail_evals,
            total.retained_occ_tails,total.retained_irr_occ_tails,total.full_q,total.irr_q,total.profile_replays,begun.elapsed().as_secs_f64());
        std::fs::write(OUT,&text).unwrap(); print!("{}",text);
    }
}
fn main(){charge_eval::run()}
