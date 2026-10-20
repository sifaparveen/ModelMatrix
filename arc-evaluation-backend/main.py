
import os
import re
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai

import pandas as pd
import json

load_dotenv()

app = FastAPI(title="AI2 ARC Evaluation API")

BASE_DIR = Path(__file__).resolve().parent
BENCHMARK_CSV_PATH = BASE_DIR.parent / "data" / "processed" / "arc_challenge_100.csv"


@lru_cache(maxsize=1)
def get_benchmark_rows():
    if not BENCHMARK_CSV_PATH.exists():
        raise FileNotFoundError(
            f"Benchmark CSV not found: {BENCHMARK_CSV_PATH}"
        )

    df = pd.read_csv(BENCHMARK_CSV_PATH)

    required_columns = {
        "question_id",
        "question",
        "choices_json",
        "correct_answer_label",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Benchmark CSV is missing columns: {sorted(missing_columns)}"
        )

    rows = []

    for _, row in df.iterrows():
        choices_dict = json.loads(row["choices_json"])

        rows.append({
            "id": str(row["question_id"]),
            "question": str(row["question"]),
            "choices": [
                {"label": str(label), "text": str(text)}
                for label, text in choices_dict.items()
            ],
            "answerKey": str(row["correct_answer_label"]).strip(),
        })

    return rows


@app.get("/")
def home():
    return {"message": "AI2 ARC Evaluation API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/questions/sample")
def sample_question():
    try:
        item = get_benchmark_rows()[0]
        return {
            "id": item["id"],
            "question": item["question"],
            "choices": item["choices"],
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/evaluate/sample")
def evaluate_sample():
    try:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="GEMINI_API_KEY is missing from .env",
            )

        item = get_benchmark_rows()[0]
        labels = [choice["label"] for choice in item["choices"]]
        texts = [choice["text"] for choice in item["choices"]]

        choices_text = "\n".join(
            f"{label}: {text}"
            for label, text in zip(labels, texts)
        )

        prompt = (
            "Answer this multiple-choice science question. "
            "Choose one of the provided labels. "
            "Return only the answer label, such as A, B, C, or D.\n\n"
            f"Question: {item['question']}\n\n"
            f"Choices:\n{choices_text}"
        )

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )

        model_output = (response.text or "").strip()

        match = re.search(
            r"\b(" + "|".join(re.escape(label) for label in labels) + r")\b",
            model_output.upper(),
        )

        predicted_answer = match.group(1) if match else None
        correct_answer = item["answerKey"]

        return {
            "question_id": item["id"],
            "question": item["question"],
            "choices": [
                {"label": label, "text": text}
                for label, text in zip(labels, texts)
            ],
            "model": "gemini-3.8-flash",
            "model_output": model_output,
            "predicted_answer": predicted_answer,
            "correct_answer": correct_answer,
            "is_correct": (
                predicted_answer == correct_answer
                if predicted_answer is not None
                else False
            ),
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@app.get("/benchmark/questions")
def benchmark_questions():
    try:
        rows = get_benchmark_rows()

        return {
            "dataset": "arc_challenge_100",
            "total_questions": len(rows),
            "questions": [
                {
                    "id": item["id"],
                    "question": item["question"],
                    "choices": item["choices"],
                }
                for item in rows
            ],
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/evaluate/benchmark")
def evaluate_benchmark():
    try:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="GEMINI_API_KEY is missing from .env",
            )

        rows = get_benchmark_rows()
        client = genai.Client(api_key=api_key)

        results = []
        correct_count = 0
        valid_predictions = 0

        for item in rows:
            labels = [choice["label"] for choice in item["choices"]]

            choices_text = "\n".join(
                f"{choice['label']}: {choice['text']}"
                for choice in item["choices"]
            )

            prompt = (
                "Answer this multiple-choice science question. "
                "Choose one provided label. Return only the label.\n\n"
                f"Question: {item['question']}\n\n"
                f"Choices:\n{choices_text}"
            )

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
            )

            model_output = (response.text or "").strip()

            match = re.fullmatch(
                r"\s*([A-Z])[\.\)]?\s*",
                model_output.upper(),
            )

            predicted_answer = match.group(1) if match else None
            correct_answer = item["answerKey"]

            is_correct = predicted_answer == correct_answer

            if predicted_answer in labels:
                valid_predictions += 1

            if is_correct:
                correct_count += 1

            results.append({
                "question_id": item["id"],
                "predicted_answer": predicted_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "model_output": model_output,
            })

        total = len(rows)

        return {
            "dataset": "arc_challenge_100",
            "model": "gemini-3.8-flash",
            "total_questions": total,
            "valid_predictions": valid_predictions,
            "correct_answers": correct_count,
            "accuracy_percent": round(
                correct_count / total * 100, 2
            ) if total else 0,
            "results": results,
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
