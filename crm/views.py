import http
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

from .forms import ProdutoForm, EstoqueForm, ClienteForm, LeadForm
from .models import Produto, Estoque, Cliente, Lead
from .utils import apagar_objeto, converter_lead_em_cliente


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
    template_name = "crm/criar.html"
    success_url = reverse_lazy("produtos")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProdutoUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "crm/editar.html"
    success_url = reverse_lazy("produtos")


def apagar_produto(request, pk):
    resposta = apagar_objeto(request, pk, Produto, "produtos")
    return resposta


# Estoque
class EstoqueList(generic.ListView):
    model = Estoque
    context_object_name = "estoque"
    template_name = "crm/listar_estoque.html"


class EstoqueCreateForm(VerificarSuperusuarioMixin, generic.FormView):
    form_class = EstoqueForm
    template_name = "crm/criar.html"
    success_url = reverse_lazy("estoque")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EstoqueUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Estoque
    form_class = EstoqueForm
    template_name = "crm/editar.html"
    success_url = reverse_lazy("estoque")


def apagar_estoque(request, pk):
    resposta = apagar_objeto(request, pk, Estoque, "estoque")
    return resposta

# Clientes
class ClienteList(generic.ListView):
    model = Cliente
    context_object_name = "clientes"
    template_name = "crm/listar_clientes.html"


class ClienteFormCreate(VerificarSuperusuarioMixin, generic.FormView):
    form_class = ClienteForm
    template_name = "crm/criar.html"
    success_url = reverse_lazy("clientes")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ClienteUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "crm/editar.html"
    success_url = reverse_lazy("clientes")


def apagar_cliente(request, pk):
    resposta = apagar_objeto(request, pk, Cliente, "clientes")
    return resposta


# Leads
class LeadList(generic.ListView):
    model = Lead
    context_object_name = "leads"
    template_name = "crm/listar_leads.html"


class LeadFormCreate(VerificarSuperusuarioMixin, generic.FormView):
    form_class = LeadForm
    template_name = "crm/criar.html"
    success_url = reverse_lazy("leads")

    def form_valid(self, form):
        form.instance.responsavel = self.request.user
        form.save()
        return super().form_valid(form)


class LeadUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = "crm/editar.html"
    success_url = reverse_lazy("leads")


def apagar_lead(request, pk):
    resposta = apagar_objeto(request, pk, Lead, "leads")
    return resposta


class ConverterLeadView(VerificarSuperusuarioMixin, generic.View):
    def post(self, request, pk):
        lead = get_object_or_404(Lead, id=pk)

        try:
            cliente = converter_lead_em_cliente(lead)
            return redirect("clientes")
        except ValueError as erro:
            return HttpResponse(f"Erro: {erro}", status=400)
