// Full external-memory hidden K16 -> K18 [2,2] collector.
// No K20 tails are generated here.
include!("../unaudited-codex-orbit0-hidden-k16-orbit-profile-prefix-2026-08-23/audit_hidden_k16_pair_orbits.rs");

use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::fs::{metadata, remove_file};

const FDIR: &str =
    "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/";
const PAIR_HEADER: usize = 80;
const EXACT_REC: usize = 49;
const ORBIT_REC: usize = 53;
const CHILD_REC: usize = 80;
const ORBIT_CHUNK: usize = 500_000;
const CHILD_CHUNK: usize = 350_000;
const GATE_SECONDS: f64 = 600.0;
const RESUME_GATE_SECONDS: f64 = 250.0;
const REFEREE_MARKER: &str =
    "computations/unaudited-codex-orbit0-hidden-k16-k2-full-orbit-2026-08-23/independent_k18_referee_pass.json";

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct ChildWitness {
    pair: PairKey,
    tail: u8,
    pair_uses: u64,
    orbit_size: u16,
    stabilizer: u16,
    m2: u8,
}
impl Ord for ChildWitness {
    fn cmp(&self, o: &Self) -> std::cmp::Ordering {
        (self.pair, self.tail, self.pair_uses, self.orbit_size, self.stabilizer, self.m2)
            .cmp(&(o.pair, o.tail, o.pair_uses, o.orbit_size, o.stabilizer, o.m2))
    }
}
impl PartialOrd for ChildWitness {
    fn partial_cmp(&self, o: &Self) -> Option<std::cmp::Ordering> { Some(self.cmp(o)) }
}
#[derive(Clone, Copy)]
struct ChildAgg { weight: i128, witness: ChildWitness, pivotable: bool }

fn put_pair_header(
    w: &mut BufWriter<File>, magic: &[u8; 8], start: u16, end: u16,
    rec_size: u16, input: u64, aux: u64, count: u64, before: u64, sum: i128,
) {
    w.write_all(magic).unwrap();
    w.write_all(&U.to_le_bytes()).unwrap();
    w.write_all(&start.to_le_bytes()).unwrap();
    w.write_all(&end.to_le_bytes()).unwrap();
    w.write_all(&rec_size.to_le_bytes()).unwrap();
    w.write_all(&[0; 2]).unwrap();
    w.write_all(&input.to_le_bytes()).unwrap();
    w.write_all(&aux.to_le_bytes()).unwrap();
    w.write_all(&count.to_le_bytes()).unwrap();
    w.write_all(&before.to_le_bytes()).unwrap();
    w.write_all(&sum.to_le_bytes()).unwrap();
}

fn read_exact_record<R: Read>(r: &mut R) -> Option<(PairKey, PairAgg)> {
    let mut b = [0u8; EXACT_REC];
    match r.read_exact(&mut b) {
        Ok(()) => {}
        Err(x) if x.kind() == std::io::ErrorKind::UnexpectedEof => return None,
        Err(x) => panic!("read exact-pair record: {x}"),
    }
    let mut row = [0u8; 24]; row.copy_from_slice(&b[..24]);
    Some((PairKey { row: Row(row), pivot: b[24] }, PairAgg {
        weight: i128::from_le_bytes(b[25..41].try_into().unwrap()),
        uses: u64::from_le_bytes(b[41..49].try_into().unwrap()),
    }))
}
fn write_exact_record<W: Write>(w: &mut W, k: PairKey, a: PairAgg) {
    w.write_all(&k.row.0).unwrap(); w.write_all(&[k.pivot]).unwrap();
    w.write_all(&a.weight.to_le_bytes()).unwrap(); w.write_all(&a.uses.to_le_bytes()).unwrap();
}
fn read_orbit_record<R: Read>(r: &mut R) -> Option<(PairKey, PairAgg, u16, u16)> {
    let mut b = [0u8; ORBIT_REC];
    match r.read_exact(&mut b) {
        Ok(()) => {}
        Err(x) if x.kind() == std::io::ErrorKind::UnexpectedEof => return None,
        Err(x) => panic!("read orbit-pair record: {x}"),
    }
    let mut row = [0u8; 24]; row.copy_from_slice(&b[..24]);
    Some((PairKey { row: Row(row), pivot: b[24] }, PairAgg {
        weight: i128::from_le_bytes(b[25..41].try_into().unwrap()),
        uses: u64::from_le_bytes(b[41..49].try_into().unwrap()),
    }, u16::from_le_bytes(b[49..51].try_into().unwrap()),
       u16::from_le_bytes(b[51..53].try_into().unwrap())))
}
fn write_orbit_record<W: Write>(w: &mut W, k: PairKey, a: PairAgg, os: u16, ss: u16) {
    write_exact_record(w, k, a); w.write_all(&os.to_le_bytes()).unwrap(); w.write_all(&ss.to_le_bytes()).unwrap();
}
fn write_child_record<W: Write>(w: &mut W, row: Row, a: ChildAgg) {
    w.write_all(&row.0).unwrap(); w.write_all(&a.weight.to_le_bytes()).unwrap();
    w.write_all(&a.witness.pair.row.0).unwrap();
    w.write_all(&[a.witness.pair.pivot, a.witness.tail]).unwrap();
    w.write_all(&a.witness.pair_uses.to_le_bytes()).unwrap();
    w.write_all(&a.witness.orbit_size.to_le_bytes()).unwrap();
    w.write_all(&a.witness.stabilizer.to_le_bytes()).unwrap();
    w.write_all(&[a.pivotable as u8, a.witness.m2]).unwrap();
}
fn read_child_record<R: Read>(r: &mut R) -> Option<(Row, ChildAgg)> {
    let mut b = [0u8; CHILD_REC];
    match r.read_exact(&mut b) {
        Ok(()) => {}
        Err(x) if x.kind() == std::io::ErrorKind::UnexpectedEof => return None,
        Err(x) => panic!("read child record: {x}"),
    }
    let mut row = [0u8;24]; row.copy_from_slice(&b[..24]);
    let mut prow = [0u8;24]; prow.copy_from_slice(&b[40..64]);
    Some((Row(row), ChildAgg {
        weight: i128::from_le_bytes(b[24..40].try_into().unwrap()),
        witness: ChildWitness {
            pair: PairKey { row: Row(prow), pivot: b[64] }, tail: b[65],
            pair_uses: u64::from_le_bytes(b[66..74].try_into().unwrap()),
            orbit_size: u16::from_le_bytes(b[74..76].try_into().unwrap()),
            stabilizer: u16::from_le_bytes(b[76..78].try_into().unwrap()), m2: b[79],
        }, pivotable: b[78] != 0,
    }))
}

