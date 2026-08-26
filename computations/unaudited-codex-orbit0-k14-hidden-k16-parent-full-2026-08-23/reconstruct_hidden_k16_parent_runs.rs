//! Full restartable recovery of the discarded K14 -> K16 pivotable parents.
#![allow(dead_code,unused_imports)]
include!("../unaudited-codex-orbit0-k14-hidden-k16-parent-prefix-2026-08-23/reconstruct_hidden_k16_parent_prefix.rs");

const FULL_OUT:&str="computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/";
const SLICE_RUN:usize=16;

fn counted_writer(path:&str,magic:&[u8;8],start:u16,end:u16,record_size:u16)->(BufWriter<File>,String,String){
    let final_path=format!("{}{}",FULL_OUT,path);let tmp=format!("{}.tmp",final_path);let mut w=BufWriter::with_capacity(1<<20,File::create(&tmp).unwrap());
    w.write_all(magic).unwrap();w.write_all(&U.to_le_bytes()).unwrap();w.write_all(&start.to_le_bytes()).unwrap();w.write_all(&end.to_le_bytes()).unwrap();w.write_all(&record_size.to_le_bytes()).unwrap();w.write_all(&0u16.to_le_bytes()).unwrap();w.write_all(&0u64.to_le_bytes()).unwrap();(w,tmp,final_path)
}
fn finish_run_file(mut w:BufWriter<File>,tmp:String,final_path:String,count:u64){w.flush().unwrap();let mut f=w.into_inner().unwrap();f.seek(SeekFrom::Start(32)).unwrap();f.write_all(&count.to_le_bytes()).unwrap();f.sync_all().unwrap();drop(f);rename(tmp,final_path).unwrap()}
fn atomic_text(path:&str,text:&str){let final_path=format!("{}{}",FULL_OUT,path);let tmp=format!("{}.tmp",final_path);std::fs::write(&tmp,text).unwrap();rename(tmp,final_path).unwrap()}
fn hist(a:&[u64;79])->String{(1..79).filter(|&i|a[i]!=0).map(|i|format!("\"{}\":{}",i,a[i])).collect::<Vec<_>>().join(",")}

fn run_one(e:&E,masses:&[i128],start:usize,end:usize){
    let begun=Instant::now();let stem=format!("{:03}_{:03}",start,end);let manifest=format!("run_{}.json",stem);
    if std::path::Path::new(&format!("{}{}",FULL_OUT,manifest)).exists(){println!("SKIP {}",stem);return}
    let parent_name=format!("parents_{}.bin",stem);let profile_name=format!("profiles_{}.bin",stem);
    let(mut pw,ptmp,pfinal)=counted_writer(&parent_name,b"H16RUN2\0",start as u16,end as u16,64);
    let mut profiles:HashMap<Key,i128>=HashMap::new();let(mut hidden,mut heads,mut first_uses,mut outgoing)=(0u64,0u64,0u64,0u64);
    let mut m1hist=[0u64;79];let mut m2hist=[0u64;79];let mut phist:HashMap<u16,u64>=HashMap::new();let(mut parent_sum,mut profile_raw_sum)=(0i128,0i128);
    for ri in start..end{let r=&e.records[ri];for(ia,a)in e.factor[0][0].iter().enumerate(){for(ib,b)in e.factor[1][0].iter().enumerate(){for(ic,c)in e.factor[2][0].iter().enumerate(){
        heads+=1;let head=make(r,a,b,c);let hs=sig(&head,e);let ps=valid(hs,e);let m1=ps.len();m1hist[m1]+=1;let mass=masses[ri];assert_eq!(mass*U%(m1 as i128),0);let w1=mass*U/(m1 as i128);
        for &p1 in &ps{first_uses+=1;for(t1,t)in e.tails[p1][0].iter().enumerate(){let row=replace(&head,&e.anchors[p1],t);let s=sig(&row,e);let ps2=avail(s,e);if ps2.is_empty(){continue}hidden+=1;parent_sum+=w1;let m2=ps2.len();m2hist[m2]+=1;assert_eq!(w1%(m2 as i128),0);let w2=-w1/(m2 as i128);*phist.entry((m1*m2)as u16).or_default()+=1;
            pw.write_all(&row.0).unwrap();pw.write_all(&w1.to_le_bytes()).unwrap();pw.write_all(&s).unwrap();pw.write_all(&(ri as u16).to_le_bytes()).unwrap();pw.write_all(&[ia as u8,ib as u8,ic as u8,p1 as u8,t1 as u8,m1 as u8,m2 as u8,0,0,0]).unwrap();
            for &p2 in &ps2{outgoing+=1;profile_raw_sum+=w2;add_weight(&mut profiles,Key{profile:profile(&row,p2,e),sig:s,pivot:p2 as u8,degree:0},w2)}
        }}
    }}}}
    finish_run_file(pw,ptmp,pfinal,hidden);
    let mut pv:Vec<_>=profiles.into_iter().filter(|(_,v)|*v!=0).collect();pv.sort_unstable_by_key(|x|x.0);let profile_sum:i128=pv.iter().map(|x|x.1).sum();assert_eq!(profile_sum,profile_raw_sum);let(mut qw,qtmp,qfinal)=counted_writer(&profile_name,b"H16PF2\0\0",start as u16,end as u16,59);for(k,v)in &pv{qw.write_all(&k.profile).unwrap();qw.write_all(&k.sig).unwrap();qw.write_all(&[k.pivot,k.degree]).unwrap();qw.write_all(&v.to_le_bytes()).unwrap()}finish_run_file(qw,qtmp,qfinal,pv.len()as u64);
    let mut products:Vec<_>=phist.into_iter().collect();products.sort_unstable();let prod=products.iter().map(|(k,v)|format!("\"{}\":{}",k,v)).collect::<Vec<_>>().join(",");let text=format!("{{\"status\":\"PASS_ATOMIC_RUN\",\"start\":{},\"end\":{},\"heads\":{},\"first_pivot_uses\":{},\"hidden_parent_occurrences\":{},\"parent_weight_sum_scaled\":\"{}\",\"outgoing_second_pivot_uses\":{},\"profile_raw_weight_sum_scaled\":\"{}\",\"unique_nonzero_profiles\":{},\"profile_weight_sum_scaled\":\"{}\",\"first_denominator_hist\":{{{}}},\"second_denominator_hist\":{{{}}},\"product_denominator_hist\":{{{}}},\"parent_file\":\"{}\",\"parent_bytes\":{},\"profile_file\":\"{}\",\"profile_bytes\":{},\"elapsed_seconds\":{:.6}}}\n",start,end,heads,first_uses,hidden,parent_sum,outgoing,profile_raw_sum,pv.len(),profile_sum,hist(&m1hist),hist(&m2hist),prod,parent_name,40+64*hidden,profile_name,40+59*pv.len()as u64,begun.elapsed().as_secs_f64());atomic_text(&manifest,&text);println!("{}",text.trim())
}

#[cfg(feature="hidden_k16_full")]
fn main(){std::fs::create_dir_all(FULL_OUT).unwrap();let begun=Instant::now();let e=parse();let masses=record_masses();for start in (0..e.records.len()).step_by(SLICE_RUN){let end=(start+SLICE_RUN).min(e.records.len());run_one(&e,&masses,start,end)}println!("FULL_RUN_PHASE_DONE {:.3}s",begun.elapsed().as_secs_f64())}
