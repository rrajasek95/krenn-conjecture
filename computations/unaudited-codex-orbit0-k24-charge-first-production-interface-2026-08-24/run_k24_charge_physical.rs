//! Exact scalar-only K24 consumers for the four non-hidden source families.
//!
//! No K24 rows or relative columns are emitted.  Every literal preterminal
//! response is followed source-faithfully; only the final K4 response is
//! profile-cached, after exhaustive terminality/full=irreducible checks.
#![allow(dead_code)]
mod fold {
include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

use std::collections::BTreeMap;
use std::fs::{metadata, rename, File};
use std::io::{BufReader, Read, Seek, SeekFrom};

const U24:i128=400_591_699_200;
const SLICES:usize=485;
const K16_INPUT:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin";
const K16_N:u64=24_097_095;
const K16_HEADER:u64=16;
const K16_RECORD:u64=32;
const BASE16:[&str;6]=["224","233","242","323","332","422"];
const BASE15:[&str;3]=["223","232","322"];
const BASE17:[&str;7]=["234","243","324","333","342","423","432"];
const BASE18:[&str;6]=["244","334","343","424","433","442"];

#[derive(Clone,Copy)]struct Spec{gid:&'static str,ids:&'static [&'static str],path:&'static[usize],valid_first:bool}
const I14A:[&str;1]=["D14:222|R:3-3-4"];
const I14B:[&str;1]=["D14:222|R:4-2-4"];
const I15A:[&str;3]=["D15:223|R:2-3-4","D15:232|R:2-3-4","D15:322|R:2-3-4"];
const I15B:[&str;3]=["D15:223|R:3-2-4","D15:232|R:3-2-4","D15:322|R:3-2-4"];
const I16A:[&str;6]=["D16:224|R:2-2-4","D16:233|R:2-2-4","D16:242|R:2-2-4","D16:323|R:2-2-4","D16:332|R:2-2-4","D16:422|R:2-2-4"];
const I16B:[&str;6]=["D16:224|R:4-4","D16:233|R:4-4","D16:242|R:4-4","D16:323|R:4-4","D16:332|R:4-4","D16:422|R:4-4"];
const I17:[&str;7]=["D17:234|R:3-4","D17:243|R:3-4","D17:324|R:3-4","D17:333|R:3-4","D17:342|R:3-4","D17:423|R:3-4","D17:432|R:3-4"];
const I18:[&str;6]=["D18:244|R:2-4","D18:334|R:2-4","D18:343|R:2-4","D18:424|R:2-4","D18:433|R:2-4","D18:442|R:2-4"];
const K14:[Spec;2]=[
 Spec{gid:"source_D14_R3_3_4",ids:&I14A,path:&[3,3,4],valid_first:true},
 Spec{gid:"source_D14_R4_2_4",ids:&I14B,path:&[4,2,4],valid_first:true},
];
const K15:[Spec;2]=[
 Spec{gid:"source_D15_R2_3_4",ids:&I15A,path:&[2,3,4],valid_first:false},
 Spec{gid:"source_D15_R3_2_4",ids:&I15B,path:&[3,2,4],valid_first:false},
];
const K16:[Spec;2]=[
 Spec{gid:"source_D16_R2_2_4",ids:&I16A,path:&[2,2,4],valid_first:false},
 Spec{gid:"source_D16_R4_4",ids:&I16B,path:&[4,4],valid_first:false},
];
const D1718:[Spec;2]=[
 Spec{gid:"source_D17_R3_4",ids:&I17,path:&[3,4],valid_first:false},
 Spec{gid:"source_D18_R2_4",ids:&I18,path:&[2,4],valid_first:false},
];

#[derive(Clone,Copy,Eq,Hash,PartialEq)]struct PlanKey{sig:[u8;12],pivot:u8,degree:u8}
#[derive(Clone)]struct PlanTail{tail:u8,sig:[u8;12],pivots:Vec<usize>}
#[derive(Clone,Default)]struct PStat{
 source_units:u64,heads:u64,source:i128,l1:i128,piv:[u64;3],tails:[u64;3],pivotable:[u64;2],
 terminal:u64,charge:i128,hits:u64,misses:u64,peak:usize,hist:BTreeMap<u32,u64>,samples:BTreeMap<usize,(u64,String)>,
}
impl PStat{fn add(&mut self,x:PStat){self.source_units+=x.source_units;self.heads+=x.heads;self.source+=x.source;self.l1+=x.l1;for i in 0..3{self.piv[i]+=x.piv[i];self.tails[i]+=x.tails[i]}for i in 0..2{self.pivotable[i]+=x.pivotable[i]}self.terminal+=x.terminal;self.charge+=x.charge;self.hits+=x.hits;self.misses+=x.misses;self.peak=self.peak.max(x.peak);for(k,v)in x.hist{*self.hist.entry(k).or_default()+=v}for(k,v)in x.samples{let z=self.samples.entry(k).or_insert_with(||v.clone());if v.0<z.0{*z=v}}}}

