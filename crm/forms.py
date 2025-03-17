from django import forms

from .models import Estoque, Lead, Produto, Cliente


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = "__all__"


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        exclude = ["responsavel"]
        widgets = {
            "data_conversao": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }