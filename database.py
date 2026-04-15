import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True # SQL visible en consola (obligatoria en dev)
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    # Cada request obtiene su propia sesion
    # No se comparte estado en cada request
    with Session(engine) as session:
        # El endpoint usa esta sesion para lee/escribir en la base de datos
        yield session
        # Al terminar la request:
        # - se cierra la sesion
        # - se devuelve la conexion al pool
