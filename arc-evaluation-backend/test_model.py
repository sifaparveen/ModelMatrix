import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

models = ["gemini-3.8-flash", "gemini-2.5-flash"]

for model in models:
    try:
        print(f"Testing model: {model}")

        response = client.models.generate_content(
            model=model,
            contents=(
                "Which gas do plants absorb during "
                "photosynthesis? Answer briefly."
            ),
        )

        print("Model API call successful!")
        print(response.text)
        break

    except errors.APIError as exc:
        print(f"{model} failed: {exc}")
else:
    print("Neither model worked. Check model availability and API quota.")
