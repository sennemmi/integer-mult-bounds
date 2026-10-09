#!/usr/bin/env python3
"""Pin every source and finite input that verify.py reads. Apache-2.0."""
from pathlib import Path
import hashlib
import json

PKG = Path(__file__).resolve().parent
REPO = PKG.parents[1]
FILES = ['scripts/paired_cube_producer.py', 'scripts/paired_cube_physical.py',
         'scripts/paired_cube_assembly.py', 'certificates/paired-cube-complex-input.json',
         'research/source-assisted/SOURCE.json',
         'research/source-assisted/decision/complex_frame_flow.py',
         'research/source-assisted/decision/exact_complex_flow_lift.py',
         'research/source-assisted/decision/certify_complex_flow_contract.py',
         'research/source-assisted/decision/source_aligned_local.py',
         'research/source-assisted/global/assemble_profiles.py',
         'research/source-assisted/global/FINITE_BRIDGE.txt',
         'research/source-assisted/global/COMMON_FRAME_LIFT_AND_GLOBAL_CONTRACT.txt',
         'research/source-assisted/bit/SOURCE_ALIGNED_BIT_WORD.txt',
         'research/source-assisted/bit/source_aligned_lifts.json',
         'research/source-assisted/bit/source_aligned_profile.json',
         'notes/source-assisted-note.tex',
         'research/paired-cube-twin-local-168/certificate.json',
         'research/paired-cube-twin-local-168/SOURCE.json',
         'research/paired-cube-twin-local-168/verify.py']
FILES += ['research/bit-leaf-bootstrap182/PROOF.md',
          'research/bit-leaf-bootstrap182/README.md',
          'research/bit-leaf-bootstrap182/NOTICE',
          'research/bit-leaf-bootstrap182/SOURCE.json',
          'research/bit-leaf-bootstrap182/certificate.json',
          'research/bit-leaf-bootstrap182/validation.json',
          'research/bit-leaf-bootstrap182/verify.py',
          'research/paired-cube-diagonal-bit-168-followup/README.md',
          'research/paired-cube-diagonal-bit-168-followup/PROOF.md',
          'research/paired-cube-diagonal-bit-168-followup/NOTICE',
          'research/paired-cube-diagonal-bit-168-followup/search.py',
          'research/paired-cube-diagonal-bit-168-followup/verify.py',
          'research/paired-cube-diagonal-bit-168-followup/pin_sources.py',
          'research/paired-cube-diagonal-bit-168-followup/frame-descent.json',
          'research/paired-cube-diagonal-bit-168-followup/SOURCE.json',
          'research/paired-cube-diagonal-bit-168-followup/certificate.json',
          'research/paired-cube-diagonal-bit-168-followup/frame-prime-witnesses.json.gz']
DIRECTORIES = ['scripts/paired_cube', 'references/paired-cube/sources', 'references/paired-cube/selected-module',
               'references/paired-cube/physical', 'references/three-stage-cover/pr117',
               'research/paired-cube-diagonal-bit-168']
OWN = ['README.md', 'PROOF.md', 'NOTICE', 'LEADERBOARD.md', 'verify.py', 'pin_sources.py', 'source_aligned_local_v4.py', 'assemble.py',
       'contract_v4.py', 'data/physical-pairs.json', 'data/kernel-pairs.json']


def main():
    names = set(FILES)
    for directory in DIRECTORIES:
        names.update(p.relative_to(REPO).as_posix() for p in (REPO / directory).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts)
    names.update((PKG / name).relative_to(REPO).as_posix() for name in OWN)
    files = {name: hashlib.sha256((REPO / name).read_bytes()).hexdigest()
             for name in sorted(names) if (REPO / name).is_file()}
    (PKG / 'SOURCE.json').write_text(json.dumps(dict(
        files=files,
        scope='Sources and finite inputs read by verify.py; certificate.json is derived.'),
        indent=2, sort_keys=True) + '\n')
    print(len(files), 'pins')


if __name__ == '__main__':
    main()
