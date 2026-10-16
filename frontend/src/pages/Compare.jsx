
import React, { useState } from 'react';
import ComparisonTable from '../components/ComparisonTable.jsx';
import ModelCard from '../components/ModelCard.jsx';
import PromptInput from '../components/PromptInput.jsx';
import ScoreCard from '../components/ScoreCard.jsx';

const demoModels = [
  {
    name: 'ChatGPT',
    response:
      'Artificial intelligence (AI) is technology that enables computers to perform tasks such as understanding language, solving problems, and generating content.',
    score: '87/100',
    accuracy: '87%',
    speed: 'Fast',
    clarity: '90/100',
  },
  {
    name: 'Gemini',
    response:
      'AI allows computers to learn from information, recognize patterns, answer questions, and help people solve everyday problems.',
    score: '84/100',
    accuracy: '84%',
    speed: 'Fast',
    clarity: '88/100',
  },
  {
    name: 'Claude',
    response:
      'Artificial intelligence refers to computer systems designed to perform tasks that usually require human intelligence, including reasoning, writing, and understanding.',
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
  const [submittedPrompt, setSubmittedPrompt] = useState(
    'Explain artificial intelligence in simple words.'
  );

  function handleSubmit(value) {
    const cleanedPrompt = value.trim();

    if (!cleanedPrompt) {
      return;
    }

    setSubmittedPrompt(cleanedPrompt);
  }

  return (
    <main className="site-main compare-page">
      <section className="compare-intro">
        <span className="eyebrow">MODELMATRIX WORKSPACE</span>
        <h1>Compare AI models</h1>
        <p>
          Explore responses side by side and compare illustrative evaluation
          scores in one place.
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
        Demonstration mode: the model responses and scores below are sample
        data. Submitting a prompt does not call live AI models.
      </div>

      <section className="results-section" aria-live="polite">
        <div className="section-heading">
          <div>
            <h2>Model responses</h2>
            <p>
              Prompt: <strong>{submittedPrompt}</strong>
            </p>
          </div>
          <span className="sample-badge">Sample results</span>
        </div>

        <div className="compare-model-grid">
          {demoModels.map((model) => (
            <ModelCard
              key={model.name}
              name={model.name}
              response={model.response}
            />
          ))}
        </div>
      </section>

      <section className="results-section">
        <div className="section-heading">
          <div>
            <h2>Evaluation overview</h2>
            <p>Illustrative scores for the demonstration dataset.</p>
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
            <p>Example metrics for planning the future evaluation interface.</p>
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
