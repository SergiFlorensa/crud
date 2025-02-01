from fastapi import FastAPI, HTTPException, Depends, status
from models import Product, User, ProductBase, UserCreate, UserOut, hash_password, verify_password  # Asegúrate de usar el modelo Pydantic UserOut para la salida
from typing import List
from sqlalchemy.orm import Session
from db import SessionLocal, engine, Base
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

# Crear las tablas en PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clave secreta para JWT
SECRET_KEY = "92d40dae5f8046ee8f0cc74e3235ff677999e08585f79baaaedd3ce46f5816ab"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración de OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()  # Corregido aquí
    try:
        yield db
    finally:
        db.close()

# Ruta para crear un producto
@app.post("/products/", response_model=ProductBase)  # Usa el modelo Pydantic ProductBase
def create_product(product: ProductBase, db: Session = Depends(get_db)):  # Usa el modelo Pydantic ProductBase para la entrada
    db_product = Product(name=product.name, description=product.description, price=product.price)  # Crear el producto SQLAlchemy
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Ruta para obtener todos los productos
@app.get("/products/", response_model=List[ProductBase])  # Usa el modelo Pydantic ProductBase
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# Ruta para obtener un producto por ID
@app.get("/products/{product_id}", response_model=ProductBase)  # Usa el modelo Pydantic ProductBase
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Ruta para actualizar un producto
@app.put("/products/{product_id}", response_model=ProductBase)  # Usa el modelo Pydantic ProductBase
def update_product(product_id: int, product: ProductBase, db: Session = Depends(get_db)):  # Usa el modelo Pydantic ProductBase
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

# Ruta para eliminar un producto
@app.delete("/products/{product_id}", response_model=ProductBase)  # Usa el modelo Pydantic ProductBase
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return db_product

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "¡Hola, FastAPI!"}


##User
# Ruta para crear un usuario
@app.post("/users/", response_model=UserOut)  # Usa el modelo Pydantic UserOut para la respuesta
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el nombre de usuario o el correo electrónico ya existen
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user_by_email = db.query(User).filter(User.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hashear la contraseña antes de almacenarla
    hashed_password = hash_password(user.password)
    
    # Crear el usuario en la base de datos
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user  # Aquí se devolverá el modelo Pydantic UserOut, que no contiene la contraseña


def create_access_token(data:dict, expires_delta:timedelta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

# Ruta para el inicio de sesión
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta para obtener los productos (solo si el usuario está autenticado)
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except jwt.PyJWTError:
        raise credentials_exception

@app.get("/products/")
def get_products(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    products = db.query(Product).all()
    return products
