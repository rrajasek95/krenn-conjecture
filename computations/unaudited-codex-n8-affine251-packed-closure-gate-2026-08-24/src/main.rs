//! Bounded, read-only fixed-width and orbit-memo gates for the retained D12 closure.
//! This is deliberately a sibling of, and has no code path into, the production engine.

use std::cmp::{Ordering, Reverse};
use std::collections::{BinaryHeap, HashMap, HashSet, VecDeque};
use std::env;
use std::fs::File;
use std::io::{Read, Seek, SeekFrom};
use std::path::Path;
use std::thread;
use std::time::Instant;

const MAGIC: &[u8; 12] = b"AFF251CL1\0\0\0";
const HEADER: u64 = 46;
const ROW_RECORD: u64 = 13;
const COL_RECORD: u64 = 15;
const GROUP_ORDER: usize = 1440;
const FIXED_ORIGINAL: usize = 27 * 9 + 1;
const T_ID: u8 = 251;

#[repr(C)]
struct RUsage { fields: [std::os::raw::c_long; 18] }
unsafe extern "C" { fn getrusage(who: std::os::raw::c_int, usage: *mut RUsage) -> std::os::raw::c_int; }
fn peak_rss_kib() -> i64 {
    let mut value=RUsage{fields:[0;18]};
    let rc=unsafe{getrusage(0,&mut value)}; if rc!=0 { fail("getrusage failed") }
    #[cfg(target_os="macos")] { value.fields[4] as i64 / 1024 }
    #[cfg(not(target_os="macos"))] { value.fields[4] as i64 }
}

