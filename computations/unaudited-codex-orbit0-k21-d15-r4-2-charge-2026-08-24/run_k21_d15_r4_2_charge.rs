//! Exact grouped K21 charge for D15:{223,232,322}|R:4-2 from K15CHK1.
mod fold {
#![allow(dead_code, unused_imports)]
include!("../unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/run_hidden_children_prefix.rs");

const INPUT:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k15.bin";
const OUTDIR:&str="computations/unaudited-codex-orbit0-k21-d15-r4-2-charge-2026-08-24/";
const EXPECTED:u64=5_311_211;

#[derive(Clone,Copy,Default)] struct K2Resp{n:u64,q:i64}
#[derive(Clone,Default)] struct Stat{
 parents:u64,input:i128,p1:u64,k4:u64,k19:u64,p2:u64,k21:u64,charge:i128,
 plan_hits:u64,plan_misses:u64,cache_hits:u64,cache_misses:u64,literal_guards:u64,
 first:HashMap<u8,u64>,second:HashMap<u8,u64>,product:HashMap<u16,u64>,
}
impl Stat{fn add(&mut self,x:Stat){self.parents+=x.parents;self.input+=x.input;self.p1+=x.p1;self.k4+=x.k4;self.k19+=x.k19;self.p2+=x.p2;self.k21+=x.k21;self.charge+=x.charge;self.plan_hits+=x.plan_hits;self.plan_misses+=x.plan_misses;self.cache_hits+=x.cache_hits;self.cache_misses+=x.cache_misses;self.literal_guards+=x.literal_guards;for(k,v)in x.first{*self.first.entry(k).or_default()+=v}for(k,v)in x.second{*self.second.entry(k).or_default()+=v}for(k,v)in x.product{*self.product.entry(k).or_default()+=v}}}

