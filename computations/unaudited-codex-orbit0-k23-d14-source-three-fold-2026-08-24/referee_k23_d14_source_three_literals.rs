mod inherited {
    #![allow(dead_code, unused_imports)]
    include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

    const U23: i128 = 400_591_699_200;
    const IDS23: [&str; 3] = [
        "D14:222|R:3-2-4",
        "D14:222|R:3-3-3",
        "D14:222|R:4-2-3",
    ];

    #[derive(Default)]
    struct Counts23 {
        p1: u64,
        first: u64,
        pivotable_first: u64,
        p2: u64,
        second: u64,
        pivotable_second: u64,
        p3: u64,
        terminal: u64,
        charge: i128,
    }

    fn hex23(row: &Row) -> String {
        row.0.iter().map(|value| format!("{:02x}", value)).collect()
    }

    fn abstract_ckey23(prof: &[u8; 29], pivot: usize, tail: &[u8; 4], e: &E) -> CKey {
        let mut endpoint = [-1i8; 24];
        for (i, &cell) in e.anchors[pivot].iter().enumerate() {
            let [u, v, a, b] = e.cells[cell as usize];
            endpoint[(3 * u + a) as usize] = (2 * i) as i8;
            endpoint[(3 * v + b) as usize] = (2 * i + 1) as i8;
        }
        let mut closure = [255u8; 8];
        for &cell in tail {
            let [u, v, a, b] = e.cells[cell as usize];
            let x = endpoint[(3 * u + a) as usize];
            let y = endpoint[(3 * v + b) as usize];
            assert!(x >= 0 && y >= 0);
            closure[x as usize] = y as u8;
            closure[y as usize] = x as u8;
        }
        assert!(closure.iter().all(|&value| value != 255));
        let mut seen = [false; 8];
        let mut parts = [0u8; 12];
        let mut n = 0usize;
        for start in 0..8 {
            if seen[start] { continue; }
            let mut stack = [0u8; 8];
            let (mut top, mut nodes, mut pathsum) = (1usize, 0u8, 0u16);
            stack[0] = start as u8;
            seen[start] = true;
            while top > 0 {
                top -= 1;
                let x = stack[top] as usize;
                nodes += 1;
                pathsum += prof[8 + x] as u16;
                for y in [prof[x], closure[x]] {
                    if !seen[y as usize] {
                        seen[y as usize] = true;
                        stack[top] = y;
                        top += 1;
                    }
                }
            }
            parts[n] = (pathsum / 2 + nodes as u16 / 2) as u8;
            n += 1;
        }
        let closed = prof[16] as usize;
        for &value in &prof[17..17 + closed] { parts[n] = value; n += 1; }
        parts[..n].sort_unstable();
        let mut key = [0u8; 13];
        key[0] = n as u8;
        key[1..1 + n].copy_from_slice(&parts[..n]);
        CKey(key)
    }

    fn literal_path23(row14: Row, mass: i128, degrees: (usize, usize, usize), e: &E) -> Counts23 {
        let (d1, d2, d3) = degrees;
        let sig14 = sig(&row14, e);
        let pivots1 = valid(sig14, e);
        let m1 = pivots1.len();
        assert!(m1 > 0 && U23 % m1 as i128 == 0);
        let mut out = Counts23::default();
        for p1 in pivots1 {
            out.p1 += 1;
            for tail1 in &e.tails[p1][d1 - 2] {
                out.first += 1;
                let sig1 = child_sig(sig14, p1, tail1, e);
                let pivots2 = avail(sig1, e);
                if pivots2.is_empty() { continue; }
                out.pivotable_first += 1;
                let m2 = pivots2.len();
                assert_eq!(U23 % (m1 * m2) as i128, 0);
                let row1 = replace(&row14, &e.anchors[p1], tail1);
                assert_eq!(sig(&row1, e), sig1);
                for p2 in pivots2 {
                    out.p2 += 1;
                    for tail2 in &e.tails[p2][d2 - 2] {
                        out.second += 1;
                        let sig2 = child_sig(sig1, p2, tail2, e);
                        let pivots3 = avail(sig2, e);
                        if pivots3.is_empty() { continue; }
                        out.pivotable_second += 1;
                        let m3 = pivots3.len();
                        let product = m1 * m2 * m3;
                        assert_eq!(U23 % product as i128, 0);
                        let unit = mass * U23 / product as i128;
                        let row2 = replace(&row1, &e.anchors[p2], tail2);
                        assert_eq!(sig(&row2, e), sig2);
                        for p3 in pivots3 {
                            out.p3 += 1;
                            let prof = profile(&row2, p3, e);
                            for tail3 in &e.tails[p3][d3 - 2] {
                                let sig23 = child_sig(sig2, p3, tail3, e);
                                assert!(avail(sig23, e).is_empty());
                                let row23 = replace(&row2, &e.anchors[p3], tail3);
                                assert_eq!(sig(&row23, e), sig23);
                                let literal = ckey(&row23, e);
                                assert!(abstract_ckey23(&prof, p3, tail3, e) == literal);
                                out.terminal += 1;
                                out.charge += unit * *e.dual.get(&literal).unwrap_or(&0) as i128;
                            }
                        }
                    }
                }
            }
        }
        assert_eq!(out.first, [12, 32, 60][d1 - 2] * out.p1);
        assert_eq!(out.second, [12, 32, 60][d2 - 2] * out.p2);
        assert_eq!(out.terminal, [12, 32, 60][d3 - 2] * out.p3);
        out
    }

    fn field23<T: std::str::FromStr>(cols: &[&str], index: usize) -> T
    where T::Err: std::fmt::Debug {
        cols[index].parse().unwrap()
    }

    fn witness23(cols: &[&str], row14: &Row, degrees: (usize, usize, usize), e: &E) -> u64 {
        let (d1, d2, d3) = degrees;
        let sig14 = sig(row14, e);
        let pivots1 = valid(sig14, e);
        let (p1, t1, p2, t2, p3) = (
            field23::<usize>(cols, 15), field23::<usize>(cols, 16),
            field23::<usize>(cols, 17), field23::<usize>(cols, 18),
            field23::<usize>(cols, 19),
        );
        assert!(pivots1.contains(&p1));
        assert_eq!(field23::<usize>(cols, 20), pivots1.len());
        let tail1 = &e.tails[p1][d1 - 2][t1];
        let sig1 = child_sig(sig14, p1, tail1, e);
        let row1 = replace(row14, &e.anchors[p1], tail1);
        assert_eq!(hex23(&row1), cols[25]);
        let pivots2 = avail(sig1, e);
        assert!(pivots2.contains(&p2));
        assert_eq!(field23::<usize>(cols, 21), pivots2.len());
        let tail2 = &e.tails[p2][d2 - 2][t2];
        let sig2 = child_sig(sig1, p2, tail2, e);
        let row2 = replace(&row1, &e.anchors[p2], tail2);
        assert_eq!(hex23(&row2), cols[26]);
        let pivots3 = avail(sig2, e);
        assert!(pivots3.contains(&p3));
        assert_eq!(field23::<usize>(cols, 22), pivots3.len());
        assert_eq!(field23::<usize>(cols, 23), d3);
        assert_eq!(U23 % (pivots1.len() * pivots2.len() * pivots3.len()) as i128, 0);
        let prof = profile(&row2, p3, e);
        let mut q = 0i64;
        let mut terminal = 0u64;
        for tail in &e.tails[p3][d3 - 2] {
            let sig23 = child_sig(sig2, p3, tail, e);
            assert!(avail(sig23, e).is_empty());
            let row23 = replace(&row2, &e.anchors[p3], tail);
            assert_eq!(sig(&row23, e), sig23);
            let literal = ckey(&row23, e);
            assert!(abstract_ckey23(&prof, p3, tail, e) == literal);
            q += *e.dual.get(&literal).unwrap_or(&0);
            terminal += 1;
        }
        assert_eq!(q, field23::<i64>(cols, 24));
        assert_eq!(field23::<u8>(cols, 27), (q != 0) as u8);
        terminal
    }

    pub fn referee_main23() {
        let args: Vec<String> = std::env::args().collect();
        let mut samples = None;
        let mut output = None;
        let mut expected_count = None;
        let mut require_complete_bins = false;
        let mut i = 1;
        while i < args.len() {
            match args[i].as_str() {
                "--samples" => { samples = Some(args[i + 1].clone()); i += 2; }
                "--output" => { output = Some(args[i + 1].clone()); i += 2; }
                "--expected-count" => { expected_count = Some(args[i + 1].parse::<usize>().unwrap()); i += 2; }
                "--require-complete-bins" => { require_complete_bins = args[i + 1].parse::<u8>().unwrap() == 1; i += 2; }
                _ => panic!("usage: referee --samples PATH --output PATH --expected-count N --require-complete-bins 0|1"),
            }
        }
        let text = std::fs::read_to_string(samples.unwrap()).unwrap();
        let mut lines = text.lines();
        assert_eq!(lines.next().unwrap(), "lineage_id\tsample_bin\thead_index\tr8_index\trow14\tsource_mass\tp1_uses\tfirst_children\tpivotable_first\tp2_uses\tsecond_children\tpivotable_second\tp3_uses\tK23_children\tcharge_scaled_U\twitness_p1\twitness_t1\twitness_p2\twitness_t2\twitness_p3\tm1\tm2\tm3\tterminal_degree\twitness_terminal_q\twitness_row1\twitness_row2\tnonzero_terminal_q");
        let rows: Vec<_> = lines.collect();
        assert_eq!(rows.len(), expected_count.unwrap());
        let e = parse();
        assert_eq!(e.records.len(), 485);
        let degrees = [(3usize, 2usize, 4usize), (3, 3, 3), (4, 2, 3)];
        let mut counts = [0usize; 3];
        let mut bins = [std::collections::BTreeSet::new(), std::collections::BTreeSet::new(), std::collections::BTreeSet::new()];
        let mut literal_terminal = 0u64;
        let mut witness_terminal = 0u64;
        for line in rows {
            let cols: Vec<_> = line.split('\t').collect();
            assert_eq!(cols.len(), 28);
            let path = IDS23.iter().position(|id| *id == cols[0]).unwrap();
            counts[path] += 1;
            let bin = field23::<usize>(&cols, 1);
            assert!(bin < 257 && bins[path].insert(bin));
            let head = field23::<usize>(&cols, 2);
            let r8 = field23::<usize>(&cols, 3);
            assert_eq!(head / 1728, r8);
            assert_eq!(bin, head * 257 / (485 * 1728));
            let local = head % 1728;
            let (a, b, c) = (local / 144, (local / 12) % 12, local % 12);
            let record = &e.records[r8];
            let row14 = make(record, &e.factor[0][0][a], &e.factor[1][0][b], &e.factor[2][0][c]);
            let mass = record.size as i128 * record.coefficient as i128;
            assert_eq!(hex23(&row14), cols[4]);
            assert_eq!(mass, field23::<i128>(&cols, 5));
            let got = literal_path23(row14, mass, degrees[path], &e);
            assert_eq!((got.p1, got.first, got.pivotable_first, got.p2, got.second, got.pivotable_second, got.p3, got.terminal, got.charge),
                (field23(&cols, 6), field23(&cols, 7), field23(&cols, 8), field23(&cols, 9), field23(&cols, 10), field23(&cols, 11), field23(&cols, 12), field23(&cols, 13), field23(&cols, 14)));
            literal_terminal += got.terminal;
            witness_terminal += witness23(&cols, &row14, degrees[path], &e);
        }
        if require_complete_bins {
            assert_eq!(counts, [257, 257, 257]);
            for set in &bins { assert_eq!(set.iter().copied().collect::<Vec<_>>(), (0..257).collect::<Vec<_>>()); }
        }
        let result = format!(concat!(
            "{{\n  \"status\":\"PASS_INDEPENDENT_K23_D14_SOURCE_THREE_LITERAL_REFEREE\",\n",
            "  \"samples\":{},\n  \"samples_per_sink\":[{},{},{}],\n",
            "  \"complete_257_bins_per_sink\":{},\n",
            "  \"literal_terminal_children_checked\":{},\n  \"witness_terminal_children_checked\":{},\n",
            "  \"source_heads_reconstructed_from_frozen_R8\":true,\n",
            "  \"all_literal_path_counts_and_charges_equal\":true,\n",
            "  \"all_U_divisions_exact\":true,\n  \"sign_rule\":\"-M with three recurrence flips gives +M/(m1*m2*m3)\",\n",
            "  \"all_terminal_K23_children_nonpivotable\":true,\n",
            "  \"all_abstract_literal_cycle_keys_equal\":true,\n",
            "  \"scope\":\"independent literal replay of supplied K23 D14 source-three witness ledger; no aggregate scalar rerun or other lineage claim\"\n}}\n"
        ), counts.iter().sum::<usize>(), counts[0], counts[1], counts[2], require_complete_bins,
            literal_terminal, witness_terminal);
        let output = output.unwrap();
        let temporary = format!("{}.tmp", output);
        std::fs::write(&temporary, &result).unwrap();
        std::fs::rename(temporary, &output).unwrap();
        print!("{}", result);
    }
}

fn main() { inherited::referee_main23(); }
