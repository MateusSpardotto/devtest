from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from elevators.sqlDocuments.demand import Base


database_url = URL.create(
    "mssql+pyodbc",
    host="localhost",
    database="master",
    query={"driver": "ODBC Driver 17 for SQL Server", "trusted_connection": "yes"}
)

# Criar a engine do SQLAlchemy
engine = create_engine(database_url)

# Criar a tabela no banco de dados
Base.metadata.create_all(engine)

# Criar uma sessão de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()