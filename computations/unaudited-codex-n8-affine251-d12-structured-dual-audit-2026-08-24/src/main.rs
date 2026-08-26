#[allow(dead_code)]
mod retained {
    include!(concat!(env!("OUT_DIR"), "/retained_main.rs"));

    use std::collections::{BTreeMap as LocalBTreeMap, BTreeSet as LocalBTreeSet};
    use std::env as local_env;

    const AUDIT_PRIME: u64 = 1_073_741_827;

    #[derive(Clone)]
    struct TemplateAudit {
        name: &'static str,
        support: usize,
        incident: usize,
        cached_incident: usize,
        missing_incident: usize,
        cached_bad: usize,
        global_bad: usize,
        first_bad: Option<(Column, i128)>,
    }

    #[derive(Clone)]
    struct AnsatzAudit {
        name: &'static str,
        groups: usize,
        cached_consistent: bool,
        cached_rank: usize,
        global_consistent: bool,
        global_rank: usize,
        candidate_constant_on_groups: bool,
    }

    fn weight_numerator(value: u64) -> i128 {
        match value {
            1 => 2,
            2 => 4,
            x if x == AUDIT_PRIME - 1 => -2,
            x if x == AUDIT_PRIME - 2 => -4,
            x if x == (AUDIT_PRIME + 1) / 2 => 1,
            x if x == (AUDIT_PRIME - 1) / 2 => -1,
            _ => fail(format!("candidate coefficient {value} is outside half-integral template")),
        }
    }

    fn signed(value: u64) -> i128 {
        if value <= AUDIT_PRIME / 2 { value as i128 } else { value as i128 - AUDIT_PRIME as i128 }
    }

    fn mod_i128(value: i128) -> u64 {
        let prime = AUDIT_PRIME as i128;
        (((value % prime) + prime) % prime) as u64
    }

    fn t_exponent(row: Mono) -> usize {
        row.slice().iter().filter(|&&x| x == T_ID).count()
    }

    fn partition(mut values: Vec<usize>) -> String {
        values.sort_unstable_by(|a, b| b.cmp(a));
        values.into_iter().map(|x| x.to_string()).collect::<Vec<_>>().join(".")
    }

    fn multiplicity_partition(row: Mono) -> String {
        let mut counts = Vec::new();
        let mut last = None;
        for &id in row.slice().iter().filter(|&&x| x != T_ID) {
            if last == Some(id) { *counts.last_mut().unwrap() += 1; }
            else { counts.push(1usize); last = Some(id); }
        }
        partition(counts)
    }

    fn edge_endpoints() -> [(usize, usize); 28] {
        let mut answer = [(0usize, 0usize); 28];
        let mut index = 0;
        for left in 0..8 {
            for right in left + 1..8 {
                answer[index] = (left, right); index += 1;
            }
        }
        answer
    }

    fn coarse_orbit_signature(row: Mono) -> String {
        let endpoints = edge_endpoints();
        let mut degrees = [0usize; 8];
        let mut edge_counts = [0usize; 28];
        let mut colours = [0usize; 3];
        let mut pair_counts = [0usize; 6]; // 00,01,02,11,12,22, unordered
        for &affine in row.slice().iter().filter(|&&x| x != T_ID) {
            let original = if (affine as usize) < FIXED_ORIGINAL { affine as usize } else { affine as usize + 1 };
            let edge = original / 9;
            let a = (original % 9) / 3;
            let b = original % 3;
            let (left, right) = endpoints[edge];
            degrees[left] += 1; degrees[right] += 1; edge_counts[edge] += 1;
            colours[a] += 1; colours[b] += 1;
            let (x, y) = if a <= b { (a, b) } else { (b, a) };
            let pair = match (x, y) { (0,0)=>0, (0,1)=>1, (0,2)=>2, (1,1)=>3, (1,2)=>4, (2,2)=>5, _=>unreachable!() };
            pair_counts[pair] += 1;
        }
        let mut degrees = degrees.to_vec(); degrees.sort_unstable_by(|a,b| b.cmp(a));
        let edge_part = partition(edge_counts.into_iter().filter(|&x| x != 0).collect());
        let colour01 = [colours[0], colours[1]];
        let colour_pair = if colour01[0] <= colour01[1] { colour01 } else { [colour01[1], colour01[0]] };
        // Canonicalize pair counts under the global 0<->1 colour flip.
        let flipped = [pair_counts[3], pair_counts[1], pair_counts[4], pair_counts[0], pair_counts[2], pair_counts[5]];
        let pair_canonical = if flipped < pair_counts { flipped } else { pair_counts };
        format!("t{}|m{}|e{}|d{:?}|c{:?}:{}|p{:?}", t_exponent(row),
            multiplicity_partition(row), edge_part, degrees, colour_pair, colours[2], pair_canonical)
    }

