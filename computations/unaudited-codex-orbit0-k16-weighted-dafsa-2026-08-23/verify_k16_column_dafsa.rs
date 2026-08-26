//! Independent structural replay of the unweighted K16 source-column DAFSA.

use std::env;
use std::convert::TryInto;
use std::fs::File;
use std::io::{BufReader, Read, Seek, SeekFrom};

const PATH: &str = "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/weighted_k16_source_columns.dafsa";
const EXPECTED_SAMPLE: &str = "0001000404080f4779797db5bccacfd3d7deeaeef2f2";
const EXPECTED_LAST: &str = "0392373a3b3c3c64656869697579797d8da4c6cacace";

fn u16le(bytes: &[u8]) -> u16 {u16::from_le_bytes(bytes.try_into().unwrap())}
fn u32le(bytes: &[u8]) -> u32 {u32::from_le_bytes(bytes.try_into().unwrap())}
fn u64le(bytes: &[u8]) -> u64 {u64::from_le_bytes(bytes.try_into().unwrap())}
fn hex(s: &str) -> Vec<u8> {(0..s.len()).step_by(2).map(|i|u8::from_str_radix(&s[i..i+2],16).unwrap()).collect()}

fn node(file: &mut File, offset: u64) -> (u8,bool,Vec<(u8,u32)>) {
    file.seek(SeekFrom::Start(offset)).unwrap();
    let mut h=[0u8;4]; file.read_exact(&mut h).unwrap();
    let degree=u16le(&h[2..4]) as usize;
    let mut edges=Vec::with_capacity(degree);
    for _ in 0..degree {
        let mut edge=[0u8;5]; file.read_exact(&mut edge).unwrap();
        edges.push((edge[0],u32le(&edge[1..5])));
    }
    (h[0],h[1]!=0,edges)
}

fn accepts(file: &mut File, offsets: &[u64], root: u32, key: &[u8]) -> bool {
    let mut state=root;
    for &label in key {
        let (_,_,edges)=node(file,offsets[state as usize]);
        let Ok(index)=edges.binary_search_by_key(&label,|e|e.0) else{return false};
        state=edges[index].1;
    }
    let (_,final_state,_)=node(file,offsets[state as usize]); final_state
}

fn extreme(file: &mut File, offsets: &[u64], root: u32, last: bool) -> Vec<u8> {
    let mut state=root; let mut key=Vec::new();
    loop {
        let (_,final_state,edges)=node(file,offsets[state as usize]);
        if final_state {return key;}
        let edge=if last {*edges.last().unwrap()} else {edges[0]};
        key.push(edge.0); state=edge.1;
    }
}

fn main() {
    let mutate=env::args().any(|x|x=="--mutate");
    let mut file=File::open(PATH).unwrap();
    let mut header=[0u8;80]; file.read_exact(&mut header).unwrap();
    assert_eq!(&header[..11],b"K16COLDAFSA");
    assert_eq!(u32le(&header[16..20]),1); assert_eq!(u32le(&header[20..24]),22);
    let nodes=u64le(&header[24..32]); let arcs=u64le(&header[32..40]);
    let root=u64le(&header[40..48]); let keys=u64le(&header[48..56]);
    let root_count=u64le(&header[56..64]);
    assert_eq!((nodes,arcs,root),(39_763_164,71_283_240,39_763_163));
    assert_eq!(keys,98_609_090); assert_eq!(root_count,98_609_090-u64::from(mutate));
    assert_eq!(u64le(&header[64..72]),384); assert_eq!(u64le(&header[72..80]),32256);

    let mut input=BufReader::with_capacity(1<<20,file.try_clone().unwrap());
    input.seek(SeekFrom::Start(80)).unwrap();
    let mut offsets=Vec::with_capacity(nodes as usize);
    let mut counts=Vec::with_capacity(nodes as usize);
    let mut position=80u64; let mut replay_arcs=0u64;
    for identifier in 0..nodes as u32 {
        offsets.push(position);
        let mut h=[0u8;4]; input.read_exact(&mut h).unwrap(); position+=4;
        let final_state=h[1]!=0; let degree=u16le(&h[2..4]) as usize;
        let mut count=u64::from(final_state); let mut last=None;
        for _ in 0..degree {
            let mut edge=[0u8;5]; input.read_exact(&mut edge).unwrap(); position+=5;
            let target=u32le(&edge[1..5]); assert!(target<identifier);
            if let Some(previous)=last {assert!(previous<edge[0]);} last=Some(edge[0]);
            count+=counts[target as usize]; replay_arcs+=1;
        }
        counts.push(count);
    }
    assert_eq!(replay_arcs,arcs); assert_eq!(counts[root as usize],keys);
    assert_eq!(position,file.metadata().unwrap().len());
    let first=extreme(&mut file,&offsets,root as u32,false);
    let last=extreme(&mut file,&offsets,root as u32,true);
    assert_eq!(first,hex(EXPECTED_SAMPLE)); assert_eq!(last,hex(EXPECTED_LAST));
    let sample=hex(EXPECTED_SAMPLE); assert_eq!(sample.len(),22);
    assert!(accepts(&mut file,&offsets,root as u32,&sample));
    let mut hostile=sample.clone(); hostile[0]=0xff;
    assert!(!accepts(&mut file,&offsets,root as u32,&hostile));
    println!("PASS nodes={} arcs={} keys={} bytes={} sample={}",nodes,arcs,keys,position,EXPECTED_SAMPLE);
}
