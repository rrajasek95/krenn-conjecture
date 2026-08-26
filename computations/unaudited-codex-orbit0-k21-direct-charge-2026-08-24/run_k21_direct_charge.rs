mod run {
 #![allow(dead_code)]
 include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
 use std::fs::rename;
 const OUT:&str="computations/unaudited-codex-orbit0-k21-direct-charge-2026-08-24/results_k21_direct_charge.json";
 const U:i128=400_591_699_200;
 const WORKERS:usize=8;
 const GATE:f64=300.0;

 #[derive(Clone,Copy,Default)]
 struct DStat { parents:u64,pivotable:u64,pivot_uses:u64,full_occ:u64,irr_occ:u64,full:i128,irr:i128 }
 impl DStat { fn add(&mut self,x:DStat){self.parents+=x.parents;self.pivotable+=x.pivotable;self.pivot_uses+=x.pivot_uses;self.full_occ+=x.full_occ;self.irr_occ+=x.irr_occ;self.full+=x.full;self.irr+=x.irr} }

 fn masses(e:&E)->Vec<i128>{e.records.iter().map(|r|(r.size as i128)*(r.coefficient as i128)).collect()}
 fn emit(row:&Row,mass:i128,shift:usize,e:&E,cache:&mut HashMap<RKey,(i64,i64,u64,u64)>,z:&mut DStat){
  z.parents+=1;let s=sig(row,e);let ps=avail(s,e);if ps.is_empty(){return}z.pivotable+=1;
  assert_eq!(mass*U%(ps.len()as i128),0);let w=mass*U/(ps.len()as i128);
  for p in ps{z.pivot_uses+=1;let(fq,iq,fnn,inn)=resp(row,s,p,shift,e,cache);z.full_occ+=fnn;z.irr_occ+=inn;z.full+=w*(fq as i128);z.irr+=w*(iq as i128)}
 }
 fn worker(e:Arc<E>,ms:Arc<Vec<i128>>,start:usize,step:usize)->([DStat;3],usize){
  let mut out=[DStat::default();3];let mut cache=HashMap::new();
  for ri in(start..e.records.len()).step_by(step){let r=&e.records[ri];let mass=ms[ri];
   // Direct K17: all permutations of 2+3+4, plus 3+3+3; respond by K4.
   for d0 in 0..3{for d1 in 0..3{if d0==d1{continue}let d2=3-d0-d1;for a in &e.factor[0][d0]{for b in &e.factor[1][d1]{for c in &e.factor[2][d2]{emit(&make(r,a,b,c),mass,4,&e,&mut cache,&mut out[0])}}}}}
   for a in &e.factor[0][1]{for b in &e.factor[1][1]{for c in &e.factor[2][1]{emit(&make(r,a,b,c),mass,4,&e,&mut cache,&mut out[0])}}}

   // Direct K18: permutations of 2+4+4 and 3+3+4; respond by K3.
   for low in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=low).collect();for a in &e.factor[low][0]{for b in &e.factor[o[0]][2]{for c in &e.factor[o[1]][2]{let row=match low{0=>make(r,a,b,c),1=>make(r,b,a,c),_=>make(r,b,c,a)};emit(&row,mass,3,&e,&mut cache,&mut out[1])}}}}
   for high in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=high).collect();for a in &e.factor[o[0]][1]{for b in &e.factor[o[1]][1]{for c in &e.factor[high][2]{let row=match high{0=>make(r,c,a,b),1=>make(r,a,c,b),_=>make(r,a,b,c)};emit(&row,mass,3,&e,&mut cache,&mut out[1])}}}}

   // Direct K19: permutations of 3+4+4; respond by K2.
   for low in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=low).collect();for a in &e.factor[low][1]{for b in &e.factor[o[0]][2]{for c in &e.factor[o[1]][2]{let row=match low{0=>make(r,a,b,c),1=>make(r,b,a,c),_=>make(r,b,c,a)};emit(&row,mass,2,&e,&mut cache,&mut out[2])}}}}
  }(out,cache.len())
 }
 pub fn run_main(){let begun=Instant::now();let e=Arc::new(parse());let ms=Arc::new(masses(&e));let mut jobs=Vec::new();for t in 0..WORKERS{let a=e.clone();let b=ms.clone();jobs.push(thread::spawn(move||worker(a,b,t,WORKERS)))}let mut z=[DStat::default();3];let mut cache=0usize;for j in jobs{let(q,c)=j.join().unwrap();cache+=c;for i in 0..3{z[i].add(q[i])}}
  assert_eq!((z[0].parents,z[0].pivotable,z[0].pivot_uses),(82_938_880,81_076_480,267_564_800));
  assert_eq!((z[1].parents,z[1].pivotable,z[1].pivot_uses),(152_251_200,137_817_600,260_736_000));
  assert_eq!((z[2].parents,z[2].pivotable),(167_616_000,111_744_000));
  assert_eq!(z[0].full_occ,60*z[0].pivot_uses);assert_eq!(z[1].full_occ,32*z[1].pivot_uses);assert_eq!(z[2].full_occ,12*z[2].pivot_uses);assert!(begun.elapsed().as_secs_f64()<GATE);
  let text=format!(concat!("{{\n  \"status\":\"PASS_COMPLETE_16_DIRECT_ID_K21_CHARGE\",\n  \"scale_U\":\"{}\",\n  \"workers\":{},\n  \"profile_cache_entries\":{},\n",
   "  \"groups\":[\n",
   "    {{\"ids\":[\"D17:234|R:4\",\"D17:243|R:4\",\"D17:324|R:4\",\"D17:333|R:4\",\"D17:342|R:4\",\"D17:423|R:4\",\"D17:432|R:4\"],\"parents\":{},\"pivotable_parents\":{},\"pivot_uses\":{},\"full_occurrences\":{},\"irreducible_occurrences\":{},\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\"}},\n",
   "    {{\"ids\":[\"D18:244|R:3\",\"D18:334|R:3\",\"D18:343|R:3\",\"D18:424|R:3\",\"D18:433|R:3\",\"D18:442|R:3\"],\"parents\":{},\"pivotable_parents\":{},\"pivot_uses\":{},\"full_occurrences\":{},\"irreducible_occurrences\":{},\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\"}},\n",
   "    {{\"ids\":[\"D19:344|R:2\",\"D19:434|R:2\",\"D19:443|R:2\"],\"parents\":{},\"pivotable_parents\":{},\"pivot_uses\":{},\"full_occurrences\":{},\"irreducible_occurrences\":{},\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\"}}\n",
   "  ],\n  \"covered_ids\":16,\n  \"individual_id_charges\":null,\n  \"scope\":\"exact grouped direct-parent responses only; no derived K17/K18/K19 parents, K21 rows, K22 tails, or membership claim\",\n  \"elapsed_seconds\":{:.6}\n}}\n"),
   U,WORKERS,cache,
   z[0].parents,z[0].pivotable,z[0].pivot_uses,z[0].full_occ,z[0].irr_occ,z[0].full,z[0].irr,
   z[1].parents,z[1].pivotable,z[1].pivot_uses,z[1].full_occ,z[1].irr_occ,z[1].full,z[1].irr,
   z[2].parents,z[2].pivotable,z[2].pivot_uses,z[2].full_occ,z[2].irr_occ,z[2].full,z[2].irr,begun.elapsed().as_secs_f64());
  let tmp=format!("{}.tmp",OUT);std::fs::write(&tmp,&text).unwrap();rename(tmp,OUT).unwrap();print!("{}",text)
 }
}
fn main(){run::run_main()}