fn exact_run_path(start: usize, end: usize) -> String { format!("{}exact_pairs_{:03}_{:03}.bin", FDIR, start, end) }
fn orbit_chunk_path(i: usize) -> String { format!("{}orbit_chunk_{:04}.bin", FDIR, i) }
fn child_chunk_path(i: usize) -> String { format!("{}child_chunk_{:04}.bin", FDIR, i) }
fn parallel_child_chunk_path(i: usize) -> String { format!("{}pchild_chunk_{:04}.bin", FDIR, i) }

fn make_exact_run(start: usize, end: usize, begun: &Instant, e: &Engine) -> (u64,u64,u64,i128) {
    let path = exact_run_path(start,end);
    if metadata(&path).is_ok() {
        let mut r=BufReader::new(File::open(&path).unwrap()); let mut h=[0u8;PAIR_HEADER];r.read_exact(&mut h).unwrap();
        assert_eq!(&h[..8],b"H16EXA1\0"); assert_eq!(u16::from_le_bytes(h[24..26].try_into().unwrap())as usize,start);
        assert_eq!(u16::from_le_bytes(h[26..28].try_into().unwrap())as usize,end); assert_eq!(u16::from_le_bytes(h[28..30].try_into().unwrap())as usize,EXACT_REC);
        let input=u64::from_le_bytes(h[32..40].try_into().unwrap()); let outgoing=u64::from_le_bytes(h[40..48].try_into().unwrap()); let count=u64::from_le_bytes(h[48..56].try_into().unwrap());
        let sum=i128::from_le_bytes(h[64..80].try_into().unwrap()); assert_eq!(metadata(&path).unwrap().len(),PAIR_HEADER as u64+EXACT_REC as u64*count);
        return(input,outgoing,count,sum)
    }
    let parent_path=format!("{}parents_{:03}_{:03}.bin",HDIR,start,end);
    let mut r=BufReader::with_capacity(1<<20,File::open(parent_path).unwrap()); let mut h=[0u8;40];r.read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"H16RUN2\0");
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()),U); let parents=u64::from_le_bytes(h[32..40].try_into().unwrap());
    let mut map:HashMap<PairKey,PairAgg>=HashMap::new(); let(mut outgoing,mut sum)=(0u64,0i128);
    for _ in 0..parents { let mut b=[0u8;64];r.read_exact(&mut b).unwrap();let mut rr=[0u8;24];rr.copy_from_slice(&b[..24]);let row=Row(rr);let w1=i128::from_le_bytes(b[24..40].try_into().unwrap());let mut s=[0u8;12];s.copy_from_slice(&b[40..52]);assert_eq!(signature(&row.0,e),s);let ps=available(s,e);let m2=b[60]as usize;assert_eq!(ps.len(),m2);assert_eq!(w1%m2 as i128,0);let w2=-w1/m2 as i128;for p in ps{outgoing+=1;sum+=w2;add_pair(&mut map,PairKey{row,pivot:p as u8},w2)}}
    let before=map.len()as u64;let mut v:Vec<_>=map.into_iter().collect();v.sort_unstable_by_key(|x|x.0);let tmp=format!("{}.tmp",path);let mut w=BufWriter::with_capacity(1<<20,File::create(&tmp).unwrap());put_pair_header(&mut w,b"H16EXA1\0",start as u16,end as u16,EXACT_REC as u16,parents,outgoing,v.len()as u64,before,sum);for(k,a)in v{write_exact_record(&mut w,k,a)}w.flush().unwrap();drop(w);rename(tmp,&path).unwrap();
    eprintln!("EXACT_RUN {}..{} parents={} outgoing={} pairs={} elapsed={:.1}",start,end,parents,outgoing,before,begun.elapsed().as_secs_f64());(parents,outgoing,before,sum)
}

