//! Exact charge-only replay of the two K17 cancellation components.
//! No monomial rows are collected: a four-segment DSU computes each tail's
//! cycle partition, while the 12-anchor signature decides K0 pivotability.
use std::collections::HashMap;
use std::convert::TryInto;
use std::fs::{read,write};
use std::hash::{Hash,Hasher};
use std::sync::Arc;
use std::thread;
use std::time::Instant;

const DIR:&str="computations/unaudited-codex-orbit0-k17-component-charges-2026-08-23/";
const INTERFACE:&str="computations/unaudited-codex-orbit0-k17-component-charges-2026-08-23/k17_charge_interface.bin";
const CYCLE:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin";
const K15:&str="computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/checkpoint_direct_k15.bin";
const SCALE:i128=3_612_840;

#[derive(Clone)] struct Pivot { head:[u8;4], k2:Vec<[u8;4]>, k3:Vec<[u8;4]> }
#[derive(Clone)] struct R8 { row:[u8;12], mass:i64 }
#[derive(Clone)] struct Engine {
    ports:[[u8;2];252], anchor_pos:[i8;252],
    pivots:Vec<Pivot>, policies:HashMap<[u8;12],Vec<u8>>, records:Vec<R8>,
    packet:Vec<[u8;12]>, dual:HashMap<Key,i64>, available:Vec<Vec<u8>>,
}
#[derive(Clone,Copy,Eq,PartialEq)] struct Key([u8;13]);
impl Hash for Key { fn hash<H:Hasher>(&self,h:&mut H){h.write(&self.0)} }
#[derive(Clone,Copy,Eq,PartialEq,Hash)] struct CacheKey([u8;36]);
#[derive(Clone,Copy,Default)] struct Response { full:i64, irreducible:i64, n_irreducible:u16 }

fn u32le(x:&[u8])->u32{u32::from_le_bytes(x.try_into().unwrap())}
fn u64le(x:&[u8])->u64{u64::from_le_bytes(x.try_into().unwrap())}
fn i64le(x:&[u8])->i64{i64::from_le_bytes(x.try_into().unwrap())}

fn parse()->Engine{
    let b=read(INTERFACE).unwrap();let mut q=0usize;
    assert_eq!(&b[q..q+8],b"K17CHG1\0");q+=8;
    let ns=u32le(&b[q..q+4])as usize;q+=4;let nr=u32le(&b[q..q+4])as usize;q+=4;
    let nw=u32le(&b[q..q+4])as usize;q+=4;let np=u32le(&b[q..q+4])as usize;q+=4;
    assert_eq!((ns,nr,nw,np),(216,485,1728,78));
    let mut anchor_pos=[-1i8;252];for i in 0..12{anchor_pos[b[q+i]as usize]=i as i8}q+=12;
    let mut ports=[[0u8;2];252];for x in &mut ports{x.copy_from_slice(&b[q..q+2]);q+=2}
    let mut pivots=Vec::new();let mut masks=[0u16;78];
    for pi in 0..78{let mut head=[0u8;4];head.copy_from_slice(&b[q..q+4]);q+=4;
        let mut mask=0u16;for &c in &head{let i=anchor_pos[c as usize];assert!(i>=0);mask|=1u16<<(i as usize)}masks[pi]=mask;
        let mut k2=Vec::new();for _ in 0..12{let mut x=[0u8;4];x.copy_from_slice(&b[q..q+4]);q+=4;k2.push(x)}
        let mut k3=Vec::new();for _ in 0..32{let mut x=[0u8;4];x.copy_from_slice(&b[q..q+4]);q+=4;k3.push(x)}
        pivots.push(Pivot{head,k2,k3});
    }
    let mut policies=HashMap::new();for _ in 0..ns{let mut s=[0u8;12];s.copy_from_slice(&b[q..q+12]);q+=12;
        let n=b[q]as usize;q+=1;policies.insert(s,b[q..q+n].to_vec());q+=n}
    let mut records=Vec::new();for _ in 0..nr{let mut row=[0u8;12];row.copy_from_slice(&b[q..q+12]);q+=12;
        let mass=i64le(&b[q..q+8]);q+=8;records.push(R8{row,mass})}
    let mut packet=Vec::new();for _ in 0..nw{let mut row=[0u8;12];row.copy_from_slice(&b[q..q+12]);q+=12;packet.push(row)}
    assert_eq!(q,b.len());
    let c=read(CYCLE).unwrap();let mut p=0usize;assert_eq!(&c[p..p+8],b"K17CYC1\0");p+=8;
    // Independently match the port encoding embedded in the cycle packet.
    for ci in 0..252{let site_ports=[3*c[p]+c[p+2],3*c[p+1]+c[p+3]];assert_eq!(site_ports,ports[ci]);p+=4}
    let nd=u32le(&c[p..p+4])as usize;p+=4;assert_eq!(nd,77);let mut dual=HashMap::new();
    for _ in 0..nd{let mut x=[0u8;13];x.copy_from_slice(&c[p..p+13]);p+=13;let value=i64le(&c[p..p+8]);p+=8;dual.insert(Key(x),value);}assert_eq!(p,c.len());
    let mut available=Vec::with_capacity(4096);for support in 0u16..4096{available.push(masks.iter().enumerate().filter_map(|(i,&m)|if support&m==m{Some(i as u8)}else{None}).collect())}
    Engine{ports,anchor_pos,pivots,policies,records,packet,dual,available}
}

