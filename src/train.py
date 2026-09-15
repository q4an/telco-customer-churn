from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

if __package__:
    from .preprocessing import build_pipeline
else:
    from preprocessing import build_pipeline


def get_models():
    """Return complete pipelines that accept raw feature DataFrames."""
    classifiers = {
        "logistic_regression": LogisticRegression(max_iter=3000, random_state=42),
        "decision_tree": DecisionTreeClassifier(random_state=42),
        "random_forest": RandomForestClassifier(random_state=42),
    }
    return {
        name: Pipeline([
            ("preprocessor", build_pipeline()),
            ("classifier", classifier),
        ])
        for name, classifier in classifiers.items()
    }


def evaluate_model(model, X, y, cv=5):
    """Return validation ROC-AUC mean and standard deviation; higher is better."""
    folds = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    scores = cross_val_score(
        model, X, y, scoring="roc_auc", cv=folds, error_score="raise",
    )
    return scores.mean(), scores.std()


def tune_models(X_train, y_train, cv=5):
    """Tune on training data only; return the best fitted pipeline and searches."""
    models = get_models()
    param_grids = {
        "logistic_regression": {
            "classifier__C": [0.01, 0.1, 1, 10],
            "classifier__class_weight": [None, "balanced"],
        },
        "decision_tree": {
            "classifier__max_depth": [None, 5, 10],
            "classifier__min_samples_leaf": [1, 5, 10],
            "classifier__class_weight": [None, "balanced"],
        },
        "random_forest": {
            "classifier__n_estimators": [100, 300],
            "classifier__max_depth": [None, 10],
            "classifier__min_samples_leaf": [1, 5],
            "classifier__max_features": ["sqrt", 0.5],
            "classifier__class_weight": [None, "balanced"],
        },
    }
    folds = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    searches = {}

    for name, model in models.items():
        print(f"{name}: tuning...")
        search = GridSearchCV(
            estimator=model,
            param_grid=param_grids[name],
            scoring="roc_auc",
            cv=folds,
            n_jobs=-1,
            refit=True,
            verbose=1,
            error_score="raise",
        )
        search.fit(X_train, y_train)
        searches[name] = search
        print("Best parameters:", search.best_params_)
        print(f"CV ROC-AUC: {search.best_score_:.4f}")

    best_name = max(searches, key=lambda name: searches[name].best_score_)
    print(f"Selected model: {best_name}")
    return searches[best_name].best_estimator_, searches
