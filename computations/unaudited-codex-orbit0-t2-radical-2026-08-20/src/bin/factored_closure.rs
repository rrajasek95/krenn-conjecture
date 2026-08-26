//! First-layer census for the sound factored subideal
//!   m_0^2 * < H_w : w opposite on every M0 pair >.
//! Rows have factored degree 16, columns are H_w times degree-12
//! non-anchor multipliers, and every one of the 105 H_w terms is grade 16.

use std::collections::{BTreeMap, HashSet};
use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};
use std::path::Path;
use std::time::Instant;

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Row16([u8; 16]);

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Column {
    word: u16,
    multiplier: [u8; 12],
}

#[derive(Clone, Copy)]
struct Action {
    sites: [u8; 8],
    colours: [u8; 3],
}

struct Seed {
    anchors: [bool; 252],
    actions: Vec<Action>,
    target: Vec<(Row16, i64)>,
}

struct Engine {
    anchors: [bool; 252],
    cell_u: [u8; 252],
    cell_v: [u8; 252],
    cell_a: [u8; 252],
    cell_b: [u8; 252],
    edge_id: [[u8; 8]; 8],
    cell_transforms: Vec<[u8; 252]>,
    word_transforms: Vec<Vec<u16>>,
    matchings: Vec<[(u8, u8); 4]>,
}

fn fail(message: impl AsRef<str>) -> ! {
    eprintln!("factored-closure: {}", message.as_ref());
    std::process::exit(2);
}

fn hex_nibble(byte: u8) -> u8 {
    match byte {
        b'0'..=b'9' => byte - b'0',
        b'a'..=b'f' => byte - b'a' + 10,
        b'A'..=b'F' => byte - b'A' + 10,
        _ => fail("bad hex digit"),
    }
}

fn parse_hex<const N: usize>(text: &str) -> [u8; N] {
    if text.len() != 2 * N { fail(format!("expected {} hex digits", 2 * N)); }
    let bytes = text.as_bytes();
    let mut answer = [0_u8; N];
    for index in 0..N {
        answer[index] = 16 * hex_nibble(bytes[2 * index]) + hex_nibble(bytes[2 * index + 1]);
    }
    answer
}

fn parse_seed(path: &Path) -> io::Result<Seed> {
    let mut anchors = [false; 252];
    let mut actions = Vec::new();
    let mut target = Vec::new();
    for (line_number, line_result) in BufReader::new(File::open(path)?).lines().enumerate() {
        let line = line_result?;
        let fields: Vec<_> = line.split_whitespace().collect();
        if fields.is_empty() { continue; }
        match fields[0] {
            "KRENN_FACTORED_P0_SQUARE_SEED_V1" => {
                if line_number != 0 { fail("seed magic is not first"); }
            }
            "ANCHORS" => for cell in parse_hex::<12>(fields[1]) { anchors[cell as usize] = true; },
            "DEGREE" => if fields[1] != "16" { fail("factored degree changed"); },
            "COMMON_FACTOR" => if fields[1] != "00007575c6c6f3f3" { fail("common factor changed"); },
            "ACTION" => {
                if fields[1].len() != 8 || fields[2].len() != 3 { fail("bad action"); }
                let mut sites = [0; 8];
                let mut colours = [0; 3];
                for (index, byte) in fields[1].bytes().enumerate() { sites[index] = byte - b'0'; }
                for (index, byte) in fields[2].bytes().enumerate() { colours[index] = byte - b'0'; }
                actions.push(Action { sites, colours });
            }
            "TARGET" => {
                let row = Row16(parse_hex::<16>(fields[1]));
                let numerator = fields[2].parse::<i64>().unwrap_or_else(|_| fail("bad target coefficient"));
                let denominator = fields[3].parse::<i64>().unwrap_or_else(|_| fail("bad target denominator"));
                if denominator != 1 { fail("factored target unexpectedly nonintegral"); }
                target.push((row, numerator));
            }
            _ => fail(format!("unknown seed record {}", fields[0])),
        }
    }
    if actions.len() != 768 || target.len() != 1_578_292 { fail("seed count changed"); }
    Ok(Seed { anchors, actions, target })
}

