from typing import Optional
from sqlmodel import SQLModel, Field

# 1. Clase Base (Campos compartidos)
class UserBase(SQLModel):
    name: str
    email: str

# 2. Modelo de Tabla (Lo que va a la Base de Datos)
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str # Ejemplo de dato sensible que no debe salir

# 3. Modelo de Creación (Lo que el cliente envía en el POST)
class UserCreate(UserBase):
    password: str

# 4. Modelo Público (Lo que devuelves en el GET/POST, sin la password)
class UserPublic(UserBase):
    id: int