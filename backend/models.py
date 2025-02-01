from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String, Float
from db import Base

# Encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelo SQLAlchemy para Product
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)

# Modelo Pydantic para Product (para validación y serialización de datos)
class ProductBase(BaseModel):
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True  # Esto le permite a Pydantic trabajar con SQLAlchemy

# Modelo SQLAlchemy para User
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Modelo Pydantic para la creación de usuarios (registro)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True  # Esto le permite a Pydantic trabajar con SQLAlchemy

# Modelo Pydantic para la salida de usuarios (sin la contraseña)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True  # Esto le permite a Pydantic trabajar con SQLAlchemy

# Función para hashear contraseñas
def hash_password(password: str):
    return pwd_context.hash(password)
# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
