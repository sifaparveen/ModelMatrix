import ComparisonTable from '../components/ComparisonTable.jsx';
import ModelCard from '../components/ModelCard.jsx';
import PromptInput from '../components/PromptInput.jsx';

export default function Compare() {
  return <main className="site-main"><h1>Compare models</h1><PromptInput /><section aria-label="Model results"><ModelCard /><ComparisonTable /></section></main>;
}
