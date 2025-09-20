import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
import pickle
import os

# Simulate dataset
np.random.seed(42)
n = 150
workstations = ['A', 'B', 'C']

df = pd.DataFrame({
    'planned_start_days_from_today': np.random.randint(0, 10, n),
    'raw_material_available': np.random.randint(0, 2, n),
    'machine_availability': np.round(np.random.uniform(0.5, 1.0, n), 2),
    'shift_capacity': np.round(np.random.uniform(0.5, 1.0, n), 2),
    'workforce_available': np.random.randint(0, 2, n),
    'planned_quantity': np.random.randint(10, 100, n),
    'workstation': np.random.choice(workstations, n),
})

# Simple rule to define delay
df['delayed'] = 0
df.loc[
    (df['raw_material_available'] == 0) |
    (df['machine_availability'] < 0.7) |
    (df['workforce_available'] == 0),
    'delayed'
] = 1

# Split features & target
X = df.drop('delayed', axis=1)
y = df['delayed']

# OneHotEncode workstation
ohe = OneHotEncoder(sparse_output=False)
ws_encoded = ohe.fit_transform(X[['workstation']])
X_encoded = np.hstack([X.drop('workstation', axis=1).values, ws_encoded])

feature_columns = list(X.drop('workstation', axis=1).columns) + list(
    ohe.get_feature_names_out(['workstation'])
)

# Train Decision Tree
model = DecisionTreeClassifier(random_state=42)
model.fit(X_encoded, y)

# Save files inside your site aiml.com
site = "aiml.com"
model_path = os.path.join("sites", site, "public", "files", "models")
os.makedirs(model_path, exist_ok=True)

with open(os.path.join(model_path, "delay_model.pkl"), "wb") as f:
    pickle.dump(model, f)
with open(os.path.join(model_path, "workstation_ohe.pkl"), "wb") as f:
    pickle.dump(ohe, f)
with open(os.path.join(model_path, "feature_columns.pkl"), "wb") as f:
    pickle.dump(feature_columns, f)

print(f"✅ Model and encoder saved in {model_path}")
