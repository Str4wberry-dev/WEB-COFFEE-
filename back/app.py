from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://192.168.169.111:5500","http://elbuensabor.test"])
# CORS(app, resources={r"/*": {"origins": ["http://localhost:5500", "https://mi-dominio.com"]}})
# CORS(
#     app,
#     supports_credentials=True,
#     origins=["http://localhost:5500","elbuensabor.test"],
# )

@app.before_request
def before_request(): 
    headers = { 
        'Access-Control-Allow-Origin': '*', 
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 
        'Access-Control-Allow-Headers': 'Content-Type' 
    }
    if request.method == 'OPTIONS' or request.method == 'options':
        return jsonify(headers), 200

listado_productos = [
    {
        "id": 1,
        "nombre": "Mocca",
        "descripcion": "Este café es una mezcla deliciosa de espresso, leche vaporizada y jarabe de chocolate. Su sabor combina el amargor del café con la dulzura del chocolate, siempre decorado con crema batida.",
        "imagen": "img/food1.png",
        "comentarios": [
            "La comida fue espectacular y el ambiente muy acogedor. Sin duda, un lugar al que volveré.",
        ],
    },
    {
        "id": 2,
        "nombre": "Cappuccino",
        "descripcion": "Bebida de café que combina partes iguales de espresso, leche vaporada y espuma de leche. Su textura cremosa y sabor equilibrado entre el café y la leche lo hacen muy popular. Se le espolvorea con cacao o canela por encima para darle un toque extra de sabor.",
        "imagen": "img/food2.png",
        "comentarios": [
            "Excelente servicio y platos deliciosos. ¡Muy recomendado!",
        ],
    },
    {
        "id": 3,
        "nombre": "Latte",
        "descripcion": "Bebida que combina leche vaporizada y un toque de espresso, creando un contraste visual y de sabor. Se caracteriza por su textura cremosa, un ligero sabor a café y un aspecto atrayente, con capas distintas de leche y café.",
        "imagen": "img/food3.jpg",
        "comentarios": [
            "Excelente servicio y platos deliciosos. ¡Muy recomendado!",
        ],
    },
]


@app.route("/productos", methods=["GET"])
def get_productos():
    return jsonify(listado_productos)

@app.route("/productos", methods=["POST"])
def crear_producto():
    idNuevoProducto = len(listado_productos) + 1
    listado_productos.append({
        "id": idNuevoProducto,
        "nombre": request.form["nombre"],
        "descripcion": request.form["descripcion"],
        "imagen": request.form["imagen"],
        "comentarios": []
    })
    return jsonify({"mensaje": "OK"}), 200

@app.route("/productos/<int:producto_id>", methods=["GET"])
def get_producto(producto_id):
    producto = next((item for item in listado_productos if item["id"] == producto_id), None)
    if producto:
        return jsonify(producto)
    return jsonify({"error": "Producto no encontrado"}), 404


@app.route("/productos/<int:producto_id>/comentario", methods=["POST"])
def comentar_producto(producto_id):
    producto = next((item for item in listado_productos if item["id"] == producto_id), None)
    if producto:
        comentario = request.get_data().decode("utf-8")
        producto["comentarios"].append(comentario)
        return jsonify(producto), 201
    return jsonify({"error": "Producto no encontrado"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
