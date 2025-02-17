import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

connectstr = f"dbname='{DB_NAME}' user='{DB_USER}' host='{DB_HOST}' password='{DB_PASSWORD}'"

# Conectar a la base de datos
try:
    conn = psycopg2.connect(connectstr)
    conn.autocommit = True
    print("✅ Conectado a PostgreSQL")
except Exception as e:
    print(f"❌ Error conectando a PostgreSQL: {e}")

def execute(sql, update=False):
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            if not update:
                result = cur.fetchone()
                if result:
                    return result[0]  # Retorna el primer valor
                return None
            return 0
    except Exception as e:
        print(f"❌ Error ejecutando consulta: {e}")
        return None


def execute_not_injection(sql, obj, update=False):
    try:
        with conn.cursor() as cur:
            cur.execute(sql, obj)
            if not update:
                return cur.fetchone()[0]  # Retorna ID si es un INSERT
            return 0
    except Exception as e:
        print(f"❌ Error ejecutando consulta con parámetros: {e}")
        print(f"Consulta SQL: {sql}")
        print(f"Parámetros: {obj}")
        return None


def execute_query(sql):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            res = cur.fetchall()
            cur.close()
            return res
    except Exception as e:
        print(f"❌ Error ejecutando consulta SELECT: {e}")
        return None
    

def execute_query_not_injection(sql, obj):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, obj)
            return cur.fetchall()
    except Exception as e:
        print(f"❌ Error ejecutando consulta SELECT con parámetros: {e}")
        return None


def execute_insert_not_injection(sql, obj):
    try:
        with conn.cursor() as cur:
            cur.execute(sql, obj)
            conn.commit()
            return True
    except Exception as e:
        print(f"❌ Error ejecutando consulta INSERT con parámetros: {e}")
        conn.rollback()  # En caso de error, deshacer la operación
        return False