fn signature(row:&[u8;24],e:&Engine)->[u8;12]{let mut s=[0u8;12];for &c in row{let i=e.anchor_pos[c as usize];if i>=0{s[i as usize]+=1}}s}
fn support(s:&[u8;12])->u16{let mut x=0u16;for(i,&v)in s.iter().enumerate(){if v>0{x|=1<<i}}x}
fn make_row(a:&[u8;12],b:&[u8;12])->[u8;24]{let mut x=[0u8;24];x[..12].copy_from_slice(a);x[12..].copy_from_slice(b);x.sort_unstable();x}

fn find(p:[u8;24],mut x:u8)->u8{while p[x as usize]!=x{x=p[x as usize]}x}
fn union(p:&mut[u8;24],a:u8,b:u8){let x=find(*p,a);let y=find(*p,b);if x!=y{p[y as usize]=x}}

// Canonical four-path context after deleting one copy of the pivot head.
fn context(row:&[u8;24],pivot:&Pivot,e:&Engine,base:&[u8;12])->CacheKey{
    let mut removed=[false;24];for &h in &pivot.head{let i=(0..24).find(|&i|!removed[i]&&row[i]==h).unwrap();removed[i]=true}
    let mut parent=[0u8;24];for i in 0..24{parent[i]=i as u8}
    for i in 0..24{if !removed[i]{let [u,v]=e.ports[row[i]as usize];union(&mut parent,u,v)}}
    let mut sizes=[0u8;24];for i in 0..24{let r=find(parent,i as u8);sizes[r as usize]+=1}
    let mut endpoints=[0u8;8];for(i,&h)in pivot.head.iter().enumerate(){let [u,v]=e.ports[h as usize];endpoints[2*i]=u;endpoints[2*i+1]=v}
    let mut root_to_segment=[255u8;24];let mut seg_for_slot=[0u8;8];let mut segment_sizes=[0u8;4];let mut ns=0usize;
    for(i,&x)in endpoints.iter().enumerate(){let r=find(parent,x);if root_to_segment[r as usize]==255{assert!(ns<4);root_to_segment[r as usize]=ns as u8;segment_sizes[ns]=sizes[r as usize];ns+=1}seg_for_slot[i]=root_to_segment[r as usize]}
    assert_eq!(ns,4);
    let mut closed=[0u8;8];let mut nc=0usize;for r in 0..24{if find(parent,r as u8)==r as u8&&sizes[r]>0&&root_to_segment[r]==255{closed[nc]=sizes[r];nc+=1}}
    closed[..nc].sort_unstable();let mut key=[0u8;36];key[..8].copy_from_slice(&seg_for_slot);key[8..12].copy_from_slice(&segment_sizes);key[12]=nc as u8;key[13..13+nc].copy_from_slice(&closed[..nc]);key[24..].copy_from_slice(base);CacheKey(key)
}

