//! Streaming, exact H-orbit incidence census for the weighted K16 DAFSA keys.
//!
//! This does not build a Macaulay matrix.  It reads the frozen sorted terminal
//! representatives, enumerates literal perfect-matching divisors, and
//! canonicalizes source columns under the exact order-384 factor stabilizer.

use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap};
use std::fs::{File, create_dir, remove_dir, remove_file};
use std::hash::{Hash, Hasher};
use std::io::{BufRead, BufReader, BufWriter, Read, Seek, SeekFrom, Write};
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

const INPUT: &str = "computations/unaudited-codex-orbit0-k16-literal-collection-2026-08-22/results_orbit0_k16_literal_residual.json";
const KEY_COUNT: usize = 1_848_174;
const TIME_CAP: Duration = Duration::from_secs(295);
const COLUMN_DAFSA: &str = "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/weighted_k16_source_columns.dafsa";
const RUN_KEYS: usize = 2_000_000;

#[derive(Clone)]
struct Action {
    sites: [u8; 8],
    colours: [u8; 3],
    cells: [u8; 252],
}

fn cell_id(mut u: u8, mut v: u8, mut a: u8, mut b: u8) -> u8 {
    if u > v {
        std::mem::swap(&mut u, &mut v);
        std::mem::swap(&mut a, &mut b);
    }
    let mut edge = 0u8;
    for x in 0..u { edge += 7 - x; }
    edge += v - u - 1;
    edge * 9 + a * 3 + b
}

fn decode(cell: u8) -> (u8, u8, u8, u8) {
    let edge = cell / 9;
    let a = (cell % 9) / 3;
    let b = cell % 3;
    let mut seen = 0u8;
    for u in 0..8u8 {
        for v in (u + 1)..8u8 {
            if seen == edge { return (u, v, a, b); }
            seen += 1;
        }
    }
    unreachable!()
}

fn next_permutation(values: &mut [u8]) -> bool {
    if values.len() < 2 { return false; }
    let Some(i) = (0..values.len()-1).rev().find(|&i| values[i] < values[i+1]) else {
        return false;
    };
    let j = (i+1..values.len()).rev().find(|&j| values[i] < values[j]).unwrap();
    values.swap(i, j);
    values[i+1..].reverse();
    true
}

fn permutations(n: u8) -> Vec<Vec<u8>> {
    let mut p: Vec<u8> = (0..n).collect();
    let mut out = vec![p.clone()];
    while next_permutation(&mut p) { out.push(p.clone()); }
    out
}

fn move_word(code: u16, action: &Action) -> u16 {
    let mut word = [0u8; 8];
    let mut value = code;
    for i in (0..8).rev() { word[i] = (value % 3) as u8; value /= 3; }
    let mut moved = [0u8; 8];
    for i in 0..8 { moved[action.sites[i] as usize] = action.colours[word[i] as usize]; }
    let mut answer = 0u16;
    for x in moved { answer = answer * 3 + x as u16; }
    answer
}

fn anchors() -> Vec<[u8; 4]> {
    let patterns = [[0,0,1,1], [1,1,2,2], [2,2,0,0]];
    patterns.iter().map(|p| {
        let mut row = [0u8; 4];
        for k in 0..4 { row[k] = cell_id(2*k as u8, 2*k as u8+1, p[k], p[k]); }
        row.sort_unstable();
        row
    }).collect()
}

fn actions() -> Vec<Action> {
    let block_perms = permutations(4);
    let colour_perms = permutations(3);
    let factor = anchors();
    let mut answer = Vec::new();
    for blocks in block_perms {
        for flip_mask in 0..16u8 {
            let mut sites = [0u8; 8];
            for source in 0..4 {
                let target = blocks[source] as usize;
                let flip = ((flip_mask >> source) & 1) as usize;
                sites[2*source] = (2*target + flip) as u8;
                sites[2*source+1] = (2*target + 1-flip) as u8;
            }
            for cp in &colour_perms {
                let colours = [cp[0], cp[1], cp[2]];
                let mut cells = [0u8; 252];
                for c in 0..252u16 {
                    let (u,v,a,b) = decode(c as u8);
                    cells[c as usize] = cell_id(sites[u as usize], sites[v as usize],
                                                colours[a as usize], colours[b as usize]);
                }
                let action = Action { sites, colours, cells };
                let mut moved: Vec<[u8;4]> = factor.iter().map(|row| {
                    let mut r = *row;
                    for x in &mut r { *x = action.cells[*x as usize]; }
                    r.sort_unstable();
                    r
                }).collect();
                moved.sort_unstable();
                let mut expected = factor.clone(); expected.sort_unstable();
                if moved == expected { answer.push(action); }
            }
        }
    }
    assert_eq!(answer.len(), 384);
    answer
}

