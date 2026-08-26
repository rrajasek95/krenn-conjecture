//! Bounded first-layer estimator for the sound whole degree-24 cutoff<17
//! target component.  It uses every literal incident mixed H_w column and
//! retains every output whose anchor-K degree is below 17.

use std::collections::{BTreeMap, HashSet};
use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;
use std::time::Instant;

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row24([u8;24]);

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column { word:u16, multiplier:[u8;20] }

#[derive(Clone,Copy)]
struct Action { sites:[u8;8], colours:[u8;3] }

struct Seed { anchors:[bool;252], actions:Vec<Action>, target:Vec<Row24>, cutoff:u8 }

struct Engine {
    anchors:[bool;252], cutoff:u8, cell_u:[u8;252], cell_v:[u8;252], cell_a:[u8;252], cell_b:[u8;252],
    edge_id:[[u8;8];8], transforms:Vec<[u8;252]>, word_transforms:Vec<Vec<u16>>,
    minimum_actions:Vec<Vec<u16>>, word_minimum:[u8;6561], matchings:Vec<[(u8,u8);4]>,
}

fn fail(message:impl AsRef<str>)->!{eprintln!("whole-cutoff17: {}",message.as_ref());std::process::exit(2)}
fn nibble(byte:u8)->u8{match byte{b'0'..=b'9'=>byte-b'0',b'a'..=b'f'=>byte-b'a'+10,b'A'..=b'F'=>byte-b'A'+10,_=>fail("bad hex")}}
fn parse_hex<const N:usize>(text:&str)->[u8;N]{if text.len()!=2*N{fail("bad hex length")}let bytes=text.as_bytes();let mut out=[0;N];for i in 0..N{out[i]=16*nibble(bytes[2*i])+nibble(bytes[2*i+1]);}out}

fn parse_seed(path:&Path)->io::Result<Seed>{
    let mut anchors=[false;252];let mut actions=Vec::new();let mut target=Vec::new();let mut cutoff=None;
    for (number,line) in BufReader::new(File::open(path)?).lines().enumerate(){let line=line?;let f:Vec<_>=line.split_whitespace().collect();if f.is_empty(){continue}match f[0]{
        "KRENN_WHOLE_CUTOFF17_T2_SEED_V1"|"KRENN_WHOLE_ANCHOR_TIMES_R8_CUTOFF9_SEED_V1"|"KRENN_WHOLE_ANCHOR_TIMES_E9_CUTOFF10_SEED_V1"=>if number!=0{fail("magic not first")},
        "DEGREE"=>if f[1]!="24"{fail("degree changed")},"CUTOFF"=>cutoff=Some(f[1].parse::<u8>().unwrap_or_else(|_|fail("bad cutoff"))),
        "ANCHORS"=>for cell in parse_hex::<12>(f[1]){anchors[cell as usize]=true},
        "ACTION"=>{let mut sites=[0;8];let mut colours=[0;3];for(i,b)in f[1].bytes().enumerate(){sites[i]=b-b'0'}for(i,b)in f[2].bytes().enumerate(){colours[i]=b-b'0'}actions.push(Action{sites,colours});},
        "TARGET"=>{if f[3]!="1"{fail("nonintegral target")};target.push(Row24(parse_hex::<24>(f[1])));},
        _=>fail(format!("unknown record {}",f[0])),
    }}
    if actions.len()!=2304||target.is_empty(){fail("seed count changed")}
    target.sort_unstable();
    Ok(Seed{anchors,actions,target,cutoff:cutoff.unwrap_or_else(||fail("missing cutoff"))})
}

fn decode_word(mut code:u16)->[u8;8]{let mut word=[0;8];for i in(0..8).rev(){word[i]=(code%3)as u8;code/=3;}word}
fn encode_word(word:&[u8;8])->u16{word.iter().fold(0,|code,digit|3*code+*digit as u16)}
fn matchings()->Vec<[(u8,u8);4]>{fn rec(v:&[u8],p:&mut Vec<(u8,u8)>,o:&mut Vec<[(u8,u8);4]>){if v.is_empty(){o.push([p[0],p[1],p[2],p[3]]);return}for i in 1..v.len(){let mut r=Vec::new();r.extend_from_slice(&v[1..i]);r.extend_from_slice(&v[i+1..]);p.push((v[0],v[i]));rec(&r,p,o);p.pop();}}let mut o=Vec::new();rec(&[0,1,2,3,4,5,6,7],&mut Vec::new(),&mut o);if o.len()!=105{fail("matching count")};o}

