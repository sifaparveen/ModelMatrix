import React from 'react';
export default function ScoreCard({ label = 'Accuracy', value = '—' }) {
  return <article className="score-card"><span>{label}</span><strong>{value}</strong></article>;
}
