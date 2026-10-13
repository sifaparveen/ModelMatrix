import json
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "arc_challenge_100.csv"
df = pd.read_csv(DATASET_PATH)

print("Dataset shape:", df.shape)
print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicate question IDs:",
      df["question_id"].duplicated().sum())

row = df.iloc[0]
choices = json.loads(row["choices_json"])

print("\nSample question:")
print(row["question"])

print("\nOptions:")
for label, text in choices.items():
    print(f"{label}. {text}")

print("\nCorrect answer:",
      row["correct_answer_label"],
      row["correct_answer_text"])
