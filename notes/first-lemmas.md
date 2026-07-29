# First rigorous lemmas

## Aggregation lemma

For each unordered pair `u<v` of vertices of `B`, define the matrix

\[
X_{uv}(i,j)=\sum_{a:\,N(a)=\{u,v\},\ k(a,u)=i,\ k(a,v)=j}w(a).
\]

Expanding a perfect matching one pair at a time shows that the coefficient
tensor of the original decorated multigraph is exactly

\[
H_n(X)=\sum_{M\text{ perfect}}\bigotimes_{uv\in M}X_{uv}.
\]

This retains endpoint order and all cancellation among parallel sources with
the same endpoint-color pair.  It does not justify deleting palette colors:
every original palette color still has a required constant coefficient one.

## Four-vertex upper bound

For four vertices,

\[
H_4=X_{12}\otimes X_{34}+X_{13}\otimes X_{24}
     +X_{14}\otimes X_{23}.
\]

Each summand has partition rank one (under its displayed bipartition), hence
`prank(H_4)<=3`.  The diagonal tensor
`D_{4,q}=sum_i e_i tensor e_i tensor e_i tensor e_i` has partition rank `q`
over every field; this is the diagonal partition-rank lemma.  Therefore an
exact monochromatic representation has `q<=3`.  The K4 one-factorization
attains three.

The final proof should include a self-contained proof of the diagonal
partition-rank lemma rather than relying only on a citation.

## Exact six-vertex border degeneration

Let the vertices be `0,...,5` and take the three perfect matchings

\[
M_0=\{04,12,35\},\quad M_1=\{05,14,23\},\quad
M_2=\{03,15,24\}.
\]

Their union is the triangular prism and has exactly one further perfect
matching `R={04,15,23}`.  Put a diagonal color-`i` entry on every edge of
`M_i`, all other entries zero.  Choose the three products along each `M_i` to
be one, while assigning weights `t,1,t^{-1}` on `04,12,35` and unit weights
on the other two matchings.  Then exactly

\[
H_6(X(t))=D_{6,3}+t\,e_0^{(0)}e_2^{(1)}e_1^{(2)}
 e_1^{(3)}e_0^{(4)}e_2^{(5)}.
\]

Thus `D_{6,3}` lies in the Euclidean and Zariski closure of the parameterized
hafnian image although this family has no finite value at `t=0`.  Consequently
no polynomial identity in the output tensor alone can prove the desired
non-representability.  Any successful upper-bound proof must use a
finite-versus-border argument, a conditional/rational invariant, or direct
parameter structure.
