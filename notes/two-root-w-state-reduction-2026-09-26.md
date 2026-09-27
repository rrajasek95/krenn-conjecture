# Two unrestricted roots reduce to one when the cofactor graph has an odd cycle

September 26, 2026. **Written theorem with exact supporting examples;
awaiting independent audit.**

[Guide](../explainers/BOUNDARY-STRUCTURE.md) ·
[Replay](../computations/boundary-structure-2026-09-26/README.md)

## 1. A larger architecture class with the same sharp optimum

Let \(n=2m\ge6\). Choose two root sites \(p,q\), and let \(D\) be the
scalar color-\(a\) source on the other \(n-2\) sites. All edges incident
to either root may have arbitrary complex endpoint-color entries. Define

\[
 C_{ij}=\operatorname{haf}(D\setminus\{i,j\})\quad(i\ne j),
 \qquad C_{ii}=0.
\]

The **cofactor graph** has an edge \(ij\) exactly when \(C_{ij}\ne0\).
Assume this graph is connected and contains an odd cycle.

**Theorem.** Every exact nonzero uniform W-state source in this class can
be changed into a one-root source by deleting source cells whose total
contribution to the output is zero. Output is preserved and source norm
cannot increase. Consequently the exact optimum over this two-root class is

\[
 \boxed{R_{\max}=\frac{n B_n}{(n-1)^2+1},\qquad
 B_n=\frac{((n-1)!!)^2}{\binom{n}{2}^{m}}.}
\]

At six sites it is \(1/65\). A complete equal-weight core and the previous
one-root construction attain it, so this is an attained optimum over the
larger class. The cofactor matrix itself may be singular: invertibility is
not an assumption.

## 2. The graph cancellation lemma

Suppose a connected graph contains an odd cycle, and complex numbers
\(u_i,v_i\) satisfy

\[
 u_iv_j+u_jv_i=0\quad(ij\text{ an edge}),\qquad
                         (u_i,v_i)\ne(0,0)\quad\text{for all }i.
\]

Then one vector is identically zero and the other is nonzero at every vertex.

If \(u_i\ne0,v_i=0\) anywhere, the edge equations force the same type at
every neighbor, and connectedness propagates it to the whole graph. The
opposite case is symmetric. If neither type occurs, all entries of both
vectors are nonzero. The ratios \(v_i/u_i\) then change sign on every
edge. An odd cycle forces a ratio to equal its negative, a contradiction
over \(\mathbb C\). This proves the lemma.

The related linear statement will also be used: if every \(u_i\ne0\) and
\(u_iw_j+u_jw_i=0\) on such a graph, then \(w=0\).

## 3. The target forces one root to stop exciting the core

Let
\(u_i=A_{pi}(a,b)\) and \(v_i=A_{qi}(a,b)\).
The output with core excitations at \(i,j\) and both roots in color \(a\)
is

\[
                         C_{ij}(u_iv_j+u_jv_i).
\]

It must vanish. Meanwhile, the desired nonzero output with only core site
\(i\) excited can only arise through one of these two cells, so
\((u_i,v_i)\ne(0,0)\). The graph lemma applies. Exchange root names if
necessary so that \(v=0\) and all \(u_i\ne0\).

Now fix any color \(h\) at root \(q\). Two core \(b\) excitations give

\[
 C_{ij}\bigl(u_i A_{qj}(h,b)+u_j A_{qi}(h,b)\bigr)=0.
\]

The linear version of the graph lemma forces \(A_{qi}(h,b)=0\) for all
\(i,h\). For any other non-ground core color \(c\), the output with
\(b\) at \(i\) and \(c\) at \(j\) reduces to
\(C_{ij}u_i A_{qj}(h,c)=0\), because the exchanged term contains the
already zero \(A_{qi}(h,b)\). Every vertex has a neighbor, so
\(A_{qj}(h,c)=0\) as well.

Thus every surviving edge from \(q\) to the core has color \(a\) at its
core endpoint. Root \(q\) itself could still have a non-ground color.

## 4. Remaining non-ground root entries are invisible

For \(h\ne a\), set \(x_i=A_{qi}(h,a)\). The output with core site
\(i\) in color \(b\), root \(p\) in \(a\), and root \(q\) in \(h\)
must vanish. It is \(u_i(Cx)_i\), so

\[
                              Cx=0.
\]

Delete all such \(x\)'s. This preserves the *entire* output tensor:
terms using a deleted entry and an edge from \(p\) to another core site
sum to a row of \(Cx\), multiplied by that incident entry. They vanish
for every color at \(p\) and its neighbor. Terms using the direct edge
\(pq\) do not use any deleted entry. No matching can contain two deleted
entries, since they share root \(q\).

After deletion, every edge not incident to \(p\) is purely \(aa\).
The source is now in the earlier one-root architecture. Since deletion
reduces the sum of squared cell magnitudes, the
[one-root W theorem](w-state-optimal-design-2026-09-26.md) proves the upper
bound. Its complete-core construction satisfies the cofactor graph hypothesis
and proves attainment.

This argument also preserves a weighted W target when every retained-core
excitation amplitude is nonzero. The appropriate earlier weighted-target
bounds then apply. Uniform W is the case with a sharp architecture-wide
constant displayed in §1.

## 5. Why the graph hypothesis matters

On a connected bipartite cofactor graph, both excitation vectors can be
nonzero: take \(u_i=1\) everywhere and \(v_i=1\) on one part,
\(v_i=-1\) on the other. Every two-excitation coefficient still cancels.
There is no odd-cycle contradiction.

The package contains a complete exact six-site W construction of this kind.
The four-site scalar core is \(K_{2,2}\); both roots have nonzero excitation
cells. Its normalized rate is \(48/4913\), below \(1/65\). It demonstrates
that the cancellation branch is real, not that it beats the existing optimum.
Optimality for general bipartite or disconnected cofactor graphs remains open.

Another example has a complete cofactor support graph but a rank-three
cofactor matrix. It includes eight units of squared source norm in complex
kernel entries. The checker removes them and verifies that all 729 ternary
output coefficients are unchanged. This tests why the theorem uses the
support graph rather than requiring an invertible matrix.