fn decode_word(mut code: u16) -> [u8; 8] {
    let mut word = [0; 8];
    for index in (0..8).rev() { word[index] = (code % 3) as u8; code /= 3; }
    word
}

fn encode_word(word: &[u8; 8]) -> u16 {
    word.iter().fold(0_u16, |code, digit| 3 * code + *digit as u16)
}

fn generate_matchings() -> Vec<[(u8, u8); 4]> {
    fn recurse(vertices: &[u8], pairs: &mut Vec<(u8, u8)>, out: &mut Vec<[(u8, u8); 4]>) {
        if vertices.is_empty() {
            out.push([pairs[0], pairs[1], pairs[2], pairs[3]]);
            return;
        }
        let u = vertices[0];
        for index in 1..vertices.len() {
            let v = vertices[index];
            let mut rest = Vec::with_capacity(vertices.len() - 2);
            rest.extend_from_slice(&vertices[1..index]);
            rest.extend_from_slice(&vertices[index + 1..]);
            pairs.push((u, v)); recurse(&rest, pairs, out); pairs.pop();
        }
    }
    let mut answer = Vec::new();
    recurse(&[0,1,2,3,4,5,6,7], &mut Vec::new(), &mut answer);
    if answer.len() != 105 { fail("matching count changed"); }
    answer
}

impl Engine {
    fn new(seed: &Seed) -> Self {
        let mut cell_u = [0; 252];
        let mut cell_v = [0; 252];
        let mut cell_a = [0; 252];
        let mut cell_b = [0; 252];
        let mut edge_id = [[0; 8]; 8];
        let mut edge = 0_u8;
        for u in 0..8_u8 {
            for v in u+1..8_u8 {
                edge_id[u as usize][v as usize] = edge;
                edge_id[v as usize][u as usize] = edge;
                for a in 0..3_u8 { for b in 0..3_u8 {
                    let id = edge as usize * 9 + a as usize * 3 + b as usize;
                    cell_u[id]=u; cell_v[id]=v; cell_a[id]=a; cell_b[id]=b;
                }}
                edge += 1;
            }
        }
        let cell_id = |u:u8,v:u8,a:u8,b:u8| -> u8 {
            (edge_id[u as usize][v as usize] as usize * 9 + a as usize*3 + b as usize) as u8
        };
        let mut cell_transforms = Vec::new();
        let mut word_transforms = Vec::new();
        for action in &seed.actions {
            let mut transform=[0_u8;252];
            for id in 0..252 {
                let (mut u,mut v)=(action.sites[cell_u[id] as usize],action.sites[cell_v[id] as usize]);
                let (mut a,mut b)=(action.colours[cell_a[id] as usize],action.colours[cell_b[id] as usize]);
                if u>v { std::mem::swap(&mut u,&mut v); std::mem::swap(&mut a,&mut b); }
                transform[id]=cell_id(u,v,a,b);
            }
            cell_transforms.push(transform);
            let mut words=vec![0_u16;6561];
            for code in 0..6561_u16 {
                let word=decode_word(code); let mut image=[0_u8;8];
                for site in 0..8 { image[action.sites[site] as usize]=action.colours[word[site] as usize]; }
                words[code as usize]=encode_word(&image);
            }
            word_transforms.push(words);
        }
        Self { anchors:seed.anchors,cell_u,cell_v,cell_a,cell_b,edge_id,
               cell_transforms,word_transforms,matchings:generate_matchings() }
    }

    fn cell_id(&self,u:u8,v:u8,a:u8,b:u8)->u8 {
        (self.edge_id[u as usize][v as usize] as usize*9+a as usize*3+b as usize) as u8
    }

    fn word_is_grade4(word:&[u8;8])->bool {
        word[0]!=word[1] && word[2]!=word[3] && word[4]!=word[5] && word[6]!=word[7]
    }

    fn canonical_row(&self,row:Row16)->Row16 {
        let mut best=None;
        for transform in &self.cell_transforms {
            let mut image=row.0.map(|cell|transform[cell as usize]); image.sort_unstable();
            let candidate=Row16(image);
            if best.map_or(true,|current|candidate<current){best=Some(candidate);}
        }
        best.unwrap()
    }

