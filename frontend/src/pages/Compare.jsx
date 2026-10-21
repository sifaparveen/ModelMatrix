
import React, { useEffect, useState } from 'react';
import ComparisonTable from '../components/ComparisonTable.jsx';
import ModelCard from '../components/ModelCard.jsx';
import PromptInput from '../components/PromptInput.jsx';
import ScoreCard from '../components/ScoreCard.jsx';
import { getBackendHealth, evaluateSample, generateResponse } from '../api.js';

const demoModels = [
  {
    name: 'ChatGPT',
    response:
      'Demonstration response. Connect a ChatGPT API to display a live answer here.',
    score: '87/100',
    accuracy: '87%',
    speed: 'Fast',
    clarity: '90/100',
  },
  {
    name: 'Gemini',
    response:
      'Enter a prompt above and submit it to generate a live Gemini response.',
    score: '84/100',
    accuracy: '84%',
    speed: 'Fast',
    clarity: '88/100',
  },
  {
    name: 'Claude',
    response:
      'Demonstration response. Connect a Claude API to display a live answer here.',
    score: '89/100',
    accuracy: '89%',
    speed: 'Moderate',
    clarity: '92/100',
  },
];

export default function Compare() {
  const [prompt, setPrompt] = useState(
    'Explain artificial intelligence in simple words.'
  );

  const [submittedPrompt, setSubmittedPrompt] = useState('');

  const [backendStatus, setBackendStatus] = useState(
    'Checking backend...'
  );

  const [geminiResponse, setGeminiResponse] = useState('');
  const [generationLoading, setGenerationLoading] = useState(false);
  const [generationError, setGenerationError] = useState('');

  const [evaluation, setEvaluation] = useState(null);
  const [evaluationLoading, setEvaluationLoading] = useState(false);
  const [evaluationError, setEvaluationError] = useState('');

  useEffect(() => {
    getBackendHealth()
      .then(() => setBackendStatus('Connected'))
      .catch(() => setBackendStatus('Not connected'));
  }, []);

  async function handleSubmit(value) {
    const cleanedPrompt = value.trim();

    if (!cleanedPrompt || generationLoading) {
      return;
    }

    setSubmittedPrompt(cleanedPrompt);
    setGeminiResponse('');
    setGenerationError('');
    setGenerationLoading(true);

    try {
      const result = await generateResponse(cleanedPrompt);
      setGeminiResponse(result.response);
    } catch (error) {
      setGenerationError(
        error.message || 'Gemini could not generate a response.'
      );
    } finally {
      setGenerationLoading(false);
    }
  }

  async function handleGeminiEvaluation() {
    setEvaluationLoading(true);
    setEvaluationError('');
    setEvaluation(null);

    try {
      const result = await evaluateSample();
      setEvaluation(result);
    } catch (error) {
      setEvaluationError(
        error.message || 'The Gemini evaluation failed.'
      );
    } finally {
      setEvaluationLoading(false);
    }
  }

  return (
    <main className="site-main compare-page">
      <p role="status">
        Backend status: {backendStatus}
      </p>

      <section className="compare-intro">
        <span className="eyebrow">MODELMATRIX WORKSPACE</span>
        <h1>Compare AI models</h1>
        <p>
          Explore responses side by side and compare illustrative
          evaluation scores in one place.
        </p>
      </section>

      <section className="compare-prompt-panel">
        <PromptInput
          value={prompt}
          onChange={setPrompt}
          onSubmit={handleSubmit}
        />
      </section>

      <div className="demo-notice">
        <span aria-hidden="true">ⓘ</span>
        Gemini generates a live response when you submit a prompt.
        ChatGPT and Claude responses and the displayed scores are
        demonstration data.
      </div>

      <section className="results-section" aria-live="polite">
        <div className="section-heading">
          <div>
            <h2>Model responses</h2>
            <p>
              Prompt:{' '}
              <strong>
                {submittedPrompt || 'Submit a prompt to begin.'}
              </strong>
            </p>
          </div>
          <span className="sample-badge">
            Gemini: Live API
          </span>
        </div>

        {generationLoading && (
          <p role="status">Gemini is generating a response...</p>
        )}

        {generationError && (
          <p role="alert">
            Gemini request failed: {generationError}
          </p>
        )}

        <div className="compare-model-grid">
          {demoModels.map((model) => (
            <ModelCard
              key={model.name}
              name={model.name}
              response={
                model.name === 'Gemini'
                  ? geminiResponse || model.response
                  : model.response
              }
            />
          ))}
        </div>
      </section>

      <section className="results-section">
        <div className="section-heading">
          <div>
            <h2>Live Gemini benchmark evaluation</h2>
            <p>
              Run Gemini against an ARC-Challenge question and
              compare its answer with the dataset's correct answer.
              This is separate from the prompt above.
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={handleGeminiEvaluation}
          disabled={evaluationLoading}
        >
          {evaluationLoading
            ? 'Evaluating...'
            : 'Run Gemini Evaluation'}
        </button>

        {evaluationError && (
          <p role="alert">
            Evaluation failed: {evaluationError}
          </p>
        )}

        {evaluation && (
          <div className="evaluation-result">
            <h3>Evaluation result</h3>

            <p>
              <strong>Question ID:</strong>{' '}
              {evaluation.question_id}
            </p>

            <p>
              <strong>Question:</strong>{' '}
              {evaluation.question}
            </p>

            <h4>Answer choices</h4>
            <ul>
              {evaluation.choices.map((choice) => (
                <li key={choice.label}>
                  <strong>{choice.label}:</strong>{' '}
                  {choice.text}
                </li>
              ))}
            </ul>

            <p>
              <strong>Model:</strong> {evaluation.model}
            </p>

            <p>
              <strong>Gemini response:</strong>{' '}
              {evaluation.model_output || 'No response text'}
            </p>

            <p>
              <strong>Predicted answer:</strong>{' '}
              {evaluation.predicted_answer ?? 'Could not identify'}
            </p>

            <p>
              <strong>Correct answer:</strong>{' '}
              {evaluation.correct_answer}
            </p>

            <p role="status">
              <strong>Result:</strong>{' '}
              {evaluation.is_correct ? 'Correct' : 'Incorrect'}
            </p>
          </div>
        )}
      </section>

      <section className="results-section">
        <div className="section-heading">
          <div>
            <h2>Evaluation overview</h2>
            <p>
              These scores are illustrative demonstration data,
              not results from the live benchmark evaluation.
            </p>
          </div>
        </div>

        <div className="score-grid">
          {demoModels.map((model) => (
            <ScoreCard
              key={model.name}
              label={`${model.name} · Sample score`}
              value={model.score}
            />
          ))}
        </div>
      </section>

      <section className="results-section">
        <div className="section-heading">
          <div>
            <h2>Side-by-side metrics</h2>
            <p>
              Example metrics for planning the future evaluation interface.
            </p>
          </div>
        </div>

        <div className="comparison-table-wrap">
          <table className="comparison-table">
            <thead>
              <tr>
                <th scope="col">Metric</th>
                {demoModels.map((model) => (
                  <th scope="col" key={model.name}>
                    {model.name}
                  </th>
                ))}
              </tr>
            </thead>

            <tbody>
              <tr>
                <th scope="row">Sample score</th>
                {demoModels.map((model) => (
                  <td key={model.name}>{model.score}</td>
                ))}
              </tr>

              <tr>
                <th scope="row">Illustrative accuracy</th>
                {demoModels.map((model) => (
                  <td key={model.name}>{model.accuracy}</td>
                ))}
              </tr>

              <tr>
                <th scope="row">Response speed</th>
                {demoModels.map((model) => (
                  <td key={model.name}>{model.speed}</td>
                ))}
              </tr>

              <tr>
                <th scope="row">Clarity</th>
                {demoModels.map((model) => (
                  <td key={model.name}>{model.clarity}</td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
