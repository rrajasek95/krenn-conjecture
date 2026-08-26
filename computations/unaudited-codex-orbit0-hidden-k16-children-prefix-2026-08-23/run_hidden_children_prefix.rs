// One-H-slice measured prefix for the recovered hidden K16 children.
include!("../unaudited-codex-orbit0-filtered-k16-run-2026-08-23/run_filtered_k17.rs");
use std::fs::rename;
use std::io::{BufReader, Read, Seek, SeekFrom};

const HDIR: &str = "computations/unaudited-codex-orbit0-k14-hidden-k16-parent-full-2026-08-23/";
const ODIR: &str = "computations/unaudited-codex-orbit0-hidden-k16-children-prefix-2026-08-23/";
const K4FILE: &str =
    "computations/unaudited-codex-orbit0-filtered-k18-charge-2026-08-23/filtered_k18_k4.bin";
const CYCLEFILE: &str =
    "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/filtered_k17_cycle_aux.bin";
const U: i128 = 400_591_699_200;
const PARENTS: u64 = 156_064;

#[derive(Clone, Copy, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct PKey {
    profile: [u8; 29],
    sig: [u8; 12],
    pivot: u8,
}
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct CKey([u8; 13]);
#[derive(Clone, Copy)]
struct Agg {
    weight: i128,
    uses: u64,
    witness: u64,
    witness_row: Row,
}
#[derive(Clone, Copy, Default)]
struct Resp {
    full_n: u64,
    irr_n: u64,
    full_q: i64,
    irr_q: i64,
}
#[derive(Clone, Copy)]
struct Witness {
    parent: u64,
    pivot: u8,
    tail: u8,
    m2: u8,
    raw_child: Row,
}
#[derive(Clone, Copy)]
struct Val {
    weight: i128,
    pivotable: bool,
    witness: Witness,
}
struct CEnv {
    cells: [[u8; 4]; 252],
    dual: HashMap<CKey, i64>,
    k4: Vec<Vec<[u8; 4]>>,
}
fn cenv() -> CEnv {
    let b = read(CYCLEFILE).unwrap();
    assert_eq!(&b[..8], b"K17CYC1\0");
    let mut p = 8;
    let mut cells = [[0; 4]; 252];
    for c in &mut cells {
        c.copy_from_slice(&b[p..p + 4]);
        p += 4
    }
    let n = u32le(&b[p..p + 4]) as usize;
    p += 4;
    let mut dual = HashMap::new();
    for _ in 0..n {
        let mut k = [0; 13];
        k.copy_from_slice(&b[p..p + 13]);
        p += 13;
        let v = i64le(&b[p..p + 8]);
        p += 8;
        dual.insert(CKey(k), v);
    }
    assert_eq!(p, b.len());
    let z = read(K4FILE).unwrap();
    assert_eq!(&z[..7], b"K18K4A1");
    let mut q = 7;
    let mut k4 = vec![Vec::new(); 78];
    for row in &mut k4 {
        for _ in 0..60 {
            let mut t = [0; 4];
            t.copy_from_slice(&z[q..q + 4]);
            q += 4;
            row.push(t)
        }
    }
    assert_eq!(q, z.len());
    CEnv { cells, dual, k4 }
}
fn remove4(row: &Row, a: &[u8; 4]) -> [u8; 20] {
    let mut x = [0; 20];
    let (mut j, mut k) = (0, 0);
    for &c in &row.0 {
        if j < 4 && c == a[j] {
            j += 1
        } else {
            x[k] = c;
            k += 1
        }
    }
    assert_eq!((j, k), (4, 20));
    x
}
fn path_profile(row: &Row, p: usize, e: &Engine, c: &CEnv) -> [u8; 29] {
    let m = remove4(row, &e.anchors[p]);
    let mut edges = [(0u8, 0u8); 20];
    let mut adj = [[255u8; 2]; 24];
    let mut deg = [0usize; 24];
    for (i, &cell) in m.iter().enumerate() {
        let [u, v, a, b] = c.cells[cell as usize];
        let x = 3 * u + a;
        let y = 3 * v + b;
        edges[i] = (x, y);
        adj[x as usize][deg[x as usize]] = i as u8;
        deg[x as usize] += 1;
        adj[y as usize][deg[y as usize]] = i as u8;
        deg[y as usize] += 1
    }
    let mut eid = [-1i8; 24];
    for (i, &cell) in e.anchors[p].iter().enumerate() {
        let [u, v, a, b] = c.cells[cell as usize];
        eid[(3 * u + a) as usize] = (2 * i) as i8;
        eid[(3 * v + b) as usize] = (2 * i + 1) as i8
    }
    let mut partner = [255; 8];
    let mut lens = [0; 8];
    let mut used = [false; 20];
    for s in 0..8 {
        if partner[s] != 255 {
            continue;
        }
        let mut v = eid.iter().position(|&x| x == s as i8).unwrap();
        let mut prev = 255;
        let mut len = 0;
        loop {
            let edge = *adj[v].iter().find(|&&x| x != 255 && x != prev).unwrap();
            used[edge as usize] = true;
            let (a, b) = edges[edge as usize];
            v = if a as usize == v {
                b as usize
            } else {
                a as usize
            };
            prev = edge;
            len += 1;
            if eid[v] >= 0 {
                let t = eid[v] as usize;
                partner[s] = t as u8;
                partner[t] = s as u8;
                lens[s] = len;
                lens[t] = len;
                break;
            }
        }
    }
    let mut closed = [0; 12];
    let mut nc = 0;
    for seed in 0..20 {
        if used[seed] {
            continue;
        }
        let mut edge = seed as u8;
        let mut v = edges[seed].0 as usize;
        let start = v;
        let mut len = 0;
        loop {
            used[edge as usize] = true;
            let (a, b) = edges[edge as usize];
            v = if a as usize == v {
                b as usize
            } else {
                a as usize
            };
            len += 1;
            if v == start {
                break;
            }
            edge = *adj[v].iter().find(|&&x| x != edge).unwrap()
        }
        closed[nc] = len;
        nc += 1
    }
    closed[..nc].sort_unstable();
    let mut out = [0; 29];
    out[..8].copy_from_slice(&partner);
    out[8..16].copy_from_slice(&lens);
    out[16] = nc as u8;
    out[17..17 + nc].copy_from_slice(&closed[..nc]);
    out
}
fn literal_ckey(row: &Row, c: &CEnv) -> CKey {
    let mut adj = [[0u8; 2]; 24];
    let mut deg = [0usize; 24];
    for &cell in &row.0 {
        let [u, v, a, b] = c.cells[cell as usize];
        let x = (3 * u + a) as usize;
        let y = (3 * v + b) as usize;
        adj[x][deg[x]] = y as u8;
        deg[x] += 1;
        adj[y][deg[y]] = x as u8;
        deg[y] += 1
    }
    assert!(deg.iter().all(|&d| d == 2));
    let mut seen = [false; 24];
    let mut parts = [0; 12];
    let mut n = 0;
    for st in 0..24 {
        if seen[st] {
            continue;
        }
        let mut stack = [0u8; 24];
        let (mut top, mut size) = (1, 0);
        stack[0] = st as u8;
        seen[st] = true;
        while top > 0 {
            top -= 1;
            let x = stack[top] as usize;
            size += 1;
            for &yy in &adj[x] {
                let y = yy as usize;
                if !seen[y] {
                    seen[y] = true;
                    stack[top] = yy;
                    top += 1
                }
            }
        }
        parts[n] = size;
        n += 1
    }
    parts[..n].sort_unstable();
    let mut k = [0; 13];
    k[0] = n as u8;
    k[1..1 + n].copy_from_slice(&parts[..n]);
    CKey(k)
}
fn abstract_ckey(prof: &[u8; 29], p: usize, t: &[u8; 4], e: &Engine, c: &CEnv) -> CKey {
    let mut eid = [-1i8; 24];
    for (i, &cell) in e.anchors[p].iter().enumerate() {
        let [u, v, a, b] = c.cells[cell as usize];
        eid[(3 * u + a) as usize] = (2 * i) as i8;
        eid[(3 * v + b) as usize] = (2 * i + 1) as i8
    }
    let mut tp = [255; 8];
    for &cell in t {
        let [u, v, a, b] = c.cells[cell as usize];
        let x = eid[(3 * u + a) as usize];
        let y = eid[(3 * v + b) as usize];
        assert!(x >= 0 && y >= 0);
        tp[x as usize] = y as u8;
        tp[y as usize] = x as u8
    }
    assert!(tp.iter().all(|&x| x != 255));
    let mut seen = [false; 8];
    let mut parts = [0u8; 12];
    let mut n = 0;
    for st in 0..8 {
        if seen[st] {
            continue;
        }
        let mut stack = [0u8; 8];
        let (mut top, mut nodes, mut pathsum) = (1, 0u8, 0u16);
        stack[0] = st as u8;
        seen[st] = true;
        while top > 0 {
            top -= 1;
            let x = stack[top] as usize;
            nodes += 1;
            pathsum += prof[8 + x] as u16;
            for y in [prof[x], tp[x]] {
                let yy = y as usize;
                if !seen[yy] {
                    seen[yy] = true;
                    stack[top] = y;
                    top += 1
                }
            }
        }
        parts[n] = (pathsum / 2 + (nodes as u16) / 2) as u8;
        n += 1
    }
    let nc = prof[16] as usize;
    for &x in &prof[17..17 + nc] {
        parts[n] = x;
        n += 1
    }
    parts[..n].sort_unstable();
    let mut k = [0; 13];
    k[0] = n as u8;
    k[1..1 + n].copy_from_slice(&parts[..n]);
    CKey(k)
}
fn response(row: &Row, key: PKey, degree: usize, e: &Engine, c: &CEnv) -> Resp {
    let tails: &[[u8; 4]] = match degree {
        3 => &e.all_k3[key.pivot as usize],
        4 => &c.k4[key.pivot as usize],
        _ => unreachable!(),
    };
    let mut z = Resp::default();
    for t in tails {
        let child = replace_anchor(row, &e.anchors[key.pivot as usize], t);
        let ak = abstract_ckey(&key.profile, key.pivot as usize, t, e, c);
        let lk = literal_ckey(&child, c);
        assert_eq!(ak, lk);
        let q = *c.dual.get(&ak).unwrap_or(&0);
        z.full_n += 1;
        z.full_q += q;
        if available(signature(&child.0, e), e).is_empty() {
            z.irr_n += 1;
            z.irr_q += q
        }
    }
    z
}
fn add_literal(map: &mut HashMap<Row, Val>, row: Row, w: i128, pivotable: bool, wi: Witness) {
    use std::collections::hash_map::Entry;
    match map.entry(row) {
        Entry::Vacant(e) => {
            e.insert(Val {
                weight: w,
                pivotable,
                witness: wi,
            });
        }
        Entry::Occupied(mut e) => {
            assert_eq!(e.get().pivotable, pivotable);
            let x = e.get_mut();
            x.weight += w;
            if x.weight == 0 {
                e.remove();
            }
        }
    }
}
#[cfg(not(feature = "full_hidden_charge"))]
fn main() {
    std::fs::create_dir_all(ODIR).unwrap();
    let begun = Instant::now();
    let e = parse();
    let c = cenv();
    let mut r = BufReader::with_capacity(
        1 << 20,
        File::open(format!("{}parents_000_016.bin", HDIR)).unwrap(),
    );
    let mut h = [0; 40];
    r.read_exact(&mut h).unwrap();
    assert_eq!(&h[..8], b"H16RUN2\0");
    assert_eq!(i128::from_le_bytes(h[8..24].try_into().unwrap()), U);
    assert!(PARENTS <= u64::from_le_bytes(h[32..40].try_into().unwrap()));
    let mut profiles: HashMap<PKey, Agg> = HashMap::new();
    let mut literal: HashMap<Row, Val> = HashMap::new();
    let (mut outgoing, mut k2raw, mut k2irr, mut incoming_sum) = (0u64, 0u64, 0u64, 0i128);
    for parent in 0..PARENTS {
        let mut rec = [0; 64];
        r.read_exact(&mut rec).unwrap();
        let mut rr = [0; 24];
        rr.copy_from_slice(&rec[..24]);
        let row = Row(rr);
        let w1 = i128::from_le_bytes(rec[24..40].try_into().unwrap());
        let mut s = [0; 12];
        s.copy_from_slice(&rec[40..52]);
        assert_eq!(signature(&row.0, &e), s);
        let m2 = rec[60] as usize;
        let ps = available(s, &e);
        assert_eq!(ps.len(), m2);
        assert_eq!(w1 % (m2 as i128), 0);
        let w2 = -w1 / (m2 as i128);
        for p in ps {
            outgoing += 1;
            incoming_sum += w2;
            let key = PKey {
                profile: path_profile(&row, p, &e, &c),
                sig: s,
                pivot: p as u8,
            };
            profiles
                .entry(key)
                .and_modify(|x| {
                    x.weight += w2;
                    x.uses += 1
                })
                .or_insert(Agg {
                    weight: w2,
                    uses: 1,
                    witness: parent,
                    witness_row: row,
                });
            for (ti, t) in e.all_k2[p].iter().enumerate() {
                k2raw += 1;
                let child = replace_anchor(&row, &e.anchors[p], t);
                let pivotable = pivotable(&child, &e);
                if !pivotable {
                    k2irr += 1
                }
                add_literal(
                    &mut literal,
                    child,
                    w2,
                    pivotable,
                    Witness {
                        parent,
                        pivot: p as u8,
                        tail: ti as u8,
                        m2: m2 as u8,
                        raw_child: child,
                    },
                )
            }
        }
    }
    let collected = Instant::now();
    let literal_nonzero = literal.len();
    let mut ccache = HashMap::new();
    let mut canonical_map: HashMap<Row, Val> = HashMap::new();
    let mut canonical_seen = HashSet::new();
    for (row, v) in literal {
        let q = canonical(row, &e, &mut ccache);
        canonical_seen.insert(q);
        add_literal(&mut canonical_map, q, v.weight, v.pivotable, v.witness)
    }
    let canonical_zero = canonical_seen.len() - canonical_map.len();
    let canonical_time = collected.elapsed().as_secs_f64();
    let mut pv: Vec<_> = canonical_map.into_iter().collect();
    pv.sort_unstable_by_key(|x| x.0);
    let support = pv.len();
    let pivot_support = pv.iter().filter(|x| x.1.pivotable).count();
    let irr_support = support - pivot_support;
    let weight_sum: i128 = pv.iter().map(|x| x.1.weight).sum();
    assert_eq!(weight_sum, 12 * incoming_sum);
    let path = format!("{}k18_k2_canonical_prefix.bin", ODIR);
    let tmp = format!("{}.tmp", path);
    let mut w = BufWriter::new(File::create(&tmp).unwrap());
    w.write_all(b"H18K2P1\0").unwrap();
    w.write_all(&U.to_le_bytes()).unwrap();
    w.write_all(&0u64.to_le_bytes()).unwrap();
    w.write_all(&PARENTS.to_le_bytes()).unwrap();
    w.write_all(&k2raw.to_le_bytes()).unwrap();
    w.write_all(&(support as u64).to_le_bytes()).unwrap();
    w.write_all(&76u16.to_le_bytes()).unwrap();
    w.write_all(&[0; 6]).unwrap();
    for (row, v) in &pv {
        w.write_all(&row.0).unwrap();
        w.write_all(&v.weight.to_le_bytes()).unwrap();
        w.write_all(&[v.pivotable as u8]).unwrap();
        w.write_all(&v.witness.parent.to_le_bytes()).unwrap();
        w.write_all(&[v.witness.pivot, v.witness.tail, v.witness.m2])
            .unwrap();
        w.write_all(&v.witness.raw_child.0).unwrap()
    }
    w.flush().unwrap();
    drop(w);
    rename(tmp, &path).unwrap();
    assert_eq!(
        std::fs::metadata(&path).unwrap().len(),
        64 + 76 * support as u64
    );
    let charge_start = Instant::now();
    let mut pkeys: Vec<_> = profiles.into_iter().collect();
    pkeys.sort_unstable_by_key(|x| x.0);
    assert_eq!(pkeys.iter().map(|x| x.1.weight).sum::<i128>(), incoming_sum);
    let profile_path = format!("{}hidden_child_profiles_prefix.bin", ODIR);
    let profile_tmp = format!("{}.tmp", profile_path);
    let mut profile_writer = BufWriter::new(File::create(&profile_tmp).unwrap());
    profile_writer.write_all(b"HCPROF1\0").unwrap();
    profile_writer.write_all(&U.to_le_bytes()).unwrap();
    profile_writer.write_all(&0u16.to_le_bytes()).unwrap();
    profile_writer.write_all(&[0; 6]).unwrap();
    profile_writer
        .write_all(&(pkeys.len() as u64).to_le_bytes())
        .unwrap();
    profile_writer.write_all(&90u16.to_le_bytes()).unwrap();
    profile_writer.write_all(&[0; 22]).unwrap();
    for (key, a) in &pkeys {
        profile_writer.write_all(&key.profile).unwrap();
        profile_writer.write_all(&key.sig).unwrap();
        profile_writer.write_all(&[key.pivot]).unwrap();
        profile_writer.write_all(&a.weight.to_le_bytes()).unwrap();
        profile_writer.write_all(&a.uses.to_le_bytes()).unwrap();
        profile_writer.write_all(&a.witness_row.0).unwrap();
    }
    profile_writer.flush().unwrap();
    drop(profile_writer);
    rename(profile_tmp, &profile_path).unwrap();
    assert_eq!(
        std::fs::metadata(&profile_path).unwrap().len(),
        64 + 90 * pkeys.len() as u64
    );
    let (mut k3n, mut k3i, mut k4n, mut k4i) = (0u64, 0u64, 0u64, 0u64);
    let (mut k3q, mut k3iq, mut k4q, mut k4iq) = (0i128, 0i128, 0i128, 0i128);
    for (key, a) in &pkeys {
        let row = a.witness_row;
        assert_eq!(path_profile(&row, key.pivot as usize, &e, &c), key.profile);
        for d in [3usize, 4] {
            let z = response(&row, *key, d, &e, &c);
            let full = a.uses * z.full_n;
            let irr = a.uses * z.irr_n;
            let fq = a.weight * (z.full_q as i128);
            let iq = a.weight * (z.irr_q as i128);
            if d == 3 {
                k3n += full;
                k3i += irr;
                k3q += fq;
                k3iq += iq
            } else {
                k4n += full;
                k4i += irr;
                k4q += fq;
                k4iq += iq
            }
        }
    }
    let charge_time = charge_start.elapsed().as_secs_f64();
    let elapsed = begun.elapsed().as_secs_f64();
    let full_factor = 485f64;
    let profile_factor = 6_229_700f64 / (pkeys.len() as f64);
    let text=format!("{{\n\"status\":\"PASS_MEASURED_CHILD_PREFIX\",\"H_slice\":0,\"parent_occurrences\":{},\"outgoing_profile_uses\":{},\"unique_profile_keys\":{},\"profile_weight_sum_scaled\":\"{}\",\"K18_22\":{{\"raw_children\":{},\"raw_irreducible\":{},\"literal_nonzero_before_H\":{},\"canonical_seen\":{},\"canonical_exact_zero\":{},\"canonical_nonzero\":{},\"canonical_pivotable_support\":{},\"canonical_irreducible_support\":{},\"canonical_weight_sum_scaled\":\"{}\",\"checkpoint_bytes\":{}}},\"K19_23_charge\":{{\"full_occurrences\":{},\"irreducible_occurrences\":{},\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\"}},\"K20_24_charge\":{{\"full_occurrences\":{},\"irreducible_occurrences\":{},\"full_charge_scaled\":\"{}\",\"irreducible_charge_scaled\":\"{}\"}},\"abstract_literal_cycle_guards\":{},\"shared_provider_sound\":true,\"timing_seconds\":{{\"collect_through_literal_K2\":{:.6},\"canonicalize_K2\":{:.6},\"profile_charge_both_degrees\":{:.6},\"total\":{:.6}}},\"full_estimates\":{{\"parent_pass_factor\":485,\"linear_parent_pass_wall_seconds\":{:.3},\"linear_K2_checkpoint_bytes_upper\":{},\"merged_profile_factor\":{:.9},\"K3_K4_charge_wall_seconds_from_merged_profiles\":{:.3}}}\n}}\n",PARENTS,outgoing,pkeys.len(),incoming_sum,k2raw,k2irr,literal_nonzero,canonical_seen.len(),canonical_zero,support,pivot_support,irr_support,weight_sum,64+76*support as u64,k3n,k3i,k3q,k3iq,k4n,k4i,k4q,k4iq,pkeys.len()*(32+60),collected.duration_since(begun).as_secs_f64(),canonical_time,charge_time,elapsed,elapsed*full_factor,(64+76*support as u64)*485,profile_factor,charge_time*profile_factor);
    let jt = format!("{}results_hidden_children_prefix.json.tmp", ODIR);
    let jf = format!("{}results_hidden_children_prefix.json", ODIR);
    std::fs::write(&jt, &text).unwrap();
    rename(jt, jf).unwrap();
    print!("{}", text)
}