    fn shifted_old_seven() -> LocalBTreeMap<Mono, u64> {
        let rows = [
            ("00096399a2abcfea", 1u64), ("000d6799a2afdce1", 1),
            ("00116b99a2b3e0e1", 2), ("0075cfeafbfbfbfb", 2),
            ("08116ba1aab3d7f2", (AUDIT_PRIME + 1) / 2),
            ("087dd7f2fbfbfbfb", 1), ("fbfbfbfbfbfbfbfb", 1),
        ];
        let mut answer = LocalBTreeMap::new();
        for (hex, value) in rows {
            let mut ids = hex.as_bytes().chunks_exact(2).map(|pair|
                u8::from_str_radix(std::str::from_utf8(pair).unwrap(), 16).unwrap()).collect::<Vec<_>>();
            ids.extend([T_ID; 4]);
            answer.insert(Mono::new(ids), value);
        }
        answer
    }

    fn incidents(provider: &Provider, support: &LocalBTreeMap<Mono, u64>, workers: usize) -> Vec<Column> {
        let rows: Vec<_> = support.keys().copied().collect();
        let mut set = LocalBTreeSet::new();
        for (_, columns) in sparse_parallel_incident_lists(provider, &rows, workers) {
            set.extend(columns);
        }
        set.into_iter().collect()
    }

    fn materialize(provider: &Provider, columns: &[Column], workers: usize) -> Vec<(Column, Vec<(Mono, u64)>)> {
        let mut answer = Vec::with_capacity(columns.len());
        for batch in columns.chunks(256) {
            let vectors = parallel_invariant_columns(provider, batch, AUDIT_PRIME, workers);
            answer.extend(batch.iter().copied().zip(vectors));
        }
        answer
    }

    fn audit_template(name: &'static str, support: &LocalBTreeMap<Mono, u64>,
                      cached: &HashSet<Column>, vectors: &[(Column, Vec<(Mono, u64)>)]) -> TemplateAudit {
        let inverse_two = (AUDIT_PRIME + 1) / 2;
        let mut cached_bad = 0usize;
        let mut global_bad = 0usize;
        let mut cached_incident = 0usize;
        let mut first_bad = None;
        for (column, vector) in vectors {
            let mut pairing = 0u64;
            let mut exact_numerator = 0i128;
            for &(row, coefficient) in vector {
                if let Some(&weight) = support.get(&row) {
                    pairing = ((pairing as u128 + coefficient as u128 * weight as u128) % AUDIT_PRIME as u128) as u64;
                    exact_numerator += signed(coefficient) * weight_numerator(weight);
                }
            }
            if pairing != mod_i128(exact_numerator) * inverse_two % AUDIT_PRIME {
                fail("modular/exact half-integral replay mismatch");
            }
            let is_cached = cached.contains(column);
            if is_cached { cached_incident += 1; }
            if pairing != 0 {
                global_bad += 1;
                if is_cached { cached_bad += 1; }
                if first_bad.is_none() { first_bad = Some((*column, exact_numerator)); }
            }
        }
        TemplateAudit { name, support: support.len(), incident: vectors.len(), cached_incident,
            missing_incident: vectors.len() - cached_incident, cached_bad, global_bad, first_bad }
    }

