from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL de conexión a la base de datos PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")  # Asegúrate de que la variable de entorno esté configurada

# Conexión a la base de datos con la librería 'databases'
database = Database(DATABASE_URL)

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear la sesión local (conexión a la base de datos)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para declarar los modelos
Base = declarative_base()  # Aquí estaba el error, le falta el paréntesis al final
