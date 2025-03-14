from django import forms

from .models import Estoque, Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = "__all__"