fn perfect_matchings(vertices: &[u8]) -> Vec<Vec<(u8,u8)>> {
    if vertices.is_empty() { return vec![vec![]]; }
    let u = vertices[0];
    let mut answer = Vec::new();
    for i in 1..vertices.len() {
        let v = vertices[i];
        let mut rest = Vec::new();
        rest.extend_from_slice(&vertices[1..i]);
        rest.extend_from_slice(&vertices[i+1..]);
        for mut tail in perfect_matchings(&rest) {
            let mut row = vec![(u,v)]; row.append(&mut tail); answer.push(row);
        }
    }
    answer
}

fn edge_index(u: u8, v: u8) -> usize {
    let mut edge = 0usize;
    for x in 0..u { edge += (7-x) as usize; }
    edge + (v-u-1) as usize
}

fn word_maps(actions: &[Action]) -> Vec<(u16, Vec<[u8;252]>)> {
    let mut stabilizers: HashMap<u16, Vec<usize>> = HashMap::new();
    for code in 0..6561u16 {
        let st: Vec<usize> = actions.iter().enumerate()
            .filter_map(|(i,a)| (move_word(code,a)==code).then_some(i)).collect();
        stabilizers.insert(code, st);
    }
    let mut answer = Vec::with_capacity(6561);
    for code in 0..6561u16 {
        let (h0, canonical) = actions.iter().enumerate()
            .map(|(i,a)|(i,move_word(code,a))).min_by_key(|x|x.1).unwrap();
        let maps = stabilizers[&canonical].iter().map(|&g| {
            let mut composed = [0u8;252];
            for c in 0..252 { composed[c] = actions[g].cells[actions[h0].cells[c] as usize]; }
            composed
        }).collect();
        answer.push((canonical, maps));
    }
    answer
}

fn canonical_column(word: u16, multiplier: &[u8;20], maps: &[(u16,Vec<[u8;252]>)]) -> [u8;22] {
    let (canonical, transforms) = &maps[word as usize];
    let mut best = [255u8;20];
    for transform in transforms {
        let mut moved = [0u8;20];
        for i in 0..20 { moved[i] = transform[multiplier[i] as usize]; }
        moved.sort_unstable();
        if moved < best { best = moved; }
    }
    let mut answer = [0u8;22];
    answer[0..2].copy_from_slice(&canonical.to_be_bytes());
    answer[2..].copy_from_slice(&best);
    answer
}

fn parse_hex(s: &str) -> Vec<u8> {
    let bytes = s.as_bytes();
    (0..bytes.len()).step_by(2).map(|i| {
        let h = (bytes[i] as char).to_digit(16).unwrap();
        let l = (bytes[i+1] as char).to_digit(16).unwrap();
        (16*h+l) as u8
    }).collect()
}

fn enumerate_column_keys<FN: FnMut([u8;22])>(
    row: &[u8;24], pms: &[[usize;4]], maps: &[(u16,Vec<[u8;252]>)], mut emit: FN
) -> usize {
    let mut candidates: Vec<Vec<u8>> = (0..28).map(|_| Vec::new()).collect();
    let mut previous = 255u8;
    for &cell in row {
        if cell == previous { continue; }
        previous = cell;
        let (u,v,_,_) = decode(cell);
        candidates[edge_index(u,v)].push(cell);
    }
    let mut raw = 0usize;
    for pm in pms {
        if pm.iter().any(|&e| candidates[e].is_empty()) { continue; }
        for &a in &candidates[pm[0]] { for &b in &candidates[pm[1]] {
        for &c in &candidates[pm[2]] { for &d in &candidates[pm[3]] {
            let mut term = [a,b,c,d]; term.sort_unstable();
            let mut digits = [0u8;8];
            for &cell in &term {
                let (u,v,x,y)=decode(cell); digits[u as usize]=x; digits[v as usize]=y;
            }
            if digits.iter().all(|&x|x==digits[0]) { continue; }
            let mut code=0u16; for x in digits { code=code*3+x as u16; }
            let mut multiplier=[0u8;20]; let mut i=0usize; let mut j=0usize; let mut k=0usize;
            while i<24 {
                if j<4 && row[i]==term[j] { i+=1; j+=1; }
                else { multiplier[k]=row[i]; k+=1; i+=1; }
            }
            assert_eq!((j,k),(4,20));
            emit(canonical_column(code,&multiplier,maps));
            raw += 1;
        }}}}
    }
    raw
}

fn flush_run(buffer: &mut Vec<[u8;22]>, directory: &Path, index: usize) -> PathBuf {
    buffer.sort_unstable();
    buffer.dedup();
    let path = directory.join(format!("run_{index:03}.bin"));
    let file = File::create(&path).unwrap();
    let mut out = BufWriter::with_capacity(1 << 20, file);
    for key in buffer.iter() { out.write_all(key).unwrap(); }
    out.flush().unwrap();
    buffer.clear();
    path
}

