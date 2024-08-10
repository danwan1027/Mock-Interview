import {useEffect, useRef, useState} from 'react';
import './App.css';
import Avatar from './components/Avatar';
import Home from './components/Home';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/avatar" element={<Avatar />} />
      </Routes>
    </Router>
  );
}

export default App;
