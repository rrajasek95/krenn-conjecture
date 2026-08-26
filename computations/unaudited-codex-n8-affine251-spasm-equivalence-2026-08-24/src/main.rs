#[allow(dead_code)]
mod retained {
    include!(concat!(env!("OUT_DIR"), "/retained_main.rs"));

    use std::collections::HashMap as LocalHashMap;
    use std::env as local_env;

    fn arg_map() -> LocalHashMap<String, String> {
        let args: Vec<String> = local_env::args().collect();
        let mut out = LocalHashMap::new();
        let mut i = 1usize;
        while i < args.len() {
            if !args[i].starts_with("--") || i + 1 >= args.len() {
                fail("exporter expects --key value arguments");
            }
            if out.insert(args[i].clone(), args[i + 1].clone()).is_some() {
                fail("duplicate exporter argument");
            }
            i += 2;
        }
        out
    }

    pub fn export_entry() {
        let args = arg_map();
        let get = |key: &str| args.get(key).cloned().unwrap_or_else(|| fail(format!("missing {key}")));
        let input = PathBuf::from(get("--input"));
        let checkpoint = PathBuf::from(get("--checkpoint"));
        let matrix_path = PathBuf::from(get("--matrix"));
        let rhs_path = PathBuf::from(get("--rhs"));
        let metadata_path = PathBuf::from(get("--metadata"));
        let degree: usize = get("--degree").parse().unwrap_or_else(|_| fail("bad degree"));
        let prime: u64 = get("--prime").parse().unwrap_or_else(|_| fail("bad prime"));
        let workers: usize = get("--workers").parse().unwrap_or_else(|_| fail("bad workers"));
        let wall_seconds: u64 = get("--wall-seconds").parse().unwrap_or_else(|_| fail("bad wall"));
        let rss_gib: u64 = get("--rss-gib").parse().unwrap_or_else(|_| fail("bad rss"));
        if !(degree == 10 || degree == 11) || prime != 1_073_741_827 || workers == 0 || workers > 16 {
            fail("export scope/prime/workers mismatch");
        }

        let mut gate = Gate::new(wall_seconds, rss_gib);
        let provider = parse_provider(&input);
        if provider.parsed_terms != 688_908 || provider.distinct_terms != 688_906 {
            fail("provider census mismatch");
        }
        let closure = read_checkpoint(&checkpoint, degree).unwrap_or_else(|| fail("missing checkpoint"));
        if !closure.complete || !closure.row_frontier.is_empty() || !closure.column_frontier.is_empty() {
            fail("checkpoint is not complete");
        }
        let mut rows: Vec<_> = closure.rows.iter().copied().collect();
        let mut columns: Vec<_> = closure.columns.iter().copied().collect();
        rows.sort_unstable();
        columns.sort_unstable();
        let row_id: HashMap<Mono, usize> = rows.iter().enumerate().map(|(i, row)| (*row, i)).collect();
        let target = Mono::new(vec![T_ID; degree]);
        let target_id = *row_id.get(&target).unwrap_or_else(|| fail("target absent"));

        let matrix_tmp = matrix_path.with_extension("sms.tmp");
        let rhs_tmp = rhs_path.with_extension("sms.tmp");
        let metadata_tmp = metadata_path.with_extension("json.tmp");
        let mut matrix = BufWriter::new(File::create(&matrix_tmp).unwrap_or_else(|e| fail(e.to_string())));
        writeln!(matrix, "{} {} M", columns.len(), rows.len()).unwrap();
        let mut nnz = 0usize;
        let mut max_abs = 0i64;
        for (batch_index, batch) in columns.chunks(1024).enumerate() {
            if gate.check().is_err() {
                drop(matrix);
                let _ = fs::remove_file(&matrix_tmp);
                fail("export resource gate");
            }
            let invariants = parallel_invariant_columns(&provider, batch, prime, workers);
            for (within, invariant) in invariants.into_iter().enumerate() {
                let column_id = batch_index * 1024 + within;
                for (row, value) in invariant {
                    let rid = *row_id.get(&row).unwrap_or_else(|| fail("matrix row absent"));
                    let signed = if value <= prime / 2 { value as i64 } else { value as i64 - prime as i64 };
                    if signed == 0 || signed.unsigned_abs() >= prime / 2 {
                        fail("coefficient signed-lift failure");
                    }
                    max_abs = max_abs.max(signed.abs());
                    writeln!(matrix, "{} {} {}", column_id + 1, rid + 1, signed).unwrap();
                    nnz += 1;
                }
            }
        }
        writeln!(matrix, "0 0 0").unwrap();
        matrix.flush().unwrap();
        drop(matrix);

        let mut rhs = BufWriter::new(File::create(&rhs_tmp).unwrap_or_else(|e| fail(e.to_string())));
        writeln!(rhs, "1 {} M", rows.len()).unwrap();
        writeln!(rhs, "1 {} 1", target_id + 1).unwrap();
        writeln!(rhs, "0 0 0").unwrap();
        rhs.flush().unwrap();
        drop(rhs);

        if gate.check().is_err() {
            let _ = fs::remove_file(&matrix_tmp);
            let _ = fs::remove_file(&rhs_tmp);
            fail("final export resource gate");
        }
        fs::rename(&matrix_tmp, &matrix_path).unwrap_or_else(|e| fail(e.to_string()));
        fs::rename(&rhs_tmp, &rhs_path).unwrap_or_else(|e| fail(e.to_string()));
        let mut metadata = BufWriter::new(File::create(&metadata_tmp).unwrap_or_else(|e| fail(e.to_string())));
        writeln!(metadata, "{{").unwrap();
        writeln!(metadata, "  \"schema\": \"KRENN_AFFINE251_SPASM_EXPORT_V1\",").unwrap();
        writeln!(metadata, "  \"status\": \"PASS\",").unwrap();
        writeln!(metadata, "  \"degree\": {degree},").unwrap();
        writeln!(metadata, "  \"lift_prime\": {prime},").unwrap();
        writeln!(metadata, "  \"matrix_orientation\": \"orbit_columns_by_orbit_rows_A_transpose\",").unwrap();
        writeln!(metadata, "  \"row_orbits\": {},", rows.len()).unwrap();
        writeln!(metadata, "  \"column_orbits\": {},", columns.len()).unwrap();
        writeln!(metadata, "  \"matrix_nnz\": {nnz},").unwrap();
        writeln!(metadata, "  \"target_row_id_zero_based\": {target_id},").unwrap();
        writeln!(metadata, "  \"max_abs_integer_coefficient\": {max_abs},").unwrap();
        writeln!(metadata, "  \"workers\": {workers},").unwrap();
        writeln!(metadata, "  \"elapsed_seconds\": {:.6},", gate.elapsed()).unwrap();
        writeln!(metadata, "  \"peak_rss_kib\": {}", gate.peak_rss_kib).unwrap();
        writeln!(metadata, "}}").unwrap();
        metadata.flush().unwrap();
        drop(metadata);
        fs::rename(&metadata_tmp, &metadata_path).unwrap_or_else(|e| fail(e.to_string()));
    }
}

fn main() {
    retained::export_entry();
}
