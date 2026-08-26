//! Source-linear grouped direct-K15 K24 charge-only fold: two sinks / six IDs.
mod fold {
#![allow(dead_code, unused_imports)]
include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
use std::collections::BTreeMap;
use std::fs::rename;

const U24: i128 = 400_591_699_200;
const SLICES: usize = 485;
const HEADS_PER_SLICE: u64 = 13_824;
const NAMES: [&str; 2] = [
    "D15:{223,232,322}|R:2-3-4",
    "D15:{223,232,322}|R:3-2-4",
];
const GIDS: [&str; 2] = ["source_D15_R2_3_4", "source_D15_R3_2_4"];
const IDS: [[&str; 3]; 2] = [
    ["D15:223|R:2-3-4", "D15:232|R:2-3-4", "D15:322|R:2-3-4"],
    ["D15:223|R:3-2-4", "D15:232|R:3-2-4", "D15:322|R:3-2-4"],
];
const PATHS: [&[usize]; 2] = [&[2,3,4], &[3,2,4]];

#[derive(Clone, Default)]
struct St {
    heads: u64, mass: i128, l1: i128,
    piv: [u64; 3], cand: [u64; 3], pivotable: [u64; 2],
    terminal: u64, charge: i128, hist: BTreeMap<u16, u64>,
    terminal_keys: u64,
    samples: BTreeMap<usize, (u64, String)>,
}
impl St {
    fn add(&mut self, x: St) {
        self.heads += x.heads; self.mass += x.mass; self.l1 += x.l1;
        for i in 0..3 { self.piv[i] += x.piv[i]; self.cand[i] += x.cand[i]; }
        for i in 0..2 { self.pivotable[i] += x.pivotable[i]; }
        self.terminal += x.terminal; self.charge += x.charge; self.terminal_keys += x.terminal_keys;
        for (k,v) in x.hist { *self.hist.entry(k).or_default() += v; }
        for (k,v) in x.samples { let z=self.samples.entry(k).or_insert_with(||v.clone()); if v.0<z.0{*z=v} }
    }
}
type Plan = Vec<(u8, [u8; 12], Vec<usize>)>;

fn packet_row(r: &R8, packet: usize, a: &[u8;4], b: &[u8;4], c: &[u8;4]) -> Row {
    match packet { 0 => make(r,c,a,b), 1 => make(r,a,c,b), 2 => make(r,a,b,c), _ => unreachable!() }
}
fn hx(r:&Row)->String{r.0.iter().map(|x|format!("{:02x}",x)).collect()}

#[allow(clippy::too_many_arguments)]
fn walk(
    row: &Row, s: [u8;12], ps: Vec<usize>, positive: i128,
    degs: &[usize], d: usize, den: &mut [usize;3], st: &mut St,
    plans: &mut HashMap<([u8;12],u8,u8),Plan>,
    terminal: &mut HashMap<RKey,(i64,i64,u64,u64)>, e: &E,
    source_head: &Row, source_head_ordinal: u64, group: usize,
    trace: &mut Vec<(usize,usize,usize,Row)>, witness: &mut Option<String>,
) {
    let m = ps.len(); assert!(m > 0); den[d] = m; st.piv[d] += m as u64;
    let degree = degs[d];
    for p in ps {
        if d + 1 == degs.len() {
            let n = e.tails[p][degree-2].len() as u64; st.cand[d] += n;
            let product = den[..=d].iter().product::<usize>();
            assert_eq!(U24 % product as i128, 0);
            let sign = if degs.len() % 2 == 0 { -positive } else { positive };
            let unit = sign * U24 / product as i128;
            let before = terminal.len();
            let z = resp(row, s, p, degree, e, terminal);
            st.terminal_keys += (terminal.len() - before) as u64;
            assert_eq!((z.2,z.3),(n,n), "nonterminal final response in K24 sink");
            assert_eq!(z.0,z.1);
            st.terminal += n; st.charge += unit * z.0 as i128;
            *st.hist.entry(product as u16).or_default() += 1;
            if witness.is_none() && z.0 != 0 {
                let mut steps=trace.iter().map(|(pp,tt,dd,rr)|format!("{}:{}:{}:{}",pp,tt,dd,hx(rr))).collect::<Vec<_>>();
                steps.push(format!("{}:-:{}:{}",p,degree,hx(row)));
                *witness=Some(format!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",GIDS[group],IDS[group].join("+"),source_head_ordinal,hx(source_head),-positive,product,unit,z.0,unit*z.0 as i128,steps.join(";")));
            }
        } else {
            let tails = e.tails[p][degree-2].len() as u64; st.cand[d] += tails;
            let key = (s,p as u8,degree as u8);
            let plan = plans.entry(key).or_insert_with(|| {
                let mut v = Vec::new();
                for (ti,t) in e.tails[p][degree-2].iter().enumerate() {
                    let sc = child_sig(s,p,t,e); let q = avail(sc,e);
                    if !q.is_empty() { v.push((ti as u8,sc,q)); }
                }
                v
            }).clone();
            st.pivotable[d] += plan.len() as u64;
            for (ti,sc,q) in plan {
                let child = replace(row,&e.anchors[p],&e.tails[p][degree-2][ti as usize]);
                assert_eq!(sig(&child,e),sc);
                trace.push((p,ti as usize,degree,child));
                walk(&child,sc,q,positive,degs,d+1,den,st,plans,terminal,e,source_head,source_head_ordinal,group,trace,witness);
                trace.pop();
            }
        }
    }
}

fn worker(e: Arc<E>, start: usize, end: usize, step: usize) -> [St;2] {
    let mut out: [St;2] = std::array::from_fn(|_| St::default());
    let mut plans = HashMap::new();
    for ri in (start..end).step_by(step) {
        let r = &e.records[ri]; let positive = r.coefficient as i128 * r.size as i128;
        let mut terminal = HashMap::new();
        let mut cursor=0u64; let mut witnesses:[Option<String>;2]=[None,None];
        for packet in 0..3 {
            let other: Vec<_> = (0..3).filter(|&x| x != packet).collect();
            for a in &e.factor[other[0]][0] { for b in &e.factor[other[1]][0] { for c in &e.factor[packet][1] {
                let head = packet_row(r,packet,a,b,c); let s = sig(&head,&e);
                let source_head_ordinal=cursor; cursor+=1;
                assert_eq!(s.iter().map(|&x|x as usize).sum::<usize>(),9);
                let ps = avail(s,&e); assert!(!ps.is_empty());
                for k in 0..2 {
                    out[k].heads += 1; out[k].mass -= positive; out[k].l1 += positive.abs();
                    walk(&head,s,ps.clone(),positive,PATHS[k],0,&mut [0;3],&mut out[k],&mut plans,&mut terminal,&e,&head,source_head_ordinal,k,&mut Vec::new(),&mut witnesses[k]);
                }
            }}}
        }
        assert_eq!(cursor,HEADS_PER_SLICE);
        let bin=((ri as u64*257/SLICES as u64).min(256))as usize;
        for k in 0..2 { if let Some(w)=witnesses[k].take(){let line=format!("{}\t{}\t{}",bin,ri,w);let z=out[k].samples.entry(bin).or_insert((ri as u64,line.clone()));if (ri as u64)<z.0{*z=(ri as u64,line)}} }
    }
    out
}

fn hist(h: &BTreeMap<u16,u64>) -> String {
    h.iter().map(|(k,v)|format!("\"{}\":{}",k,v)).collect::<Vec<_>>().join(",")
}
fn sink_json(k: usize, s: &St) -> String {
    let ids = IDS[k].iter().map(|x|format!("\"{}\"",x)).collect::<Vec<_>>().join(",");
    format!(concat!(
        "\"{}\":{{\"ids\":[{}],\"individual_id_charges\":null,\"degrees\":[{}],",
        "\"source_heads\":{},\"source_mass\":\"{}\",\"source_l1\":\"{}\",",
        "\"stage_pivot_uses\":[{},{},{}],\"stage_tail_candidates\":[{},{},{}],",
        "\"stage_pivotable_children\":[{},{}],\"terminal_response_keys_evaluated\":{},",
        "\"terminal_K24_occurrences\":{},\"full_occurrences\":{},\"irreducible_occurrences\":{},",
        "\"full_charge_scaled_U\":\"{}\",\"irreducible_charge_scaled_U\":\"{}\",",
        "\"denominator_product_hist\":{{{}}},\"literal_witnesses\":{}}}"
    ), NAMES[k], ids, PATHS[k].iter().map(|x|x.to_string()).collect::<Vec<_>>().join(","),
        s.heads,s.mass,s.l1,s.piv[0],s.piv[1],s.piv[2],s.cand[0],s.cand[1],s.cand[2],
        s.pivotable[0],s.pivotable[1],s.terminal_keys,s.terminal,s.terminal,s.terminal,s.charge,s.charge,hist(&s.hist),s.samples.len())
}

pub fn run() {
    let args: Vec<_> = std::env::args().collect();
    let (mut begin,mut count,mut workers)=(0usize,SLICES,8usize);
    let mut output="computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_direct_k15_prefix1.json".to_string();
    let mut i=1; while i<args.len() { match args[i].as_str() {
        "--start-slice" => { begin=args[i+1].parse().unwrap(); i+=2; },
        "--count-slices" => { count=args[i+1].parse().unwrap(); i+=2; },
        "--workers" => { workers=args[i+1].parse().unwrap(); i+=2; },
        "--output" => { output=args[i+1].clone(); i+=2; }, _=>panic!("bad arg")
    }}
    assert!(begin<=SLICES && count>0 && count<=SLICES-begin && (1..=8).contains(&workers));
    let begun=Instant::now(); let e=Arc::new(parse()); let mut jobs=Vec::new();
    for w in 0..workers { let x=e.clone(); jobs.push(thread::spawn(move||worker(x,begin+w,begin+count,workers))); }
    let mut all:[St;2]=std::array::from_fn(|_|St::default());
    for j in jobs { let z=j.join().unwrap(); for k in 0..2 { all[k].add(z[k].clone()); }}
    for s in &all {
        assert_eq!(s.heads,count as u64*HEADS_PER_SLICE);
        assert_eq!((s.mass,s.l1),(all[0].mass,all[0].l1));
        assert_eq!(s.terminal,s.cand[if s.piv[2]>0 {2} else {1}]);
        assert!(s.hist.keys().all(|&x|U24 % x as i128 == 0));
    }
    if begin==0 && count==SLICES {
        for s in &all { assert_eq!((s.heads,s.mass,s.l1),(6_704_640,322_486_272,3_085_516_800)); assert_eq!(s.samples.len(),257); }
    }
    let elapsed=begun.elapsed().as_secs_f64(); assert!(elapsed<600.0,"600-second interval publication gate exceeded");
    let projected=elapsed*SLICES as f64/count as f64;
    let status=if begin==0&&count==SLICES{"PASS_COMPLETE_GROUPED_DIRECT_K15_TWO_SINK_K24_CHARGE"}else{"PASS_BOUNDED_GROUPED_DIRECT_K15_TWO_SINK_K24_GATE"};
    let sample_path=format!("{}.samples.tsv",output);
    let mut lines=vec!["sample_bin\tsource_index\tgroup_id\tlineage_scope\tsource_head_ordinal\tsource_head_row\tsource_coefficient\tdenominator_product\tunit_scaled_U\tterminal_K4_charge\tcontribution_scaled_U\tliteral_steps".to_string()];
    for s in &all { lines.extend(s.samples.values().map(|x|x.1.clone())); }
    let sample_tmp=format!("{}.tmp",sample_path);std::fs::write(&sample_tmp,format!("{}\n",lines.join("\n"))).unwrap();rename(sample_tmp,&sample_path).unwrap();
    let text=format!(concat!(
        "{{\n  \"status\":\"{}\",\n  \"scale_U\":\"{}\",\n  \"slice_interval\":[{},{}],",
        "\n  \"source_slices\":{},\n  \"source_heads_per_slice\":{},\n  \"workers\":{},",
        "\n  \"degree\":24,\n  \"covered_ids\":6,\n  \"scalar_groups\":2,\n  \"sample_schema\":\"k24_physical_literal_v2_source_head\",\n  \"sample_ledger\":\"{}\",\n  \"sinks\":{{{},{}}},",
        "\n  \"packet_grouping_guard\":\"packet witnesses 322/232/223 retained only as grouped source classes; no individual scalar split\",",
        "\n  \"sign_rule\":\"direct K15 head is -positive; every selected pivot flips sign and divides by its occurrencewise multiplicity; U is exactly divisible by every recorded denominator product\",",
        "\n  \"terminality\":\"every realized final K4 response key is exhaustively expanded; all K24 outputs have anchor-signature mass zero, so full equals irreducible\",",
        "\n  \"scope\":\"two separate grouped scalar K24 sinks covering exactly 6 IDs; charge only, no rows, columns, membership, span, or conjecture verdict\",",
        "\n  \"elapsed_seconds\":{:.6},\n  \"projected_full_seconds\":{:.6}\n}}\n"
    ),status,U24,begin,begin+count,count,HEADS_PER_SLICE,workers,sample_path,
        sink_json(0,&all[0]),sink_json(1,&all[1]),elapsed,projected);
    let tmp=format!("{}.tmp",output);std::fs::write(&tmp,&text).unwrap();rename(tmp,&output).unwrap();print!("{}",text);
}
}
fn main(){fold::run()}
