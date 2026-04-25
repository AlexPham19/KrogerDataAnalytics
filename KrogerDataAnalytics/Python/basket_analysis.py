import pandas as pd
import matplotlib.pyplot as plt

from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

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
# 2. Merge Data
# ===============================
df = df_transactions.merge(df_households, on='HSHD_NUM', how='left')
df = df.merge(df_products, on='PRODUCT_NUM', how='left')

print(df.head())
print(df.columns)

# ===============================
# 3. Clean Basket Data
# ===============================
df = df.dropna(subset=['BASKET_NUM', 'COMMODITY', 'UNITS'])

df['COMMODITY'] = df['COMMODITY'].astype(str).str.strip()
df = df[df['COMMODITY'] != '']

# ===============================
# 4. Create Basket Matrix
# rows = baskets
# columns = commodities
# values = 1 if bought, 0 if not
# ===============================
basket = df.groupby(['BASKET_NUM', 'COMMODITY'])['UNITS'].sum().unstack().fillna(0)

basket = (basket > 0).astype(int)

print("\nBasket matrix:")
print(basket.head())

# ===============================
# 5. Association Rule Mining
# ===============================
frequent_itemsets = apriori(
    basket,
    min_support=0.02,
    use_colnames=True
)

rules = association_rules(
    frequent_itemsets,
    metric='lift',
    min_threshold=1.2
)

rules = rules.sort_values(by='lift', ascending=False)

print("\nTop Product Combination Rules:")
print(
    rules[
        ['antecedents', 'consequents', 'support', 'confidence', 'lift']
    ].head(20)
)

# ===============================
# 6. Save Association Rules
# ===============================
rules_export = rules.copy()
rules_export['antecedents'] = rules_export['antecedents'].apply(lambda x: ', '.join(list(x)))
rules_export['consequents'] = rules_export['consequents'].apply(lambda x: ', '.join(list(x)))

from pathlib import Path

# Get the path of the current working directory
current_path = Path.cwd()

target_path = current_path.parent / "wwwroot" / "charts"

rules_export.to_csv(f'{target_path}/basket_association_rules.csv', index=False)

# ===============================
# 7. Select Target Product for ML
# ===============================
# Change this to a real COMMODITY in your dataset
print("\nAvailable commodities:")
print(list(basket.columns)[:50])

target_product = basket.columns[0]   # automatic choice
# Example:
# target_product = 'MILK'

print("\nTarget product for Random Forest prediction:", target_product)

# ===============================
# 8. Prepare ML Dataset
# Predict whether target_product is bought
# using all other products in the basket
# ===============================
X = basket.drop(columns=[target_product])
y = basket[target_product]

print("\nTarget distribution:")
print(y.value_counts())

# If target has only one class, choose another product
if y.nunique() < 2:
    raise ValueError("Target product has only one class. Choose another commodity.")

# ===============================
# 9. Train/Test Split
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ===============================
# 10. Train Random Forest
# ===============================
rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight='balanced'
)

rf.fit(X_train, y_train)

# ===============================
# 11. Evaluate Model
# ===============================
y_pred = rf.predict(X_test)

print("\nRandom Forest Results")
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# ===============================
# 12. Feature Importance
# Products that drive target_product purchase
# ===============================
feature_importance = pd.DataFrame({
    'product': X.columns,
    'importance': rf.feature_importances_
}).sort_values(by='importance', ascending=False)

print("\nTop Cross-Sell Drivers:")
print(feature_importance.head(20))

# ===============================
# 13. Plot Top Cross-Sell Drivers
# ===============================
top_n = 20
plot_df = feature_importance.head(top_n)

plt.figure(figsize=(10, 7))
plt.barh(plot_df['product'], plot_df['importance'])
plt.gca().invert_yaxis()
plt.title(f"Top Products Driving Purchase of {target_product}")
plt.xlabel("Random Forest Importance")
plt.ylabel("Product")
plt.yticks(fontsize=7)
plt.tight_layout()
plt.savefig(f"{target_path}/top_cross_sell_drivers.png", bbox_inches="tight")
plt.show()

# ===============================
# 14. Plot Top Association Rules by Lift
# ===============================
top_rules = rules_export.sort_values(by='lift', ascending=False).head(15)

rule_labels = top_rules['antecedents'] + " → " + top_rules['consequents']

plt.figure(figsize=(12, 7))
plt.barh(rule_labels, top_rules['lift'])
plt.gca().invert_yaxis()
plt.title("Top Product Combinations by Lift")
plt.xlabel("Lift")
plt.ylabel("Rule")
plt.yticks(fontsize=7)
plt.tight_layout()

plt.savefig(f"{target_path}/top_association_rules.png", bbox_inches="tight")

plt.show()

# ===============================
# 15. Business Recommendations
# ===============================
print("\nBusiness Recommendations:")
print("1. Use high-lift rules for bundle promotions.")
print("2. Place frequently paired products near each other.")
print("3. Use Random Forest feature importance to recommend products when the target product is likely.")
print("4. Products with high confidence rules are strong cross-sell candidates.")
print("5. Products with high lift show combinations that happen more often than random chance.")