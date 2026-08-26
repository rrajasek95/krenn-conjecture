//! Exact external merge of the 31 sorted labelled parent-profile runs.
use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::convert::TryInto;
use std::fs::{File,rename};
use std::io::{BufReader,BufWriter,Read,Write,Seek,SeekFrom};
use std::path::Path;
use std::time::Instant;

const DIR:&str="computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/";
const U:i128=400_591_699_200;
#[derive(Clone,Copy,Eq,Ord,PartialEq,PartialOrd)]struct Key([u8;43]);
struct Run{reader:BufReader<File>,remaining:u64}
impl Run{fn open(path:&str,start:u16,end:u16)->Self{let mut reader=BufReader::with_capacity(1<<20,File::open(path).unwrap());let mut h=[0u8;40];reader.read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"H16PF2\0\0");assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()),U);assert_eq!((u16::from_le_bytes(h[24..26].try_into().unwrap()),u16::from_le_bytes(h[26..28].try_into().unwrap()),u16::from_le_bytes(h[28..30].try_into().unwrap())),(start,end,59));let remaining=u64::from_le_bytes(h[32..40].try_into().unwrap());Self{reader,remaining}}fn next(&mut self)->Option<(Key,i128)>{if self.remaining==0{return None}let mut k=[0;43];let mut v=[0;16];self.reader.read_exact(&mut k).unwrap();self.reader.read_exact(&mut v).unwrap();self.remaining-=1;Some((Key(k),i128::from_le_bytes(v)))}}
fn main(){let begun=Instant::now();let mut runs=Vec::new();for start in(0..485usize).step_by(16){let end=(start+16).min(485);runs.push(Run::open(&format!("{}profiles_{:03}_{:03}.bin",DIR,start,end),start as u16,end as u16))}
 let mut heap:BinaryHeap<Reverse<(Key,usize,i128)>>=BinaryHeap::new();for(i,r)in runs.iter_mut().enumerate(){if let Some((k,v))=r.next(){heap.push(Reverse((k,i,v)))}}
 let final_path=format!("{}hidden_k16_second_pivot_profiles_full.bin",DIR);let tmp=format!("{}.tmp",final_path);let mut w=BufWriter::with_capacity(1<<20,File::create(&tmp).unwrap());w.write_all(b"H16MER2\0").unwrap();w.write_all(&U.to_le_bytes()).unwrap();w.write_all(&0u64.to_le_bytes()).unwrap();
 let(mut input,mut distinct,mut output,mut zero,mut input_sum,mut output_sum)=(0u64,0u64,0u64,0u64,0i128,0i128);let mut prior=None;let mut sum=0i128;
 while let Some(Reverse((key,i,value)))=heap.pop(){input+=1;input_sum+=value;if prior==Some(key){sum+=value}else{if let Some(k)=prior{distinct+=1;if sum!=0{w.write_all(&k.0).unwrap();w.write_all(&sum.to_le_bytes()).unwrap();output+=1;output_sum+=sum}else{zero+=1}}prior=Some(key);sum=value}if let Some((k,v))=runs[i].next(){heap.push(Reverse((k,i,v)))}}
 if let Some(k)=prior{distinct+=1;if sum!=0{w.write_all(&k.0).unwrap();w.write_all(&sum.to_le_bytes()).unwrap();output+=1;output_sum+=sum}else{zero+=1}}assert_eq!(input_sum,output_sum);assert_eq!(distinct,output+zero);w.flush().unwrap();let mut f=w.into_inner().unwrap();f.seek(SeekFrom::Start(24)).unwrap();f.write_all(&output.to_le_bytes()).unwrap();f.sync_all().unwrap();drop(f);rename(tmp,final_path).unwrap();let text=format!("{{\"status\":\"PASS_EXACT_EXTERNAL_MERGE\",\"input_runs\":{},\"input_records\":{},\"distinct_keys_before_zero\":{},\"exact_zero_keys\":{},\"output_nonzero_profiles\":{},\"input_weight_sum_scaled\":\"{}\",\"output_weight_sum_scaled\":\"{}\",\"output_bytes\":{},\"elapsed_seconds\":{:.6}}}\n",runs.len(),input,distinct,zero,output,input_sum,output_sum,32+59*output,begun.elapsed().as_secs_f64());let jt=format!("{}results_profile_merge.json.tmp",DIR);let jf=format!("{}results_profile_merge.json",DIR);std::fs::write(&jt,&text).unwrap();rename(jt,jf).unwrap();print!("{}",text)}
