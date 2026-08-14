# One strict common four-cut homotopy kills the whole moment tower

## Outcome

The all-order rootless moment problem has a shorter positive target than a
separate construction of every weighted lift.

Let the two endpoint-ordered physical curvature factors be

\[
 K^\rightarrow=q-x,
 \qquad K^\leftarrow=q-r+x.
\]

Suppose their nullhomotopies have been descended into one source-labelled
augmented differential module, with legal multiplication by the literal
cycles \(q,r\):

\[
 d\Gamma^\rightarrow=K^\rightarrow,
 \qquad d\Gamma^\leftarrow=K^\leftarrow,
 \qquad dq=dr=0.
\]

Then

\[
 \Gamma=-(\Gamma^\rightarrow+\Gamma^\leftarrow)
 \quad\Longrightarrow\quad
 d\Gamma=r-2q.                                      \tag{1}
\]

For every \(h\ge3\) and every \(s\ge0\), put

\[
 H_s=\int_0^1t^s(q+tr)^{[h-2]},dt,
 \qquad c_s=(r-2q)H_s.
\]

The strict Leibniz rule now gives the explicit simultaneous filling

\[
 \boxed{\quad d(\Gamma H_s)=c_s\quad\text{for every }s.\quad}   \tag{2}
\]

Thus one physical \(\Gamma\) supplies the entire Hilbert--Cauchy tower,
including \(c_0\), the first weighted class \(c_1\), and the prefix through
\(c_{h-3}\) used by the all-order scalar-unit calculation.  The companion
checker verifies the divided-power coefficients through \(h=24\) and the
rank-\(h\) carrier hyperplane at every order.

This is a reduction, not a construction of \(\Gamma\).  Its value is to
separate the genuinely geometric theorem from the moment bookkeeping:

> **Strict common-four-cut homotopy theorem (open).**  Descend the two
> oriented four-cut cells to a single complete physical module so that their
> sum is a source-valid \(k[q,r]\)-linear homotopy with boundary \(r-2q\).

If this theorem is proved, no independent weighted-moment comparison is
needed on the scalar-unit branch.

## Why this removes the based-loop ambiguity

The based-loop obstruction arises when a top-suspended response path is
desuspended through a noncanonical comparison.  Two lifts can then differ
by \(z\,d(t(1-t))\), which fixes endpoints and the unweighted integral but
changes the first weighted integral by \(-z/6\).

Equation (2) takes a different route.  It constructs a boundary directly in
the lower physical module.  No choice of horizontal lift is made: use the
single chain element \(\Gamma\) and multiply it by the literal polynomial
\(H_s(q,r)\).  A different choice of \(\Gamma\) may differ by a cycle, but
each choice still exhibits \(c_s\) as a boundary.  Hence existence of one
strict common \(\Gamma\) is stronger than zero-indeterminacy for a
transferred first moment and makes the latter unnecessary for vanishing.

This observation does not contradict the pinned based-loop countermodels.
They grant coefficient projectors, restriction/insertion maps, or an
unweighted carrier while withholding exactly the strict common chain
element (1).

## Exact relation to the two existing open gates

The same missing descent controls both the local and uniform frontiers.

1. The centered-occurrence/Gate-II construction is trying to put the two
   endpoint orientations, the primitive cap, target, ordinary residue,
   physical \(q\), and shifted ridge in one augmented source object.
2. The rootless Hilbert--Cauchy construction needs the resulting common
   object to be a module over the clean parameters \(q,r\).
3. Once both statements hold, (1)--(2) convert the local comparison into all
   moment relations.  The certified moment-span theorem then eliminates the
   exceptional clean coordinate.

The source provenance is load-bearing.  Having
\(d\Gamma^\rightarrow=q-x\) and
\(d\Gamma^\leftarrow=q-r+x\) in two unrelated restriction complexes does
not allow their sum.  Coefficient equality between those restrictions is
also insufficient.  One needs a common mapping-cylinder/Čech descent that
preserves word, fine, repeated, target, anchor, terminal, residue, physical
\(q\), and ridge labels, followed by a genuine module action of \(q,r\).

The exact overlap/Bianchi identities are the natural descent data, but their
homogeneous overlap complex has a common-factor Koszul kernel.  Therefore
flatness alone does not construct (1).  The remaining proof must either:

- use the complete mixed-target/four-cut rows to kill that kernel and glue
  the two oriented cells; or
- extend a nonzero overlap class to the already accepted physical
  terminal/active-clean alternative.

This is now the shortest uniform source theorem on the moment side.

## Verification

Run

```sh
python3 computations/verify_uniform_strict_four_cut_homotopy_moment_collapse.py
python3 -O computations/verify_uniform_strict_four_cut_homotopy_moment_collapse.py
python3 -I -S computations/verify_uniform_strict_four_cut_homotopy_moment_collapse.py
```

The checker audits the oriented sign in (1), every divided-power boundary
in (2), the exact \(h=3\) value

\[
 c_1=-2q^{[2]}-\frac16qr+\frac23r^{[2]},
\]

and the rank of the full prescribed initial moment prefix.
