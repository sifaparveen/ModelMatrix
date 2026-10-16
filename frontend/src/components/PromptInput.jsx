import React from 'react';
export default function PromptInput({ value = '', onChange, onSubmit }) {
  return (
    <form onSubmit={(event) => { event.preventDefault(); onSubmit?.(value); }}>
      <label htmlFor="prompt">Your prompt</label>
      <textarea id="prompt" value={value} onChange={(event) => onChange?.(event.target.value)} rows={4} placeholder="What would you like to compare?" />
      <button type="submit">Compare models</button>
    </form>
  );
}
