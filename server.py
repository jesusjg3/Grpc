import grpc
from concurrent import futures
import libros_pb2
import libros_pb2_grpc
import db

class LibroServiceServicer(libros_pb2_grpc.LibroServiceServicer):
    def CrearLibro(self, request, context):
        libro_id = db.crear_libro(request.nombre, request.autor, request.anio_publicacion)
        # Devolver el libro creado con su id
        return libros_pb2.Libro(id=libro_id, nombre=request.nombre, autor=request.autor, anio_publicacion=request.anio_publicacion)

    def ObtenerLibro(self, request, context):
        row = db.obtener_libro(request.id)
        if row:
            return libros_pb2.Libro(id=row[0], nombre=row[1], autor=row[2], anio_publicacion=row[3])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Libro no encontrado')
            return libros_pb2.Libro()

    def ActualizarLibro(self, request, context):
        updated = db.actualizar_libro(request.id, request.nombre, request.autor, request.anio_publicacion)
        if updated:
            return libros_pb2.Respuesta(mensaje="Libro actualizado")
        else:
            return libros_pb2.Respuesta(mensaje="Libro no existe")

    def EliminarLibro(self, request, context):
        deleted = db.eliminar_libro(request.id)
        if deleted:
            return libros_pb2.Respuesta(mensaje="Libro eliminado")
        else:
            return libros_pb2.Respuesta(mensaje="Libro no encontrado")

    def ListarLibros(self, request, context):
        rows = db.listar_libros()
        libros = [libros_pb2.Libro(id=row[0], nombre=row[1], autor=row[2], anio_publicacion=row[3]) for row in rows]
        return libros_pb2.ListaLibros(libros=libros)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    libros_pb2_grpc.add_LibroServiceServicer_to_server(LibroServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor corriendo en puerto 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
