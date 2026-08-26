use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::convert::TryInto;
use std::fs::{File,metadata,read_dir};
use std::io::{BufReader,Read};
use std::time::Instant;

const DIR:&str="computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/";
const OUT:&str="computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/checkpoint_k15_k3_profiles_merged.bin";
const IH:usize=96;const OH:usize=128;const REC:usize=104;const U:i128=400_591_699_200;
#[derive(Clone,Copy,Debug,Eq,Ord,PartialEq,PartialOrd)]struct Key([u8;42]);
#[derive(Clone,Copy,Debug,Eq,PartialEq)]struct Record{key:Key,weight:i128,uses:u64,witness:[u8;38]}
fn u16le(x:&[u8])->u16{u16::from_le_bytes(x.try_into().unwrap())}fn u32le(x:&[u8])->u32{u32::from_le_bytes(x.try_into().unwrap())}fn u64le(x:&[u8])->u64{u64::from_le_bytes(x.try_into().unwrap())}fn i128le(x:&[u8])->i128{i128::from_le_bytes(x.try_into().unwrap())}
fn path(n:usize)->String{format!("{}stage{}_shards/record_{:03}_attempt_000.part000000.bin",DIR,if n<242{1}else{2},n)}
fn decode(x:&[u8;REC])->Record{let mut k=[0;42];k.copy_from_slice(&x[..42]);let mut w=[0;38];w.copy_from_slice(&x[66..]);Record{key:Key(k),weight:i128le(&x[42..58]),uses:u64le(&x[58..66]),witness:w}}
struct Input{r:BufReader<File>,source:u64,n:u64,seen:u64,expect_uses:u64,expect_weight:i128,uses:u64,weight:i128,prior:Option<Key>}
impl Input{fn open(source:usize)->Self{let p=path(source);let mut r=BufReader::with_capacity(1<<17,File::open(&p).unwrap());let mut h=[0u8;IH];r.read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"K18PRF2\0");assert_eq!(u32le(&h[8..12]),2);assert_eq!((h[12],h[13],u16le(&h[14..16])as usize),(2,2,REC));assert_eq!(u64le(&h[16..24]),U as u64);let n=u64le(&h[32..40]);assert_eq!(metadata(p).unwrap().len(),IH as u64+REC as u64*n);Self{r,source:source as u64,n,seen:0,expect_uses:u64le(&h[40..48]),expect_weight:i128le(&h[48..64]),uses:0,weight:0,prior:None}}
fn next(&mut self)->Option<Record>{if self.seen==self.n{assert_eq!((self.uses,self.weight),(self.expect_uses,self.expect_weight));return None}let mut b=[0u8;REC];self.r.read_exact(&mut b).unwrap();let x=decode(&b);if let Some(p)=self.prior{assert!(p<x.key)}self.prior=Some(x.key);assert_ne!(x.weight,0);assert!(x.uses>0);assert_eq!(u64le(&x.witness[24..32]),self.source);assert_eq!(x.witness[34],x.key.0[41]);let(m1,m2)=(x.witness[35]as i128,x.witness[36]as i128);assert!(m1>0&&m2>0&&U%(m1*m2)==0);assert!(x.witness[37]<3);self.seen+=1;self.uses+=x.uses;self.weight+=x.weight;Some(x)}}
fn count_parts(d:&str)->usize{read_dir(d).unwrap().filter_map(Result::ok).filter(|x|{let s=x.file_name();let s=s.to_string_lossy();s.contains(".part")&&s.ends_with(".bin")}).count()}
fn main(){let begun=Instant::now();assert_eq!(count_parts(&format!("{}stage1_shards",DIR)),242);assert_eq!(count_parts(&format!("{}stage2_shards",DIR)),243);
 let mut out=BufReader::with_capacity(8<<20,File::open(OUT).unwrap());let mut oh=[0u8;OH];out.read_exact(&mut oh).unwrap();assert_eq!(&oh[..8],b"K15MRG1\0");assert_eq!((u32le(&oh[8..12]),u16le(&oh[12..14])as usize),(1,REC));assert_eq!(i128le(&oh[16..32]),U);let expected_out=u64le(&oh[56..64]);
 let mut ins:Vec<_>=(0..485).map(Input::open).collect();let mut cur=Vec::new();let mut heap=BinaryHeap::new();for(i,x)in ins.iter_mut().enumerate(){let q=x.next();if let Some(r)=q{heap.push(Reverse((r.key,i)))}cur.push(q)}
 let(mut ir,mut iu,mut iw)=(0u64,0u64,0i128);let(mut or,mut ou,mut ow,mut zg,mut zu)=(0u64,0u64,0i128,0u64,0u64);let mut prior=None;
 while let Some(Reverse((key,i)))=heap.pop(){let mut a=cur[i].take().unwrap();ir+=1;iu+=a.uses;iw+=a.weight;cur[i]=ins[i].next();if let Some(x)=cur[i]{heap.push(Reverse((x.key,i)))}while let Some(Reverse((k,j)))=heap.peek().copied(){if k!=key{break}heap.pop();let b=cur[j].take().unwrap();ir+=1;iu+=b.uses;iw+=b.weight;a.weight+=b.weight;a.uses+=b.uses;if b.witness<a.witness{a.witness=b.witness}cur[j]=ins[j].next();if let Some(x)=cur[j]{heap.push(Reverse((x.key,j)))}}
  if a.weight==0{zg+=1;zu+=a.uses}else{let mut b=[0u8;REC];out.read_exact(&mut b).unwrap();let actual=decode(&b);assert_eq!(actual,a);if let Some(p)=prior{assert!(p<a.key)}prior=Some(a.key);or+=1;ou+=a.uses;ow+=a.weight}
 }
 let mut tail=[0u8;1];assert_eq!(out.read(&mut tail).unwrap(),0);for x in&ins{assert_eq!(x.seen,x.n)}
 assert_eq!((ir,iu,iw),(202_344_547,2_358_046_720,1_865_098_870_468_588_339_200));assert_eq!((or,ou,ow),(25_564_391,2_311_887_188,iw));assert_eq!((zg,zu),(1_411_149,46_159_532));assert_eq!(or,expected_out);assert_eq!(ou+zu,iu);
 let text=format!("{{\"status\":\"PASS_FULL_485_WAY_STREAM_AND_BYTE_REPLAY\",\"input_parts\":485,\"input_records\":{},\"input_uses\":{},\"input_weight_scaled\":\"{}\",\"output_records\":{},\"output_uses\":{},\"output_weight_scaled\":\"{}\",\"exact_zero_groups\":{},\"exact_zero_uses\":{},\"elapsed_seconds\":{:.6}}}\n",ir,iu,iw,or,ou,ow,zg,zu,begun.elapsed().as_secs_f64());std::fs::write(format!("{}results_k15_merge_full_stream_referee.json",DIR),&text).unwrap();print!("{}",text)}
