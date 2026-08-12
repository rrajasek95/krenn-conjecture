# The shifted chart-H1 candidate has a complete derived target filler but no source comparison filler

## Outcome

The unique candidate isolated in `f872900` can be completed one step further,
and the completion separates two logically different attaching problems.

Let \(F_0=H_0-u\), let \(u_v,t\) be the two marked endpoint directions,
and let \(h_v=\partial_{u_v}\partial_tH_m\).  In the squarefree
two-direction Hasse presentation, the complete source-labelled chain is

\[
\begin{split}
s_{ut}={}&H_m r_0[ut]
 +(\partial_{u_v}H_m)r_0[t]
 +(\partial_tH_m)r_0[u_v]\\
&+h_vr_0[\varnothing]-F_0r_m[ut].
\end{split}                                                   \tag{1}
\]

The Hasse differential gives \(ds_{ut}=0\).  Therefore

\[
                n_v=s_{ut}-h_vT                         \tag{2}
\]

satisfies, exactly,

\[
 d_{tot}n_v=h_vYw,
 \qquad tgt(n_v)=ores(n_v)=0.                           \tag{3}
\]

Here \(Yw\) is the committed normalized cap-row representation of the
pure-output reset \(Y_0\).  Thus the target-side equation required by
`f872900`, \(dn_v=h_vY_0\), has a genuine source-labelled solution in the
**prolonged Hasse presentation**.  It is not a declared cap column: (1)
lists all five row terms, including the four compulsory proper-face
companions.

The chart sign is also exact.  The oppositely oriented strict chart cycle
has marked tail

\[
     -S_v=-(h_v)_{pq,direct}+(h_v)_{pr,two-star},       \tag{4}
\]

terminal value \(-1\), target zero, and ordinary residue zero.  This is the
unique primitive both-chart placement from `f872900`.

What is still absent is the source comparison cell \(b_v\) with

\[
                            db_v=k_v.                   \tag{5}
\]

The strict chart difference in (4) is a closed cycle; it is not a
Čech/overlap two-cell whose boundary is the primitive chart kernel.  The
complete first fine-degree census still has \(k_v\) as correction \(H_1\),
and the Hasse prolongation adds row-face copies, not the higher comparison
differential (5).  Therefore (3)--(4) do not yet kill the chart class in the
physical source.

## The four companions are load-bearing

If one keeps only the tempting diagonal term

\[
                         h_v(r_0-T),                    \tag{6}
\]

then its old differential is

\[
 d(6)=h_vF_0e_{Eq}+h_vYw.                              \tag{7}
\]

The other four terms of (1) have boundary

\[
                       -h_vF_0e_{Eq},                   \tag{8}
\]

and (8) is precisely what turns (7) into (3).  Hence the selected diagonal
term is not a chain by itself; the complete Boolean face system is
mandatory.

Adding the two internal matching directions gives the committed
four-direction totalization.  Its \(q\)-zero top is \(r_0-T\), while its
diagonal projection to the underived source has

\[
             [d,pi_{top}](r_0-T)=F_0e_{Eq}
                              =(H_0-u)e_{Eq}.            \tag{9}
\]

The checker reconstructs (9) for all five deleted sites and all three
internal matchings.  Equation (9), not a sign or a missing polynomial face,
is the first primitive physical-descent residual.

## Fine degree and provenance

The degree alignment remains the unique one proved in `f872900`:

\[
 sigma=e_{x,0}+e_{p,0}+e_{q,0},
 \qquad deg(h_vY_0)+sigma=lambda_v.                    \tag{10}
\]

Equations (1)--(3) show what the aligned denominator face must bring with
it.  Equation (4) fixes its chart orientation.  They do not turn the module
shift into a physical overlap generator: the missing datum is still (5),
or equivalently a comparison from the prolonged Hasse presentation to the
actual source resolution that sends the closed chart cycle to a boundary
without reintroducing (9), target, or old residue.

Thus the exact verdict is:

- **positive:** the derived target filler \(n_v\), all its companions,
  target/ores zero, and the required \(-S_v\) terminal sign;
- **negative at the current source stage:** no constructed \(b_v\) with
  \(db_v=k_v\); and
- **first residual under physical diagonal projection:**
  \((H_0-u)e_{\rm Eq}\).

This is an \(h=3\), direct-free, selected-fine-degree statement.  It does
not claim that the prolonged presentation descends to the physical source,
and it does not prove Krenn's conjecture.

## Verification

Run

```text
python3 computations/verify_h3_shifted_chart_h1_candidate_complete_differential.py
python3 -O computations/verify_h3_shifted_chart_h1_candidate_complete_differential.py
python3 -I -S computations/verify_h3_shifted_chart_h1_candidate_complete_differential.py
```

The checker pins `f872900` and the full Hasse/Koszul/cap totalization.  It
reconstructs (1)--(3) for all five faces, the four companion boundaries,
the unique chart placement (4), and the fifteen instances of (9).  Its
frozen ledger digest is

```text
82445db6604e473d0957e42e484f4496a7c9b31d16c4da7ba918dbcd780c4502
```
