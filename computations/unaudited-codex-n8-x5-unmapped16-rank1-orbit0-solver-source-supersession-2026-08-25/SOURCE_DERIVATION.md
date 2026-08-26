# Rank-one orbit-zero solver-source supersession

The superseded diagnostic source is copied byte-for-byte from pinned Q input SHA `1d9875cab81417094d51193862f40097b1c03e4816aedd8ceaf07a917eeb248b`. Its final count-only `quit` epilogue is replaced exactly once by the standard `slimgb(I)`, basis-size, `reduce(1,G)`, remainder, and unit/nonunit status epilogue. The p=32,003 source is then derived from that solver-ready Q source by replacing its unique `ring r=0,` token with `ring r=32003,`.

No ideal generator, variable, monomial order, or chart datum is changed. Neither source is launched by this package.
