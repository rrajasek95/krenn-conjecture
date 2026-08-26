# The slice master relations (W26-M and W26-M*)

> **UNAUDITED STAGING — not spine, not committed.** Drafted 2026-08-20 by lane
> **P3** at pinned repository HEAD
> `e2123f2c006944972cefcdce1b8a3c021f9c2a18`. Staged for manager review on the
> verdict of audit **A10**
> (`computations/unaudited-audit-a10-2026-08-20/REPORT.md`), whose
> "Promotion-ready" list opens with "W26-M/M* identities".
>
> Source lanes: **W26** (`computations/unaudited-blockers-w26-2026-08-16/`,
> pinned `dee2ca3293f5f0c12831b374f6cf521aa2c02e14`) proved the relations;
> **A10** (`computations/unaudited-audit-a10-2026-08-20/`, pinned
> `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`) **re-derived them by hand from
> the model definition, importing nothing from W26 or W30**, and re-verified
> them numerically.
>
> **The statement below is A10's form.** Where A10's re-derivation and W26's
> reported form differ in notation, A10's wins, per the exactness discipline of
> this lane. See §6 for the reconciliation.

## 1. The model, fixed once

`N = 8`, alphabet `{0,1,2}`, one `3 x 3` block `A_uv` per edge `uv` of `K_8`.
For a word `w : V -> {0,1,2}`,

```
    H_w(A, z)  =  sum over the 105 perfect matchings M of K_8
                    of  prod_{(u,v) in M}  c_uv( w_u , w_v ),
```

where an edge with mask `511` (a **Gamma** edge) contributes `A_uv[w_u][w_v]`,
an edge with a one-bit mask (a **single**, at cell `(a,b)`) contributes `z_uv`
when `(w_u, w_v) = (a,b)` and `0` otherwise, and an absent edge contributes
`0`. Write

```
    Phi(w)  :=  the z-free part of H_w  =  sum over the perfect matchings
                that lie inside Gamma.
```

Fix the bipartition and the pairing

```
    L = {0,1,2,3},   R = {4,5,6,7},
    sigma = ( 0 <-> 7 ,  1 <-> 4 ,  2 <-> 5 ,  3 <-> 6 ).
```

`Gamma` is `K_4(L)` together with the `R`-graph and the *present* `sigma`
edges. Write

```
    l_ij  =  A_{i,j}[x_i][x_j]            for i < j in L,
    r_ab  =  A_{a,b}[y_a][y_b]            for a < b in R,
    d_a   =  A_{a, sigma a}[x_a][y_{sigma a}]     for a in L,

    hafL  =  l_01 l_23 + l_02 l_13 + l_03 l_12,
    hafR  =  r_45 r_67 + r_46 r_57 + r_47 r_56.
```

*(Source of the model and of these names:
`computations/unaudited-audit-a10-2026-08-20/a10_lib.py`, module docstring
"MODEL" and "HAND RE-DERIVATION OF THE SLICE ROWS", lines 16–44.)*

Every `Gamma` perfect matching uses `k in {0, 2, 4}` sigma edges, so

```
    Phi  =  hafL * hafR
            +  sum_{i<j in L}  l_ij * r_{sigma i, sigma j} * d_p * d_q
            +  d_0 d_1 d_2 d_3 ,                                        (1)
```

with `{p,q} = L - {i,j}` in the middle sum. **(1) is the whole structural
input**; everything below is (1) plus one three-pairing identity.

## 2. Theorem (W26-M): the R-vertex master relation