struct ExactReader { r: BufReader<File>, cur: Option<(PairKey,PairAgg)> }
struct OrbitReader { r: BufReader<File>, cur: Option<(PairKey,PairAgg,u16,u16)> }
struct ChildReader { r: BufReader<File>, cur: Option<(Row,ChildAgg)> }

#[derive(Clone,Copy,Debug)]
struct ChildChunkMeta { start:u64, end:u64, count:u64, raw:u64, sum:i128 }

fn validate_child_chunk(path:&str,expected:Option<(u64,u64)>)->ChildChunkMeta{
    let mut r=BufReader::new(File::open(path).unwrap());let mut h=[0u8;PAIR_HEADER];r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8],b"H18CHC1\0");
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()),U);
    assert_eq!((u16::from_le_bytes(h[24..26].try_into().unwrap()),u16::from_le_bytes(h[26..28].try_into().unwrap())),(0,0));
    assert_eq!(u16::from_le_bytes(h[28..30].try_into().unwrap())as usize,CHILD_REC);
    assert_eq!(&h[30..32],&[0,0]);
    let m=ChildChunkMeta{start:u64::from_le_bytes(h[32..40].try_into().unwrap()),end:u64::from_le_bytes(h[40..48].try_into().unwrap()),count:u64::from_le_bytes(h[48..56].try_into().unwrap()),raw:u64::from_le_bytes(h[56..64].try_into().unwrap()),sum:i128::from_le_bytes(h[64..80].try_into().unwrap())};
    assert!(m.end>m.start);assert_eq!(m.raw,12*(m.end-m.start));assert!(m.count>0);
    assert_eq!(metadata(path).unwrap().len(),PAIR_HEADER as u64+CHILD_REC as u64*m.count);
    if let Some((start,end))=expected{assert_eq!((m.start,m.end),(start,end))}
    m
}

fn scan_pair_stabilizers(path:&str,expected_count:u64,expected_sum:i128)->BTreeMap<usize,u64>{
    let mut r=BufReader::with_capacity(8<<20,File::open(path).unwrap());let mut h=[0u8;PAIR_HEADER];r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8],b"H16ORM1\0");assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()),U);assert_eq!(u16::from_le_bytes(h[28..30].try_into().unwrap())as usize,ORBIT_REC);
    let count=u64::from_le_bytes(h[48..56].try_into().unwrap());let sum0=i128::from_le_bytes(h[64..80].try_into().unwrap());assert_eq!((count,sum0),(expected_count,expected_sum));assert_eq!(metadata(path).unwrap().len(),PAIR_HEADER as u64+ORBIT_REC as u64*count);
    let mut hist=BTreeMap::new();let mut sum=0i128;let mut prior=None;
    for _ in 0..count{let(k,a,os,ss)=read_orbit_record(&mut r).unwrap();if let Some(p)=prior{assert!(p<k)}prior=Some(k);assert_eq!(u32::from(os)*u32::from(ss),384);sum+=a.weight;*hist.entry(ss as usize).or_default()+=1}
    assert!(read_orbit_record(&mut r).is_none());assert_eq!(sum,expected_sum);assert_eq!(hist.values().sum::<u64>(),expected_count);assert!(!hist.is_empty());hist
}

fn assert_stabilizer_histogram(hist:&BTreeMap<usize,u64>,pair_count:u64){assert!(!hist.is_empty());assert_eq!(hist.values().sum::<u64>(),pair_count);for(&ss,_)in hist{assert!(ss>0&&384%ss==0)}}

fn validate_final_checkpoint(path:&str,magic:&[u8;8],flag:u64,pair_count:u64,generated:u64)->u64{
    let mut r=BufReader::new(File::open(path).unwrap());let mut h=[0u8;PAIR_HEADER];r.read_exact(&mut h).unwrap();assert_eq!(&h[..8],magic);assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()),U);assert_eq!((u16::from_le_bytes(h[24..26].try_into().unwrap()),u16::from_le_bytes(h[26..28].try_into().unwrap())),(0,0));assert_eq!(u16::from_le_bytes(h[28..30].try_into().unwrap())as usize,CHILD_REC);assert_eq!(&h[30..32],&[0,0]);assert_eq!(u64::from_le_bytes(h[32..40].try_into().unwrap()),pair_count);assert_eq!(u64::from_le_bytes(h[40..48].try_into().unwrap()),generated);let count=u64::from_le_bytes(h[48..56].try_into().unwrap());assert_eq!(u64::from_le_bytes(h[56..64].try_into().unwrap()),flag);assert_eq!(metadata(path).unwrap().len(),PAIR_HEADER as u64+CHILD_REC as u64*count);count
}

