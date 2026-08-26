//! Exact site-colour fine-grade census for K16 targets and source columns.
//!
//! Grades have 24 entries `(site,colour)`.  Target rows are streamed from the
//! frozen literal-orbit JSON; source columns are traversed from the exact
//! 98,609,090-key DAFSA.  Only grades and counts are retained.

use std::collections::HashMap;
use std::env;
use std::fs::{File, read};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::path::Path;
use std::time::{Duration,Instant};

const ROOT: &str = "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23";
const TARGET: &str = "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/results_orbit0_k16_literal_residual.json";
const COLUMN_DAFSA: &str = "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/weighted_k16_source_columns.dafsa";
const TARGET_COUNT:u64=1_848_174;
const COLUMN_COUNT:u64=98_609_090;
const CAP:Duration=Duration::from_secs(295);

#[derive(Clone)]
struct Action {sites:[u8;8], colours:[u8;3]}

#[derive(Default,Clone,Copy)]
struct Counts {target:u64, columns:u64}

fn cell_id(mut u:u8,mut v:u8,mut a:u8,mut b:u8)->u8 {
    if u>v {std::mem::swap(&mut u,&mut v);std::mem::swap(&mut a,&mut b);}
    let mut edge=0u8;for x in 0..u{edge+=7-x;}edge+=v-u-1;edge*9+a*3+b
}

fn decode(cell:u8)->(u8,u8,u8,u8){
    let edge=cell/9;let a=(cell%9)/3;let b=cell%3;let mut seen=0u8;
    for u in 0..8u8{for v in u+1..8u8{if seen==edge{return(u,v,a,b);}seen+=1;}}
    unreachable!()
}

fn next_permutation(v:&mut[u8])->bool{
    let Some(i)=(0..v.len()-1).rev().find(|&i|v[i]<v[i+1])else{return false};
    let j=(i+1..v.len()).rev().find(|&j|v[i]<v[j]).unwrap();v.swap(i,j);v[i+1..].reverse();true
}

fn permutations(n:u8)->Vec<Vec<u8>>{
    let mut p:Vec<u8>=(0..n).collect();let mut out=vec![p.clone()];
    while next_permutation(&mut p){out.push(p.clone());}out
}

fn anchors()->Vec<[u8;4]>{
    [[0,0,1,1],[1,1,2,2],[2,2,0,0]].iter().map(|p|{
        let mut r=[0u8;4];for k in 0..4{r[k]=cell_id(2*k as u8,2*k as u8+1,p[k],p[k]);}
        r.sort_unstable();r
    }).collect()
}

fn actions()->Vec<Action>{
    let factor=anchors();let mut expected=factor.clone();expected.sort_unstable();let mut out=Vec::new();
    for blocks in permutations(4){for mask in 0..16u8{
        let mut sites=[0u8;8];for source in 0..4{let target=blocks[source]as usize;let flip=((mask>>source)&1)as usize;
            sites[2*source]=(2*target+flip)as u8;sites[2*source+1]=(2*target+1-flip)as u8;}
        for cp in permutations(3){let action=Action{sites,colours:[cp[0],cp[1],cp[2]]};
            let mut moved:Vec<[u8;4]>=factor.iter().map(|row|{let mut r=[0u8;4];for(i,&cell)in row.iter().enumerate(){
                let(u,v,a,b)=decode(cell);r[i]=cell_id(action.sites[u as usize],action.sites[v as usize],action.colours[a as usize],action.colours[b as usize]);}
                r.sort_unstable();r}).collect();moved.sort_unstable();if moved==expected{out.push(action);}
        }
    }}assert_eq!(out.len(),384);out
}

fn moved_grade(grade:&[u8;24],action:&Action)->[u8;24]{
    let mut out=[0u8;24];for site in 0..8{for colour in 0..3{
        out[3*action.sites[site]as usize+action.colours[colour]as usize]=grade[3*site+colour];
    }}out
}

fn canonical_grade(grade:[u8;24],actions:&[Action],cache:&mut HashMap<[u8;24],[u8;24]>)->[u8;24]{
    if let Some(answer)=cache.get(&grade){return *answer;}
    let mut best=[255u8;24];let mut orbit=Vec::with_capacity(384);
    for action in actions{let moved=moved_grade(&grade,action);if moved<best{best=moved;}orbit.push(moved);}
    for moved in orbit{cache.entry(moved).or_insert(best);}best
}

fn grade_cells(cells:impl Iterator<Item=u8>)->[u8;24]{
    let mut grade=[0u8;24];for cell in cells{let(u,v,a,b)=decode(cell);
        grade[3*u as usize+a as usize]+=1;grade[3*v as usize+b as usize]+=1;}grade
}