    fn canonical_column(&self,column:Column)->Column {
        let mut minimum_word=u16::MAX;
        for words in &self.word_transforms { minimum_word=minimum_word.min(words[column.word as usize]); }
        let mut best=None;
        for (action,words) in self.word_transforms.iter().enumerate() {
            if words[column.word as usize]!=minimum_word {continue;}
            let mut multiplier=column.multiplier.map(|cell|self.cell_transforms[action][cell as usize]);
            multiplier.sort_unstable();
            let candidate=Column{word:minimum_word,multiplier};
            if best.map_or(true,|current|candidate<current){best=Some(candidate);}
        }
        best.unwrap()
    }

    fn multiplier_after_removal(&self,row:Row16,selected:&[u8;4])->[u8;12] {
        let mut counts=[0_u8;252];
        for &cell in selected { counts[cell as usize]+=1; }
        let mut answer=[0_u8;12]; let mut next=0;
        for &cell in &row.0 {
            if counts[cell as usize]>0 { counts[cell as usize]-=1; }
            else { answer[next]=cell; next+=1; }
        }
        if next!=12 || counts.iter().any(|&value|value!=0){fail("term does not divide row");}
        answer
    }

    fn incident_columns(&self,row:Row16)->HashSet<Column> {
        let mut by_edge:Vec<Vec<u8>>=(0..28).map(|_|Vec::new()).collect();
        for &cell in &row.0 {
            let edge=self.edge_id[self.cell_u[cell as usize] as usize][self.cell_v[cell as usize] as usize] as usize;
            if !by_edge[edge].contains(&cell){by_edge[edge].push(cell);}
        }
        let mut answer=HashSet::new();
        for matching in &self.matchings {
            let lists:[&[u8];4]=matching.map(|(u,v)|{
                let edge=self.edge_id[u as usize][v as usize] as usize;
                by_edge[edge].as_slice()
            });
            if lists.iter().any(|list|list.is_empty()){continue;}
            for &c0 in lists[0] {for &c1 in lists[1] {for &c2 in lists[2] {for &c3 in lists[3] {
                let selected=[c0,c1,c2,c3]; let mut word=[255_u8;8];
                for &cell in &selected {
                    let id=cell as usize;
                    word[self.cell_u[id] as usize]=self.cell_a[id];
                    word[self.cell_v[id] as usize]=self.cell_b[id];
                }
                if !Self::word_is_grade4(&word){continue;}
                let raw=Column{word:encode_word(&word),multiplier:self.multiplier_after_removal(row,&selected)};
                if raw.multiplier.iter().any(|cell|self.anchors[*cell as usize]){fail("factored multiplier gained anchor");}
                answer.insert(self.canonical_column(raw));
            }}}}
        }
        answer
    }

    fn leading_outputs(&self,column:Column)->Vec<Row16> {
        let word=decode_word(column.word);
        if !Self::word_is_grade4(&word){fail("column word left grade four");}
        let mut answer=Vec::with_capacity(105);
        for matching in &self.matchings {
            let mut row=[0_u8;16]; row[..12].copy_from_slice(&column.multiplier);
            for (index,&(u,v)) in matching.iter().enumerate(){
                row[12+index]=self.cell_id(u,v,word[u as usize],word[v as usize]);
            }
            row.sort_unstable();
            if row.iter().any(|cell|self.anchors[*cell as usize]){fail("grade-four word emitted anchor");}
            answer.push(self.canonical_row(Row16(row)));
        }
        answer
    }
}

#[derive(Default)]
struct Piece {
    columns: HashSet<Column>,
    incidence: usize,
    row_histogram: BTreeMap<usize,usize>,
    zero_incidence_witness: Option<(Row16,i64)>,
}

