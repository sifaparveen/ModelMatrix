
import React from 'react';

const models = [
  {
    name: 'ChatGPT',
    symbol: '✳',
    className: 'chatgpt',
    response:
      'AI is like a smart computer that can understand, learn and solve problems.',
    tag: 'Detailed',
  },
  {
    name: 'Gemini',
    symbol: '✦',
    className: 'gemini',
    response:
      'AI helps machines learn from data and make decisions like humans.',
    tag: 'Concise',
  },
  {
    name: 'Claude',
    symbol: '✺',
    className: 'claude',
    response:
      'AI refers to systems that can think, reason and create, similar to humans.',
    tag: 'Thoughtful',
  },
];

export default function Hero() {
  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">AI MODEL COMPARISON PLATFORM</span>

          <h1>
            Find the Right AI.
            <br />
            <span>Compare. Evaluate. Decide.</span>
          </h1>

          <p>
            Compare AI model responses, explore benchmark scores, and discover
            which model works best for your prompts.
          </p>

          <a className="primary-button" href="/compare">
            Start Comparing <span aria-hidden="true">→</span>
          </a>
        </div>

        <div className="comparison-preview">
          <div className="preview-heading">
            <div className="preview-title">
              <span className="mini-logo">M</span>
              <strong>Model Comparison</strong>
            </div>
            <span className="live-status">
              <span /> Preview
            </span>
          </div>

          <div className="prompt-box">
            <label htmlFor="sample-prompt">Your prompt</label>
            <div id="sample-prompt" className="sample-prompt">
              Explain artificial intelligence in simple words.
            </div>
          </div>

          <div className="model-grid">
            {models.map((model) => (
              <article
                className={`model-card ${model.className}`}
                key={model.name}
              >
                <div className="model-heading">
                  <span className="model-symbol" aria-hidden="true">
                    {model.symbol}
                  </span>
                  <strong>{model.name}</strong>
                </div>

                <p>{model.response}</p>
                <span className="model-tag">{model.tag}</span>
              </article>
            ))}
          </div>
          <p className="preview-note">
            Illustrative responses · Sample content for demonstration
          </p>
        </div>
      </section>

      <section className="features" aria-label="Platform features">
        <article className="feature-item">
          <span className="feature-icon purple">⚖</span>
          <div>
            <h3>Side-by-Side Comparison</h3>
            <p>See how different AI models respond to the same prompt.</p>
          </div>
        </article>

        <article className="feature-item">
          <span className="feature-icon green">▥</span>
          <div>
            <h3>Benchmark Evaluation</h3>
            <p>Explore performance scores based on custom benchmarks.</p>
          </div>
        </article>

        <article className="feature-item">
          <span className="feature-icon pink">⚙</span>
          <div>
            <h3>Custom Dataset</h3>
            <p>Use our dataset for fair and consistent evaluation.</p>
          </div>
        </article>

        <article className="feature-item">
          <span className="feature-icon blue">◎</span>
          <div>
            <h3>Make Better Decisions</h3>
            <p>Find the AI that fits your needs, not just the hype.</p>
          </div>
        </article>
      </section>

      <section className="why-section">
        <div className="why-intro">
          <span className="eyebrow">WHY MODELMATRIX?</span>
          <h2>
            Smarter comparison.
            <br />
            Better results.
          </h2>
          <p>
            ModelMatrix gives you a simple and effective way to evaluate AI
            models with real prompts, clear metrics and transparent results.
          </p>
        </div>

        <article className="benefit-item">
          <span className="benefit-icon purple">ϟ</span>
          <h3>Save Time</h3>
          <p>
            Compare model responses in one place, without switching between
            platforms.
          </p>
        </article>

        <article className="benefit-item">
          <span className="benefit-icon blue">⬡</span>
          <h3>Be Confident</h3>
          <p>
            Use objective benchmarks and evaluation metrics for reliable
            results.
          </p>
        </article>

        <article className="benefit-item">
          <span className="benefit-icon green">♙</span>
          <h3>Built for Everyone</h3>
          <p>
            Whether you are a student, creator or professional, find the best
            AI for your use case.
          </p>
        </article>
      </section>
    </>
  );
}
