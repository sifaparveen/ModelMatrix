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
