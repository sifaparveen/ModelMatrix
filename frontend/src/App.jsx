import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home.jsx';
import Compare from './pages/Compare.jsx';
import Navbar from './components/Navbar.jsx';
import Footer from './components/Footer.jsx';
import './App.css';

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Navbar />

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/compare" element={<Compare />} />
        </Routes>

        <Footer />
      </div>
    </BrowserRouter>
  );
}