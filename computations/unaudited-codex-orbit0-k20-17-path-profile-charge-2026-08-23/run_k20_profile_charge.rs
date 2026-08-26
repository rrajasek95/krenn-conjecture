mod base {
include!("../unaudited-codex-orbit0-k19-profile-census-2026-08-23/run_k19_profile_census.rs");
use std::io::{BufReader,Read};

const K19:&str="computations/unaudited-codex-orbit0-k19-charge-2026-08-23/";
const K4:&str="computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin";
const OUT20:&str="computations/unaudited-codex-orbit0-k20-17-path-profile-charge-2026-08-23/";
const U:i128=400_591_699_200;
const OLD_SCALE:i128=(SCALE as i128)*(SCALE as i128);
const SCALE_RATIO:i128=OLD_SCALE/U;

#[derive(Default,Clone,Copy)]
struct Q{full_n:u64,irr_n:u64,full:i128,irr:i128,keys:u64,signed:i128,l1:i128}
impl Q{fn add(&mut self,x:Q){self.full_n+=x.full_n;self.irr_n+=x.irr_n;self.full+=x.full;self.irr+=x.irr;self.keys+=x.keys;self.signed+=x.signed;self.l1+=x.l1}}

fn aux(e:&E)->(Vec<Vec<[u8;4]>>,HashMap<[u8;13],i64>){
 let b=read(K4).unwrap();assert_eq!(&b[..7],b"K18K4A1");let mut p=7;let mut k4=vec![Vec::new();78];
 for x in &mut k4{for _ in 0..60{let mut t=[0;4];t.copy_from_slice(&b[p..p+4]);p+=4;x.push(t)}}assert_eq!(p,b.len());
 let c=read(format!("{}filtered_k17_cycle_aux.bin",DIR)).unwrap();assert_eq!(&c[..8],b"K17CYC1\0");let mut z=8+252*4;
 let n=u32le(&c[z..z+4])as usize;z+=4;let mut dual=HashMap::new();for _ in 0..n{let mut k=[0;13];k.copy_from_slice(&c[z..z+13]);z+=13;let v=i64::from_le_bytes(c[z..z+8].try_into().unwrap());z+=8;dual.insert(k,v);}assert_eq!(z,c.len());assert_eq!(e.anchors.len(),78);(k4,dual)
}

fn row_cycle(row:&Row,e:&E)->[u8;13]{
 let mut adj=[[0u8;2];24];let mut deg=[0usize;24];for &c in &row.0{let[u,v,a,b]=e.cells[c as usize];let x=(3*u+a)as usize;let y=(3*v+b)as usize;adj[x][deg[x]]=y as u8;deg[x]+=1;adj[y][deg[y]]=x as u8;deg[y]+=1}assert!(deg.iter().all(|&d|d==2));
 let mut seen=[false;24];let mut parts=[0;12];let mut n=0;for st in 0..24{if seen[st]{continue}let mut stack=[0u8;24];stack[0]=st as u8;let(mut top,mut len)=(1,0);seen[st]=true;while top>0{top-=1;let x=stack[top]as usize;len+=1;for &y in &adj[x]{if !seen[y as usize]{seen[y as usize]=true;stack[top]=y;top+=1}}}parts[n]=len;n+=1}parts[..n].sort_unstable();let mut k=[0;13];k[0]=n as u8;k[1..1+n].copy_from_slice(&parts[..n]);k
}

fn key_cycle(k:&Key,tail:&[u8;4],e:&E)->[u8;13]{
 let p=k.pivot as usize;let mut label=[255u8;24];for(i,&c)in e.anchors[p].iter().enumerate(){let[u,v,a,b]=e.cells[c as usize];label[(3*u+a)as usize]=(2*i)as u8;label[(3*v+b)as usize]=(2*i+1)as u8}
 let mut adj=[[(255u8,0u8);2];8];let mut deg=[0usize;8];let mut edge=|a:usize,b:usize,w:u8|{adj[a][deg[a]]=(b as u8,w);deg[a]+=1;adj[b][deg[b]]=(a as u8,w);deg[b]+=1;};
 for a in 0..8{let b=k.profile[a]as usize;if a<b{edge(a,b,k.profile[8+a])}}
 for &c in tail{let[u,v,a,b]=e.cells[c as usize];let x=label[(3*u+a)as usize];let y=label[(3*v+b)as usize];assert!(x<8&&y<8);edge(x as usize,y as usize,1)}assert!(deg.iter().all(|&x|x==2));
 let mut parts=[0u8;12];let nc=k.profile[16]as usize;parts[..nc].copy_from_slice(&k.profile[17..17+nc]);let mut n=nc;let mut seen=[false;8];for st in 0..8{if seen[st]{continue}let mut stack=[0u8;8];stack[0]=st as u8;let(mut top,mut twice)=(1,0u16);seen[st]=true;while top>0{top-=1;let x=stack[top]as usize;for &(y,w)in &adj[x]{twice+=w as u16;if !seen[y as usize]{seen[y as usize]=true;stack[top]=y;top+=1}}}assert_eq!(twice%2,0);parts[n]=(twice/2)as u8;n+=1}parts[..n].sort_unstable();let mut out=[0;13];out[0]=n as u8;out[1..1+n].copy_from_slice(&parts[..n]);out
}

fn eval(k:&Key,w:i128,e:&E,k4:&[Vec<[u8;4]>],dual:&HashMap<[u8;13],i64>)->Q{
 let p=k.pivot as usize;let tails:&Vec<[u8;4]>=match k.degree{2=>&e.tails[p][0],3=>&e.tails[p][1],4=>&k4[p],_=>panic!("degree")};let mut q=Q::default();q.keys=1;q.signed=w;q.l1=w.abs();
 for t in tails{let z=*dual.get(&key_cycle(k,t,e)).unwrap_or(&0)as i128;q.full_n+=1;q.full+=w*z;if avail(child_sig(k.sig,p,t,e),e).is_empty(){q.irr_n+=1;q.irr+=w*z}}q
}

fn literal_selftest(e:&E,k4:&[Vec<[u8;4]>])->u64{
 let mut n=0;for r in e.records.iter().take(8){for a in e.factor[0][0].iter().take(4){for b in e.factor[1][0].iter().take(4){for c in e.factor[2][0].iter().take(4){let row=make(r,a,b,c);let s=sig(&row,e);for p in avail(s,e){let k=Key{profile:profile(&row,p,e),sig:s,pivot:p as u8,degree:2};for(d,tails)in [(2,&e.tails[p][0]),(3,&e.tails[p][1]),(4,&k4[p])]{let mut z=k;z.degree=d;for t in tails.iter().step_by(7){assert_eq!(key_cycle(&z,t,e),row_cycle(&replace(&row,&e.anchors[p],t),e));n+=1}}}}}}}assert!(n>1000);n
}

fn read_group(mode:&str,path:&str,stored_degree:u8,target_degree:u8,e:&E,k4:&[Vec<[u8;4]>],dual:&HashMap<[u8;13],i64>)->Q{
 let mut r=BufReader::with_capacity(1<<20,File::open(path).unwrap());let mut h=[0;16];r.read_exact(&mut h).unwrap();assert_eq!(&h[..8],b"K19SUM1\0");let n=u64::from_le_bytes(h[8..16].try_into().unwrap());
 let mut out=Q::default();let mut prev:Option<Key>=None;for _ in 0..n{let mut z=[0;59];r.read_exact(&mut z).unwrap();let mut p=[0;29];p.copy_from_slice(&z[..29]);let mut s=[0;12];s.copy_from_slice(&z[29..41]);let mut k=Key{profile:p,sig:s,pivot:z[41],degree:z[42]};assert_eq!(k.degree,stored_degree);if let Some(x)=prev{assert!(x<k)}prev=Some(k);assert!(avail(k.sig,e).contains(&(k.pivot as usize)));let old=i128::from_le_bytes(z[43..59].try_into().unwrap());assert_ne!(old,0);assert_eq!(old%SCALE_RATIO,0);let w=old/SCALE_RATIO;k.degree=target_degree;out.add(eval(&k,w,e,k4,dual));}
 let mut extra=[0u8;1];assert_eq!(r.read(&mut extra).unwrap(),0);assert_eq!(out.keys,n);eprintln!("PASS {} keys={} full={} irr={}",mode,out.keys,out.full_n,out.irr_n);out
}

fn json_q(name:&str,path:&str,stored:u8,target:u8,q:Q)->String{format!("\"{}\":{{\"source_profile\":\"{}\",\"stored_degree\":{},\"target_degree\":{},\"keys\":{},\"full_evaluations\":{},\"irreducible_evaluations\":{},\"full_charge_scaled_U\":\"{}\",\"irreducible_charge_scaled_U\":\"{}\",\"signed_weight_scaled_U\":\"{}\",\"l1_weight_scaled_U\":\"{}\"}}",name,path,stored,target,q.keys,q.full_n,q.irr_n,q.full,q.irr,q.signed,q.l1)}

pub fn run(){
 assert_eq!(OLD_SCALE%U,0);assert_eq!(SCALE_RATIO,198237);let begun=Instant::now();let e=parse();let(k4,dual)=aux(&e);let literal=literal_selftest(&e,&k4);eprintln!("PASS literal profile/cycle checks={}",literal);
 let specs=[
  ("K14_R33",format!("{}weights_k17_k14_k2.bin",K19),2,3),
  ("K15_R23",format!("{}weights_k17_k15_k2.bin",K19),2,3),
  ("K16_R4",format!("{}weights_k16_direct_k3.bin",K19),3,4),
  ("K17_R3",format!("{}weights_k17_direct_k2.bin",K19),2,3),
 ];
 let mut fields=Vec::new();let mut total=Q::default();for(name,path,stored,target)in specs{let q=read_group(name,&path,stored,target,&e,&k4,&dual);total.add(q);fields.push(json_q(name,&path,stored,target,q));}
 let text=format!("{{\"status\":\"PASS_K20_17_PATH_PROFILE_CHARGE\",\"scale_U\":{},\"old_scale\":{},\"scale_ratio\":{},\"literal_profile_cycle_checks\":{},\"groups\":{{{}}},\"subtotal\":{{\"covered_DAG_paths\":17,\"keys\":{},\"full_evaluations\":{},\"irreducible_evaluations\":{},\"full_charge_scaled_U\":\"{}\",\"irreducible_charge_scaled_U\":\"{}\"}},\"elapsed_seconds\":{:.3},\"scope\":\"four source-compressed terminal profile evaluators only; no parent-row collection or K21 tails\"}}",U,OLD_SCALE,SCALE_RATIO,literal,fields.join(","),total.keys,total.full_n,total.irr_n,total.full,total.irr,begun.elapsed().as_secs_f64());
 let tmp=format!("{}results_k20_17_path_profile_charge.json.tmp",OUT20);let dst=format!("{}results_k20_17_path_profile_charge.raw.json",OUT20);std::fs::write(&tmp,&text).unwrap();rename(tmp,dst).unwrap();println!("{}",text)
}
}
fn main(){base::run()}
