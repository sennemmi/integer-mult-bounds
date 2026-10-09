# PR200 bit frame descent follow-up

This package applies the endpoint-frame descent used in PR198 to the stronger
PR200 bit word at exact head
`a1175449f34d39ff933d9d8ab23ced1f32b290ec`. It does not alter PR200's frozen
word, frames, terminal sinks, or source manifest. The 112 selected operation
frames and their exact basis rows are an overlay in `frame-descent.json`.

The search scans 41,288 operations, finds 2,596 structurally feasible frame
lowerings, and deterministically selects 112 nonconflicting moves on the actual
physical role chains. Floating point scores only rank proposals. The frozen
batch is independently checked using exact frame inclusion, physical-chain
nesting, terminal sink chronology, complete F2 and integer-column replay,
exact rational moment bounds, and exact prime witnesses for every used frame.

The PR200 bit coarse saving rises from
`677773948354561/10^18` to `677840450131861/10^18`. With PR184 pricing and the
depth-2 finite ordinary-leaf wrapper credited to PR185/PR199, the composed
conditional exponent rises from PR199's `1693287/2500000000` to
`1693453/2500000000`. This is also strictly above open PR204's exact
`1693287/2500000000`. Both public compositions reuse PR200's published bit
certificate without rebuilding the word; this follow-up adds a separately
replayed physical frame overlay. This is a finite conditional candidate, not an
unconditional theorem or a global-optimality claim.

## Reproduce

From the repository root, regenerate the deterministic search receipt and
replay the frozen physical witness:

```sh
python3 -B research/paired-cube-diagonal-bit-168-followup/search.py
python3 -B research/paired-cube-diagonal-bit-168-followup/verify.py
make verify-source-assisted-v4
```

The first command rewrites `frame-descent.json`; the make target repeats it and
CI requires that regeneration to leave the frozen receipt unchanged. The
verifier checks it against
the pinned PR200 source tree, compares the exact rank histogram delta and
terminal profile, and compares the canonical certificate and compressed prime
witnesses. The source-assisted v4 target then independently rebuilds the
complex supplier and checks the final 47 assembly constraints and seven
positive margins.

See `PROOF.md` for the exact deltas and the remaining proof dependencies.
