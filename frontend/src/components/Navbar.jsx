export default function Navbar() {
  return (
    <header className="site-header">
      <a className="brand" href="/">ModelMatrix</a>
      <nav className="site-nav" aria-label="Main navigation">
        <a href="/">Home</a>
        <a href="/compare">Compare</a>
        <a href="/benchmark">Benchmark</a>
        <a href="/about">About</a>
      </nav>
    </header>
  );
}
