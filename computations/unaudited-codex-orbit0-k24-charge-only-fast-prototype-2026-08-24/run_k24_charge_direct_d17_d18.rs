//! Exact charge-only K24 fold for direct D17 R3-4 and D18 R2-4.
#![allow(dead_code)]
mod fold {
include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
use std::collections::BTreeMap;
use std::fs::rename;
use std::sync::Mutex;

const U:i128=400_591_699_200;
const SLICES:usize=485;
const MAX_FIRST_KEYS_PER_R8:usize=2_000_000;
const MAX_TERMINAL_KEYS_PER_R8:usize=1_000_000;
const OUT:&str="computations/unaudited-codex-orbit0-k24-charge-only-fast-prototype-2026-08-24/results_direct_d17_d18_prefix1.json";
const IDS17_34:[&str;7]=["D17:234|R:3-4","D17:243|R:3-4","D17:324|R:3-4","D17:333|R:3-4","D17:342|R:3-4","D17:423|R:3-4","D17:432|R:3-4"];
const IDS18_24:[&str;6]=["D18:244|R:2-4","D18:334|R:2-4","D18:343|R:2-4","D18:424|R:2-4","D18:433|R:2-4","D18:442|R:2-4"];

#[derive(Clone,Copy,Default)]struct Q{heads:u64,pivotable:u64,p1:u64,mid:u64,pivmid:u64,p2:u64,terminal:u64,charge:i128}
impl Q{fn add(&mut self,x:Q){self.heads+=x.heads;self.pivotable+=x.pivotable;self.p1+=x.p1;self.mid+=x.mid;self.pivmid+=x.pivmid;self.p2+=x.p2;self.terminal+=x.terminal;self.charge+=x.charge}}
#[derive(Clone)]struct O{mid:u64,pivmid:u64,p2:u64,terminal:u64,unit_charge:i128,hist:[u8;79]}
impl Default for O{fn default()->Self{Self{mid:0,pivmid:0,p2:0,terminal:0,unit_charge:0,hist:[0;79]}}}
#[derive(Clone,Copy,Eq,Hash,PartialEq)]struct FKey{row:Row,p:u8,first:u8,finald:u8}
#[derive(Default)]struct W{q:[Q;2],hist:[BTreeMap<(u8,u8),u64>;2],first_hit:u64,first_miss:u64,terminal_hit:u64,terminal_miss:u64,terminality_assertions:u64,peak_first:usize,peak_terminal:usize}
impl W{fn add(&mut self,x:W){for i in 0..2{self.q[i].add(x.q[i]);for(k,v)in x.hist[i].iter(){*self.hist[i].entry(*k).or_default()+=*v}}self.first_hit+=x.first_hit;self.first_miss+=x.first_miss;self.terminal_hit+=x.terminal_hit;self.terminal_miss+=x.terminal_miss;self.terminality_assertions+=x.terminality_assertions;self.peak_first=self.peak_first.max(x.peak_first);self.peak_terminal=self.peak_terminal.max(x.peak_terminal)}}
fn hx(r:&Row)->String{r.0.iter().map(|x|format!("{:02x}",x)).collect()}
fn target(ri:usize)->Option<(usize,usize)>{for j in 0..257{if j*484/256==ri{return Some((j,j%2))}}None}

// Compute the response only from literal K23 children.  Terminality is proved
// for every tail of every realized abstract response key before it is cached.
fn response(row:&Row,s:[u8;12],p:usize,d:usize,e:&E,c:&mut HashMap<RKey,(i64,i64,u64,u64)>,w:&mut W)->(i64,u64){
 let k=RKey{profile:profile(row,p,e),sig:s,pivot:p as u8,degree:d as u8};
 let z=if let Some(&x)=c.get(&k){w.terminal_hit+=1;x}else{
  w.terminal_miss+=1;let mut q=0i64;let mut n=0u64;
  for t in &e.tails[p][d-2]{let cs=child_sig(s,p,t,e);assert!(avail(cs,e).is_empty());w.terminality_assertions+=1;let child=replace(row,&e.anchors[p],t);assert_eq!(sig(&child,e),cs);q+=charge(&child,e);n+=1}
  let x=(q,q,n,n);c.insert(k,x);x
 };
 assert_eq!(z.0,z.1);assert_eq!(z.2,z.3);let expect=match d{2=>12,3=>32,4=>60,_=>unreachable!()};assert_eq!(z.2,expect);(z.0,z.2)
}
fn terminal_witness(row:&Row,s:[u8;12],p:usize,d:usize,e:&E)->(usize,Row,i64){for(ti,t)in e.tails[p][d-2].iter().enumerate(){let cs=child_sig(s,p,t,e);assert!(avail(cs,e).is_empty());let child=replace(row,&e.anchors[p],t);assert_eq!(sig(&child,e),cs);let q=charge(&child,e);if q!=0{return(ti,child,q)}}panic!("nonzero aggregate response had no nonzero literal child")}

#[allow(clippy::too_many_arguments)]
fn out2(row:&Row,p1:usize,m1:usize,first:usize,finald:usize,e:&E,tc:&mut HashMap<RKey,(i64,i64,u64,u64)>,w:&mut W,sample:&mut Option<String>,meta:(usize,usize,i128))->O{let s1=sig(row,e);let mut z=O::default();for(ti,t)in e.tails[p1][first-2].iter().enumerate(){z.mid+=1;let s2=child_sig(s1,p1,t,e);let ps2=avail(s2,e);if ps2.is_empty(){continue}z.pivmid+=1;let m2=ps2.len();z.hist[m2]+=1;assert_eq!(U%((m1*m2)as i128),0);let unit=-U/((m1*m2)as i128);let r2=replace(row,&e.anchors[p1],t);assert_eq!(sig(&r2,e),s2);for p2 in ps2{z.p2+=1;let(q,n)=response(&r2,s2,p2,finald,e,tc,w);z.terminal+=n;z.unit_charge+=unit*(q as i128);if sample.is_none()&&q!=0{let(t2,r3,q3)=terminal_witness(&r2,s2,p2,finald,e);let(j,ri,mass)=meta;*sample=Some(format!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",j,ri,mass,hx(row),hx(&r2),hx(&r3),p1,ti,p2,t2,m1,m2,first,finald,q3,q,unit,mass*unit*(q as i128),"two_response"))}}}z}
#[allow(clippy::too_many_arguments)]
fn emit2(row:Row,g:usize,mass:i128,firstd:usize,finald:usize,e:&E,fc:&mut HashMap<FKey,O>,tc:&mut HashMap<RKey,(i64,i64,u64,u64)>,w:&mut W,sample:&mut Option<String>,meta:(usize,usize,i128)){w.q[g].heads+=1;let s=sig(&row,e);let ps=avail(s,e);if ps.is_empty(){return}w.q[g].pivotable+=1;let m1=ps.len();w.q[g].p1+=m1 as u64;for p in ps{let k=FKey{row,p:p as u8,first:firstd as u8,finald:finald as u8};let z=if let Some(x)=fc.get(&k){w.first_hit+=1;x.clone()}else{w.first_miss+=1;let x=out2(&row,p,m1,firstd,finald,e,tc,w,sample,meta);fc.insert(k,x.clone());x};w.q[g].mid+=z.mid;w.q[g].pivmid+=z.pivmid;w.q[g].p2+=z.p2;w.q[g].terminal+=z.terminal;w.q[g].charge+=mass*z.unit_charge;for(m2,&n)in z.hist.iter().enumerate(){if n>0{*w.hist[g].entry((m1 as u8,m2 as u8)).or_default()+=n as u64}}}}
fn worker(e:Arc<E>,indices:Arc<Vec<usize>>,wi:usize,nw:usize,samples:Arc<Mutex<Vec<String>>>)->W{let mut w=W::default();for ii in(wi..indices.len()).step_by(nw){let ri=indices[ii];let r=&e.records[ri];let mass=(r.size as i128)*(r.coefficient as i128);let mut fc=HashMap::new();let mut tc=HashMap::new();let tar=target(ri);let mut slots:[Option<String>;2]=std::array::from_fn(|_|None);
 // Direct K17: six permutations of 2+3+4 and symmetric 3+3+3, then K3,K4.
 let specs=[(0usize,0usize,1usize,2usize),(1,0,2,1),(2,1,0,2),(4,1,2,0),(5,2,0,1),(6,2,1,0)];
 for &(_sector,d2,d3,d4)in &specs{for a in &e.factor[d2][0]{for b in &e.factor[d3][1]{for c in &e.factor[d4][2]{let mut f:[Option<&[u8;4]>;3]=[None,None,None];f[d2]=Some(a);f[d3]=Some(b);f[d4]=Some(c);let q=[f[0].unwrap(),f[1].unwrap(),f[2].unwrap()];let row=make(r,q[0],q[1],q[2]);emit2(row,0,mass,3,4,&e,&mut fc,&mut tc,&mut w,&mut slots[0],(tar.map(|x|x.0).unwrap_or(0),ri,mass))}}}}
 for a in &e.factor[0][1]{for b in &e.factor[1][1]{for c in &e.factor[2][1]{let row=make(r,a,b,c);emit2(row,0,mass,3,4,&e,&mut fc,&mut tc,&mut w,&mut slots[0],(tar.map(|x|x.0).unwrap_or(0),ri,mass))}}}
 // Direct K18: 2+4+4 and 3+3+4, followed by K2,K4.
 for low in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=low).collect();for a in &e.factor[low][0]{for b in &e.factor[o[0]][2]{for c in &e.factor[o[1]][2]{let row=match low{0=>make(r,a,b,c),1=>make(r,b,a,c),_=>make(r,b,c,a)};emit2(row,1,mass,2,4,&e,&mut fc,&mut tc,&mut w,&mut slots[1],(tar.map(|x|x.0).unwrap_or(0),ri,mass))}}}}
 for high in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=high).collect();for a in &e.factor[o[0]][1]{for b in &e.factor[o[1]][1]{for c in &e.factor[high][2]{let row=match high{0=>make(r,c,a,b),1=>make(r,a,c,b),_=>make(r,a,b,c)};emit2(row,1,mass,2,4,&e,&mut fc,&mut tc,&mut w,&mut slots[1],(tar.map(|x|x.0).unwrap_or(0),ri,mass))}}}}
 if let Some((_,preferred))=tar{let(g,line)=(0..2).map(|delta|(preferred+delta)%2).find_map(|g|slots[g].take().map(|line|(g,line))).unwrap_or_else(||panic!("no nonzero sample in any group at ri={}",ri));samples.lock().unwrap().push(format!("{}\t{}",g,line))}
 assert!(fc.len()<=MAX_FIRST_KEYS_PER_R8,"literal first cache cap exceeded at R8 {}: {}",ri,fc.len());assert!(tc.len()<=MAX_TERMINAL_KEYS_PER_R8,"terminal cache cap exceeded at R8 {}: {}",ri,tc.len());w.peak_first=w.peak_first.max(fc.len());w.peak_terminal=w.peak_terminal.max(tc.len())}w}
fn h(m:&BTreeMap<(u8,u8),u64>)->String{m.iter().map(|(&(a,b),v)|format!("\"{}_{}\":{}",a,b,v)).collect::<Vec<_>>().join(",")}
fn ids(v:&[&str])->String{v.iter().map(|x|format!("\"{}\"",x)).collect::<Vec<_>>().join(",")}
fn list(v:&[usize])->String{v.iter().map(|x|x.to_string()).collect::<Vec<_>>().join(",")}

pub fn run(){
 let begun=Instant::now();let a:Vec<_>=std::env::args().collect();let(mut start,mut end,mut workers,mut output)=(0usize,SLICES,8usize,OUT.to_string());let mut i=1;
 while i<a.len(){match a[i].as_str(){"--start-record"=>{start=a[i+1].parse().unwrap();i+=2},"--end-record"=>{end=a[i+1].parse().unwrap();i+=2},"--workers"=>{workers=a[i+1].parse().unwrap();i+=2},"--output"=>{output=a[i+1].clone();i+=2},_=>panic!("bad arg")}}
 assert!((1..=8).contains(&workers)&&start<end&&end<=SLICES);let e=Arc::new(parse());assert_eq!(e.records.len(),SLICES);let selection:Vec<_>=(start..end).collect();let consumed=selection.len();let indices=Arc::new(selection);let samples=Arc::new(Mutex::new(Vec::new()));let mut jobs=Vec::new();
 for wi in 0..workers{let x=e.clone();let ix=indices.clone();let s=samples.clone();jobs.push(thread::spawn(move||worker(x,ix,wi,workers,s)))}let mut z=W::default();for j in jobs{z.add(j.join().unwrap())}
 if start==0&&end==SLICES{assert_eq!(z.q[0].p2,842_301_440);assert_eq!(z.q[1].p2,230_937_600)}assert_eq!(z.q[0].terminal,60*z.q[0].p2);assert_eq!(z.q[1].terminal,60*z.q[1].p2);
 let elapsed=begun.elapsed().as_secs_f64();assert!(elapsed<600.0);let projected=elapsed*SLICES as f64/consumed as f64;let names=[("source_D17_R3_4",ids(&IDS17_34)),("source_D18_R2_4",ids(&IDS18_24))];
 let groups=(0..2).map(|g|format!("    {{\"group_id\":\"{}\",\"ids\":[{}],\"source_heads\":{},\"pivotable_source_heads\":{},\"p1_uses\":{},\"intermediate_children\":{},\"pivotable_intermediate_children\":{},\"p2_uses\":{},\"K24_terminal_occurrences\":{},\"full_occurrences\":{},\"irreducible_occurrences\":{},\"full_charge_scaled_U\":\"{}\",\"irreducible_charge_scaled_U\":\"{}\",\"denominator_hist\":{{{}}}}}",names[g].0,names[g].1,z.q[g].heads,z.q[g].pivotable,z.q[g].p1,z.q[g].mid,z.q[g].pivmid,z.q[g].p2,z.q[g].terminal,z.q[g].terminal,z.q[g].terminal,z.q[g].charge,z.q[g].charge,h(&z.hist[g]))).collect::<Vec<_>>().join(",\n");
 let text=format!("{{\n  \"status\":\"PASS_BOUNDED_K24_CHARGE_ONLY_DIRECT_D17_D18\",\n  \"degree\":24,\n  \"scale_U\":\"{}\",\n  \"source_interval\":[{},{}],\n  \"source_slices\":{},\n  \"covered_ids\":13,\n  \"scalar_groups\":2,\n  \"groups\":[\n{}\n  ],\n  \"cache\":{{\"literal_first_hits\":{},\"literal_first_misses\":{},\"terminal_hits\":{},\"terminal_misses\":{},\"terminality_assertions_on_realized_keys\":{},\"peak_literal_first_keys_per_R8\":{},\"peak_terminal_keys_per_R8\":{}}},\n  \"column_or_row_output\":false,\n  \"terminality\":\"all K24 K4 children have anchor mass zero and no frozen pivot\",\n  \"elapsed_seconds\":{:.6},\n  \"projected_full_seconds\":{:.6},\n  \"scope\":\"charge-only exact prefix for 13 direct D17/D18 K24 IDs; no columns, rows, span, membership, or conjecture claim\"\n}}\n",U,start,end,consumed,groups,z.first_hit,z.first_miss,z.terminal_hit,z.terminal_miss,z.terminality_assertions,z.peak_first,z.peak_terminal,elapsed,projected);
 let tmp=format!("{}.tmp",output);std::fs::write(&tmp,&text).unwrap();rename(tmp,&output).unwrap();print!("{}",text)
}
}
fn main(){fold::run()}
