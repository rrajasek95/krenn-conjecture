mod referee {
    #![allow(dead_code)]
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    use std::fs::{metadata, rename, File};
    use std::io::{Read, Seek, SeekFrom};

    const K4_PATH: &str = "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin";
    const OUTPUT: &str = "computations/unaudited-codex-orbit0-k22-profile-ready-charge-2026-08-24/results_k22_profile_literal_sample_referee.json";
    const SAMPLES: u64 = 257;

    #[derive(Clone, Copy)]
    enum Kind { Direct, K14, K15, K16 }
    #[derive(Clone, Copy)]
    struct Spec { name: &'static str, path: &'static str, kind: Kind, header: u64, record: u64, records: u64 }

    fn i128le(x: &[u8]) -> i128 { i128::from_le_bytes(x.try_into().unwrap()) }
    fn u64x(x: &[u8]) -> u64 { u64::from_le_bytes(x.try_into().unwrap()) }

    fn k4_tails() -> Vec<Vec<[u8; 4]>> {
        let bytes = read(K4_PATH).unwrap();
        assert_eq!(&bytes[..7], b"K18K4A1");
        let mut at = 7usize;
        let mut result = vec![Vec::new(); 78];
        for pivot in 0..78 {
            for _ in 0..60 {
                let mut tail = [0u8; 4];
                tail.copy_from_slice(&bytes[at..at + 4]);
                at += 4;
                result[pivot].push(tail);
            }
        }
        assert_eq!(at, bytes.len());
        result
    }

    fn direct_row(e: &E, lineage: u8, ri: u16, ix: [u8; 3]) -> Row {
        assert!(lineage < 6 && (ri as usize) < e.records.len());
        let record = &e.records[ri as usize];
        let index = [ix[0] as usize, ix[1] as usize, ix[2] as usize];
        if lineage < 3 {
            let low = lineage as usize;
            let other: Vec<_> = (0..3).filter(|&x| x != low).collect();
            let a = e.factor[low][0][index[low]];
            let b = e.factor[other[0]][2][index[other[0]]];
            let c = e.factor[other[1]][2][index[other[1]]];
            match low { 0 => make(record, &a, &b, &c), 1 => make(record, &b, &a, &c), _ => make(record, &b, &c, &a) }
        } else {
            let high = (lineage - 3) as usize;
            let other: Vec<_> = (0..3).filter(|&x| x != high).collect();
            let a = e.factor[other[0]][1][index[other[0]]];
            let b = e.factor[other[1]][1][index[other[1]]];
            let c = e.factor[high][2][index[high]];
            match high { 0 => make(record, &c, &a, &b), 1 => make(record, &a, &c, &b), _ => make(record, &a, &b, &c) }
        }
    }

    fn inspect(spec: Spec, e: &E, tails: &[Vec<[u8; 4]>]) -> (i128, u64, u64, u64, u64) {
        assert_eq!(metadata(spec.path).unwrap().len(), spec.header + spec.record * spec.records);
        let mut file = File::open(spec.path).unwrap();
        let mut header = vec![0u8; spec.header as usize];
        file.read_exact(&mut header).unwrap();
        let magic: &[u8; 8] = match spec.kind { Kind::Direct => b"D18MRG1\0", Kind::K14 => b"K14MRG1\0", Kind::K15 => b"K15MRG1\0", Kind::K16 => b"K16MRG1\0" };
        assert_eq!(&header[..8], magic);
        let mut sample_charge = 0i128;
        let mut index_checksum = 0u64;
        let mut profile_checks = 0u64;
        let mut terminal_checks = 0u64;
        let mut literal_tail_checks = 0u64;
        for sample in 0..SAMPLES {
            let index = if SAMPLES == 1 { 0 } else { sample * (spec.records - 1) / (SAMPLES - 1) };
            index_checksum = index_checksum.wrapping_add(index.wrapping_mul(sample + 1));
            file.seek(SeekFrom::Start(spec.header + spec.record * index)).unwrap();
            let mut z = vec![0u8; spec.record as usize];
            file.read_exact(&mut z).unwrap();
            let (stored_profile, stored_sig, pivot, weight, row) = match spec.kind {
                Kind::Direct => {
                    let mut p = [0u8; 29]; p.copy_from_slice(&z[1..30]);
                    let mut s = [0u8; 12]; s.copy_from_slice(&z[30..42]);
                    let row = direct_row(e, z[0], u16::from_le_bytes(z[67..69].try_into().unwrap()), [z[69], z[70], z[71]]);
                    (p, s, z[42] as usize, i128le(&z[43..59]), row)
                }
                Kind::K14 | Kind::K15 | Kind::K16 => {
                    let mut p = [0u8; 29]; p.copy_from_slice(&z[..29]);
                    let mut s = [0u8; 12]; s.copy_from_slice(&z[29..41]);
                    let mut cells = [0u8; 24]; cells.copy_from_slice(&z[66..90]);
                    assert!(cells.windows(2).all(|x| x[0] <= x[1]));
                    let m1 = z[101] as i128;
                    let m2 = z[102] as i128;
                    assert!(m1 > 0 && m2 > 0 && 400_591_699_200i128 % (m1 * m2) == 0);
                    assert_eq!(z[100], z[41]);
                    (p, s, z[41] as usize, i128le(&z[42..58]), Row(cells))
                }
            };
            assert_ne!(weight, 0);
            assert_eq!(sig(&row, e), stored_sig);
            assert_eq!(profile(&row, pivot, e), stored_profile);
            assert!(avail(stored_sig, e).contains(&pivot));
            assert_eq!(stored_sig.iter().map(|&x| x as usize).sum::<usize>(), 6);
            assert_eq!(e.piv[pivot].iter().map(|&x| x as usize).sum::<usize>(), 4);
            profile_checks += 1;
            for tail in &tails[pivot] {
                let child_signature = child_sig(stored_sig, pivot, tail, e);
                assert_eq!(child_signature.iter().map(|&x| x as usize).sum::<usize>(), 2);
                assert!(avail(child_signature, e).is_empty());
                let child = replace(&row, &e.anchors[pivot], tail);
                sample_charge += weight * charge(&child, e) as i128;
                terminal_checks += 1;
                literal_tail_checks += 1;
            }
        }
        (sample_charge, index_checksum, profile_checks, terminal_checks, literal_tail_checks)
    }

    pub fn run_main() {
        let begun = Instant::now();
        let e = parse();
        assert!(e.piv.iter().all(|p| p.iter().map(|&x| x as usize).sum::<usize>() == 4));
        let tails = k4_tails();
        let specs = [
            Spec { name: "direct_D18_R4", path: "computations/unaudited-codex-orbit0-direct-k18-profile-census-2026-08-23/direct_k18_enriched_profiles.bin", kind: Kind::Direct, header: 256, record: 72, records: 979_091 },
            Spec { name: "D14_R4_4", path: "computations/unaudited-codex-orbit0-k18-k14-full-profiles-2026-08-23/k14_k4_enriched_profiles.bin", kind: Kind::K14, header: 256, record: 104, records: 18_217_226 },
            Spec { name: "grouped_D15_R3_4", path: "computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/checkpoint_k15_k3_profiles_merged.bin", kind: Kind::K15, header: 128, record: 104, records: 25_564_391 },
            Spec { name: "grouped_D16_R2_4", path: "computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/checkpoint_k16_k2_profiles_merged.bin", kind: Kind::K16, header: 128, record: 104, records: 6_876_260 },
        ];
        let mut rows = Vec::new();
        for spec in specs {
            let (sample_charge, checksum, profiles, terminals, literals) = inspect(spec, &e, &tails);
            rows.push(format!(concat!(
                "{{\"name\":\"{}\",\"distributed_records\":{},\"index_checksum\":{},",
                "\"profile_vs_row_checks\":{},\"literal_K4_tail_checks\":{},",
                "\"terminal_child_checks\":{},\"sample_charge_scaled_U\":\"{}\"}}"),
                spec.name, SAMPLES, checksum, profiles, literals, terminals, sample_charge));
        }
        let text = format!(concat!(
            "{{\n  \"status\":\"PASS_INDEPENDENT_DISTRIBUTED_LITERAL_K22_PROFILE_REFEREE\",\n",
            "  \"samples_per_group\":{},\n  \"groups\":[{}],\n",
            "  \"total_distributed_records\":{},\n  \"total_literal_K4_tail_checks\":{},\n",
            "  \"all_profile_signature_pivot_witnesses_replayed\":true,\n",
            "  \"all_sample_children_anchor_sum_2_and_nonpivotable\":true,\n",
            "  \"elapsed_seconds\":{:.6}\n}}\n"),
            SAMPLES, rows.join(",\n    "), SAMPLES * 4, SAMPLES * 4 * 60,
            begun.elapsed().as_secs_f64());
        let temporary = format!("{}.tmp", OUTPUT);
        std::fs::write(&temporary, &text).unwrap();
        rename(&temporary, OUTPUT).unwrap();
        print!("{text}");
    }
}

fn main() { referee::run_main(); }