fn hx(r:&Row)->String{r.0.iter().map(|x|format!("{:02x}",x)).collect()}
fn ids(xs:&[&str])->String{xs.iter().map(|x|format!("\"{}\"",x)).collect::<Vec<_>>().join(",")}
fn hist(x:&BTreeMap<u32,u64>)->String{x.iter().map(|(k,v)|format!("\"{}\":{}",k,v)).collect::<Vec<_>>().join(",")}
fn plan(s:[u8;12],p:usize,d:usize,e:&E)->Vec<PlanTail>{e.tails[p][d-2].iter().enumerate().filter_map(|(ti,t)|{let z=child_sig(s,p,t,e);let ps=avail(z,e);(!ps.is_empty()).then_some(PlanTail{tail:ti as u8,sig:z,pivots:ps})}).collect()}

#[allow(clippy::too_many_arguments)]
fn walk(row:&Row,source_head:&Row,source_head_ordinal:u64,s:[u8;12],ps:Vec<usize>,source:i128,spec:Spec,depth:usize,den:u32,e:&E,plans:&mut HashMap<PlanKey,Vec<PlanTail>>,term:&mut HashMap<RKey,(i64,i64,u64,u64)>,st:&mut PStat,trace:&mut Vec<(usize,usize,usize,Row)>,witness:&mut Option<String>){
 let m=ps.len();assert!(m>0);let den2=den*m as u32;assert_eq!(U24%(den2 as i128),0);st.piv[depth]+=m as u64;let degree=spec.path[depth];
 for p in ps{
  if depth+1==spec.path.len(){
   let n=e.tails[p][degree-2].len()as u64;st.tails[depth]+=n;let key=RKey{profile:profile(row,p,e),sig:s,pivot:p as u8,degree:degree as u8};let z=if let Some(&v)=term.get(&key){st.hits+=1;v}else{st.misses+=1;resp(row,s,p,degree,e,term)};assert_eq!((z.2,z.3),(n,n));assert_eq!(z.0,z.1);for t in &e.tails[p][degree-2]{assert!(avail(child_sig(s,p,t,e),e).is_empty())}let sign=if spec.path.len()%2==0{1}else{-1};let unit=source*sign*U24/(den2 as i128);st.terminal+=n;st.charge+=unit*z.0 as i128;*st.hist.entry(den2).or_default()+=1;if witness.is_none()&&z.0!=0{let mut steps=trace.iter().map(|(pp,tt,dd,rr)|format!("{}:{}:{}:{}",pp,tt,dd,hx(rr))).collect::<Vec<_>>();steps.push(format!("{}:-:{}:{}",p,degree,hx(row)));*witness=Some(format!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",spec.gid,spec.ids.join("+"),source_head_ordinal,hx(source_head),source,den2,unit,z.0,unit*z.0 as i128,steps.join(";")))}
  }else{
   let key=PlanKey{sig:s,pivot:p as u8,degree:degree as u8};let choices=plans.entry(key).or_insert_with(||plan(s,p,degree,e)).clone();st.tails[depth]+=e.tails[p][degree-2].len()as u64;st.pivotable[depth]+=choices.len()as u64;for x in choices{let child=replace(row,&e.anchors[p],&e.tails[p][degree-2][x.tail as usize]);assert_eq!(sig(&child,e),x.sig);trace.push((p,x.tail as usize,degree,child));walk(&child,source_head,source_head_ordinal,x.sig,x.pivots,source,spec,depth+1,den2,e,plans,term,st,trace,witness);trace.pop();}
  }
 }
}

fn consume_head(row:Row,source_head_ordinal:u64,source:i128,spec:Spec,e:&E,plans:&mut HashMap<PlanKey,Vec<PlanTail>>,term:&mut HashMap<RKey,(i64,i64,u64,u64)>,st:&mut PStat,witness:&mut Option<String>){st.heads+=1;st.source+=source;st.l1+=source.abs();let s=sig(&row,e);let ps=if spec.valid_first{valid(s,e)}else{avail(s,e)};if ps.is_empty(){return}walk(&row,&row,source_head_ordinal,s,ps,source,spec,0,1,e,plans,term,st,&mut Vec::new(),witness)}
fn consume_formula_head(row:Row,cursor:&mut u64,source:i128,spec:Spec,e:&E,plans:&mut HashMap<PlanKey,Vec<PlanTail>>,term:&mut HashMap<RKey,(i64,i64,u64,u64)>,st:&mut PStat,witness:&mut Option<String>){let ordinal=*cursor;*cursor+=1;consume_head(row,ordinal,source,spec,e,plans,term,st,witness)}
fn sample_bin(index:u64,total:u64)->usize{((index*257/total).min(256))as usize}

fn worker_formula(e:Arc<E>,family:&str,start:usize,end:usize,step:usize)->[PStat;2]{
 let specs=if family=="k14"{K14}else if family=="k15"{K15}else{D1718};let mut out:[PStat;2]=std::array::from_fn(|_|PStat::default());let mut plans=HashMap::new();let mut term=HashMap::new();
 for ri in(start..end).step_by(step){let r=&e.records[ri];let positive=r.size as i128*r.coefficient as i128;let mut witnesses:[Option<String>;2]=[None,None];let mut source_head_ordinal=[0u64;2];
  if family=="k14"{for a in &e.factor[0][0]{for b in &e.factor[1][0]{for c in &e.factor[2][0]{let row=make(r,a,b,c);for g in 0..2{consume_formula_head(row,&mut source_head_ordinal[g],-positive,specs[g],&e,&mut plans,&mut term,&mut out[g],&mut witnesses[g])}}}}}
  else if family=="k15"{for packet in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=packet).collect();for a in &e.factor[o[0]][0]{for b in &e.factor[o[1]][0]{for c in &e.factor[packet][1]{let row=match packet{0=>make(r,c,a,b),1=>make(r,a,c,b),_=>make(r,a,b,c)};for g in 0..2{consume_formula_head(row,&mut source_head_ordinal[g],-positive,specs[g],&e,&mut plans,&mut term,&mut out[g],&mut witnesses[g])}}}}}}
  else{
   let specs17=[(0usize,0usize,1usize,2usize),(1,0,2,1),(2,1,0,2),(4,1,2,0),(5,2,0,1),(6,2,1,0)];for &(sector,d2,d3,d4)in &specs17{for a in &e.factor[d2][0]{for b in &e.factor[d3][1]{for c in &e.factor[d4][2]{let mut f:[Option<&[u8;4]>;3]=[None,None,None];f[d2]=Some(a);f[d3]=Some(b);f[d4]=Some(c);let row=make(r,f[0].unwrap(),f[1].unwrap(),f[2].unwrap());consume_formula_head(row,&mut source_head_ordinal[0],-positive,specs[0],&e,&mut plans,&mut term,&mut out[0],&mut witnesses[0])}}}}for a in &e.factor[0][1]{for b in &e.factor[1][1]{for c in &e.factor[2][1]{consume_formula_head(make(r,a,b,c),&mut source_head_ordinal[0],-positive,specs[0],&e,&mut plans,&mut term,&mut out[0],&mut witnesses[0])}}}
   for low in 0..3{let sector=[0usize,3,5][low];let o:Vec<_>=(0..3).filter(|&x|x!=low).collect();for a in &e.factor[low][0]{for b in &e.factor[o[0]][2]{for c in &e.factor[o[1]][2]{let row=match low{0=>make(r,a,b,c),1=>make(r,b,a,c),_=>make(r,b,c,a)};let _=sector;consume_formula_head(row,&mut source_head_ordinal[1],-positive,specs[1],&e,&mut plans,&mut term,&mut out[1],&mut witnesses[1])}}}}for high in 0..3{let sector=[4usize,2,1][high];let o:Vec<_>=(0..3).filter(|&x|x!=high).collect();for a in &e.factor[o[0]][1]{for b in &e.factor[o[1]][1]{for c in &e.factor[high][2]{let row=match high{0=>make(r,c,a,b),1=>make(r,a,c,b),_=>make(r,a,b,c)};let _=sector;consume_formula_head(row,&mut source_head_ordinal[1],-positive,specs[1],&e,&mut plans,&mut term,&mut out[1],&mut witnesses[1])}}}}
  }
  for g in 0..2{out[g].source_units+=1;if let Some(w)=witnesses[g].take(){let bin=sample_bin(ri as u64,SLICES as u64);out[g].samples.entry(bin).or_insert((ri as u64,format!("{}\t{}\t{}",bin,ri,w)));}out[g].peak=out[g].peak.max(term.len())}
 }
 out
}

