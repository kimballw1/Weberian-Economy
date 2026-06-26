


import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from sklearn.preprocessing import StandardScaler

# Load the cleaned dataset
df = pd.read_csv("/Users/kimballweeks/Downloads/cleaned_data.csv")

# Rename for compatibility (IMPORTANT: these must match your CSV column names)
df = df.rename(columns={
    "pct_highschool_or_more (1990)": "pct_hs_1990",
    "Pop 2023": "pop_2023",
    "Established firms 2022": "firms_2022",
    "Established firms 1989": "firms_1989"
})

# Convert relevant columns to numeric
df['church_persistence_index'] = pd.to_numeric(df['church_persistence_index'], errors='coerce')
df['income_1989_real_2023'] = pd.to_numeric(df['income_1989_real_2023'], errors='coerce')
df['pct_hs_1990'] = pd.to_numeric(df['pct_hs_1990'], errors='coerce')
df['pop_2023'] = pd.to_numeric(df['pop_2023'], errors='coerce')
df['firms_2022'] = pd.to_numeric(df['firms_2022'], errors='coerce')
df['firms_1989'] = pd.to_numeric(df['firms_1989'], errors='coerce')

# Drop rows with missing values in these columns
df = df.dropna(subset=[
    'church_persistence_index',
    'income_1989_real_2023',
    'pct_hs_1990',
    'pop_2023',
    'firms_2022',
    'firms_1989'
])

# Drop rows where log would break
df = df[(df['firms_2022'] > 0) & (df['pop_2023'] > 0) & (df['firms_1989'] > 0)]

# Log-transform outcome and population + 1989 firms
df['log_firms_2022'] = np.log(df['firms_2022'])
df['log_pop_2023'] = np.log(df['pop_2023'])
df['log_firms_1989'] = np.log(df['firms_1989'])

# Standardize income and education
scaler = StandardScaler()
df[['income_1989_scaled', 'pct_hs_1990_scaled']] = scaler.fit_transform(
    df[['income_1989_real_2023', 'pct_hs_1990']]
)

# Run the regression
model = smf.ols(
    formula='log_firms_2022 ~ church_persistence_index + income_1989_scaled + pct_hs_1990_scaled + log_pop_2023 + log_firms_1989 + C(State)',
    data=df
).fit(cov_type='HC3')

# Output the summary
print(model.summary())


