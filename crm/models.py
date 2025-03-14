from django.db import models


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

class Estoque(models.Model):
    """
    Classe responsável por gerenciar a quantidade de produtos disponíveis no estoque.
    """
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE, related_name="estoque")
    quantia = models.PositiveIntegerField("Quantidade em estoque", blank=True, default=0)

    def __str__(self) -> str:
        return f"Produto {self.produto} - {self.quantia} disponíveis em estoque"


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
    pass


class Venda(models.Model):
    pass
