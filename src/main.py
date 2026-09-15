import pandas as pd 
import numpy as np
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

from data import load_data, split_data, DATA_PATH
from preprocessing import build_pipeline
from train import get_models, evaluate_model, tune_models



def main():
    #veri yükle
    df = load_data(path=DATA_PATH)

    #train ve test seti ayır
    train_set ,test_set =split_data(df)

    x_train = train_set.drop(columns=["Churn", "customerID"])
    y_train =train_set["Churn"].map({"No":0,"Yes":1})
    x_test = test_set.drop(columns=["Churn", "customerID"])
    y_test =test_set["Churn"].map({"No":0,"Yes":1})

    
    #modelleri al
    models = get_models()

    for name, model in models.items():
        mean_auc, std_auc = evaluate_model(
            model,
            x_train,
            y_train,
        )

        print(f"{name}: ROC-AUC = {mean_auc:.4f} ± {std_auc:.4f}")

    best_model, searches = tune_models(x_train, y_train)

    # Seçilen pipeline zaten eğitildi; test verisini yalnızca değerlendirmede kullan.
    y_pred = best_model.predict(x_test)
    y_proba = best_model.predict_proba(x_test)[:, 1]

    print(f"\nTest ROC-AUC: {roc_auc_score(y_test, y_proba):.4f}")

    print("\nSınıflandırma raporu:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=["Kalıyor", "Ayrılıyor"],
        zero_division=0,
    ))

    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, y_pred))

        




if __name__ == "__main__":
     main()
