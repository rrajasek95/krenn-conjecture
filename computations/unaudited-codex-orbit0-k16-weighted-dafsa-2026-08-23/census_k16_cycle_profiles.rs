//! Exact cycle-partition quotient census for the balanced K16 packet.

use std::collections::HashMap;
use std::fs::{File,read};
use std::io::{BufRead,BufReader,BufWriter,Write};
use std::path::Path;
use std::time::{Duration,Instant};

const ROOT:&str="computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23";
const TARGET:&str="computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/results_orbit0_k16_literal_residual.json";
const COLUMNS:&str="computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/weighted_k16_source_columns.dafsa";
const TARGET_COUNT:u64=1_848_174;const COLUMN_COUNT:u64=98_609_090;const CAP:Duration=Duration::from_secs(295);

#[derive(Clone,Copy,Debug)]struct Rat{n:i128,d:i128}
fn gcd(mut a:i128,mut b:i128)->i128{a=a.abs();b=b.abs();while b!=0{let r=a%b;a=b;b=r;}a}
impl Rat{fn new(mut n:i128,mut d:i128)->Self{assert!(d!=0);if d<0{n=-n;d=-d;}let g=gcd(n,d);Self{n:n/g,d:d/g}}
    fn add(self,other:Self)->Self{Self::new(self.n*other.d+other.n*self.d,self.d*other.d)}}

fn decode(cell:u8)->(u8,u8,u8,u8){let edge=cell/9;let a=(cell%9)/3;let b=cell%3;let mut seen=0u8;
    for u in 0..8u8{for v in u+1..8u8{if seen==edge{return(u,v,a,b);}seen+=1;}}unreachable!()}
fn ports(cell:u8)->(usize,usize){let(u,v,a,b)=decode(cell);((3*u+a)as usize,(3*v+b)as usize)}

struct Graph{parent:[u8;24],size:[u8;24],edges:[u8;24],degree:[u8;24]}
impl Graph{fn new()->Self{let mut parent=[0u8;24];for i in 0..24{parent[i]=i as u8;}Self{parent,size:[1;24],edges:[0;24],degree:[0;24]}}
    fn root(&self,mut x:usize)->usize{while self.parent[x]as usize!=x{x=self.parent[x]as usize;}x}
    fn add(&mut self,u:usize,v:usize){self.degree[u]+=1;self.degree[v]+=1;let mut a=self.root(u);let mut b=self.root(v);
        if a==b{self.edges[a]+=1;return;}if self.size[a]<self.size[b]{std::mem::swap(&mut a,&mut b);}self.parent[b]=a as u8;
        self.size[a]+=self.size[b];self.edges[a]+=self.edges[b]+1;}
}

type Partition=[u8;13]; // length, then at most twelve sorted cycle lengths
type Profile=[u8;13];   // four sorted path lengths, cycle count, up to eight sorted cycle lengths

fn partition(cells:&[u8])->Partition{let mut g=Graph::new();for &cell in cells{let(u,v)=ports(cell);g.add(u,v);}assert!(g.degree.iter().all(|&x|x==2));
    let mut parts=Vec::new();for i in 0..24{if g.root(i)==i{assert_eq!(g.edges[i],g.size[i]);parts.push(g.edges[i]);}}
    parts.sort_unstable();let mut out=[0u8;13];out[0]=parts.len()as u8;out[1..1+parts.len()].copy_from_slice(&parts);out}

fn profile(key:&[u8;22])->Profile{let mut g=Graph::new();for &cell in &key[2..]{let(u,v)=ports(cell);g.add(u,v);}let code=u16::from_be_bytes([key[0],key[1]]);
    let mut value=code;let mut word=[0u8;8];for i in(0..8).rev(){word[i]=(value%3)as u8;value/=3;}
    for site in 0..8{for colour in 0..3{let expected=if colour==word[site]as usize{1}else{2};assert_eq!(g.degree[3*site+colour],expected);}}
    let mut paths=Vec::new();let mut cycles=Vec::new();for i in 0..24{if g.root(i)!=i{continue;}let mut ones=0;
        for v in 0..24{if g.root(v)==i&&g.degree[v]==1{ones+=1;}else if g.root(v)==i{assert_eq!(g.degree[v],2);}}
        if ones==0{assert_eq!(g.edges[i],g.size[i]);cycles.push(g.edges[i]);}else{assert_eq!(ones,2);assert_eq!(g.edges[i]+1,g.size[i]);paths.push(g.edges[i]);}}
    assert_eq!(paths.len(),4);paths.sort_unstable();cycles.sort_unstable();assert!(cycles.len()<=8);let mut out=[0u8;13];
    out[..4].copy_from_slice(&paths);out[4]=cycles.len()as u8;out[5..5+cycles.len()].copy_from_slice(&cycles);out}

