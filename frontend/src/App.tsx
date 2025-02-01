// src/App.tsx
import React from 'react';
import Header from './components/Header';
import Title from './components/Title';
import ProductList from './components/ProductList';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="App">
      <Header />
      <Title />
      <ProductList />
    </div>
  );
};

export default App;
