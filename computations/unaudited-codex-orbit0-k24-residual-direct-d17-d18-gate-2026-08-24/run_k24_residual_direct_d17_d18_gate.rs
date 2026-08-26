//! Prefix-only, residual-preserving K24 fold for direct D17 R3-4 / D18 R2-4.
//!
//! Raw labelled rows are exact-collected first, then H-canonicalized into
//! sorted binary runs, and finally exact-merged to the sealed TSV interface.
//! The program deliberately refuses every source count except 1, 8, or 61.
#![allow(dead_code)]
mod fold {
include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

use std::cmp::Reverse;
use std::collections::{BTreeMap, BinaryHeap};
use std::fs::{create_dir_all, read_dir, File};
use std::io::{self, BufReader, BufWriter, ErrorKind, Read, Write};
use std::path::{Path, PathBuf};

const U24:i128=400_591_699_200;
const SLICES:usize=485;
const RAW_BUFFER_TOTAL:usize=2_000_000;
const CANON_BUFFER:usize=100_000;
const MERGE_FANIN:usize=96;
const INPUT_STRUCTURE_SHA:&str="55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b";
const INPUT_AUX_SHA:&str="f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab";
const INPUT_K4_SHA:&str="4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3";
const INPUT_CYCLE_SHA:&str="8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7";
const IDS17:[&str;7]=["D17:234|R:3-4","D17:243|R:3-4","D17:324|R:3-4","D17:333|R:3-4","D17:342|R:3-4","D17:423|R:3-4","D17:432|R:3-4"];
const IDS18:[&str;6]=["D18:244|R:2-4","D18:334|R:2-4","D18:343|R:2-4","D18:424|R:2-4","D18:433|R:2-4","D18:442|R:2-4"];
const GIDS:[&str;2]=["source_D17_R3_4","source_D18_R2_4"];

#[derive(Clone)]struct HMaps(Vec<[u8;252]>);
fn full_h_maps()->HMaps{
    let b=read(format!("{}filtered_k16_structure.bin",DIR)).unwrap();
    let mut p=11;
    let nt=u32le(&b[p..p+4])as usize;p+=4;
    let nr=u32le(&b[p..p+4])as usize;p+=4;
    let np=u32le(&b[p..p+4])as usize;p+=4;
    let na=u32le(&b[p..p+4])as usize;p+=4;
    assert_eq!((nt,nr,np,na),(384,485,78,12));p+=12;
    let mut maps=Vec::with_capacity(nt);
    for _ in 0..nt{let mut m=[0u8;252];m.copy_from_slice(&b[p..p+252]);p+=252;p+=12;maps.push(m)}
    HMaps(maps)
}
fn moved(row:Row,map:&[u8;252])->Row{let mut x=[0u8;24];for(i,&c)in row.0.iter().enumerate(){x[i]=map[c as usize]}x.sort_unstable();Row(x)}
fn hx(row:&Row)->String{row.0.iter().map(|x|format!("{:02x}",x)).collect()}
fn canon(row:Row,h:&HMaps)->(Row,u16,u16){let mut best=row;let mut witness=0u16;let mut stabilizer=0u16;for(i,m)in h.0.iter().enumerate(){let x=moved(row,m);if x==row{stabilizer+=1}if x<best{best=x;witness=i as u16}}assert!(stabilizer>0&&384%stabilizer==0);(best,384/stabilizer,witness)}

fn put_raw(w:&mut BufWriter<File>,row:Row,mass:i128){w.write_all(&row.0).unwrap();w.write_all(&mass.to_le_bytes()).unwrap()}
fn get_raw(r:&mut BufReader<File>)->io::Result<Option<(Row,i128)>>{let mut x=[0u8;24];match r.read_exact(&mut x){Ok(())=>{},Err(e)if e.kind()==ErrorKind::UnexpectedEof=>return Ok(None),Err(e)=>return Err(e)}let mut m=[0u8;16];r.read_exact(&mut m)?;Ok(Some((Row(x),i128::from_le_bytes(m))))}
fn put_canon(w:&mut BufWriter<File>,row:Row,orbit:u16,mass:i128){w.write_all(&row.0).unwrap();w.write_all(&orbit.to_le_bytes()).unwrap();w.write_all(&mass.to_le_bytes()).unwrap()}
fn get_canon(r:&mut BufReader<File>)->io::Result<Option<(Row,u16,i128)>>{let mut x=[0u8;24];match r.read_exact(&mut x){Ok(())=>{},Err(e)if e.kind()==ErrorKind::UnexpectedEof=>return Ok(None),Err(e)=>return Err(e)}let mut o=[0u8;2];let mut m=[0u8;16];r.read_exact(&mut o)?;r.read_exact(&mut m)?;Ok(Some((Row(x),u16::from_le_bytes(o),i128::from_le_bytes(m))))}

struct RawWriter{group:usize,worker:usize,root:PathBuf,buckets:Vec<HashMap<Row,i128>>,runs:[usize;8],entries:usize,emitted:u64}
impl RawWriter{
 fn new(group:usize,worker:usize,root:&Path)->Self{Self{group,worker,root:root.to_path_buf(),buckets:(0..8).map(|_|HashMap::new()).collect(),runs:[0;8],entries:0,emitted:0}}
 fn add(&mut self,row:Row,mass:i128){let b=(row.0[0]as usize)%8;match self.buckets[b].entry(row){std::collections::hash_map::Entry::Occupied(mut x)=>*x.get_mut()+=mass,std::collections::hash_map::Entry::Vacant(x)=>{x.insert(mass);self.entries+=1}}self.emitted+=1;if self.entries>=RAW_BUFFER_TOTAL{let bucket=(0..8).max_by_key(|&i|self.buckets[i].len()).unwrap();self.flush(bucket)}}
 fn flush(&mut self,b:usize){if self.buckets[b].is_empty(){return}let drained=self.buckets[b].len();let mut rows:Vec<_>=self.buckets[b].drain().filter(|x|x.1!=0).collect();self.entries-=drained;rows.sort_unstable_by_key(|x|x.0);let dir=self.root.join(format!("raw/{}/b{}",GIDS[self.group],b));create_dir_all(&dir).unwrap();let path=dir.join(format!("w{:02}.r{:05}.bin",self.worker,self.runs[b]));self.runs[b]+=1;let mut out=BufWriter::new(File::create(path).unwrap());for(row,mass)in rows{put_raw(&mut out,row,mass)}out.flush().unwrap()}
 fn finish(mut self)->(u64,usize){for b in 0..8{self.flush(b)}(self.emitted,self.runs.iter().sum())}
}

#[derive(Clone,Copy,Default)]struct Q{heads:u64,pivotable:u64,p1:u64,mid:u64,pivmid:u64,p2:u64,terminal:u64,raw_runs:u64}
impl Q{fn add(&mut self,x:Q){self.heads+=x.heads;self.pivotable+=x.pivotable;self.p1+=x.p1;self.mid+=x.mid;self.pivmid+=x.pivmid;self.p2+=x.p2;self.terminal+=x.terminal;self.raw_runs+=x.raw_runs}}
struct WorkerOut{q:[Q;2],witnesses:Vec<String>}

#[allow(clippy::too_many_arguments)]
fn emit_path(row:Row,group:usize,lineage:&str,mass:i128,firstd:usize,source_cursor:&str,e:&E,h:&HMaps,out:&mut RawWriter,q:&mut Q,witness:&mut Option<String>){
 q.heads+=1;let s1=sig(&row,e);let ps1=avail(s1,e);if ps1.is_empty(){return}q.pivotable+=1;let m1=ps1.len();q.p1+=m1 as u64;
 for p1 in ps1{for(t1i,t1)in e.tails[p1][firstd-2].iter().enumerate(){q.mid+=1;let s2=child_sig(s1,p1,t1,e);let ps2=avail(s2,e);if ps2.is_empty(){continue}q.pivmid+=1;let m2=ps2.len();q.p2+=m2 as u64;assert_eq!(U24%((m1*m2)as i128),0);let scaled=-mass*(U24/((m1*m2)as i128));let r2=replace(&row,&e.anchors[p1],t1);assert_eq!(sig(&r2,e),s2);
   for p2 in ps2{for(t2i,t2)in e.tails[p2][2].iter().enumerate(){let r3=replace(&r2,&e.anchors[p2],t2);assert!(avail(sig(&r3,e),e).is_empty());out.add(r3,scaled);q.terminal+=1;if witness.is_none(){let(c,os,act)=canon(r3,h);let d=gcd(scaled,U24);*witness=Some(format!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\taction_index={}\t{}/{}",GIDS[group],lineage,source_cursor,p1,t1i,p2,t2i,m1,m2,hx(&row),hx(&r2),hx(&r3),hx(&c),os,act,scaled/d,U24/d))}}}
 }}
}

fn worker(e:Arc<E>,h:Arc<HMaps>,start:usize,end:usize,wi:usize,nw:usize,root:PathBuf)->WorkerOut{
 let mut q=[Q::default();2];let mut witnesses=Vec::new();let mut w17=RawWriter::new(0,wi,&root);let mut w18=RawWriter::new(1,wi,&root);
 for ri in(start+wi..end).step_by(nw){let r=&e.records[ri];let mass=(r.size as i128)*(r.coefficient as i128);let mut witness17=None;let mut witness18=None;
  // Direct K17: the six permutations of 2+3+4, then 3+3+3.  Respond K3,K4.
  let specs=[(0usize,0usize,1usize,2usize),(1,0,2,1),(2,1,0,2),(4,1,2,0),(5,2,0,1),(6,2,1,0)];
  for &(sector,d2,d3,d4)in &specs{for(ai,a)in e.factor[d2][0].iter().enumerate(){for(bi,b)in e.factor[d3][1].iter().enumerate(){for(ci,c)in e.factor[d4][2].iter().enumerate(){let mut f:[Option<&[u8;4]>;3]=[None,None,None];f[d2]=Some(a);f[d3]=Some(b);f[d4]=Some(c);let z=[f[0].unwrap(),f[1].unwrap(),f[2].unwrap()];let row=make(r,z[0],z[1],z[2]);let cur=format!("r8={};sector={};factor_ordinals={},{},{}",ri,sector,ai,bi,ci);emit_path(row,0,IDS17[sector],mass,3,&cur,&e,&h,&mut w17,&mut q[0],&mut witness17)}}}}
  for(ai,a)in e.factor[0][1].iter().enumerate(){for(bi,b)in e.factor[1][1].iter().enumerate(){for(ci,c)in e.factor[2][1].iter().enumerate(){let row=make(r,a,b,c);let cur=format!("r8={};sector=3;factor_ordinals={},{},{}",ri,ai,bi,ci);emit_path(row,0,IDS17[3],mass,3,&cur,&e,&h,&mut w17,&mut q[0],&mut witness17)}}}
  // Direct K18: 2+4+4 and 3+3+4.  Respond K2,K4.
  for low in 0..3{let sector=[0usize,3,5][low];let o:Vec<_>=(0..3).filter(|&x|x!=low).collect();for(ai,a)in e.factor[low][0].iter().enumerate(){for(bi,b)in e.factor[o[0]][2].iter().enumerate(){for(ci,c)in e.factor[o[1]][2].iter().enumerate(){let row=match low{0=>make(r,a,b,c),1=>make(r,b,a,c),_=>make(r,b,c,a)};let cur=format!("r8={};sector={};factor_ordinals={},{},{}",ri,sector,ai,bi,ci);emit_path(row,1,IDS18[sector],mass,2,&cur,&e,&h,&mut w18,&mut q[1],&mut witness18)}}}}
  for high in 0..3{let sector=[4usize,2,1][high];let o:Vec<_>=(0..3).filter(|&x|x!=high).collect();for(ai,a)in e.factor[o[0]][1].iter().enumerate(){for(bi,b)in e.factor[o[1]][1].iter().enumerate(){for(ci,c)in e.factor[high][2].iter().enumerate(){let row=match high{0=>make(r,c,a,b),1=>make(r,a,c,b),_=>make(r,a,b,c)};let cur=format!("r8={};sector={};factor_ordinals={},{},{}",ri,sector,ai,bi,ci);emit_path(row,1,IDS18[sector],mass,2,&cur,&e,&h,&mut w18,&mut q[1],&mut witness18)}}}}
  witnesses.push(witness17.unwrap_or_else(||panic!("no D17 witness slice {}",ri)));witnesses.push(witness18.unwrap_or_else(||panic!("no D18 witness slice {}",ri)));
 }
 let(a,r17)=w17.finish();let(b,r18)=w18.finish();assert_eq!(a,q[0].terminal);assert_eq!(b,q[1].terminal);q[0].raw_runs=r17 as u64;q[1].raw_runs=r18 as u64;WorkerOut{q,witnesses}
}

struct CanonWriter{group:usize,bucket:usize,batch:usize,root:PathBuf,map:HashMap<Row,(i128,u16)>,run:usize}
impl CanonWriter{
 fn new(group:usize,bucket:usize,batch:usize,root:&Path)->Self{Self{group,bucket,batch,root:root.to_path_buf(),map:HashMap::new(),run:0}}
 fn add(&mut self,row:Row,orbit:u16,mass:i128){let x=self.map.entry(row).or_insert((0,orbit));assert_eq!(x.1,orbit);x.0+=mass;if self.map.len()>=CANON_BUFFER{self.flush()}}
 fn flush(&mut self){if self.map.is_empty(){return}let mut rows:Vec<_>=self.map.drain().filter(|x|x.1.0!=0).collect();rows.sort_unstable_by_key(|x|x.0);let dir=self.root.join(format!("canonical/{}/b{}",GIDS[self.group],self.bucket));create_dir_all(&dir).unwrap();let path=dir.join(format!("batch{:03}.r{:05}.bin",self.batch,self.run));self.run+=1;let mut out=BufWriter::new(File::create(path).unwrap());for(row,(mass,orbit))in rows{put_canon(&mut out,row,orbit,mass)}out.flush().unwrap()}
 fn finish(mut self)->usize{self.flush();self.run}
}

fn files_in(path:&Path)->Vec<PathBuf>{if !path.exists(){return Vec::new()}let mut x:Vec<_>=read_dir(path).unwrap().map(|e|e.unwrap().path()).filter(|p|p.extension().and_then(|x|x.to_str())==Some("bin")).collect();x.sort();x}
#[derive(Default,Clone,Copy)]struct MergeStat{raw_records:u64,raw_nonzero:u64,raw_zero:u64,canonical_runs:u64,raw_charge:i128,raw_mass:i128,canon_checks:u64}
impl MergeStat{fn add(&mut self,x:MergeStat){self.raw_records+=x.raw_records;self.raw_nonzero+=x.raw_nonzero;self.raw_zero+=x.raw_zero;self.canonical_runs+=x.canonical_runs;self.raw_charge+=x.raw_charge;self.raw_mass+=x.raw_mass;self.canon_checks+=x.canon_checks}}
fn canonicalize_batch(paths:&[PathBuf],group:usize,bucket:usize,batch:usize,e:&E,h:&HMaps,root:&Path)->MergeStat{
 let mut readers:Vec<_>=paths.iter().map(|p|BufReader::new(File::open(p).unwrap())).collect();let mut heap:BinaryHeap<Reverse<(Row,usize,i128)>>=BinaryHeap::new();for(i,r)in readers.iter_mut().enumerate(){if let Some((row,mass))=get_raw(r).unwrap(){heap.push(Reverse((row,i,mass)))}}
 let mut out=CanonWriter::new(group,bucket,batch,root);let mut z=MergeStat::default();
 while let Some(Reverse((row,i,mass)))=heap.pop(){let mut total=mass;z.raw_records+=1;if let Some(x)=get_raw(&mut readers[i]).unwrap(){heap.push(Reverse((x.0,i,x.1)))}while heap.peek().map(|x|x.0.0==row).unwrap_or(false){let Reverse((_r,j,m))=heap.pop().unwrap();total+=m;z.raw_records+=1;if let Some(x)=get_raw(&mut readers[j]).unwrap(){heap.push(Reverse((x.0,j,x.1)))} }if total==0{z.raw_zero+=1;continue}z.raw_nonzero+=1;let(c,orbit,_)=canon(row,h);assert_eq!(charge(&row,e),charge(&c,e));z.canon_checks+=1;z.raw_charge+=total*(charge(&row,e)as i128);z.raw_mass+=total;out.add(c,orbit,total)}
 z.canonical_runs=out.finish()as u64;z
}

fn compact_canon(paths:&[PathBuf],output:&Path)->(u64,u64){let mut readers:Vec<_>=paths.iter().map(|p|BufReader::new(File::open(p).unwrap())).collect();let mut heap:BinaryHeap<Reverse<(Row,usize,u16,i128)>>=BinaryHeap::new();for(i,r)in readers.iter_mut().enumerate(){if let Some((row,o,m))=get_canon(r).unwrap(){heap.push(Reverse((row,i,o,m)))}}let mut out=BufWriter::new(File::create(output).unwrap());let(mut kept,mut zeros)=(0u64,0u64);while let Some(Reverse((row,i,o,m)))=heap.pop(){let(mut total,orbit)=(m,o);if let Some(x)=get_canon(&mut readers[i]).unwrap(){heap.push(Reverse((x.0,i,x.1,x.2)))}while heap.peek().map(|x|x.0.0==row).unwrap_or(false){let Reverse((_r,j,oo,mm))=heap.pop().unwrap();assert_eq!(orbit,oo);total+=mm;if let Some(x)=get_canon(&mut readers[j]).unwrap(){heap.push(Reverse((x.0,j,x.1,x.2)))}}if total==0{zeros+=1}else{put_canon(&mut out,row,orbit,total);kept+=1}}out.flush().unwrap();(kept,zeros)}
fn gcd(mut a:i128,mut b:i128)->i128{a=a.abs();b=b.abs();while b!=0{let r=a%b;a=b;b=r}a}
#[derive(Default)]struct FinalStat{rows:u64,zeros:u64,mass:i128,charge:i128,orbit_hist:BTreeMap<u16,u64>,tsv_bytes:u64}
fn final_tsv(group:usize,mut paths:Vec<PathBuf>,e:&E,root:&Path)->FinalStat{
 let compact=root.join(format!("compact/{}",GIDS[group]));create_dir_all(&compact).unwrap();let mut pass=0;while paths.len()>MERGE_FANIN{let mut next=Vec::new();for(i,chunk)in paths.chunks(MERGE_FANIN).enumerate(){let p=compact.join(format!("pass{:02}.chunk{:04}.bin",pass,i));compact_canon(chunk,&p);next.push(p)}paths=next;pass+=1}
 let merged=compact.join("final.bin");compact_canon(&paths,&merged);let tsv=root.join(format!("{}.rows.tsv",GIDS[group]));let mut input=BufReader::new(File::open(&merged).unwrap());let mut output=BufWriter::new(File::create(&tsv).unwrap());let mut z=FinalStat::default();while let Some((row,orbit,mass))=get_canon(&mut input).unwrap(){assert_ne!(mass,0);let d=gcd(mass,U24);let num=mass/d;let den=U24/d;let line=format!("{}\t{}\t{}\t{}\n",hx(&row),orbit,num,den);output.write_all(line.as_bytes()).unwrap();z.tsv_bytes+=line.len()as u64;z.rows+=1;z.mass+=mass;z.charge+=mass*(charge(&row,e)as i128);*z.orbit_hist.entry(orbit).or_default()+=1}output.flush().unwrap();z
}
fn ids(v:&[&str])->String{v.iter().map(|x|format!("\"{}\"",x)).collect::<Vec<_>>().join(",")}
fn hist(v:&BTreeMap<u16,u64>)->String{v.iter().map(|(x,n)|format!("\"{}\":{}",x,n)).collect::<Vec<_>>().join(",")}

pub fn run(){
 let args:Vec<_>=std::env::args().collect();let(mut start,mut count,mut workers)=(0usize,1usize,1usize);let mut root=PathBuf::new();let mut engine_sha=String::new();let mut i=1;while i<args.len(){match args[i].as_str(){"--start-slice"=>{start=args[i+1].parse().unwrap();i+=2},"--count-slices"=>{count=args[i+1].parse().unwrap();i+=2},"--workers"=>{workers=args[i+1].parse().unwrap();i+=2},"--output-dir"=>{root=PathBuf::from(&args[i+1]);i+=2},"--engine-sha256"=>{engine_sha=args[i+1].clone();i+=2},_=>panic!("bad arg {}",args[i])}}
 assert!(start==0&&[1usize,8,61].contains(&count));assert!((1..=8).contains(&workers));assert!(!root.as_os_str().is_empty());assert_eq!(engine_sha.len(),64);create_dir_all(&root).unwrap();let begun=Instant::now();let e=Arc::new(parse());let h=Arc::new(full_h_maps());assert_eq!(e.records.len(),SLICES);let active=workers.min(count);let stage1=Instant::now();let mut jobs=Vec::new();for w in 0..active{let ee=e.clone();let hh=h.clone();let rr=root.clone();jobs.push(thread::spawn(move||worker(ee,hh,start,start+count,w,active,rr)))}let mut q=[Q::default();2];let mut witness=Vec::new();for j in jobs{let x=j.join().unwrap();for g in 0..2{q[g].add(x.q[g])}witness.extend(x.witnesses)}let stage1_sec=stage1.elapsed().as_secs_f64();
 let wt=root.join("literal_witnesses.tsv");let mut lines=vec!["group_id\tlineage_id\tsource_cursor\tp1\tt1\tp2\tt2\tm1\tm2\tsource_row\tintermediate_row\tliteral_K24_row\tH_canonical_row\torbit_size\tH_action_or_witness\texact_signed_fraction".to_string()];witness.sort();lines.extend(witness);std::fs::write(&wt,format!("{}\n",lines.join("\n"))).unwrap();
 let stage2=Instant::now();let mut merges=[MergeStat::default();2];for g in 0..2{for b in 0..8{let paths=files_in(&root.join(format!("raw/{}/b{}",GIDS[g],b)));for(batch,chunk)in paths.chunks(MERGE_FANIN).enumerate(){let z=canonicalize_batch(chunk,g,b,batch,&e,&h,&root);merges[g].add(z)}}}let stage2_sec=stage2.elapsed().as_secs_f64();
 let stage3=Instant::now();let mut finals=[FinalStat::default(),FinalStat::default()];for g in 0..2{let mut paths=Vec::new();for b in 0..8{paths.extend(files_in(&root.join(format!("canonical/{}/b{}",GIDS[g],b))))}finals[g]=final_tsv(g,paths,&e,&root);assert_eq!(finals[g].charge,merges[g].raw_charge);assert_eq!(finals[g].mass,merges[g].raw_mass)}let stage3_sec=stage3.elapsed().as_secs_f64();let elapsed=begun.elapsed().as_secs_f64();let projected=elapsed*SLICES as f64/count as f64;
 let groups=(0..2).map(|g|{let group_ids=if g==0{ids(&IDS17)}else{ids(&IDS18)};format!("    {{\"group_id\":\"{}\",\"ids\":[{}],\"source_heads\":{},\"pivotable_source_heads\":{},\"p1_uses\":{},\"intermediate_children\":{},\"pivotable_intermediate_children\":{},\"p2_uses\":{},\"K24_terminal_occurrences\":{},\"raw_sorted_runs\":{},\"raw_merged_records\":{},\"raw_nonzero_rows_before_H_collection\":{},\"raw_exact_zero_cancellations\":{},\"H_canonical_sorted_runs\":{},\"nonzero_H_row_orbits\":{},\"orbit_size_histogram\":{{{}}},\"orbit_mass_scaled_U_sum\":\"{}\",\"derived_charge_scaled_U\":\"{}\",\"derived_charge\":\"{}/{}\",\"row_tsv\":\"{}.rows.tsv\",\"row_tsv_bytes\":{}}}",GIDS[g],group_ids,q[g].heads,q[g].pivotable,q[g].p1,q[g].mid,q[g].pivmid,q[g].p2,q[g].terminal,q[g].raw_runs,merges[g].raw_records,merges[g].raw_nonzero,merges[g].raw_zero,merges[g].canonical_runs,finals[g].rows,hist(&finals[g].orbit_hist),finals[g].mass,finals[g].charge,finals[g].charge,U24,GIDS[g],finals[g].tsv_bytes)}).collect::<Vec<_>>().join(",\n");
 let text=format!("{{\n  \"status\":\"PASS_BOUNDED_K24_RESIDUAL_DIRECT_D17_D18_PREFIX\",\n  \"schema\":\"literal-k24-h-row-orbit-residual-v1\",\n  \"degree\":24,\n  \"complete_35_id_coverage\":false,\n  \"covered_lineage_ids\":[{} , {}],\n  \"strict_scalar_groups\":2,\n  \"source_interval\":[{},{}],\n  \"source_slices\":{},\n  \"workers\":{},\n  \"scale_U\":{},\n  \"recurrence_policy\":\"all_literal_dividing_pivots_occurrencewise_average_v1\",\n  \"canonicalization_policy\":\"sorted_24_cell_row_then_minimum_under_frozen_H_v1\",\n  \"groups\":[\n{}\n  ],\n  \"literal_witnesses\":{},\n  \"literal_witness_ledger\":\"literal_witnesses.tsv\",\n  \"input_sha256\":{{\"orbit0_structure\":\"{}\",\"response_aux\":\"{}\",\"response_k4\":\"{}\",\"cycle_aux\":\"{}\"}},\n  \"engine_sha256\":\"{}\",\n  \"exact_external_merge\":true,\n  \"raw_sorted_runs_retained\":true,\n  \"canonical_sorted_runs_retained\":true,\n  \"charge_is_derived_from_exact_merged_rows\":true,\n  \"row_charge_equals_raw_labelled_charge\":true,\n  \"all_K24_children_anchor_mass_zero_and_terminal\":true,\n  \"timings_seconds\":{{\"source_emit\":{:.6},\"raw_merge_and_H_canonicalize\":{:.6},\"canonical_merge_and_tsv\":{:.6},\"total\":{:.6}}},\n  \"linear_projected_full_seconds\":{:.6},\n  \"scope\":\"prefix gate for exactly D17 R3-4 and D18 R2-4; no full K24 production, no other lineage, no terminal-span claim\"\n}}\n",ids(&IDS17),ids(&IDS18),start,start+count,count,active,U24,groups,lines.len()-1,INPUT_STRUCTURE_SHA,INPUT_AUX_SHA,INPUT_K4_SHA,INPUT_CYCLE_SHA,engine_sha,stage1_sec,stage2_sec,stage3_sec,elapsed,projected);std::fs::write(root.join("result.json.tmp"),&text).unwrap();std::fs::rename(root.join("result.json.tmp"),root.join("result.json")).unwrap();print!("{}",text)
}
}
fn main(){fold::run()}