**Theorem 2.1 (R-vertex master relation; W26-M, in A10's form).**
Let `v in R`, put `p = sigma^{-1}(v) in L`, and vary *only* the letter `t` at
`v`, holding the other seven coordinates fixed. Then

```
    hafL * Phi(t)  =  sum_{q != p}  B_q * ROW(t)[q] ,                    (M)
```

where the sum is over `q in L - {p}` and

```
    B_q       =  hafL * r_{sigma i, sigma j}  +  l_pq * d_i * d_j ,
                                                    {i,j} = L - {p,q},

    ROW(t)[q] =  d_p(t) * ( d_q * l_ij )  +  hafL * r_{v, sigma q}(t) .
```

Here `d_p(t)` and `r_{v, sigma q}(t)` are the two objects that carry the letter
`t` at `v`: `d_p(t) = A_{p, v}[x_p][t]` and
`r_{v, sigma q}(t) = A_{v, sigma q}[t][y_{sigma q}]`. Every other symbol is
constant in `t`.

*Proof.* Collect (1) by the two occurrences of `v`:

```
    Phi(t)  =  sum_{q != p}  r_{v, sigma q}(t) * B_q  +  d_p(t) * A,
    A       =  sum_{q != p}  l_ij * r_{sigma i, sigma j} * d_q
               +  prod_{q != p} d_q .
```

Multiply by `hafL` and apply the **three-pairing identity**

```
    hafL * prod_{q != p} d_q  =  sum_{q != p}  l_pq * l_ij * d_i * d_j * d_q ,
                                                    {i,j} = L - {p,q},   (2)
```

which is the expansion of `hafL = l_pq l_ij + l_pi l_qj + l_pj l_qi` against
the product of the three `d`'s. Regrouping gives exactly (M). `∎`

**Theorem 2.2 (W26-M*: the L-dual).** Let `p in L` and vary only the letter `s`
at `p`. Then

```
    hafR * Phi(s)  =  sum_{a != p}  X_a * ROW(s)[a] ,                   (M*)

    X_a        =  hafR * l_bc  +  r_{sigma p, sigma a} * d_b * d_c ,
                                                    {b,c} = L - {p,a},

    ROW(s)[a]  =  d_p(s) * ( d_a * r_{sigma b, sigma c} )
                  +  hafR * l_{p,a}(s) .
```

*Proof.* The same computation with the roles of `L` and `R` exchanged; the
sigma-pairing makes the exchange an involution of (1). `∎`

*Source of both statements, verbatim:*
`computations/unaudited-audit-a10-2026-08-20/a10_lib.py`, lines 31–44 —
A10's independent hand re-derivation. The implementations are
`slice_rows()` (the `ROW` vectors and the scale) and `psi_vector()` (the
coefficient vectors `B_q` / `X_a`), `a10_lib.py` lines 375–465.

## 3. Hypotheses — stated explicitly, because they are load-bearing

**(H-M1) The relation is an identity in the block entries.** (M) and (M*) hold
at *every* assignment of the blocks, over any commutative ring. They are not
properties of clean points, of off-stratum points, or of any solution locus.
A10 tested exactly this by verifying them at **random** blocks (§4).

**(H-M2) The relation carries information only where its scale is nonzero.**
The scale of (M) is `hafL`; the scale of (M*) is `hafR`. When the scale
vanishes both sides are `0 = 0` and the relation says nothing about
`Phi`. This is not a defect to be repaired — it is the mechanism behind the
`(H)` escape and behind the `m=28/L2` exception (see
`draft_lemma_w30y.md` §5). It is enforced in code:

> `slice_rows(...)` "Returns None when the scale (hafL at an R-vertex, hafR at
> an L-vertex) vanishes — the master relation carries no information there."
> (`computations/unaudited-audit-a10-2026-08-20/a10_lib.py`, lines 375–381.)

**(H-M3) No hypothesis on the point.** Cleanness, off-stratum-ness, all-cells-
nonzero and the vanishing stratum are **not** used. They enter only in the
downstream lemmas that consume the relation, never in (M)/(M*).

**(H-M4) `t` and `s` range over the full alphabet.** The relation is stated for
each of the three letters separately; nothing is assumed about which letters
are clean, triggered or firing. That bookkeeping belongs to the delivery
predicate, not to the identity.

## 4. Verification record

### 4.1 W26 (the origin lane)

W26's final report records the relations as **proved**, in this wording:

> THEOREM W26-M (R-vertex master relation) + W26-M* (L-dual):
> h Psi[D_p] = sum_q D_q l_ij Psi_q — every vertex at every support
> (incl. m=28) reduces to a three-vector slice equation. Symbolic,
> **16 (m,vertex) pairs**, mutation controls 8/8.

(`computations/unaudited-blockers-w26-2026-08-16/REPORT.md`, lines 16–19.)

W26's report does not enumerate *which* 16 of the 32 `(m, vertex)` pairs were
checked symbolically. See `MANIFEST.md` §"Open questions", item 2 — this is a
question for W26 or for the promotion audit, not something this lane can
resolve from documentation. It does not affect the standing of the theorem,
because A10's independent check below covers **all 32** pairs.

W26's engine was cross-checked against `w21_core` / `w24_core`, reproducing
**39/39** stored verdicts (same report, line 4).

### 4.2 A10 (the audit lane, from scratch)

A10 re-derived (M) and (M*) by hand and checked them numerically at random
blocks — the correct control for an identity, since a check at clean points
alone could not distinguish an identity from a coincidence on the locus.
Control `C2_master_relation`:

```
    4 supports (m = 25, 26, 27, 28)
      x 2 fields (F_31 and Q, the latter with Fraction blocks)
      x 8 vertices (R4 R5 R6 R7 L0 L1 L2 L3)
      x 12 random words
      x 3 letters
    ------------------------------------------------------
    violations = 0
```

Sources: `computations/unaudited-audit-a10-2026-08-20/results_smoke.json`, key
`C2_master_relation`: `{"violations": 0, "sample": [], "ok": true}`;
`computations/unaudited-audit-a10-2026-08-20/log_smoke.txt`, line 2:
`C2 master relation: violations=0`. The driver is `a10_smoke.py` lines 73–92
(the loop is quoted structurally above); the checker is
`a10_lib.py:check_master()`. The declared-control manifest is asserted at the
end of the run — `MANIFEST OK ['C1_phi_two_routes', 'C2_master_relation',
'C3_structure', 'C4_index_counts', 'C5_mutation_on_phi_identity']` — which is
the ledger-item-21 guard (a control that never runs must fail loudly).