fn cleanup_refereed_child_chunks(marker_path:&str){
    let marker=std::fs::read_to_string(marker_path).expect("independent referee marker is required");assert!(marker.contains("\"status\": \"PASS_INDEPENDENT_K18_REFEREE\""));assert!(marker.contains("\"pivotable_sha256\""));assert!(marker.contains("\"irreducible_sha256\""));
    let pair_path=format!("{}hidden_k16_decorated_pair_orbits_full.bin",FDIR);let mut r=BufReader::new(File::open(&pair_path).unwrap());let mut h=[0u8;PAIR_HEADER];r.read_exact(&mut h).unwrap();let pair_count=u64::from_le_bytes(h[48..56].try_into().unwrap());let generated=12*pair_count;
    validate_final_checkpoint(&format!("{}checkpoint_k18_22_pivotable.bin",FDIR),b"H18PIV2\0",1,pair_count,generated);validate_final_checkpoint(&format!("{}checkpoint_k18_22_irreducible.bin",FDIR),b"H18IRR2\0",0,pair_count,generated);
    let nchunks=((pair_count+CHILD_CHUNK as u64-1)/CHILD_CHUNK as u64)as usize;for ci in 0..nchunks{let path=parallel_child_chunk_path(ci);validate_child_chunk(&path,None);}for ci in 0..nchunks{remove_file(parallel_child_chunk_path(ci)).unwrap()}eprintln!("CLEANED {} independently-refereed child chunks",nchunks)
}

fn flush_orbit_chunk(index:usize,map:&mut HashMap<PairKey,(PairAgg,u16,u16)>)->u64{
    let path=orbit_chunk_path(index);let mut v:Vec<_>=map.drain().collect();v.sort_unstable_by_key(|x|x.0);let count=v.len()as u64;let sum:i128=v.iter().map(|x|(x.1).0.weight).sum();let tmp=format!("{}.tmp",path);let mut w=BufWriter::with_capacity(1<<20,File::create(&tmp).unwrap());put_pair_header(&mut w,b"H16ORC1\0",index as u16,0,ORBIT_REC as u16,0,0,count,count,sum);for(k,(a,os,ss))in v{write_orbit_record(&mut w,k,a,os,ss)}w.flush().unwrap();drop(w);rename(tmp,path).unwrap();count}

fn build_orbit_chunks(run_paths:&[String], begun:&Instant,e:&Engine,pp:&[[u8;78]])->(Vec<String>,u64,u64,i128,BTreeMap<usize,u64>){
    let mut rs=Vec::new();let mut heap=BinaryHeap::new();for(i,path)in run_paths.iter().enumerate(){let mut r=BufReader::with_capacity(1<<20,File::open(path).unwrap());let mut h=[0u8;PAIR_HEADER];r.read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"H16EXA1\0");let cur=read_exact_record(&mut r);if let Some((k,_))=cur{heap.push(Reverse((k,i)))}rs.push(ExactReader{r,cur})}
    let mut chunks=Vec::new();let mut map:HashMap<PairKey,(PairAgg,u16,u16)>=HashMap::new();let(mut distinct,mut zero,mut sum)=(0u64,0u64,0i128);let mut sig_actions=HashMap::new();let mut stab_actions=HashMap::new();let mut stab_hist:BTreeMap<usize,u64>=BTreeMap::new();
    while let Some(Reverse((key,i)))=heap.pop(){assert_eq!(rs[i].cur.unwrap().0,key);let mut a=rs[i].cur.unwrap().1;rs[i].cur=read_exact_record(&mut rs[i].r);if let Some((k,_))=rs[i].cur{heap.push(Reverse((k,i)))}while let Some(Reverse((k,j)))=heap.peek().copied(){if k!=key{break}heap.pop();let b=rs[j].cur.unwrap().1;a.weight+=b.weight;a.uses+=b.uses;rs[j].cur=read_exact_record(&mut rs[j].r);if let Some((n,_))=rs[j].cur{heap.push(Reverse((n,j)))}}
        distinct+=1;if a.weight==0{zero+=1;continue}sum+=a.weight;let q=canonical_pair(key,e,pp,&mut sig_actions);let(os,ss)=orbit_stabilizer(q,e,pp,&mut stab_actions);*stab_hist.entry(ss).or_default()+=1;use std::collections::hash_map::Entry;match map.entry(q){Entry::Vacant(v)=>{v.insert((a,os as u16,ss as u16));}Entry::Occupied(mut o)=>{let x=o.get_mut();assert_eq!((x.1,x.2),(os as u16,ss as u16));x.0.weight+=a.weight;x.0.uses+=a.uses;if x.0.weight==0{o.remove();}}}
        if map.len()>=ORBIT_CHUNK{let idx=chunks.len();flush_orbit_chunk(idx,&mut map);chunks.push(orbit_chunk_path(idx));if begun.elapsed().as_secs_f64()>GATE_SECONDS{panic!("600s gate during orbit chunks")}}
    }
    if !map.is_empty(){let idx=chunks.len();flush_orbit_chunk(idx,&mut map);chunks.push(orbit_chunk_path(idx))}eprintln!("ORBIT_CHUNKS n={} exact_distinct={} exact_zero={} elapsed={:.1}",chunks.len(),distinct,zero,begun.elapsed().as_secs_f64());(chunks,distinct,zero,sum,stab_hist)
}

