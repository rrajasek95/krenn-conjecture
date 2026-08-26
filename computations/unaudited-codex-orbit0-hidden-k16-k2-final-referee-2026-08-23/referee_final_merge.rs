use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap};
use std::convert::TryInto;
use std::fs::{metadata, read, File};
use std::io::{BufReader, Read, Seek, SeekFrom, Write};
use std::time::Instant;

const DIR: &str = "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/";
const STRUCTURE: &str = "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin";
const AUX: &str = "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin";
const OUT: &str = "computations/unaudited-codex-orbit0-hidden-k16-k2-final-referee-2026-08-23/results_final_merge_referee.json";
const U: i128 = 400_591_699_200;
const H: usize = 80;
const R: usize = 80;
const PAIR_R: usize = 53;

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row([u8; 24]);

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Witness {
    pair_row: Row,
    pivot: u8,
    tail: u8,
    uses: u64,
    orbit: u16,
    stabilizer: u16,
    m2: u8,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Rec { row: Row, weight: i128, witness: Witness, pivotable: bool }

#[derive(Clone, Copy)]
struct Header { start: u64, end: u64, count: u64, raw: u64, sum: i128 }

struct Reader {
    r: BufReader<File>,
    cur: Option<Rec>,
    prior: Option<Row>,
    read: u64,
    declared: u64,
}

struct Engine {
    anchor_pos: [i8; 252],
    transforms: Vec<[u8; 252]>,
    permutations: Vec<[u8; 12]>,
    pivots: Vec<[u8; 12]>,
    anchors: Vec<[u8; 4]>,
    all_k2: Vec<Vec<[u8; 4]>>,
}

fn u16le(x: &[u8]) -> u16 { u16::from_le_bytes(x.try_into().unwrap()) }
fn u32le(x: &[u8]) -> u32 { u32::from_le_bytes(x.try_into().unwrap()) }
fn u64le(x: &[u8]) -> u64 { u64::from_le_bytes(x.try_into().unwrap()) }
fn i128le(x: &[u8]) -> i128 { i128::from_le_bytes(x.try_into().unwrap()) }

fn parse_engine() -> Engine {
    let b = read(STRUCTURE).unwrap();
    assert_eq!(&b[..11], b"K16DIRECT1\0");
    let mut p = 11;
    let nt = u32le(&b[p..p + 4]) as usize; p += 4;
    let nr = u32le(&b[p..p + 4]) as usize; p += 4;
    let np = u32le(&b[p..p + 4]) as usize; p += 4;
    let na = u32le(&b[p..p + 4]) as usize; p += 4;
    assert_eq!((nt, nr, np, na), (384, 485, 78, 12));
    let mut anchor_pos = [-1i8; 252];
    for i in 0..12 { anchor_pos[b[p + i] as usize] = i as i8; }
    p += 12;
    let mut transforms = Vec::with_capacity(nt);
    let mut permutations = Vec::with_capacity(nt);
    for _ in 0..nt {
        let mut t = [0u8; 252]; t.copy_from_slice(&b[p..p + 252]); p += 252;
        let mut q = [0u8; 12]; q.copy_from_slice(&b[p..p + 12]); p += 12;
        transforms.push(t); permutations.push(q);
    }
    p += nr * (12 + 4 + 8);
    let mut pivots = Vec::with_capacity(np);
    for _ in 0..np { let mut q=[0u8;12]; q.copy_from_slice(&b[p..p+12]); p+=12; pivots.push(q); }

    let a = read(AUX).unwrap();
    assert_eq!(&a[..8], b"K17AUX1\0");
    let mut q = 8;
    assert_eq!(u64le(&a[q..q+8]), 281_801_520); q += 8;
    let nc=u32le(&a[q..q+4]) as usize; q+=4;
    let npa=u32le(&a[q..q+4]) as usize; q+=4;
    assert_eq!((nc,npa),(25,78)); q += nc*12;
    let mut anchors=Vec::with_capacity(npa); let mut all_k2=Vec::with_capacity(npa);
    for _ in 0..npa {
        let mut x=[0u8;4]; x.copy_from_slice(&a[q..q+4]); q+=4; anchors.push(x);
        let mut tails=Vec::with_capacity(12);
        for _ in 0..12 { let mut y=[0u8;4];y.copy_from_slice(&a[q..q+4]);q+=4;tails.push(y); }
        all_k2.push(tails); q += 32*4;
    }
    assert_eq!(q,a.len());
    Engine { anchor_pos, transforms, permutations, pivots, anchors, all_k2 }
}

fn signature(row: &Row, e: &Engine) -> [u8;12] {
    let mut s=[0u8;12];
    for &c in &row.0 { let i=e.anchor_pos[c as usize]; if i>=0 { s[i as usize]+=1; } }
    s
}

fn pivotable_sig(s: &[u8;12], e: &Engine) -> bool {
    e.pivots.iter().any(|p|(0..12).all(|i|s[i]>=p[i]))
}

fn sig_move(s: &[u8;12], p: &[u8;12]) -> [u8;12] {
    let mut x=[0u8;12]; for old in 0..12 { x[p[old] as usize]=s[old]; } x
}

fn canonical(row: Row, e: &Engine) -> Row {
    let s=signature(&row,e);
    let best_sig=e.permutations.iter().map(|p|sig_move(&s,p)).min().unwrap();
    let mut best=None;
    for (t,p) in e.transforms.iter().zip(&e.permutations) {
        if sig_move(&s,p)!=best_sig { continue; }
        let mut x=row.0.map(|c|t[c as usize]); x.sort_unstable(); let y=Row(x);
        if best.map_or(true,|z|y<z) { best=Some(y); }
    }
    best.unwrap()
}

fn replace_anchor(row: &Row, anchor: &[u8;4], tail: &[u8;4]) -> Row {
    let mut x=[0u8;24]; let(mut ai,mut k)=(0usize,0usize);
    for &c in &row.0 { if ai<4 && c==anchor[ai] { ai+=1; } else { x[k]=c;k+=1; } }
    assert_eq!((ai,k),(4,20)); x[20..].copy_from_slice(tail); x.sort_unstable(); Row(x)
}

fn read_header(path: &str, magic: &[u8;8], final_flag: Option<u64>) -> Header {
    let mut f=File::open(path).unwrap(); let mut h=[0u8;H]; f.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8],magic); assert_eq!(i128le(&h[8..24]),U);
    assert_eq!((u16le(&h[24..26]),u16le(&h[26..28]),u16le(&h[28..30]),&h[30..32]),(0,0,R as u16,&[0,0][..]));
    let out=Header{start:u64le(&h[32..40]),end:u64le(&h[40..48]),count:u64le(&h[48..56]),raw:u64le(&h[56..64]),sum:i128le(&h[64..80])};
    assert_eq!(metadata(path).unwrap().len(),H as u64+R as u64*out.count);
    if let Some(flag)=final_flag { assert_eq!(out.raw,flag); } else { assert_eq!(out.raw,12*(out.end-out.start)); }
    out
}

