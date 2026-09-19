
import os

from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def obtener_coleccion():
    cliente = MongoClient(os.environ["MONGO_URI"])

    print("Bases de datos disponibles:", cliente.list_database_names())

    base_datos = cliente["veterinario"]
    print("Colecciones disponibles:", base_datos.list_collection_names())

    return base_datos["inventario"]


@app.route("/inventario", methods=["GET"])
def listar_inventario():
    coleccion = obtener_coleccion()
    productos = []

    for producto in coleccion.find():
        productos.append({
            "id": str(producto["_id"]),
            "nombre": producto["nombre"],
            "categoria": producto["categoria"],
            "cantidad": producto["cantidad"],
            "precio": producto["precio"]
        })

    return jsonify(productos)


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)