impl Engine{
    fn new(seed:&Seed)->Self{
        let mut cell_u=[0;252];let mut cell_v=[0;252];let mut cell_a=[0;252];let mut cell_b=[0;252];let mut edge_id=[[0;8];8];let mut edge=0u8;
        for u in 0..8u8{for v in u+1..8u8{edge_id[u as usize][v as usize]=edge;edge_id[v as usize][u as usize]=edge;for a in 0..3u8{for b in 0..3u8{let id=edge as usize*9+a as usize*3+b as usize;cell_u[id]=u;cell_v[id]=v;cell_a[id]=a;cell_b[id]=b;}}edge+=1;}}
        let cid=|u:u8,v:u8,a:u8,b:u8|->u8{(edge_id[u as usize][v as usize]as usize*9+a as usize*3+b as usize)as u8};
        let mut transforms=Vec::new();let mut word_transforms=Vec::new();
        for action in &seed.actions{let mut transform=[0;252];for id in 0..252{let(mut u,mut v)=(action.sites[cell_u[id]as usize],action.sites[cell_v[id]as usize]);let(mut a,mut b)=(action.colours[cell_a[id]as usize],action.colours[cell_b[id]as usize]);if u>v{std::mem::swap(&mut u,&mut v);std::mem::swap(&mut a,&mut b)}transform[id]=cid(u,v,a,b);}transforms.push(transform);let mut wt=vec![0u16;6561];for code in 0..6561u16{let word=decode_word(code);let mut image=[0;8];for site in 0..8{image[action.sites[site]as usize]=action.colours[word[site]as usize];}wt[code as usize]=encode_word(&image);}word_transforms.push(wt);}
        let mut minimum_actions:Vec<Vec<u16>>=(0..6561).map(|_|Vec::new()).collect();
        for code in 0..6561usize{let minimum=word_transforms.iter().map(|table|table[code]).min().unwrap();for(action,table)in word_transforms.iter().enumerate(){if table[code]==minimum{minimum_actions[code].push(action as u16);}}}
        let ms=matchings();let mut word_minimum=[4u8;6561];for code in 0..6561u16{let word=decode_word(code);let mut minimum=4;for matching in &ms{let mut off=0;for&(u,v)in matching{let id=cid(u,v,word[u as usize],word[v as usize]);off+=(!seed.anchors[id as usize])as u8;}minimum=minimum.min(off);}word_minimum[code as usize]=minimum;}
        Self{anchors:seed.anchors,cutoff:seed.cutoff,cell_u,cell_v,cell_a,cell_b,edge_id,transforms,word_transforms,minimum_actions,word_minimum,matchings:ms}
    }
    fn cid(&self,u:u8,v:u8,a:u8,b:u8)->u8{(self.edge_id[u as usize][v as usize]as usize*9+a as usize*3+b as usize)as u8}
    fn degree(&self,cells:&[u8])->u8{cells.iter().map(|cell|(!self.anchors[*cell as usize])as u8).sum()}
    fn canonical_row(&self,row:Row24)->Row24{let mut best=None;for transform in &self.transforms{let mut image=row.0.map(|cell|transform[cell as usize]);image.sort_unstable();let candidate=Row24(image);if best.map_or(true,|old|candidate<old){best=Some(candidate)}}best.unwrap()}
    fn canonical_column(&self,column:Column)->Column{let mut best=None;let min_word=self.word_transforms[self.minimum_actions[column.word as usize][0]as usize][column.word as usize];for&action in &self.minimum_actions[column.word as usize]{let mut multiplier=column.multiplier.map(|cell|self.transforms[action as usize][cell as usize]);multiplier.sort_unstable();let candidate=Column{word:min_word,multiplier};if best.map_or(true,|old|candidate<old){best=Some(candidate)}}best.unwrap()}
    fn remove(&self,row:Row24,selected:&[u8;4])->[u8;20]{let mut counts=[0u8;252];for&cell in selected{counts[cell as usize]+=1}let mut answer=[0;20];let mut next=0;for&cell in &row.0{if counts[cell as usize]>0{counts[cell as usize]-=1}else{answer[next]=cell;next+=1}}if next!=20{fail("bad divisor")};answer}
    fn incident(&self,row:Row24)->HashSet<Column>{let mut by_edge:Vec<Vec<u8>>=(0..28).map(|_|Vec::new()).collect();for&cell in &row.0{let edge=self.edge_id[self.cell_u[cell as usize]as usize][self.cell_v[cell as usize]as usize]as usize;if !by_edge[edge].contains(&cell){by_edge[edge].push(cell)}}let mut answer=HashSet::new();for matching in &self.matchings{let lists:[&[u8];4]=matching.map(|(u,v)|by_edge[self.edge_id[u as usize][v as usize]as usize].as_slice());if lists.iter().any(|x|x.is_empty()){continue}for&c0 in lists[0]{for&c1 in lists[1]{for&c2 in lists[2]{for&c3 in lists[3]{let selected=[c0,c1,c2,c3];let mut word=[255;8];for&cell in &selected{let id=cell as usize;word[self.cell_u[id]as usize]=self.cell_a[id];word[self.cell_v[id]as usize]=self.cell_b[id];}if word.iter().all(|colour|*colour==word[0]){continue}let raw=Column{word:encode_word(&word),multiplier:self.remove(row,&selected)};if self.degree(&raw.multiplier)+self.word_minimum[raw.word as usize]>=self.cutoff{fail("incident column escaped cutoff")};answer.insert(self.canonical_column(raw));}}}}}answer}
    fn retained_histogram(&self,column:Column,histogram:&mut BTreeMap<u8,usize>)->usize{let word=decode_word(column.word);let multiplier_degree=self.degree(&column.multiplier);let mut count=0;for matching in &self.matchings{let mut degree=multiplier_degree;for&(u,v)in matching{degree+=(!self.anchors[self.cid(u,v,word[u as usize],word[v as usize])as usize])as u8;}if degree<self.cutoff{*histogram.entry(degree).or_default()+=1;count+=1}}count}
    fn canonical_outputs(&self,column:Column)->Vec<Row24>{let word=decode_word(column.word);let md=self.degree(&column.multiplier);let mut answer=Vec::new();for matching in &self.matchings{let mut row=[0;24];row[..20].copy_from_slice(&column.multiplier);let mut degree=md;for(i,&(u,v))in matching.iter().enumerate(){let cell=self.cid(u,v,word[u as usize],word[v as usize]);row[20+i]=cell;degree+=(!self.anchors[cell as usize])as u8;}if degree<self.cutoff{row.sort_unstable();answer.push(self.canonical_row(Row24(row)));}}answer}
}

