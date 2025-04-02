from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# tipo de loja: floricultura

class Produto(models.Model):
    """Modelo que representa um produto na loja."""
    CATEGORIA_CHOICES = {
        "plantas": "Plantas",
        "vasos": "Vasos",
        "flores": "Flores",
        "buquê": "Buquê de Flores",
        "arranjo": "Arranjo de Flores",
        "cesta": "Cesta de Presente",
    }

    nome = models.CharField("Nome do produto", max_length=100)
    descricao = models.CharField("Descrição do produto", max_length=255)
    preco = models.DecimalField("Preço do produto (R$)", max_digits=7, decimal_places=2)
    ativo = models.BooleanField("Produto ativo", default=True)
    data_criacao = models.DateField("Data de criação", auto_now_add=True)
    categoria = models.CharField("Categoria do produto", max_length=17, choices=CATEGORIA_CHOICES)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["nome",]

    def __str__(self) -> str:
        return f"{self.nome} (R$ {self.preco}): {self.descricao}"

    def get_absolute_url(self):
        return reverse("ver_produto", kwargs={"pk": self.id})

class Estoque(models.Model):
    """
    Classe responsável por gerenciar a quantidade de produtos disponíveis no estoque.
    """
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE, related_name="estoque")
    quantia = models.PositiveIntegerField("Quantidade em estoque", blank=True, default=0)

    def __str__(self) -> str:
        return f"Produto {self.produto} - {self.quantia} disponíveis em estoque"

    def get_absolute_url(self):
        return reverse("ver_estoque", kwargs={"pk": self.id})


class Cliente(models.Model):
    STATUS_CHOICES = {
        "ativo": "Ativo",
        "inativo": "Inativo",
        "bloqueado": "Bloqueado",
    }

    nome = models.CharField("Nome", max_length=255)
    telefone = models.CharField("Telefone", max_length=15)
    email = models.EmailField("E-mail")
    endereco = models.TextField("Endereço")
    fonte = models.CharField("Fonte", max_length=255)
    status = models.CharField("Status", max_length=25, choices=STATUS_CHOICES, default="ativo")
    notas = models.TextField("Notas e pontos importantes", blank=True, default="")
    data_criacao = models.DateTimeField("Data de criação", auto_now_add=True)

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        ordering = ["nome", "-data_criacao"]

    def __str__(self) -> str:
        return f"Cliente {self.id} - {self.nome}, {self.email}, {self.status}"


class Lead(models.Model):
    STATUS_CHOICES = [
        ("novo", "Novo"),
        ("em_progresso", "Em Progresso"),
        ("qualificado", "Qualificado"),
        ("desqualificado", "Desqualificado"),
        ("fechado", "Fechado"),
    ]

    nome = models.CharField("Nome", max_length=255)
    telefone = models.CharField("Telefone", max_length=15)
    email = models.EmailField("E-mail")
    endereco = models.TextField("Endereço")
    fonte = models.CharField("Fonte", max_length=255)
    status = models.CharField("Status", max_length=25, choices=STATUS_CHOICES, default="ativo")
    notas = models.TextField("Notas e pontos importantes", blank=True, default="")
    produto_interesse = models.CharField("Produtos ou serviços de interesse", max_length=255)
    data_conversao = models.DateTimeField("Data de conversão", blank=True, null=True)
    responsavel = models.ForeignKey(User, verbose_name="Responsável", on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "lead"
        verbose_name_plural = "leads"
        ordering = ["nome",]

    def __str__(self):
        return f"Lead {self.id} - {self.nome}, {self.email}, {self.status}"


class Venda(models.Model):
    STATUS_CHOICES = [
        ("em_processamento", "Em Processamento"),
        ("concluida", "Concluída"),
        ("cancelada", "Cancelada"),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, related_name="vendas", null=True)
    produtos = models.ManyToManyField(Produto, related_name="vendas")
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default="em_processamento")
    data_venda = models.DateTimeField("Data da venda", auto_now_add=True)
    forma_pagamento = models.CharField("Forma de pagamento", max_length=50)

    class Meta:
        ordering = ["-data_venda",]
        verbose_name = "venda"
        verbose_name_plural = "vendas"

    def __str__(self):
        return f"Venda {self.id} - {self.cliente.nome} - {self.data_venda} - {self.forma_pagamento}"

    @property
    def valor_total(self):
        return sum(produto.preco for produto in self.produtos.all())
