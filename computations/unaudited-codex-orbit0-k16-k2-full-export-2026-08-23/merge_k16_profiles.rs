use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::convert::TryInto;
use std::fs::{File,metadata,rename};
use std::io::{BufReader,BufWriter,Read,Seek,SeekFrom,Write};
use std::path::Path;
use std::time::Instant;

const CAT:&str="computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/k16_merge_inputs.tsv";
const OUT:&str="computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/checkpoint_k16_k2_profiles_merged.bin";
const RESULT:&str="computations/unaudited-codex-orbit0-k16-k2-full-export-2026-08-23/results_k16_profile_merge.json";
const U:i128=400_591_699_200;
const IH:usize=96;const OH:usize=128;const REC:usize=104;
const EXPECT_PARTS:usize=281;const EXPECT_RECORDS:u64=63_918_401;
// The exporter counts every raw outgoing pivot use before its worker-local
// signed collection.  A locally cancelling key is deliberately absent from
// the part files, so the sum of the retained record `uses` fields is smaller.
// Keep both quantities explicit: the merge can replay the latter exactly,
// while the former remains a pinned source-generation statistic.
const EXPECT_COLLECTED_USES:u64=1_614_846_654;
const EXPECT_RAW_OUTGOING_USES:u64=2_049_974_172;
const EXPECT_WEIGHT:i128=3_218_269_567_887_566_438_400;

fn u16x(x:&[u8])->u16{u16::from_le_bytes(x.try_into().unwrap())}
fn u32x(x:&[u8])->u32{u32::from_le_bytes(x.try_into().unwrap())}
fn u64x(x:&[u8])->u64{u64::from_le_bytes(x.try_into().unwrap())}
fn i128x(x:&[u8])->i128{i128::from_le_bytes(x.try_into().unwrap())}

#[derive(Clone,Copy,Eq,Ord,PartialEq,PartialOrd)]struct Key([u8;42]);
#[derive(Clone,Copy)]struct Record{key:Key,weight:i128,uses:u64,witness:[u8;38]}
struct Input{r:BufReader<File>,count:u64,expected_uses:u64,expected_weight:i128,seen:u64,uses:u64,weight:i128,prior:Option<Key>}

impl Input{
 fn open(path:&str,expected_bytes:u64)->Self{
  assert_eq!(metadata(path).unwrap().len(),expected_bytes);
  let mut r=BufReader::with_capacity(1<<18,File::open(path).unwrap());let mut h=[0u8;IH];r.read_exact(&mut h).unwrap();
  assert_eq!(&h[..8],b"K18PRF2\0");assert_eq!(u32x(&h[8..12]),2);assert_eq!((h[12],h[13]),(3,2));assert_eq!(u16x(&h[14..16])as usize,REC);assert_eq!(u64x(&h[16..24]),U as u64);
  let count=u64x(&h[32..40]);assert_eq!(expected_bytes,IH as u64+REC as u64*count);
  Self{r,count,expected_uses:u64x(&h[40..48]),expected_weight:i128x(&h[48..64]),seen:0,uses:0,weight:0,prior:None}
 }
 fn next(&mut self)->Option<Record>{
  if self.seen==self.count{assert_eq!((self.uses,self.weight),(self.expected_uses,self.expected_weight));return None}
  let mut x=[0u8;REC];self.r.read_exact(&mut x).unwrap();let mut k=[0u8;42];k.copy_from_slice(&x[..42]);let key=Key(k);if let Some(p)=self.prior{assert!(p<key)}self.prior=Some(key);
  let weight=i128x(&x[42..58]);let uses=u64x(&x[58..66]);assert_ne!(weight,0);assert!(uses>0);
  let mut witness=[0u8;38];witness.copy_from_slice(&x[66..]);let source=u64x(&witness[24..32]);let(p1,t1,p2,m1,m2,packet)=(witness[32],witness[33],witness[34],witness[35]as i128,witness[36]as i128,witness[37]);
  assert!(source<24_097_095&&p1<78&&t1<12&&p2<78&&m1>0&&m2>0);assert_eq!(packet,255);assert_eq!(p2,key.0[41]);assert_eq!(U%(m1*m2),0);
  self.seen+=1;self.uses+=uses;self.weight+=weight;Some(Record{key,weight,uses,witness})
 }
}
fn write_record<W:Write>(w:&mut W,x:Record){w.write_all(&x.key.0).unwrap();w.write_all(&x.weight.to_le_bytes()).unwrap();w.write_all(&x.uses.to_le_bytes()).unwrap();w.write_all(&x.witness).unwrap()}

