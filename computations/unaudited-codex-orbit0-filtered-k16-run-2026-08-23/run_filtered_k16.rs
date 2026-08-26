//! Bounded direct K15/K16 collector and combined K16 initial-ideal reduction.
use std::collections::HashMap;
use std::convert::TryInto;
use std::fs::{read,File};
use std::hash::{Hash,Hasher};
use std::io::{Read,Write,BufWriter};
use std::sync::Arc;
use std::thread;
use std::time::Instant;

const STRUCTURE:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin";
const RESPONSE:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/frozen_k14_k2_response.bin";
const OUT15:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k15.bin";
const OUT16:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k16.bin";
const OUTRED:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_reduced_k16.bin";

#[derive(Clone,Copy,Debug,Eq,Ord,PartialEq,PartialOrd)] struct Row([u8;24]);
impl Hash for Row { fn hash<H:Hasher>(&self,state:&mut H){state.write(&self.0)} }
#[derive(Clone)] struct R8 { row:[u8;12], size:u32, coefficient:i64 }
#[derive(Clone)] struct Engine {
    transforms:Vec<Vec<u8>>, permutations:Vec<[u8;12]>, anchor_pos:[i8;252],
    pivots:Vec<[u8;12]>, tails:Vec<Vec<Vec<[u8;4]>>>, records:Vec<R8>
}
fn u32le(x:&[u8])->u32{u32::from_le_bytes(x.try_into().unwrap())}
fn i64le(x:&[u8])->i64{i64::from_le_bytes(x.try_into().unwrap())}
fn parse()->Engine{
    let b=read(STRUCTURE).unwrap(); let mut p=0usize;
    assert_eq!(&b[p..p+11],b"K16DIRECT1\0");p+=11;
    let nt=u32le(&b[p..p+4])as usize;p+=4;let nr=u32le(&b[p..p+4])as usize;p+=4;
    let np=u32le(&b[p..p+4])as usize;p+=4;let na=u32le(&b[p..p+4])as usize;p+=4;
    assert_eq!((nt,nr,np,na),(384,485,78,12));
    let anchors=&b[p..p+12];p+=12;let mut anchor_pos=[-1i8;252];
    for(i,&cell)in anchors.iter().enumerate(){anchor_pos[cell as usize]=i as i8}
    let mut transforms=Vec::new();let mut permutations=Vec::new();
    for _ in 0..nt {transforms.push(b[p..p+252].to_vec());p+=252;
        let mut q=[0u8;12];q.copy_from_slice(&b[p..p+12]);p+=12;permutations.push(q)}
    let mut records=Vec::new();for _ in 0..nr{let mut row=[0u8;12];row.copy_from_slice(&b[p..p+12]);p+=12;
        let size=u32le(&b[p..p+4]);p+=4;let coefficient=i64le(&b[p..p+8]);p+=8;
        records.push(R8{row,size,coefficient})}
    let mut pivots=Vec::new();for _ in 0..np{let mut x=[0u8;12];x.copy_from_slice(&b[p..p+12]);p+=12;pivots.push(x)}
    let mut tails=vec![vec![Vec::new();3];3];for f in 0..3{for d in 0..3{let n=u32le(&b[p..p+4])as usize;p+=4;
        for _ in 0..n{let mut x=[0u8;4];x.copy_from_slice(&b[p..p+4]);p+=4;tails[f][d].push(x)}}}
    assert_eq!(p,b.len());for f in 0..3{assert_eq!((tails[f][0].len(),tails[f][1].len(),tails[f][2].len()),(12,32,60))}
    Engine{transforms,permutations,anchor_pos,pivots,tails,records}
}
fn signature(row:&[u8;24],pos:&[i8;252])->[u8;12]{let mut s=[0u8;12];for &c in row{let i=pos[c as usize];if i>=0{s[i as usize]+=1}}s}
fn sig_move(s:[u8;12],perm:&[u8;12])->[u8;12]{let mut x=[0u8;12];for old in 0..12{x[perm[old]as usize]=s[old]}x}
fn canonical(row:Row,e:&Engine,cache:&mut HashMap<[u8;12],Vec<usize>>)->Row{
    let s=signature(&row.0,&e.anchor_pos);let actions=cache.entry(s).or_insert_with(||{
        let mut best=None;let mut a=Vec::new();for(i,p)in e.permutations.iter().enumerate(){let x=sig_move(s,p);
            if best.map_or(true,|b|x<b){best=Some(x);a.clear();a.push(i)}else if Some(x)==best{a.push(i)}}a});
    let mut best=None;for &action in actions.iter(){let t=&e.transforms[action];let mut x=row.0.map(|c|t[c as usize]);x.sort_unstable();let y=Row(x);if best.map_or(true,|b|y<b){best=Some(y)}}best.unwrap()
}
fn add(map:&mut HashMap<Row,i64>,row:Row,value:i64){let x=map.entry(row).or_default();*x+=value;if *x==0{map.remove(&row);}}
fn make_row(r:&R8,a:&[u8;4],b:&[u8;4],c:&[u8;4])->Row{let mut x=[0u8;24];x[..12].copy_from_slice(&r.row);x[12..16].copy_from_slice(a);x[16..20].copy_from_slice(b);x[20..24].copy_from_slice(c);Row(x)}
fn worker(e:Arc<Engine>,start:usize,step:usize)->(HashMap<Row,i64>,HashMap<Row,i64>,u64,u64){
    let mut k15=HashMap::new();let mut k16=HashMap::new();let mut cache=HashMap::new();let mut n15=0;let mut n16=0;
    for ri in (start..e.records.len()).step_by(step){let r=&e.records[ri];let mass=-(r.coefficient*(r.size as i64));
        for high in 0..3{let other:Vec<_>=(0..3).filter(|&x|x!=high).collect();
            // 2+2+3 direct K15.
            for a in &e.tails[other[0]][0]{for b in &e.tails[other[1]][0]{for c in &e.tails[high][1]{
                // Restore factor-family order.
                let row=match high{0=>make_row(r,c,a,b),1=>make_row(r,a,c,b),_=>make_row(r,a,b,c)};
                let q=canonical(row,&e,&mut cache);add(&mut k15,q,mass);n15+=1}}}
            // 2+2+4 direct K16.
            for a in &e.tails[other[0]][0]{for b in &e.tails[other[1]][0]{for c in &e.tails[high][2]{let row=match high{0=>make_row(r,c,a,b),1=>make_row(r,a,c,b),_=>make_row(r,a,b,c)};
                let q=canonical(row,&e,&mut cache);add(&mut k16,q,mass);n16+=1}}}
            // 2+3+3 direct K16: high is the K2 family.
            for a in &e.tails[high][0]{for b in &e.tails[other[0]][1]{for c in &e.tails[other[1]][1]{let row=match high{0=>make_row(r,a,b,c),1=>make_row(r,b,a,c),_=>make_row(r,b,c,a)};
                let q=canonical(row,&e,&mut cache);add(&mut k16,q,mass);n16+=1}}}
        }
    }(k15,k16,n15,n16)
}
fn write_map(path:&str,magic:&[u8;8],map:&HashMap<Row,i64>){let mut rows:Vec<_>=map.iter().filter(|(_,v)|**v!=0).map(|(r,v)|(*r,*v)).collect();rows.sort_unstable_by_key(|x|x.0);
    let mut w=BufWriter::new(File::create(path).unwrap());w.write_all(magic).unwrap();w.write_all(&(rows.len()as u64).to_le_bytes()).unwrap();for(r,v)in rows{w.write_all(&r.0).unwrap();w.write_all(&v.to_le_bytes()).unwrap()}}
