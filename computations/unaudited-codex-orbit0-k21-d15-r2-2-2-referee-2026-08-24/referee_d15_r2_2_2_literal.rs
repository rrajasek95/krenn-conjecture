//! Bounded independent literal-continuation referee for grouped D15 R2-2-2.
mod replay {
#![allow(dead_code, unused_imports)]
include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
use std::collections::BTreeMap;

const U:i128=400_591_699_200;
const SLICES:usize=485;
const PER_PACKET:usize=12*12*32;
const PER_SLICE:usize=3*PER_PACKET;
const N:usize=SLICES*PER_SLICE;
const OUT:&str="computations/unaudited-codex-orbit0-k21-d15-r2-2-2-referee-2026-08-24/samples_d15_r2_2_2_literal.tsv";
const RESULT:&str="computations/unaudited-codex-orbit0-k21-d15-r2-2-2-referee-2026-08-24/results_d15_r2_2_2_literal_referee.json";

fn rowhex(r:&Row)->String{r.0.iter().map(|x|format!("{:02x}",x)).collect()}
fn packet_row(r:&R8,packet:usize,a:&[u8;4],b:&[u8;4],c:&[u8;4])->Row{
 match packet{0=>make(r,c,a,b),1=>make(r,a,c,b),2=>make(r,a,b,c),_=>unreachable!()}
}
fn source_head(index:usize,e:&E)->(usize,usize,Row,i128){
 let(ri,within)=(index/PER_SLICE,index%PER_SLICE);let(packet,z)=(within/PER_PACKET,within%PER_PACKET);
 let(ai,rem)=(z/(12*32),z%(12*32));let(bi,ci)=(rem/32,rem%32);
 let other:Vec<_>=(0..3).filter(|&x|x!=packet).collect();let r=&e.records[ri];
 let row=packet_row(r,packet,&e.factor[other[0]][0][ai],&e.factor[other[1]][0][bi],&e.factor[packet][1][ci]);
 (ri,packet,row,(r.coefficient as i128)*(r.size as i128))
}
#[derive(Clone)]struct W{index:usize,ri:usize,packet:usize,row15:Row,row17:Row,row19:Row,p1:usize,t1:usize,p2:usize,t2:usize,p3:usize,m1:usize,m2:usize,m3:usize,q:i64,unit:i128}
fn witness(index:usize,e:&E)->Option<W>{let(ri,packet,row15,positive)=source_head(index,e);let s15=sig(&row15,e);assert_eq!(s15.iter().map(|&x|x as usize).sum::<usize>(),9);let ps1=avail(s15,e);let m1=ps1.len();assert!(m1>0);
 for p1 in ps1{for(t1,tail1)in e.tails[p1][0].iter().enumerate(){let s17=child_sig(s15,p1,tail1,e);assert_eq!(s17.iter().map(|&x|x as usize).sum::<usize>(),7);let ps2=avail(s17,e);if ps2.is_empty(){continue}let m2=ps2.len();let row17=replace(&row15,&e.anchors[p1],tail1);assert_eq!(sig(&row17,e),s17);
  for p2 in ps2{for(t2,tail2)in e.tails[p2][0].iter().enumerate(){let s19=child_sig(s17,p2,tail2,e);assert_eq!(s19.iter().map(|&x|x as usize).sum::<usize>(),5);let ps3=avail(s19,e);if ps3.is_empty(){continue}let m3=ps3.len();let product=m1*m2*m3;assert_eq!(U%(product as i128),0);let unit=positive*U/(product as i128);let row19=replace(&row17,&e.anchors[p2],tail2);assert_eq!(sig(&row19,e),s19);
   for p3 in ps3{let mut q=0i64;let mut n=0;for tail3 in &e.tails[p3][0]{let s21=child_sig(s19,p3,tail3,e);assert_eq!(s21.iter().map(|&x|x as usize).sum::<usize>(),3);assert!(avail(s21,e).is_empty());let row21=replace(&row19,&e.anchors[p3],tail3);assert_eq!(sig(&row21,e),s21);q+=charge(&row21,e);n+=1}assert_eq!(n,12);if q!=0{return Some(W{index,ri,packet,row15,row17,row19,p1,t1,p2,t2,p3,m1,m2,m3,q,unit})}}
  }}
 }}None}
pub fn run(){let begun=std::time::Instant::now();let e=parse();assert_eq!(e.records.len(),SLICES);assert!(e.piv.iter().all(|p|p.iter().map(|&x|x as usize).sum::<usize>()==4));assert!(e.tails.iter().all(|x|x[0].iter().all(|t|tsig(t,&e).iter().map(|&z|z as usize).sum::<usize>()==2)));
 let mut lines=vec!["sample_bin\thead_index\tr8_index\tpacket\trow15\trow17\trow19\tp1\tt1\tp2\tt2\tp3\tm1\tm2\tm3\tterminal_q\tunit_scaled_U\tnonzero_contribution_scaled_U".to_string()];let mut packets=BTreeMap::new();let(mut scanned,mut max_scan)=(0usize,0usize);
 for bin in 0..257{let start=(bin*N+256)/257;let end=((bin+1)*N+256)/257;let mut got=None;for index in start..end{scanned+=1;if let Some(w)=witness(index,&e){max_scan=max_scan.max(index-start+1);got=Some(w);break}}let w=got.unwrap_or_else(||panic!("no nonzero continuation in bin {}",bin));*packets.entry(w.packet).or_insert(0usize)+=1;lines.push(format!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",bin,w.index,w.ri,w.packet,rowhex(&w.row15),rowhex(&w.row17),rowhex(&w.row19),w.p1,w.t1,w.p2,w.t2,w.p3,w.m1,w.m2,w.m3,w.q,w.unit,w.unit*(w.q as i128)))}
 std::fs::write(OUT,format!("{}\n",lines.join("\n"))).unwrap();let elapsed=begun.elapsed().as_secs_f64();let result=format!(concat!("{{\n  \"status\":\"PASS_INDEPENDENT_257_NONZERO_LITERAL_D15_R2_2_2_REFEREE\",\n  \"samples\":257,\n  \"source_grid_heads\":{},\n  \"sample_bins\":257,\n  \"scanned_heads\":{},\n  \"maximum_scan_within_bin\":{},\n  \"literal_terminal_children\":{},\n  \"all_terminal_children_irreducible\":true,\n  \"all_denominator_products_divide_U\":true,\n  \"all_sample_contributions_nonzero\":true,\n  \"packet_sample_counts\":{{\"322\":{},\"232\":{},\"223\":{}}},\n  \"ledger\":\"{}\",\n  \"elapsed_seconds\":{:.6},\n  \"scope\":\"257 distributed nonzero literal continuations only; no full fold rerun and no individual packet scalar claim\"\n}}\n"),N,scanned,max_scan,257*12,packets.get(&0).unwrap_or(&0),packets.get(&1).unwrap_or(&0),packets.get(&2).unwrap_or(&0),OUT,elapsed);std::fs::write(RESULT,&result).unwrap();print!("{}",result)}
}
fn main(){replay::run()}
