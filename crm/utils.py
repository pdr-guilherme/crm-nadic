from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect

def apagar_objeto(request, pk, classe, url_redirect):
    usuario = request.user
    autenticado = usuario.is_authenticated and usuario.is_superuser
    if request.method == "POST" and autenticado:
        objeto = get_object_or_404(classe, id=pk)
        objeto.delete()
        return redirect(url_redirect)
    return HttpResponseForbidden()