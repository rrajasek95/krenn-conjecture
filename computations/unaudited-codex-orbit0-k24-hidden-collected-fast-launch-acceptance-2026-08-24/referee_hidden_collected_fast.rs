//! Independent source-backed replay of all 257 fast hidden-collected witnesses.
mod replay {
    include!("../unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/k24_hidden_base.rs");
    use std::io::BufRead;

    const INPUT: &str = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/checkpoint_k18_22_pivotable.bin";
    const TOTAL: u64 = 158_439_965;

    fn need(ok: bool, why: &str) { if !ok { panic!("{}", why) } }
    fn num(s: &str) -> i128 { s.parse().expect("integer") }
    fn row(s: &str) -> Row {
        need(s.len() == 48, "row hex length");
        let mut b = [0u8; 24];
        for i in 0..24 { b[i] = u8::from_str_radix(&s[2*i..2*i+2], 16).expect("row hex") }
        Row(b)
    }
    fn terminal_charge(r: &Row, s: [u8;12], p: usize, e: &Engine, c: &CEnv) -> i64 {
        let mut q = 0;
        for tail in &c.k4[p] {
            let child = replace_anchor(r, &e.anchors[p], tail);
            let z = child_sig(s, p, tail, e);
            need(signature(&child.0, e) == z, "literal child signature");
            need(z.iter().map(|&x| x as usize).sum::<usize>() == 0, "terminal mass");
            need(!pivotable_sig(z, e), "K24 child pivotable");
            q += *c.dual.get(&literal_ckey(&child, c)).unwrap_or(&0);
        }
        q
    }

    pub fn run() {
        let args: Vec<_> = std::env::args().collect();
        need(args.len() == 7 && args[1] == "--samples" && args[3] == "--sample-span" && args[5] == "--output", "usage: referee --samples LEDGER --sample-span RECORDS --output JSON");
        let sample_span: u64 = args[4].parse().expect("sample span");
        need(sample_span > 0 && sample_span <= TOTAL, "sample span range");
        let e = parse(); let c = cenv();
        let mut input = File::open(INPUT).unwrap();
        let mut header = [0u8;80]; input.read_exact(&mut header).unwrap();
        need(&header[..8] == b"H18PIV2\0", "input magic");
        need(i128::from_le_bytes(header[8..24].try_into().unwrap()) == U, "input U");
        need(u64::from_le_bytes(header[48..56].try_into().unwrap()) == TOTAL, "input count");
        need(u64::from_le_bytes(header[56..64].try_into().unwrap()) == 1, "input flag");
        let mut lines = BufReader::new(File::open(&args[2]).unwrap()).lines();
        need(lines.next().unwrap().unwrap() == "input_index\tK18_row\tretained_K16_pair_witness\tweight_before_p3_scaled_U\tp2\tt2\tpair_uses\torbit\tstabilizer\tm2\tm3\tselected_p3_uses\tpivotable_K20_children\tselected_p4_uses\tterminal_K4_children\tliteral_charge_scaled_U", "ledger header");
        let mut count = 0u64;
        for line in lines {
            let line = line.unwrap(); need(!line.is_empty(), "blank row");
            let f: Vec<_> = line.split('\t').collect(); need(f.len() == 16, "row arity");
            let index: u64 = f[0].parse().unwrap();
            need(index == count * (sample_span-1) / 256, "distributed source index");
            input.seek(SeekFrom::Start(80 + 80*index)).unwrap();
            let mut rec = [0u8;80]; input.read_exact(&mut rec).unwrap();
            let source = row(f[1]); let witness = row(f[2]);
            need(source.0 == rec[..24], "source row seek mismatch");
            need(witness.0 == rec[40..64], "retained witness seek mismatch");
            let weight = i128::from_le_bytes(rec[24..40].try_into().unwrap());
            need(weight == num(f[3]) && weight != 0, "weight mismatch/zero");
            need(rec[64].to_string() == f[4] && rec[65].to_string() == f[5], "p2/t2 mismatch");
            let uses = u64::from_le_bytes(rec[66..74].try_into().unwrap());
            let orbit = u16::from_le_bytes(rec[74..76].try_into().unwrap());
            let stabilizer = u16::from_le_bytes(rec[76..78].try_into().unwrap());
            need(uses.to_string() == f[6] && uses > 0, "pair uses mismatch");
            need(orbit.to_string() == f[7] && stabilizer.to_string() == f[8] && orbit as u32 * stabilizer as u32 == 384, "orbit identity");
            need(rec[78] == 1 && rec[79].to_string() == f[9], "pivotable/m2 mismatch");
            let m2 = rec[79] as usize; need(m2 > 0, "zero m2");
            let s18 = signature(&source.0, &e); need(s18.iter().map(|&x|x as usize).sum::<usize>() == 6, "K18 mass");
            let ps3 = available(s18, &e); let m3 = ps3.len();
            need(m3 > 0 && m3.to_string() == f[10] && m3.to_string() == f[11], "m3/p3 count");
            need(weight % m3 as i128 == 0 && U % (m2*m3) as i128 == 0, "division/U");
            let mut k20 = 0u64; let mut p4uses = 0u64; let mut terminal = 0u64; let mut charge = 0i128;
            for p3 in ps3 {
                for tail in &e.all_k2[p3] {
                    let r20 = replace_anchor(&source, &e.anchors[p3], tail);
                    let s20 = signature(&r20.0, &e); let ps4 = available(s20, &e);
                    if ps4.is_empty() { continue }
                    need(ps4.len() == 1, "K20 final pivot multiplicity"); k20 += 1;
                    for p4 in ps4 { p4uses += 1; terminal += 60; charge += weight/(m3 as i128) * terminal_charge(&r20,s20,p4,&e,&c) as i128 }
                }
            }
            need(k20.to_string() == f[12] && p4uses.to_string() == f[13], "K20/p4 counts");
            need(terminal.to_string() == f[14] && charge.to_string() == f[15], "terminal/charge replay");
            count += 1;
        }
        need(count == 257, "witness count");
        let result="{\n  \"status\":\"PASS_INDEPENDENT_HIDDEN_COLLECTED_FAST_LITERAL_REPLAY\",\n  \"witnesses_replayed\":257,\n  \"source_backed\":true,\n  \"terminal_K4_exhaustive\":true,\n  \"scalar_full_rerun\":false\n}\n";
        std::fs::write(&args[6],result).unwrap(); print!("{}",result);
    }
}
fn main(){ replay::run() }
