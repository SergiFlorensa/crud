from fastapi import FastAPI
from models import Product
from typing import List

app = FastAPI()

# Repositorio simulado (en memoria)
products_db = []

# Ruta para crear un producto
@app.post("/products/", response_model=Product)
def create_product(product: Product):
    products_db.append(product)
    return product

# Ruta para obtener todos los productos
@app.get("/products/", response_model=List[Product])
def get_products():
    return products_db


# Ruta para obtener un producto por ID
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    return products_db[product_id]

# Ruta para actualizar un producto
@app.put("/products/{product_id}", response_model=Product)  # Corregido aquí
def update_product(product_id: int, product: Product):
    products_db[product_id] = product
    return product

# Ruta para eliminar un producto
@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int):
    product = products_db.pop(product_id)
    return product

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI!"}