fn parse_hex(s:&str)->Vec<u8>{let b=s.as_bytes();(0..b.len()).step_by(2).map(|i|{
    let h=(b[i]as char).to_digit(16).unwrap();let l=(b[i+1]as char).to_digit(16).unwrap();(16*h+l)as u8}).collect()}

fn target_census(actions:&[Action],cache:&mut HashMap<[u8;24],[u8;24]>,counts:&mut HashMap<[u8;24],Counts>)->u64{
    let reader=BufReader::with_capacity(1<<20,File::open(TARGET).unwrap());let mut inside=false;let mut expect=0u8;let mut records=0u64;
    for line in reader.lines(){let line=line.unwrap();if !inside{if line.starts_with("  \"literal_orbits\": ["){inside=true;}continue;}
        if line=="  ],"{break;}let token=line.trim().trim_end_matches(',');
        if expect==0&&token.len()==50&&token.starts_with('"'){let row=parse_hex(&token[1..49]);
            let grade=canonical_grade(grade_cells(row.into_iter()),actions,cache);counts.entry(grade).or_default().target+=1;expect=1;
        }else if expect==1{expect=2;}else if expect==2{expect=0;records+=1;}
    }assert_eq!(records,TARGET_COUNT);records
}

fn u16le(x:&[u8])->u16{u16::from_le_bytes([x[0],x[1]])}
fn u32le(x:&[u8])->u32{u32::from_le_bytes([x[0],x[1],x[2],x[3]])}
fn u64le(x:&[u8])->u64{u64::from_le_bytes([x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]])}

struct Traversal<'a>{
    data:&'a[u8],offsets:Vec<u32>,actions:&'a[Action],cache:&'a mut HashMap<[u8;24],[u8;24]>,
    counts:&'a mut HashMap<[u8;24],Counts>,key:[u8;22],grade:[u8;24],columns:u64,visits:u64,
    samples:Vec<(u64,[u8;22],[u8;24])>,started:Instant,
}

impl<'a> Traversal<'a>{
    fn walk(&mut self,state:u32,depth:usize){
        self.visits+=1;let off=self.offsets[state as usize]as usize;let final_state=self.data[off+1]!=0;let degree=u16le(&self.data[off+2..off+4])as usize;
        if final_state{assert_eq!(depth,22);self.columns+=1;let canonical=canonical_grade(self.grade,self.actions,self.cache);
            self.counts.entry(canonical).or_default().columns+=1;
            if matches!(self.columns,1|49_304_545|98_609_090){self.samples.push((self.columns,self.key,self.grade));}
            if self.columns%5_000_000==0{eprintln!("COLUMNS {} grades={} cache={} visits={} elapsed={:.1}",self.columns,self.counts.len(),self.cache.len(),self.visits,self.started.elapsed().as_secs_f64());}
            return;
        }
        let base=off+4;for i in 0..degree{let p=base+5*i;let label=self.data[p];let target=u32le(&self.data[p+1..p+5]);self.key[depth]=label;
            if depth==1{let code=u16::from_be_bytes([self.key[0],label]);let mut value=code;let mut word=[0u8;8];for j in(0..8).rev(){word[j]=(value%3)as u8;value/=3;}
                for site in 0..8{self.grade[3*site+word[site]as usize]+=1;}self.walk(target,depth+1);for site in 0..8{self.grade[3*site+word[site]as usize]-=1;}
            }else if depth>=2{let(u,v,a,b)=decode(label);self.grade[3*u as usize+a as usize]+=1;self.grade[3*v as usize+b as usize]+=1;
                self.walk(target,depth+1);self.grade[3*u as usize+a as usize]-=1;self.grade[3*v as usize+b as usize]-=1;
            }else{self.walk(target,depth+1);}
        }
    }
}

fn perfect_matchings(vertices:&[u8])->Vec<Vec<(u8,u8)>>{if vertices.is_empty(){return vec![vec![]];}let u=vertices[0];let mut out=Vec::new();
    for i in 1..vertices.len(){let v=vertices[i];let mut rest=Vec::new();rest.extend_from_slice(&vertices[1..i]);rest.extend_from_slice(&vertices[i+1..]);
        for mut tail in perfect_matchings(&rest){let mut row=vec![(u,v)];row.append(&mut tail);out.push(row);}}out}

fn verify_samples(samples:&[(u64,[u8;22],[u8;24])]){
    let pms=perfect_matchings(&(0..8u8).collect::<Vec<_>>());assert_eq!(pms.len(),105);
    for &(ordinal,key,expected)in samples{let code=u16::from_be_bytes([key[0],key[1]]);let mut value=code;let mut word=[0u8;8];for j in(0..8).rev(){word[j]=(value%3)as u8;value/=3;}
        for pm in &pms{let mut row=Vec::from(&key[2..]);for &(u,v)in pm{row.push(cell_id(u,v,word[u as usize],word[v as usize]));}row.sort_unstable();
            assert_eq!(grade_cells(row.into_iter()),expected,"sample ordinal {} word {}",ordinal,code);}
    }
}

