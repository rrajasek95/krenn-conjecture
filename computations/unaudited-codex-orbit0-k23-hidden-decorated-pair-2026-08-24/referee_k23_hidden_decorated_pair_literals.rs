mod inherited {
    #![allow(dead_code, unused_imports)]
    include!("../unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs");
    include!("k23_hidden_decorated_pair_impl.rs");

    fn field<T: std::str::FromStr>(fields: &[&str], index: usize) -> T
    where
        T::Err: std::fmt::Debug,
    {
        fields[index].parse().unwrap()
    }

    pub fn referee_main() {
        let args: Vec<String> = std::env::args().collect();
        let mut start = None;
        let mut end = None;
        let mut samples = None;
        let mut output = None;
        let mut arbitrary_indices = false;
        let mut i = 1;
        while i < args.len() {
            match args[i].as_str() {
                "--start" => {
                    start = Some(args[i + 1].parse::<u64>().unwrap());
                    i += 2;
                }
                "--end" => {
                    end = Some(args[i + 1].parse::<u64>().unwrap());
                    i += 2;
                }
                "--samples" => {
                    samples = Some(args[i + 1].clone());
                    i += 2;
                }
                "--output" => {
                    output = Some(args[i + 1].clone());
                    i += 2;
                }
                "--arbitrary-indices" => {
                    arbitrary_indices = true;
                    i += 1;
                }
                _ => panic!("usage: referee --start N --end N --samples PATH --output PATH"),
            }
        }
        let (start, end) = (start.unwrap(), end.unwrap());
        let samples = samples.unwrap();
        let output = output.unwrap();
        assert!(start < end && end <= K23_RECORDS);
        assert_eq!(k23_header(K23_PAIR_INPUT), K23_RECORDS);
        let engine = parse();
        let cycles = cenv();
        let text = std::fs::read_to_string(&samples).unwrap();
        let mut lines = text.lines();
        assert_eq!(lines.next().unwrap(), "input_index\tK16_row\tp2\tweight_after_p2\tpair_uses\torbit\tstabilizer\tR234_first_children\tR234_pivotable_intermediate\tR234_selected_p3\tR234_terminal_K23\tR234_terminal_weight_scaled\tR234_charge_scaled\tR243_first_children\tR243_pivotable_intermediate\tR243_selected_p3\tR243_terminal_K23\tR243_terminal_weight_scaled\tR243_charge_scaled\tR234_nonzero\tR243_nonzero");
        let rows = lines.collect::<Vec<_>>();
        assert_eq!(rows.len(), 257);
        let mut file = File::open(K23_PAIR_INPUT).unwrap();
        let mut prior = None;
        let mut nonzero34 = 0usize;
        let mut nonzero43 = 0usize;
        for (ordinal, line) in rows.iter().enumerate() {
            let fields = line.split('\t').collect::<Vec<_>>();
            assert_eq!(fields.len(), 21);
            let index = field::<u64>(&fields, 0);
            if !arbitrary_indices {
                let expected = start + ordinal as u64 * (end - start - 1) / 256;
                assert_eq!(index, expected);
            }
            assert!(start <= index && index < end);
            assert!(prior.map_or(true, |x| x < index));
            prior = Some(index);
            file.seek(SeekFrom::Start(
                K23_HEADER as u64 + K23_RECORD as u64 * index,
            ))
            .unwrap();
            let mut record = [0u8; K23_RECORD];
            file.read_exact(&mut record).unwrap();
            let pair = k23_decode(&record);
            assert_eq!(fields[1], k23_hex(&pair.key.row));
            assert_eq!(field::<u8>(&fields, 2), pair.key.pivot);
            assert_eq!(field::<i128>(&fields, 3), pair.weight_after_p2);
            assert_eq!(field::<u64>(&fields, 4), pair.uses);
            assert_eq!(field::<u16>(&fields, 5), pair.orbit);
            assert_eq!(field::<u16>(&fields, 6), pair.stabilizer);
            assert_eq!(record[..24], pair.key.row.0);
            assert_eq!(record[24], pair.key.pivot);
            assert_eq!(
                i128::from_le_bytes(record[25..41].try_into().unwrap()),
                pair.weight_after_p2
            );
            assert_eq!(
                u64::from_le_bytes(record[41..49].try_into().unwrap()),
                pair.uses
            );
            assert_eq!(
                u16::from_le_bytes(record[49..51].try_into().unwrap()),
                pair.orbit
            );
            assert_eq!(
                u16::from_le_bytes(record[51..53].try_into().unwrap()),
                pair.stabilizer
            );
            let d34 = k23_eval34_literal(pair, &engine, &cycles);
            let d43 = k23_eval43_literal(pair, &engine, &cycles);
            assert_eq!(field::<u64>(&fields, 7), d34.first_children);
            assert_eq!(field::<u64>(&fields, 8), d34.pivotable_intermediate);
            assert_eq!(field::<u64>(&fields, 9), d34.selected_p3);
            assert_eq!(field::<u64>(&fields, 10), d34.terminal_children);
            assert_eq!(field::<i128>(&fields, 11), d34.terminal_weight);
            assert_eq!(field::<i128>(&fields, 12), d34.charge);
            assert_eq!(field::<u64>(&fields, 13), d43.first_children);
            assert_eq!(field::<u64>(&fields, 14), d43.pivotable_intermediate);
            assert_eq!(field::<u64>(&fields, 15), d43.selected_p3);
            assert_eq!(field::<u64>(&fields, 16), d43.terminal_children);
            assert_eq!(field::<i128>(&fields, 17), d43.terminal_weight);
            assert_eq!(field::<i128>(&fields, 18), d43.charge);
            assert_eq!(field::<u8>(&fields, 19), (d34.selected_p3 > 0) as u8);
            assert_eq!(field::<u8>(&fields, 20), (d43.selected_p3 > 0) as u8);
            nonzero34 += (d34.selected_p3 > 0) as usize;
            nonzero43 += (d43.selected_p3 > 0) as usize;
        }
        let result = format!(concat!(
            "{{\n  \"status\":\"PASS_INDEPENDENT_K23_HIDDEN_DECORATED_PAIR_LITERAL_REPLAY\",\n",
            "  \"input_interval\":[{},{}],\n  \"samples\":257,\n",
            "  \"R234_nonzero\":{},\n  \"R243_nonzero\":{},\n",
            "  \"source_sha256_expected\":\"{}\",\n  \"source_header_checked\":true,\n",
            "  \"all_source_fields_exact\":true,\n  \"all_occurrencewise_U_and_weight_divisions_exact\":true,\n",
            "  \"all_literal_terminal_K23_children_nonpivotable\":true,\n",
            "  \"all_abstract_literal_cycle_keys_and_charges_equal\":true,\n",
            "  \"sign_rule\":\"w3=-w2/m3\",\n",
            "  \"sample_index_mode\":\"{}\",\n",
            "  \"scope\":\"independent literal replay for declared hidden-decorated source indices; no aggregate scalar or membership claim\"\n}}\n"
        ), start, end, nonzero34, nonzero43, K23_PAIR_SHA256,
            if arbitrary_indices { "caller-selected distinct sorted indices" } else { "exact interval-distributed indices" });
        let temporary = format!("{}.tmp", output);
        std::fs::write(&temporary, &result).unwrap();
        std::fs::rename(temporary, &output).unwrap();
        print!("{}", result);
    }
}

fn main() {
    inherited::referee_main();
}
