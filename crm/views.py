from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect

from .forms import EstoqueForm, ProdutoForm, ClienteForm
from .models import Produto, Estoque, Cliente


class IndexView(generic.TemplateView):
    template_name = "crm/index.html"


class VerificarSuperusuarioMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


# Produto
class ProdutoList(generic.ListView):
    model = Produto
    context_object_name = "produtos"
    template_name = "crm/listar_produtos.html"


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
    usuario = request.user
    autenticado = usuario.is_authenticated and usuario.is_superuser
    if request.method == "POST" and autenticado:
        produto = get_object_or_404(Produto, id=pk)
        produto.delete()
        return redirect("produtos")
    return HttpResponseForbidden()


# Estoque
class EstoqueList(generic.ListView):
    model = Estoque
    context_object_name = "estoque"
    template_name = "crm/listar_estoque.html"


class EstoqueCreateForm(VerificarSuperusuarioMixin, generic.FormView):
    form_class = EstoqueForm
    template_name = "crm/criar_estoque.html"
    success_url = reverse_lazy("estoque")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EstoqueUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Estoque
    form_class = EstoqueForm
    template_name = "crm/editar_estoque.html"
    success_url = reverse_lazy("estoque")


def apagar_estoque(request, pk):
    usuario = request.user
    autenticado = usuario.is_authenticated and usuario.is_superuser
    if request.method == "POST" and autenticado:
        estoque = get_object_or_404(Estoque, id=pk)
        estoque.delete()
        return redirect("estoque")
    return HttpResponseForbidden()


# Clientes
class ClienteList(generic.ListView):
    model = Cliente
    context_object_name = "clientes"
    template_name = "crm/listar_clientes.html"


class ClienteFormCreate(VerificarSuperusuarioMixin, generic.FormView):
    form_class = ClienteForm
    template_name = "crm/criar_cliente.html"
    success_url = reverse_lazy("clientes")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ClienteUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "crm/editar_produto.html"
    success_url = reverse_lazy("clientes")


def apagar_cliente(request, pk):
    usuario = request.user
    autenticado = usuario.is_authenticated and usuario.is_superuser
    if request.method == "POST" and autenticado:
        cliente = get_object_or_404(Cliente, id=pk)
        cliente.delete()
        return redirect("clientes")
    return HttpResponseForbidden()
