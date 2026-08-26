//! Read-only support-aware candidate census for the K24 K16 R4-4 sink.
//!
//! This accumulates no family scalar.  It freezes 257 deterministic nonzero
//! literal continuations balanced over the 37 bins realized by the sealed
//! distributed prefix: quota 7 in bins 0..34 and quota 6 in bins 35..36.
#![allow(dead_code)]
mod census {
include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
use std::fs::{File,rename};
use std::io::{BufReader,Read,Seek,SeekFrom};

const INPUT:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin";
const N:u64=24_097_095;
const U:i128=400_591_699_200;
fn hx(r:&Row)->String{r.0.iter().map(|x|format!("{:02x}",x)).collect()}
fn lo(bin:u64)->u64{(bin*N+256)/257}

fn first_nonzero(row:&Row,v:i128,e:&E,cache:&mut HashMap<RKey,(i64,i64,u64,u64)>)->Option<String>{let s1=sig(row,e);let ps1=avail(s1,e);let m1=ps1.len();if m1==0{return None}for p1 in ps1{for(t1,t)in e.tails[p1][2].iter().enumerate(){let s2=child_sig(s1,p1,t,e);let ps2=avail(s2,e);let m2=ps2.len();if m2==0{continue}let row2=replace(row,&e.anchors[p1],t);assert_eq!(sig(&row2,e),s2);let product=m1*m2;assert_eq!(U%product as i128,0);let unit=U/product as i128;for p2 in ps2{let key=RKey{profile:profile(&row2,p2,e),sig:s2,pivot:p2 as u8,degree:4};let z=if let Some(&x)=cache.get(&key){x}else{resp(&row2,s2,p2,4,e,cache)};assert_eq!((z.2,z.3),(60,60));assert_eq!(z.0,z.1);for tail in &e.tails[p2][2]{assert!(avail(child_sig(s2,p2,tail,e),e).is_empty())}if z.0!=0{return Some(format!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",v,hx(row),hx(&row2),p1,t1,p2,m1,m2,z.0,unit,v*unit*z.0 as i128,4))}}}}None}

pub fn run(){let a:Vec<_>=std::env::args().collect();let mut output="/tmp/k24_k16_r44_support_candidates.tsv".to_string();let mut report="/tmp/k24_k16_r44_support_census.json".to_string();let mut i=1;while i<a.len(){match a[i].as_str(){"--output"=>{output=a[i+1].clone();i+=2},"--report"=>{report=a[i+1].clone();i+=2},_=>panic!("bad argument")}}let begun=Instant::now();let e=parse();let f=File::open(INPUT).unwrap();let mut rd=BufReader::with_capacity(4<<20,f);let mut rows=Vec::new();let mut scanned=0u64;let mut slot=0usize;let mut counts=Vec::new();for bin in 0..37u64{let quota=if bin<35{7}else{6};let start=lo(bin);let end=lo(bin+1).min(N);rd.seek(SeekFrom::Start(16+32*start)).unwrap();let mut found=0usize;let mut cache=HashMap::new();for index in start..end{let mut b=[0u8;32];rd.read_exact(&mut b).unwrap();scanned+=1;let mut rr=[0u8;24];rr.copy_from_slice(&b[..24]);let row=Row(rr);let v=i64::from_le_bytes(b[24..].try_into().unwrap())as i128;if let Some(w)=first_nonzero(&row,v,&e,&mut cache){rows.push(format!("{}\t{}\t{}\t{}",slot,bin,index,w));slot+=1;found+=1;if found==quota{break}}}assert_eq!(found,quota,"support bin {} did not realize quota",bin);counts.push(format!("\"{}\":{}",bin,found))}assert_eq!(slot,257);let header="candidate_slot\tsupport_bin\trecord_index\tcoefficient\tsource_row\tintermediate_row\tp1\tt1\tp2\tm1\tm2\tterminal_q\tunit_scaled_U\tnonzero_contribution_scaled_U\tfinal_degree";let tmp=format!("{}.tmp",output);std::fs::write(&tmp,format!("{}\n{}\n",header,rows.join("\n"))).unwrap();rename(tmp,&output).unwrap();let elapsed=begun.elapsed().as_secs_f64();assert!(elapsed<60.0);let text=format!("{{\n  \"status\":\"PASS_K24_K16_R44_READ_ONLY_SUPPORT_CENSUS\",\n  \"realized_support_bins\":[{}],\n  \"quota_by_bin\":{{{}}},\n  \"candidate_count\":257,\n  \"records_scanned\":{},\n  \"candidate_ledger\":\"{}\",\n  \"all_nonzero\":true,\n  \"all_terminal\":true,\n  \"scalar_charge_accumulated\":false,\n  \"elapsed_seconds\":{:.6}\n}}\n",(0..37).map(|x|x.to_string()).collect::<Vec<_>>().join(","),counts.join(","),scanned,output,elapsed);let tmp_r=format!("{}.tmp",report);std::fs::write(&tmp_r,&text).unwrap();rename(tmp_r,&report).unwrap();print!("{}",text)}
}
fn main(){census::run()}
