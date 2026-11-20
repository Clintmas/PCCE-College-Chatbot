
import json
import joblib

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline

from src.preprocess import preprocess_text


# 1. Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "intents.json"
MODEL_PATH = BASE_DIR / "models" / "chatbot_model.pkl"


# 2. Load the training dataset
with open(DATA_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)


# 3. Extract patterns and their corresponding intents
sentences = []
labels = []

for intent in data["intents"]:

    for pattern in intent["patterns"]:

        cleaned_text = preprocess_text(pattern)

        sentences.append(cleaned_text)
        labels.append(intent["tag"])


print("Total training examples:", len(sentences))
print("Total intent categories:", len(set(labels)))


# 4. Create a pipeline for cross-validation
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("model", LogisticRegression(max_iter=1000))
])


# 5. Perform Stratified 5-Fold Cross-Validation
class_counts = {
    label: labels.count(label)
    for label in set(labels)
}

minimum_samples = min(class_counts.values())

if minimum_samples < 2:
    print("\nCross-validation cannot be performed.")
    print("At least 2 examples are required for every intent.")
else:
    folds = min(5, minimum_samples)

    cv = StratifiedKFold(
        n_splits=folds,
        shuffle=True,
        random_state=42
    )

    scores = cross_val_score(
        pipeline,
        sentences,
        labels,
        cv=cv,
        scoring="accuracy"
    )

    print(f"\n{folds}-Fold Cross-Validation Results:")

    for i, score in enumerate(scores, start=1):
        print(f"Fold {i} Accuracy: {score * 100:.2f}%")

    print(
        "\nAverage Cross-Validation Accuracy:",
        round(scores.mean() * 100, 2),
        "%"
    )


# 6. Split data into training and testing sets
X_train_text, X_test_text, y_train, y_test = train_test_split(
    sentences,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)


# 7. Convert text into numerical features using TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(1, 2))

X_train = vectorizer.fit_transform(X_train_text)

X_test = vectorizer.transform(X_test_text)


# 8. Create and train Logistic Regression model
model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)


# 9. Evaluate the final model
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n80:20 Train-Test Split Accuracy:",
      round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))


# 10. Save the trained model and vectorizer
joblib.dump(
    {
        "model": model,
        "vectorizer": vectorizer
    },
    MODEL_PATH
)

print("\nModel successfully saved!")
print("Saved at:", MODEL_PATH)
