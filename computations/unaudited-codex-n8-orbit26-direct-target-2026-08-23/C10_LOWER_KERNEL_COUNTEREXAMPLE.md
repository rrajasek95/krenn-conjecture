# The lex C10 coefficient is not lower-kernel invariant

Let `G0` and `G1` be the two normalized mixed generators with constant term
one, of word codes 3780 and 5108.  Write

`G1-G0 = Delta2 + Delta3 + Delta4`

by encoded y degree.  The constant and linear layers vanish.  For the y6
monomial

`m = 0111204950f8`

(with implicit multiplier `t^2`), form the literal source combination which
starts with `m*(G1-G0)`, cancels the 24 rows of `m*Delta2` using the code-3780
constant provider, and cancels the 64 rows of `m*Delta3` using the frozen
monic linear providers.

This combination has 90 nonzero source columns.  Direct literal replay of
all their normalized matching terms gives:

- zero collected output in every y degree at most 9;
- 714 nonzero y10 rows;
- coefficient `+1` at `q = 0111202020494f4f50f8`.

It is therefore an exact vector in the lower contraction kernel on which the
lex C10 coordinate is nonzero.  The deterministic scale-four residual has q
coefficient `-4`.  Because residual equals target minus source image, adding
`-4` times this kernel vector to the source correction cancels that one
coefficient exactly.

Thus the lex coefficient is not canonical: it depends on the lower-degree
kernel choice.  This does not cancel the other 713 rows of this mutation,
nor the full 140-million-row y10 residual, and does not establish ideal
membership.

Subsequent full degree-12 dual replay sharpens the guard: the same 90-column
mutation has `lambda` contribution `+1` in y10 and `-1` in y11, hence total
pairing zero (each literal source column pairs zero individually).  The full
dual therefore annihilates the complete source image, but not its y10
projection.  Since deterministic `C10` keeps that projected transfer layer,
this prevents promoting its fixed-representative certificate to a
right-inverse-invariant residual or full-`F^h` claim; see the degree-12
full-dual `REPORT.md` and `results_lower_kernel_dual_invariance.json`.

Replay:

```text
python3 computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/audit_c10_constant_provider_kernel.py
```

The checker passes normally, with `-O`, and with `-I -S`.  Logical digest:
`edc37a9c5c1785db383cc518fa151912ad1589e70d929b9e71915153fb3db80e`.
Result file SHA-256:
`cb1a569493022716d118e8796f8441f902ba693ed7699ccea7a3e51ca6ceb6f0`.
