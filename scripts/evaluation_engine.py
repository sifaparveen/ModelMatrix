
import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = (
    PROJECT_ROOT / "data" / "processed" / "arc_challenge_100.csv"
)
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def normalize_answer(answer):
    if answer is None or pd.isna(answer):
        return None

    return str(answer).strip().upper()


def evaluate_prediction(row, predicted_answer):
    choices = json.loads(row["choices_json"])

    valid_labels = {
        normalize_answer(label)
        for label in choices
    }

    predicted = normalize_answer(predicted_answer)
    correct = normalize_answer(row["correct_answer_label"])

    prediction_valid = predicted in valid_labels
    is_correct = prediction_valid and predicted == correct

    return {
        "predicted_answer": predicted,
        "correct_answer": correct,
        "prediction_valid": prediction_valid,
        "is_correct": is_correct,
        "score": int(is_correct),
    }


def evaluate_model(df, model_name, predictions):
    if len(df) != len(predictions):
        raise ValueError(
            f"{model_name}: expected {len(df)} predictions, "
            f"received {len(predictions)}"
        )

    results = []

    for (_, row), prediction in zip(
        df.iterrows(), predictions
    ):
        evaluation = evaluate_prediction(row, prediction)

        results.append({
            "question_id": row["question_id"],
            "model": model_name,
            **evaluation,
        })

    return pd.DataFrame(results)


def main():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(DATASET_PATH)

    df = pd.read_csv(DATASET_PATH)

    required = {
        "question_id",
        "choices_json",
        "correct_answer_label",
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Temporary baseline: predict the first available option.
    # This is NOT a real AI model.
    predictions = []

    for _, row in df.iterrows():
        choices = json.loads(row["choices_json"])
        first_label = next(iter(choices))
        predictions.append(first_label)

    results = evaluate_model(
        df,
        model_name="First-Option Baseline",
        predictions=predictions,
    )

    results_path = OUTPUT_DIR / "baseline_results.csv"
    results.to_csv(results_path, index=False)

    summary = (
        results.groupby("model")
        .agg(
            questions_evaluated=("question_id", "count"),
            valid_predictions=("prediction_valid", "sum"),
            correct_answers=("is_correct", "sum"),
            accuracy=("score", "mean"),
        )
        .reset_index()
    )

    summary["accuracy_percent"] = (
        summary["accuracy"] * 100
    ).round(2)

    summary_path = OUTPUT_DIR / "baseline_summary.csv"
    summary.to_csv(summary_path, index=False)

    print("\nBaseline summary:")
    print(summary.to_string(index=False))

    print(f"\nIndividual results: {results_path}")
    print(f"Summary results: {summary_path}")


if __name__ == "__main__":
    main()
