//! Sample-only repair for the frozen fast D17/D18 scalar producer.
//!
//! The fast full producer computes witnesses but does not serialize them.
//! This bounded companion visits exactly the 257 frozen source slices and
//! stops each group at its first nonzero continuation.  It never accumulates
//! or claims a scalar family charge.
#![allow(dead_code)]
mod sampler {
include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
use std::fs::rename;

const U:i128=400_591_699_200;
const TOTAL:usize=485;
const IDS17:&str="D17:234|R:3-4+D17:243|R:3-4+D17:324|R:3-4+D17:333|R:3-4+D17:342|R:3-4+D17:423|R:3-4+D17:432|R:3-4";
const IDS18:&str="D18:244|R:2-4+D18:334|R:2-4+D18:343|R:2-4+D18:424|R:2-4+D18:433|R:2-4+D18:442|R:2-4";
fn hx(r:&Row)->String{r.0.iter().map(|x|format!("{:02x}",x)).collect()}

fn try_head(row:Row,ordinal:u64,source:i128,gid:&str,ids:&str,first:usize,e:&E,term:&mut HashMap<RKey,(i64,i64,u64,u64)>)->Option<String>{
 let s1=sig(&row,e);let ps1=avail(s1,e);let m1=ps1.len();if m1==0{return None}
 for p1 in ps1{for(t1,t)in e.tails[p1][first-2].iter().enumerate(){let s2=child_sig(s1,p1,t,e);let ps2=avail(s2,e);let m2=ps2.len();if m2==0{continue}let row2=replace(&row,&e.anchors[p1],t);assert_eq!(sig(&row2,e),s2);for p2 in ps2{let key=RKey{profile:profile(&row2,p2,e),sig:s2,pivot:p2 as u8,degree:4};let z=if let Some(&x)=term.get(&key){x}else{resp(&row2,s2,p2,4,e,term)};assert_eq!((z.2,z.3),(60,60));assert_eq!(z.0,z.1);for tail in &e.tails[p2][2]{assert!(avail(child_sig(s2,p2,tail,e),e).is_empty())}if z.0!=0{let den=m1*m2;assert_eq!(U%den as i128,0);let unit=source*U/den as i128;return Some(format!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",gid,ids,ordinal,hx(&row),source,den,unit,z.0,unit*z.0 as i128,format!("{}:{}:{}:{};{}:-:4:{}",p1,t1,first,hx(&row2),p2,hx(&row2))))}}}}
 None
}

fn find(e:&E,ri:usize,which:usize)->String{let r=&e.records[ri];let source=-(r.size as i128*r.coefficient as i128);let mut ordinal=0u64;let mut term=HashMap::new();
 macro_rules! emit{($row:expr)=>{{let row=$row;if let Some(w)=try_head(row,ordinal,source,if which==0{"source_D17_R3_4"}else{"source_D18_R2_4"},if which==0{IDS17}else{IDS18},if which==0{3}else{2},e,&mut term){return w}ordinal+=1;}}}
 if which==0{let specs=[(0usize,1usize,2usize),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)];for &(d2,d3,d4)in &specs{for a in &e.factor[d2][0]{for b in &e.factor[d3][1]{for c in &e.factor[d4][2]{let mut f:[Option<&[u8;4]>;3]=[None,None,None];f[d2]=Some(a);f[d3]=Some(b);f[d4]=Some(c);emit!(make(r,f[0].unwrap(),f[1].unwrap(),f[2].unwrap()));}}}}for a in &e.factor[0][1]{for b in &e.factor[1][1]{for c in &e.factor[2][1]{emit!(make(r,a,b,c));}}}}
 else{for low in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=low).collect();for a in &e.factor[low][0]{for b in &e.factor[o[0]][2]{for c in &e.factor[o[1]][2]{emit!(match low{0=>make(r,a,b,c),1=>make(r,b,a,c),_=>make(r,b,c,a)});}}}}for high in 0..3{let o:Vec<_>=(0..3).filter(|&x|x!=high).collect();for a in &e.factor[o[0]][1]{for b in &e.factor[o[1]][1]{for c in &e.factor[high][2]{emit!(match high{0=>make(r,c,a,b),1=>make(r,a,c,b),_=>make(r,a,b,c)});}}}}}
 panic!("no nonzero continuation at source {} group {}",ri,which)
}

pub fn run(){let a:Vec<_>=std::env::args().collect();let mut workers=8usize;let mut output="/tmp/k24_direct17_distributed_literals.json".to_string();let mut i=1;while i<a.len(){match a[i].as_str(){"--workers"=>{workers=a[i+1].parse().unwrap();i+=2},"--output"=>{output=a[i+1].clone();i+=2},_=>panic!("bad argument")}}assert!((1..=8).contains(&workers));let begun=Instant::now();let e=Arc::new(parse());let mut jobs=Vec::new();for w in 0..workers{let ee=e.clone();jobs.push(thread::spawn(move||{let mut out=Vec::new();for bin in(w..257).step_by(workers){let ri=(bin*TOTAL+256)/257;assert_eq!(ri*257/TOTAL,bin);for g in 0..2{out.push((g,bin,ri,find(&ee,ri,g)))}}out}))}let mut lines=Vec::new();for j in jobs{lines.extend(j.join().unwrap())}lines.sort_by_key(|x|(x.0,x.1));assert_eq!(lines.len(),514);for g in 0..2{for bin in 0..257{assert_eq!((lines[257*g+bin].0,lines[257*g+bin].1),(g,bin))}}let sample_path=format!("{}.samples.tsv",output);let header="sample_bin\tsource_index\tgroup_id\tlineage_scope\tsource_head_ordinal\tsource_head_row\tsource_coefficient\tdenominator_product\tunit_scaled_U\tterminal_K4_charge\tcontribution_scaled_U\tliteral_steps";let body=lines.iter().map(|x|format!("{}\t{}\t{}",x.1,x.2,x.3)).collect::<Vec<_>>().join("\n");let tmp_s=format!("{}.tmp",sample_path);std::fs::write(&tmp_s,format!("{}\n{}\n",header,body)).unwrap();rename(tmp_s,&sample_path).unwrap();let elapsed=begun.elapsed().as_secs_f64();assert!(elapsed<600.0);let text=format!("{{\n  \"status\":\"PASS_K24_DIRECT17_DISTRIBUTED_LITERAL_SAMPLE_ONLY\",\n  \"degree\":24,\n  \"family\":\"direct17\",\n  \"scale_U\":\"{}\",\n  \"sample_schema\":\"k24_physical_literal_v2_source_head\",\n  \"groups\":[\"source_D17_R3_4\",\"source_D18_R2_4\"],\n  \"bins_per_group\":257,\n  \"literal_witnesses\":514,\n  \"literal_witness_ledger\":\"{}\",\n  \"scalar_charge_accumulated\":false,\n  \"production_scalar_rerun\":false,\n  \"elapsed_seconds\":{:.6}\n}}\n",U,sample_path,elapsed);let tmp=format!("{}.tmp",output);std::fs::write(&tmp,&text).unwrap();rename(tmp,&output).unwrap();print!("{}",text)}
}
fn main(){sampler::run()}
