from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from crm.models import Cliente, Produto, Estoque, Venda


class ApagarVendaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser(
            "admin", "admin@email.com", "admin"
        )
        cls.usuario_comum = User.objects.create_user(
            "usuario", "usuario@email.com", "usuario"
        )
        cls.cliente = Cliente.objects.create(
            nome="Cliente comum",
            telefone="(11) 99122-1331",
            email="cliente@email.com",
            endereco="Ruas das Flores, 123",
            fonte="Viu na rua",
            status="ativo",
            notas="",
        )

    def setUp(self):
        self.produto1 = Produto.objects.create(
            nome="Produto Teste 1",
            descricao="Produto de Teste 1",
            preco=10.99,
            categoria="flores",
            ativo=True,
        )
        self.produto2 = Produto.objects.create(
            nome="Produto Teste 2",
            descricao="Produto de Teste 2",
            preco=20.99,
            categoria="vasos",
            ativo=True,
        )
        self.estoque1 = Estoque.objects.create(produto=self.produto1, quantia=10)
        self.estoque2 = Estoque.objects.create(produto=self.produto2, quantia=5)

        self.venda = Venda.objects.create(
            cliente=self.cliente, forma_pagamento="Crédito", status="concluida"
        )
        self.venda.produtos.set([self.produto1, self.produto2])

        self.url = reverse("apagar_venda", kwargs={"pk": self.venda.id})

    def test_apagar_superusuario(self):
        """Testa se o superusuário consegue apagar uma venda e é redirecionado para a lista de vendas."""
        self.client.login(username="admin", password="admin")

        resposta = self.client.post(self.url)

        self.assertEqual(Venda.objects.count(), 0)
        self.assertRedirects(resposta, reverse("vendas"))

    def test_apagar_usuario_comum(self):
        """Testa se um usuário comum não pode apagar uma venda e recebe um status de erro 403."""
        self.client.login(username="usuario", password="usuario")

        resposta = self.client.post(self.url)

        self.assertEqual(Venda.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)

    def test_apagar_sem_metodo_post(self):
        """Testa se ao tentar apagar uma venda sem usar o método POST, o servidor retorna erro 403."""
        self.client.login(username="admin", password="admin")

        resposta = self.client.get(self.url)

        self.assertEqual(Venda.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)
