from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, ButtonHolder, Submit

from .models import Estoque, Lead, Produto, Cliente, Venda


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-4"  # tamanho do label
        self.helper.field_class = "col-md-8"  # tamanho do campo
        self.helper.layout = Layout(
            Fieldset(
                "Informações do Produto",
                Row(
                    Column("nome", css_class="form-group col-md-6"),
                    Column("preco", css_class="form-group col-md-6"),
                    css_class="form-row",
                ),
                "descricao",
                Row(
                    Column("categoria", css_class="form-group col-md-6"),
                    Column("ativo", css_class="form-group col-md-6"),
                    css_class="form-row",
                ),
            ),
            ButtonHolder(Submit("submit", "Salvar", css_class="btn btn-primary w-100")),
        )


class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-4"
        self.helper.field_class = "col-md-8"
        self.helper.layout = Layout(
            Fieldset(
                "Informações do estoque",
                Row(
                    Column("produto", css_class="form-group col-md-6"),
                    Column("quantia", css_class="form-group col-md-6"),
                    css_class="form-row",
                ),
            ),
            ButtonHolder(
                Submit("submit", "Adicionar", css_class="btn btn-primary w-100")
            ),
        )


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-4"
        self.helper.field_class = "col-md-8"
        self.helper.layout = Layout(
            Fieldset(
                "Dados do cliente",
                Row(
                    Column("nome", css_class="form-group col-md-6"),
                    css_class="form-row",
                ),
            ),
            Fieldset(
                "Informações de contato",
                Row(
                    Column("telefone", css_class="form-group col-md-6"),
                    Column("email", css_class="form-group col-md-6"),
                    Column("endereco", css_class="form-group col-md-6"),
                    css_class="form-row",
                ),
            ),
            Fieldset(
                "Outros dados",
                Row(
                    Column("fonte", css_class="form-group col-md-6"),
                    Column("status", css_class="form-group col-md-6"),
                    Column("notas", css_class="form-group col-md-6"),
                ),
            ),
            ButtonHolder(
                Submit("submit", "Adicionar", css_class="btn btn-primary w-100 mb-3")
            ),
        )


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        exclude = ["responsavel"]
        widgets = {
            "data_conversao": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-4"
        self.helper.field_class = "col-md-8"
        self.helper.layout = Layout(
            Fieldset(
                "Dados do lead",
                Row(
                    Column("nome", css_class="form-group col-md-6"),
                    css_class="form-row",
                ),
            ),
            Fieldset(
                "Informações de contato",
                Row(
                    Column("telefone", css_class="form-group col-md-6"),
                    Column("email", css_class="form-group col-md-6"),
                    Column("endereco", css_class="form-group col-md-6"),
                    css_class="form-row",
                ),
            ),
            Fieldset(
                "Outros dados",
                Row(
                    Column("fonte", css_class="form-group col-md-6"),
                    Column("status", css_class="form-group col-md-6"),
                    Column("notas", css_class="form-group col-md-6"),
                    Column("produto_interesse", css_class="form-group col-md-6"),
                    Column("data_conversao", css_class="form-group col-md-6"),
                ),
            ),
            ButtonHolder(
                Submit("submit", "Adicionar", css_class="btn btn-primary w-100 mb-3")
            ),
        )


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = "__all__"
        # widgets = {
        #     "produtos": forms.CheckboxSelectMultiple()
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-4"
        self.helper.field_class = "col-md-8"
        self.helper.layout = Layout(
            Fieldset(
                "Dados da venda",
                Row(
                    Column("cliente", css_class="form-group col-md-6"),
                    Column("produtos", css_class="form-group col-md-8"),
                    css_class="form-row",
                ),
            ),
            Fieldset(
                "Outros dados",
                Row(
                    Column("status", css_class="form-group col-md-6"),
                    Column("forma_pagamento", css_class="form-group col-md-6"),
                    css_class="form-row",
                ),
            ),
            ButtonHolder(
                Submit("submit", "Adicionar", css_class="btn btn-primary w-100 mb-3")
            ),
        )