    fn group_rows(support: &LocalBTreeMap<Mono, u64>, mode: &str) -> (Vec<usize>, usize, bool) {
        let mut labels = LocalBTreeMap::<String, usize>::new();
        let mut groups = Vec::with_capacity(support.len());
        let mut group_value = HashMap::<usize, u64>::new();
        let mut constant = true;
        for (&row, &value) in support {
            let label = match mode {
                "t" => format!("t{}", t_exponent(row)),
                "t_partition" => format!("t{}|{}", t_exponent(row), multiplicity_partition(row)),
                "coarse_orbit" => coarse_orbit_signature(row),
                _ => unreachable!(),
            };
            let next = labels.len();
            let group = *labels.entry(label).or_insert(next);
            if group_value.insert(group, value).is_some_and(|old| old != value) { constant = false; }
            groups.push(group);
        }
        (groups, labels.len(), constant)
    }

    fn ansatz_consistency(support: &LocalBTreeMap<Mono, u64>, groups: &[usize], group_count: usize,
                          cached: &HashSet<Column>, vectors: &[(Column, Vec<(Mono, u64)>)], cached_only: bool)
        -> (bool, usize)
    {
        let rows: Vec<_> = support.keys().copied().collect();
        let row_group: HashMap<_, _> = rows.into_iter().zip(groups.iter().copied()).collect();
        let target = Mono::new(vec![T_ID; 12]);
        let target_group = row_group[&target];
        let mut basis = HashMap::<usize, (LocalBTreeMap<usize, u64>, u64)>::new();
        for (column, vector) in vectors {
            if cached_only && !cached.contains(column) { continue; }
            let mut equation = LocalBTreeMap::<usize, u64>::new();
            for &(row, coefficient) in vector {
                if let Some(&group) = row_group.get(&row) {
                    let old = equation.get(&group).copied().unwrap_or(0);
                    let value = old + coefficient;
                    let value = if value >= AUDIT_PRIME { value - AUDIT_PRIME } else { value };
                    if value == 0 { equation.remove(&group); } else { equation.insert(group, value); }
                }
            }
            let fixed = equation.remove(&target_group).unwrap_or(0);
            let mut rhs = if fixed == 0 { 0 } else { AUDIT_PRIME - fixed };
            let mut inserted = false;
            while let Some((&pivot, &value)) = equation.first_key_value() {
                if let Some((record, record_rhs)) = basis.get(&pivot) {
                    let factor = value;
                    for (&group, &coefficient) in record {
                        let old = equation.get(&group).copied().unwrap_or(0);
                        let subtract = (factor as u128 * coefficient as u128 % AUDIT_PRIME as u128) as u64;
                        let new = if old >= subtract { old - subtract } else { old + AUDIT_PRIME - subtract };
                        if new == 0 { equation.remove(&group); } else { equation.insert(group, new); }
                    }
                    let subtract = (factor as u128 * *record_rhs as u128 % AUDIT_PRIME as u128) as u64;
                    rhs = if rhs >= subtract { rhs - subtract } else { rhs + AUDIT_PRIME - subtract };
                } else {
                    let inverse = inverse_mod(value, AUDIT_PRIME);
                    for coefficient in equation.values_mut() {
                        *coefficient = (*coefficient as u128 * inverse as u128 % AUDIT_PRIME as u128) as u64;
                    }
                    rhs = (rhs as u128 * inverse as u128 % AUDIT_PRIME as u128) as u64;
                    basis.insert(pivot, (equation.clone(), rhs));
                    inserted = true;
                    break;
                }
            }
            if !inserted && equation.is_empty() && rhs != 0 { return (false, basis.len()); }
        }
        let _ = group_count;
        (true, basis.len())
    }

    fn column_text(column: Column) -> String {
        format!("{}:{}", column.word, mono_hex(column.multiplier))
    }

