mod audit {
    #![allow(dead_code, unused_imports)]
    include!(
        "../unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs"
    );

    use std::fs::metadata;

    const INPUT: &str = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin";
    const SAMPLES: &str = "computations/unaudited-codex-orbit0-k21-remaining22-design-2026-08-24/results_hidden_223_k21_charge.json.samples.tsv";
    const OUTPUT: &str = "computations/unaudited-codex-orbit0-k21-remaining22-design-2026-08-24/results_hidden_223_k21_referee_samples.json";
    const RECORD: usize = 80;
    const RECORDS: u64 = 158_439_965;
    const PAIR_ORBITS: u64 = 101_545_723;
    const PRIOR_CHILDREN: u64 = 1_218_548_676;
    const MASS: i128 = 724_159_651_336_720_220_160;

    #[derive(Clone, Copy)]
    struct Parent {
        row: Row,
        weight: i128,
        witness: Row,
        p2: u8,
        t2: u8,
        pair_uses: u64,
        orbit: u16,
        stabilizer: u16,
        pivotable: u8,
        m2: u8,
    }

    fn decode(rec: &[u8; RECORD]) -> Parent {
        let mut row = [0; 24];
        row.copy_from_slice(&rec[..24]);
        let mut witness = [0; 24];
        witness.copy_from_slice(&rec[40..64]);
        Parent {
            row: Row(row),
            weight: i128::from_le_bytes(rec[24..40].try_into().unwrap()),
            witness: Row(witness),
            p2: rec[64],
            t2: rec[65],
            pair_uses: u64::from_le_bytes(rec[66..74].try_into().unwrap()),
            orbit: u16::from_le_bytes(rec[74..76].try_into().unwrap()),
            stabilizer: u16::from_le_bytes(rec[76..78].try_into().unwrap()),
            pivotable: rec[78],
            m2: rec[79],
        }
    }

    fn row_hex(row: &Row) -> String {
        row.0.iter().map(|x| format!("{:02x}", x)).collect()
    }

    fn expected_indices() -> Vec<u64> {
        (0..257).map(|j| j * (RECORDS - 1) / 256).collect()
    }

