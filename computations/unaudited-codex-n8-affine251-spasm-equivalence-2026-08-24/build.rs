use std::env;
use std::fs;
use std::path::PathBuf;

fn main() {
    let manifest = PathBuf::from(env::var("CARGO_MANIFEST_DIR").unwrap());
    let retained = manifest.join("../unaudited-codex-n8-affine251-orbit-membership-2026-08-24/src/main.rs");
    println!("cargo:rerun-if-changed={}", retained.display());
    let source = fs::read_to_string(&retained).unwrap();
    // include! inside a module rejects crate-level inner documentation.  This
    // build-only derivative changes documentation markers, never executable
    // tokens, and the runner pins the retained source itself.
    let sanitized = source.lines().map(|line| {
        if let Some(rest) = line.strip_prefix("//!") { format!("//{rest}") } else { line.to_owned() }
    }).collect::<Vec<_>>().join("\n") + "\n";
    fs::write(PathBuf::from(env::var("OUT_DIR").unwrap()).join("retained_main.rs"), sanitized).unwrap();
}
