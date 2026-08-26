# Advanced D11 triangle resume design

`PASS_READY_TO_SEAL`: this sibling resumes only the independently replayed 230,091-column / 80,922-support p=1073741827 triangle checkpoint. It preserves the provider, arithmetic, checkpoint logic, safe dual-before-selected persistence, and 500,000-column cap. The only engine-source change from the sealed 16-GiB resume is the native wall guard from 350 to 590 seconds; the watchdog changes only to 20 GiB / 600 seconds and a distinct schema.

The prior run reached 15,308,688 KiB at 360.177739 seconds and had already persisted its useful checkpoint. A linear diagnostic extrapolation reaches 20 GiB near 493.5 seconds, leaving about 96.5 seconds before the new native wall. Resume pivot geometry can be nonlinear, so this is not a terminality projection, but the evidence does not project a 20-GiB breach before useful persistence; the bounded launch is accepted.

The sealed input is owned by this package before launch. Any future output pair is atomically written dual first and revalidated on resume. No second prime, other branch, or D12 path exists in the launcher.