#[derive(Default)]struct Piece{columns:HashSet<Column>,incidence:usize,row_hist:BTreeMap<usize,usize>}
fn sample_incidence(engine:&Engine,rows:&[Row24],workers:usize)->Piece{let chunk=rows.len().div_ceil(workers);let mut pieces=Vec::new();std::thread::scope(|scope|{let mut handles=Vec::new();for worker in 0..workers{let start=worker*chunk;let end=((worker+1)*chunk).min(rows.len());if start>=end{continue}handles.push(scope.spawn(move||{let begun=Instant::now();let mut p=Piece::default();for&row in &rows[start..end]{let columns=engine.incident(row);p.incidence+=columns.len();*p.row_hist.entry(columns.len()).or_default()+=1;p.columns.extend(columns);}eprintln!("sample worker={start}..{end} incidence={} cols={} elapsed={:.3}s",p.incidence,p.columns.len(),begun.elapsed().as_secs_f64());p}));}for handle in handles{pieces.push(handle.join().unwrap_or_else(|_|fail("worker panic")))}});let mut out=Piece::default();for p in pieces{out.incidence+=p.incidence;for(k,v)in p.row_hist{*out.row_hist.entry(k).or_default()+=v}out.columns.extend(p.columns);}out}

fn write_results(path:&Path,seed:&Seed,sample:&[Row24],piece:&Piece,retained:&BTreeMap<u8,usize>,retained_total:usize,bounded_columns:usize,bounded_outputs:usize,bounded_new:usize,elapsed:f64)->io::Result<()>{let mut out=File::create(path)?;write!(out,"{{\n  \"status\":\"UNAUDITED deterministic whole-cutoff first-layer estimate\",\n  \"scope\":\"All sampled incident mixed source columns are literal and all their outputs below the stated cutoff are retained; counts beyond the deterministic sample are estimates only.\",\n  \"cutoff\":{},\n  \"stabilizer_order\":{},\n  \"target_row_orbits\":{},\n  \"sample_rows\":{},\n  \"sample_incidence\":{},\n  \"sample_distinct_columns\":{},\n  \"estimated_total_incidence\":{},\n  \"sample_row_incidence_histogram\":{{",seed.cutoff,seed.actions.len(),seed.target.len(),sample.len(),piece.incidence,piece.columns.len(),piece.incidence as u128*seed.target.len()as u128/sample.len()as u128)?;for(i,(k,v))in piece.row_hist.iter().enumerate(){if i!=0{write!(out,",")?}write!(out,"\"{k}\":{v}")?}write!(out,"}},\n  \"sample_column_retained_output_degree_histogram\":{{")?;for(i,(k,v))in retained.iter().enumerate(){if i!=0{write!(out,",")?}write!(out,"\"{k}\":{v}")?}write!(out,"}},\n  \"sample_column_retained_outputs\":{retained_total},\n  \"bounded_output_columns\":{bounded_columns},\n  \"bounded_canonical_output_orbits\":{bounded_outputs},\n  \"bounded_output_orbits_outside_target\":{bounded_new},\n  \"elapsed_seconds\":{elapsed:.6}\n}}\n")?;Ok(())}