fn target_incidence(engine:&Engine,target:&[(Row16,i64)],workers:usize)->Piece {
    let chunk=target.len().div_ceil(workers);
    let mut pieces=Vec::new();
    std::thread::scope(|scope|{
        let mut handles=Vec::new();
        for worker in 0..workers {
            let start=worker*chunk; let end=((worker+1)*chunk).min(target.len());
            if start>=end{continue;}
            handles.push(scope.spawn(move||{
                let begun=Instant::now(); let mut piece=Piece::default();
                for &(row,_coefficient) in &target[start..end] {
                    let columns=engine.incident_columns(row);
                    if columns.is_empty()
                        && piece.zero_incidence_witness.map_or(true, |(old,_)| row < old)
                    { piece.zero_incidence_witness=Some((row,_coefficient)); }
                    piece.incidence+=columns.len();
                    *piece.row_histogram.entry(columns.len()).or_default()+=1;
                    piece.columns.extend(columns);
                }
                eprintln!("worker={start}..{end} incidence={} columns={} elapsed={:.3}s",
                          piece.incidence,piece.columns.len(),begun.elapsed().as_secs_f64());
                piece
            }));
        }
        for handle in handles {pieces.push(handle.join().unwrap_or_else(|_|fail("incidence worker panicked")));}
    });
    let mut answer=Piece::default();
    for piece in pieces {
        answer.incidence+=piece.incidence;
        for (degree,count) in piece.row_histogram {*answer.row_histogram.entry(degree).or_default()+=count;}
        if let Some(witness)=piece.zero_incidence_witness {
            if answer.zero_incidence_witness.map_or(true,|(old,_)|witness.0<old){
                answer.zero_incidence_witness=Some(witness);
            }
        }
        answer.columns.extend(piece.columns);
    }
    answer
}

fn write_results(path:&Path,seed:&Seed,piece:&Piece,elapsed:f64)->io::Result<()> {
    let mut out=File::create(path)?;
    write!(out,"{{\n  \"status\":\"UNAUDITED exact factored-subideal target incidence census\",\n  \"scope\":\"Positive membership in this m0^2-factored subideal is sound; negative membership is not an obstruction for the complete gr16 image.\",\n  \"stabilizer_order\":{},\n  \"target_row_orbits\":{},\n  \"target_incidence\":{},\n  \"distinct_incident_columns\":{},\n  \"row_incident_column_histogram\":{{",seed.actions.len(),seed.target.len(),piece.incidence,piece.columns.len())?;
    for (number,(degree,count)) in piece.row_histogram.iter().enumerate(){if number!=0{write!(out,",")?;}write!(out,"\"{degree}\":{count}")?;}
    let (witness,coefficient)=piece.zero_incidence_witness.unwrap_or_else(||fail("missing zero-incidence witness"));
    write!(out,"}},\n  \"zero_incidence_witness\":{{\"row\":\"")?;
    const HEX:&[u8;16]=b"0123456789abcdef";
    for byte in witness.0 {write!(out,"{}{}",HEX[(byte>>4) as usize] as char,HEX[(byte&15) as usize] as char)?;}
    write!(out,"\",\"target_coefficient\":{coefficient},\"literal_incident_columns\":0}},\n  \"restricted_nonmembership\":\"The displayed nonzero target coordinate is absent from every H_w times degree-12 nonanchor multiplier column with w opposite on all four M0 pairs.\",\n  \"elapsed_seconds\":{elapsed:.6}\n}}\n")?;
    Ok(())
}

fn main(){
    let args:Vec<_>=env::args().collect();
    if args.len()!=3{eprintln!("usage: factored_closure SEED.txt RESULTS.json");std::process::exit(2);}
    let begun=Instant::now();
    let seed=parse_seed(Path::new(&args[1])).unwrap_or_else(|error|fail(error.to_string()));
    let engine=Engine::new(&seed);
    for &(row,_coefficient) in seed.target.iter().take(256){
        if engine.canonical_row(row)!=row{fail("factored target row is not subgroup-canonical");}
    }
    let workers=std::thread::available_parallelism().map_or(4,|value|value.get()).min(8);
    let piece=target_incidence(&engine,&seed.target,workers);
    write_results(Path::new(&args[2]),&seed,&piece,begun.elapsed().as_secs_f64())
        .unwrap_or_else(|error|fail(error.to_string()));
    eprintln!("PASS target={} incidence={} columns={} elapsed={:.3}s",
              seed.target.len(),piece.incidence,piece.columns.len(),begun.elapsed().as_secs_f64());
}
