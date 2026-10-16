import React from 'react';
export default function ComparisonTable({ models = [] }) {
  return (
    <div className="comparison-table-wrap">
      <table className="comparison-table">
        <thead><tr><th>Metric</th>{models.map((model) => <th key={model.name}>{model.name}</th>)}</tr></thead>
        <tbody><tr><th scope="row">Score</th>{models.map((model) => <td key={model.name}>{model.score ?? '—'}</td>)}</tr></tbody>
      </table>
    </div>
  );
}