fn worker_k16(e:Arc<E>,ranges:Vec<(u64,u64)>)->[PStat;2]{let mut out:[PStat;2]=std::array::from_fn(|_|PStat::default());let mut plans=HashMap::new();let mut term=HashMap::new();let f=File::open(K16_INPUT).unwrap();let mut rd=BufReader::with_capacity(4<<20,f);for(start,end)in ranges{rd.seek(SeekFrom::Start(K16_HEADER+K16_RECORD*start)).unwrap();for index in start..end{let mut b=[0u8;32];rd.read_exact(&mut b).unwrap();let mut rr=[0u8;24];rr.copy_from_slice(&b[..24]);let row=Row(rr);let v=i64::from_le_bytes(b[24..].try_into().unwrap())as i128;let mut witness=[None,None];for g in 0..2{consume_head(row,0,v,K16[g],&e,&mut plans,&mut term,&mut out[g],&mut witness[g]);out[g].source_units+=1;if let Some(w)=witness[g].take(){let bin=sample_bin(index,K16_N);out[g].samples.entry(bin).or_insert((index,format!("{}\t{}\t{}",bin,index,w)));}}}for g in 0..2{out[g].peak=out[g].peak.max(term.len())}}out}

fn ranges(total:u64,start:u64,count:u64,workers:usize,distributed:bool)->Vec<Vec<(u64,u64)>>{let pieces=workers*8;let mut out=vec![Vec::new();workers];for p in 0..pieces{let(a,b)=if distributed{let wa=count*p as u64/pieces as u64;let wb=count*(p+1)as u64/pieces as u64;let base=total*p as u64/pieces as u64;(base,base+wb-wa)}else{(start+count*p as u64/pieces as u64,start+count*(p+1)as u64/pieces as u64)};if a<b{out[p%workers].push((a,b))}}out}
fn sink_json(spec:Spec,s:&PStat)->String{format!("{{\"group_id\":\"{}\",\"ids\":[{}],\"path\":[{}],\"source_units\":{},\"source_heads\":{},\"source_coefficient_sum\":\"{}\",\"source_l1\":\"{}\",\"stage_pivot_uses\":[{},{},{}],\"stage_tail_candidates\":[{},{},{}],\"stage_pivotable_children\":[{},{}],\"terminal_K24_occurrences\":{},\"full_occurrences\":{},\"irreducible_occurrences\":{},\"full_charge_scaled_U\":\"{}\",\"irreducible_charge_scaled_U\":\"{}\",\"denominator_product_hist\":{{{}}},\"terminal_cache\":{{\"hits\":{},\"misses\":{},\"peak_keys_per_worker\":{}}},\"literal_witnesses\":{}}}",spec.gid,ids(spec.ids),spec.path.iter().map(|x|x.to_string()).collect::<Vec<_>>().join(","),s.source_units,s.heads,s.source,s.l1,s.piv[0],s.piv[1],s.piv[2],s.tails[0],s.tails[1],s.tails[2],s.pivotable[0],s.pivotable[1],s.terminal,s.terminal,s.terminal,s.charge,s.charge,hist(&s.hist),s.hits,s.misses,s.peak,s.samples.len())}

