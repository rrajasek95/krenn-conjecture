//! Exhaustive source-faithful cycle-Morse pivot census on the frozen K16 rows.

use std::collections::BTreeMap;
use std::fs::{read,File};
use std::io::{BufWriter,Write};
use std::time::{Duration,Instant};

const INPUT:&str="computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/weighted_k16_literal_orbits.dafsa";
const OUTPUT:&str="computations/unaudited-codex-orbit0-k16-cycle-morse-census-2026-08-23/results_k16_cycle_morse_census.json";
const EXPECTED_ROWS:u64=1_848_174;
const EXPECTED_NODES:u64=768_820;
const EXPECTED_ARCS:u64=1_192_523;
const CAP:Duration=Duration::from_secs(240);

fn u16le(x:&[u8])->u16{u16::from_le_bytes([x[0],x[1]])}
fn u32le(x:&[u8])->u32{u32::from_le_bytes([x[0],x[1],x[2],x[3]])}
fn u64le(x:&[u8])->u64{u64::from_le_bytes([x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]])}
fn i64le(x:&[u8])->i64{i64::from_le_bytes([x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]])}

#[derive(Clone,Copy,Debug)] struct Rat{n:i128,d:i128}
fn gcd(mut a:i128,mut b:i128)->i128{a=a.abs();b=b.abs();while b!=0{let r=a%b;a=b;b=r;}if a==0{1}else{a}}
impl Rat{
    fn new(mut n:i128,mut d:i128)->Self{assert!(d!=0);if d<0{n=-n;d=-d;}let g=gcd(n,d);Self{n:n/g,d:d/g}}
    fn zero()->Self{Self{n:0,d:1}}
    fn add(self,x:Self)->Self{Self::new(self.n*x.d+x.n*self.d,self.d*x.d)}
    fn abs(self)->Self{Self{n:self.n.abs(),d:self.d}}
    fn text(self)->String{format!("[{},{ }]",self.n,self.d)}
}

#[derive(Clone,Copy,Default)] struct EdgeOption{cycle:u8,a:u8,b:u8}

#[derive(Clone)] struct Dsu{p:[u8;24],size:[u8;24],edges:[u8;24],degree:[u8;24]}
impl Dsu{
    fn new()->Self{let mut p=[0u8;24];for i in 0..24{p[i]=i as u8;}Self{p,size:[1;24],edges:[0;24],degree:[0;24]}}
    fn root(&self,mut x:usize)->usize{while self.p[x]as usize!=x{x=self.p[x]as usize;}x}
    fn add(&mut self,u:usize,v:usize){self.degree[u]+=1;self.degree[v]+=1;let mut a=self.root(u);let mut b=self.root(v);
        if a==b{self.edges[a]+=1;return;}if self.size[a]<self.size[b]{std::mem::swap(&mut a,&mut b);}self.p[b]=a as u8;
        self.size[a]+=self.size[b];self.edges[a]+=self.edges[b]+1;}
}

#[derive(Clone)] struct Stats{
    total:u64,pivotable:u64,unpivotable:u64,
    signed_total:Rat,signed_unpivotable:Rat,absolute_total:Rat,absolute_unpivotable:Rat,
}
impl Stats{fn new()->Self{Self{total:0,pivotable:0,unpivotable:0,signed_total:Rat::zero(),signed_unpivotable:Rat::zero(),absolute_total:Rat::zero(),absolute_unpivotable:Rat::zero()}}}

struct Analyzer{
    decoded:[(u8,u8,u8,u8);252],
    partition_stats:BTreeMap<Vec<u8>,Stats>,
    cycle_count_stats:BTreeMap<usize,Stats>,
    total:Stats,
    reasons:BTreeMap<&'static str,u64>,
    first_blocker:Option<(Vec<u8>,Rat,Vec<u8>,&'static str)>,
    first_pivot:Option<(Vec<u8>,String,Vec<u8>,Vec<u8>)>,
    mutate:bool,
}

impl Analyzer{
    fn new(mutate:bool)->Self{
        let mut decoded=[(0,0,0,0);252];let mut id=0usize;
        for u in 0..8u8{for v in u+1..8u8{for a in 0..3u8{for b in 0..3u8{decoded[id]=(u,v,a,b);id+=1;}}}}
        assert_eq!(id,252);
        Self{decoded,partition_stats:BTreeMap::new(),cycle_count_stats:BTreeMap::new(),total:Stats::new(),reasons:BTreeMap::new(),first_blocker:None,first_pivot:None,mutate}
    }

