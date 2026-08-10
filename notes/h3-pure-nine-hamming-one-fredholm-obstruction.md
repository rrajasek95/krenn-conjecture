# A five-row Fredholm obstruction kills the nonclean pure-nine family

## Outcome

The integral pure-nine packet of
[`h3-pure-nine-rank-two-hafnian-update-boundary.md`](h3-pure-nine-rank-two-hafnian-update-boundary.md)
has good shared stars, satisfies all 27 pure coefficients, and has selected
clean tail \(\chi_2=-28\).  Freeze those three pure \(q\)-slices and the
endpoint stars, but allow all 90 ordered cross-colour cells on the 15
physical \(q\)-blocks to vary freely.

Write \(F_{ij}(w)\) for the full-nine residual in row \((i,j)\) and word
\(w\).  Direct expansion gives the source-faithful identity

\[
\begin{split}
 &F_{02}(002000)+F_{10}(002000)-F_{01}(020000)\\
 &\hspace{22mm}-F_{02}(020000)-F_{00}(022222)=-1. \tag{1}
\end{split}
\]

Every coefficient of every one of the 90 free cross-colour \(q\)-cells
cancels in (1).  Thus the pure packet cannot be completed even through the
Hamming-one full-nine equations.  The certificate has support five; it is
the exact left-Fredholm obstruction in the 209-by-90 affine Hamming-one
system, whose coefficient rank is 86.

The colour-2 second star in the original packet has the rational parameter
\(t\), with entries \(s_{2,4}^{1}=t\) and
\(s_{2,5}^{1}=-3-t\).  Both sides of (1) are affine in \(t\), and the exact
checker verifies (1) at \(t=0,1\); hence it holds in \(\mathbf Q[t]\).
The fixed rows \(0,1,2\) of that star have determinant one, so goodness is
uniform in \(t\).  The corresponding selected tail is

\[
             \chi_2(t)=-16t^2-48t-28,
\]

which is nonzero for every rational \(t\).

## Scope

This is a genuine all-cross-cell exclusion, not a support census: no
cross-colour support or coefficient was restricted.  It removes the sharp
known pure-nine nonclean family as a candidate full-row counterexample.

It does **not** prove the general tangent-or-clean implication
\(\chi_c=0\).  The Fredholm weights in (1) use this packet's fixed pure
slices and stars.  A general theorem still needs either a universal
weighted Hamming-two syzygy or a proof that every nonzero-tail pure packet
specializes to an obstruction of this type.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_pure_packet_hamming_one_fredholm_obstruction.py
```

The checker expands the literal hafnian/full-nine rows, verifies every
cross-cell coefficient cancels, verifies the remaining unit, and checks
the affine parameter family and the fixed good-star minor exactly over
\(\mathbf Q\).
