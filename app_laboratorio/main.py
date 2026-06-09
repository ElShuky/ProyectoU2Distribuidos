import os
from fastapi import FastAPI, HTTPException
import psycopg2

app = FastAPI()

def get_connection(host_type="REPLICA"):
    """Intenta conectar al host solicitado"""
    host = os.getenv("DB_HOST_REPLICA") if host_type == "REPLICA" else os.getenv("DB_HOST_PRIMARY")
    return psycopg2.connect(
        host=host,
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )

@app.get("/examenes/{paciente_id}")
def ver_examenes(paciente_id: int):
    conn = None
    origen = "db_replica" 
    
    try:
        # INTENTO 1: Conectar a la Réplica
        conn = get_connection("REPLICA")
    except Exception as e:
        print(f" ¡ALERTA! db_replica caída. Fallo: {e}. Iniciando Failover...")
        try:
            # FAILOVER: Conmutar a la base de datos Primaria
            conn = get_connection("PRIMARY")
            origen = "db_primary (Por Failover de Emergencia)"
        except Exception as e_fatal:
            raise HTTPException(status_code=500, detail="Catástrofe: Ambos servidores de BD están caídos.")

    # Ejecutar la consulta en la conexión que haya sobrevivido
    try:
        cur = conn.cursor()
        cur.execute("SELECT tipo_examen, estado, fecha_solicitud FROM examenes_laboratorio WHERE paciente_id = %s;", (paciente_id,))
        filas = cur.fetchall()
        cur.close()
        conn.close()
        
        examenes = [{"examen": f[0], "estado": f[1], "fecha": f[2]} for f in filas]
        
        # Devolvemos los datos y anunciamos qué nodo nos salvó
        return {"paciente_id": paciente_id, "examenes": examenes, "nodo_lector": origen}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ejecutando SQL: {str(e)}")
