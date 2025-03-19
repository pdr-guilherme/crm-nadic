from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from .models import Cliente, Lead


def apagar_objeto(request, pk, classe, url_redirect):
    usuario = request.user
    autenticado = usuario.is_authenticated and usuario.is_superuser
    if request.method == "POST" and autenticado:
        objeto = get_object_or_404(classe, id=pk)
        objeto.delete()
        return redirect(url_redirect)
    return HttpResponseForbidden()


def converter_lead_em_cliente(lead: Lead) -> Cliente:
    if lead.status not in ["qualificado", "fechado"]:
        raise ValueError(f"O lead não está no status adequado para conversão. Status atual: {lead.status}")

    cliente = Cliente(
        nome=lead.nome,
        telefone=lead.telefone,
        email=lead.email,
        endereco=lead.endereco,
        fonte=lead.fonte,
        notas=lead.notas,
        status="ativo",
        data_criacao=timezone.now()
    )

    cliente.save()

    lead.status = "fechado"
    lead.data_conversao = timezone.now()
    lead.save()

    return cliente
