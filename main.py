from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session

# Importamos lo que creamos en nuestros otros archivos
from database import create_db_and_tables, get_session
from models import User, UserCreate, UserPublic

app = FastAPI()

# Evento que se ejecuta al iniciar la aplicación
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ---------------------------------------------------------
# 💉 INYECCIÓN DE DEPENDENCIAS (El estándar moderno)
# ---------------------------------------------------------
# Creamos un tipo personalizado llamado "SessionDep". 
# Significa: "Esto es una Session de SQLModel, y depende de get_session"
SessionDep = Annotated[Session, Depends(get_session)]

# ---------------------------------------------------------
# 🚀 ENDPOINTS
# ---------------------------------------------------------

@app.post("/users", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    """
    Crea un usuario en la base de datos.
    Fíjate lo limpio que quedó el parámetro 'session: SessionDep'
    """
    # 1. Transformamos el modelo de entrada (UserCreate) al modelo de tabla (User)
    db_user = User.model_validate(user)
    
    # 2. Manejo de transacciones seguro (como pide la guía)
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user # El response_model=UserPublic se encarga de ocultar datos sensibles
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error al guardar en la base de datos")