fn parse_hex(s:&str)->Vec<u8>{let b=s.as_bytes();(0..b.len()).step_by(2).map(|i|((b[i]as char).to_digit(16).unwrap()*16+(b[i+1]as char).to_digit(16).unwrap())as u8).collect()}
fn target_vector()->(HashMap<Partition,Rat>,u64){let reader=BufReader::with_capacity(1<<20,File::open(TARGET).unwrap());let mut inside=false;let mut state=0u8;
    let mut row=Vec::new();let mut numerator=0i128;let mut count=0u64;let mut out:HashMap<Partition,Rat>=HashMap::new();for line in reader.lines(){let line=line.unwrap();
        if !inside{if line.starts_with("  \"literal_orbits\": ["){inside=true;}continue;}if line=="  ],"{break;}let token=line.trim().trim_end_matches(',');
        if state==0&&token.len()==50&&token.starts_with('"'){row=parse_hex(&token[1..49]);state=1;}else if state==1{numerator=token.parse().unwrap();state=2;}
        else if state==2{let denominator:i128=token.parse().unwrap();let p=partition(&row);let value=Rat::new(numerator,denominator);out.entry(p).and_modify(|x|*x=x.add(value)).or_insert(value);count+=1;state=0;}}
    assert_eq!(count,TARGET_COUNT);out.retain(|_,x|x.n!=0);(out,count)}

fn u16le(x:&[u8])->u16{u16::from_le_bytes([x[0],x[1]])}fn u32le(x:&[u8])->u32{u32::from_le_bytes([x[0],x[1],x[2],x[3]])}
fn u64le(x:&[u8])->u64{u64::from_le_bytes([x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]])}

struct Walk<'a>{data:&'a[u8],offsets:Vec<u32>,key:[u8;22],profiles:HashMap<Profile,u64>,columns:u64,visits:u64,samples:Vec<(u64,[u8;22],Profile)>,start:Instant}
impl<'a>Walk<'a>{fn go(&mut self,state:u32,depth:usize){self.visits+=1;let off=self.offsets[state as usize]as usize;let final_state=self.data[off+1]!=0;
    if final_state{assert_eq!(depth,22);self.columns+=1;let p=profile(&self.key);*self.profiles.entry(p).or_default()+=1;
        if matches!(self.columns,1|49_304_545|98_609_090){self.samples.push((self.columns,self.key,p));}
        if self.columns%5_000_000==0{eprintln!("COLUMNS {} profiles={} visits={} elapsed={:.1}",self.columns,self.profiles.len(),self.visits,self.start.elapsed().as_secs_f64());}return;}
    let degree=u16le(&self.data[off+2..off+4])as usize;for i in 0..degree{let p=off+4+5*i;self.key[depth]=self.data[p];self.go(u32le(&self.data[p+1..p+5]),depth+1);}}
}

fn perfect_matchings(vertices:&[u8])->Vec<Vec<(u8,u8)>>{if vertices.is_empty(){return vec![vec![]];}let u=vertices[0];let mut out=Vec::new();
    for i in 1..vertices.len(){let v=vertices[i];let mut rest=Vec::new();rest.extend_from_slice(&vertices[1..i]);rest.extend_from_slice(&vertices[i+1..]);
        for mut tail in perfect_matchings(&rest){let mut row=vec![(u,v)];row.append(&mut tail);out.push(row);}}out}
fn cell_id(mut u:u8,mut v:u8,mut a:u8,mut b:u8)->u8{if u>v{std::mem::swap(&mut u,&mut v);std::mem::swap(&mut a,&mut b);}let mut e=0u8;for x in 0..u{e+=7-x;}e+=v-u-1;e*9+a*3+b}

fn abstract_completion_vector(profile:&Profile)->HashMap<Partition,u64>{let pms=perfect_matchings(&(0..8u8).collect::<Vec<_>>());let mut out=HashMap::new();
    for pm in pms{let mut parent=[0u8,1,2,3];fn root(parent:&[u8;4],mut x:usize)->usize{while parent[x]as usize!=x{x=parent[x]as usize;}x}
        for(a,b)in pm{let x=root(&parent,(a/2)as usize);let y=root(&parent,(b/2)as usize);if x!=y{parent[y]=x as u8;}}
        let mut groups:HashMap<usize,Vec<usize>>=HashMap::new();for i in 0..4{groups.entry(root(&parent,i)).or_default().push(i);}let mut cycles=Vec::new();
        for i in 0..profile[4]as usize{cycles.push(profile[5+i]);}for group in groups.values(){cycles.push(group.iter().map(|&i|profile[i]+1).sum());}
        cycles.sort_unstable();let mut partition=[0u8;13];partition[0]=cycles.len()as u8;partition[1..1+cycles.len()].copy_from_slice(&cycles);*out.entry(partition).or_default()+=1;
    }assert_eq!(out.values().sum::<u64>(),105);out}

