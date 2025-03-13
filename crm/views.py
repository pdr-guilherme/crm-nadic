from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect

from .forms import ProdutoForm
from .models import Produto


class ProdutoList(generic.ListView):
    model = Produto
    context_object_name = "produtos"
    template_name = "crm/listar_produtos.html"


class VerificarSuperusuarioMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class ProdutoCreateForm(VerificarSuperusuarioMixin, generic.FormView):
    form_class = ProdutoForm
    template_name = "crm/criar_produto.html"
    success_url = reverse_lazy("produtos")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProdutoUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "crm/editar_produto.html"
    success_url = reverse_lazy("produtos")


def apagar_produto(request, pk):
    if request.method == "POST":
        produto = get_object_or_404(Produto, id=pk)
        produto.delete()
        return redirect("produtos")
    return HttpResponseForbidden()
