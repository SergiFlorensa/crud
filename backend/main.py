from fastapi import FastAPI
from models import Product
from typing import List

app = FastAPI()

products_db = []

@app.post("/products/", response_model=Product)
def create_product(product:Product):
    products_db.append(product)
    return product

@app.get("/products", response_model=List[Product])
def get_products():
    return products_db

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id:int):
    return products_db[product_id]

@app.put("products/{product_id}", response_model=Product)
def update_product(product_id:int, product:Product):
    products_db[product_id]= product
    return product

@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int):
    product = products_db.pop(product_id)
    return product

@app.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI!"}