fn merge_orbit_chunks(paths:&[String],begun:&Instant)->(String,u64,u64,i128,BTreeMap<usize,u64>){
    let out=format!("{}hidden_k16_decorated_pair_orbits_full.bin",FDIR);let mut rs=Vec::new();let mut heap=BinaryHeap::new();for(i,path)in paths.iter().enumerate(){let mut r=BufReader::with_capacity(1<<20,File::open(path).unwrap());let mut h=[0u8;PAIR_HEADER];r.read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"H16ORC1\0");let cur=read_orbit_record(&mut r);if let Some((k,_,_,_))=cur{heap.push(Reverse((k,i)))}rs.push(OrbitReader{r,cur})}
    let tmp=format!("{}.tmp",out);let mut w=BufWriter::with_capacity(1<<20,File::create(&tmp).unwrap());put_pair_header(&mut w,b"H16ORM1\0",0,0,ORBIT_REC as u16,paths.len()as u64,0,0,0,0);let(mut count,mut zero,mut sum)=(0u64,0u64,0i128);let mut sh:BTreeMap<usize,u64>=BTreeMap::new();
    while let Some(Reverse((key,i)))=heap.pop(){let(_,mut a,os,ss)=rs[i].cur.unwrap();rs[i].cur=read_orbit_record(&mut rs[i].r);if let Some((k,_,_,_))=rs[i].cur{heap.push(Reverse((k,i)))}while let Some(Reverse((k,j)))=heap.peek().copied(){if k!=key{break}heap.pop();let(_,b,o2,s2)=rs[j].cur.unwrap();assert_eq!((os,ss),(o2,s2));a.weight+=b.weight;a.uses+=b.uses;rs[j].cur=read_orbit_record(&mut rs[j].r);if let Some((n,_,_,_))=rs[j].cur{heap.push(Reverse((n,j)))}}if a.weight==0{zero+=1}else{write_orbit_record(&mut w,key,a,os,ss);count+=1;sum+=a.weight;*sh.entry(ss as usize).or_default()+=1}}
    w.flush().unwrap();let mut f=w.into_inner().unwrap();f.seek(SeekFrom::Start(40)).unwrap();f.write_all(&zero.to_le_bytes()).unwrap();f.write_all(&count.to_le_bytes()).unwrap();f.seek(SeekFrom::Start(64)).unwrap();f.write_all(&sum.to_le_bytes()).unwrap();f.sync_all().unwrap();drop(f);rename(tmp,&out).unwrap();eprintln!("ORBIT_MERGE count={} zero={} elapsed={:.1}",count,zero,begun.elapsed().as_secs_f64());(out,count,zero,sum,sh)
}

fn add_child(map:&mut HashMap<Row,ChildAgg>,row:Row,a:ChildAgg){use std::collections::hash_map::Entry;match map.entry(row){Entry::Vacant(v)=>{v.insert(a);}Entry::Occupied(mut o)=>{assert_eq!(o.get().pivotable,a.pivotable);let x=o.get_mut();x.weight+=a.weight;if a.witness<x.witness{x.witness=a.witness}if x.weight==0{o.remove();}}}}
fn flush_child_chunk(index:usize,map:&mut HashMap<Row,ChildAgg>,start:u64,end:u64,generated:u64)->u64{let path=child_chunk_path(index);let mut v:Vec<_>=map.drain().collect();v.sort_unstable_by_key(|x|x.0);let count=v.len()as u64;let sum:i128=v.iter().map(|x|x.1.weight).sum();let tmp=format!("{}.tmp",path);let mut w=BufWriter::with_capacity(1<<20,File::create(&tmp).unwrap());put_pair_header(&mut w,b"H18CHC1\0",0,0,CHILD_REC as u16,start,end,count,generated,sum);for(r,a)in v{write_child_record(&mut w,r,a)}w.flush().unwrap();drop(w);rename(tmp,path).unwrap();count}
fn flush_child_chunk_named(path:&str,map:&mut HashMap<Row,ChildAgg>,start:u64,end:u64,generated:u64)->u64{let mut v:Vec<_>=map.drain().collect();v.sort_unstable_by_key(|x|x.0);let count=v.len()as u64;let sum:i128=v.iter().map(|x|x.1.weight).sum();let tmp=format!("{}.tmp",path);let mut w=BufWriter::with_capacity(1<<20,File::create(&tmp).unwrap());put_pair_header(&mut w,b"H18CHC1\0",0,0,CHILD_REC as u16,start,end,count,generated,sum);for(r,a)in v{write_child_record(&mut w,r,a)}w.flush().unwrap();drop(w);rename(tmp,path).unwrap();count}

fn build_child_chunks(pair_path:&str,pair_count:u64,begun:&Instant,e:&Engine)->(Vec<String>,u64){let mut r=BufReader::with_capacity(1<<20,File::open(pair_path).unwrap());let mut h=[0u8;PAIR_HEADER];r.read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"H16ORM1\0");let mut chunks=Vec::new();let mut map=HashMap::new();let mut cache=HashMap::new();let(mut index,mut chunk_start,mut generated)=(0u64,0u64,0u64);while let Some((key,a,os,ss))=read_orbit_record(&mut r){let m2=available(signature(&key.row.0,e),e).len();assert!(m2>0&&m2<256);for(ti,t)in e.all_k2[key.pivot as usize].iter().enumerate(){let child=replace_anchor(&key.row,&e.anchors[key.pivot as usize],t);let q=canonical(child,e,&mut cache);let ca=ChildAgg{weight:a.weight,witness:ChildWitness{pair:key,tail:ti as u8,pair_uses:a.uses,orbit_size:os,stabilizer:ss,m2:m2 as u8},pivotable:pivotable(&q,e)};add_child(&mut map,q,ca);generated+=1}index+=1;if index-chunk_start>=CHILD_CHUNK as u64{let ci=chunks.len();flush_child_chunk(ci,&mut map,chunk_start,index,generated-12*chunk_start);chunks.push(child_chunk_path(ci));chunk_start=index;eprintln!("CHILD_CHUNK {} pairs={}/{} elapsed={:.1}",ci,index,pair_count,begun.elapsed().as_secs_f64());if begun.elapsed().as_secs_f64()>GATE_SECONDS{panic!("600s gate during child generation")}}}if!map.is_empty(){let ci=chunks.len();flush_child_chunk(ci,&mut map,chunk_start,index,generated-12*chunk_start);chunks.push(child_chunk_path(ci))}assert_eq!(index,pair_count);eprintln!("CHILD_CHUNKS n={} generated={} elapsed={:.1}",chunks.len(),generated,begun.elapsed().as_secs_f64());(chunks,generated)}