fn quantiles(mut values:Vec<u64>)->[u64;8]{values.sort_unstable();let n=values.len();let at=|num:usize,den:usize|values[((n-1)*num)/den];
    [values[0],at(1,4),at(1,2),at(3,4),at(9,10),at(19,20),at(99,100),values[n-1]]}

fn hex_grade(g:&[u8;24])->String{g.iter().map(|x|format!("{x:02x}")).collect()}

fn main(){let started=Instant::now();let actions=actions();let mut cache=HashMap::new();let mut counts=HashMap::new();
    let targets=target_census(&actions,&mut cache,&mut counts);eprintln!("TARGETS {} grades={} cache={} elapsed={:.1}",targets,counts.len(),cache.len(),started.elapsed().as_secs_f64());
    let data=read(COLUMN_DAFSA).unwrap();assert_eq!(data.len(),515_468_936);assert_eq!(&data[..11],b"K16COLDAFSA");let nodes=u64le(&data[24..32]);let arcs=u64le(&data[32..40]);let root=u64le(&data[40..48])as u32;
    assert_eq!((nodes,arcs,root),(39_763_164,71_283_240,39_763_163));let mut offsets=Vec::with_capacity(nodes as usize);let mut pos=80usize;
    for _ in 0..nodes{offsets.push(pos as u32);let degree=u16le(&data[pos+2..pos+4])as usize;pos+=4+5*degree;}assert_eq!(pos,data.len());
    let mut traversal=Traversal{data:&data,offsets,actions:&actions,cache:&mut cache,counts:&mut counts,key:[0;22],grade:[0;24],columns:0,visits:0,samples:Vec::new(),started};
    traversal.walk(root,0);assert_eq!(traversal.columns,COLUMN_COUNT);verify_samples(&traversal.samples);let visits=traversal.visits;let samples=traversal.samples.clone();drop(traversal);
    assert!(started.elapsed()<CAP,"fine-grade census exceeded hard cap");assert_eq!(counts.values().map(|x|x.target).sum::<u64>(),TARGET_COUNT);
    let column_total=counts.values().map(|x|x.columns).sum::<u64>();
    if env::args().any(|x|x=="--mutate"){assert_eq!(column_total,COLUMN_COUNT+1,"hostile column-total mutation fired");}
    assert_eq!(column_total,COLUMN_COUNT);
    assert!(counts.values().all(|x|x.target>0&&x.columns>0),"target/column grade supports differ");
    let mut records:Vec<_>=counts.into_iter().collect();records.sort_unstable_by_key(|x|x.0);let target_q=quantiles(records.iter().map(|x|x.1.target).collect());let column_q=quantiles(records.iter().map(|x|x.1.columns).collect());
    let table=Path::new(ROOT).join("k16_fine_grade_census.tsv");let mut out=BufWriter::new(File::create(&table).unwrap());writeln!(out,"grade_hex\ttarget_row_H_orbits\tsource_column_H_orbits").unwrap();
    for(g,c)in &records{writeln!(out,"{}\t{}\t{}",hex_grade(g),c.target,c.columns).unwrap();}out.flush().unwrap();
    let result=Path::new(ROOT).join("results_k16_fine_grade_census.json");let mut out=BufWriter::new(File::create(&result).unwrap());
    writeln!(out,"{{\n  \"schema\": \"orbit0-k16-fine-grade-census-v1\",\n  \"H_order\": 384,\n  \"grade_coordinates\": 24,\n  \"target_row_H_orbits\": {},\n  \"source_column_H_orbits\": {},\n  \"target_bearing_fine_grade_H_orbits\": {},\n  \"ordinary_column_trie_nodes_visited\": {},\n  \"target_count_quantiles_min_p25_p50_p75_p90_p95_p99_max\": {:?},\n  \"column_count_quantiles_min_p25_p50_p75_p90_p95_p99_max\": {:?},\n  \"grade_supports_equal\": true,\n  \"sample_output_grade_checks\": {},\n  \"elapsed_seconds\": {:.3}\n}}",
        TARGET_COUNT,COLUMN_COUNT,records.len(),visits,target_q,column_q,samples.len()*105,started.elapsed().as_secs_f64()).unwrap();out.flush().unwrap();
    println!("PASS grades={} target_q={:?} column_q={:?} visits={} cache={} samples={} elapsed={:.3}",records.len(),target_q,column_q,visits,cache.len(),samples.len()*105,started.elapsed().as_secs_f64());
}
