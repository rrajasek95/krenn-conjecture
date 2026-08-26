//! Exact bounded K24 B20 sparse-Gram gate; never performs production closure.
mod gate {
include!("../unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/run_k18_charge.rs");

use std::cmp::Ordering;
use std::collections::{BTreeMap, BTreeSet};
use std::fs::{create_dir_all, metadata, rename, File};
use std::io::{self, BufRead, BufReader, BufWriter, ErrorKind, Read, Write};
use std::path::{Path, PathBuf};
use std::process::Command;

const EXPECTED_SAMPLES:usize=257;
const RECORD_BYTES:u64=39;
const SOURCE_COLUMN_CAP:u64=1_000_000;
const WITNESS_SHA:&str="477b9ae9249b72d2e1c9ba4c71fd5b63605866ce533c6c79eb199b8103dd001c";
const D17_BIN_SHA:&str="cf4843d1ffc826c361e16540b33c3bd4bdf52be51c2a24f54a6d9182a7cc6a69";
const D18_BIN_SHA:&str="85fbfab465a7c007e6a3222e251c076c05457f86da421a0cb70251fe270f5fd1";
const EXPECTED_D17:u64=1_689_600;
const EXPECTED_D18:u64=476_160;

#[derive(Clone,Copy,Eq,Hash,Ord,PartialEq,PartialOrd)]
struct Column{word:u8,mult:[u8;20]}

#[derive(Clone)]
struct HMaps{
    maps:Vec<[u8;252]>,
    word_image:Vec<[u8;78]>,
    words:Vec<[u8;8]>,
    min_word_actions:Vec<Vec<u16>>,
    word_orbit_size:[u8;78],
}

#[derive(Clone,Copy)]
struct SourceRecord{column:Column,orbit:u16,mass:i128}

#[derive(Clone)]
struct Seed{column:Column,orbit:u16,numerator:i128,denominator:i128,key:String}

fn need(condition:bool,message:&str){if !condition{panic!("{}",message)}}

fn sha256(path:&Path)->String{
    let output=Command::new("shasum").arg("-a").arg("256").arg(path).output().unwrap();
    need(output.status.success(),"shasum failed");
    String::from_utf8(output.stdout).unwrap().split_whitespace().next().unwrap().to_string()
}

fn mixed_words()->Vec<[u8;8]>{
    let mut out=Vec::new();
    for a in 0..3u8{for b in 0..3u8{for c in 0..3u8{for d in 0..3u8{
        if a==b&&b==c&&c==d{continue}
        out.push([a,a,b,b,c,c,d,d]);
    }}}}
    need(out.len()==78,"mixed-word dictionary census");
    out
}

fn full_h_maps(e:&E)->HMaps{
    let b=read(format!("{}filtered_k16_structure.bin",DIR)).unwrap();
    let mut p=11;
    let nt=u32le(&b[p..p+4])as usize;p+=4;
    let nr=u32le(&b[p..p+4])as usize;p+=4;
    let np=u32le(&b[p..p+4])as usize;p+=4;
    let na=u32le(&b[p..p+4])as usize;p+=4;
    need((nt,nr,np,na)==(384,485,78,12),"structure header");
    p+=12;
    let mut maps=Vec::with_capacity(nt);
    for _ in 0..nt{
        let mut map=[0u8;252];map.copy_from_slice(&b[p..p+252]);p+=252;p+=12;maps.push(map);
    }
    let lookup:HashMap<[u8;4],u8>=e.anchors.iter().enumerate().map(|(i,&a)|(a,i as u8)).collect();
    need(lookup.len()==78,"anchor lookup");
    let mut word_image=Vec::new();
    for map in &maps{
        let mut image=[0u8;78];
        for(pivot,anchor)in e.anchors.iter().enumerate(){
            let mut moved=[0u8;4];
            for(i,&cell)in anchor.iter().enumerate(){moved[i]=map[cell as usize]}
            moved.sort_unstable();image[pivot]=*lookup.get(&moved).unwrap();
        }
        word_image.push(image);
    }
    let mut min_word_actions=Vec::with_capacity(78);
    let mut word_orbit_size=[0u8;78];
    for word in 0..78{
        let minimum=word_image.iter().map(|x|x[word]).min().unwrap();
        let actions:Vec<u16>=word_image.iter().enumerate().filter_map(|(a,x)|(x[word]==minimum).then_some(a as u16)).collect();
        let distinct:BTreeSet<u8>=word_image.iter().map(|x|x[word]).collect();
        need(384==actions.len()*distinct.len(),"word fibre theorem");
        word_orbit_size[word]=distinct.len()as u8;min_word_actions.push(actions);
    }
    HMaps{maps,word_image,words:mixed_words(),min_word_actions,word_orbit_size}
}

fn moved_column(c:Column,action:usize,h:&HMaps)->Column{
    let mut mult=[0u8;20];
    for(i,&cell)in c.mult.iter().enumerate(){mult[i]=h.maps[action][cell as usize]}
    mult.sort_unstable();
    Column{word:h.word_image[action][c.word as usize],mult}
}

fn canonical_column(c:Column,h:&HMaps)->(Column,u16){
    let actions=&h.min_word_actions[c.word as usize];
    let minimum_word=h.word_image[actions[0]as usize][c.word as usize];
    let mut images=BTreeSet::new();
    for &action in actions{
        let moved=moved_column(c,action as usize,h);
        need(moved.word==minimum_word,"minimum word fibre");
        images.insert(moved);
    }
    let orbit=(h.word_orbit_size[c.word as usize]as usize*images.len())as u16;
    need(orbit>0&&384%orbit==0,"column orbit divisor");
    (*images.iter().next().unwrap(),orbit)
}

fn column_orbit(c:Column,h:&HMaps)->BTreeSet<Column>{
    h.maps.iter().enumerate().map(|(action,_)|moved_column(c,action,h)).collect()
}

fn col_key(c:Column,h:&HMaps)->String{
    format!("{}:{}",h.words[c.word as usize].iter().map(|x|x.to_string()).collect::<String>(),
            c.mult.iter().map(|x|format!("{:02x}",x)).collect::<String>())
}

fn parse_key(key:&str,h:&HMaps)->Column{
    let mut pieces=key.split(':');
    let word_text=pieces.next().unwrap();
    let mult_text=pieces.next().unwrap();
    need(pieces.next().is_none()&&word_text.len()==8&&mult_text.len()==40,"column-key shape");
    let mut word=[0u8;8];
    for(i,ch)in word_text.bytes().enumerate(){need((b'0'..=b'2').contains(&ch),"word digit");word[i]=ch-b'0'}
    let word_id=h.words.binary_search(&word).expect("word outside frozen 78-word source dictionary")as u8;
    let mut mult=[0u8;20];
    for i in 0..20{mult[i]=u8::from_str_radix(&mult_text[2*i..2*i+2],16).unwrap()}
    need(mult.windows(2).all(|x|x[0]<=x[1]),"multiplier not sorted");
    Column{word:word_id,mult}
}

fn row_from(mult:&[u8;20],tail:&[u8;4])->Row{
    let mut bytes=[0u8;24];bytes[..20].copy_from_slice(mult);bytes[20..].copy_from_slice(tail);bytes.sort_unstable();Row(bytes)
}

fn source_read(reader:&mut BufReader<File>)->io::Result<Option<SourceRecord>>{
    let mut word=[0u8;1];
    match reader.read_exact(&mut word){
        Ok(())=>{},
        Err(error)if error.kind()==ErrorKind::UnexpectedEof=>return Ok(None),
        Err(error)=>return Err(error),
    }
    let mut mult=[0u8;20];let mut orbit=[0u8;2];let mut mass=[0u8;16];
    reader.read_exact(&mut mult)?;reader.read_exact(&mut orbit)?;reader.read_exact(&mut mass)?;
    Ok(Some(SourceRecord{column:Column{word:word[0],mult},orbit:u16::from_le_bytes(orbit),mass:i128::from_le_bytes(mass)}))
}

fn parse_seeds(path:&Path,h:&HMaps)->Vec<Seed>{
    need(sha256(path)==WITNESS_SHA,"witness hash");
    let file=BufReader::new(File::open(path).unwrap());
    let mut lines=file.lines();
    let header=lines.next().unwrap().unwrap();
    let expected="group_id\tlineage_id\tsample_bin\tglobal_selected_pivot_rank\tsource_cursor\tp1\tt1\tp2\tm1\tm2\tsource_row\tK20_parent_row\tmixed_word\tU20_multiplier\tcanonical_column_key\tcolumn_orbit_size\tH_action_to_canonical\texact_coefficient_numerator\texact_coefficient_denominator\tliteral_K24_row\ttop_output_count\ttop_charge_sum\ttop_self_pairing\tliteral_K24_terminal";
    need(header==expected,"witness header");
    let mut seeds=Vec::new();let mut keys=BTreeSet::new();
    for (expected_bin,line) in lines.enumerate(){
        let line=line.unwrap();let fields:Vec<_>=line.split('\t').collect();need(fields.len()==24,"witness width");
        need(fields[2].parse::<usize>().unwrap()==expected_bin,"sample-bin sequence");
        need(fields[22]=="60"&&fields[23]=="1","top literal guard");
        let column=parse_key(fields[14],h);let(canonical,orbit)=canonical_column(column,h);
        need(canonical==column,"witness key not natural canonical");
        need(orbit==fields[15].parse::<u16>().unwrap(),"witness orbit size");
        let numerator=fields[17].parse::<i128>().unwrap();let denominator=fields[18].parse::<i128>().unwrap();
        need(denominator>0&&numerator!=0,"witness coefficient");
        need(keys.insert(column),"duplicate natural witness key");
        seeds.push(Seed{column,orbit,numerator,denominator,key:fields[14].to_string()});
    }
    need(seeds.len()==EXPECTED_SAMPLES,"257 witness census");seeds
}

fn source_census(d17:&Path,d18:&Path,h:&HMaps)->(u64,u64,u64,u64,i128,BTreeMap<u16,u64>,BTreeSet<u8>){
    need(sha256(d17)==D17_BIN_SHA,"D17 compact hash");need(sha256(d18)==D18_BIN_SHA,"D18 compact hash");
    need(metadata(d17).unwrap().len()==EXPECTED_D17*RECORD_BYTES,"D17 record bytes");
    need(metadata(d18).unwrap().len()==EXPECTED_D18*RECORD_BYTES,"D18 record bytes");
    let mut a=BufReader::new(File::open(d17).unwrap());let mut b=BufReader::new(File::open(d18).unwrap());
    let mut x=source_read(&mut a).unwrap();let mut y=source_read(&mut b).unwrap();
    let(mut union,mut overlaps,mut zeros,mut retained,mut mass)=(0u64,0u64,0u64,0u64,0i128);
    let mut hist=BTreeMap::new();let mut words=BTreeSet::new();let mut previous=None;
    while x.is_some()||y.is_some(){
        let record=match (x,y){
            (Some(left),Some(right))=>match left.column.cmp(&right.column){
                Ordering::Less=>{x=source_read(&mut a).unwrap();left},
                Ordering::Greater=>{y=source_read(&mut b).unwrap();right},
                Ordering::Equal=>{need(left.orbit==right.orbit,"cross-group orbit mismatch");overlaps+=1;x=source_read(&mut a).unwrap();y=source_read(&mut b).unwrap();SourceRecord{column:left.column,orbit:left.orbit,mass:left.mass+right.mass}},
            },
            (Some(left),None)=>{x=source_read(&mut a).unwrap();left},
            (None,Some(right))=>{y=source_read(&mut b).unwrap();right},
            (None,None)=>unreachable!(),
        };
        union+=1;need(previous.map(|old|old<record.column).unwrap_or(true),"merged natural order");previous=Some(record.column);
        let(canonical,orbit)=canonical_column(record.column,h);need(canonical==record.column&&orbit==record.orbit,"compact natural canonical replay");
        if record.mass==0{zeros+=1}else{retained+=1;mass+=record.mass;*hist.entry(record.orbit).or_insert(0)+=1;words.insert(record.column.word);}
    }
    need(union+overlaps==EXPECTED_D17+EXPECTED_D18,"source merge count identity");
    (union,overlaps,zeros,retained,mass,hist,words)
}

fn edge_index(i:usize,j:usize,n:usize)->usize{need(i<=j,"upper edge index");i*n-i*(i.saturating_sub(1))/2+(j-i)}

fn build_sparse_gram(seeds:&[Seed],e:&E,h:&HMaps,edge_path:&Path)->(Vec<[u64;4]>,[u64;4],[u64;4],[u64;4],[usize;4],f64){
    let begun=Instant::now();let n=seeds.len();let mut grams=vec![[0u64;4];n*(n+1)/2];
    let term_counts=[1usize,12,32,60];
    let mut events_by_degree=[0u64;4];let mut unique_rows=[0u64;4];let mut maximum_row_columns=[0u64;4];let mut word_tables=BTreeSet::new();
    for(seed_index,seed)in seeds.iter().enumerate(){word_tables.insert(seed.column.word);let orbit=column_orbit(seed.column,h);need(orbit.len()==seed.orbit as usize,"seed orbit enumeration");need(seed_index<u16::MAX as usize,"seed index width");}
    for block in 0..4{
        let expected:usize=seeds.iter().map(|seed|seed.orbit as usize*term_counts[block]).sum();
        let mut events:Vec<(Row,u16)>=Vec::with_capacity(expected);
        for(index,seed)in seeds.iter().enumerate(){
            for moved in column_orbit(seed.column,h){
                if block==0{events.push((row_from(&moved.mult,&e.anchors[moved.word as usize]),index as u16));}
                else{for tail in &e.tails[moved.word as usize][block-1]{events.push((row_from(&moved.mult,tail),index as u16));}}
            }
        }
        need(events.len()==expected,"block event census");events.sort_unstable();events_by_degree[block]=events.len()as u64;
        let mut cursor=0usize;
        while cursor<events.len(){
            let row=events[cursor].0;let mut entries=Vec::<(usize,u64)>::new();
            while cursor<events.len()&&events[cursor].0==row{
                let column=events[cursor].1;let mut multiplicity=0u64;
                while cursor<events.len()&&events[cursor].0==row&&events[cursor].1==column{multiplicity+=1;cursor+=1}
                entries.push((column as usize,multiplicity));
            }
            unique_rows[block]+=1;maximum_row_columns[block]=maximum_row_columns[block].max(entries.len()as u64);
            for left in 0..entries.len(){for right in left..entries.len(){
                let(i,a)=entries[left];let(j,b)=entries[right];let(lo,hi)=if i<=j{(i,j)}else{(j,i)};
                grams[edge_index(lo,hi,n)][block]+=a*b;
            }}
        }
    }
    let mut out=BufWriter::new(File::create(edge_path.with_extension("tsv.tmp")).unwrap());
    writeln!(out,"left_index\tright_index\tG20\tG22\tG23\tG24").unwrap();
    for i in 0..n{for j in i..n{let g=grams[edge_index(i,j,n)];if g.iter().any(|&x|x!=0){writeln!(out,"{}\t{}\t{}\t{}\t{}\t{}",i,j,g[0],g[1],g[2],g[3]).unwrap();}}}
    out.flush().unwrap();rename(edge_path.with_extension("tsv.tmp"),edge_path).unwrap();
    (grams,events_by_degree,unique_rows,maximum_row_columns,[word_tables.len(),0,0,0],begun.elapsed().as_secs_f64())
}

fn gcd(mut a:i128,mut b:i128)->i128{a=a.abs();b=b.abs();while b!=0{let r=a%b;a=b;b=r}a}

fn write_columns(seeds:&[Seed],path:&Path){
    let temporary=path.with_extension("tsv.tmp");let mut out=BufWriter::new(File::create(&temporary).unwrap());
    writeln!(out,"index\tnatural_column_key\torbit_size\ttarget_coefficient_numerator\ttarget_coefficient_denominator").unwrap();
    for(i,seed)in seeds.iter().enumerate(){let divisor=gcd(seed.numerator,seed.denominator);writeln!(out,"{}\t{}\t{}\t{}\t{}",i,seed.key,seed.orbit,seed.numerator/divisor,seed.denominator/divisor).unwrap();}
    out.flush().unwrap();rename(temporary,path).unwrap();
}

fn main_inner(){
    let args:Vec<String>=std::env::args().collect();need(args.len()==6,"usage: gate witness d17.bin d18.bin output_dir");
    let witness=PathBuf::from(&args[1]);let d17=PathBuf::from(&args[2]);let d18=PathBuf::from(&args[3]);let output=PathBuf::from(&args[4]);let source_tag=&args[5];
    need(!output.exists(),"refuse output overwrite");create_dir_all(&output).unwrap();
    let begun=Instant::now();let e=parse();let h=full_h_maps(&e);let seeds=parse_seeds(&witness,&h);
    let(union,overlaps,zeros,retained,mass,hist,source_words)=source_census(&d17,&d18,&h);
    let columns_path=output.join("sample257_columns.tsv");let edges_path=output.join("sample257_sparse_gram_edges.tsv");write_columns(&seeds,&columns_path);
    let(grams,events,rows,max_incidence,word_info,gram_seconds)=build_sparse_gram(&seeds,&e,&h,&edges_path);
    let n=seeds.len();let(mut edges_any,mut edges_lower,mut edges_top)=(0u64,0u64,0u64);
    for g in &grams{if g.iter().any(|&x|x!=0){edges_any+=1}if g[..3].iter().any(|&x|x!=0){edges_lower+=1}if g[3]!=0{edges_top+=1}}
    need((0..n).all(|i|grams[edge_index(i,i,n)].iter().all(|&x|x>0)),"every seed diagonal realizes four blocks");
    let hist_json=hist.iter().map(|(k,v)|format!("\"{}\":{}",k,v)).collect::<Vec<_>>().join(",");
    let source_status=if retained>SOURCE_COLUMN_CAP{"COLUMN_CAP_BEFORE_INCIDENCE"}else{"SEED_ACCEPTED_NOT_CLOSED"};
    let result_path=output.join("results_k24_sparse_257_and_source1_gate.json");let temporary=result_path.with_extension("json.tmp");
    let text=format!(concat!(
        "{{\n",
        "  \"status\":\"PASS_BOUNDED_K24_SPARSE_CLOSURE_GATES_NO_LAUNCH\",\n",
        "  \"degree\":24,\n",
        "  \"source_tag\":\"{}\",\n",
        "  \"sample257\":{{\"input_records\":257,\"natural_unique_columns\":257,\"shared_word_tables\":{},\"events_by_degree\":{{\"20\":{},\"22\":{},\"23\":{},\"24\":{}}},\"unique_labelled_rows_by_degree\":{{\"20\":{},\"22\":{},\"23\":{},\"24\":{}}},\"maximum_columns_on_one_labelled_row_by_degree\":{{\"20\":{},\"22\":{},\"23\":{},\"24\":{}}},\"nonzero_upper_edges_any\":{},\"nonzero_upper_edges_lower\":{},\"nonzero_upper_edges_top\":{},\"dense_upper_pairs\":{},\"gram_seconds\":{:.9},\"natural_order_dedup_exact\":true}},\n",
        "  \"one_source_unit\":{{\"D17_records\":{},\"D18_records\":{},\"premerge_records\":{},\"natural_union_columns\":{},\"cross_group_duplicate_keys\":{},\"exact_zero_sums\":{},\"retained_nonzero_columns_N\":{},\"source_word_dictionary_entries\":{},\"orbit_size_histogram\":{{{}}},\"merged_orbit_mass_scaled_U\":\"{}\",\"column_cap\":{},\"closure_status\":\"{}\",\"processed_columns\":0,\"queued_columns\":{},\"known_nonzero_self_edges_lower_bound_E\":{},\"lower_transfer_below_K20_complete\":false}},\n",
        "  \"artifacts\":{{\"columns_path\":\"{}\",\"columns_sha256\":\"{}\",\"edges_path\":\"{}\",\"edges_sha256\":\"{}\",\"witness_sha256\":\"{}\",\"D17_compact_sha256\":\"{}\",\"D18_compact_sha256\":\"{}\"}},\n",
        "  \"resources\":{{\"total_seconds\":{:.9},\"retained_output_bytes\":{},\"event_storage_is_ephemeral\":true,\"broad_production_launched\":false}},\n",
        "  \"decision\":\"NO_LAUNCH_RELATIVE_CLOSURE: one source unit exceeds the frozen column cap before incidence; E and lower-transfer closure are incomplete\",\n",
        "  \"scope\":\"257 distributed source columns plus exact one-source-unit natural merge/cap only; no complete component, K24 membership, charge, or 103-shard production claim\"\n",
        "}}\n"),
        source_tag,word_info[0],events[0],events[1],events[2],events[3],rows[0],rows[1],rows[2],rows[3],max_incidence[0],max_incidence[1],max_incidence[2],max_incidence[3],edges_any,edges_lower,edges_top,n*(n+1)/2,gram_seconds,
        EXPECTED_D17,EXPECTED_D18,EXPECTED_D17+EXPECTED_D18,union,overlaps,zeros,retained,source_words.len(),hist_json,mass,SOURCE_COLUMN_CAP,source_status,retained,retained,
        columns_path.display(),sha256(&columns_path),edges_path.display(),sha256(&edges_path),WITNESS_SHA,D17_BIN_SHA,D18_BIN_SHA,
        begun.elapsed().as_secs_f64(),metadata(&columns_path).unwrap().len()+metadata(&edges_path).unwrap().len());
    File::create(&temporary).unwrap().write_all(text.as_bytes()).unwrap();rename(temporary,&result_path).unwrap();print!("{}",text);
}

pub fn run(){main_inner()}
}

fn main(){gate::run()}
