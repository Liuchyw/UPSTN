# UPSTCN supplementary experimental results

Supporting material for *Auxiliary Supervision in Graph Traffic Forecasting: A Controlled Study of Utility and Loss Effects*.

This repository contains the supplementary tables reproduced in the response letter but not displayed as tables in the main manuscript. Table numbers match the revised supplementary material. It does not contain reviewer reports or the response letter.

## Appendix

- [Complete supplementary results PDF](appendix/supplementary_results.pdf)
- [Complete supplementary LaTeX source](appendix/supplementary_results.tex)
- [Table index and captions](appendix/table_index.json)

| Table | Contents | Files |
| --- | --- | --- |
| Table S2 | JiNan paired effects and seed-level uncertainty | [PDF](appendix/tables/Table_S2.pdf) / [PNG](appendix/tables/Table_S2.png) / [TeX](appendix/tables/Table_S2.tex) |
| Table S4 | METR-LA metrics for matched alignment-on/off models | [PDF](appendix/tables/Table_S4.pdf) / [PNG](appendix/tables/Table_S4.png) / [TeX](appendix/tables/Table_S4.tex) |
| Table S5 | METR-LA paired effect summaries | [PDF](appendix/tables/Table_S5.pdf) / [PNG](appendix/tables/Table_S5.png) / [TeX](appendix/tables/Table_S5.tex) |
| Table S6 | Checkpoint gradient direction and magnitude summaries | [PDF](appendix/tables/Table_S6.pdf) / [PNG](appendix/tables/Table_S6.png) / [TeX](appendix/tables/Table_S6.tex) |
| Table S7 | Representation variance and effective rank summaries | [PDF](appendix/tables/Table_S7.pdf) / [PNG](appendix/tables/Table_S7.png) / [TeX](appendix/tables/Table_S7.tex) |
| Table S8 | Relative view distance and forecasting-error associations | [PDF](appendix/tables/Table_S8.pdf) / [PNG](appendix/tables/Table_S8.png) / [TeX](appendix/tables/Table_S8.tex) |
| Table S9 (panel a) | Benchmark training settings | [PDF](appendix/tables/Table_S9_panel_a.pdf) / [PNG](appendix/tables/Table_S9_panel_a.png) / [TeX](appendix/tables/Table_S9_panel_a.tex) |
| Table S9 (panel b) | Joint-model benchmark results | [PDF](appendix/tables/Table_S9_panel_b.pdf) / [PNG](appendix/tables/Table_S9_panel_b.png) / [TeX](appendix/tables/Table_S9_panel_b.tex) |
| Table S10 | DIM checkpoint discrimination and representation diagnostics | [PDF](appendix/tables/Table_S10.pdf) / [PNG](appendix/tables/Table_S10.png) / [TeX](appendix/tables/Table_S10.tex) |

The full appendix also retains Tables S1 and S3 as run-inventory and weight-sensitivity context. These two tables are not separate image occurrences in the response letter. Figures 1-4 and Tables 1-6 are already in the main manuscript and are not duplicated here. The audit found no additional response-only experimental figures.

## Source data and interpretation

Numeric CSV files are in [source_data](source_data/README.md). Table PNG files are byte-identical to those embedded in the current response Word document. Individual table PDFs retain the corresponding vector artwork and complete outer rules. The table-only TeX fragments use the packages and `revisionblue` definition listed in the source-data README.

Training seeds, not diagnostic batches, are the independent units in paired training comparisons. Five probe batches are nested within each seed. JiNan all-entry normalized metrics and original-scale validity-masked metrics are distinct. Public physical speed errors are in mph, and MAPE is in percent. The paired uncertainty intervals and mixed-hardware qualifications are retained as reported; they are not a claim of multiplicity-adjusted significance. Consult the complete appendix for exact definitions and protocols.

## Access and scope

This repository is currently private. Uploading these files does not itself provide reviewer access, and this account-based URL is not anonymous. The supplementary PDF should also be submitted through the journal system unless a working review-access route is arranged.

Raw third-party traffic datasets, trained checkpoints, private server addresses, credentials, training caches and unrelated project files are not included. Absolute local/server path columns have been removed from CSV copies without changing their numeric fields. No new redistribution licence is assigned by this deposit.

## Integrity

`SHA256SUMS.txt` records the uploaded file hashes. This package was assembled on 4 November 2026 from the revised supplementary material and the current response-letter figures/tables. It records existing results and introduces no new experiments.
