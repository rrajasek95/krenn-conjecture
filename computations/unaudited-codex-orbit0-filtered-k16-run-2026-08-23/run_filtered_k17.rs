// One bounded exact-rational (globally cleared) filtered reduction through K17.
use std::collections::{HashMap,HashSet};
use std::convert::TryInto;
use std::fs::{read,File};
use std::hash::{Hash,Hasher};
use std::io::{Write,BufWriter};
use std::sync::Arc;
use std::thread;
use std::time::Instant;

const STRUCTURE:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k16_structure.bin";
const AUX:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_aux.bin";
const OUT_DIRECT:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_k17_direct.bin";
const OUT_K14:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_k17_from_k14.bin";
const OUT_K15:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_k17_from_k15.bin";
const OUT_COMBINED:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_reduced_k17.bin";

#[derive(Clone,Copy,Debug,Eq,Ord,PartialEq,PartialOrd)] struct Row([u8;24]);
impl Hash for Row { fn hash<H:Hasher>(&self,state:&mut H){state.write(&self.0)} }
#[derive(Clone)] struct R8 { row:[u8;12], size:u32, coefficient:i64 }
#[derive(Clone)] struct Engine {
    transforms:Vec<Vec<u8>>, permutations:Vec<[u8;12]>, anchor_pos:[i8;252],
    pivots:Vec<[u8;12]>, factor_tails:Vec<Vec<Vec<[u8;4]>>>, records:Vec<R8>,
    anchors:Vec<[u8;4]>, all_k2:Vec<Vec<[u8;4]>>, all_k3:Vec<Vec<[u8;4]>>,
    cover:HashSet<[u8;12]>, scale:i128,
}
fn u32le(x:&[u8])->u32{u32::from_le_bytes(x.try_into().unwrap())}
fn u64le(x:&[u8])->u64{u64::from_le_bytes(x.try_into().unwrap())}
fn i64le(x:&[u8])->i64{i64::from_le_bytes(x.try_into().unwrap())}
fn parse()->Engine{
    let b=read(STRUCTURE).unwrap();let mut p=0usize;
    assert_eq!(&b[p..p+11],b"K16DIRECT1\0");p+=11;
    let nt=u32le(&b[p..p+4])as usize;p+=4;let nr=u32le(&b[p..p+4])as usize;p+=4;
    let np=u32le(&b[p..p+4])as usize;p+=4;let na=u32le(&b[p..p+4])as usize;p+=4;
    assert_eq!((nt,nr,np,na),(384,485,78,12));
    let anchor_cells=&b[p..p+12];p+=12;let mut anchor_pos=[-1i8;252];
    for(i,&cell)in anchor_cells.iter().enumerate(){anchor_pos[cell as usize]=i as i8}
    let mut transforms=Vec::new();let mut permutations=Vec::new();
    for _ in 0..nt{transforms.push(b[p..p+252].to_vec());p+=252;let mut q=[0u8;12];q.copy_from_slice(&b[p..p+12]);p+=12;permutations.push(q)}
    let mut records=Vec::new();for _ in 0..nr{let mut row=[0u8;12];row.copy_from_slice(&b[p..p+12]);p+=12;let size=u32le(&b[p..p+4]);p+=4;let coefficient=i64le(&b[p..p+8]);p+=8;records.push(R8{row,size,coefficient})}
    let mut pivots=Vec::new();for _ in 0..np{let mut x=[0u8;12];x.copy_from_slice(&b[p..p+12]);p+=12;pivots.push(x)}
    let mut factor_tails=vec![vec![Vec::new();3];3];for f in 0..3{for d in 0..3{let n=u32le(&b[p..p+4])as usize;p+=4;for _ in 0..n{let mut x=[0u8;4];x.copy_from_slice(&b[p..p+4]);p+=4;factor_tails[f][d].push(x)}}}assert_eq!(p,b.len());
    let a=read(AUX).unwrap();let mut q=0usize;assert_eq!(&a[q..q+8],b"K17AUX1\0");q+=8;
    let scale=u64le(&a[q..q+8])as i128;q+=8;let nc=u32le(&a[q..q+4])as usize;q+=4;let npa=u32le(&a[q..q+4])as usize;q+=4;assert_eq!((scale,nc,npa),(281_801_520,25,78));
    let mut cover=HashSet::new();for _ in 0..nc{let mut x=[0u8;12];x.copy_from_slice(&a[q..q+12]);q+=12;cover.insert(x);}
    let mut anchors=Vec::new();let mut all_k2=Vec::new();let mut all_k3=Vec::new();
    for _ in 0..npa{let mut x=[0u8;4];x.copy_from_slice(&a[q..q+4]);q+=4;anchors.push(x);let mut k2=Vec::new();for _ in 0..12{let mut y=[0u8;4];y.copy_from_slice(&a[q..q+4]);q+=4;k2.push(y)}all_k2.push(k2);let mut k3=Vec::new();for _ in 0..32{let mut y=[0u8;4];y.copy_from_slice(&a[q..q+4]);q+=4;k3.push(y)}all_k3.push(k3)}assert_eq!(q,a.len());
    Engine{transforms,permutations,anchor_pos,pivots,factor_tails,records,anchors,all_k2,all_k3,cover,scale}
}
fn signature(row:&[u8;24],e:&Engine)->[u8;12]{let mut s=[0u8;12];for &c in row{let i=e.anchor_pos[c as usize];if i>=0{s[i as usize]+=1}}s}
fn tail_signature(tail:&[u8;4],e:&Engine)->[u8;12]{let mut s=[0u8;12];for &c in tail{let i=e.anchor_pos[c as usize];if i>=0{s[i as usize]+=1}}s}
fn sig_move(s:[u8;12],p:&[u8;12])->[u8;12]{let mut x=[0u8;12];for old in 0..12{x[p[old]as usize]=s[old]}x}
fn canonical_sig(s:[u8;12],e:&Engine)->[u8;12]{e.permutations.iter().map(|p|sig_move(s,p)).min().unwrap()}
fn available(s:[u8;12],e:&Engine)->Vec<usize>{e.pivots.iter().enumerate().filter_map(|(j,p)|if(0..12).all(|i|s[i]>=p[i]){Some(j)}else{None}).collect()}
fn child_sig(s:[u8;12],pivot:usize,tail:&[u8;4],e:&Engine)->[u8;12]{let t=tail_signature(tail,e);let mut x=[0u8;12];for i in 0..12{x[i]=s[i]-e.pivots[pivot][i]+t[i]}x}
fn valid_pivots(s:[u8;12],e:&Engine)->Vec<usize>{let mut out=Vec::new();for pivot in available(s,e){let mut ok=true;for tail in &e.all_k2[pivot]{let child=child_sig(s,pivot,tail,e);if available(child,e).is_empty()&&!e.cover.contains(&canonical_sig(child,e)){ok=false;break}}if ok{out.push(pivot)}}assert!(!out.is_empty());out}
fn canonical(row:Row,e:&Engine,cache:&mut HashMap<[u8;12],Vec<usize>>)->Row{let s=signature(&row.0,e);let actions=cache.entry(s).or_insert_with(||{let mut best=None;let mut a=Vec::new();for(i,p)in e.permutations.iter().enumerate(){let x=sig_move(s,p);if best.map_or(true,|b|x<b){best=Some(x);a.clear();a.push(i)}else if Some(x)==best{a.push(i)}}a});let mut best=None;for &action in actions.iter(){let t=&e.transforms[action];let mut x=row.0.map(|c|t[c as usize]);x.sort_unstable();let y=Row(x);if best.map_or(true,|b|y<b){best=Some(y)}}best.unwrap()}
fn pivotable_sig(s:[u8;12],e:&Engine)->bool{e.pivots.iter().any(|p|(0..12).all(|i|s[i]>=p[i]))}
fn pivotable(row:&Row,e:&Engine)->bool{pivotable_sig(signature(&row.0,e),e)}
fn add(map:&mut HashMap<Row,i128>,row:Row,value:i128){let x=map.entry(row).or_default();*x+=value;if *x==0{map.remove(&row);}}
fn make_row(r:&R8,a:&[u8;4],b:&[u8;4],c:&[u8;4])->Row{let mut x=[0u8;24];x[..12].copy_from_slice(&r.row);x[12..16].copy_from_slice(a);x[16..20].copy_from_slice(b);x[20..24].copy_from_slice(c);x.sort_unstable();Row(x)}
fn replace_anchor(row:&Row,anchor:&[u8;4],tail:&[u8;4])->Row{let mut x=[0u8;24];let(mut ai,mut k)=(0usize,0usize);for &c in &row.0{if ai<4&&c==anchor[ai]{ai+=1}else{x[k]=c;k+=1}}assert_eq!((ai,k),(4,20));x[20..24].copy_from_slice(tail);x.sort_unstable();Row(x)}
fn response_plan(s:[u8;12],valid:bool,degree:usize,e:&Engine)->(usize,Vec<(usize,usize)>){let piv=if valid{valid_pivots(s,e)}else{available(s,e)};assert!(!piv.is_empty());let n=piv.len();let mut keep=Vec::new();for &p in &piv{let tails=if degree==2{&e.all_k2[p]}else{&e.all_k3[p]};for(ti,t)in tails.iter().enumerate(){if !pivotable_sig(child_sig(s,p,t,e),e){keep.push((p,ti))}}}(n,keep)}
fn worker(e:Arc<Engine>,start:usize,step:usize)->(HashMap<Row,i128>,HashMap<Row,i128>,HashMap<Row,i128>,[u64;3]){
    let(mut direct,mut from14,mut from15)=(HashMap::new(),HashMap::new(),HashMap::new());let mut canonical_cache=HashMap::new();let mut plan14=HashMap::new();let mut plan15=HashMap::new();let(mut raw_direct,mut raw14,mut raw15)=(0u64,0u64,0u64);
    for ri in (start..e.records.len()).step_by(step){let r=&e.records[ri];let positive=(r.coefficient as i128)*(r.size as i128);let direct_mass=-positive*e.scale;
        // Direct K17: all six 2+3+4 placements plus 3+3+3.
        for d2 in 0..3{for d3 in 0..3{if d3==d2{continue}let d4=3-d2-d3;for a in &e.factor_tails[d2][0]{for b in &e.factor_tails[d3][1]{for c in &e.factor_tails[d4][2]{let mut terms:[Option<&[u8;4]>;3]=[None,None,None];terms[d2]=Some(a);terms[d3]=Some(b);terms[d4]=Some(c);let row=make_row(r,terms[0].unwrap(),terms[1].unwrap(),terms[2].unwrap());raw_direct+=1;if !pivotable(&row,&e){let q=canonical(row,&e,&mut canonical_cache);add(&mut direct,q,direct_mass)}}}}}}
        for a in &e.factor_tails[0][1]{for b in &e.factor_tails[1][1]{for c in &e.factor_tails[2][1]{let row=make_row(r,a,b,c);raw_direct+=1;if !pivotable(&row,&e){let q=canonical(row,&e,&mut canonical_cache);add(&mut direct,q,direct_mass)}}}}
        // K14 cancellation via the frozen valid-pivot averaging, now with K3 tails.
        for a in &e.factor_tails[0][0]{for b in &e.factor_tails[1][0]{for c in &e.factor_tails[2][0]{let head=make_row(r,a,b,c);let s=signature(&head.0,&e);let plan=plan14.entry(s).or_insert_with(||response_plan(s,true,3,&e));let weight=positive*e.scale/(plan.0 as i128);assert_eq!(positive*e.scale%(plan.0 as i128),0);for &(pivot,ti) in &plan.1{let child=replace_anchor(&head,&e.anchors[pivot],&e.all_k3[pivot][ti]);let q=canonical(child,&e,&mut canonical_cache);add(&mut from14,q,weight);raw14+=1}}}}
        // Direct K15 (2+2+3), canceled by all available pivots with K2 tails.
        for high in 0..3{let other:Vec<_>=(0..3).filter(|&x|x!=high).collect();for a in &e.factor_tails[other[0]][0]{for b in &e.factor_tails[other[1]][0]{for c in &e.factor_tails[high][1]{let head=match high{0=>make_row(r,c,a,b),1=>make_row(r,a,c,b),_=>make_row(r,a,b,c)};let s=signature(&head.0,&e);let plan=plan15.entry(s).or_insert_with(||response_plan(s,false,2,&e));let weight=positive*e.scale/(plan.0 as i128);assert_eq!(positive*e.scale%(plan.0 as i128),0);for &(pivot,ti) in &plan.1{let child=replace_anchor(&head,&e.anchors[pivot],&e.all_k2[pivot][ti]);let q=canonical(child,&e,&mut canonical_cache);add(&mut from15,q,weight);raw15+=1}}}}}
    }(direct,from14,from15,[raw_direct,raw14,raw15])
}
fn stats(map:&HashMap<Row,i128>)->(usize,i128,i128){(map.len(),map.values().copied().sum(),map.values().map(|x|x.abs()).sum())}
fn write_map(path:&str,magic:&[u8;8],map:&HashMap<Row,i128>){let mut rows:Vec<_>=map.iter().filter(|(_,v)|**v!=0).map(|(r,v)|(*r,*v)).collect();rows.sort_unstable_by_key(|x|x.0);let mut w=BufWriter::new(File::create(path).unwrap());w.write_all(magic).unwrap();w.write_all(&(rows.len()as u64).to_le_bytes()).unwrap();for(r,v)in rows{w.write_all(&r.0).unwrap();w.write_all(&v.to_le_bytes()).unwrap()}}
#[cfg(not(feature="hidden_child_prefix"))]
fn main(){let begun=Instant::now();let e=Arc::new(parse());let workers=thread::available_parallelism().map_or(4,|x|x.get()).min(8);let mut jobs=Vec::new();for t in 0..workers{let c=e.clone();jobs.push(thread::spawn(move||worker(c,t,workers)))}let(mut direct,mut from14,mut from15)=(HashMap::new(),HashMap::new(),HashMap::new());let mut raw=[0u64;3];for j in jobs{let(a,b,c,n)=j.join().unwrap();for(r,v)in a{add(&mut direct,r,v)}for(r,v)in b{add(&mut from14,r,v)}for(r,v)in c{add(&mut from15,r,v)}for i in 0..3{raw[i]+=n[i]}}
    assert_eq!(raw[0],485*171008);assert!(direct.keys().all(|r|!pivotable(r,&e)));assert!(from14.keys().all(|r|!pivotable(r,&e)));assert!(from15.keys().all(|r|!pivotable(r,&e)));write_map(OUT_DIRECT,b"K17DIR2\0",&direct);write_map(OUT_K14,b"K17K142\0",&from14);write_map(OUT_K15,b"K17K152\0",&from15);
    let component_support_sum=direct.len()+from14.len()+from15.len();let mut union=HashSet::with_capacity(component_support_sum);for r in direct.keys().chain(from14.keys()).chain(from15.keys()){union.insert(*r);}let union_support=union.len();let mut combined=direct.clone();for(r,v)in &from14{add(&mut combined,*r,*v)}for(r,v)in &from15{add(&mut combined,*r,*v)}let exact_zero=union_support-combined.len();assert!(combined.keys().all(|r|!pivotable(r,&e)));write_map(OUT_COMBINED,b"K17RED2\0",&combined);
    println!("{{\"scale\":{},\"workers\":{},\"raw_irreducible_occurrences\":{:?},\"direct\":{:?},\"from_K14_K3\":{:?},\"from_K15_K2\":{:?},\"component_support_sum\":{},\"support_union\":{},\"overlap_incidences\":{},\"exact_zero_rows\":{},\"combined\":{:?},\"elapsed_seconds\":{:.3}}}",e.scale,workers,raw,stats(&direct),stats(&from14),stats(&from15),component_support_sum,union_support,component_support_sum-union_support,exact_zero,stats(&combined),begun.elapsed().as_secs_f64());
}