fn main(){let args:Vec<_>=env::args().collect();if args.len()!=4{eprintln!("usage: whole_cutoff17 SEED RESULTS SAMPLE_ROWS");std::process::exit(2)}let begun=Instant::now();let seed=parse_seed(Path::new(&args[1])).unwrap_or_else(|e|fail(e.to_string()));let engine=Engine::new(&seed);for&row in seed.target.iter().take(64){if engine.canonical_row(row)!=row{fail("target not canonical")}}let requested=args[3].parse::<usize>().unwrap_or_else(|_|fail("bad sample"));let count=requested.min(seed.target.len());let sample:Vec<_>=(0..count).map(|i|seed.target[i*seed.target.len()/count]).collect();let workers=std::thread::available_parallelism().map_or(4,|v|v.get()).min(8);let piece=sample_incidence(&engine,&sample,workers);let mut retained=BTreeMap::new();let mut retained_total=0;for&column in &piece.columns{retained_total+=engine.retained_histogram(column,&mut retained)}let bounded_columns=piece.columns.len().min(if seed.target.len()<=1000{piece.columns.len()}else{128});let mut outputs=HashSet::new();for&column in piece.columns.iter().take(bounded_columns){outputs.extend(engine.canonical_outputs(column))}let bounded_new=outputs.iter().filter(|row|seed.target.binary_search(row).is_err()).count();write_results(Path::new(&args[2]),&seed,&sample,&piece,&retained,retained_total,bounded_columns,outputs.len(),bounded_new,begun.elapsed().as_secs_f64()).unwrap_or_else(|e|fail(e.to_string()));eprintln!("PASS sample={} incidence={} cols={} retained={} bounded_outputs={} new={} elapsed={:.3}s",sample.len(),piece.incidence,piece.columns.len(),retained_total,outputs.len(),bounded_new,begun.elapsed().as_secs_f64());}
