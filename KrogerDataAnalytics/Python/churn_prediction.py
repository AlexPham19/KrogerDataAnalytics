import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# ===============================
# 1. Load Data
# ===============================
df_households = pd.read_csv('8451_The_Complete_Journey_2_Sample-2/400_households.csv')
df_products = pd.read_csv('8451_The_Complete_Journey_2_Sample-2/400_products.csv')
df_transactions = pd.read_csv('8451_The_Complete_Journey_2_Sample-2/400_transactions.csv')

df_households.columns = df_households.columns.str.strip()
df_products.columns = df_products.columns.str.strip()
df_transactions.columns = df_transactions.columns.str.strip()

# ===============================
# 2. Merge
# ===============================
df = df_transactions.merge(df_households, on='HSHD_NUM', how='left')
df = df.merge(df_products, on='PRODUCT_NUM', how='left')

print(df.head())
print(df.columns)

# ===============================
# 3. Fix Date Column
# ===============================
# Change 'PURCHASE_' to your real date column if different
date_col = 'PURCHASE_'

df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
df = df.dropna(subset=[date_col])

# ===============================
# 4. Create Churn Label
# ===============================
max_date = df[date_col].max()
CHURN_THRESHOLD = 90

last_purchase = df.groupby('HSHD_NUM')[date_col].max().reset_index()
last_purchase['days_since_last_purchase'] = (
    max_date - last_purchase[date_col]
).dt.days

last_purchase['churn'] = (
    last_purchase['days_since_last_purchase'] > CHURN_THRESHOLD
).astype(int)

# ===============================
# 5. Create Household-Level Features
# ===============================
rfm = df.groupby('HSHD_NUM').agg(
    recency=(date_col, lambda x: (max_date - x.max()).days),
    frequency=('BASKET_NUM', 'nunique'),
    total_spend=('SPEND', 'sum'),
    avg_spend=('SPEND', 'mean'),
    total_units=('UNITS', 'sum'),
    avg_units=('UNITS', 'mean')
).reset_index()

# ===============================
# 6. Add Category / Brand Features
# ===============================

# Number of unique departments and commodities bought
category_features = df.groupby('HSHD_NUM').agg(
    unique_departments=('DEPARTMENT', 'nunique'),
    unique_commodities=('COMMODITY', 'nunique')
).reset_index()

# Organic purchase ratio
if 'NATURAL_ORGANIC_FLAG' in df.columns:
    df['is_organic'] = (
        df['NATURAL_ORGANIC_FLAG']
        .astype(str)
        .str.strip()
        .str.upper()
        .map({'Y': 1, 'N': 0})
    )

    organic_features = df.groupby('HSHD_NUM').agg(
        organic_ratio=('is_organic', 'mean')
    ).reset_index()
else:
    organic_features = pd.DataFrame({'HSHD_NUM': df['HSHD_NUM'].unique()})
    organic_features['organic_ratio'] = 0

# Private / National brand ratio
if 'BRAND_TY' in df.columns:
    df['is_national'] = (
        df['BRAND_TY']
        .astype(str)
        .str.strip()
        .str.title()
        .map({'National': 1, 'Private': 0})
    )

    brand_features = df.groupby('HSHD_NUM').agg(
        national_brand_ratio=('is_national', 'mean')
    ).reset_index()
else:
    brand_features = pd.DataFrame({'HSHD_NUM': df['HSHD_NUM'].unique()})
    brand_features['national_brand_ratio'] = 0

# ===============================
# 7. Add Demographics
# ===============================
demo_cols = ['HSHD_NUM', 'INCOME_RANGE', 'AGE_RANGE', 'MARITAL', 'HH_SIZE']

available_demo_cols = [col for col in demo_cols if col in df.columns]

df_demo = df[available_demo_cols].drop_duplicates(subset=['HSHD_NUM'])

# ===============================
# 8. Merge All Features
# ===============================
df_model = rfm.merge(category_features, on='HSHD_NUM', how='left')
df_model = df_model.merge(organic_features, on='HSHD_NUM', how='left')
df_model = df_model.merge(brand_features, on='HSHD_NUM', how='left')
df_model = df_model.merge(df_demo, on='HSHD_NUM', how='left')
df_model = df_model.merge(
    last_purchase[['HSHD_NUM', 'churn']],
    on='HSHD_NUM',
    how='left'
)

# ===============================
# 9. Handle NaN
# ===============================
numeric_cols = df_model.select_dtypes(include=['int64', 'float64']).columns.tolist()
numeric_cols = [col for col in numeric_cols if col not in ['HSHD_NUM', 'churn']]

for col in numeric_cols:
    df_model[col] = df_model[col].fillna(df_model[col].median())

categorical_cols = df_model.select_dtypes(include=['object']).columns.tolist()

for col in categorical_cols:
    df_model[col] = df_model[col].fillna('Unknown')

# ===============================
# 10. Prepare X and y
# ===============================
X = df_model.drop(columns=['HSHD_NUM', 'churn'])
y = df_model['churn']

X = pd.get_dummies(X, drop_first=True)

print("Feature table:")
print(X.head())

print("Churn distribution:")
print(y.value_counts())