    pub fn run() {
        let e = parse();
        let c = cenv();

        // Universal terminality theorem: a K18 parent has anchor sum 6;
        // every K0 pivot consumes anchor sum 4; every K3 tail restores anchor
        // sum 1.  Hence every K21 child has anchor sum 3 and no K0 pivot,
        // each of which requires total anchor multiplicity 4, can divide it.
        assert_eq!(e.pivots.len(), 78);
        assert!(e.pivots.iter().all(|p| p.iter().map(|&x| x as usize).sum::<usize>() == 4));
        assert_eq!(e.all_k3.len(), 78);
        let mut universal_k3_tails = 0u64;
        for tails in &e.all_k3 {
            assert_eq!(tails.len(), 32);
            for tail in tails {
                assert_eq!(tail_signature(tail, &e).iter().map(|&x| x as usize).sum::<usize>(), 1);
                universal_k3_tails += 1;
            }
        }
        assert_eq!(universal_k3_tails, 78 * 32);

        let mut input = File::open(INPUT).unwrap();
        let mut header = [0u8; 80];
        input.read_exact(&mut header).unwrap();
        assert_eq!(&header[..8], b"H18PIV2\0");
        assert_eq!(i128::from_le_bytes(header[8..24].try_into().unwrap()), U);
        assert_eq!(&header[24..28], &[0, 0, 0, 0]);
        assert_eq!(u16::from_le_bytes(header[28..30].try_into().unwrap()) as usize, RECORD);
        assert_eq!(&header[30..32], &[0, 0]);
        assert_eq!(u64::from_le_bytes(header[32..40].try_into().unwrap()), PAIR_ORBITS);
        assert_eq!(u64::from_le_bytes(header[40..48].try_into().unwrap()), PRIOR_CHILDREN);
        assert_eq!(u64::from_le_bytes(header[48..56].try_into().unwrap()), RECORDS);
        assert_eq!(u64::from_le_bytes(header[56..64].try_into().unwrap()), 1);
        assert_eq!(i128::from_le_bytes(header[64..80].try_into().unwrap()), MASS);
        assert_eq!(metadata(INPUT).unwrap().len(), 80 + RECORDS * RECORD as u64);

        let text = std::fs::read_to_string(SAMPLES).unwrap();
        let mut lines = text.lines();
        assert_eq!(lines.next().unwrap(), "input_index\trow\twitness_pair\tweight_before_p3\tm2\tm3\tpivot_uses\tK3_children\tcharge_scaled\tp2\tt2\tpair_uses\torbit\tstabilizer");
        let lines: Vec<_> = lines.collect();
        let indices = expected_indices();
        assert_eq!(lines.len(), indices.len());
        assert_eq!(indices.len(), 257);
        assert!(indices.windows(2).all(|w| w[0] < w[1]));
        assert_eq!((indices[0], *indices.last().unwrap()), (0, RECORDS - 1));

        let mut canonical_cache = HashMap::new();
        let mut response_cache: HashMap<PKey, (u64, i64)> = HashMap::new();
        let mut sample_hits = 0u64;
        let mut sample_misses = 0u64;
        let mut checked_pivots = 0u64;
        let mut checked_children = 0u64;
        let mut checked_charge = 0i128;
        let mut denominator_products = std::collections::BTreeSet::new();
        for (line, &index) in lines.iter().zip(&indices) {
            let fields: Vec<_> = line.split('\t').collect();
            assert_eq!(fields.len(), 14);
            assert_eq!(fields[0].parse::<u64>().unwrap(), index);
            input.seek(SeekFrom::Start(80 + index * RECORD as u64)).unwrap();
            let mut rec = [0u8; RECORD];
            input.read_exact(&mut rec).unwrap();
            let x = decode(&rec);
            assert_eq!(row_hex(&x.row), fields[1]);
            assert_eq!(row_hex(&x.witness), fields[2]);
            assert_eq!(x.weight, fields[3].parse::<i128>().unwrap());
            assert_eq!(x.m2, fields[4].parse::<u8>().unwrap());
            let recorded_m3 = fields[5].parse::<usize>().unwrap();
            assert_eq!(x.p2, fields[9].parse::<u8>().unwrap());
            assert_eq!(x.t2, fields[10].parse::<u8>().unwrap());
            assert_eq!(x.pair_uses, fields[11].parse::<u64>().unwrap());
            assert_eq!(x.orbit, fields[12].parse::<u16>().unwrap());
            assert_eq!(x.stabilizer, fields[13].parse::<u16>().unwrap());
            assert!(x.row.0.windows(2).all(|w| w[0] <= w[1]));
            assert!(x.witness.0.windows(2).all(|w| w[0] <= w[1]));
            assert_ne!(x.weight, 0);
            assert_eq!(x.pivotable, 1);
            assert!(x.pair_uses > 0);
            assert_eq!(u32::from(x.orbit) * u32::from(x.stabilizer), 384);

            // Replay the retained literal K16-pair/K2 witness into the stored
            // canonical K18 row.  It is a support witness, not a coefficient
            // decomposition of the already aggregated orbit mass.
            assert!((x.p2 as usize) < e.anchors.len());
            assert!((x.t2 as usize) < e.all_k2[x.p2 as usize].len());
            let witness_sig = signature(&x.witness.0, &e);
            assert_eq!(witness_sig.iter().map(|&z| z as usize).sum::<usize>(), 8);
            let witness_pivots = available(witness_sig, &e);
            assert_eq!(witness_pivots.len(), x.m2 as usize);
            assert!(witness_pivots.contains(&(x.p2 as usize)));
            let raw_child = replace_anchor(&x.witness, &e.anchors[x.p2 as usize], &e.all_k2[x.p2 as usize][x.t2 as usize]);
            assert_eq!(canonical(raw_child, &e, &mut canonical_cache), x.row);

            let sig = signature(&x.row.0, &e);
            assert_eq!(sig.iter().map(|&z| z as usize).sum::<usize>(), 6);
            let pivots = available(sig, &e);
            assert_eq!(pivots.len(), recorded_m3);
            let m3 = pivots.len() as i128;
            assert!(m3 > 0);
            assert_eq!(U % ((x.m2 as i128) * m3), 0);
            assert_eq!(x.weight % m3, 0);
            denominator_products.insert((x.m2 as i128) * m3);
            let w3 = -x.weight / m3;
            let mut parent_pivots = 0u64;
            let mut parent_children = 0u64;
            let mut parent_charge = 0i128;
            for p3 in pivots {
                parent_pivots += 1;
                let profile = path_profile(&x.row, p3, &e, &c);
                let key = PKey { profile, sig, pivot: p3 as u8 };
                let mut response_n = 0u64;
                let mut response_q = 0i64;
                for tail in &e.all_k3[p3] {
                    let predicted = child_sig(sig, p3, tail, &e);
                    assert_eq!(predicted.iter().map(|&z| z as usize).sum::<usize>(), 3);
                    assert!(available(predicted, &e).is_empty());
                    let child = replace_anchor(&x.row, &e.anchors[p3], tail);
                    let literal_sig = signature(&child.0, &e);
                    assert_eq!(literal_sig, predicted);
                    let literal = literal_ckey(&child, &c);
                    let abstracted = abstract_ckey(&profile, p3, tail, &e, &c);
                    assert_eq!(literal, abstracted);
                    response_n += 1;
                    response_q += *c.dual.get(&literal).unwrap_or(&0);
                }
                assert_eq!(response_n, 32);
                if let Some(&(n, q)) = response_cache.get(&key) {
                    sample_hits += 1;
                    assert_eq!((n, q), (response_n, response_q));
                } else {
                    sample_misses += 1;
                    response_cache.insert(key, (response_n, response_q));
                }
                parent_children += response_n;
                parent_charge += w3 * response_q as i128;
            }
            assert_eq!(parent_pivots, fields[6].parse::<u64>().unwrap());
            assert_eq!(parent_children, fields[7].parse::<u64>().unwrap());
            assert_eq!(parent_charge, fields[8].parse::<i128>().unwrap());
            checked_pivots += parent_pivots;
            checked_children += parent_children;
            checked_charge += parent_charge;
        }
        assert_eq!(checked_children, 32 * checked_pivots);
        assert_eq!(sample_hits + sample_misses, checked_pivots);
        assert_eq!(sample_misses as usize, response_cache.len());

        let products = denominator_products.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",");
        let result = format!(
            concat!(
                "{{\n",
                "  \"status\":\"PASS_INDEPENDENT_257_LITERAL_HIDDEN_223_K21_REFEREE\",\n",
                "  \"lineage_id\":\"D14:222|R:2-2-3\",\n",
                "  \"input_header\":{{\"magic\":\"H18PIV2\",\"scale_U\":\"{}\",\"record_bytes\":{},\"pair_orbits\":{},\"prior_K2_children\":{},\"records\":{},\"flag\":1,\"signed_mass_scaled\":\"{}\",\"exact_file_size\":{}}},\n",
                "  \"universal_terminality\":{{\"pivot_signatures\":78,\"pivot_anchor_sum\":4,\"K3_tail_families\":78,\"K3_tails_checked\":{},\"K3_tail_anchor_sum\":1,\"K18_parent_anchor_sum\":6,\"K21_child_anchor_sum\":3,\"all_K21_children_nonpivotable\":true}},\n",
                "  \"literal_sample\":{{\"parents\":257,\"first_index\":0,\"last_index\":{},\"pivots\":{},\"K3_children\":{},\"charge_scaled\":\"{}\",\"witness_to_canonical_K18_replays\":257,\"literal_abstract_cycle_key_matches\":{},\"child_signature_terminality_checks\":{}}},\n",
                "  \"sample_cache\":{{\"distinct_keys\":{},\"hits\":{},\"misses\":{},\"query_identity_pass\":true,\"key_schema\":\"profile29,signature12,pivot\",\"cached_value_schema\":\"unweighted 32-tail count and cycle-charge sum\"}},\n",
                "  \"denominator_products_observed\":[{}],\n",
                "  \"sign_rule\":\"third response coefficient w3=-w2/m3; w2 is the signed, U-scaled K18 orbit mass after two prior responses\",\n",
                "  \"scope\":\"257 distributed random-access literal parents plus universal signature theorem; no full 158439965-parent rerun and no other lineage\"\n",
                "}}\n"
            ),
            U, RECORD, PAIR_ORBITS, PRIOR_CHILDREN, RECORDS, MASS, metadata(INPUT).unwrap().len(),
            universal_k3_tails, RECORDS - 1, checked_pivots, checked_children, checked_charge,
            checked_children, checked_children, response_cache.len(), sample_hits, sample_misses, products,
        );
        std::fs::write(OUTPUT, &result).unwrap();
        print!("{}", result);
    }
}

fn main() {
    audit::run()
}
