import os

from flask import Flask, jsonify
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv("../.env")

app = Flask(__name__)


def obtener_conexion():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"
    )


@app.route("/inventario", methods=["GET"])
def listar_inventario():
    conexion = None

    try:
        conexion = obtener_conexion()

        cursor = conexion.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            SELECT id, nombre, categoria, cantidad, precio
            FROM mascotas_productoinventario
            ORDER BY id
        """)

        productos = cursor.fetchall()

        cursor.close()

        return jsonify(productos)

    except Exception as error:
        print("ERROR:", error)

        return jsonify({
            "mensaje": "Error al consultar inventario"
        }), 500

    finally:
        if conexion:
            conexion.close()


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=False,
        use_reloader=False
    )