fn catalog()->Vec<(String,u64)>{
 let s=std::fs::read_to_string(CAT).unwrap();let mut it=s.lines();assert_eq!(it.next(),Some("path\tbytes\tsha256\tshard"));let mut v=Vec::new();
 for line in it{let q:Vec<_>=line.split('\t').collect();assert_eq!(q.len(),4);assert_eq!(q[2].len(),64);v.push((q[0].to_string(),q[1].parse().unwrap()))}
 assert_eq!(v.len(),EXPECT_PARTS);v
}

#[derive(Debug)]struct Stats{input_records:u64,input_uses:u64,input_weight:i128,output_records:u64,output_uses:u64,output_weight:i128,zero_groups:u64,zero_uses:u64}
fn merge(paths:&[(String,u64)],out:&str,expected:Option<(u64,u64,i128)>)->Stats{
 assert!(!Path::new(out).exists()&&!Path::new(&format!("{}.tmp",out)).exists());let begun=Instant::now();
 let mut inputs:Vec<_>=paths.iter().map(|(p,b)|Input::open(p,*b)).collect();let mut heap:BinaryHeap<Reverse<(Key,usize)>>=BinaryHeap::new();let mut current=Vec::new();
 for(i,x)in inputs.iter_mut().enumerate(){let q=x.next();if let Some(r)=q{heap.push(Reverse((r.key,i)))}current.push(q)}
 let tmp=format!("{}.tmp",out);let mut w=BufWriter::with_capacity(8<<20,File::create(&tmp).unwrap());w.write_all(&[0u8;OH]).unwrap();
 let(mut ir,mut iu,mut iw,mut or,mut ou,mut ow,mut zeros,mut zu)=(0u64,0u64,0i128,0u64,0u64,0i128,0u64,0u64);let mut last=None;
 while let Some(Reverse((key,i)))=heap.pop(){
  let mut a=current[i].take().unwrap();ir+=1;iu+=a.uses;iw+=a.weight;current[i]=inputs[i].next();if let Some(q)=current[i]{heap.push(Reverse((q.key,i)))}
  while let Some(Reverse((k,j)))=heap.peek().copied(){if k!=key{break}heap.pop();let b=current[j].take().unwrap();ir+=1;iu+=b.uses;iw+=b.weight;a.weight+=b.weight;a.uses+=b.uses;if b.witness<a.witness{a.witness=b.witness}current[j]=inputs[j].next();if let Some(q)=current[j]{heap.push(Reverse((q.key,j)))}}
  if a.weight==0{zeros+=1;zu+=a.uses}else{if let Some(p)=last{assert!(p<a.key)}last=Some(a.key);or+=1;ou+=a.uses;ow+=a.weight;write_record(&mut w,a)}
 }
 assert_eq!(iw,ow);assert_eq!(iu,ou+zu);if let Some(e)=expected{assert_eq!((ir,iu,iw),e)}
 let mut f=w.into_inner().unwrap();let mut h=[0u8;OH];h[..8].copy_from_slice(b"K16MRG1\0");h[8..12].copy_from_slice(&1u32.to_le_bytes());h[12..14].copy_from_slice(&(REC as u16).to_le_bytes());h[16..32].copy_from_slice(&U.to_le_bytes());h[32..40].copy_from_slice(&(paths.len()as u64).to_le_bytes());h[40..48].copy_from_slice(&ir.to_le_bytes());h[48..56].copy_from_slice(&iu.to_le_bytes());h[56..64].copy_from_slice(&or.to_le_bytes());h[64..72].copy_from_slice(&zeros.to_le_bytes());h[72..80].copy_from_slice(&ou.to_le_bytes());h[80..96].copy_from_slice(&iw.to_le_bytes());h[96..112].copy_from_slice(&ow.to_le_bytes());h[112..120].copy_from_slice(&zu.to_le_bytes());h[120..128].copy_from_slice(&EXPECT_RAW_OUTGOING_USES.to_le_bytes());f.seek(SeekFrom::Start(0)).unwrap();f.write_all(&h).unwrap();f.sync_all().unwrap();drop(f);rename(&tmp,out).unwrap();assert_eq!(metadata(out).unwrap().len(),OH as u64+REC as u64*or);
 eprintln!("PASS_MERGE parts={} input={} output={} zeros={} elapsed={:.3}",paths.len(),ir,or,zeros,begun.elapsed().as_secs_f64());Stats{input_records:ir,input_uses:iu,input_weight:iw,output_records:or,output_uses:ou,output_weight:ow,zero_groups:zeros,zero_uses:zu}
}
fn write_part(path:&str,part:u64,records:&[Record]){
 let mut h=[0u8;IH];h[..8].copy_from_slice(b"K18PRF2\0");h[8..12].copy_from_slice(&2u32.to_le_bytes());h[12]=3;h[13]=2;h[14..16].copy_from_slice(&(REC as u16).to_le_bytes());h[16..24].copy_from_slice(&(U as u64).to_le_bytes());h[24..32].copy_from_slice(&part.to_le_bytes());h[32..40].copy_from_slice(&(records.len()as u64).to_le_bytes());h[40..48].copy_from_slice(&(records.iter().map(|x|x.uses).sum::<u64>()).to_le_bytes());h[48..64].copy_from_slice(&(records.iter().map(|x|x.weight).sum::<i128>()).to_le_bytes());let mut w=File::create(path).unwrap();w.write_all(&h).unwrap();for&x in records{write_record(&mut w,x)}
}
fn rec(key:u8,weight:i128,uses:u64,witness0:u8)->Record{let mut k=[0u8;42];k[0]=key;k[41]=1;let mut w=[0u8;38];w[0]=witness0;w[34]=1;w[35]=1;w[36]=1;w[37]=255;Record{key:Key(k),weight,uses,witness:w}}
fn self_test(){let base=format!("/tmp/k16_merge_selftest_{}",std::process::id());std::fs::create_dir(&base).unwrap();let a=format!("{}/a.bin",base);let b=format!("{}/b.bin",base);let o=format!("{}/out.bin",base);let r1=[rec(1,5,1,9),rec(2,3,1,8)];let r2=[rec(1,-5,2,1),rec(3,7,1,7)];write_part(&a,0,&r1);write_part(&b,1,&r2);let s=merge(&[(a,metadata(format!("{}/a.bin",base)).unwrap().len()),(b,metadata(format!("{}/b.bin",base)).unwrap().len())],&o,Some((4,5,10)));assert_eq!((s.output_records,s.zero_groups,s.output_uses,s.zero_uses,s.output_weight),(2,1,2,3,10));std::fs::remove_dir_all(base).unwrap();println!("PASS_K16_281_WAY_MERGE_SELF_TEST")}
fn production(){let paths=catalog();let s=merge(&paths,OUT,Some((EXPECT_RECORDS,EXPECT_COLLECTED_USES,EXPECT_WEIGHT)));let text=format!("{{\n  \"status\":\"PASS_K16_281_WAY_SIGNED_PROFILE_MERGE\",\n  \"scope\":\"grouped six-ID K16/K2 merge only; source parts retained; no K21\",\n  \"scale_U\":\"{}\",\n  \"input_parts\":{},\n  \"input_records\":{},\n  \"raw_outgoing_pivot_uses\":{},\n  \"input_collected_uses\":{},\n  \"worker_local_cancelled_uses\":{},\n  \"input_weight_scaled\":\"{}\",\n  \"output_records\":{},\n  \"output_uses\":{},\n  \"output_weight_scaled\":\"{}\",\n  \"cross_part_exact_zero_groups\":{},\n  \"cross_part_exact_zero_group_uses\":{},\n  \"no_cleanup\":true\n}}\n",U,EXPECT_PARTS,s.input_records,EXPECT_RAW_OUTGOING_USES,s.input_uses,EXPECT_RAW_OUTGOING_USES-s.input_uses,s.input_weight,s.output_records,s.output_uses,s.output_weight,s.zero_groups,s.zero_uses);assert!(!Path::new(RESULT).exists());std::fs::write(RESULT,text).unwrap()}
fn main(){let a:Vec<_>=std::env::args().collect();match a.get(1).map(String::as_str){Some("--self-test")=>self_test(),Some("--merge")=>production(),_=>panic!("use --self-test or explicitly authorized --merge")}}
