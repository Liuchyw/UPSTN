# Numeric source data

All CSV files are UTF-8. Numeric values and non-path fields are preserved from the revision delivery source-data bundle. Only columns containing absolute local or server paths are omitted; see `removed_path_columns.json`. No raw third-party sensor observations are distributed.

| Folder | Contents | Related supplementary tables |
| --- | --- | --- |
| core | JiNan run metrics, component/deviation contrasts, paired means, SDs and intervals | S1, S2 |
| final | Recomputed JiNan weight metrics and matched METR-LA metrics/paired summaries | S3, S4, S5 |
| probes | Gradient, representation variance/rank and distance-error records | S6, S7, S8 |
| probes/dim | Five-batch DIM checkpoint diagnostic | S10 |

Historical settings and benchmark values for S9 are available in the appendix and its table-only TeX fragments. `P`/`Prototype`, `S+P`/`+Spatial`, `TP+P`/`+Temporal`, and `Full`/`Joint` are corresponding source-record/display labels, not different configurations. Positive On-minus-Off penalties indicate lower error with alignment disabled.

`normalized_mae` and `normalized_rmse` refer to normalized traffic errors. Physical MAE/RMSE on METR-LA are in mph. MAPE fields ending in `_percent` are percentages; MAPE differences are percentage points. `sample_sd` denotes sample standard deviation across independent training seeds in paired summaries. Probe SDs describe within-seed batch variation. Complete metric/masking and sampling definitions are in `appendix/supplementary_results.pdf`.

To compile the full appendix, use `pdflatex supplementary_results.tex` from `appendix/`. Table-only fragments need T1 `fontenc`, `amsmath`, `amssymb`, `booktabs`, `longtable`, `array`, `xcolor`, and `stix` with the `notext` option, with `\definecolor{revisionblue}{RGB}{35,82,163}`. They omit captions for layout fidelity; captions are supplied as adjacent `_caption.txt` files and in the complete appendix.
