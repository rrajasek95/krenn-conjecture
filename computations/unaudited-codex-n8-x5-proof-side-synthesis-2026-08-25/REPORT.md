# X5 proof-side evidence synthesis

Status: **the retained evidence completes the four frozen branches through D10
and the direct branch at D11; it does not close coloured D11 or an all-degree
derivation.**

## Exact chain already available

Each of the four canonical frozen providers has a primitive integer dual with
target value one and exhaustive literal source replay in degrees 6, 7, 8, 9,
and 10.  Supports grow from 10--14 at D6 to 243--253 at D10.  D6--D9 weights
are ±1; the three coloured D10 certificates use ±1,±2 while direct remains ±1.
These are exact characteristic-zero homogeneous nonmembership statements, not
a full-conjecture result.

At D11, direct is also exact: its 243-row D10 certificate transports by one t
with zero failures.  The coloured transports instead have exactly 76, 76, and
70 failures, all t-free C1 columns.  The current triangle checkpoint is exact
only over p107 and only on its selected 1,250,001 columns (support 1,378,456).
It is neither globally scanned after its final recomputation nor lifted to
characteristic zero.  Third and cap have no accepted repair certificate.

## Cheap exact identity tests

The sealed coefficient files confirm only three pure adjacent transports:
direct D6→D7, direct D8→D9, and direct D10→D11.  No other adjacent D6--D10
transport is exact.  Searching the normalized two-step scalar templates
`lambda_d=a E(lambda_(d-1))+(1-a)E^2(lambda_(d-2))` for small integral a finds
only the already-known direct D8→D9 pure shift.  No correction at D9 or D10 is
the t-shift of the previous correction; the tested maps have zero matching
shifted correction rows.  Thus a simple scalar or shifted-carrier recurrence is
contradicted by the retained certificates.

One new supported identity is useful: for every coloured branch,

```text
lambda_10,b - E(lambda_9,b) = Q_10 + B_10,b.
```

Here `Q_10` is the same 168-row, entirely t-free ±1 map in all three branches;
the branch tails have 14/16/16 entirely t-free rows with weights ±1,±2.  The
tails are not shifted D8 carriers and share zero such rows.  This isolates a
real common correction core, but it is not itself a D11 repair theorem.

The finite all-degree contraction test also closes negatively.  Direct D10
has no C1 failure, explaining D11, but it fails all 491 C2 candidates and all
615 C4 candidates.  Hence even the newest exact direct certificate cannot be
iterated beyond one step by the sealed contraction lemma.

## A proved same-source response lemma

There is one exact bridge that had not been stated in the certificate
inventory.  For two disjoint physical pairs `pq` and `ab`, endpoint-ordered
cap covectors `K` on `pq` and `L` on `ab` obey

```text
<L,R_ab^pq(K)> = <K,R_pq^ab(L)>.                       (A)
```

Indeed, on the basis coordinates `(i,j;alpha,beta)`, both sides are the same
two literal source monomials

```text
A_pa[i,alpha] A_qb[j,beta]
  + A_pb[i,beta] A_qa[j,alpha].                        (B)
```

The checker proves equality of the stored-edge labels on all 420 disjoint
named pair configurations and all 81 coordinate pairs (34,020 identities).
Thus (A) is not a comparison of independently chosen sources: it is the
adjoint response for the switched physical cap pair on the same source.

Combine (A) with the sealed cyclic five-set identity.  If coloured branch
`d` has `ell_d in rowspan L_T^pq`, then

```text
b_d ell_d - Theta_(t,beta,d) R_ab^pq in rowspan L_T^pq
```

implies, after subtracting the blocker row,

```text
R_pq^ab(L_(t,beta,d)) in rowspan L_T^pq,               (C)
```

where `L_(t,beta,d)` is the literal covector represented by `Theta`.  This is
a genuine source-labelled different-cap cancellation statement for each of
the three coloured canonical branches.  To turn (C) into the missing clean-
cap arrow one still has to prove for this same `L` the activity conditions
`s_L*kappa_0*kappa_1*kappa_2 != 0` and the cap-error identity
`E_ab(L)=0`; neither follows from (A)--(C).

The retained formal hostile source isolates the first false strengthening.
There `L=E00` on switched cap `12`; its response is supported only on edge
`67`, so `r^2=0` and the cap error is clean, and (A) still pairs to one.
Nevertheless

```text
s_L=<E00,A_12>=0,       (kappa_0,kappa_1,kappa_2)=(1,0,0).
```

So “the reciprocal five-set covector is automatically an active clean cap”
already fails at activity.  This guard is deliberately not a normalized X5
point; it proves only that a pure-row/full-X5 input is load-bearing for any
such strengthening.

For the fourth, direct blocker branch there is an earlier obstruction: all
15 matchings containing the direct edge `pq` lie in the one-crossing sector
annihilated by `beta`.  Hence the surviving cyclic identity contains no
`s=<K,A_pq>` row to subtract.  The first literal missing term is
`67|01|23|45`.  Direct-branch cancellation therefore needs a different
source identity, not another rearrangement of the cyclic five-set formula.

## Three finite missing-arrow lemmas

1. A target-zero correction `R_11,b` satisfying
   `R_11,b(c)=-E(lambda_10,b)(c)` on every incident literal column would make
   `E(lambda_10,b)+R_11,b` an exact coloured D11 dual.  This is the most direct
   missing arrow.  It is supported as a finite problem beginning with
   76/76/70 C1 equations, but the two tested small spaces are exactly
   inconsistent: transported support plus violation rows, and the complete
   362-shift span.  Any solution needs genuinely new support.

2. An explicit variable permutation fixing t and carrying the triangle
   provider to third or cap would transfer a future global triangle D11 dual.
   This is a finite 6,571-generator identity.  The identity permutation is
   contradicted: the three initial offender sets are pairwise disjoint, and
   identity-coordinate transport of the older sealed 307,885-column triangle
   checkpoint leaves 208,088 violations in each target.  This test does not
   cover the newer 1,250,001-column checkpoint or any nontrivial permutation;
   no such permutation certificate is retained.

3. The sealed finite-contraction identities would turn one dual into an
   all-degree obstruction.  The lemma itself is proved, but every available
   candidate base is contradicted by explicit contraction failures; direct D10
   adds the new exact 491 C2 plus 615 C4 failure count.  Existing evidence
   therefore cannot supply this induction arrow.

## Conclusion

Existing artifacts rigorously finish the bounded D6--D10 derivations and
direct D11.  They do not, by recombination alone, finish coloured D11 or the
unrestricted-degree step.  The only currently viable exact arrow is a new-
support coloured D11 correction followed by a second-prime/characteristic-zero
lift and exhaustive replay; the modular partial checkpoint is progress toward
that computation, not a substitute for it.  No D12 data was read and no new
heavy solve was run.

## Provenance pins

The authoritative manifest hashes are: D6 `a23dbe45...`, D7 `ec76bf16...`,
D8 `735a75ce...`, coloured D9 `8bcc657b...`, direct D9/recurrence theorem
`dc529b4d...`, D10 `28ccf267...`, D11 seeded gate `828fb7ac...`, cross-branch
identity transport `69c49063...`, and the current triangle partial checkpoint
`6a392f8f...`. Full hashes and exact local/upstream file pins are in
`EVIDENCE.json`, `results_synthesis_audit.json`, and `MANIFEST.sha256`.
