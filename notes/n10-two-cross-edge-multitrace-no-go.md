# Scalar multitraces do not repair the two-cross contraction

## Outcome

The natural finite repair of the one-controller contraction fails exactly on
the explicit two-cross witness

\[
 A_{10}(t,s)=A_8\otimes g_{89}+tE_{08;00}+sE_{19;00}.    \tag{1}
\]

On a cut \(z\), let \(P_a\) be the controlled trace for an old controller
\(a\) on the five-vertex insertion shore.  Every scalar multitrace which
reconstructs the forced-pair lift and preserves the target has the form

\[
          Q_\lambda=\sum_{a\in U_z}\lambda_aP_a,
          \qquad \sum_a\lambda_a=1.                     \tag{2}
\]

For each candidate cut \(z=0,1,5\), exact quotient equations from the mixed
\(ts\) residual instead force

\[
                         \sum_a\lambda_a=0.              \tag{3}
\]

Thus no scalar combination of any finite family of the old controlled
traces can repair the contraction.  On cut 5, the quadratic cofactor
conditions alone are already inconsistent with (2).

There is also a precise direct-sum obstruction.  The fatal mixed row has the
same image under every controller, so retaining a controller label does not
separate it from diagonal forced-lift data.  Any direct-sum reconstruction
which is the identity on all diagonal old rows must retain the fatal class.
The next possible repair therefore needs a genuinely new, non-scalar datum:
a tag recording the ordered pair of old endpoints, or equivalently the
\(ts\)-provenance of the outward two-edge matching.  Another linear
combination of one-vertex traces cannot suffice.

This is a no-go for the stated contraction architecture, not for Krenn's
conjecture.  The witness (1) also changes the colour-zero pure coefficient
when \(ts\ne0\); an admissible anchored N=10 construction would need a
compensating source and must be audited separately.

## 1. Why reconstruction imposes one equation

For every old tensor \(X\), every old controller satisfies

\[
             P_a(X\otimes g_{89})=X,
             \qquad P_a(\Delta_{10,3})=\Delta_{8,3}.     \tag{4}
\]

Consequently

\[
 Q_\lambda(X\otimes g_{89})=left(\sum_a\lambda_a\right)X,
 \qquad
 Q_\lambda(\Delta_{10,3})=left(\sum_a\lambda_a\right)\Delta_{8,3}.
                                                                    \tag{5}
\]

Both exact reconstruction and target preservation give (2).  This does not
depend on the anchored N=8 source.

## 2. The common mixed row

The mixed full tensor of (1) contains

\[
 -e_{(0,0,0,0,0,0,1,2,0,0)}.                           \tag{6}
\]

For all three candidate cuts, the boundary word of (6) is \((0,1,2)\).
The five old insertion-shore colours and both new colours are all zero.
Therefore every possible old controller accepts the word and, after
stripping vertices 8 and 9, gives literally

\[
       P_a\bigl((H_{10}-\Delta_{10})_{012}^{[ts]}\bigr)
                    =-e_{00000}.                         \tag{7}
\]

The old N=8 insertion cylinders do not contain this row.  Exact normal forms
modulo their cofactor-column bases are

| cut | normal form of \(-e_{00000}\) |
|---:|---|
| 0 | \(e_{63}\) |
| 1 | \(e_{63}\) |
| 5 | \(e_{21}+e_{150}\) |

Applying (2) to (7) multiplies the displayed nonzero quotient class by
\(\sum_a\lambda_a\).  Containment forces (3), contradicting reconstruction
and target preservation.

## 3. Exact rank certificate

The checker converts every contracted nonconstant cofactor and residual
coefficient to its quotient normal form.  Each quotient coordinate is a
linear equation in the five controller weights.  The exact ranks are:

| cut | system | coefficient rank | augmented rank | result |
|---:|---|---:|---:|---|
| 0 | preserve + cofactors | 2 | 2 | feasible |
| 0 | preserve + residuals | 2 | 3 | inconsistent |
| 1 | preserve + cofactors | 2 | 2 | feasible |
| 1 | preserve + residuals | 2 | 3 | inconsistent |
| 5 | preserve + cofactors | 3 | 4 | inconsistent |
| 5 | preserve + residuals | 2 | 3 | inconsistent |

For cuts 0 and 1, the full-residual obstruction is essential: the linear and
quadratic cofactor images alone admit scalar multitraces.  On cut 5, both
the quadratic old-hole cofactor and the mixed residual independently block
the repair.

These are symbolic coefficient equations over \(\mathbb Q[t,s]\), not a
weight grid.  The four coefficient corners used by the preceding checker
recover the multiaffine coefficients exactly.

## 4. Why a plain direct sum still fails

Let

\[
                 F_z=(P_a)_{a\in U_z}.                   \tag{8}
\]

Equation (4) says that every forced-lift row has diagonal image

\[
                  F_z(X\otimes g)=(X,X,X,X,X).           \tag{9}

The fatal row (7) has exactly the same form:

\[
                  F_z(q)=(-e_0,-e_0,-e_0,-e_0,-e_0).    \tag{10}

Suppose a coupled direct-sum cylinder \(M_z\) contains the contracted cross
directions and has a reconstruction map \(R_z\) satisfying

\[
 R_z(X,X,X,X,X)=X,
 \qquad R_z(M_z)\subseteq{\cal S}^{(8)}_z.               \tag{11}

Then (10)--(11) force \(-e_0\in{\cal S}^{(8)}_z\), contrary to the exact
normal forms above.  This rules out not only scalar recombination but any
direct-sum repair whose recovery is the identity on all diagonal old-row
data.

The hypothesis in (11) is the load-bearing scope.  A construction which
does not reconstruct arbitrary old rows, or which carries an additional
source-provenance grading, is not ruled out.

## 5. The next required datum

A viable repair has to distinguish two occurrences of the same tensor row:

1. a row inherited from \(X\otimes g_{89}\); and
2. the same row created at coefficient degree \(ts\) by the ordered outward
   pair \((0,8),(1,9)\).

No output-linear trace can make that distinction.  The smallest extra datum
is a two-endpoint provenance component indexed by

\[
             ((v,8;\alpha,\beta),(w,9;\gamma,\delta)),   \tag{12}
\]

or its symmetry quotient.  It should record the six-site cofactor on the
remaining old vertices before summing it into the ordinary output tensor.
The next bounded test is therefore a source-graded four-point contraction:
keep the ordinary forced-lift component and the ordered cross-pair
coefficient in separate summands, and ask whether the four simultaneous
cylinder equations eliminate the second summand.  Without such a grading,
the N=8-to-N=10 lane is stopped.

## Reproduction

    python3 computations/verify_n10_two_cross_edge_multitrace_repair.py
    python3 -O computations/verify_n10_two_cross_edge_multitrace_repair.py
    python3 -I computations/verify_n10_two_cross_edge_multitrace_repair.py
    python3 -S computations/verify_n10_two_cross_edge_multitrace_repair.py

All ranks, quotient normal forms, and coefficient identities are computed
over the rationals.