fn build_child_chunks_parallel(pair_path:&str,pair_count:u64,begun:&Instant,e:Engine)->(Vec<String>,u64){let workers=8usize;let nchunks=((pair_count+CHILD_CHUNK as u64-1)/CHILD_CHUNK as u64)as usize;let e=Arc::new(e);let pair_path=Arc::new(pair_path.to_string());let mut jobs=Vec::new();for worker in 0..workers{let ee=e.clone();let pp=pair_path.clone();jobs.push(thread::spawn(move||{let mut out=Vec::new();let mut cache=HashMap::new();for ci in(worker..nchunks).step_by(workers){let start=ci as u64*CHILD_CHUNK as u64;let end=(start+CHILD_CHUNK as u64).min(pair_count);let path=parallel_child_chunk_path(ci);if metadata(&path).is_ok(){validate_child_chunk(&path,Some((start,end)));out.push(path);continue}let mut f=File::open(pp.as_str()).unwrap();f.seek(SeekFrom::Start(PAIR_HEADER as u64+ORBIT_REC as u64*start)).unwrap();let mut r=BufReader::with_capacity(1<<20,f);let mut map=HashMap::new();for _ in start..end{let(key,a,os,ss)=read_orbit_record(&mut r).unwrap();let m2=available(signature(&key.row.0,&ee),&ee).len();for(ti,t)in ee.all_k2[key.pivot as usize].iter().enumerate(){let child=replace_anchor(&key.row,&ee.anchors[key.pivot as usize],t);let q=canonical(child,&ee,&mut cache);add_child(&mut map,q,ChildAgg{weight:a.weight,witness:ChildWitness{pair:key,tail:ti as u8,pair_uses:a.uses,orbit_size:os,stabilizer:ss,m2:m2 as u8},pivotable:pivotable(&q,&ee)})}}flush_child_chunk_named(&path,&mut map,start,end,12*(end-start));validate_child_chunk(&path,Some((start,end)));eprintln!("PCHILD w={} chunk={} pairs={}..{}",worker,ci,start,end);out.push(path)}out}))}let mut paths=Vec::new();for j in jobs{paths.extend(j.join().unwrap())}paths.sort();assert_eq!(paths.len(),nchunks);let mut expected=0;for path in&paths{let m=validate_child_chunk(path,Some((expected,(expected+CHILD_CHUNK as u64).min(pair_count))));expected=m.end}assert_eq!(expected,pair_count);assert!(begun.elapsed().as_secs_f64()<=RESUME_GATE_SECONDS,"resume gate after parallel child stage");eprintln!("PARALLEL_CHILD_CHUNKS n={} generated={} elapsed={:.1}",paths.len(),12*pair_count,begun.elapsed().as_secs_f64());(paths,12*pair_count)}

fn open_final(path:&str,magic:&[u8;8],pair_count:u64,generated:u64,flag:u8)->(String,BufWriter<File>){let tmp=format!("{}.tmp",path);let mut w=BufWriter::with_capacity(1<<20,File::create(&tmp).unwrap());put_pair_header(&mut w,magic,0,0,CHILD_REC as u16,pair_count,generated,0,flag as u64,0);(tmp,w)}
fn merge_child_chunks(paths:&[String],pair_count:u64,generated:u64,begun:&Instant)->(u64,u64,u64,i128,i128,String,String){let mut rs=Vec::new();let mut heap=BinaryHeap::new();let mut expected=0u64;for(i,path)in paths.iter().enumerate(){let m=validate_child_chunk(path,Some((expected,(expected+CHILD_CHUNK as u64).min(pair_count))));expected=m.end;let mut r=BufReader::with_capacity(1<<20,File::open(path).unwrap());let mut h=[0u8;PAIR_HEADER];r.read_exact(&mut h).unwrap();let cur=read_child_record(&mut r);if let Some((k,_))=cur{heap.push(Reverse((k,i)))}rs.push(ChildReader{r,cur})}assert_eq!(expected,pair_count);
    let piv=format!("{}checkpoint_k18_22_pivotable.bin",FDIR);let irr=format!("{}checkpoint_k18_22_irreducible.bin",FDIR);let(ptmp,mut pw)=open_final(&piv,b"H18PIV2\0",pair_count,generated,1);let(itmp,mut iw)=open_final(&irr,b"H18IRR2\0",pair_count,generated,0);let(mut pc,mut ic,mut zero,mut ps,mut is)=(0u64,0u64,0u64,0i128,0i128);
    while let Some(Reverse((row,i)))=heap.pop(){let(_,mut a)=rs[i].cur.unwrap();rs[i].cur=read_child_record(&mut rs[i].r);if let Some((k,_))=rs[i].cur{heap.push(Reverse((k,i)))}while let Some(Reverse((k,j)))=heap.peek().copied(){if k!=row{break}heap.pop();let(_,b)=rs[j].cur.unwrap();assert_eq!(a.pivotable,b.pivotable);a.weight+=b.weight;if b.witness<a.witness{a.witness=b.witness}rs[j].cur=read_child_record(&mut rs[j].r);if let Some((n,_))=rs[j].cur{heap.push(Reverse((n,j)))}}if a.weight==0{zero+=1}else if a.pivotable{write_child_record(&mut pw,row,a);pc+=1;ps+=a.weight}else{write_child_record(&mut iw,row,a);ic+=1;is+=a.weight}}
    for(w,tmp,path,count,sum)in[(pw,ptmp,piv.clone(),pc,ps),(iw,itmp,irr.clone(),ic,is)]{let mut f=w.into_inner().unwrap();f.seek(SeekFrom::Start(48)).unwrap();f.write_all(&count.to_le_bytes()).unwrap();f.seek(SeekFrom::Start(64)).unwrap();f.write_all(&sum.to_le_bytes()).unwrap();f.sync_all().unwrap();drop(f);rename(tmp,path).unwrap()}eprintln!("CHILD_MERGE pivotable={} irreducible={} zero={} elapsed={:.1}",pc,ic,zero,begun.elapsed().as_secs_f64());(pc,ic,zero,ps,is,piv,irr)}

