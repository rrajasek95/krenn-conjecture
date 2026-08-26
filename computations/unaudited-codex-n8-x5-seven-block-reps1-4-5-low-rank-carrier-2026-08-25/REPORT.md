# Remaining full-family representatives: exact carrier closure

Status: **superseded/retracted: representatives 1, 4, and 5 are closed only in the zero outside-factor branch; nonzero ranks have pairing activity only.** The earlier all-rank claim omitted the three separate diagonal-functional conditions.

The exact sequential choice was rep5, rep1, rep4. Each has 12 independently regenerated supported perfect matchings and a two-term cap03/star4 carrier. Rep5 is the true first choice from the frozen 64-to-13 ledger because its selected best record already has guard-controlled common factor `A06`. The selected best records for reps1/4 instead have `P=RowSpan(A04^T,A06^T)`, and singularity of `A06` does not force that larger space proper; this first obstruction is recorded explicitly. Independent source enumeration then supplies a different exact two-term common-`A06` carrier for each of reps1/4, checked against the expanded full-family ledger.

For representative `i`, let `A_r7` be its outside factor (`A47` for reps1/4, `A37` for rep5), and `A_r6` its companion. The identity-guard equations are

`A06 A_r7^T=0`, `A_r7^T+A17 A_r6^T=0`, and `A26 A_r7^T+A_r6^T=0`.

If `A_r7=0`, then `A_r6=0`, the cap67 response map vanishes, and nonzero full-family `A67` makes cap67 active. If `A_r7` is nonzero, the first guard makes `A06` singular. In each representative, independent enumeration gives a two-term cap03/star4 factorization with left space `P=Row(A06^T)=Col(A06)`. Fixed `A03=I` proves only that the cap pairing is live. Each diagonal additionally requires `not(e_i in P and e_i in Q)`; singularity of `A06` does not establish all three exclusions.

Each record now includes a compatible local countermodel with outside factor `E11`, companion `-E11`, `A06=E00`, and a partner block `E00`. The guard holds and pairing is live, while `E00` lies in the response row space, so `K00` is dead. Ranks 1–3 remain open.

The exact source-labelled factors are `A06^T K [A13^T|A35]` (rep1), `A06^T K [A23^T|A35]` (rep4), and `A06^T K [A35|A37]` (rep5). A distinct rational rank-one local replay is checked for each support. No full-X5 equation or Gröbner solver is needed.

Scope is strict: rep2 and all non-full-family strata remain open.
