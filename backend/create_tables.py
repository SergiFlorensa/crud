from db import engine, Base
from models import Product, User

# Crear las tablas
Base.metadata.create_all(bind=engine)
