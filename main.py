from fastapi import FastAPI, Depends
from database import create_db_and_tables, get_session
from models import User
from sqlmodel import Session

app = FastAPI()

# Evento que se ejecuta al iniciar la aplicacion
@app.on_event("startup")
def on_startup():
    # Crea las tablas en la base de datos si no existen
    create_db_and_tables()

@app.post("/users")
def create_user(user: User, session: Session = Depends(get_session)
):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user