fn tail_slots(pivot:&Pivot,tail:&[u8;4],e:&Engine)->[u8;8]{
    let mut ep=[0u8;8];for(i,&h)in pivot.head.iter().enumerate(){let [u,v]=e.ports[h as usize];ep[2*i]=u;ep[2*i+1]=v}
    let mut out=[0u8;8];for(i,&c)in tail.iter().enumerate(){let [u,v]=e.ports[c as usize];out[2*i]=ep.iter().position(|&x|x==u).unwrap()as u8;out[2*i+1]=ep.iter().position(|&x|x==v).unwrap()as u8}out
}

fn response(key:CacheKey,pivot_index:usize,tails:&[[u8;4]],e:&Engine)->Response{
    let k=&key.0;let mut answer=Response::default();let pivot=&e.pivots[pivot_index];
    for tail in tails{let slots=tail_slots(pivot,tail,e);let mut p=[0u8,1,2,3];
        for j in 0..4{let a=k[slots[2*j]as usize];let b=k[slots[2*j+1]as usize];let mut x=a;while p[x as usize]!=x{x=p[x as usize]};let mut y=b;while p[y as usize]!=y{y=p[y as usize]};if x!=y{p[y as usize]=x}}
        let mut sums=[0u8;4];for i in 0..4{let mut x=i as u8;while p[x as usize]!=x{x=p[x as usize]};sums[x as usize]+=k[8+i]}
        let mut parts=[0u8;12];let nc=k[12]as usize;parts[..nc].copy_from_slice(&k[13..13+nc]);let mut np=nc;for i in 0..4{if sums[i]>0{parts[np]=sums[i];np+=1}}parts[..np].sort_unstable();
        let mut ck=[0u8;13];ck[0]=np as u8;ck[1..1+np].copy_from_slice(&parts[..np]);let value=*e.dual.get(&Key(ck)).unwrap_or(&0);answer.full+=value;
        let mut s=[0u8;12];s.copy_from_slice(&k[24..36]);for &c in tail{let ap=e.anchor_pos[c as usize];if ap>=0{s[ap as usize]+=1}}
        if e.available[support(&s)as usize].is_empty(){answer.irreducible+=value;answer.n_irreducible+=1}
    }answer
}

fn a_worker(e:Arc<Engine>,tid:usize,nthreads:usize)->(i128,i128,u64,u64){
    let mut full=0i128;let mut irr=0i128;let mut uses=0u64;let mut tails=0u64;let mut caches:Vec<HashMap<CacheKey,Response>>=(0..78).map(|_|HashMap::new()).collect();
    for ri in (tid..e.records.len()).step_by(nthreads){let rec=&e.records[ri];for word in &e.packet{let row=make_row(&rec.row,word);let s=signature(&row,&e);let choices=e.policies.get(&s).unwrap();let unit=SCALE/(choices.len()as i128);
        for &pi8 in choices{let pi=pi8 as usize;let mut base=s;for &c in &e.pivots[pi].head{let ap=e.anchor_pos[c as usize];base[ap as usize]-=1}let key=context(&row,&e.pivots[pi],&e,&base);
            let response=*caches[pi].entry(key).or_insert_with(||response(key,pi,&e.pivots[pi].k3,&e));let w=(rec.mass as i128)*unit;full+=w*(response.full as i128);irr+=w*(response.irreducible as i128);uses+=1;tails+=32}
    }}(full,irr,uses,tails)
}

fn b_worker(e:Arc<Engine>,bytes:Arc<Vec<u8>>,tid:usize,nthreads:usize)->(i128,i128,u64,u64,[u64;79]){
    let n=u64le(&bytes[8..16])as usize;let mut full=0i128;let mut irr=0i128;let mut records=0u64;let mut tails=0u64;let mut hist=[0u64;79];let mut caches:Vec<HashMap<CacheKey,Response>>=(0..78).map(|_|HashMap::new()).collect();
    for ri in (tid..n).step_by(nthreads){let q=16+32*ri;let mut row=[0u8;24];row.copy_from_slice(&bytes[q..q+24]);let mass=i64le(&bytes[q+24..q+32]);let s=signature(&row,&e);let choices=&e.available[support(&s)as usize];assert!(!choices.is_empty());hist[choices.len()]+=1;let unit=SCALE/(choices.len()as i128);
        for &pi8 in choices{let pi=pi8 as usize;let mut base=s;for &c in &e.pivots[pi].head{let ap=e.anchor_pos[c as usize];base[ap as usize]-=1}let key=context(&row,&e.pivots[pi],&e,&base);
            let response=*caches[pi].entry(key).or_insert_with(||response(key,pi,&e.pivots[pi].k2,&e));let w=-(mass as i128)*unit;full+=w*(response.full as i128);irr+=w*(response.irreducible as i128);tails+=12}
        records+=1;
    }(full,irr,records,tails,hist)
}

