# The canonical seven-block guard has a triangle-inactive point, but stars survive

Status: **an exact integer matrix-unit source on the canonical stuck support
satisfies the formal guard and normalized pure rows while having no active
carrier among all 560 cap/triangle choices.**  It is not globally cap-inactive:
two star carriers are active.  It also fails the full X5 equations.  Thus it
is a sharp negative control for a triangle-only lemma, not a counterexample to
the support-cap dichotomy or conjecture.

## Exact source on the referee's canonical support

Retain

```text
A03=A16=A27=A45=I3
S*={06,13,17,24,26,56,57}
variable family={04,12,35,67}.
```

All eleven nonidentity blocks are nonzero matrix units:

```text
A04= E20   A06= E10   A12=-E00   A13=-E11
A17=-E12   A24=-E12   A26=-E21   A35= E22
A56=-E22   A57=-E21   A67=-E01.
```

The four fixed blocks make all fifteen named support blocks nonzero.  This is
the exact seven-block stratum isolated by the independent referee manifest
`583bea19...`; the parent chain proves minimality relative to the present
support calculus because every at-most-six-block support is closed.

## Literal formal-guard equations

For cap `67`, triangle `012`, and `K=I3`, the audit separately evaluates the
direct and switched matrix term in each of the twelve forbidden response
equations.  Ten vanish termwise.  The two complete-rectangle cancellations
are

```text
R_15: -E12 + E12 = 0,
R_25:  E22 - E22 = 0.
```

Thus every forbidden response is literally zero, while no source block has
been specialized to zero.  The three pure amplitudes are exactly `(1,1,1)`.

## Complete activity-minor replay

For each of the 28 cap pairs and each of its 20 residual triangles, the audit
constructs the exact rational forbidden-response matrix `L_C`, computes its
rank, and tests whether each of

```text
K00, K11, K22, <K,A_C>
```

is nontrivial on `ker(L_C)`.  Across all 560 choices there are **zero active
triangle carriers**.  The rank census is

```text
rank 2:25, 3:21, 4:24, 5:55, 6:8, 7:29, 8:10, 9:388.
```

The same exact test was applied supplementarily to all 168 cap/star choices.
It finds exactly two active stars:

```text
cap16, center2: rank2, kernel dimension7,
cap45, center2: rank1, kernel dimension8.
```

All four activity restrictions are live in both kernels.  Therefore the
broader triangle-or-star terminal rule still routes this point to an active
clean cap.  This is load-bearing: omitting stars would yield a false lemma.

## Full X5 replay

The six distinguished mixed residual amplitudes are

```text
1, 1, 1, 1, 1, 2,
```

and exhaustive evaluation of all `3^8` words finds 114 nonzero mixed
amplitudes.  The first failed equation is `Phi(01100011)=1`.  Hence this point
is not X5 and does not refute the referee's missing lemma if all mixed source
equations are hypotheses.

## Exact conclusion

The statement

```text
formal guard + pure normalization
  => block zero or active triangle
```

is false already on `S*`.  Replacing “triangle” by “triangle or star” is not
refuted by this source, and adding the full X5 equations remains open.  The
64-locus coefficient boundary is therefore genuine, but the present witness
does not close it or produce a conjecture counterexample.  No broad CEGAR,
Gröbner sweep, or D12 artifact was used.
