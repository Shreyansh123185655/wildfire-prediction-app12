import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
import joblib
import os

# Load and clean dataset
data = pd.read_csv("data/CA_Weather_Fire_Dataset_1984-2025.csv")

rename_map = {
    "MAX_TEMP": "temperature",
    "PRECIPITATION": "rainfall",
    "AVG_WIND_SPEED": "wind_speed",
    "SEASON": "season",
    "FIRE_START_DAY": "fire_risk"
}
data = data.rename(columns=rename_map)
# Handle missing values for lagged features
data = data.dropna(subset=["temperature", "rainfall", "wind_speed", "season", "fire_risk", "LAGGED_PRECIPITATION", "LAGGED_AVG_WIND_SPEED"])
data["fire_risk"] = data["fire_risk"].astype(int)

# Features and Target - using expanded feature set
X = data[[
    "temperature", "rainfall", "wind_speed", "season",
    "MIN_TEMP", "TEMP_RANGE", "WIND_TEMP_RATIO", "MONTH",
    "LAGGED_PRECIPITATION", "LAGGED_AVG_WIND_SPEED", "DAY_OF_YEAR"
]]
y = data["fire_risk"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Preprocessing
numeric_features = [
    "temperature", "rainfall", "wind_speed",
    "MIN_TEMP", "TEMP_RANGE", "WIND_TEMP_RATIO", "MONTH",
    "LAGGED_PRECIPITATION", "LAGGED_AVG_WIND_SPEED", "DAY_OF_YEAR"
]
categorical_features = ["season"]

numeric_transformer = Pipeline(steps=[("scaler", StandardScaler())])
categorical_transformer = Pipeline(steps=[("encoder", OneHotEncoder(handle_unknown="ignore"))])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# SMOTE
smote = SMOTE(random_state=42)

# Model with improved hyperparameters
rf = RandomForestClassifier(
    n_estimators=500,
    random_state=42,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt'
)

# Build an Imbalanced-Learn Pipeline
model = ImbPipeline(steps=[
    ("preprocessor", preprocessor),
    ("smote", smote),
    ("classifier", rf)
])

# Train the model
print("Training model...")
model.fit(X_train, y_train)

# Save model to notebooks directory
model_path = "notebooks/wildfire_risk_model.pkl"
joblib.dump(model, model_path)
print("✅ Model trained and saved successfully!")
print("Model path:", model_path)

# Model Evaluation
y_pred = model.predict(X_test)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("Accuracy Score:", accuracy_score(y_test, y_pred))