fn read_rec<Rd: Read>(r: &mut Rd) -> Option<Rec> {
    let mut b=[0u8;R];
    match r.read_exact(&mut b) { Ok(())=>{},Err(x) if x.kind()==std::io::ErrorKind::UnexpectedEof=>return None,Err(x)=>panic!("record: {x}") }
    let mut row=[0u8;24];row.copy_from_slice(&b[..24]);
    let mut prow=[0u8;24];prow.copy_from_slice(&b[40..64]);
    Some(Rec{row:Row(row),weight:i128le(&b[24..40]),witness:Witness{pair_row:Row(prow),pivot:b[64],tail:b[65],uses:u64le(&b[66..74]),orbit:u16le(&b[74..76]),stabilizer:u16le(&b[76..78]),m2:b[79]},pivotable:b[78]!=0})
}

impl Reader {
    fn open(path: &str, declared: u64) -> Self {
        let mut r=BufReader::with_capacity(1<<20,File::open(path).unwrap()); let mut h=[0u8;H];r.read_exact(&mut h).unwrap();
        let mut z=Self{r,cur:None,prior:None,read:0,declared}; z.advance(); z
    }
    fn advance(&mut self) {
        let n=read_rec(&mut self.r);
        if let Some(v)=n { if let Some(p)=self.prior { assert!(p<v.row); } self.prior=Some(v.row); self.read+=1; assert!(self.read<=self.declared); }
        self.cur=n;
    }
    fn finish(&self) { assert!(self.cur.is_none()); assert_eq!(self.read,self.declared); }
}

fn pair_at(f: &mut File, index: u64) -> ([u8;25],i128,u64,u16,u16) {
    f.seek(SeekFrom::Start(H as u64+PAIR_R as u64*index)).unwrap(); let mut b=[0u8;PAIR_R];f.read_exact(&mut b).unwrap();
    let mut k=[0u8;25];k.copy_from_slice(&b[..25]);(k,i128le(&b[25..41]),u64le(&b[41..49]),u16le(&b[49..51]),u16le(&b[51..53]))
}

fn replay_witness(rec: &Rec, pair: &mut File, pair_count: u64, e: &Engine) {
    let mut key=[0u8;25];key[..24].copy_from_slice(&rec.witness.pair_row.0);key[24]=rec.witness.pivot;
    let(mut lo,mut hi)=(0u64,pair_count);
    while lo<hi { let m=(lo+hi)/2;let(k,_,_,_,_)=pair_at(pair,m);if k<key{lo=m+1}else{hi=m} }
    assert!(lo<pair_count);let(k,_w,uses,orbit,stab)=pair_at(pair,lo);assert_eq!(k,key);
    assert_eq!((uses,orbit,stab),(rec.witness.uses,rec.witness.orbit,rec.witness.stabilizer));assert_eq!(u32::from(orbit)*u32::from(stab),384);
    let p=rec.witness.pivot as usize;let t=rec.witness.tail as usize;assert!(p<78&&t<12);
    assert_eq!(e.pivots.iter().filter(|x|(0..12).all(|i|signature(&rec.witness.pair_row,e)[i]>=x[i])).count(),rec.witness.m2 as usize);
    let raw=replace_anchor(&rec.witness.pair_row,&e.anchors[p],&e.all_k2[p][t]);assert_eq!(canonical(raw,e),rec.row);
}

