from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder


numeric_columns = [
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
    ]

categorical_columns = [
        "gender",
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "PhoneService",
        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaperlessBilling",
        "PaymentMethod",
    ]

def build_pipeline():

    num_pipeline = Pipeline([
        ("imputer",SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    full_pipeline = ColumnTransformer([
        ("num",num_pipeline,numeric_columns),
        ("cat",OneHotEncoder(handle_unknown="ignore"),categorical_columns)

    ])
    return full_pipeline