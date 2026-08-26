// Measured, provenance-preserving prefix of the K14 -> K16 discarded subtree.
// This deliberately emits no K18/K19/K20 tail rows.  The parent stream stores
// each pivotable K16 occurrence before collection.  The profile stream stores
// the exact aggregated coefficient for each possible second-pivot environment.
include!("../unaudited-codex-orbit0-k19-profile-census-2026-08-23/run_k19_profile_census.rs");

use std::fs::{OpenOptions};
use std::io::{BufReader,Read,Seek,SeekFrom};

const OUT_PREFIX:&str="computations/unaudited-codex-orbit0-k14-hidden-k16-parent-prefix-2026-08-23/";
const STRUCTURE_PATH:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin";
const U:i128=400_591_699_200;
const SAMPLE_MOD:usize=16;

fn record_masses()->Vec<i128>{
    let b=read(STRUCTURE_PATH).unwrap();let mut p=11usize;
    let nt=u32le(&b[p..p+4])as usize;p+=4;let nr=u32le(&b[p..p+4])as usize;p+=4;
    let np=u32le(&b[p..p+4])as usize;p+=4;let na=u32le(&b[p..p+4])as usize;p+=4;
    assert_eq!((nt,nr,np,na),(384,485,78,12));p+=12+nt*(252+12);
    let mut out=Vec::new();
    for _ in 0..nr{p+=12;let size=u32le(&b[p..p+4])as i128;p+=4;let coefficient=i64::from_le_bytes(b[p..p+8].try_into().unwrap())as i128;p+=8;out.push(size*coefficient)}
    out
}
fn add_weight(map:&mut HashMap<Key,i128>,key:Key,value:i128){let x=map.entry(key).or_default();*x+=value;if *x==0{map.remove(&key);}}
fn atomic_writer(name:&str,magic:&[u8;8],scale:i128,modulus:u32,count_placeholder:bool)->(BufWriter<File>,String,String){
    let final_path=format!("{}{}",OUT_PREFIX,name);let tmp_path=format!("{}.tmp",final_path);
    let mut w=BufWriter::new(File::create(&tmp_path).unwrap());w.write_all(magic).unwrap();w.write_all(&scale.to_le_bytes()).unwrap();w.write_all(&modulus.to_le_bytes()).unwrap();w.write_all(&0u64.to_le_bytes()).unwrap();
    let _=count_placeholder;(w,tmp_path,final_path)
}
fn finish_counted(mut w:BufWriter<File>,tmp:String,final_path:String,count:u64){w.flush().unwrap();let mut f=w.into_inner().unwrap();f.seek(SeekFrom::Start(28)).unwrap();f.write_all(&count.to_le_bytes()).unwrap();f.sync_all().unwrap();drop(f);rename(tmp,final_path).unwrap()}

