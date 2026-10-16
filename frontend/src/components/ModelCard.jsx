import React from 'react';
export default function ModelCard({ name = 'Model name', response = 'Model response will appear here.' }) {
  return <article className="model-card"><h2>{name}</h2><p>{response}</p></article>;
}
