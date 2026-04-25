import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# Get the path of the current working directory
current_path = Path.cwd()

# Show the parent directory
print(f"Parent directory: {current_path.parent}")
target_path = current_path.parent / "wwwroot" / "charts"
print(f"Target path for charts: {target_path}")
open(f"{target_path}/myfile.txt", "w").close()

# ===============================
# 1. Load + Merge (yes, I don't have time to get data from SQLServer to Python, so I will just load from CSV)
# ===============================
df_households = pd.read_csv('8451_The_Complete_Journey_2_Sample-2/400_households.csv')
df_products = pd.read_csv('8451_The_Complete_Journey_2_Sample-2/400_products.csv')
df_transactions = pd.read_csv('8451_The_Complete_Journey_2_Sample-2/400_transactions.csv')

df_households.columns = df_households.columns.str.strip()
df_products.columns = df_products.columns.str.strip()
df_transactions.columns = df_transactions.columns.str.strip()

df = df_transactions.merge(df_households, on='HSHD_NUM', how='left')
df = df.merge(df_products, on='PRODUCT_NUM', how='left')

print(df.columns)
# ===============================
# 2. Handle NaN (IMPORTANT)
# ===============================

# --- Categorical columns ---
cat_cols = ['INCOME_RANGE', 'AGE_RANGE', 'MARITAL', 'HH_SIZE']

for col in cat_cols:
    df[col] = df[col].fillna('Unknown')

# ===============================
# 3. Feature Selection
# ===============================
features = cat_cols

X = pd.get_dummies(df[features], drop_first=True)
y = df['BRAND_TY']
print(y.head())

# ===============================
# 4. Train/Test Split
# ===============================
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# 5. Random Forest Model
# ===============================
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# ===============================
# 7. Feature Influence (Direction)
# ===============================

# Convert prediction to numeric if needed
# (if BRAND_TY is still string, fix it first)
df['BRAND_TY'] = df['BRAND_TY'].astype(str).str.strip().str.title()
df['BRAND_TY'] = df['BRAND_TY'].map({'Private': 0, 'National': 1})

print(df['BRAND_TY'].head())

influence_list = []
yy = df['BRAND_TY'].values
for col in X.columns:
    # rows where feature = 1
    mask_1 = X[col] == 1
    mask_0 = X[col] == 0

    if mask_1.sum() == 0 or mask_0.sum() == 0:
        continue

    avg_1 = yy[mask_1].mean()
    avg_0 = yy[mask_0].mean()

    diff = avg_1 - avg_0

    if diff > 0:
        direction = "→ National"
    else:
        direction = "→ Private"

    influence_list.append({
        'feature': col.strip(),
        'importance': rf.feature_importances_[list(X.columns).index(col)],
        'avg_when_1': avg_1,
        'avg_when_0': avg_0,
        'difference': diff,
        'influence': direction
    })

print(influence_list[:5])

# Convert to DataFrame
df_influence = pd.DataFrame(influence_list)

# Sort by importance
df_influence = df_influence.sort_values(by='importance', ascending=False)

print(df_influence.head(20))
# ===============================
# Plot ALL features + legend
# ===============================

plt.figure(figsize=(10, max(6, len(df_influence) * 0.25)))  # dynamic height
plt.yticks(fontsize=6)

# Map colors
color_map = {
    '→ National': 'green',
    '→ Private': 'red'
}
colors = df_influence['influence'].map(color_map)

# Plot ALL features
plt.barh(df_influence['feature'], df_influence['importance'], color=colors)

plt.gca().invert_yaxis()

plt.title("Feature Importance + Direction (All Features)")
plt.xlabel("Importance")
plt.ylabel("Feature")

# ===============================
# Add legend manually
# ===============================
from matplotlib.patches import Patch

legend_elements = [
    Patch(facecolor='green', label='Favors National Brand'),
    Patch(facecolor='red', label='Favors Private Brand')
]

plt.legend(handles=legend_elements, loc='lower right')

plt.tight_layout()
import time

filename = f"chart_feature_influence_to_brand.png"

plt.savefig(f"{target_path}/{filename}", bbox_inches="tight")
plt.show()


# ===============================
# 2. Handle NaN (UPDATED)
# ===============================

# --- Target cleaning ---
df['NATURAL_ORGANIC_FLAG'] = (
    df['NATURAL_ORGANIC_FLAG']
    .astype(str)
    .str.strip()
    .str.upper()
)

# Keep only valid rows
df = df[df['NATURAL_ORGANIC_FLAG'].isin(['Y', 'N'])]

# Encode target
df['NATURAL_ORGANIC_FLAG'] = df['NATURAL_ORGANIC_FLAG'].map({
    'N': 0,   # Non-organic
    'Y': 1    # Organic
})

# --- Categorical columns ---
cat_cols = ['INCOME_RANGE', 'AGE_RANGE', 'MARITAL', 'HH_SIZE']

for col in cat_cols:
    df[col] = df[col].fillna('Unknown')

# ===============================
# 3. Feature Selection
# ===============================
features = cat_cols

X = pd.get_dummies(df[features], drop_first=True)
y = df['NATURAL_ORGANIC_FLAG']

# ===============================
# 4. Train/Test Split
# ===============================
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# 5. Random Forest Model
# ===============================
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# ===============================
# 6. Feature Influence (Organic)
# ===============================

influence_list = []
yy = y.values  # organic = 1

for col in X.columns:
    mask_1 = X[col] == 1
    mask_0 = X[col] == 0

    if mask_1.sum() == 0 or mask_0.sum() == 0:
        continue

    avg_1 = yy[mask_1].mean()
    avg_0 = yy[mask_0].mean()

    diff = avg_1 - avg_0

    if diff > 0:
        direction = "→ Organic"
    else:
        direction = "→ Non-Organic"

    influence_list.append({
        'feature': col.strip(),
        'importance': rf.feature_importances_[list(X.columns).index(col)],
        'avg_when_1': avg_1,
        'avg_when_0': avg_0,
        'difference': diff,
        'influence': direction
    })

df_influence = pd.DataFrame(influence_list)
df_influence = df_influence.sort_values(by='importance', ascending=False)

print(df_influence.head(20))

plt.figure(figsize=(10, max(6, len(df_influence)*0.25)))

color_map = {
    '→ Organic': 'blue',
    '→ Non-Organic': 'orange'
}

colors = df_influence['influence'].map(color_map)

plt.barh(df_influence['feature'], df_influence['importance'], color=colors)
plt.gca().invert_yaxis()

plt.title("Feature Importance + Direction (Organic Preference)")
plt.xlabel("Importance")
plt.ylabel("Feature")

plt.yticks(fontsize=6)

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='blue', label='Favors Organic'),
    Patch(facecolor='orange', label='Favors Non-Organic')
]

plt.legend(handles=legend_elements)

plt.tight_layout()
filename = f"chart_feature_influence_organic.png"
plt.savefig(f"{target_path}/{filename}", bbox_inches="tight")
plt.show()

