
import os
import re
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from datasets import load_from_disk, load_dataset
from google import genai

load_dotenv()

app = FastAPI(title="AI2 ARC Evaluation API")

DATASET_PATH = Path("data/arc_challenge")


@lru_cache(maxsize=1)
def get_dataset():
    if DATASET_PATH.exists():
        return load_from_disk(str(DATASET_PATH))
    return load_dataset("allenai/ai2_arc", "ARC-Challenge")


@app.get("/")
def home():
    return {"message": "AI2 ARC Evaluation API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/questions/sample")
def sample_question():
    try:
        dataset = get_dataset()
        item = dataset["train"][0]

        return {
            "id": item["id"],
            "question": item["question"],
            "choices": [
                {"label": label, "text": text}
                for label, text in zip(
                    item["choices"]["label"],
                    item["choices"]["text"],
                )
            ],
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

        dataset = get_dataset()
        item = dataset["train"][0]

        labels = item["choices"]["label"]
        texts = item["choices"]["text"]

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
