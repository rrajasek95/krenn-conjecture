//! Independent 257-slice literal continuation referee for grouped D15 R2-2-2.
mod referee {
#![allow(dead_code,unused_imports)]
include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
const U21:i128=400_591_699_200;
const SLICES:usize=485;
const OUT:&str="computations/unaudited-codex-orbit0-k21-d15-r2-2-2-charge-2026-08-24/results_k21_d15_r2_2_2_samples.json";
const TSV:&str="computations/unaudited-codex-orbit0-k21-d15-r2-2-2-charge-2026-08-24/k21_d15_r2_2_2_samples.tsv";

fn packet_row(r:&R8,packet:usize,a:&[u8;4],b:&[u8;4],c:&[u8;4])->Row{
 match packet{0=>make(r,c,a,b),1=>make(r,a,c,b),2=>make(r,a,b,c),_=>unreachable!()}
}
struct W{a:usize,b:usize,c:usize,p1:usize,t1:usize,m1:usize,p2:usize,t2:usize,m2:usize,m3:usize,k21:usize,q:i64,scaled:i128}
fn witness(e:&E,r:&R8,packet:usize)->W{
 let other:Vec<_>=(0..3).filter(|&x|x!=packet).collect();
 for(ai,a)in e.factor[other[0]][0].iter().enumerate(){for(bi,b)in e.factor[other[1]][0].iter().enumerate(){for(ci,c)in e.factor[packet][1].iter().enumerate(){
  let row15=packet_row(r,packet,a,b,c);let s15=sig(&row15,e);assert_eq!(s15.iter().map(|&x|x as usize).sum::<usize>(),9);let ps1=avail(s15,e);let m1=ps1.len();assert!(m1>0);
  for &p1 in &ps1{for(ti1,t1)in e.tails[p1][0].iter().enumerate(){let row17=replace(&row15,&e.anchors[p1],t1);let s17=child_sig(s15,p1,t1,e);assert_eq!(sig(&row17,e),s17);assert_eq!(s17.iter().map(|&x|x as usize).sum::<usize>(),7);let ps2=avail(s17,e);let m2=ps2.len();if m2==0{continue}
   for &p2 in &ps2{for(ti2,t2)in e.tails[p2][0].iter().enumerate(){let row19=replace(&row17,&e.anchors[p2],t2);let s19=child_sig(s17,p2,t2,e);assert_eq!(sig(&row19,e),s19);assert_eq!(s19.iter().map(|&x|x as usize).sum::<usize>(),5);let ps3=avail(s19,e);let m3=ps3.len();if m3==0{continue}
    let mut q=0i64;let mut k21=0usize;for &p3 in &ps3{for t3 in &e.tails[p3][0]{let row21=replace(&row19,&e.anchors[p3],t3);let s21=child_sig(s19,p3,t3,e);assert_eq!(sig(&row21,e),s21);assert_eq!(s21.iter().map(|&x|x as usize).sum::<usize>(),3);assert!(avail(s21,e).is_empty());q+=charge(&row21,e);k21+=1}}
    assert_eq!(k21,12*m3);let denom=(m1*m2*m3)as i128;assert_eq!(U21%denom,0);let positive=(r.coefficient as i128)*(r.size as i128);return W{a:ai,b:bi,c:ci,p1,t1:ti1,m1,p2,t2:ti2,m2,m3,k21,q,scaled:positive*(U21/denom)*(q as i128)}
   }}
  }}
 }}}
 panic!("no nonzero K19-to-K21 continuation for distributed source slice")
}
pub fn run(){let begun=Instant::now();let e=parse();assert_eq!(e.records.len(),SLICES);let labels=["322","232","223"];let mut lines=vec!["ordinal\tsource_slice\tpacket\tlineage_witness\ta\tb\tc\tp1\tt1\tm1\tp2\tt2\tm2\tm3\tK21_children\tliteral_charge\tweighted_charge_scaled_U".to_string()];let(mut children,mut qsum,mut scaled)=(0usize,0i64,0i128);let mut packets=[0usize;3];
 for j in 0..257{let ri=j*(SLICES-1)/256;let packet=j%3;let w=witness(&e,&e.records[ri],packet);packets[packet]+=1;children+=w.k21;qsum+=w.q;scaled+=w.scaled;lines.push(format!("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}",j,ri,packet,labels[packet],w.a,w.b,w.c,w.p1,w.t1,w.m1,w.p2,w.t2,w.m2,w.m3,w.k21,w.q,w.scaled));}
 assert_eq!(lines.len(),258);assert_eq!(packets,[86,86,85]);let text=format!("{{\n  \"status\":\"PASS_INDEPENDENT_257_DISTRIBUTED_NONZERO_LITERAL_D15_R_2_2_2_K21_REPLAY\",\n  \"strict_grouped_ids\":[\"D15:223|R:2-2-2\",\"D15:232|R:2-2-2\",\"D15:322|R:2-2-2\"],\n  \"source_slices\":257,\n  \"first_slice\":0,\n  \"last_slice\":484,\n  \"packet_witness_counts\":{{\"322\":{},\"232\":{},\"223\":{}}},\n  \"nonzero_K19_to_K21_continuations\":257,\n  \"literal_terminal_K21_children\":{},\n  \"literal_charge_sum\":\"{}\",\n  \"sample_weighted_charge_scaled_U\":\"{}\",\n  \"all_divisions_exact\":true,\n  \"all_K21_children_terminal\":true,\n  \"source_provenance_preserved_through_both_prior_pivots\":true,\n  \"elapsed_seconds\":{:.6},\n  \"scope\":\"257 distributed nonzero literal continuations only; not a second full scalar pass and no K22\"\n}}\n",packets[0],packets[1],packets[2],children,qsum,scaled,begun.elapsed().as_secs_f64());std::fs::write(TSV,format!("{}\n",lines.join("\n"))).unwrap();std::fs::write(OUT,&text).unwrap();print!("{}",text)}
}
fn main(){referee::run()}
