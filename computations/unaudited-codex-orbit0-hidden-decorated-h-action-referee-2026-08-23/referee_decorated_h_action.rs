//! Exact H-action/orbit-mass referee for hidden K16 decorated parents.
#![allow(dead_code, unused_imports)]
include!("../unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs");

const CYCLE_K2: &str = "computations/unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/k18_k2_canonical_prefix.bin";
const PARENT_FILE: &str = "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/parents_000_016.bin";
const OUT_H: &str = "computations/unaudited-codex-orbit0-hidden-decorated-h-action-referee-2026-08-23/results_decorated_h_action.json";
const GENERIC_LEDGER: &str = "computations/unaudited-codex-orbit0-hidden-k16-orbit-profile-prefix-2026-08-23/decorated_pair_orbits_prefix.bin";

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Decorated { row: Row, pivot: u8 }
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
struct DAgg { weight: i128, uses: u64 }

fn moved_row(row: Row, action: usize, e: &Engine) -> Row {
    let t = &e.transforms[action];
    let mut x = row.0.map(|c| t[c as usize]);
    x.sort_unstable();
    Row(x)
}

fn moved_tail(tail: &[u8;4], action: usize, e: &Engine) -> [u8;4] {
    let tr = &e.transforms[action];
    let mut x = tail.map(|c| tr[c as usize]);
    x.sort_unstable();
    x
}

fn pivot_action(e: &Engine) -> Vec<Vec<usize>> {
    let by_vector: HashMap<[u8;12],usize> = e.pivots.iter().copied()
        .enumerate().map(|(i,x)|(x,i)).collect();
    assert_eq!(by_vector.len(), 78);
    e.permutations.iter().map(|g| e.pivots.iter().map(|&p|
        *by_vector.get(&sig_move(p,g)).unwrap()).collect()).collect()
}

fn canonical_decorated(d: Decorated, pa: &[Vec<usize>], e: &Engine) -> Decorated {
    // Frozen convention: signature first, then literal row, then pivot.
    let s=signature(&d.row.0,e);
    let best=e.permutations.iter().map(|p|sig_move(s,p)).min().unwrap();
    (0..e.transforms.len()).filter(|&g|sig_move(s,&e.permutations[g])==best)
        .map(|g| Decorated { row:moved_row(d.row,g,e), pivot:pa[g][d.pivot as usize]as u8 })
        .min().unwrap()
}

fn add_d(map: &mut HashMap<Decorated,DAgg>, key: Decorated, value: i128) {
    let x=map.entry(key).or_default(); x.weight+=value; x.uses+=1;
    if x.weight==0 { map.remove(&key); }
}

fn load_cycle_checkpoint() -> HashMap<Row,(i128,bool)> {
    let b=read(CYCLE_K2).unwrap();
    assert_eq!(&b[..8],b"H18K2P1\0");
    assert_eq!(i128::from_le_bytes(b[8..24].try_into().unwrap()),U);
    assert_eq!(u64::from_le_bytes(b[32..40].try_into().unwrap()),PARENTS);
    assert_eq!(u64::from_le_bytes(b[40..48].try_into().unwrap()),12_655_104);
    let n=u64::from_le_bytes(b[48..56].try_into().unwrap()) as usize;
    assert_eq!((n,u16::from_le_bytes(b[56..58].try_into().unwrap())),(694_172,76));
    assert_eq!(b.len(),64+76*n);
    let mut out=HashMap::with_capacity(n);
    let mut prior=None;
    for i in 0..n {
        let r=&b[64+76*i..64+76*(i+1)];
        let mut row=[0;24]; row.copy_from_slice(&r[..24]); let row=Row(row);
        let w=i128::from_le_bytes(r[24..40].try_into().unwrap());
        assert!(prior.map_or(true,|x|x<row)); prior=Some(row);
        assert!(w!=0 && r[40]<=1);
        assert!(out.insert(row,(w,r[40]!=0)).is_none());
    }
    out
}