    fn matching_flags(options:&[[EdgeOption;9];28],counts:&[u8;28],site_mask:u16,cycle_mask:u16,first:u8,mixed:bool)->u8{
        if site_mask==0xff{return 1|if mixed{2}else{0};}
        let u=(0..8usize).find(|&i|site_mask&(1u16<<i)==0).unwrap();let mut flags=0u8;
        for v in u+1..8usize{if site_mask&(1u16<<v)!=0{continue;}let edge=u*(15-u)/2+(v-u-1);
            for oi in 0..counts[edge]as usize{let op=options[edge][oi];if cycle_mask&(1u16<<op.cycle)!=0{continue;}
                let (cu,cv)=if u<v{(op.a,op.b)}else{(op.b,op.a)};let mut nf=first;let mut nm=mixed;
                if nf==3{nf=cu;}else if cu!=nf{nm=true;}if cv!=nf{nm=true;}
                flags|=Self::matching_flags(options,counts,site_mask|(1u16<<u)|(1u16<<v),cycle_mask|(1u16<<op.cycle),nf,nm);
                if flags&2!=0{return flags;}
            }
        }flags
    }

    fn analyze(&mut self,row:&[u8;24],value:Rat){
        let mut graph=Dsu::new();for &cell in row{let(u,v,a,b)=self.decoded[cell as usize];graph.add((3*u+a)as usize,(3*v+b)as usize);}
        assert!(graph.degree.iter().all(|&x|x==2));
        let mut roots=Vec::new();for i in 0..24{if graph.root(i)==i{assert_eq!(graph.edges[i],graph.size[i]);roots.push(i);}}
        roots.sort_unstable_by_key(|&r|graph.size[r]);let partition:Vec<u8>=roots.iter().map(|&r|graph.size[r]).collect();
        let mut root_id=[0u8;24];for(i,&root)in roots.iter().enumerate(){for v in 0..24{if graph.root(v)==root{root_id[v]=i as u8;}}}
        let mut options=[[EdgeOption::default();9];28];let mut counts=[0u8;28];
        for &cell in row{let(u,v,a,b)=self.decoded[cell as usize];let edge=(u as usize)*(15-u as usize)/2+(v-u-1)as usize;
            let op=EdgeOption{cycle:root_id[(3*u+a)as usize],a,b};let mut duplicate=false;
            for i in 0..counts[edge]as usize{let x=options[edge][i];if x.cycle==op.cycle&&x.a==op.a&&x.b==op.b{duplicate=true;break;}}
            if !duplicate{let n=counts[edge]as usize;assert!(n<9);options[edge][n]=op;counts[edge]+=1;}}
        let flags=if roots.len()>=4{Self::matching_flags(&options,&counts,0,0,3,false)}else{0};
        let mut pivotable=flags&2!=0;if self.mutate&&self.total.total==0{pivotable=false;}let reason=if pivotable{"pivotable"}else if roots.len()<4{"fewer_than_four_cycles"}
            else if flags&1==0{"no_physical_pm_across_four_cycles"}else{"only_pure_pm_across_four_cycles"};
        *self.reasons.entry(reason).or_default()+=1;
        fn update(s:&mut Stats,value:Rat,pivotable:bool){s.total+=1;s.signed_total=s.signed_total.add(value);s.absolute_total=s.absolute_total.add(value.abs());
            if pivotable{s.pivotable+=1;}else{s.unpivotable+=1;s.signed_unpivotable=s.signed_unpivotable.add(value);s.absolute_unpivotable=s.absolute_unpivotable.add(value.abs());}}
        update(&mut self.total,value,pivotable);update(self.partition_stats.entry(partition.clone()).or_insert_with(Stats::new),value,pivotable);
        update(self.cycle_count_stats.entry(roots.len()).or_insert_with(Stats::new),value,pivotable);
        if !pivotable&&self.first_blocker.is_none(){self.first_blocker=Some((row.to_vec(),value,partition,reason));}
        if pivotable&&self.first_pivot.is_none(){
            // Recover the lexicographically first witness by a tiny exhaustive DFS with provenance.
            if let Some((word,cells))=witness(&options,&counts){let mut multiplier=row.to_vec();for cell in &cells{let p=multiplier.iter().position(|x|x==cell).unwrap();multiplier.remove(p);}self.first_pivot=Some((row.to_vec(),word,multiplier,cells));}
        }
    }
}

fn witness(options:&[[EdgeOption;9];28],counts:&[u8;28])->Option<(String,Vec<u8>)>{
    fn cell_id(u:usize,v:usize,a:u8,b:u8)->u8{let mut edge=0usize;for x in 0..u{edge+=7-x;}edge+=v-u-1;(9*edge+3*a as usize+b as usize)as u8}
    fn go(options:&[[EdgeOption;9];28],counts:&[u8;28],mask:u16,cycles:u16,colors:&mut[u8;8],cells:&mut Vec<u8>)->bool{
        if mask==0xff{return colors.iter().any(|&x|x!=colors[0]);}let u=(0..8).find(|&i|mask&(1<<i)==0).unwrap();
        for v in u+1..8{if mask&(1<<v)!=0{continue;}let edge=u*(15-u)/2+(v-u-1);for i in 0..counts[edge]as usize{let op=options[edge][i];if cycles&(1<<op.cycle)!=0{continue;}
            colors[u]=op.a;colors[v]=op.b;cells.push(cell_id(u,v,op.a,op.b));if go(options,counts,mask|(1<<u)|(1<<v),cycles|(1<<op.cycle),colors,cells){return true;}cells.pop();}}
        false}
    let mut colors=[0u8;8];let mut cells=Vec::new();if go(options,counts,0,0,&mut colors,&mut cells){Some((colors.iter().map(|x|char::from(b'0'+*x)).collect(),cells))}else{None}
}

fn hex(row:&[u8])->String{row.iter().map(|x|format!("{:02x}",x)).collect()}
fn stats_json(s:&Stats)->String{format!("{{\"orbits\":{},\"pivotable_orbits\":{},\"unpivotable_orbits\":{},\"signed_mass\":{},\"signed_unpivotable_mass\":{},\"absolute_mass\":{},\"absolute_unpivotable_mass\":{}}}",
    s.total,s.pivotable,s.unpivotable,s.signed_total.text(),s.signed_unpivotable.text(),s.absolute_total.text(),s.absolute_unpivotable.text())}

struct Walk<'a>{data:&'a[u8],offsets:Vec<u32>,key:[u8;24],rows:u64,analyzer:Analyzer,start:Instant,capped:bool}
impl<'a> Walk<'a>{fn go(&mut self,state:u32,depth:usize){if self.capped{return;}let off=self.offsets[state as usize]as usize;let final_state=self.data[off+1]!=0;
    if final_state{assert_eq!(depth,24);let n=i64le(&self.data[off+4..off+12]);let d=i64le(&self.data[off+12..off+20]);self.rows+=1;self.analyzer.analyze(&self.key,Rat::new(n as i128,d as i128));
        if self.rows%100_000==0{eprintln!("ROWS {} pivotable={} elapsed={:.1}",self.rows,self.analyzer.total.pivotable,self.start.elapsed().as_secs_f64());if self.start.elapsed()>=CAP{self.capped=true;}}return;}
    let degree=u16le(&self.data[off+2..off+4])as usize;for i in 0..degree{let p=off+20+5*i;self.key[depth]=self.data[p];self.go(u32le(&self.data[p+1..p+5]),depth+1);if self.capped{return;}}}}

