import React from 'react';
import { NavLink, Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <header className="site-header">
      <Link className="brand" to="/" aria-label="ModelMatrix home">
        <span className="brand-mark" aria-hidden="true">M</span>
        <span>
          Model<span className="brand-accent">Matrix</span>
        </span>
      </Link>

      <nav className="site-nav" aria-label="Main navigation">
        <NavLink to="/" end>
          Home
        </NavLink>

        <NavLink to="/compare">
          Compare
        </NavLink>

        <NavLink to="/benchmark">
          Benchmarks
        </NavLink>

        <NavLink to="/about">
          About
        </NavLink>
      </nav>

      <div className="nav-actions">
        <button
          className="theme-toggle"
          type="button"
          aria-label="Theme toggle preview"
          title="Theme toggle (visual preview)"
        >
          ☼
        </button>

        <Link className="nav-cta" to="/compare">
          Get Started
        </Link>
      </div>
    </header>
  );
}