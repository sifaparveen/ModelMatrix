
const API_BASE_URL = 'http://127.0.0.1:8000';

export async function getBackendHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error(`Backend health check failed: ${response.status}`);
  }

  return response.json();
}

export async function getSampleQuestion() {
  const response = await fetch(`${API_BASE_URL}/questions/sample`);

  if (!response.ok) {
    throw new Error(`Could not load sample question: ${response.status}`);
  }

  return response.json();
}

export async function evaluateSample() {
  const response = await fetch(`${API_BASE_URL}/evaluate/sample`);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Gemini evaluation failed.');
  }

  return data;
}


export async function generateResponse(prompt) {
  const response = await fetch('http://127.0.0.1:8000/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Failed to generate a response.');
  }

  return data;
}
