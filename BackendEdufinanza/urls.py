from django.urls import path, include
from usuarios.views import ActualizarClave, usuarioRecuperar,login, usuarioCrear,obtenerUsuario, usuarioActualizar, usuarioEliminar, index
from comentarios.views import crearComentario, obtenerComentario, comentarioActualizar, comentarioEliminar
from django.contrib import admin
urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('usuario/crear/', usuarioCrear),
    path('usuario/obtener/', obtenerUsuario),
    path('api/login/', login),
    path('usuario/actualizar/<int:id>', usuarioActualizar ),
    path('usuario/eliminar/<int:id>', usuarioEliminar ),
    path('comentario/crear/', crearComentario),
    path('obtener/comentario/', obtenerComentario),
    path('comentario/actualizar/<int:id>', comentarioActualizar ),
    path('comentario/eliminar/<int:id>', comentarioEliminar ),
    path('usuario/recuperar/', usuarioRecuperar),
    path('usuario/clavenueva/', ActualizarClave)
]