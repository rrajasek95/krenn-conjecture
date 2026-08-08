# Bounded unrestricted search protocol at \(N=8\)

Research evidence only.  This protocol can discover a counterexample, but a
failed numerical run proves nothing.  Every candidate still requires exact
reconstruction and an independent audit of all \(3^8=6561\) coefficients.

## Purpose

The unrestricted solver has 252 complex aggregate entries.  Its previous
border-start runs drove the residual down while the source norm grew.  That is
expected from the exact Laurent families and is not evidence for a finite
point.  `computations/search_n8_full_complex.py` now supports two controls:

* `--entry-bound B` makes the numerical search compact by bounding every real
  optimization coordinate in `[-B,B]`;
* `--l2-penalty lambda` is a discovery-only norm bias.  The script always
  reports and applies the candidate threshold to the unpenalized residual.

The output separately records the largest pure and mixed residuals, the
largest aggregate entry, and the number of real coordinates sitting
numerically on the imposed boundary.  Candidate archives include the three
pure values, cap, penalty, and boundary count.

## Campaign

Run independent real and complex starts at caps \(B=1,2,4,8\), first with no
penalty and then with small penalties such as \(10^{-8}\) and \(10^{-6}\).
For example:

```console
.venv/bin/python computations/search_n8_full_complex.py \
  --seed 10000 --starts 32 --maxiter 10000 --entry-bound 2 \
  --l2-penalty 1e-8 --candidate-threshold 1e-9 \
  --candidate-dir /tmp/krenn-n8-candidates
```

Repeat with `--real` and with border starts.  A residual which improves only
as the cap grows, with active boundary coordinates and growing norm, is a
border-escape signature.  A small residual stable under a tighter cap and
without boundary contact is worth high-precision refinement and exact
recognition.  Neither signature is an exact theorem.

## Acceptance gate

A saved floating-point archive is only a lead.  Before it can affect the
conjecture status it must be recognized over \(\mathbb Q\), a cyclotomic
field, or another explicit number field, and a separate exact checker must
expand all 105 perfect matchings for all 6561 color words.  The three pure
coefficients must equal one and all 6558 mixed coefficients must equal zero.

The numerical implementation itself is guarded by
`computations/verify_n8_full_complex_search.py`, which independently expands
the matching polynomial, checks the real and complex analytic gradients, and
rechecks the two-word Laurent border residual.

## Initial bounded census

The first smoke census used complex cap \(B=2\), penalty \(10^{-8}\), and 400
iterations.  Four generic starts (seeds 10000--10003) all stopped at raw loss
\(1/2\), maximum residual one, and zero boundary coordinates.  Two starts from
the known Laurent family (seeds 10100--10101, 600 iterations) instead reached
losses \(3.45\cdot10^{-4}\) and \(2.44\cdot10^{-4}\), but used respectively 13
and 12 boundary coordinates.  Their largest complex entry had modulus
\(2\sqrt2\), the maximum allowed when both real and imaginary parts are at the
cap.  This cleanly reproduces the distinction the bounded protocol is meant
to expose: the only small residuals in this census lean directly on the
artificial boundary.  It remains numerical evidence only.