#[cfg(feature="decorated_h_referee")]
fn main() {
    std::fs::create_dir_all(std::path::Path::new(OUT_H).parent().unwrap()).unwrap();
    let begun=Instant::now(); let e=parse(); let pa=pivot_action(&e);
    assert_eq!(e.transforms.len(),384);

    // Exhaustive local equivariance: H permutes pivots and each 12-tail fibre.
    let mut tail_checks=0u64;
    for g in 0..384 { assert_eq!(pa[g].iter().copied().collect::<HashSet<_>>().len(),78);
        for p in 0..78 { let q=pa[g][p];
            let moved_anchor=moved_tail(&e.anchors[p],g,&e);
            assert_eq!(moved_anchor,e.anchors[q]);
            let moved:HashSet<_>=e.all_k2[p].iter().map(|t|moved_tail(t,g,&e)).collect();
            let target:HashSet<_>=e.all_k2[q].iter().copied().collect();
            assert_eq!(moved,target); tail_checks+=12;
        }
    }

    // Quotient the exact Cycle prefix at the decorated-parent level.
    let mut f=BufReader::new(File::open(PARENT_FILE).unwrap()); let mut h=[0;40];
    f.read_exact(&mut h).unwrap(); assert_eq!(&h[..8],b"H16RUN2\0");
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()),U);
    let mut decorated=HashMap::new(); let mut occurrences=0u64; let mut raw_sum=0i128;
    for _ in 0..PARENTS { let mut r=[0;64]; f.read_exact(&mut r).unwrap();
        let mut rr=[0;24]; rr.copy_from_slice(&r[..24]); let row=Row(rr);
        let w1=i128::from_le_bytes(r[24..40].try_into().unwrap());
        let mut s=[0;12]; s.copy_from_slice(&r[40..52]); assert_eq!(signature(&row.0,&e),s);
        let ps=available(s,&e); let m2=r[60] as usize; assert_eq!(ps.len(),m2);
        assert_eq!(w1%(m2 as i128),0); let w2=-w1/(m2 as i128);
        for p in ps { occurrences+=1; raw_sum+=w2;
            let d=canonical_decorated(Decorated{row,pivot:p as u8},&pa,&e);
            add_d(&mut decorated,d,w2);
        }
    }
    assert_eq!(occurrences,1_054_592);
    let decorated_sum:i128=decorated.values().map(|x|x.weight).sum(); assert_eq!(decorated_sum,raw_sum);

    // Byte-level comparison to Generic's independently produced decorated
    // ledger (same frozen representative convention).
    let gb=read(GENERIC_LEDGER).unwrap(); assert_eq!(&gb[..8],b"H16PORB1");
    assert_eq!(i128::from_le_bytes(gb[8..24].try_into().unwrap()),U);
    let gn=u64::from_le_bytes(gb[32..40].try_into().unwrap())as usize;
    assert_eq!((gn,u16::from_le_bytes(gb[40..42].try_into().unwrap())),(decorated.len(),53));
    assert_eq!(gb.len(),48+53*gn); let mut generic=HashMap::with_capacity(gn);
    for rec in gb[48..].chunks_exact(53) { let mut row=[0;24];row.copy_from_slice(&rec[..24]);
        let d=Decorated{row:Row(row),pivot:rec[24]}; let a=DAgg{
            weight:i128::from_le_bytes(rec[25..41].try_into().unwrap()),
            uses:u64::from_le_bytes(rec[41..49].try_into().unwrap())};
        assert_eq!((u16::from_le_bytes(rec[49..51].try_into().unwrap()),u16::from_le_bytes(rec[51..53].try_into().unwrap())),(384,1));
        assert!(generic.insert(d,a).is_none());
    }
    assert_eq!(decorated,generic);

    // Emission after decorated canonicalization must equal emission first and
    // child-row canonicalization later (Cycle's frozen checkpoint).
    let mut child=HashMap::new(); let mut cache=HashMap::new();
    for (d,a) in &decorated { for t in &e.all_k2[d.pivot as usize] {
        let raw=replace_anchor(&d.row,&e.anchors[d.pivot as usize],t);
        let q=canonical(raw,&e,&mut cache); add(&mut child,q,a.weight);
    }}
    let frozen=load_cycle_checkpoint(); assert_eq!(child.len(),frozen.len());
    for (row,w) in &child { let &(fw,piv)=frozen.get(row).unwrap();
        assert_eq!(*w,fw); assert_eq!(pivotable(row,&e),piv);
    }

    // Stabilizer/orbit-mass theorem checked on deterministic 257 decorated
    // representatives.  Representative-tail emission with mass M equals the
    // sum over stabilizer tail orbits M*|orbit| into each child H-orbit.
    let mut dk:Vec<_>=decorated.iter().collect(); dk.sort_unstable_by_key(|x|x.0);
    let sample:Vec<usize>=(0..257).map(|i|i*(dk.len()-1)/256).collect();
    let mut stab_hist:HashMap<usize,u64>=HashMap::new();
    for i in sample { let (&d,a)=dk[i]; let mass=a.weight;
        let images:HashSet<_>=(0..384).map(|g|Decorated{row:moved_row(d.row,g,&e),pivot:pa[g][d.pivot as usize]as u8}).collect();
        let stabilizer:Vec<_>=(0..384).filter(|&g|moved_row(d.row,g,&e)==d.row&&pa[g][d.pivot as usize]==d.pivot as usize).collect();
        assert_eq!(images.len()*stabilizer.len(),384); *stab_hist.entry(stabilizer.len()).or_default()+=1;
        let tails=&e.all_k2[d.pivot as usize]; let mut unseen:HashSet<[u8;4]>=tails.iter().copied().collect();
        let mut by_orbit:HashMap<Row,i128>=HashMap::new();
        while let Some(&t)=unseen.iter().next() { let orbit:HashSet<_>=stabilizer.iter().map(|&g|moved_tail(&t,g,&e)).collect();
            assert!(orbit.iter().all(|x|tails.contains(x))); for x in &orbit {unseen.remove(x);}
            let raw=replace_anchor(&d.row,&e.anchors[d.pivot as usize],&t);
            let q=canonical(raw,&e,&mut cache); add(&mut by_orbit,q,mass*(orbit.len()as i128));
        }
        let mut direct=HashMap::new(); for t in tails { let raw=replace_anchor(&d.row,&e.anchors[d.pivot as usize],t);
            let q=canonical(raw,&e,&mut cache); add(&mut direct,q,mass); }
        assert_eq!(direct,by_orbit);
    }
    let mut sh:Vec<_>=stab_hist.into_iter().collect(); sh.sort_unstable();
    let shj=sh.iter().map(|(k,v)|format!("\"{}\":{}",k,v)).collect::<Vec<_>>().join(",");
    let text=format!("{{\n  \"status\":\"PASS_EXACT_DECORATED_H_ACTION_PREFIX\",\n  \"H_order\":384,\n  \"pivot_tail_equivariance_checks\":{},\n  \"decorated_occurrences\":{},\n  \"decorated_nonzero_orbits\":{},\n  \"decorated_signed_mass_scaled\":\"{}\",\n  \"K2_emitted_raw_terms_after_quotient\":{},\n  \"Cycle_checkpoint_support\":{},\n  \"Cycle_checkpoint_exact_match\":true,\n  \"Generic_decorated_ledger_exact_match\":true,\n  \"stabilizer_sample_size\":257,\n  \"stabilizer_sample_histogram\":{{{}}},\n  \"formula\":\"For decorated orbit D with mass M and stabilizer S, each S-tail orbit O contributes M*|O| to its canonical child H-orbit; equivalently emit all 12 representative tails with mass M.\",\n  \"scope\":\"Exact one-H-slice prefix comparison against Generic's decorated ledger and Cycle's emitted K2 checkpoint; no global K2 collection.\",\n  \"elapsed_seconds\":{:.6}\n}}\n",tail_checks,occurrences,decorated.len(),decorated_sum,12*decorated.len(),child.len(),shj,begun.elapsed().as_secs_f64());
    std::fs::write(OUT_H,&text).unwrap(); print!("{}",text);
}