fn gcd(mut a:i128,mut b:i128)->i128{a=a.abs();b=b.abs();while b!=0{let r=a%b;a=b;b=r}a}
fn frac(x:i128)->String{let g=gcd(x,SCALE);format!("{}/{}",x/g,SCALE/g)}
fn main(){let begun=Instant::now();let e=Arc::new(parse());let nt=thread::available_parallelism().map_or(4,|x|x.get()).min(8);
    let mut jobs=Vec::new();for t in 0..nt{let ee=e.clone();jobs.push(thread::spawn(move||a_worker(ee,t,nt)))}let(mut af,mut ai,mut au,mut at)=(0i128,0i128,0u64,0u64);for j in jobs{let(a,b,c,d)=j.join().unwrap();af+=a;ai+=b;au+=c;at+=d}assert_eq!((au,at),(6_619_280,211_816_960));
    eprintln!("A done {:.3}s full={} irreducible={}",begun.elapsed().as_secs_f64(),frac(af),frac(ai));
    let kb=Arc::new(read(K15).unwrap());assert_eq!(&kb[..8],b"K15CHK1\0");assert_eq!(u64le(&kb[8..16]),5_311_211);assert_eq!(kb.len(),16+32*5_311_211);
    let mut jobs=Vec::new();for t in 0..nt{let ee=e.clone();let bb=kb.clone();jobs.push(thread::spawn(move||b_worker(ee,bb,t,nt)))}let(mut bf,mut bi,mut br,mut bt)=(0i128,0i128,0u64,0u64);let mut hist=[0u64;79];for j in jobs{let(a,b,c,d,h)=j.join().unwrap();bf+=a;bi+=b;br+=c;bt+=d;for i in 0..79{hist[i]+=h[i]}}
    assert_eq!(br,5_311_211);assert_eq!(bt,532_114_572);let expected=[(1,49212),(2,97836),(3,588509),(5,1180076),(7,1180102),(8,246460),(11,1278516),(14,49716),(15,294972),(17,148092),(22,49708),(23,148012)];for &(n,c) in &expected{assert_eq!(hist[n],c)}assert_eq!(hist.iter().sum::<u64>(),br);
    let direct=-62_386_176i128*SCALE;let total_full=direct+af+bf;let total_irr=direct+ai+bi;
    let output=format!("{{\"status\":\"EXACT_K17_COMPONENT_CHARGES\",\"scale\":{},\"A_K14_K3\":{{\"full_scaled\":{},\"full\":\"{}\",\"irreducible_scaled\":{},\"irreducible\":\"{}\",\"pivotable\":\"{}\",\"pivot_uses\":{},\"tail_occurrences\":{}}},\"B_K15_K2\":{{\"full_scaled\":{},\"full\":\"{}\",\"irreducible_scaled\":{},\"irreducible\":\"{}\",\"pivotable\":\"{}\",\"checkpoint_rows\":{},\"tail_occurrences\":{}}},\"direct_irreducible\":-62386176,\"sum_with_direct\":{{\"using_full_A_B\":\"{}\",\"using_irreducible_A_B\":\"{}\"}},\"elapsed_seconds\":{:.3},\"scope\":\"charge projection only; no support or membership inference\"}}\n",SCALE,af,frac(af),ai,frac(ai),frac(af-ai),au,at,bf,frac(bf),bi,frac(bi),frac(bf-bi),br,bt,frac(total_full),frac(total_irr),begun.elapsed().as_secs_f64());
    write(format!("{}results_k17_component_charges.json",DIR),output.as_bytes()).unwrap();print!("{}",output);
}
