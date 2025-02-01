// src/components/ProductCard.tsx
import React from 'react';

// Definimos el tipo para un producto
type Product = {
  name: string;
  description: string;
  price: number;
};

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  return (
    <div className="product-card">
      <h3>{product.name}</h3>
      <p>{product.description}</p>
      <p><strong>Price:</strong> ${product.price.toFixed(2)}</p>
      <button className="buy-button">Buy Now</button>
    </div>
  );
};

export default ProductCard;