fn fail(s: impl AsRef<str>) -> ! {
    eprintln!("affine251-packed-gate: {}", s.as_ref());
    std::process::exit(2)
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row([u8; 12]);

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Col { word: u16, ids: [u8; 8] }

impl Ord for Col {
    fn cmp(&self, other: &Self) -> Ordering {
        self.word.cmp(&other.word).then(self.ids.cmp(&other.ids))
    }
}
impl PartialOrd for Col { fn partial_cmp(&self, other: &Self) -> Option<Ordering> { Some(self.cmp(other)) } }

// Byte-for-byte field shapes of the current production HashSet keys.
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct LegacyMono { len: u8, ids: [u8; 12] }
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct LegacyCol { word: u16, multiplier: LegacyMono }

#[derive(Clone, Copy)]
struct Header { rows: u64, cols: u64, row_frontier: u64, col_frontier: u64 }

fn u64le(v: &[u8]) -> u64 { u64::from_le_bytes(v.try_into().unwrap()) }

fn read_header(file: &mut File) -> Header {
    let mut b = [0u8; 46];
    file.seek(SeekFrom::Start(0)).unwrap_or_else(|e| fail(e.to_string()));
    file.read_exact(&mut b).unwrap_or_else(|e| fail(e.to_string()));
    if &b[..12] != MAGIC { fail("bad closure checkpoint magic"); }
    if b[12] != 12 || b[13] > 1 { fail("checkpoint degree/status mismatch"); }
    Header { rows: u64le(&b[14..22]), cols: u64le(&b[22..30]),
             row_frontier: u64le(&b[30..38]), col_frontier: u64le(&b[38..46]) }
}

fn blocks(total: u64, wanted: usize) -> Vec<(u64, usize)> {
    if wanted as u64 > total { fail("sample exceeds retained population"); }
    let nblocks = 16usize.min(wanted.max(1));
    let mut remain = wanted;
    let mut answer = Vec::new();
    for block in 0..nblocks {
        let take = (remain + nblocks - block - 1) / (nblocks - block);
        let max_start = total.saturating_sub(take as u64);
        let start = if nblocks == 1 { 0 } else { max_start * block as u64 / (nblocks - 1) as u64 };
        answer.push((start, take));
        remain -= take;
    }
    answer
}

fn load_rows(path: &Path, wanted: usize) -> Vec<Row> {
    let mut f = File::open(path).unwrap_or_else(|e| fail(e.to_string()));
    let h = read_header(&mut f);
    let mut out = Vec::with_capacity(wanted);
    for (start, take) in blocks(h.rows, wanted) {
        f.seek(SeekFrom::Start(HEADER + start * ROW_RECORD)).unwrap();
        for _ in 0..take {
            let mut b = [0u8; 13]; f.read_exact(&mut b).unwrap();
            if b[0] != 12 || !b[1..].windows(2).all(|w| w[0] <= w[1]) { fail("bad D12 row record"); }
            out.push(Row(b[1..].try_into().unwrap()));
        }
    }
    out.sort_unstable(); out.dedup();
    if out.len() != wanted { fail("distributed row blocks overlap"); }
    out
}

fn load_cols(path: &Path, wanted: usize) -> Vec<Col> {
    let mut f = File::open(path).unwrap_or_else(|e| fail(e.to_string()));
    let h = read_header(&mut f);
    let base = HEADER + h.rows * ROW_RECORD;
    let mut out = Vec::with_capacity(wanted);
    for (start, take) in blocks(h.cols, wanted) {
        f.seek(SeekFrom::Start(base + start * COL_RECORD)).unwrap();
        for _ in 0..take {
            let mut b = [0u8; 15]; f.read_exact(&mut b).unwrap();
            let word = u16::from_le_bytes([b[0], b[1]]);
            if word >= 6561 || b[2] != 8 || !b[3..11].windows(2).all(|w| w[0] <= w[1])
                || b[11..].iter().any(|x| *x != 0) { fail("bad D12 column record"); }
            out.push(Col { word, ids: b[3..11].try_into().unwrap() });
        }
    }
    out.sort_unstable(); out.dedup();
    if out.len() != wanted { fail("distributed column blocks overlap"); }
    out
}

fn source_index(i:usize, unique:usize, next:&mut usize)->usize {
    if i%5==4 { ((i/5).wrapping_mul(2_654_435_761usize))%unique }
    else { let answer=*next;*next+=1;answer }
}

fn pack_row(row: Row) -> u128 { row.0.iter().fold(0u128, |a, b| (a << 8) | *b as u128) }
fn unpack_row(mut x: u128) -> Row {
    let mut b = [0u8; 12]; for i in (0..12).rev() { b[i] = x as u8; x >>= 8; } Row(b)
}
fn pack_col(c: Col) -> u128 {
    let ids = c.ids.iter().fold(0u128, |a, b| (a << 8) | *b as u128);
    ((c.word as u128) << 64) | ids
}
fn unpack_col(x: u128) -> Col {
    let mut ids = [0u8; 8]; let mut y = x;
    for i in (0..8).rev() { ids[i] = y as u8; y >>= 8; }
    Col { word: (x >> 64) as u16, ids }
}

fn parallel_sort_dedup(mut values: Vec<u128>, workers: usize) -> Vec<u128> {
    let workers = workers.max(1).min(values.len().max(1));
    let chunk = (values.len() + workers - 1) / workers;
    thread::scope(|scope| {
        for part in values.chunks_mut(chunk) { scope.spawn(move || part.sort_unstable()); }
    });
    let ranges: Vec<(usize, usize)> = (0..values.len()).step_by(chunk)
        .map(|start| (start, (start + chunk).min(values.len()))).collect();
    let mut heap = BinaryHeap::new();
    for (run, &(start, end)) in ranges.iter().enumerate() {
        if start < end { heap.push(Reverse((values[start], run, start))); }
    }
    let mut out = Vec::with_capacity(values.len());
    while let Some(Reverse((value, run, index))) = heap.pop() {
        if out.last().copied() != Some(value) { out.push(value); }
        let next = index + 1;
        if next < ranges[run].1 { heap.push(Reverse((values[next], run, next))); }
    }
    out
}

// Small dependency-free SHA-256, used so equality is over exact sorted bytes.
fn sha256(input: &[u8]) -> String {
    const H0: [u32;8] = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
    const K: [u32;64] = [
        0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
        0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
        0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
        0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
        0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
        0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
        0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
        0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
    let bit_len = (input.len() as u64) * 8;
    let mut msg = input.to_vec(); msg.push(0x80);
    while msg.len() % 64 != 56 { msg.push(0); }
    msg.extend_from_slice(&bit_len.to_be_bytes());
    let mut h = H0;
    for block in msg.chunks_exact(64) {
        let mut w = [0u32;64];
        for i in 0..16 { w[i] = u32::from_be_bytes(block[4*i..4*i+4].try_into().unwrap()); }
        for i in 16..64 {
            let s0=w[i-15].rotate_right(7)^w[i-15].rotate_right(18)^(w[i-15]>>3);
            let s1=w[i-2].rotate_right(17)^w[i-2].rotate_right(19)^(w[i-2]>>10);
            w[i]=w[i-16].wrapping_add(s0).wrapping_add(w[i-7]).wrapping_add(s1);
        }
        let (mut a,mut b,mut c,mut d,mut e,mut f,mut g,mut z)=(h[0],h[1],h[2],h[3],h[4],h[5],h[6],h[7]);
        for i in 0..64 {
            let s1=e.rotate_right(6)^e.rotate_right(11)^e.rotate_right(25);
            let ch=(e&f)^(!e&g); let t1=z.wrapping_add(s1).wrapping_add(ch).wrapping_add(K[i]).wrapping_add(w[i]);
            let s0=a.rotate_right(2)^a.rotate_right(13)^a.rotate_right(22);
            let maj=(a&b)^(a&c)^(b&c); let t2=s0.wrapping_add(maj);
            z=g;g=f;f=e;e=d.wrapping_add(t1);d=c;c=b;b=a;a=t1.wrapping_add(t2);
        }
        for (x,y) in h.iter_mut().zip([a,b,c,d,e,f,g,z]) { *x=x.wrapping_add(y); }
    }
    h.iter().map(|x| format!("{x:08x}")).collect()
}

fn rows_bytes(values: &[Row]) -> Vec<u8> { values.iter().flat_map(|x| x.0).collect() }
fn cols_bytes(values: &[Col]) -> Vec<u8> {
    let mut out=Vec::with_capacity(values.len()*10);
    for c in values { out.extend_from_slice(&c.word.to_le_bytes()); out.extend_from_slice(&c.ids); }
    out
}

fn bench(path: &Path, kind: &str, backend: &str, n: usize, workers: usize) {
    if n < 5 || n % 5 != 0 { fail("candidate count must be a positive multiple of five"); }
    let unique = n*4/5;
    let start=Instant::now();
    match (kind,backend) {
        ("row","hashset") => {
            let base=load_rows(path,unique); let loaded=start.elapsed().as_secs_f64();
            let timed=Instant::now(); let mut set=HashSet::<LegacyMono>::new();let mut next=0;
            for i in 0..n { let r=base[source_index(i,unique,&mut next)];set.insert(LegacyMono{len:12,ids:r.0}); }
            let mut old:Vec<LegacyMono>=set.into_iter().collect(); old.sort_unstable();
            let out:Vec<Row>=old.into_iter().map(|r|Row(r.ids)).collect();
            let seconds=timed.elapsed().as_secs_f64(); let digest=sha256(&rows_bytes(&out));
            println!("{{\"kind\":\"row\",\"backend\":\"hashset\",\"candidates\":{n},\"input_unique\":{unique},\"output_count\":{},\"sorted_sha256\":\"{digest}\",\"load_seconds\":{loaded:.9},\"dedup_seconds\":{seconds:.9},\"workers\":1,\"key_bytes\":{},\"peak_rss_kib\":{}}}",out.len(),std::mem::size_of::<LegacyMono>(),peak_rss_kib()); return
        },
        ("row","packed") => {
            let base=load_rows(path,unique); let loaded=start.elapsed().as_secs_f64();
            let timed=Instant::now();let mut next=0;let mut packed=Vec::with_capacity(n);
            for i in 0..n {packed.push(pack_row(base[source_index(i,unique,&mut next)]));}
            let packed=parallel_sort_dedup(packed,workers); let out:Vec<Row>=packed.into_iter().map(unpack_row).collect();
            let seconds=timed.elapsed().as_secs_f64(); let digest=sha256(&rows_bytes(&out));
            println!("{{\"kind\":\"row\",\"backend\":\"packed_parallel_sort\",\"candidates\":{n},\"input_unique\":{unique},\"output_count\":{},\"sorted_sha256\":\"{digest}\",\"load_seconds\":{loaded:.9},\"dedup_seconds\":{seconds:.9},\"workers\":{workers},\"key_bytes\":16,\"peak_rss_kib\":{}}}",out.len(),peak_rss_kib()); return
        },
        ("column","hashset") => {
            let base=load_cols(path,unique); let loaded=start.elapsed().as_secs_f64();
            let timed=Instant::now(); let mut set=HashSet::<LegacyCol>::new();let mut next=0;
            for i in 0..n {let c=base[source_index(i,unique,&mut next)];set.insert(LegacyCol{word:c.word,multiplier:LegacyMono{len:8,ids:{let mut ids=[0;12];ids[..8].copy_from_slice(&c.ids);ids}}});}
            let mut old:Vec<LegacyCol>=set.into_iter().collect();old.sort_unstable();
            let out:Vec<Col>=old.into_iter().map(|c|Col{word:c.word,ids:c.multiplier.ids[..8].try_into().unwrap()}).collect();
            let seconds=timed.elapsed().as_secs_f64(); let digest=sha256(&cols_bytes(&out));
            println!("{{\"kind\":\"column\",\"backend\":\"hashset\",\"candidates\":{n},\"input_unique\":{unique},\"output_count\":{},\"sorted_sha256\":\"{digest}\",\"load_seconds\":{loaded:.9},\"dedup_seconds\":{seconds:.9},\"workers\":1,\"key_bytes\":{},\"peak_rss_kib\":{}}}",out.len(),std::mem::size_of::<LegacyCol>(),peak_rss_kib()); return
        },
        ("column","packed") => {
            let base=load_cols(path,unique); let loaded=start.elapsed().as_secs_f64();
            let timed=Instant::now();let mut next=0;let mut packed=Vec::with_capacity(n);
            for i in 0..n {packed.push(pack_col(base[source_index(i,unique,&mut next)]));}
            let packed=parallel_sort_dedup(packed,workers); let out:Vec<Col>=packed.into_iter().map(unpack_col).collect();
            let seconds=timed.elapsed().as_secs_f64(); let digest=sha256(&cols_bytes(&out));
            println!("{{\"kind\":\"column\",\"backend\":\"packed_parallel_sort\",\"candidates\":{n},\"input_unique\":{unique},\"output_count\":{},\"sorted_sha256\":\"{digest}\",\"load_seconds\":{loaded:.9},\"dedup_seconds\":{seconds:.9},\"workers\":{workers},\"key_bytes\":16,\"peak_rss_kib\":{}}}",out.len(),peak_rss_kib()); return
        },
        _ => fail("unknown benchmark kind/backend")
    }
}

fn permutations_six() -> Vec<[u8;6]> {
    fn visit(p:usize, used:&mut[bool;6], cur:&mut[u8;6], out:&mut Vec<[u8;6]>) {
        if p==6 { out.push(*cur); return }
        for x in 0..6 { if !used[x] { used[x]=true;cur[p]=x as u8;visit(p+1,used,cur,out);used[x]=false; } }
    }
    let mut out=Vec::with_capacity(720); visit(0,&mut[false;6],&mut[0;6],&mut out); out
}

fn actions() -> Vec<[u8;252]> {
    let mut edges=[(0u8,0u8);28]; let mut edge_id=[[0u8;8];8]; let mut next=0usize;
    for l in 0..8u8 { for r in l+1..8u8 { edges[next]=(l,r);edge_id[l as usize][r as usize]=next as u8;edge_id[r as usize][l as usize]=next as u8;next+=1; } }
    let mut original_to_affine=[T_ID;252]; let mut a=0usize;
    for o in 0..252 { if o!=FIXED_ORIGINAL { original_to_affine[o]=a as u8;a+=1; } }
    let mut out=Vec::with_capacity(1440);
    for perm in permutations_six() { for flip in 0..2usize {
        let mut sites=[0u8;8];sites[..6].copy_from_slice(&perm);sites[6]=if flip==0{6}else{7};sites[7]=if flip==0{7}else{6};
        let colours=if flip==0{[0u8,1,2]}else{[1u8,0,2]}; let mut map=[0u8;252];
        for affine in 0..251usize {
            let original=if affine<FIXED_ORIGINAL{affine}else{affine+1};let edge=original/9;let ca=(original%9)/3;let cb=original%3;
            let (l,r)=edges[edge];let(mut ml,mut mr)=(sites[l as usize],sites[r as usize]);let(mut ma,mut mb)=(colours[ca],colours[cb]);
            if ml>mr { std::mem::swap(&mut ml,&mut mr);std::mem::swap(&mut ma,&mut mb); }
            let moved=edge_id[ml as usize][mr as usize] as usize*9+ma as usize*3+mb as usize;map[affine]=original_to_affine[moved];
        }
        map[251]=251;out.push(map);
    }}
    if out.len()!=GROUP_ORDER { fail("action count mismatch") } out
}

fn moved(row:Row, action:&[u8;252])->Row { let mut x=row.0;for b in &mut x{*b=action[*b as usize];}x.sort_unstable();Row(x) }
fn brute(row:Row, actions:&[[u8;252]])->Row { actions.iter().map(|a|moved(row,a)).min().unwrap() }

fn canon_bench(path:&Path, backend:&str, n:usize) {
    let maps=actions(); let base_count=256usize.min(n.max(1)); let bases=load_rows(path,base_count);
    let raw:Vec<Row>=(0..n).map(|i| moved(bases[i%base_count],&maps[(i.wrapping_mul(7919)+i/base_count)%GROUP_ORDER])).collect();
    let start=Instant::now(); let mut cache=HashMap::<Row,Row>::new(); let mut output=Vec::with_capacity(n);
    match backend {
        "exact_cache" => for x in raw { let c=if let Some(c)=cache.get(&x){*c}else{let c=brute(x,&maps);cache.insert(x,c);c};output.push(c); },
        "orbit_memo" => for x in raw { let c=if let Some(c)=cache.get(&x){*c}else{let c=brute(x,&maps);for a in &maps{cache.insert(moved(x,a),c);}c};output.push(c); },
        _=>fail("unknown canonical backend")
    }
    let seconds=start.elapsed().as_secs_f64(); output.sort_unstable();
    let digest=sha256(&rows_bytes(&output));
    println!("{{\"kind\":\"row_natural_minimum\",\"backend\":\"{backend}\",\"candidates\":{n},\"base_orbits\":{base_count},\"output_count\":{},\"sorted_sha256\":\"{digest}\",\"seconds\":{seconds:.9},\"memo_entries\":{},\"actions\":1440,\"peak_rss_kib\":{}}}",output.len(),cache.len(),peak_rss_kib());
}

fn capped_insert(cache:&mut HashMap<Row,Row>,fifo:&mut VecDeque<Row>,key:Row,value:Row,cap:usize,evictions:&mut usize) {
    if cache.contains_key(&key){return}
    while cache.len()>=cap {let old=fifo.pop_front().unwrap();if cache.remove(&old).is_some(){*evictions+=1;}}
    cache.insert(key,value);fifo.push_back(key);
}

fn canon_cap_bench(path:&Path,backend:&str,pattern:&str,n:usize,cap:usize) {
    if cap==0{fail("zero memo cap")}
    let maps=actions();let base_count=match pattern{"correlated"=>256usize.min(n.max(1)),"adversarial"=>n,_=>fail("unknown canonical pattern")};
    let bases=load_rows(path,base_count);
    let raw:Vec<Row>=(0..n).map(|i|moved(bases[i%base_count],&maps[(i.wrapping_mul(7919)+i/base_count)%GROUP_ORDER])).collect();
    let start=Instant::now();let mut cache=HashMap::<Row,Row>::new();let mut fifo=VecDeque::new();let(mut hits,mut misses,mut evictions)=(0usize,0usize,0usize);let mut output=Vec::with_capacity(n);
    match backend {
      "exact_cache"=>for x in raw {if let Some(c)=cache.get(&x){hits+=1;output.push(*c)}else{misses+=1;let c=brute(x,&maps);capped_insert(&mut cache,&mut fifo,x,c,cap,&mut evictions);output.push(c)}},
      "orbit_memo_cap"=>for x in raw {if let Some(c)=cache.get(&x){hits+=1;output.push(*c)}else{misses+=1;let c=brute(x,&maps);for a in &maps{capped_insert(&mut cache,&mut fifo,moved(x,a),c,cap,&mut evictions);}output.push(c)}},
      _=>fail("unknown capped canonical backend")
    }
    let seconds=start.elapsed().as_secs_f64();output.sort_unstable();let digest=sha256(&rows_bytes(&output));
    println!("{{\"kind\":\"row_natural_minimum_capped\",\"backend\":\"{backend}\",\"pattern\":\"{pattern}\",\"candidates\":{n},\"base_orbits\":{base_count},\"cap_entries\":{cap},\"output_count\":{},\"sorted_sha256\":\"{digest}\",\"seconds\":{seconds:.9},\"memo_entries\":{},\"hits\":{hits},\"misses\":{misses},\"evictions\":{evictions},\"hit_rate\":{:.9},\"actions\":1440,\"peak_rss_kib\":{}}}",output.len(),cache.len(),hits as f64/n as f64,peak_rss_kib());
}

fn validate(path:&Path) {
    let mut f=File::open(path).unwrap_or_else(|e|fail(e.to_string()));let h=read_header(&mut f);
    let expected=HEADER+h.rows*ROW_RECORD+h.cols*COL_RECORD+h.row_frontier*ROW_RECORD+h.col_frontier*COL_RECORD;
    let mut prev_row=None;
    for _ in 0..h.rows+h.row_frontier { let mut b=[0u8;13];f.read_exact(&mut b).unwrap_or_else(|e|fail(e.to_string()));if b[0]!=12||!b[1..].windows(2).all(|w|w[0]<=w[1]){fail("bad D12 row record")}let r:Row=Row(b[1..].try_into().unwrap());if prev_row==Some(r){fail("duplicate row")}prev_row=Some(r); }
    // Full closure order is rows, columns, row frontier, column frontier. Tiny hostile files have no frontier.
    if h.row_frontier!=0||h.col_frontier!=0{fail("validator only accepts frontier-free hostile fixtures")}
    for _ in 0..h.cols {let mut b=[0u8;15];f.read_exact(&mut b).unwrap_or_else(|e|fail(e.to_string()));let w=u16::from_le_bytes([b[0],b[1]]);if w>=6561||b[2]!=8||!b[3..11].windows(2).all(|x|x[0]<=x[1])||b[11..].iter().any(|x|*x!=0){fail("bad D12 column record")}}
    if f.metadata().unwrap().len()!=expected{fail("trailing checkpoint bytes")}
    println!("{{\"status\":\"PASS\",\"rows\":{},\"columns\":{}}}",h.rows,h.cols);
}

fn selftest() {
    let r1=Row([0,1,1,3,5,8,13,21,34,55,89,251]);let r2=Row([0,1,1,3,5,8,13,21,34,56,80,251]);
    assert_eq!(unpack_row(pack_row(r1)),r1);assert_eq!(r1.cmp(&r2),pack_row(r1).cmp(&pack_row(r2)));
    let c1=Col{word:255,ids:[0,1,2,3,4,5,6,7]};let c2=Col{word:256,ids:[0;8]};
    assert_eq!(unpack_col(pack_col(c1)),c1);assert_eq!(c1.cmp(&c2),pack_col(c1).cmp(&pack_col(c2)));
    let raw=vec![pack_row(r2),pack_row(r1),pack_row(r2)];let got=parallel_sort_dedup(raw,3);assert_eq!(got,vec![pack_row(r1),pack_row(r2)]);
    assert_eq!(std::mem::size_of::<LegacyMono>(),13);assert_eq!(std::mem::size_of::<LegacyCol>(),16);
    assert_eq!(sha256(b"abc"),"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
    println!("{{\"status\":\"PASS\",\"cases\":[\"row_roundtrip\",\"row_natural_order\",\"column_roundtrip\",\"column_natural_order\",\"parallel_dedup\",\"legacy_layout_13_16\",\"sha256_vector\"]}}");
}

fn main() {
    let a:Vec<String>=env::args().collect();if a.len()<2{fail("expected bench|canon|canoncap|validate|selftest")}
    match a[1].as_str(){
        "bench" if a.len()==7=>bench(Path::new(&a[2]),&a[3],&a[4],a[5].parse().unwrap(),a[6].parse().unwrap()),
        "canon" if a.len()==5=>canon_bench(Path::new(&a[2]),&a[3],a[4].parse().unwrap()),
        "canoncap" if a.len()==7=>canon_cap_bench(Path::new(&a[2]),&a[3],&a[4],a[5].parse().unwrap(),a[6].parse().unwrap()),
        "validate" if a.len()==3=>validate(Path::new(&a[2])),
        "selftest" if a.len()==2=>selftest(),
        _=>fail("bad arguments")
    }
}