struct RunReader { input: BufReader<File> }

impl RunReader {
    fn new(path: &Path) -> Self {
        Self { input: BufReader::with_capacity(1 << 20, File::open(path).unwrap()) }
    }
    fn next(&mut self) -> Option<[u8;22]> {
        let mut key = [0u8;22];
        match self.input.read_exact(&mut key) {
            Ok(()) => Some(key),
            Err(error) if error.kind() == std::io::ErrorKind::UnexpectedEof => None,
            Err(error) => panic!("run read failed: {}", error),
        }
    }
}

#[derive(Clone, Eq)]
struct StateSignature {
    depth: u8,
    final_state: bool,
    edges: Box<[(u8,u32)]>,
}

impl PartialEq for StateSignature {
    fn eq(&self, other: &Self) -> bool {
        self.depth == other.depth && self.final_state == other.final_state
            && self.edges == other.edges
    }
}

impl Hash for StateSignature {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.depth.hash(state); self.final_state.hash(state); self.edges.hash(state);
    }
}

struct DafsaBuilder {
    registry: HashMap<StateSignature,u32>,
    language_counts: Vec<u64>,
    path: Vec<Vec<(u8,u32)>>,
    previous: Option<[u8;22]>,
    output: BufWriter<File>,
    nodes: u64,
    arcs: u64,
    keys: u64,
}

impl DafsaBuilder {
    fn new(path: &Path) -> Self {
        let mut output = BufWriter::with_capacity(1 << 20, File::create(path).unwrap());
        output.write_all(&[0u8;80]).unwrap();
        Self {
            registry: HashMap::new(), language_counts: Vec::new(),
            path: (0..23).map(|_| Vec::new()).collect(), previous: None,
            output, nodes: 0, arcs: 0, keys: 0,
        }
    }
    fn intern(&mut self, depth: usize) -> u32 {
        let edges: Box<[(u8,u32)]> = std::mem::take(&mut self.path[depth]).into_boxed_slice();
        let signature = StateSignature { depth: depth as u8, final_state: depth == 22, edges };
        if let Some(&identifier) = self.registry.get(&signature) { return identifier; }
        let identifier = self.nodes as u32;
        assert_eq!(identifier as usize, self.language_counts.len());
        let mut language_count = u64::from(signature.final_state);
        for &(_, target) in signature.edges.iter() {
            assert!(target < identifier);
            language_count += self.language_counts[target as usize];
        }
        self.output.write_all(&[signature.depth, u8::from(signature.final_state)]).unwrap();
        self.output.write_all(&(signature.edges.len() as u16).to_le_bytes()).unwrap();
        for &(label,target) in signature.edges.iter() {
            self.output.write_all(&[label]).unwrap();
            self.output.write_all(&target.to_le_bytes()).unwrap();
        }
        self.arcs += signature.edges.len() as u64;
        self.nodes += 1;
        self.language_counts.push(language_count);
        self.registry.insert(signature, identifier);
        identifier
    }
    fn push(&mut self, key: [u8;22]) {
        if let Some(previous) = self.previous {
            assert!(previous < key, "merged keys lost strict order");
            let common = previous.iter().zip(key.iter()).take_while(|(a,b)|a==b).count();
            for depth in ((common+1)..=22).rev() {
                let id = self.intern(depth);
                self.path[depth-1].push((previous[depth-1],id));
            }
        }
        self.previous = Some(key); self.keys += 1;
    }
    fn finish(mut self) -> (u64,u64,u32,u64) {
        let previous = self.previous.expect("empty column language");
        for depth in (1..=22).rev() {
            let id = self.intern(depth);
            self.path[depth-1].push((previous[depth-1],id));
        }
        let root = self.intern(0);
        let root_count = self.language_counts[root as usize];
        assert_eq!(root_count,self.keys);
        self.output.flush().unwrap();
        let mut file = self.output.into_inner().unwrap();
        file.seek(SeekFrom::Start(0)).unwrap();
        let mut magic=[0u8;16]; magic[..11].copy_from_slice(b"K16COLDAFSA");
        file.write_all(&magic).unwrap();
        file.write_all(&1u32.to_le_bytes()).unwrap();
        file.write_all(&22u32.to_le_bytes()).unwrap();
        file.write_all(&self.nodes.to_le_bytes()).unwrap();
        file.write_all(&self.arcs.to_le_bytes()).unwrap();
        file.write_all(&(root as u64).to_le_bytes()).unwrap();
        file.write_all(&self.keys.to_le_bytes()).unwrap();
        file.write_all(&root_count.to_le_bytes()).unwrap();
        file.write_all(&384u64.to_le_bytes()).unwrap();
        file.write_all(&32256u64.to_le_bytes()).unwrap();
        file.flush().unwrap();
        (self.nodes,self.arcs,root,root_count)
    }
}

