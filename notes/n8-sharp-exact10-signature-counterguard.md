# The exact-ten incidence signature does not select the Laurent branch

This note records a sharp guard on the residual cap-26 attack from
`notes/n8-sharp-full-fibre-completion-frontier.md`.  After the exact closure
of all eight- and nine-cell direct repairs, a hypothetical cap-26 completion
must add ten cells forming an inclusion-minimal transversal of the eleven
original singleton-mate obligations.

It is natural to hope that the `11 obligations / 10 cells` incidence pattern,
together with alternating-cycle data, selects one of two coefficient
certificates:

1. an odd dependency in the signed binomial lattice; or
2. a nonzero one-class residual after quotienting by that lattice.

The accompanying exact checker

```text
computations/verify_n8_sharp_exact10_signature_counterguard.py
```

shows that the branch cannot be selected from those structural invariants.

## Two exact-ten repairs

Over the corrected 16-cell chart-26 seed, adjoin either

```text
A = 04;22 17;11 26;00 26;21 34;02
    36;22 37;00 37;12 45;11 67;21
```

or

```text
B = 01;20 17;11 26;00 26;21 34;02
    35;21 37;00 37;12 45;11 67;21.
```

Both sets have ten cells, repair all eleven seed singleton fibres, and are
inclusion-minimal: deleting any displayed cell reopens at least one original
obligation.

The following data agree exactly, not merely as degree histograms:

* all eleven original fibres become binomial;
* the full mixed binomial system has 25 rows and rational rank 7;
* after ordering the ten cells lexicographically, the essential
  obligation-to-cell incidence rows are

```text
(9), (2,6), (3,7), (3,7), (2,6), (9),
(3,7), (4,9), (4,9), (0,5), (1,8);
```

* the obligation-overlap graph is literally the same labelled graph, with
  edges

```text
05 07 08 14 23 26 36 57 58 78;
```

* across all 25 binomial fibres, the matching symmetric differences are
  exactly 23 single alternating `C4` cycles and two single alternating `C6`
  cycles.

Thus rank, circuit parity opportunity, the complete alternating-cycle
census, essential-cell provenance, and the obligation-overlap graph do not
distinguish the examples.

## Different exact algebra

For `A`, the signed binomial lattice is consistent.  Quotienting by its
maximal exact lattice leaves the four-term sharp fibre `00002121` in one
Laurent class with coefficient `-2`.  Since every chart variable is nonzero,
that coefficient cannot vanish in characteristic zero.

For `B`, the signed binomial lattice is inconsistent.  It contains ten unit
odd triangles.  The first uses words

```text
00000021, 10102121, 20002121
```

and its exact exponent rows satisfy

\[
                         -r_0+r_{12}+r_{18}=0.
\]

The coefficient sum is one, whereas every binomial equation requires
character `-1`, giving the usual odd Laurent contradiction.

Both supports also have secondary singleton fibres: their mixed histograms
are respectively `{1:49,2:25,4:1}` and `{1:53,2:25,4:1}`.  They are not
semantic survivors and certainly are not Krenn counterexamples.

## Consequence

The observed odd-or-one-class dichotomy remains a plausible exhaustive
cap-26 theorem, but it cannot be derived by assigning a certificate branch
to the named incidence/cycle signatures.  The signed endpoint-colour
exponents are load-bearing even when every coarse and labelled incidence
datum above agrees.  A successful theorem must either:

* prove a non-exclusive statement in which the one-class mechanism includes
  the forced secondary singleton directly; or
* retain enough signed exponent provenance to distinguish the two supports.

This is the stopping rule for signature compression: do not enumerate more
degree/cycle palettes unless the canonical key retains the actual signed
Laurent row matroid.

Reproduce with

```bash
PYTHONPATH=computations .venv/bin/python \
  computations/verify_n8_sharp_exact10_signature_counterguard.py
```
