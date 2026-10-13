
from pathlib import Path
import json

import pandas as pd
from datasets import load_dataset


# -------------------------------
# 1. Project configuration
# -------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "reports"

for folder in (RAW_DIR, PROCESSED_DIR, REPORT_DIR):
    folder.mkdir(parents=True, exist_ok=True)

DATASET_NAME = "allenai/ai2_arc"
CONFIG_NAME = "ARC-Challenge"
SPLIT_NAME = "test"
SAMPLE_SIZE = 100
RANDOM_SEED = 42


# -------------------------------
# 2. Load the existing dataset
# -------------------------------

print("Loading AI2 ARC dataset...")

dataset = load_dataset(
    DATASET_NAME,
    CONFIG_NAME,
    split=SPLIT_NAME,
)

print(f"Source rows: {len(dataset)}")

# Select a reproducible sample for the prototype.
sample_size = min(SAMPLE_SIZE, len(dataset))

sample = dataset.shuffle(
    seed=RANDOM_SEED
).select(range(sample_size))


# -------------------------------
# 3. Normalize the records
# -------------------------------

records = []

for item in sample:
    question_id = str(item["id"]).strip()
    question = str(item["question"]).strip()

    choices_data = item["choices"]
    labels = choices_data["label"]
    texts = choices_data["text"]

    # Ensure each answer label matches its choice text.
    if len(labels) != len(texts) or not labels:
        continue

    choices = {
        str(label).strip(): str(text).strip()
        for label, text in zip(labels, texts)
    }

    answer_key = str(item["answerKey"]).strip()

    # Normally answerKey matches a choice label.
    # Handle numeric keys only when they map unambiguously.
    if answer_key in choices:
        correct_label = answer_key
    elif answer_key.isdigit():
        numeric_matches = [
            label
            for label in choices
            if label.isdigit()
            and int(label) == int(answer_key)
        ]

        if len(numeric_matches) == 1:
            correct_label = numeric_matches[0]
        else:
            continue
    else:
        continue

    if not question_id or not question:
        continue

    records.append({
        "question_id": question_id,
        "subject": "Science",
        "difficulty": "not_provided",
        "benchmark_subset": CONFIG_NAME,
        "question": question,
        "choices_json": json.dumps(
            choices, ensure_ascii=False
        ),
        "correct_answer_label": correct_label,
        "correct_answer_text": choices[correct_label],
        "source_dataset": DATASET_NAME,
        "source_config": CONFIG_NAME,
        "source_split": SPLIT_NAME,
        "source_license": "CC-BY-SA-4.0",
    })


# -------------------------------
# 4. Build and validate the table
# -------------------------------

df = pd.DataFrame(records)

required_columns = [
    "question_id",
    "question",
    "choices_json",
    "correct_answer_label",
    "correct_answer_text",
]

if df.empty:
    raise ValueError("No valid records were produced.")

missing_columns = set(required_columns) - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

# Detect missing values in required fields.
missing_counts = df[required_columns].isna().sum()

# Remove blank required text fields.
for column in required_columns:
    if df[column].dtype == "object":
        df[column] = df[column].astype("string").str.strip()

df = df.dropna(subset=required_columns)

for column in required_columns:
    df = df[df[column].astype(str).str.len() > 0]

# Remove duplicate IDs and duplicate question text.
df = df.drop_duplicates(subset="question_id")
df = df.drop_duplicates(subset="question")

# Verify every correct answer exists in the choice dictionary.
def correct_answer_is_valid(row):
    choices = json.loads(row["choices_json"])

    return (
        row["correct_answer_label"] in choices
        and choices[row["correct_answer_label"]]
        == row["correct_answer_text"]
    )


df = df[df.apply(correct_answer_is_valid, axis=1)]

# Keep a stable, predictable order.
df = df.sort_values("question_id").reset_index(drop=True)


# -------------------------------
# 5. Export standardized dataset
# -------------------------------

output_path = PROCESSED_DIR / "arc_challenge_100.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

quality_report = {
    "source_dataset": DATASET_NAME,
    "configuration": CONFIG_NAME,
    "source_split": SPLIT_NAME,
    "requested_sample_size": SAMPLE_SIZE,
    "valid_rows": len(df),
    "unique_question_ids": int(df["question_id"].nunique()),
    "unique_questions": int(df["question"].nunique()),
    "missing_values_before_cleanup": {
        str(key): int(value)
        for key, value in missing_counts.items()
    },
    "output_file": str(output_path),
}

report_path = REPORT_DIR / "dataset_quality_report.json"
report_path.write_text(
    json.dumps(quality_report, indent=2),
    encoding="utf-8",
)

print("\nDataset preparation complete.")
print(f"Valid questions: {len(df)}")
print(f"CSV saved to: {output_path}")
print(f"Quality report saved to: {report_path}")

print("\nSample records:")
print(
    df[
        [
            "question_id",
            "question",
            "correct_answer_label",
            "correct_answer_text",
        ]
    ].head(3).to_string(index=False)
)
