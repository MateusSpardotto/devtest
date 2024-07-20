from fastapi import FastAPI
import pyodbc

app = FastAPI()

@app.get("/number")
def get_number():
    conn_str = (
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"SERVER=localhost;"  # ou o nome do seu servidor
            r"DATABASE=master;"
            r"TRUSTED_CONNECTION=yes"
        )

        # Conectar ao banco de dados
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Executar uma consulta
    result = cursor.execute("SELECT * FROM demands")
    return {result}