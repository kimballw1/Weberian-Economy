# Data

`cleaned_data_v3.csv` is the analysis-ready county panel (one row per U.S.
county, ~3,055 counties). It is assembled from public sources; raw files are not
redistributed here, but each block below notes where to obtain them.

## Sources

| Block | Source | Years |
|---|---|---|
| Church congregation counts | Association of Religion Data Archives (ARDA), U.S. Religion Census | 1890, 1990, 2010, 2020 |
| Income, education, population | U.S. Census / ACS via IPUMS NHGIS | 1890–2023 |
| New establishment births | Census Business Dynamics Statistics (BDS) | 1989, 2010, 2022 |

Connecticut and Rhode Island (no functional county governments) and Alaska
(non-aligned borough system) are excluded, along with a small number of counties
with incomplete historical reporting; see manuscript Appendix D.

## Variable dictionary

**Identifiers**
- `State`, `County` — county identifiers.

**Religious institutions (ARDA)**
- `churches_1890`, `churches_1990`, `churches_2010`, `churches_2020` — congregation counts.
- `church_density_1890 … _2020` — congregations per 1,000 residents.

**Persistence index** (constructed; see manuscript §3.2)
- `Index_v2` — **the persistence index used throughout the analysis** (four-period,
  robust-z, Spearman-weighted, standardized across counties).
- `church_persistence_index`, `Church_persistence_index_3yr` — earlier index variants.
- `z1890`, `z1990`, `index_1890_1990_raw`, `index_1890_1990` — components and the
  two-period (1890–1990) robustness index.

**Outcomes & controls (Census / BDS)**
- `Established firms 1989 / 2010 / 2022` — new establishment births (BDS).
- `pct_highschool_or_more (1990) / (2010) / _(2023)` — share of adults 25+ with at
  least a high-school diploma.
- `income_1989 / 2010 / 2023` (nominal) and `income_1989_real_2023`,
  `income_2010_real_2023` — median household income, real ($2023) versions used in
  estimation.
- `Pop 1890 / 1990 / 2010 / 2023` — county population.

## Notes
- Estimation standardizes 1989 income and 1990 education to z-scores; population
  and firm counts enter in logs (`log` for population/pre-period firms, `log(1+·)`
  for the 2022 outcome to retain zero-birth counties).
- `income_2023.1` is a duplicate import column and is unused.
