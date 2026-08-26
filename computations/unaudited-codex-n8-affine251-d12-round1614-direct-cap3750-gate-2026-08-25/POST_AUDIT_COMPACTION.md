# Post-audit compaction at round 1614

Status: PASS

Independent cap audit `9c03838c5adf159f6cbfcbfb74c9e200b03489da2130c5a4af429060ac9ef4a7` and manifest `f36c4f7ab37e3347b3f289a2f6c4ead2ee3f14f112405d785b5efafdeef9cd05` sealed PASS before this operation.

Exactly four superseded payloads were removed:

- `control_cap3500/checkpoint.bin` (`4c84bb8978083a0b2437bcc10730b40fc260fce90068f597c408789546c7f76e`)
- `control_cap3500/vectors.bin` (`ab1da9e006abd643b977fe1af879c9f7c7ee99b80be95ac82fcb71c9a960d88d`)
- `../unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1601_cap3500_to1613/stage11_cap1613/checkpoint.bin` (`4bd2b4d8f854e1cedc147f9824b876d3c7d4715e42bbde0cf0112a1bd666b2ac`)
- `../unaudited-codex-n8-affine251-d12-hierarchical-v4-rare-index-2026-08-25/production_from_round1601_cap3500_to1613/stage11_cap1613/vectors.bin` (`3defad7e9dba3495e1ecdb0f40f0148b1dbe0d79a6f34452db205dcd6a88ec16`)

All small evidence and the accepted candidate were retained. Candidate revalidation passed:

- checkpoint `4c84bb8978083a0b2437bcc10730b40fc260fce90068f597c408789546c7f76e`
- cache `ab1da9e006abd643b977fe1af879c9f7c7ee99b80be95ac82fcb71c9a960d88d`

Free space increased from125,757,592 KiB to139,879,504 KiB.
