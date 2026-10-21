import json
import os
import re
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from google import genai


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "arc_challenge_100.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
RESULTS_PATH = OUTPUT_DIR / "gemini_results.csv"
SUMMARY_PATH = OUTPUT_DIR / "gemini_summary.csv"

load_dotenv(PROJECT_ROOT / "arc-evaluation-backend" / ".env")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def normalize_answer(answer):
    if answer is None or pd.isna(answer):
        return None
    return str(answer).strip().upper()


def parse_answer(model_output, labels):
    """Extract a choice label from Gemini's response, if it returned one."""
    output = (model_output or "").strip().upper()
    alternatives = "|".join(
        re.escape(label)
        for label in sorted(labels, key=len, reverse=True)
    )
    match = re.search(rf"(?<![A-Z0-9])({alternatives})(?![A-Z0-9])", output)
    return match.group(1) if match else None


def request_gemini_predictions(df, client):
    predictions = []
    model_outputs = []

    for index, row in df.iterrows():
        choices = json.loads(row["choices_json"])
        choices_text = "\n".join(
            f"{label}: {text}" for label, text in choices.items()
        )
        prompt = (
            "Answer this multiple-choice science question. Choose the correct "
            "provided answer label. Return only the label, with no explanation.\n\n"
            f"Question: {row['question']}\n\nChoices:\n{choices_text}"
        )

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
        except Exception as exc:
            question_id = row.get("question_id", index)
            raise RuntimeError(
                f"Gemini request failed for question {question_id}: {exc}"
            ) from exc

        model_output = (response.text or "").strip()
        model_outputs.append(model_output)
        predictions.append(parse_answer(model_output, list(choices)))

        print(f"Evaluated {len(predictions)}/{len(df)} questions", flush=True)

    return predictions, model_outputs


def evaluate_predictions(df, predictions, model_outputs):
    results = []

    for (_, row), prediction, model_output in zip(
        df.iterrows(), predictions, model_outputs
    ):
        choices = json.loads(row["choices_json"])
        valid_labels = {normalize_answer(label) for label in choices}
        predicted = normalize_answer(prediction)
        correct = normalize_answer(row["correct_answer_label"])
        prediction_valid = predicted in valid_labels
        is_correct = prediction_valid and predicted == correct

        results.append({
            "question_id": row["question_id"],
            "model": MODEL_NAME,
            "model_output": model_output,
            "predicted_answer": predicted,
            "correct_answer": correct,
            "prediction_valid": prediction_valid,
            "is_correct": is_correct,
            "score": int(is_correct),
        })

    return pd.DataFrame(results)


def main():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Benchmark CSV not found: {DATASET_PATH}. "
            "Run scripts/prepare_dataset.py first."
        )

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to "
            "arc-evaluation-backend/.env or your environment."
        )

    df = pd.read_csv(DATASET_PATH)
    required = {
        "question_id",
        "question",
        "choices_json",
        "correct_answer_label",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Benchmark CSV is missing columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("Benchmark CSV contains no questions.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=api_key)
    print(f"Evaluating {len(df)} questions with {MODEL_NAME}...")
    predictions, model_outputs = request_gemini_predictions(df, client)
    results = evaluate_predictions(df, predictions, model_outputs)
    results.to_csv(RESULTS_PATH, index=False)

    summary = pd.DataFrame([{
        "model": MODEL_NAME,
        "questions_evaluated": len(results),
        "valid_predictions": int(results["prediction_valid"].sum()),
        "correct_answers": int(results["is_correct"].sum()),
        "accuracy": results["score"].mean(),
        "accuracy_percent": round(results["score"].mean() * 100, 2),
    }])
    summary.to_csv(SUMMARY_PATH, index=False)

    print("\nGemini evaluation summary:")
    print(summary.to_string(index=False))
    print(f"\nIndividual results: {RESULTS_PATH}")
    print(f"Summary results: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
