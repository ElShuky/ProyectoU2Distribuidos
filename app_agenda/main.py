import os # <-- Añadir esta importación al principio del archivo
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# --- FUNCIONES DE CONEXIÓN A LAS BASES DE DATOS ---

def get_primary_connection():
    """Conexión para ESCRITURA"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST_PRIMARY"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

def get_replica_connection():
    """Conexión para LECTURA"""
    return psycopg2.connect(
        host=os.getenv("DB_HOST_REPLICA"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

# --- MODELO DE DATOS PARA EL POST ---
class Cita(BaseModel):
    paciente_id: int
    medico: str
    box: str
    fecha_cita: str

# --- ENDPOINTS (RUTAS) ---

@app.get("/")
def home_clinica():
    return {"modulo": "Área Clínica", "estado": "Conectado a BD Replicada"}

@app.get("/pacientes")
def listar_pacientes():
    """Lee desde la BD Réplica para no sobrecargar la primaria"""
    try:
        conn = get_replica_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, rut, nombre_completo FROM pacientes;")
        filas = cur.fetchall()
        cur.close()
        conn.close()
        
        # Formateamos el resultado
        pacientes = [{"id": f[0], "rut": f[1], "nombre": f[2]} for f in filas]
        return {"origen": "db_replica", "pacientes": pacientes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de BD: {str(e)}")

@app.post("/agendar")
def crear_cita(cita: Cita):
    """Escribe en la BD Primaria"""
    try:
        conn = get_primary_connection()
        cur = conn.cursor()
        query = """
            INSERT INTO citas_medicas (paciente_id, medico, box, fecha_cita) 
            VALUES (%s, %s, %s, %s) RETURNING id;
        """
        cur.execute(query, (cita.paciente_id, cita.medico, cita.box, cita.fecha_cita))
        nueva_cita_id = cur.fetchone()[0]
        
        conn.commit() # Guardamos los cambios
        cur.close()
        conn.close()
        
        return {
            "mensaje": "Cita registrada exitosamente en la BD", 
            "id_cita": nueva_cita_id,
            "origen_escritura": "db_primary"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de BD: {str(e)}")