fn verify_samples(samples:&[(u64,[u8;22],Profile)]){let pms=perfect_matchings(&(0..8u8).collect::<Vec<_>>());assert_eq!(pms.len(),105);
    for &(ordinal,key,expected)in samples{assert_eq!(profile(&key),expected);let code=u16::from_be_bytes([key[0],key[1]]);let mut value=code;let mut word=[0u8;8];
        for i in(0..8).rev(){word[i]=(value%3)as u8;value/=3;}let mut actual=HashMap::new();for pm in &pms{let mut row=Vec::from(&key[2..]);for &(u,v)in pm{row.push(cell_id(u,v,word[u as usize],word[v as usize]));}
            row.sort_unstable();*actual.entry(partition(&row)).or_default()+=1;}assert_eq!(actual,abstract_completion_vector(&expected));eprintln!("SAMPLE ordinal={} profile={:?}",ordinal,expected);}}

fn partition_text(p:&Partition)->String{(0..p[0]as usize).map(|i|p[i+1].to_string()).collect::<Vec<_>>().join(",")}
fn profile_text(p:&Profile)->(String,String){let paths=p[..4].iter().map(|x|x.to_string()).collect::<Vec<_>>().join(",");
    let cycles=(0..p[4]as usize).map(|i|p[5+i].to_string()).collect::<Vec<_>>().join(",");(paths,cycles)}

fn main(){let start=Instant::now();let(target,count)=target_vector();eprintln!("TARGET rows={} support={} elapsed={:.1}",count,target.len(),start.elapsed().as_secs_f64());
    let data=read(COLUMNS).unwrap();assert_eq!(data.len(),515_468_936);let nodes=u64le(&data[24..32]);let root=u64le(&data[40..48])as u32;let mut offsets=Vec::with_capacity(nodes as usize);let mut pos=80usize;
    for _ in 0..nodes{offsets.push(pos as u32);pos+=4+5*u16le(&data[pos+2..pos+4])as usize;}assert_eq!(pos,data.len());
    let mut walk=Walk{data:&data,offsets,key:[0;22],profiles:HashMap::new(),columns:0,visits:0,samples:Vec::new(),start};walk.go(root,0);
    assert_eq!(walk.columns,COLUMN_COUNT);assert!(start.elapsed()<CAP);verify_samples(&walk.samples);assert_eq!(walk.profiles.values().sum::<u64>(),COLUMN_COUNT);
    let mut profiles:Vec<_>=walk.profiles.into_iter().collect();profiles.sort_unstable_by_key(|x|x.0);let mut targets:Vec<_>=target.into_iter().collect();targets.sort_unstable_by_key(|x|x.0);
    let pp=Path::new(ROOT).join("k16_multiplier_cycle_profiles.tsv");let mut out=BufWriter::new(File::create(pp).unwrap());writeln!(out,"path_edge_lengths\tclosed_cycle_lengths\tcolumn_H_orbits").unwrap();
    for(p,n)in &profiles{let(a,b)=profile_text(p);writeln!(out,"{}\t{}\t{}",a,b,n).unwrap();}out.flush().unwrap();
    let tp=Path::new(ROOT).join("k16_target_cycle_partition_vector.tsv");let mut out=BufWriter::new(File::create(tp).unwrap());writeln!(out,"cycle_partition\tnumerator\tdenominator").unwrap();
    for(p,r)in &targets{writeln!(out,"{}\t{}\t{}",partition_text(p),r.n,r.d).unwrap();}out.flush().unwrap();
    let rp=Path::new(ROOT).join("results_k16_cycle_profile_census.json");let mut out=BufWriter::new(File::create(rp).unwrap());
    writeln!(out,"{{\n  \"schema\": \"orbit0-k16-cycle-profile-census-v1\",\n  \"target_row_H_orbits\": {},\n  \"source_column_H_orbits\": {},\n  \"realized_multiplier_path_cycle_profiles\": {},\n  \"nonzero_target_cycle_partitions\": {},\n  \"column_prefix_states_visited\": {},\n  \"literal_completion_sample_partitions_checked\": {},\n  \"elapsed_seconds\": {:.3}\n}}",
        TARGET_COUNT,COLUMN_COUNT,profiles.len(),targets.len(),walk.visits,walk.samples.len()*105,start.elapsed().as_secs_f64()).unwrap();out.flush().unwrap();
    println!("PASS profiles={} target_support={} visits={} samples={} elapsed={:.3}",profiles.len(),targets.len(),walk.visits,walk.samples.len()*105,start.elapsed().as_secs_f64());}
