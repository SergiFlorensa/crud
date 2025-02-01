// src/components/ProductList.tsx
import React, { useEffect, useState } from 'react';
import ProductCard from './ProductCard';

type Product = {
  name: string;
  description: string;
  price: number;
};

const ProductList: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Llamada a la API para obtener los productos
  const fetchProducts = async () => {
    try {
      const response = await fetch('https://my-fastapi-app-production-6bb9.up.railway.app/products/');
      if (!response.ok) {
        throw new Error('Failed to fetch products');
      }
      const data = await response.json();
      setProducts(data);
    } catch (err) {
      setError('Failed to load products');
      console.error(err);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div className="product-list">
      {error && <p>{error}</p>}
      {products.length > 0 ? (
        <div className="product-grid">
          {products.map((product, index) => (
            <ProductCard key={index} product={product} />
          ))}
        </div>
      ) : (
        <p>No products available</p>
      )}
    </div>
  );
};

export default ProductList;
