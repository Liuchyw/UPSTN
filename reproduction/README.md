# Reproduce the revised numerical figures

These files reproduce Figures 1 and 4 from exported measurements. They do not train models or generate illustrative observations. Run from each figure folder with Python 3 and the packages in requirements.txt. Times New Roman reproduces the manuscript typography; a system font substitution changes appearance only.

Figure 1: `python plot_a.py`, `python plot_components.py`, `python assemble.py`.
Figure 4: `python plot_main.py`.

Figure 1(a) uses a 2,016-slot weekly summary and the JiNan sensor coordinates/connections distributed with STDN (https://github.com/roarer008/STDN). Coordinates are the supplied relative/anonymized coordinates. The original dataset remains subject to its source terms. Panels (b,c) use exported same-seed horizon errors and the prespecified node-210 first-complete-test-day case. No smoothing, offsets or favorable-case filtering are applied.

Figure 4 includes 75 weighted gradient observations, 1,226 seed-42 node effects across two datasets/configurations, and 32,480 node-window observations in each of six clouds. Each cloud combines five disjoint 16-window batches at 406 nodes. Seeds are the training replication units; nodes and batches are dependent descriptive observations. Per-batch correlations use complete arrays. MAE above 0.5 is counted in annotations, not silently removed from statistics. Node ECDF insets use pooled fifth/95th percentiles and full-sample cumulative fractions. Gradient point area is 24 times its weighted norm divided by the median within its objective. JiNan errors are normalized; METR-LA node errors use original-scale validity masking in mph.

The original plotting geometry and numerical inputs are retained. Project-internal layout-audit calls are omitted from the portable scripts. Full training code/checkpoints follow the manuscript Data availability statement. This package contains derived plotting measurements, not raw traffic sequences, private server information, reviewer reports or credentials.
