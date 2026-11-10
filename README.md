# UPSTCN supplementary experimental results

Supporting material for *Auxiliary Supervision in Graph Traffic Forecasting: A Controlled Study of Utility and Loss Effects*.

This repository contains the supplementary tables reproduced in the response letter but not displayed as tables in the main manuscript. Table numbers match the revised supplementary material. It does not contain reviewer reports or the response letter.

## Appendix

- [Complete supplementary results PDF](appendix/supplementary_results.pdf)
- [Complete supplementary LaTeX source](appendix/supplementary_results.tex)
- [Table index and captions](appendix/table_index.json)

| Table | Contents | Files |
| --- | --- | --- |
| Table S1 (excerpt) | JiNan delayed-activation Prototype/Joint comparison | [PDF](appendix/tables/Table_S1_delayed_activation.pdf) / [PNG](appendix/tables/Table_S1_delayed_activation.png) / [TeX](appendix/tables/Table_S1_delayed_activation.tex) |
| Table S2 | JiNan paired effects and seed-level uncertainty | [PDF](appendix/tables/Table_S2.pdf) / [PNG](appendix/tables/Table_S2.png) / [TeX](appendix/tables/Table_S2.tex) |
| Table S4 | METR-LA metrics for matched alignment-on/off models | [PDF](appendix/tables/Table_S4.pdf) / [PNG](appendix/tables/Table_S4.png) / [TeX](appendix/tables/Table_S4.tex) |
| Table S5 | METR-LA paired effect summaries | [PDF](appendix/tables/Table_S5.pdf) / [PNG](appendix/tables/Table_S5.png) / [TeX](appendix/tables/Table_S5.tex) |
| Table S6 | Checkpoint gradient direction and magnitude summaries | [PDF](appendix/tables/Table_S6.pdf) / [PNG](appendix/tables/Table_S6.png) / [TeX](appendix/tables/Table_S6.tex) |
| Table S7 | Representation variance and effective rank summaries | [PDF](appendix/tables/Table_S7.pdf) / [PNG](appendix/tables/Table_S7.png) / [TeX](appendix/tables/Table_S7.tex) |
| Table S8 | Relative view distance and forecasting-error associations | [PDF](appendix/tables/Table_S8.pdf) / [PNG](appendix/tables/Table_S8.png) / [TeX](appendix/tables/Table_S8.tex) |
| Table S9 (panel a) | Benchmark training settings | [PDF](appendix/tables/Table_S9_panel_a.pdf) / [PNG](appendix/tables/Table_S9_panel_a.png) / [TeX](appendix/tables/Table_S9_panel_a.tex) |
| Table S9 (panel b) | Joint-model benchmark results | [PDF](appendix/tables/Table_S9_panel_b.pdf) / [PNG](appendix/tables/Table_S9_panel_b.png) / [TeX](appendix/tables/Table_S9_panel_b.tex) |
| Table S10 | DIM checkpoint discrimination and representation diagnostics | [PDF](appendix/tables/Table_S10.pdf) / [PNG](appendix/tables/Table_S10.png) / [TeX](appendix/tables/Table_S10.tex) |

The full appendix retains Table S1 as the complete run inventory and Table S3 as weight-sensitivity context. The Table S1 excerpt above reproduces the delayed-activation JiNan comparison retained in the response letter; main Table 5 reports the two-dataset warm-up-zero comparisons. The excerpt preserves the existing results and their configuration distinction. Figures 1-4 and Tables 1-6 appear in the main manuscript and are not separately deposited here. There are no additional response-only experimental figures.

## Source data and interpretation

Numeric CSV files are in [source_data](source_data/README.md). Table PNG files are byte-identical to those embedded in the current response Word document. Individual table PDFs retain vector artwork and complete outer rules. All supplementary tables follow the main manuscript's CAS table typography: CM Sans at 9 TeX pt (approximately 8.97 PDF pt), with STIX mathematics and consistent row spacing. Standalone tables are regenerated from the preserved TeX cell contents and inserted at natural size, without page-width stretching. All response-only appendix tables are blue, matching the response letter. In main-manuscript table screenshots, revised content is blue and unchanged content remains black; those main tables are not deposited here. The table-only TeX fragments retain the same numerical contents. To compile them, load T1 fontenc, amsmath, amssymb, booktabs, array, longtable, xcolor, and STIX with the notext option, and define revisionblue as HTML 2352A3. The complete supplementary PDF uses the same table typography.

Training seeds, not diagnostic batches, are the independent units in paired training comparisons. Five probe batches are nested within each seed. JiNan all-entry normalized metrics and original-scale validity-masked metrics are distinct. Public physical speed errors are in mph, and MAPE is in percent. The paired uncertainty intervals and mixed-hardware qualifications are retained as reported; they are not a claim of multiplicity-adjusted significance. Consult the complete appendix for exact definitions and protocols.

## Access and scope

The source repository is private. For peer review, use the author-provided [anonymous repository](https://anonymous.4open.science/r/UPSTN-5C86/). Supplementary results are under `appendix/`, and numerical evidence is under `source_data/`.

Raw third-party traffic datasets, trained checkpoints, private server addresses, credentials, training caches and unrelated project files are not included. Absolute local/server path columns have been removed from CSV copies without changing their numeric fields. No new redistribution licence is assigned by this deposit.

## Integrity

`SHA256SUMS.txt` records the uploaded file hashes. This package was assembled on 4 November 2026 from the revised supplementary material and response-letter tables. On 9 November 2026, the Table S1 delayed-activation excerpt was added to match the revised response letter. Existing numerical source files and the complete supplementary results are unchanged. This update introduces no new experiments. On 10 November 2026, the response-only table PDF/PNG files were synchronized with direct source-PDF captures in the response letter. Numerical source data and the complete supplementary PDF were not changed.

The 10 November 2026 color-only update marks every response-only appendix table in blue. Table contents, numerical source data, source fonts, crop dimensions and layout are unchanged.

The final 10 November 2026 typography correction replaces the earlier Times/10 pt standalone styling with the main manuscript CAS table standard: CM Sans 9 TeX pt and STIX mathematics. It updates the standalone tables and the complete supplementary PDF. PDFs remain vector-based and PNGs are rendered at 300 dpi. Table contents, numerical source data, and the blue revision color are unchanged.
