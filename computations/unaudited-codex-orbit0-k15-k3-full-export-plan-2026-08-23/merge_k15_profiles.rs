use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::convert::TryInto;
use std::fs::{File,metadata,read_dir,rename};
use std::io::{BufReader,BufWriter,Read,Seek,SeekFrom,Write};
use std::path::Path;
use std::time::Instant;

const DIR:&str="computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/";
const U:i128=400_591_699_200;
const IH:usize=96;const OH:usize=128;const REC:usize=104;
const EXPECT_RECORDS:u64=202_344_547;const EXPECT_SOURCE_USES:u64=2_358_046_720;
const GATE:f64=600.0;

#[derive(Clone,Copy,Eq,Ord,PartialEq,PartialOrd)]struct Key([u8;42]);
#[derive(Clone,Copy)]struct Record{key:Key,weight:i128,uses:u64,witness:[u8;38]}
struct Input{r:BufReader<File>,source:u64,count:u64,expected_uses:u64,expected_weight:i128,seen:u64,uses:u64,weight:i128,prior:Option<Key>}
fn u16le(x:&[u8])->u16{u16::from_le_bytes(x.try_into().unwrap())}fn u32le(x:&[u8])->u32{u32::from_le_bytes(x.try_into().unwrap())}fn u64le(x:&[u8])->u64{u64::from_le_bytes(x.try_into().unwrap())}fn i128le(x:&[u8])->i128{i128::from_le_bytes(x.try_into().unwrap())}
fn input_path(n:usize)->String{format!("{}stage{}_shards/record_{:03}_attempt_000.part000000.bin",DIR,if n<242{1}else{2},n)}
fn open_input(n:usize)->Input{let path=input_path(n);let mut r=BufReader::with_capacity(1<<18,File::open(&path).unwrap());let mut h=[0u8;IH];r.read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"K18PRF2\0");assert_eq!(u32le(&h[8..12]),2);assert_eq!((h[12],h[13]),(2,2));assert_eq!(u16le(&h[14..16])as usize,REC);assert_eq!(u64le(&h[16..24]),U as u64);assert_eq!(u64le(&h[24..32]),0);let count=u64le(&h[32..40]);let uses=u64le(&h[40..48]);let weight=i128le(&h[48..64]);assert!(h[64..].iter().all(|&x|x==0));assert_eq!(metadata(&path).unwrap().len(),IH as u64+REC as u64*count);Input{r,source:n as u64,count,expected_uses:uses,expected_weight:weight,seen:0,uses:0,weight:0,prior:None}}
impl Input{fn next(&mut self)->Option<Record>{if self.seen==self.count{assert_eq!((self.uses,self.weight),(self.expected_uses,self.expected_weight));return None}let mut x=[0u8;REC];self.r.read_exact(&mut x).unwrap();let mut k=[0;42];k.copy_from_slice(&x[..42]);let key=Key(k);if let Some(p)=self.prior{assert!(p<key)}self.prior=Some(key);let weight=i128le(&x[42..58]);let uses=u64le(&x[58..66]);assert_ne!(weight,0);assert!(uses>0);let mut witness=[0;38];witness.copy_from_slice(&x[66..]);assert_eq!(u64le(&witness[24..32]),self.source);assert_eq!(witness[34],key.0[41]);let m1=witness[35]as i128;let m2=witness[36]as i128;assert!(m1>0&&m2>0&&U%(m1*m2)==0);assert!(witness[37]<3);self.seen+=1;self.uses+=uses;self.weight+=weight;Some(Record{key,weight,uses,witness})}}
fn write_record<W:Write>(w:&mut W,x:Record){w.write_all(&x.key.0).unwrap();w.write_all(&x.weight.to_le_bytes()).unwrap();w.write_all(&x.uses.to_le_bytes()).unwrap();w.write_all(&x.witness).unwrap()}
fn count_parts(dir:&str)->usize{read_dir(dir).unwrap().filter_map(Result::ok).filter(|x|{let s=x.file_name();let s=s.to_string_lossy();s.contains(".part")&&s.ends_with(".bin")}).count()}
fn main(){let begun=Instant::now();assert_eq!(count_parts(&format!("{}stage1_shards",DIR)),242);assert_eq!(count_parts(&format!("{}stage2_shards",DIR)),243);let out=format!("{}checkpoint_k15_k3_profiles_merged.bin",DIR);let tmp=format!("{}.tmp",out);assert!(!Path::new(&out).exists());assert!(!Path::new(&tmp).exists());
 let mut inputs:Vec<_>=(0..485).map(open_input).collect();let mut heap:BinaryHeap<Reverse<(Key,usize)>>=BinaryHeap::new();let mut current:Vec<Option<Record>>=Vec::with_capacity(485);for(i,x)in inputs.iter_mut().enumerate(){let q=x.next();if let Some(r)=q{heap.push(Reverse((r.key,i)))}current.push(q)}
 let mut w=BufWriter::with_capacity(8<<20,File::create(&tmp).unwrap());w.write_all(&[0u8;OH]).unwrap();let(mut input_records,mut input_uses,mut input_weight)=(0u64,0u64,0i128);let(mut output_records,mut output_uses,mut output_weight,mut zeros,mut zero_uses)=(0u64,0u64,0i128,0u64,0u64);let mut last_out=None;
 while let Some(Reverse((key,i)))=heap.pop(){let mut a=current[i].take().unwrap();assert!(a.key==key);input_records+=1;input_uses+=a.uses;input_weight+=a.weight;current[i]=inputs[i].next();if let Some(q)=current[i]{heap.push(Reverse((q.key,i)))}while let Some(Reverse((k,j)))=heap.peek().copied(){if k!=key{break}heap.pop();let b=current[j].take().unwrap();input_records+=1;input_uses+=b.uses;input_weight+=b.weight;a.weight+=b.weight;a.uses+=b.uses;if b.witness<a.witness{a.witness=b.witness}current[j]=inputs[j].next();if let Some(q)=current[j]{heap.push(Reverse((q.key,j)))}}
   if a.weight==0{zeros+=1;zero_uses+=a.uses}else{if let Some(p)=last_out{assert!(p<a.key)}last_out=Some(a.key);output_records+=1;output_uses+=a.uses;output_weight+=a.weight;write_record(&mut w,a)}
   if input_records%20_000_000==0{eprintln!("CHECKPOINT input={} output={} zeros={} elapsed={:.1}",input_records,output_records,zeros,begun.elapsed().as_secs_f64());assert!(begun.elapsed().as_secs_f64()<580.0)}
 }
 assert_eq!(input_records,EXPECT_RECORDS);assert_eq!(input_uses,EXPECT_SOURCE_USES);assert_eq!(input_weight,output_weight);assert_eq!(output_uses+zero_uses,input_uses);for x in&inputs{assert_eq!(x.seen,x.count);assert_eq!((x.uses,x.weight),(x.expected_uses,x.expected_weight))}
 let mut f=w.into_inner().unwrap();let mut h=[0u8;OH];h[..8].copy_from_slice(b"K15MRG1\0");h[8..12].copy_from_slice(&1u32.to_le_bytes());h[12..14].copy_from_slice(&(REC as u16).to_le_bytes());h[16..32].copy_from_slice(&U.to_le_bytes());h[32..40].copy_from_slice(&485u64.to_le_bytes());h[40..48].copy_from_slice(&input_records.to_le_bytes());h[48..56].copy_from_slice(&input_uses.to_le_bytes());h[56..64].copy_from_slice(&output_records.to_le_bytes());h[64..72].copy_from_slice(&zeros.to_le_bytes());h[72..80].copy_from_slice(&output_uses.to_le_bytes());h[80..96].copy_from_slice(&input_weight.to_le_bytes());h[96..112].copy_from_slice(&output_weight.to_le_bytes());h[112..120].copy_from_slice(&EXPECT_SOURCE_USES.to_le_bytes());h[120..128].copy_from_slice(&zero_uses.to_le_bytes());f.seek(SeekFrom::Start(0)).unwrap();f.write_all(&h).unwrap();f.sync_all().unwrap();drop(f);rename(&tmp,&out).unwrap();assert_eq!(metadata(&out).unwrap().len(),OH as u64+REC as u64*output_records);assert!(begun.elapsed().as_secs_f64()<GATE);
 println!("PASS input_parts=485 input_records={} input_uses={} input_weight={} output_records={} output_uses={} zero_uses={} output_weight={} zero_groups={} bytes={} elapsed={:.6}",input_records,input_uses,input_weight,output_records,output_uses,zero_uses,output_weight,zeros,metadata(&out).unwrap().len(),begun.elapsed().as_secs_f64())}
