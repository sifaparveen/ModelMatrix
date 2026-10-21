# ModelMatrix

ModelMatrix is a React and Vite frontend for comparing AI model responses and evaluation results.

## Getting started

```sh
cd frontend
npm install
npm run dev
```

## Project structure

- `frontend/` contains the React and Vite application.
- `data/` contains raw and processed datasets.
- `scripts/` contains dataset preparation, inspection, and evaluation scripts.
- `reports/` contains generated data quality reports.

Run the Python scripts from the project root with:

```sh
python scripts/prepare_dataset.py
python scripts/inspect_dataset.py
python scripts/evaluation_engine.py
```

`evaluation_engine.py` sends each question and its answer choices from `data/processed/arc_challenge_100.csv` to Gemini. It writes per-question responses and parsed answers to `data/processed/gemini_results.csv` and an accuracy summary to `data/processed/gemini_summary.csv`. A 100-question run makes 100 Gemini API calls and may incur API usage. Set `GEMINI_MODEL` to use a different Gemini model; the default is `gemini-3.8-flash`.

The script loads `GEMINI_API_KEY` from `arc-evaluation-backend/.env`. Install the Python packages in `requirements.txt` in the active environment before running it.