fn main() {
    let begun=Instant::now();let e=parse_engine();
    let pair_path=format!("{}hidden_k16_decorated_pair_orbits_full.bin",DIR);let mut ph=[0u8;H];let mut pair=File::open(&pair_path).unwrap();pair.read_exact(&mut ph).unwrap();
    assert_eq!(&ph[..8],b"H16ORM1\0");let pair_count=u64le(&ph[48..56]);assert_eq!(pair_count,101_545_723);

    let mut readers=Vec::new();let mut heap=BinaryHeap::new();let(mut expected,mut chunk_rows,mut chunk_sum)=(0u64,0u64,0i128);
    for i in 0..291 {
        let path=format!("{}pchild_chunk_{:04}.bin",DIR,i);let h=read_header(&path,b"H18CHC1\0",None);assert_eq!(h.start,expected);expected=h.end;chunk_rows+=h.count;chunk_sum+=h.sum;
        let r=Reader::open(&path,h.count);if let Some(x)=r.cur{heap.push(Reverse((x.row,i)));}readers.push(r);
    }
    assert_eq!(expected,pair_count);assert_eq!(chunk_rows,516_225_702);assert_eq!(chunk_sum,1_754_767_313_172_666_777_600);

    let piv_path=format!("{}checkpoint_k18_22_pivotable.bin",DIR);let irr_path=format!("{}checkpoint_k18_22_irreducible.bin",DIR);
    let hp=read_header(&piv_path,b"H18PIV2\0",Some(1));let hi=read_header(&irr_path,b"H18IRR2\0",Some(0));
    assert_eq!((hp.start,hp.end,hi.start,hi.end),(pair_count,12*pair_count,pair_count,12*pair_count));
    let mut rp=Reader::open(&piv_path,hp.count);let mut ri=Reader::open(&irr_path,hi.count);
    let(mut pc,mut ic,mut zeros,mut ps,mut is,mut global,mut samples)=(0u64,0u64,0u64,0i128,0i128,0u64,0u64);
    let mut piv_cache:HashMap<[u8;12],bool>=HashMap::new();
    while let Some(Reverse((row,j)))=heap.pop() {
        assert_eq!(readers[j].cur.unwrap().row,row);let mut a=readers[j].cur.unwrap();readers[j].advance();if let Some(x)=readers[j].cur{heap.push(Reverse((x.row,j)));}
        while let Some(Reverse((r,k)))=heap.peek().copied(){if r!=row{break}heap.pop();let b=readers[k].cur.unwrap();assert_eq!(a.pivotable,b.pivotable);a.weight+=b.weight;if b.witness<a.witness{a.witness=b.witness}readers[k].advance();if let Some(x)=readers[k].cur{heap.push(Reverse((x.row,k)));}}
        let s=signature(&row,&e);let actual=*piv_cache.entry(s).or_insert_with(||pivotable_sig(&s,&e));assert_eq!(actual,a.pivotable);
        if a.weight==0{zeros+=1;continue}
        let out=if a.pivotable{rp.cur.unwrap()}else{ri.cur.unwrap()};assert_eq!(out,a);
        if global%100_000==0 { replay_witness(&out,&mut pair,pair_count,&e);samples+=1; }
        if a.pivotable{pc+=1;ps+=a.weight;rp.advance()}else{ic+=1;is+=a.weight;ri.advance()}global+=1;
        if global%25_000_000==0{eprintln!("REFEREE rows={} zero={} samples={} elapsed={:.1}",global,zeros,samples,begun.elapsed().as_secs_f64());}
    }
    for r in &readers{r.finish()}rp.finish();ri.finish();
    assert_eq!((pc,ic,zeros),(158_439_965,110_465_931,3_346));
    assert_eq!((ps,is),(724_159_651_336_720_220_160,1_030_607_661_835_946_557_440));
    assert_eq!((hp.count,hi.count,hp.sum,hi.sum),(pc,ic,ps,is));assert_eq!(ps+is,chunk_sum);
    let text=format!("{{\n  \"status\": \"PASS_INDEPENDENT_FULL_K18_MERGE_REPLAY\",\n  \"chunks\": 291,\n  \"chunk_rows\": {},\n  \"pair_orbits\": {},\n  \"pivotable_support\": {},\n  \"irreducible_support\": {},\n  \"cross_chunk_zero_rows\": {},\n  \"pivotable_mass_scaled\": \"{}\",\n  \"irreducible_mass_scaled\": \"{}\",\n  \"total_mass_scaled\": \"{}\",\n  \"pivotability_signature_states\": {},\n  \"literal_witness_samples\": {},\n  \"recordwise_checkpoint_comparison\": true,\n  \"elapsed_seconds\": {:.6}\n}}\n",chunk_rows,pair_count,pc,ic,zeros,ps,is,ps+is,piv_cache.len(),samples,begun.elapsed().as_secs_f64());
    File::create(OUT).unwrap().write_all(text.as_bytes()).unwrap();print!("{}",text);
}