fn pivotable(row:&Row,e:&Engine)->bool{let s=signature(&row.0,&e.anchor_pos);e.pivots.iter().any(|p|(0..12).all(|i|s[i]>=p[i]))}
fn stats(map:&HashMap<Row,i64>)->(usize,i128,i128){(map.len(),map.values().map(|&x|x as i128).sum(),map.values().map(|&x|(x as i128).abs()).sum())}
fn main(){let begun=Instant::now();let e=Arc::new(parse());let workers=thread::available_parallelism().map_or(4,|x|x.get()).min(8);
    let mut jobs=Vec::new();for t in 0..workers{let c=e.clone();jobs.push(thread::spawn(move||worker(c,t,workers)))}
    let mut k15=HashMap::new();let mut k16=HashMap::new();let(mut n15,mut n16)=(0u64,0u64);
    for j in jobs{let(a,b,x,y)=j.join().unwrap();for(r,v)in a{add(&mut k15,r,v)}for(r,v)in b{add(&mut k16,r,v)}n15+=x;n16+=y}
    assert_eq!(n15,485*13824);assert_eq!(n16,485*62784);write_map(OUT15,b"K15CHK1\0",&k15);write_map(OUT16,b"K16DIR1\0",&k16);
    let before=stats(&k16);let mut f=File::open(RESPONSE).unwrap();let mut magic=[0u8;8];f.read_exact(&mut magic).unwrap();assert_eq!(&magic,b"K16RESP1");let mut nb=[0u8;8];f.read_exact(&mut nb).unwrap();let nr=u64::from_le_bytes(nb);assert_eq!(nr,1_848_174);
    let mut first=true;for _ in 0..nr{let mut row=[0u8;24];let mut vb=[0u8;8];f.read_exact(&mut row).unwrap();f.read_exact(&mut vb).unwrap();let r=Row(row);if first{assert_eq!(canonical(r,&e,&mut HashMap::new()),r);first=false}
        // Frozen collector normalizes +R8'E2^3: its tails have weight -r.
        // The requested P=-R8'E^3 has the opposite (+r) response, hence -v.
        add(&mut k16,r,-i64::from_le_bytes(vb))}
    let combined=stats(&k16);let mut pivot_count=0usize;let mut pivot_mass=0i128;let mut pivot_abs=0i128;k16.retain(|r,v|{if pivotable(r,&e){pivot_count+=1;pivot_mass+=*v as i128;pivot_abs+=(*v as i128).abs();false}else{true}});let reduced=stats(&k16);write_map(OUTRED,b"K16RED1\0",&k16);
    println!("{{\"workers\":{},\"raw_K15\":{},\"raw_K16\":{},\"direct_K15\":{:?},\"direct_K16\":{:?},\"combined_K16\":{:?},\"removed_pivotable\":[{},{},{}],\"reduced_K16\":{:?},\"elapsed_seconds\":{:.3}}}",workers,n15,n16,stats(&k15),before,combined,pivot_count,pivot_mass,pivot_abs,reduced,begun.elapsed().as_secs_f64());
}