fn prefix_guard(){let s=std::fs::read_to_string(format!("{}results_hidden_k16_pair_orbits.json",NEW_ODIR)).unwrap();assert!(s.contains("PASS_EXACT_DECORATED_PAIR_ORBIT_PREFIX"));assert!(s.contains("\"reference_mismatches\": 0"));assert!(s.contains("\"decorated_pair_H_orbits_nonzero\": 261696"));let b=read(format!("{}decorated_pair_orbits_prefix.bin",NEW_ODIR)).unwrap();assert_eq!(&b[..8],b"H16PORB1");assert_eq!(u64::from_le_bytes(b[32..40].try_into().unwrap()),261696);}

#[cfg(not(feature="resume_safety_test"))]
fn main(){std::fs::create_dir_all(FDIR).unwrap();let args:Vec<_>=std::env::args().collect();if args.len()==2&&args[1]=="--cleanup-refereed-child-chunks"{cleanup_refereed_child_chunks(REFEREE_MARKER);return}assert_eq!(args.len(),1,"only --cleanup-refereed-child-chunks is accepted");let begun=Instant::now();prefix_guard();let e=parse();let mut run_paths=Vec::new();let(mut parents,mut outgoing,mut run_pairs,mut input_sum)=(0u64,0u64,0u64,0i128);for start in(0..485usize).step_by(16){let end=(start+16).min(485);let(a,b,c,d)=make_exact_run(start,end,&begun,&e);parents+=a;outgoing+=b;run_pairs+=c;input_sum+=d;run_paths.push(exact_run_path(start,end));}
    let pair_path=format!("{}hidden_k16_decorated_pair_orbits_full.bin",FDIR);let(exact_distinct,exact_zero,pair_count,orbit_zero,pair_sum)=if metadata(&pair_path).is_ok(){let mut r=BufReader::new(File::open(&pair_path).unwrap());let mut h=[0u8;PAIR_HEADER];r.read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"H16ORM1\0");let zero=u64::from_le_bytes(h[40..48].try_into().unwrap());let count=u64::from_le_bytes(h[48..56].try_into().unwrap());let sum=i128::from_le_bytes(h[64..80].try_into().unwrap());assert_eq!(metadata(&pair_path).unwrap().len(),PAIR_HEADER as u64+ORBIT_REC as u64*count);(126_420_124,52,count,zero,sum)}else{let pp=pivot_permutations(&e);let(chunks,ed,ez,merged_sum,_)=build_orbit_chunks(&run_paths,&begun,&e,&pp);assert_eq!(input_sum,merged_sum);let(p,pc,oz,ps,_)=merge_orbit_chunks(&chunks,&begun);assert_eq!(p,pair_path);for x in&chunks{remove_file(x).unwrap()}(ed,ez,pc,oz,ps)};assert_eq!(pair_sum,input_sum);
    let stab_hist=scan_pair_stabilizers(&pair_path,pair_count,pair_sum);assert_stabilizer_histogram(&stab_hist,pair_count);let(child_chunks,generated)=build_child_chunks_parallel(&pair_path,pair_count,&begun,e);let(pc,ic,child_zero,ps,is,piv,irr)=merge_child_chunks(&child_chunks,pair_count,generated,&begun);assert_eq!(ps+is,12*pair_sum);assert!(child_chunks.iter().all(|p|metadata(p).is_ok()),"merge must retain every child chunk for independent referee");assert!(begun.elapsed().as_secs_f64()<=RESUME_GATE_SECONDS);
    let result=format!("{{\n  \"status\": \"PASS_FULL_ORBIT_AWARE_K18_22_COLLECTION\",\n  \"scope\": \"full hidden K16 K2 collection only; no K20 tails\",\n  \"scale\": \"{}\",\n  \"atomic_parent_runs\": {},\n  \"parent_occurrences\": {},\n  \"labelled_second_pivot_uses\": {},\n  \"run_exact_pair_records\": {},\n  \"global_exact_pair_keys_before_zero\": {},\n  \"global_exact_pair_zero_keys\": {},\n  \"decorated_pair_H_orbits_nonzero\": {},\n  \"decorated_pair_orbit_zero_keys\": {},\n  \"pair_weight_sum_scaled\": \"{}\",\n  \"stabilizer_histogram\": \"{:?}\",\n  \"generated_K2_children\": {},\n  \"K18_pivotable_support\": {},\n  \"K18_irreducible_support\": {},\n  \"K18_cross_chunk_exact_zero_rows\": {},\n  \"pivotable_weight_sum_scaled\": \"{}\",\n  \"irreducible_weight_sum_scaled\": \"{}\",\n  \"total_K18_weight_sum_scaled\": \"{}\",\n  \"pair_checkpoint\": \"{}\",\n  \"pivotable_checkpoint\": \"{}\",\n  \"irreducible_checkpoint\": \"{}\",\n  \"record_schema\": \"row24,weight_i128,witness_pair_row24,witness_p2,witness_tail2,pair_uses_u64,orbit_u16,stabilizer_u16,pivotable_u8,m2_u8\",\n  \"prefix_guard\": \"261696 pair orbits / 694172 child rows / zero mismatches\",\n  \"elapsed_seconds\": {:.6}\n}}\n",U,run_paths.len(),parents,outgoing,run_pairs,exact_distinct,exact_zero,pair_count,orbit_zero,pair_sum,stab_hist,generated,pc,ic,child_zero,ps,is,ps+is,pair_path,piv,irr,begun.elapsed().as_secs_f64());std::fs::write(format!("{}results_full_hidden_k16_k2_orbits.json",FDIR),&result).unwrap();print!("{}",result)}

