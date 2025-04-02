from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import F
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

from .forms import ProdutoForm, EstoqueForm, ClienteForm, LeadForm, VendaForm
from .models import Produto, Estoque, Cliente, Lead, Venda
from .utils import apagar_objeto, converter_lead_em_cliente


class IndexView(generic.TemplateView):
    template_name = "crm/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendas_totais = sum([venda.valor_total for venda in Venda.objects.all()])
        context["vendas_totais"] = vendas_totais
        return context


class VerificarSuperusuarioMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


# Produto
class ProdutoList(generic.ListView):
    model = Produto
    context_object_name = "produtos"
    template_name = "crm/listar_produtos.html"


class ProdutoDetail(generic.DetailView):
    model = Produto
    template_name = "crm/produto.html"
    context_object_name = "produto"


class ProdutoCreateForm(VerificarSuperusuarioMixin, generic.FormView):
    form_class = ProdutoForm
    template_name = "crm/criar.html"
    success_url = reverse_lazy("produtos")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["titulo"] = "Adicionar Produto"
        return context


class ProdutoUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "crm/editar.html"
    success_url = reverse_lazy("produtos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["titulo"] = "Atualizar Produto"
        return context


def apagar_produto(request, pk):
    resposta = apagar_objeto(request, pk, Produto, "produtos")
    return resposta


# Estoque
class EstoqueList(generic.ListView):
    model = Estoque
    context_object_name = "estoque"
    template_name = "crm/listar_estoque.html"


class EstoqueDetail(generic.DetailView):
    model = Estoque
    template_name = "crm/estoque.html"
    context_object_name = "estoque"


class EstoqueCreateForm(VerificarSuperusuarioMixin, generic.FormView):
    form_class = EstoqueForm
    template_name = "crm/criar.html"
    success_url = reverse_lazy("estoque")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["titulo"] = "Adicionar Produto ao Estoque"
        return context


class EstoqueUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Estoque
    form_class = EstoqueForm
    template_name = "crm/editar.html"
    success_url = reverse_lazy("estoque")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["titulo"] = "Atualizar Produto no Estoque"
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["titulo"] = "Adicionar Cliente"
        return context


class ClienteUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "crm/editar.html"
    success_url = reverse_lazy("clientes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["titulo"] = "Atualizar Cliente"
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["titulo"] = "Adicionar Lead"
        return context


class LeadUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = "crm/editar.html"
    success_url = reverse_lazy("leads")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["titulo"] = "Atualizar Lead"
        return context


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


# Vendas
class VendaList(generic.ListView):
    model = Venda
    context_object_name = "vendas"
    template_name = "crm/listar_vendas.html"


class VendaFormCreate(VerificarSuperusuarioMixin, generic.FormView):
    form_class = VendaForm
    template_name = "crm/criar.html"
    success_url = reverse_lazy("vendas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Adicionar Venda"
        return context

    def form_valid(self, form):
        form.save(commit=False)

        produtos = form.cleaned_data["produtos"]
        for produto in produtos:
            estoque = produto.estoque
            if estoque.quantia > 0:
                estoque.quantia = F("quantia") - 1
                estoque.save()
            else:
                messages.error(self.request, f"{produto.nome} não disponível, tente novamente")
                return super().form_invalid(form)

        form.save()
        return super().form_valid(form)


class VendaUpdate(VerificarSuperusuarioMixin, generic.UpdateView):
    model = Venda
    form_class = VendaForm
    template_name = "crm/editar.html"
    success_url = reverse_lazy("vendas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Atualizar Venda"
        return context

    def form_valid(self, form):
        if "produtos" in form.changed_data:
            produtos_originais = form["produtos"].initial
            produtos = form.cleaned_data["produtos"]

            # produto adicionado à lista
            for produto in produtos:
                if produto not in produtos_originais:
                    estoque = produto.estoque
                    if estoque.quantia > 0:
                        estoque.quantia = F("quantia") - 1
                        estoque.save()
                    else:
                        messages.error(self.request, f"{produto.nome} não disponível, tente novamente")
                        return super().form_invalid(form)

            # produto removido da lista
            for produto_original in produtos_originais:
                if produto_original not in produtos:
                    estoque = produto_original.estoque
                    estoque.quantia = F("quantia") + 1
                    estoque.save()

        form.save()
        return super().form_valid(form)


def apagar_venda(request, pk):
    venda = get_object_or_404(Venda, id=pk)

    for produto in venda.produtos.all():
        estoque = produto.estoque
        estoque.quantia = F("quantia") + 1
        estoque.save()

    resposta = apagar_objeto(request, pk, Venda, "vendas")
    return resposta
