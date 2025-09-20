### Predictive Manufacturing

Predictive Manufacturing

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

## Installation

1. **Go to your Frappe Bench directory**
```bash
cd ~/frappe-bench
bench get-app https://github.com/praful99665/predictive_manufacturing.git
bench --site your-site-name install-app predictive_manufacturing
bench migrate

## Train the predictive model
bench --site your-site-name execute predictive_manufacturing.train_delay_model.train
### This command creates the model files in:
sites/your-site-name/public/files/models/


        delay_model.pkl → trained machine learning model
        
        workstation_ohe.pkl → encoder for categorical features
        
        feature_columns.pkl → list of feature columns used in the model

### Usage

Once installed and trained, Work Orders will show risk indicators based on the predictive model.

You can call the model from server scripts or API endpoints in ERPNext to get delay probabilities.



### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/predictive_manufacturing
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade


#########################################################################


### Predictive Manufacturing - Delay Alert System

##Overview
This app helps manufacturers predict delays in Work Orders by using AI/ML models.  
It integrates seamlessly into ERPNext and provides early warnings based on real-world factors like material availability, machine downtime, and workforce shortage.

---

## Architecture Flow
```mermaid
flowchart TD
    A[New Work Order Created] --> B[Extract Features]
    B --> C[Check Raw Material Availability]
    C --> D[Check Machine Availability]
    D --> E[Check Workforce Availability]
    E --> F[Pass Data to ML Model]
    F --> G[Predict Delay Probability]

    G -->|0-30%| H[Low Risk (Green)]
    G -->|60-100%| J[High Risk (Red)]




#################################################################################
#################################################################################
#################################################################################


## Model Logic

### 1. Input Features
Each Work Order uses the following features to predict delay:

- **Planned start days from today**
- **Raw material availability** (`1 = available`, `0 = not available`)
- **Machine availability** (`1 = available`, `0 = not available`)
- **Workforce availability** (`1 = available`, `0 = not available`)
- **Workstation type** (categorical, e.g., Lathe, Milling, Welding)

---

### 2. Preprocessing
- Apply **One-Hot Encoding (OHE)** to categorical features such as workstation type.
- Align input features with `feature_columns.pkl` saved during training.
- Handle new or missing categories using `workstation_ohe.pkl`.

---

### 3. Model Training
- **Algorithm:** Logistic Regression or Decision Tree Classifier.
- **Dataset:** Simulated (~200 Work Orders covering different scenarios).
- **Output:** Probability of delay (0–100%).
- **Saved Artifacts:**


sites/[site-name]/public/files/models/
├── delay_model.pkl # Trained ML model
├── workstation_ohe.pkl # One-Hot Encoder for workstation
└── feature_columns.pkl # Feature column order

---

### 4. Prediction & Risk Mapping
- Preprocess new Work Order features.
- Predict probability of delay using the trained model.
- Map probability to risk levels:
  - `<30% → Low Risk (Green)`
  - `≥30% → High Risk (Red)`

---

### 5. ERPNext Integration
- Triggered when a Work Order **is created or updated**.
- Updates **status field**, **risk description**, and **colored tag** in the form and list view.
- Provides **early warning** to production managers for corrective actions.