pub fn run(){let args:Vec<_>=std::env::args().collect();let mut family="k14".to_string();let(mut start,mut count,mut workers)=(0u64,1u64,1usize);let mut distributed=false;let mut output="/tmp/k24_charge_physical.json".to_string();let mut i=1;while i<args.len(){match args[i].as_str(){"--family"=>{family=args[i+1].clone();i+=2},"--start"=>{start=args[i+1].parse().unwrap();i+=2},"--count"=>{count=args[i+1].parse().unwrap();i+=2},"--distributed"=>{distributed=true;i+=1},"--workers"=>{workers=args[i+1].parse().unwrap();i+=2},"--output"=>{output=args[i+1].clone();i+=2},_=>panic!("bad argument {}",args[i])}}assert!(["k14","k15","k16","direct17"].contains(&family.as_str()));assert!((1..=8).contains(&workers)&&count>0);let total=if family=="k16"{K16_N}else{SLICES as u64};assert!(start<=total&&count<=total-start);if distributed{assert_eq!(start,0)}if family=="k16"{let mut h=[0u8;16];File::open(K16_INPUT).unwrap().read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"K16DIR1\0");assert_eq!(u64::from_le_bytes(h[8..].try_into().unwrap()),K16_N);assert_eq!(metadata(K16_INPUT).unwrap().len(),K16_HEADER+K16_RECORD*K16_N)}let begun=Instant::now();let e=Arc::new(parse());let mut jobs=Vec::new();if family=="k16"{let mut rr=ranges(total,start,count,workers,distributed);for w in 0..workers{let ee=e.clone();let r=std::mem::take(&mut rr[w]);jobs.push(thread::spawn(move||worker_k16(ee,r)))}}else{for w in 0..workers{let ee=e.clone();let ff=family.clone();if distributed{let rr=ranges(total,0,count,workers,true);let pieces=rr[w].clone();jobs.push(thread::spawn(move||{let mut z:[PStat;2]=std::array::from_fn(|_|PStat::default());for(a,b)in pieces{let q=worker_formula(ee.clone(),&ff,a as usize,b as usize,1);for g in 0..2{z[g].add(q[g].clone())}}z}))}else{let a=start as usize+w;let end=(start+count)as usize;jobs.push(thread::spawn(move||worker_formula(ee,&ff,a,end,workers)))}}}let mut all:[PStat;2]=std::array::from_fn(|_|PStat::default());for j in jobs{let z=j.join().unwrap();for g in 0..2{all[g].add(z[g].clone())}}let specs=match family.as_str(){"k14"=>K14,"k15"=>K15,"k16"=>K16,_=>D1718};for(g,s)in all.iter().enumerate(){assert_eq!(s.source_units,count);assert_eq!(s.terminal,s.tails[specs[g].path.len()-1]);assert_eq!(s.hits+s.misses,s.piv[specs[g].path.len()-1]);assert!(s.hist.keys().all(|d|U24%(*d as i128)==0))}if family=="direct17"{assert_eq!(all[0].piv[1],1_736_704*count);assert_eq!(all[1].piv[1],476_160*count)}let elapsed=begun.elapsed().as_secs_f64();assert!(elapsed<600.0);let sample_path=format!("{}.samples.tsv",output);let mut lines=vec!["sample_bin\tsource_index\tgroup_id\tlineage_scope\tsource_head_ordinal\tsource_head_row\tsource_coefficient\tdenominator_product\tunit_scaled_U\tterminal_K4_charge\tcontribution_scaled_U\tliteral_steps".to_string()];for s in &all{lines.extend(s.samples.values().map(|x|x.1.clone()))}let tmp_s=format!("{}.tmp",sample_path);std::fs::write(&tmp_s,format!("{}\n",lines.join("\n"))).unwrap();rename(tmp_s,&sample_path).unwrap();let text=format!("{{\n  \"status\":\"PASS_BOUNDED_K24_CHARGE_ONLY_PHYSICAL\",\n  \"degree\":24,\n  \"family\":\"{}\",\n  \"scale_U\":\"{}\",\n  \"sample_schema\":\"k24_physical_literal_v2_source_head\",\n  \"source_interval\":[{},{}],\n  \"distributed\":{},\n  \"workers\":{},\n  \"groups\":[{},{}],\n  \"all_terminal_responses_exhaustive\":true,\n  \"full_equals_irreducible\":true,\n  \"literal_witness_ledger\":\"{}\",\n  \"elapsed_seconds\":{:.6},\n  \"linear_full_projection_seconds\":{:.6},\n  \"scope\":\"exact charge-only bounded source fold; no K24 rows, B records, relative Gram, or verdict\"\n}}\n",family,U24,start,start+count,distributed,workers,sink_json(specs[0],&all[0]),sink_json(specs[1],&all[1]),sample_path,elapsed,elapsed*total as f64/count as f64);let tmp=format!("{}.tmp",output);std::fs::write(&tmp,&text).unwrap();rename(tmp,&output).unwrap();print!("{}",text)}
}
fn main(){fold::run()}
