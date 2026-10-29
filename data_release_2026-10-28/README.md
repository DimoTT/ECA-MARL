# ECA-MARL supporting materials

## Scope and status

This collection accompanies *Decentralized Multi-Agent Reinforcement Learning
with Bounded Off-Policy Guarantees for Edge Collaboration in Software-Defined
Wireless Sensor Networks*.

This is a **partial supporting-materials collection**, prepared from files
available in the manuscript working directory on 2026-10-28. It contains the
current figure files, the values reported in Table 1, and documentation of the
reported experimental environment. It is **not** a raw simulation dataset or an
executable implementation of ECA-MARL.

Original numerical results, individual simulation runs, training logs,
configuration files, and experiment code are not included. The author reports
that other materials are on another computer; those materials were outside the
scope of this collection. No missing results were fabricated, reconstructed
from curves, interpolated, or regenerated.

## Contents

| Path | Contents |
| --- | --- |
| `figures/Fig1.pdf` to `figures/Fig4.pdf` | Current, author-supplied schematic figures |
| `figures/Fig5.pdf` to `figures/Fig14.pdf` | Existing PDF display copies of the result plots |
| `figures/eps/Fig5.eps` to `figures/eps/Fig14.eps` | Original result-plot EPS files used by the manuscript |
| `tables/table1_simulation_parameters.csv` | All 12 parameter/value pairs transcribed from Table 1 |
| `metadata/figure_manifest.csv` | Figure captions, file mapping, provenance, and numerical-data status |
| `metadata/simulation_environment.json` | Environment and evaluation protocol reported in the manuscript |
| `metadata/dataset_metadata.json` | Descriptive metadata and unresolved repository/licence fields |
| `metadata/materials_not_included.csv` | Explicit boundaries of this collection |
| `metadata/data_dictionary.csv` | Definitions of the CSV columns and missing-value convention |
| `documentation/reported_setup.tex` | Verbatim experimental setup and Table 1 excerpt |
| `documentation/data_availability_note.txt` | Status and instructions for the future availability statement |
| `scripts/verify_release.py` | Offline integrity and basic consistency checks; Python standard library only |
| `SHA256SUMS.txt` | SHA-256 checksums for every other file in this collection |

## Provenance and transformations

Figure files were copied without editing or resampling. The PDF copies for
Figures 5-14 already existed in the working directory; they are display
derivatives, not numerical data tables. The EPS files remain the manuscript
inputs for these figures. Checksums for the source and display files appear in
`metadata/figure_manifest.csv`.

The author confirmed that the current Figures 1-4 were manually drawn in
Microsoft Visio, without generative-AI assistance in their figure content. This
statement applies to the current PDF versions, not earlier schematic drafts.
Older local Visio files were excluded because correspondence to the current
figures has not been established. Neither the historical figure-generation
script nor manuscript-editing utilities are experiment implementations, and
they are not included here.

The parameter CSV preserves the manuscript's reported values and unit strings
verbatim. No unit corrections or conversions were inferred. In particular,
the task-computation unit `Gcycle/s`, batch-size unit `MB`, and replay-pool unit
`GB` should not be silently interpreted as different units or sample counts.
The manuscript's use of `10MB` in its computation-sweep description is also
retained as reported, rather than resolved by assumption.

Unknown software versions, run counts, random seeds, and repository identifiers
are represented by JSON `null`, not guessed values. Blank CSV fields mean
not provided or not applicable as described by the corresponding status field;
they never stand for a measured zero.

## Verification

Run from this directory with Python 3:

```text
python scripts/verify_release.py
```

The check verifies checksums, the 14-figure mapping, and exact transcription of
the 12 Table 1 rows. It does not execute simulations or verify experimental
findings. Do not change files without refreshing the checksum manifest.

## Public deposit and citation

No repository record, public URL, DOI, licence, or publication year has been
assigned by this preparation step. Before public release, the authors must
confirm redistribution rights and choose the licence in the repository record.
The authors may deposit this collection as **supporting materials**, accurately
describing its limited scope. It must not be described as all raw data, all
numerical data underlying Figures 5-14, or a complete reproducibility package.

Once a public record exists, use the actual repository-issued citation and
persistent identifier. The manuscript's final Data Availability statement must
describe what that record really contains. Do not insert a placeholder DOI or
claim that absent numerical results have been deposited.
