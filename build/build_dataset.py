"""Reproducible cleaning pipeline: raw BDS + FIPS-preserved religion/controls -> analysis_cross_section.csv"""
import pandas as pd, numpy as np, os, statsmodels.formula.api as smf
RAW="/Users/kimballweeks/Downloads/inst persist"; OUT="/Users/kimballweeks/Downloads/weberian-economy/data"
def num(s): return pd.to_numeric(s,errors="coerce")
log=[]
# 1) religion + controls, FIPS-keyed; clean DNE/dup
base=pd.read_csv(f"{RAW}/Iterations/cleaned_data_with_fips_preserved.csv")
if "income_2023.1" in base.columns: base=base.drop(columns=["income_2023.1"])
base["fips"]=num(base["fips"]).astype("Int64").astype(str).str.zfill(5)
base=base[base.fips.str.len()==5].drop_duplicates(subset="fips")
for c in base.columns:
    if c not in ("State","County","fips"): base[c]=num(base[c])
# bring Index_v2 over from v3 (same county set) for comparison
v3=pd.read_csv(f"{RAW}/Cleaned_data_v3.csv")[["State","County","Index_v2"]]
base=base.merge(v3,on=["State","County"],how="left")
log.append(f"Religion/control base (FIPS-keyed, DNE->NaN, dup col dropped): {len(base)} counties")
# 2) BDS multi-year outcome
bds=pd.read_csv(f"{RAW}/established firms /bds2022_st_cty.csv")
bds["fips"]=num(bds.st).astype("Int64").astype(str).str.zfill(2)+num(bds.cty).astype("Int64").astype(str).str.zfill(3)
for c in ["estabs_entry","estabs_entry_rate"]: bds[c]=num(bds[c])
def agg(yrs,col,name): return bds[bds.year.isin(yrs)].groupby("fips")[col].mean().rename(name)
out=pd.concat([agg(range(2015,2020),"estabs_entry","births_1519"),
               agg(range(2015,2020),"estabs_entry_rate","entryrate_1519"),
               agg([2022],"estabs_entry","births_2022")],axis=1).reset_index()
df=base.merge(out,on="fips",how="left")
log.append(f"BDS pre-COVID(2015-19) matched on FIPS: {df.births_1519.notna().sum()}/{len(df)}")
df["birthrate_pc_1519"]=1000*df.births_1519/df["Pop 2010"]
# 3) validation (robust)
val=[]
if "churches_1990" in df:
    gap=(1000*df.churches_1990/df["Pop 1990"]-df.church_density_1990).abs(); val.append(f"density==churches/pop(1990): max gap {gap.max():.4f}")
for c in ["church_density_2020","birthrate_pc_1519","entryrate_1519","Index_v2"]:
    if c in df and df[c].notna().any(): s=df[c]; val.append(f"{c}: n={int(s.notna().sum())}, range[{s.min():.2f},{s.max():.2f}]")
# 4) write
os.makedirs(OUT,exist_ok=True); df.to_csv(f"{OUT}/analysis_cross_section.csv",index=False)
open(f"{OUT}/CLEANING_LOG.txt","w").write("BUILD\n"+"\n".join(log)+"\n\nVALIDATION\n"+"\n".join(val)+"\n")
print("\n".join(log)); print("--- VALIDATION ---"); print("\n".join(val))
print(f"WROTE analysis_cross_section.csv ({df.shape[0]}x{df.shape[1]})")
# 5) does the result change on the CLEAN multi-year per-capita outcome?
print("\n=== CLEAN multi-year (2015-19) per-capita outcome, state-clustered ===")
d=df.dropna(subset=["birthrate_pc_1519","church_density_2020","income_1989_real_2023","pct_highschool_or_more (1990)"]).copy()
d=d[d.birthrate_pc_1519>0]; d["y"]=np.log(d.birthrate_pc_1519)
z=lambda x:(x-x.mean())/x.std(); d["inc"]=z(d.income_1989_real_2023); d["edu"]=z(d["pct_highschool_or_more (1990)"]); d["cd20"]=z(d.church_density_2020)
for lab,f in [("Index_v2 + ctrls","y ~ Index_v2 + inc + edu + C(State)"),
              ("church density 2020 + ctrls","y ~ cd20 + inc + edu + C(State)")]:
    m=smf.ols(f,d).fit(cov_type="cluster",cov_kwds={"groups":d.State}); k=f.split("~")[1].split("+")[0].strip()
    print(f"  {lab:32s} {k}: {m.params[k]:+.4f} (p={m.pvalues[k]:.3f}, N={int(m.nobs)})")