    pub fn audit_entry() {
        let args: Vec<_> = local_env::args().collect();
        if args.len() != 11 || args[1] != "--input" || args[3] != "--checkpoint"
            || args[5] != "--previous-checkpoint" || args[7] != "--output"
            || args[9] != "--workers" { fail("bad arguments"); }
        let input = PathBuf::from(&args[2]);
        let checkpoint = PathBuf::from(&args[4]);
        let previous_checkpoint = PathBuf::from(&args[6]);
        let output = PathBuf::from(&args[8]);
        let workers: usize = args[10].parse().unwrap_or_else(|_| fail("bad workers"));
        if workers == 0 || workers > 8 { fail("workers out of scope"); }
        let started = Instant::now();
        let provider = parse_provider(&input);
        let (round, cached, candidate) = sparse_read_checkpoint(&checkpoint, AUDIT_PRIME)
            .unwrap_or_else(|| fail("missing checkpoint"));
        let candidate: LocalBTreeMap<_, _> = candidate.into_iter().collect();
        if round != 660 || cached.len() != 246_321 || candidate.len() != 352 { fail("round660 census mismatch"); }
        let (previous_round, previous_cached, previous_candidate) =
            sparse_read_checkpoint(&previous_checkpoint, AUDIT_PRIME).unwrap_or_else(|| fail("missing previous checkpoint"));
        let previous_candidate: LocalBTreeMap<_, _> = previous_candidate.into_iter().collect();
        if previous_round != 659 || previous_cached.len() != 245_290 || previous_candidate.len() != 384 {
            fail("round659 census mismatch");
        }
        let target = Mono::new(vec![T_ID; 12]);
        if candidate.get(&target).copied() != Some(1) { fail("target normalization mismatch"); }

        let old = shifted_old_seven();
        let high: LocalBTreeMap<_, _> = candidate.iter().filter(|(row, _)| t_exponent(**row) >= 4)
            .map(|(row, value)| (*row, *value)).collect();
        if high.len() != 8 { fail("high-t core census mismatch"); }
        let overlap = old.keys().filter(|row| candidate.contains_key(row)).count();
        let previous_overlap = old.keys().filter(|row| previous_candidate.contains_key(row)).count();
        let candidate_overlap = candidate.keys().filter(|row| previous_candidate.contains_key(row)).count();
        let same_coefficients = candidate.iter().filter(|(row, value)| previous_candidate.get(row) == Some(value)).count();
        let previous_high: LocalBTreeMap<_, _> = previous_candidate.iter()
            .filter(|(row, _)| t_exponent(**row) >= 4).map(|(row, value)| (*row, *value)).collect();
        if previous_high != high { fail("high-t core changed from round659 to round660"); }

        let full_columns = incidents(&provider, &candidate, workers);
        let full_vectors = materialize(&provider, &full_columns, workers);
        let full = audit_template("round660_full_candidate", &candidate, &cached, &full_vectors);
        if full.cached_bad != 0 { fail("retained candidate violates cached system"); }

        let old_columns = incidents(&provider, &old, workers);
        let old_vectors = materialize(&provider, &old_columns, workers);
        let old_audit = audit_template("shifted_d8_seven", &old, &cached, &old_vectors);
        let high_columns = incidents(&provider, &high, workers);
        let high_vectors = materialize(&provider, &high_columns, workers);
        let high_audit = audit_template("round660_high_t_eight", &high, &cached, &high_vectors);

        let mut ansatz = Vec::new();
        for (name, mode) in [("t_exponent", "t"), ("t_exponent_multiplicity", "t_partition"),
                             ("coarse_orbit_signature", "coarse_orbit")] {
            let (groups, count, constant) = group_rows(&candidate, mode);
            let (cached_consistent, cached_rank) = ansatz_consistency(&candidate, &groups, count, &cached, &full_vectors, true);
            let (global_consistent, global_rank) = ansatz_consistency(&candidate, &groups, count, &cached, &full_vectors, false);
            ansatz.push(AnsatzAudit { name, groups: count, cached_consistent, cached_rank,
                global_consistent, global_rank, candidate_constant_on_groups: constant });
        }

        let mut t_hist = LocalBTreeMap::<usize, usize>::new();
        for row in candidate.keys() { *t_hist.entry(t_exponent(*row)).or_default() += 1; }
        let mut previous_t_hist = LocalBTreeMap::<usize, usize>::new();
        for row in previous_candidate.keys() { *previous_t_hist.entry(t_exponent(*row)).or_default() += 1; }
        let t_hist_json = t_hist.iter().map(|(key, value)| format!("\"{key}\":{value}"))
            .collect::<Vec<_>>().join(",");
        let previous_t_hist_json = previous_t_hist.iter().map(|(key, value)| format!("\"{key}\":{value}"))
            .collect::<Vec<_>>().join(",");
        let tmp = output.with_extension("json.tmp");
        let mut out = BufWriter::new(File::create(&tmp).unwrap());
        writeln!(out, "{{").unwrap();
        writeln!(out, "  \"schema\": \"KRENN_AFFINE251_D12_ROUND660_STRUCTURED_DUAL_AUDIT_V1\",").unwrap();
        writeln!(out, "  \"status\": \"PASS_NEGATIVE_STRUCTURAL_DIAGNOSIS\",").unwrap();
        writeln!(out, "  \"prime\": {AUDIT_PRIME}, \"round\": 660, \"cached_columns\": 246321,").unwrap();
        writeln!(out, "  \"candidate_support\": 352, \"old_shifted_overlap\": {overlap},").unwrap();
        writeln!(out, "  \"t_exponent_histogram\": {{{t_hist_json}}},").unwrap();
        writeln!(out, "  \"round659_comparison\": {{\"support\":384,\"cached_columns\":245290,\"t_exponent_histogram\":{{{previous_t_hist_json}}},\"old_shifted_overlap\":{previous_overlap},\"support_overlap\":{candidate_overlap},\"same_coefficients\":{same_coefficients},\"lost_rows\":{},\"gained_rows\":{},\"high_t_eight_identical\":true}},",
            previous_candidate.len() - candidate_overlap, candidate.len() - candidate_overlap).unwrap();
        writeln!(out, "  \"templates\": [").unwrap();
        for (i, audit) in [&full, &old_audit, &high_audit].iter().enumerate() {
            let first = audit.first_bad.map(|(c,n)| format!("\"{} exact_pairing_numerator_over_2={}\"", column_text(c), n))
                .unwrap_or_else(|| "null".into());
            writeln!(out, "    {{\"name\":\"{}\",\"support\":{},\"incident\":{},\"cached_incident\":{},\"missing_incident\":{},\"cached_bad\":{},\"global_bad\":{},\"first_bad\":{}}}{}",
                audit.name, audit.support, audit.incident, audit.cached_incident, audit.missing_incident,
                audit.cached_bad, audit.global_bad, first, if i == 2 { "" } else { "," }).unwrap();
        }
        writeln!(out, "  ], \"ansatz\": [").unwrap();
        for (i, item) in ansatz.iter().enumerate() {
            writeln!(out, "    {{\"name\":\"{}\",\"groups\":{},\"candidate_constant_on_groups\":{},\"cached_consistent\":{},\"cached_rank\":{},\"global_consistent\":{},\"global_rank\":{}}}{}",
                item.name, item.groups, item.candidate_constant_on_groups, item.cached_consistent,
                item.cached_rank, item.global_consistent, item.global_rank, if i+1 == ansatz.len() { "" } else { "," }).unwrap();
        }
        writeln!(out, "  ],").unwrap();
        writeln!(out, "  \"global_incidence_closed\": {},", full.global_bad == 0).unwrap();
        writeln!(out, "  \"full_closure_run\": false, \"second_prime_run\": false,").unwrap();
        writeln!(out, "  \"elapsed_seconds\": {:.6}", started.elapsed().as_secs_f64()).unwrap();
        writeln!(out, "}}").unwrap();
        out.flush().unwrap(); drop(out); fs::rename(tmp, output).unwrap();
    }
}

fn main() { retained::audit_entry(); }
