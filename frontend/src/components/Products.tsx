// src/components/Products.tsx
import React, { useEffect, useState } from 'react';
import { API_URL } from './apiConfig'; // Importamos la URL de la API

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
}

const Products: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);

  // Función para obtener los productos desde la API
  const fetchProducts = async () => {
    try {
      const response = await fetch(`${API_URL}/products/`);
      const data: Product[] = await response.json(); // Tipamos la respuesta como 'Product[]'
      setProducts(data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <div>
      <h1>Products</h1>
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            {product.name} - {product.price}€
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Products;