#[cfg(feature="resume_safety_test")]
fn main(){
    let pair_path=format!("{}hidden_k16_decorated_pair_orbits_full.bin",FDIR);let mut r=BufReader::new(File::open(&pair_path).unwrap());let mut h=[0u8;PAIR_HEADER];r.read_exact(&mut h).unwrap();let pair_count=u64::from_le_bytes(h[48..56].try_into().unwrap());let pair_sum=i128::from_le_bytes(h[64..80].try_into().unwrap());
    let hist=scan_pair_stabilizers(&pair_path,pair_count,pair_sum);assert_stabilizer_histogram(&hist,pair_count);
    let nchunks=((pair_count+CHILD_CHUNK as u64-1)/CHILD_CHUNK as u64)as usize;let mut expected=0u64;for ci in 0..nchunks{let end=(expected+CHILD_CHUNK as u64).min(pair_count);let path=parallel_child_chunk_path(ci);let m=validate_child_chunk(&path,Some((expected,end)));expected=m.end}assert_eq!(expected,pair_count);
    let old_hook=std::panic::take_hook();std::panic::set_hook(Box::new(|_|{}));
    let src=parallel_child_chunk_path(nchunks-1);let bad=format!("{}hostile_truncated_child.tmp",FDIR);std::fs::copy(&src,&bad).unwrap();let n=metadata(&bad).unwrap().len();std::fs::OpenOptions::new().write(true).open(&bad).unwrap().set_len(n-1).unwrap();let truncation_failed=std::panic::catch_unwind(||validate_child_chunk(&bad,None)).is_err();remove_file(&bad).unwrap();assert!(truncation_failed);
    let empty=BTreeMap::new();let histogram_reset_failed=std::panic::catch_unwind(||assert_stabilizer_histogram(&empty,pair_count)).is_err();assert!(histogram_reset_failed);
    let before=(0..nchunks).filter(|&ci|metadata(parallel_child_chunk_path(ci)).is_ok()).count();let eager_cleanup_failed=std::panic::catch_unwind(||cleanup_refereed_child_chunks(&format!("{}hostile_missing_referee_marker.json",FDIR))).is_err();let after=(0..nchunks).filter(|&ci|metadata(parallel_child_chunk_path(ci)).is_ok()).count();assert!(eager_cleanup_failed);assert_eq!((before,after),(nchunks,nchunks));std::panic::set_hook(old_hook);
    let text=format!("{{\n  \"status\": \"PASS_RESUME_SAFETY_GUARDS\",\n  \"chunks\": {},\n  \"pair_count\": {},\n  \"stabilizer_histogram\": \"{:?}\",\n  \"hostile_truncation_failed\": {},\n  \"hostile_histogram_reset_failed\": {},\n  \"hostile_eager_cleanup_failed\": {},\n  \"retained_chunks_after_cleanup_hostile\": {},\n  \"cleanup_policy\": \"explicit --cleanup-refereed-child-chunks requires final checkpoints plus independent PASS marker\",\n  \"child_content_hash_scope\": \"no stored per-chunk content digests; full header/interval/schema/size guards only until merge streams every record\"\n}}\n",nchunks,pair_count,hist,truncation_failed,histogram_reset_failed,eager_cleanup_failed,after);std::fs::write(format!("{}results_resume_safety.json",FDIR),&text).unwrap();print!("{}",text)
}