# ===============================
# 11. Train/Test Split
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ===============================
# 12. Train Random Forest
# ===============================
rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight='balanced'
)

rf.fit(X_train, y_train)

# ===============================
# 13. Evaluate
# ===============================
y_pred = rf.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ===============================
# 14. Predict Churn Probability
# ===============================
df_results = df_model[['HSHD_NUM']].copy()
df_results['churn_actual'] = y
df_results['churn_probability'] = rf.predict_proba(X)[:, 1]
df_results['predicted_churn'] = rf.predict(X)

print("\nTop households most likely to churn:")
print(df_results.sort_values(by='churn_probability', ascending=False).head(20))

# ===============================
# 15. Feature Importance Plot
# ===============================
feat_imp = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values(by='importance', ascending=False)

plt.figure(figsize=(10, max(6, len(feat_imp) * 0.25)))
plt.barh(feat_imp['feature'].str.strip(), feat_imp['importance'])
plt.gca().invert_yaxis()
plt.title("Random Forest Churn Prediction - Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.yticks(fontsize=6)
plt.tight_layout()
from pathlib import Path

# Get the path of the current working directory
current_path = Path.cwd()

target_path = current_path.parent / "wwwroot" / "charts"
plt.savefig(target_path / "churn_feature_importance.png", bbox_inches="tight")
plt.show()

# ===============================
# 16. Churn Probability Plot
# ===============================
plt.figure(figsize=(8, 5))
plt.hist(df_results['churn_probability'], bins=20)
plt.title("Distribution of Churn Probability")
plt.xlabel("Churn Probability")
plt.ylabel("Number of Households")
plt.tight_layout()
plt.savefig(target_path / "churn_probability_distribution.png", bbox_inches="tight")
plt.show()

# ===============================
# 17. Generate Churn CSV Report
# ===============================
from pathlib import Path
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

# Output folder
current_path = Path.cwd()
report_path = current_path.parent / "wwwroot" / "reports"
report_path.mkdir(parents=True, exist_ok=True)

# -------------------------------
# A. Household risk table
# -------------------------------
df_results['risk_level'] = pd.cut(
    df_results['churn_probability'],
    bins=[0, 0.40, 0.70, 1.00],
    labels=['Low Risk', 'Medium Risk', 'High Risk'],
    include_lowest=True
)

household_risk_report = df_results.sort_values(
    by='churn_probability',
    ascending=False
)

household_risk_report.to_csv(
    report_path / "churn_household_risk_report.csv",
    index=False
)

# -------------------------------
# B. Feature importance table
# -------------------------------
feat_imp_report = feat_imp.copy()
feat_imp_report['importance_percent'] = feat_imp_report['importance'] * 100

feat_imp_report.to_csv(
    report_path / "churn_feature_importance_report.csv",
    index=False
)

# -------------------------------
# C. Model performance summary
# -------------------------------
total_households = len(df_results)

high_risk_count = (df_results['risk_level'] == 'High Risk').sum()
medium_risk_count = (df_results['risk_level'] == 'Medium Risk').sum()
low_risk_count = (df_results['risk_level'] == 'Low Risk').sum()

actual_churn_count = df_results['churn_actual'].sum()
predicted_churn_count = df_results['predicted_churn'].sum()

summary_report = pd.DataFrame({
    'Metric': [
        'Total Households',
        'Actual Churn Households',
        'Predicted Churn Households',
        'High Risk Households',
        'Medium Risk Households',
        'Low Risk Households',
        'Actual Churn Percent',
        'Predicted Churn Percent',
        'High Risk Percent',
        'Medium Risk Percent',
        'Low Risk Percent',
        'Accuracy',
        'Precision',
        'Recall',
        'F1 Score',
        'ROC AUC'
    ],
    'Value': [
        total_households,
        actual_churn_count,
        predicted_churn_count,
        high_risk_count,
        medium_risk_count,
        low_risk_count,
        actual_churn_count / total_households * 100,
        predicted_churn_count / total_households * 100,
        high_risk_count / total_households * 100,
        medium_risk_count / total_households * 100,
        low_risk_count / total_households * 100,
        accuracy_score(y_test, y_pred),
        precision_score(y_test, y_pred, zero_division=0),
        recall_score(y_test, y_pred, zero_division=0),
        f1_score(y_test, y_pred, zero_division=0),
        roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])
    ]
})

summary_report.to_csv(
    report_path / "churn_summary_report.csv",
    index=False
)

# -------------------------------
# D. Confusion matrix report
# -------------------------------
cm = confusion_matrix(y_test, y_pred)

confusion_report = pd.DataFrame(
    cm,
    index=['Actual Not Churn', 'Actual Churn'],
    columns=['Predicted Not Churn', 'Predicted Churn']
)

confusion_report.to_csv(
    report_path / "churn_confusion_matrix_report.csv"
)

# -------------------------------
# E. Top 20 at-risk households
# -------------------------------
top_20_risk = household_risk_report.head(20)

top_20_risk.to_csv(
    report_path / "churn_top_20_at_risk_households.csv",
    index=False
)

print("\nChurn CSV reports generated successfully.")
print("Saved to:", report_path)