fn merge_runs(paths: &[PathBuf], output: &Path) -> (u64,u64,u32,u64) {
    let mut readers: Vec<RunReader> = paths.iter().map(|p|RunReader::new(p)).collect();
    let mut heap: BinaryHeap<Reverse<([u8;22],usize)>> = BinaryHeap::new();
    for (index,reader) in readers.iter_mut().enumerate() {
        if let Some(key)=reader.next(){heap.push(Reverse((key,index)));}
    }
    let mut builder=DafsaBuilder::new(output);
    let mut previous=None;
    while let Some(Reverse((key,index)))=heap.pop() {
        if previous != Some(key) {builder.push(key); previous=Some(key);}
        if let Some(next)=readers[index].next(){heap.push(Reverse((next,index)));}
    }
    builder.finish()
}

fn main() {
    let start=Instant::now();
    let actions=actions();
    let maps=word_maps(&actions);
    let raw_pms=perfect_matchings(&(0..8u8).collect::<Vec<_>>());
    assert_eq!(raw_pms.len(),105);
    let pms: Vec<[usize;4]>=raw_pms.iter().map(|pm| {
        let mut x=[0usize;4]; for i in 0..4{x[i]=edge_index(pm[i].0,pm[i].1);} x
    }).collect();
    let temporary=PathBuf::from(format!("/tmp/k16_column_runs_{}",std::process::id()));
    create_dir(&temporary).unwrap();
    let mut buffer: Vec<[u8;22]>=Vec::with_capacity(RUN_KEYS);
    let mut runs: Vec<PathBuf>=Vec::new();
    let file=File::open(INPUT).unwrap(); let reader=BufReader::with_capacity(1<<20,file);
    let mut inside=false; let mut expect=0u8; let mut pending=[0u8;24]; let mut records=0usize;
    let mut raw_incidence=0u64; let mut run_unique_sum=0u64; let mut timed_out=false;
    for line in reader.lines() {
        let line=line.unwrap();
        if !inside { if line.starts_with("  \"literal_orbits\": [") {inside=true;} continue; }
        if line=="  ]," {break;}
        let token=line.trim().trim_end_matches(',');
        if expect==0 && token.len()==50 && token.starts_with('"') {
            let v=parse_hex(&token[1..49]); pending.copy_from_slice(&v); expect=1;
        } else if expect==1 { expect=2; }
        else if expect==2 {
            raw_incidence += enumerate_column_keys(&pending,&pms,&maps,|key|buffer.push(key)) as u64;
            records+=1; expect=0;
            if buffer.len()>=RUN_KEYS {
                let before=buffer.len();
                let path=flush_run(&mut buffer,&temporary,runs.len());
                let unique=(std::fs::metadata(&path).unwrap().len()/22) as usize;
                run_unique_sum+=unique as u64; runs.push(path);
                eprintln!("RUN records={} raw={} chunk_raw={} chunk_unique={} runs={} elapsed={:.1}",
                          records,raw_incidence,before,unique,runs.len(),start.elapsed().as_secs_f64());
            }
            if start.elapsed()>TIME_CAP {timed_out=true;break;}
        }
    }
    if !buffer.is_empty() {
        let before=buffer.len(); let path=flush_run(&mut buffer,&temporary,runs.len());
        let unique=(std::fs::metadata(&path).unwrap().len()/22) as usize;
        run_unique_sum+=unique as u64; runs.push(path);
        eprintln!("RUN records={} raw={} chunk_raw={} chunk_unique={} runs={} elapsed={:.1}",
                  records,raw_incidence,before,unique,runs.len(),start.elapsed().as_secs_f64());
    }
    if timed_out || records!=KEY_COUNT {
        println!("TIMEOUT records={} raw_incidence={} runs={} run_unique_sum={} elapsed={:.3}",
                 records,raw_incidence,runs.len(),run_unique_sum,start.elapsed().as_secs_f64());
        return;
    }
    eprintln!("MERGE_START records={} raw_incidence={} runs={} run_unique_sum={} elapsed={:.1}",
              records,raw_incidence,runs.len(),run_unique_sum,start.elapsed().as_secs_f64());
    let (nodes,arcs,root,keys)=merge_runs(&runs,Path::new(COLUMN_DAFSA));
    for path in &runs {remove_file(path).unwrap();} remove_dir(&temporary).unwrap();
    println!("RESULT records={} raw_incidence={} column_orbits={} nodes={} arcs={} root={} runs={} elapsed={:.3} complete={} actions={} word_maps={}",
             records,raw_incidence,keys,nodes,arcs,root,runs.len(),start.elapsed().as_secs_f64(),
             records==KEY_COUNT,actions.len(),maps.iter().map(|x|x.1.len()).sum::<usize>());
}