**Mutation control.** `C5_mutation_on_phi_identity` reports
`base=True changed=True agree=True` (`log_smoke.txt`, line 15), i.e. the
identity checker is not vacuously true: perturbing the model changes the
verdict. Independently, A10's `Phi` itself was computed by **two** routes — raw
enumeration of all 105 perfect matchings (`phi_raw`) and the sigma-count
decomposition (`phi_formula`) — with `C1_phi_two_routes: mismatches = 0`
(`results_smoke.json`). Since `phi_formula` is precisely equation (1), **C1 is
also a check of (1)**, which is the sole structural input to (M)/(M*).

### 4.3 What is *not* claimed by the verification

The verification is numerical at random blocks in two fields plus a proof by
hand. It is **not** a computer-algebra proof of the identity in the polynomial
ring. The proof of record is the hand derivation of §2 (four lines, plus the
three-pairing identity (2)); the numerics are its control. A reviewer wanting a
symbolic certificate should ask W26 for the 16-pair symbolic run, or re-derive
(2) by inspection — it is a single expansion of `hafL`.

## 5. What the relations are used for, and what they do not give

Used for: they are the *only* bridge from the hafnian `Phi` to a finite-
dimensional linear-algebra object. The vector `ROW(t)` is the row indexed by
letter `t`; the delivery predicate and every rank statement downstream
(`draft_cofactor_qspan.md`, `draft_lemma_w30y.md`) are statements about the
span of these rows.

**They do not give**, and are nowhere used to give:

- any unconditional statement about a vertex at any support (the scale
  hypothesis (H-M2) alone forbids it);
- any statement over `Q`/`C` that is not already a statement over an arbitrary
  commutative ring — (M)/(M*) are characteristic-free, which is exactly why the
  *refutations* downstream (all over `F_p`) do not touch them;
- W26's `det M = 0` conclusion, which needs the cofactor identity as well; see
  `draft_cofactor_qspan.md` §5 and A10 correction **D8**.

## 6. Reconciliation of the two forms, and the delivery predicate

W26 reports the relation as `h Psi[D_p] = sum_q D_q l_ij Psi_q`
(`computations/unaudited-blockers-w26-2026-08-16/REPORT.md`, line 17). A10's
(M) is the same statement with every symbol named: `h = hafL`, `Psi[D_p]` is
the `d_p(t)`-weighted slice, `D_q l_ij` is the first summand of `ROW(t)[q]`,
and the `Psi_q` are the `B_q`. **This document uses A10's form throughout**;
W26's compressed form is recorded here only so that a reader of W26's report
can match the two.

For completeness, the predicate that consumes `ROW` — identical in W26's and
W30's code, and named `FAIL_primary` by A10 (see `draft_lemma_w30y.md` §3):

> at an index choice (letters on the 7 coordinates != v) let `T_f` = letters
> at which some LIVE single into v fires, `T_c` = the rest. The vertex
> DELIVERS at that index choice iff `ROW(t_f) in span{ROW(t) : t in T_c}` for
> every `t_f in T_f`; it FAILS iff it delivers at NO admissible index choice.

(`computations/unaudited-audit-a10-2026-08-20/a10_lib.py`, lines 46–50,
verbatim.)

## 7. Artifact paths

| lane | role | directory | pinned HEAD |
|---|---|---|---|
| **W26** | origin: proved W26-M / W26-M*, symbolic on 16 `(m,vertex)` pairs, mutation controls 8/8 | `computations/unaudited-blockers-w26-2026-08-16/` | `dee2ca3293f5f0c12831b374f6cf521aa2c02e14` |
| **W30** | consumer: built the slice-matrix machinery on top of the relations | `computations/unaudited-exclusion-w30-2026-08-19/` | `021b1a307e8edb10b964fadefd4b823bdb589035` |
| **A10** | independent re-derivation and re-verification (zero imports from W26/W30) | `computations/unaudited-audit-a10-2026-08-20/` | `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a` |
| **P3** | this write-up | `computations/unaudited-promotion-p3-2026-08-20/` | `e2123f2c006944972cefcdce1b8a3c021f9c2a18` |

Specific artifacts:

- statement and hand derivation — `computations/unaudited-audit-a10-2026-08-20/a10_lib.py`, lines 25–51;
- implementation — same file, `slice_rows()` (375–427), `psi_vector()` (428–465), `check_master()`;
- verification — `computations/unaudited-audit-a10-2026-08-20/results_smoke.json` (`C1_phi_two_routes`, `C2_master_relation`, `C5_mutation_on_phi_identity`) and `log_smoke.txt`;
- W26's origin claim — `computations/unaudited-blockers-w26-2026-08-16/REPORT.md`, §"Proved", first bullet;
- A10's green light — `computations/unaudited-audit-a10-2026-08-20/REPORT.md`, §"Promotion-ready (A10's list)";
- master-plan context — `notes/2026-08-15-resolution-master-plan.md`, v48 addendum (W26 final) and v57 addendum (A10's confirmation).

**Standing.** Per the ledger's rule, this is a piece of machinery, not a
closure: it proves no part of the Krenn–Gu conjecture and narrows nothing. It
is promoted because it is an identity that three lanes now depend on, and
because A10 re-derived it independently.
