mod audit {
 #![allow(dead_code)]
 include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");
 use std::fs::File;use std::io::{Read,Seek,SeekFrom};
 const P:&str="computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/checkpoint_k15_k3_profiles_merged.bin";
 const SAMPLE_PATH:&str="computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/k15_k3_group_charge_samples.tsv";
 const O:&str="computations/unaudited-codex-orbit0-k15-k3-full-export-plan-2026-08-23/results_k15_group_charge_sample_referee.json";
 const H:u64=128;const R:u64=104;const U:i128=400_591_699_200;
 fn dec(s:&str)->Vec<u8>{assert_eq!(s.len()%2,0);(0..s.len()).step_by(2).map(|i|u8::from_str_radix(&s[i..i+2],16).unwrap()).collect()}
 pub fn run(){let e=parse();let text=std::fs::read_to_string(SAMPLE_PATH).unwrap();let mut f=File::open(P).unwrap();let(mut n,mut packets)=(0u64,[0u64;3]);let mut seen=std::collections::BTreeSet::new();let mut last=0u64;
  for line in text.lines().skip(1){let x:Vec<_>=line.split('\t').collect();assert_eq!(x.len(),9);let index:u64=x[0].parse().unwrap();assert!(seen.insert(index));last=last.max(index);let key=dec(x[1]);assert_eq!(key.len(),42);let ew:i128=x[2].parse().unwrap();let eu:u64=x[3].parse().unwrap();let efq:i64=x[4].parse().unwrap();let eiq:i64=x[5].parse().unwrap();let einn:u64=x[6].parse().unwrap();let epacket:usize=x[7].parse().unwrap();let esource:u64=x[8].parse().unwrap();
   f.seek(SeekFrom::Start(H+R*index)).unwrap();let mut b=[0u8;104];f.read_exact(&mut b).unwrap();assert_eq!(&b[..42],&key);let weight=i128::from_le_bytes(b[42..58].try_into().unwrap());let uses=u64::from_le_bytes(b[58..66].try_into().unwrap());assert_eq!((weight,uses),(ew,eu));let mut rr=[0u8;24];rr.copy_from_slice(&b[66..90]);let row=Row(rr);let source=u64::from_le_bytes(b[90..98].try_into().unwrap());let p1=b[98]as usize;let t1=b[99]as usize;let p=b[100]as usize;let(m1,m2)=(b[101]as i128,b[102]as usize);let packet=b[103]as usize;assert_eq!((packet,source),(epacket,esource));assert!(packet<3&&source<485&&p1<78&&t1<32);assert_eq!(p,b[41]as usize);let s=sig(&row,&e);assert_eq!(&s[..],&b[29..41]);assert_eq!(&profile(&row,p,&e)[..],&b[..29]);let ps=avail(s,&e);assert_eq!(ps.len(),m2);assert!(ps.contains(&p));assert!(m1>0&&U%(m1*m2 as i128)==0);
   let(mut fq,mut iq,mut inn)=(0i64,0i64,0u64);for t in&e.tails[p][0]{let child=replace(&row,&e.anchors[p],t);let q=charge(&child,&e);fq+=q;if avail(child_sig(s,p,t,&e),&e).is_empty(){iq+=q;inn+=1}}assert_eq!((fq,iq,inn),(efq,eiq,einn));packets[packet]+=1;n+=1;
  }
  assert_eq!(n,256);assert_eq!(last,25_500_000);assert!(packets.iter().all(|&x|x>0));let out=format!("{{\"status\":\"PASS_ALL_256_LITERAL_CHARGE_SAMPLE_REPLAY\",\"samples\":{},\"packet_histogram\":{{\"322_packet0\":{},\"232_packet1\":{},\"223_packet2\":{}}},\"last_record_index\":{},\"scale_U\":\"{}\"}}\n",n,packets[0],packets[1],packets[2],last,U);std::fs::write(O,&out).unwrap();print!("{}",out)
 }
}
fn main(){audit::run()}