fn rec(data:&[u8],i:usize)->(Row,i64){let o=16+32*i;let mut x=[0;24];x.copy_from_slice(&data[o..o+24]);(Row(x),i64::from_le_bytes(data[o+24..o+32].try_into().unwrap()))}
fn plan(sig:[u8;12],p1:usize,e:&Engine,c:&CEnv)->Vec<(u8,[u8;12],Vec<usize>)>{
 let mut out=Vec::new();for(ti,t)in c.k4[p1].iter().enumerate(){let s19=child_sig(sig,p1,t,e);let ps=available(s19,e);if !ps.is_empty(){out.push((ti as u8,s19,ps))}}out
}
fn k2_response(row:&Row,key:PKey,e:&Engine,c:&CEnv)->K2Resp{
 assert_eq!(path_profile(row,key.pivot as usize,e,c),key.profile);let mut z=K2Resp::default();
 for t in &e.all_k2[key.pivot as usize]{let predicted=child_sig(key.sig,key.pivot as usize,t,e);assert_eq!(predicted.iter().map(|&x|x as usize).sum::<usize>(),3);assert!(available(predicted,e).is_empty());let child=replace_anchor(row,&e.anchors[key.pivot as usize],t);assert_eq!(signature(&child.0,e),predicted);let a=abstract_ckey(&key.profile,key.pivot as usize,t,e,c);let l=literal_ckey(&child,c);assert_eq!(a,l);z.n+=1;z.q+=*c.dual.get(&a).unwrap_or(&0)}assert_eq!(z.n,12);z
}
fn fold_worker(data:Arc<Vec<u8>>,e:Arc<Engine>,c:Arc<CEnv>,begin:usize,end:usize,start:usize,step:usize)->Stat{
 let mut z=Stat::default();let mut plans:HashMap<([u8;12],u8),Vec<(u8,[u8;12],Vec<usize>)>>=HashMap::new();let mut cache:HashMap<PKey,K2Resp>=HashMap::new();
 for i in (begin+start..end).step_by(step){let(row,v)=rec(&data,i);assert!(row.0.windows(2).all(|w|w[0]<=w[1]));assert_ne!(v,0);z.parents+=1;z.input+=v as i128;let s15=signature(&row.0,&e);assert_eq!(s15.iter().map(|&x|x as usize).sum::<usize>(),9);let ps1=available(s15,&e);let m1=ps1.len();assert!(m1>0);assert_eq!(U%(m1 as i128),0);*z.first.entry(m1 as u8).or_default()+=1;let w19=-(v as i128)*U/(m1 as i128);
  for p1 in ps1{z.p1+=1;z.k4+=60;let pk=(s15,p1 as u8);let pp=if let Some(x)=plans.get(&pk){z.plan_hits+=1;x.clone()}else{z.plan_misses+=1;let x=plan(s15,p1,&e,&c);plans.insert(pk,x.clone());x};
   for(ti,s19,ps2)in pp{z.k19+=1;let m2=ps2.len();assert_eq!(U%((m1*m2)as i128),0);assert_eq!(w19%(m2 as i128),0);*z.second.entry(m2 as u8).or_default()+=1;*z.product.entry((m1*m2)as u16).or_default()+=1;let row19=replace_anchor(&row,&e.anchors[p1],&c.k4[p1][ti as usize]);assert_eq!(signature(&row19.0,&e),s19);let w21=-w19/(m2 as i128);
    for p2 in ps2{z.p2+=1;let key=PKey{profile:path_profile(&row19,p2,&e,&c),sig:s19,pivot:p2 as u8};let r=if let Some(x)=cache.get(&key){z.cache_hits+=1;*x}else{z.cache_misses+=1;let x=k2_response(&row19,key,&e,&c);z.literal_guards+=x.n;cache.insert(key,x);x};z.k21+=r.n;z.charge+=w21*(r.q as i128)}
   }
  }
 }
 z
}
fn hist(m:&HashMap<u8,u64>)->String{let mut v:Vec<_>=m.iter().collect();v.sort();v.into_iter().map(|(k,x)|format!("\"{}\":{}",k,x)).collect::<Vec<_>>().join(",")}
fn hist16(m:&HashMap<u16,u64>)->String{let mut v:Vec<_>=m.iter().collect();v.sort();v.into_iter().map(|(k,x)|format!("\"{}\":{}",k,x)).collect::<Vec<_>>().join(",")}
pub fn run(){
 let args:Vec<_>=std::env::args().collect();assert!(args.len()==3||args.len()==5||args.len()==7,"usage: BIN OUT.json [--limit N | --start A --count N]");
 let begun=Instant::now();let data=Arc::new(read(INPUT).unwrap());assert_eq!(&data[..8],b"K15CHK1\0");let declared=u64::from_le_bytes(data[8..16].try_into().unwrap());assert_eq!(declared,EXPECTED);assert_eq!(data.len(),16+32*declared as usize);
 let(begin,end)=if args.len()==3{(0,declared as usize)}else if args.len()==5{assert_eq!(args[3],"--limit");(0,args[4].parse::<usize>().unwrap().min(declared as usize))}else{assert_eq!(args[3],"--start");assert_eq!(args[5],"--count");let a=args[4].parse::<usize>().unwrap();let n=args[6].parse::<usize>().unwrap();assert!(a<=declared as usize&&n<=declared as usize-a);(a,a+n)};let n=end-begin;
 let e=Arc::new(parse());let c=Arc::new(cenv());assert_eq!(e.pivots.len(),78);assert!(e.pivots.iter().all(|p|p.iter().map(|&x|x as usize).sum::<usize>()==4));assert!(c.k4.iter().flatten().all(|t|tail_signature(t,&e).iter().map(|&x|x as usize).sum::<usize>()==0));assert!(e.all_k2.iter().flatten().all(|t|tail_signature(t,&e).iter().map(|&x|x as usize).sum::<usize>()==2));
 let threads=thread::available_parallelism().map_or(4,|x|x.get()).min(8);let mut jobs=Vec::new();for t in 0..threads{let(a,b,d)=(data.clone(),e.clone(),c.clone());jobs.push(thread::spawn(move||fold_worker(a,b,d,begin,end,t,threads)))}let mut z=Stat::default();for j in jobs{z.add(j.join().unwrap())}
 assert_eq!(z.parents,n as u64);assert_eq!(z.k4,60*z.p1);assert_eq!(z.k21,12*z.p2);assert_eq!(z.cache_hits+z.cache_misses,z.p2);if begin==0&&end==declared as usize{assert_eq!(z.input,322_486_272)}let status=if begin==0&&end==declared as usize{"PASS_COMPLETE_GROUPED_D15_R4_2_K21_CHARGE"}else if args.len()==7{"PASS_ATOMIC_INTERVAL_GROUPED_D15_R4_2_K21_CHARGE"}else{"PASS_BOUNDED_GROUPED_D15_R4_2_K21_PREFIX"};
 let text=format!(concat!("{{\n","  \"status\":\"{}\",\n","  \"strict_covered_lineage_ids\":[\"D15:223|R:4-2\",\"D15:232|R:4-2\",\"D15:322|R:4-2\"],\n","  \"individual_id_charges\":null,\n","  \"scale_U\":\"{}\",\n","  \"input_interval\":[{},{}],\n","  \"input_records_consumed\":{},\n","  \"input_records_declared\":{},\n","  \"input_weight_sum\":\"{}\",\n","  \"first_pivot_uses\":{},\n","  \"K4_tail_candidates\":{},\n","  \"retained_pivotable_K19_children\":{},\n","  \"second_pivot_uses\":{},\n","  \"K2_tail_occurrences\":{},\n","  \"full_occurrences\":{},\n","  \"irreducible_occurrences\":{},\n","  \"full_charge_scaled_U\":\"{}\",\n","  \"irreducible_charge_scaled_U\":\"{}\",\n","  \"first_denominator_hist\":{{{}}},\n","  \"second_denominator_hist\":{{{}}},\n","  \"product_denominator_hist\":{{{}}},\n","  \"signature_plan_cache\":{{\"hits\":{},\"misses\":{}}},\n","  \"K2_response_cache\":{{\"hits\":{},\"misses\":{},\"literal_tail_guards_on_miss\":{}}},\n","  \"terminality\":\"K15 sum 9 - K0 4 + K4 0 = K19 sum 5; K19 sum 5 - K0 4 + K2 2 = K21 sum 3, hence terminal\",\n","  \"sign_rule\":\"w19=-w15*U/m1; w21=-w19/m2=+w15*U/(m1*m2)\",\n","  \"elapsed_seconds\":{:.6},\n","  \"scope\":\"strict grouped three-ID scalar only; retained checkpoint combines the three source IDs, so no individual-ID scalar is claimed\"\n","}}\n"),status,U,begin,end,n,declared,z.input,z.p1,z.k4,z.k19,z.p2,z.k21,z.k21,z.k21,z.charge,z.charge,hist(&z.first),hist(&z.second),hist16(&z.product),z.plan_hits,z.plan_misses,z.cache_hits,z.cache_misses,z.literal_guards,begun.elapsed().as_secs_f64());let tmp=format!("{}.tmp",args[2]);std::fs::write(&tmp,&text).unwrap();rename(tmp,&args[2]).unwrap();print!("{}",text)
}
}
fn main(){fold::run()}
