# The Weberian Economy
### How Institutional Persistence Shapes Local Entrepreneurship

Replication code for my county-level study of whether long-run institutional continuity, measured through religious institutions that endured across generations, predicts modern entrepreneurship in the United States.

The main finding: among U.S. counties that look alike today in size, income, and educational history, those whose religious institutions persisted across generations generate roughly 5.7% more new business establishments per capita in 2022. The effect runs partly through human capital (education), and 1890 church density alone does not explain it. Continuity matters more than initial conditions.

---

## The idea

Agglomeration theories predict that new firms cluster where population and density are high. Yet many small, slow-growing counties consistently outperform their demographic weight in new establishment births. This project proposes one explanation: institutional depth rather than demographic breadth. Following a Weberian view, counties where churches remained continuously active across the twentieth century accumulated the human capital, trust, and civic infrastructure that entrepreneurship draws on. To test this, the paper builds a church persistence index from county congregation counts in 1890, 1990, 2010, and 2020, and relates it to new establishment births from the Census Business Dynamics Statistics.

## The persistence index

The index rewards consistency of religious presence over 130 years, not a single historical peak. For each census year, church density is turned into a robust z-score (median/MAD, winsorized at ±3.5). Years are then weighted by how well their cross-county rankings agree with the other years (Spearman-based weights), so noisier decades count less, and the weighted composite is re-standardized across counties to mean 0, SD 1. Full construction is in §3.2 of the manuscript; the computed index ships in the dataset as `Index_v2`.

## Repository structure

```
Weberian-Economy/
├── build/
│   └── build_dataset.py            # cleaning pipeline: raw sources -> analysis_cross_section.csv
├── data/
│   ├── cleaned_data_v3.csv         # analysis-ready county panel: churches, income, education, firms, population
│   ├── analysis_cross_section.csv  # panel rebuilt by build_dataset.py, adds 2015-19 BDS outcomes
│   ├── CLEANING_LOG.txt            # log written by the build script
│   └── README.md                   # variable dictionary and sources
├── notebooks/                      # one notebook per result, numbered in reading order
│   ├── 01_baseline.ipynb
│   ├── 02_education_channel.ipynb
│   ├── 03_education_on_firms.ipynb
│   ├── 04_mediation.ipynb
│   ├── 05_initial_conditions_horserace.ipynb
│   ├── 06_robustness_1890_1990_index.ipynb
│   ├── 07_robustness_contemporary_church.ipynb
│   ├── 08_population_outcome.ipynb
│   ├── 09_income_outcome.ipynb
│   ├── 10_ppml.ipynb
│   ├── 11_forest_plot.ipynb
│   ├── 12_scatter_diagnostics.ipynb
│   └── 13_clustered_se.ipynb
├── figures/                        # generated figures land here
├── archive/                        # earlier exploratory notebooks, kept for provenance
├── Manuscript.pdf
├── requirements.txt
└── README.md
```

## How the notebooks map to the manuscript

| Notebook | Produces | Manuscript |
|---|---|---|
| `01_baseline` | Persistence → log new establishments (2022), the main estimate (β₁ ≈ 0.056) plus regression diagnostics | Table 2 |
| `02_education_channel` | Persistence → educational attainment (2023) | Table 3, col (a) |
| `03_education_on_firms` | Historical education (1990) → new establishments | Table 3, col (b) |
| `04_mediation` | Adds contemporary education to the baseline; reports the attenuation (~9% mediated) | Table 4 |
| `05_initial_conditions_horserace` | 1890 church density vs. the persistence index in one regression | §3.3, initial conditions vs. continuity |
| `06_robustness_1890_1990_index` | Two-period (1890–1990) index | Robustness |
| `07_robustness_contemporary_church` | Adds 2020 church density to the baseline | Robustness |
| `08_population_outcome` | Persistence → log population (2023): the scale placebo | §4, population outcome |
| `09_income_outcome` | Persistence → log income (2023) | §4 |
| `10_ppml` | Poisson (PPML) count model with a population offset | Robustness |
| `11_forest_plot` | Persistence coefficient across all specifications (forest plot) | Figure |
| `12_scatter_diagnostics` | Persistence vs. establishments / education / population scatters | Appendix C |
| `13_clustered_se` | Baseline with state-clustered standard errors (48 clusters): coefficient unchanged, p ≈ 0.006 | Robustness, inference check |

## Reproducing the results

```bash
# 1. create an environment (conda or venv) and install dependencies
pip install -r requirements.txt

# 2. launch Jupyter and run the notebooks in order
jupyter lab            # or: jupyter notebook
```

Each notebook is self-contained: it loads `data/cleaned_data_v3.csv`, prepares the variables, and prints the regression. All estimates use HC3 robust standard errors with state fixed effects; standardized controls are z-scored prior to estimation, matching the paper.

The notebooks only need `cleaned_data_v3.csv`, which ships with the repo. `build/build_dataset.py` is the cleaning pipeline that produced `analysis_cross_section.csv`; it reads raw files from a local folder that isn't redistributed, so it's included for transparency rather than for rerunning.

## Data sources

The county panel is assembled from public sources (see `data/README.md` for the variable dictionary):

- Church congregation counts: Association of Religion Data Archives (ARDA), 1890 / 1990 / 2010 / 2020.
- Income, education, population: U.S. Census / ACS via NHGIS.
- New establishment births: Census Business Dynamics Statistics (BDS).

The repository ships the cleaned, analysis-ready panel. Raw source files are not redistributed; download links and definitions are in `data/README.md`.

## Citation

> Weeks, Kimball. *The Weberian Economy: How Institutional Persistence Shapes
> Local Entrepreneurship.* Working paper.

## License

Released under the MIT License (see `LICENSE`).
