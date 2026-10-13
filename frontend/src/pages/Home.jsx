import Footer from '../components/Footer.jsx';
import Hero from '../components/Hero.jsx';
import Navbar from '../components/Navbar.jsx';

export default function Home() {
  return <div className="app-shell"><Navbar /><main className="site-main"><Hero /></main><Footer /></div>;
}
