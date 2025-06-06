from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import grpc
import libros_pb2
import libros_pb2_grpc

app = Flask(__name__)
CORS(app)

# Habilitar CORS para todas las rutas
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

channel = grpc.insecure_channel('localhost:50051')
stub = libros_pb2_grpc.LibroServiceStub(channel)

@app.route("/libros", methods=["POST"])
def crear_libro():
    data = request.json
    libro = libros_pb2.Libro(
        nombre=data["nombre"],
        autor=data["autor"],
        anio_publicacion=data["anio_publicacion"]
    )
    libro_creado = stub.CrearLibro(libro)
    return jsonify({
        "id": libro_creado.id,
        "nombre": libro_creado.nombre,
        "autor": libro_creado.autor,
        "anio_publicacion": libro_creado.anio_publicacion
    })

@app.route("/libros", methods=["GET"])
def listar_libros():
    res = stub.ListarLibros(libros_pb2.Vacio())
    return jsonify([
        {
            "id": l.id,
            "nombre": l.nombre,
            "autor": l.autor,
            "anio_publicacion": l.anio_publicacion
        } for l in res.libros
    ])

@app.route("/", methods=["GET"])
def home():
    return "API gRPC - Flask funcionando"


@app.route("/libros/<int:id>", methods=["GET"])
def obtener_libro(id):
    try:
        libro = stub.ObtenerLibro(libros_pb2.LibroId(id=id))
        if libro.id == 0:
            return jsonify({"error": "Libro no encontrado"}), 404
        return jsonify({
            "id": libro.id,
            "nombre": libro.nombre,
            "autor": libro.autor,
            "anio_publicacion": libro.anio_publicacion
        })
    except grpc.RpcError as e:
        return jsonify({"error": e.details()}), 404

@app.route("/libros/<int:id>", methods=["PUT"])
def actualizar_libro(id):
    data = request.json
    libro = libros_pb2.Libro(
        id=id,
        nombre=data["nombre"],
        autor=data["autor"],
        anio_publicacion=data["anio_publicacion"]
    )
    res = stub.ActualizarLibro(libro)
    return jsonify({"mensaje": res.mensaje})

@app.route("/libros/<int:id>", methods=["DELETE"])
def eliminar_libro(id):
    res = stub.EliminarLibro(libros_pb2.LibroId(id=id))
    return jsonify({"mensaje": res.mensaje})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