#[cfg(all(feature="hidden_k16_parent_prefix",not(feature="hidden_k16_full")))]
fn main(){
    std::fs::create_dir_all(OUT_PREFIX).unwrap();let begun=Instant::now();let e=parse();let masses=record_masses();assert_eq!(masses.len(),e.records.len());
    // Two deterministic tranches make the first half a nested 1/32 sample.
    let selected:Vec<usize>=(0..e.records.len()).filter(|i|i%32==0).chain((0..e.records.len()).filter(|i|i%32==16)).collect();
    assert_eq!(selected.len(),31);
    let(mut pw,ptmp,pfinal)=atomic_writer("hidden_k16_parents_prefix.bin",b"H16PAR1\0",U,SAMPLE_MOD as u32,true);
    let mut profiles:HashMap<Key,i128>=HashMap::new();let mut hidden=0u64;let mut heads=0u64;let mut first_uses=0u64;let mut outgoing=0u64;
    let mut m1hist=[0u64;79];let mut m2hist=[0u64;79];let mut phist:HashMap<u16,u64>=HashMap::new();
    let mut half=(0u64,0u64,0u64,0usize,0f64);
    for (slice_no,&ri) in selected.iter().enumerate(){let r=&e.records[ri];
        for (ia,a) in e.factor[0][0].iter().enumerate(){for(ib,b)in e.factor[1][0].iter().enumerate(){for(ic,c)in e.factor[2][0].iter().enumerate(){heads+=1;let head=make(r,a,b,c);let hs=sig(&head,&e);let ps=valid(hs,&e);let m1=ps.len();m1hist[m1]+=1;let mass=masses[ri];assert_eq!(mass*U%(m1 as i128),0);let w1=mass*U/(m1 as i128);
            for &p1 in &ps{first_uses+=1;for(t1,t)in e.tails[p1][0].iter().enumerate(){let row=replace(&head,&e.anchors[p1],t);let s=sig(&row,&e);let ps2=avail(s,&e);if ps2.is_empty(){continue}hidden+=1;let m2=ps2.len();m2hist[m2]+=1;assert_eq!(w1%(m2 as i128),0);let w2=-w1/(m2 as i128);*phist.entry((m1*m2)as u16).or_default()+=1;
                // Fixed 64-byte occurrence record: literal row, coefficient at U,
                // signature, and the complete source tuple.  Three zero bytes are
                // reserved for a versioned extension without record-size drift.
                pw.write_all(&row.0).unwrap();pw.write_all(&w1.to_le_bytes()).unwrap();pw.write_all(&s).unwrap();pw.write_all(&(ri as u16).to_le_bytes()).unwrap();pw.write_all(&[ia as u8,ib as u8,ic as u8,p1 as u8,t1 as u8,m1 as u8,m2 as u8,0,0,0]).unwrap();
                // The final key byte is zero: this is a wildcard parent
                // environment, not a K2-only child.  The same row/pivot can
                // subsequently emit the pinned K2, K3, or K4 tail table.
                for &p2 in &ps2{outgoing+=1;add_weight(&mut profiles,Key{profile:profile(&row,p2,&e),sig:s,pivot:p2 as u8,degree:0},w2)}
            }}
        }}}
        if slice_no+1==16{half=(hidden,outgoing,heads,profiles.len(),begun.elapsed().as_secs_f64())}
    }
    finish_counted(pw,ptmp,pfinal,hidden);
    let mut pv:Vec<_>=profiles.into_iter().filter(|(_,v)|*v!=0).collect();pv.sort_unstable_by_key(|x|x.0);let profile_weight_sum:i128=pv.iter().map(|x|x.1).sum();
    let(mut qw,qtmp,qfinal)=atomic_writer("hidden_k16_second_pivot_profiles_prefix.bin",b"H16PRO1\0",U,SAMPLE_MOD as u32,true);for(k,v)in &pv{qw.write_all(&k.profile).unwrap();qw.write_all(&k.sig).unwrap();qw.write_all(&[k.pivot,k.degree]).unwrap();qw.write_all(&v.to_le_bytes()).unwrap()}finish_counted(qw,qtmp,qfinal,pv.len()as u64);
    let hist=|a:&[u64;79]|(1..79).filter(|&i|a[i]!=0).map(|i|format!("\"{}\":{}",i,a[i])).collect::<Vec<_>>().join(",");let mut products:Vec<_>=phist.into_iter().collect();products.sort_unstable();let prod=products.iter().map(|(k,v)|format!("\"{}\":{}",k,v)).collect::<Vec<_>>().join(",");
    let elapsed=begun.elapsed().as_secs_f64();let scale=75_691_040f64/(hidden as f64);let text=format!("{{\n  \"status\":\"PASS_MEASURED_PREFIX\",\n  \"sample\":{{\"modulus\":16,\"schedule\":\"ri%32=0 then ri%32=16\",\"H_slices\":31,\"half_H_slices\":16}},\n  \"scale\":{},\n  \"heads\":{},\n  \"first_pivot_uses\":{},\n  \"hidden_parent_occurrences\":{},\n  \"outgoing_second_pivot_uses\":{},\n  \"unique_nonzero_second_pivot_profiles\":{},\n  \"profile_weight_sum_scaled\":\"{}\",\n  \"first_denominator_hist\":{{{}}},\n  \"second_denominator_hist\":{{{}}},\n  \"product_denominator_hist\":{{{}}},\n  \"nested_half\":{{\"hidden\":{},\"outgoing\":{},\"heads\":{},\"unique_profiles_at_that_point\":{},\"elapsed_seconds\":{:.6}}},\n  \"known_full_hidden_occurrences\":75691040,\n  \"occurrence_extrapolation_factor\":{:.9},\n  \"linear_full_wall_seconds_estimate\":{:.3},\n  \"elapsed_seconds\":{:.6}\n}}\n",U,heads,first_uses,hidden,outgoing,pv.len(),profile_weight_sum,hist(&m1hist),hist(&m2hist),prod,half.0,half.1,half.2,half.3,half.4,scale,elapsed*scale,elapsed);
    let tmp=format!("{}results_hidden_k16_parent_prefix.json.tmp",OUT_PREFIX);let final_path=format!("{}results_hidden_k16_parent_prefix.json",OUT_PREFIX);std::fs::write(&tmp,text.as_bytes()).unwrap();rename(tmp,final_path).unwrap();print!("{}",text)
}