fn main(){let start=Instant::now();let mutate=std::env::args().any(|x|x=="--mutate");let data=read(INPUT).unwrap();assert_eq!(&data[..10],b"K16WDAFSA1");assert_eq!(u32le(&data[16..20]),1);assert_eq!(u32le(&data[20..24]),24);
    let nodes=u64le(&data[24..32]);let arcs=u64le(&data[32..40]);let root=u64le(&data[40..48])as u32;let keys=u64le(&data[48..56]);assert_eq!((nodes,arcs,keys),(EXPECTED_NODES,EXPECTED_ARCS,EXPECTED_ROWS));
    let mut offsets=Vec::with_capacity(nodes as usize);let mut pos=120usize;for _ in 0..nodes{offsets.push(pos as u32);pos+=20+5*u16le(&data[pos+2..pos+4])as usize;}assert_eq!(pos,data.len());
    let mut walk=Walk{data:&data,offsets,key:[0;24],rows:0,analyzer:Analyzer::new(mutate),start,capped:false};walk.go(root,0);assert!(!walk.capped,"240-second cap reached; no complete census");assert_eq!(walk.rows,EXPECTED_ROWS);
    assert_eq!((walk.analyzer.total.pivotable,walk.analyzer.total.unpivotable),(751_988,1_096_186));
    assert_eq!(walk.analyzer.reasons.get("fewer_than_four_cycles"),Some(&889_820));assert_eq!(walk.analyzer.reasons.get("no_physical_pm_across_four_cycles"),Some(&206_366));assert_eq!(walk.analyzer.reasons.get("pivotable"),Some(&751_988));assert_eq!(walk.analyzer.reasons.get("only_pure_pm_across_four_cycles"),None);
    assert_eq!((walk.analyzer.total.signed_total.n,walk.analyzer.total.signed_total.d),(118_692_864,1));assert_eq!((walk.analyzer.total.signed_unpivotable.n,walk.analyzer.total.signed_unpivotable.d),(54_680_640,1));
    assert_eq!((walk.analyzer.total.absolute_total.n,walk.analyzer.total.absolute_total.d),(1_134_990_336,1));assert_eq!((walk.analyzer.total.absolute_unpivotable.n,walk.analyzer.total.absolute_unpivotable.d),(658_170_240,1));
    let mut out=BufWriter::new(File::create(OUTPUT).unwrap());writeln!(out,"{{").unwrap();writeln!(out,"  \"schema\": \"orbit0-k16-cycle-morse-census-v1\",").unwrap();
    writeln!(out,"  \"status\": \"EXACT_EXHAUSTIVE_LITERAL_CENSUS\",").unwrap();writeln!(out,"  \"input_rows\": {},",walk.rows).unwrap();writeln!(out,"  \"total\": {},",stats_json(&walk.analyzer.total)).unwrap();
    writeln!(out,"  \"reason_counts\": {{").unwrap();for(i,(k,v))in walk.analyzer.reasons.iter().enumerate(){writeln!(out,"    \"{}\": {}{}",k,v,if i+1==walk.analyzer.reasons.len(){""}else{","}).unwrap();}writeln!(out,"  }},").unwrap();
    writeln!(out,"  \"by_cycle_count\": {{").unwrap();for(i,(k,v))in walk.analyzer.cycle_count_stats.iter().enumerate(){writeln!(out,"    \"{}\": {}{}",k,stats_json(v),if i+1==walk.analyzer.cycle_count_stats.len(){""}else{","}).unwrap();}writeln!(out,"  }},").unwrap();
    writeln!(out,"  \"by_cycle_partition\": {{").unwrap();for(i,(k,v))in walk.analyzer.partition_stats.iter().enumerate(){let name=k.iter().map(|x|x.to_string()).collect::<Vec<_>>().join(",");writeln!(out,"    \"{}\": {}{}",name,stats_json(v),if i+1==walk.analyzer.partition_stats.len(){""}else{","}).unwrap();}writeln!(out,"  }},").unwrap();
    let(brow,bval,bpart,reason)=walk.analyzer.first_blocker.unwrap();writeln!(out,"  \"first_unpivotable\": {{\"row\":\"{}\",\"coefficient\":{},\"cycle_partition\":[{}],\"reason\":\"{}\"}},",hex(&brow),bval.text(),bpart.iter().map(|x|x.to_string()).collect::<Vec<_>>().join(","),reason).unwrap();
    let(prow,word,mult,cells)=walk.analyzer.first_pivot.unwrap();writeln!(out,"  \"first_pivotable_witness\": {{\"row\":\"{}\",\"mixed_word\":\"{}\",\"multiplier\":\"{}\",\"selected_cells\":\"{}\"}},",hex(&prow),word,hex(&mult),hex(&cells)).unwrap();
    writeln!(out,"  \"strict_descent\": \"Removing a physical PM whose four edges lie in distinct cycles gives four paths; every different completion merges at least two paths and strictly lowers cycle count.\",").unwrap();
    writeln!(out,"  \"scope_guard\": \"Frozen 1,848,174 K16 target H-orbits only; literal support pivot census, no closure or rank expansion.\"").unwrap();writeln!(out,"}}").unwrap();out.flush().unwrap();
    println!("PASS rows={} pivotable={} unpivotable={} partitions={} elapsed={:.3}",walk.rows,walk.analyzer.total.pivotable,walk.analyzer.total.unpivotable,walk.analyzer.partition_stats.len(),start.elapsed().as_secs_f64());}
