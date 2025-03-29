from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from crm.models import Estoque, Produto


class EstoqueCreateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser(
            "admin", "admin@email.com", "admin"
        )
        cls.produto = Produto.objects.create(
            nome="Produto Teste",
            descricao="Produto feito para testes",
            preco=10.99,
            ativo=True,
            categoria="vasos",
        )
        cls.url = reverse("criar_estoque")

    def setUp(self):
        self.client.login(username="admin", password="admin")

    def test_form_valid(self):
        """Testa se o formulário de criação de estoque com dados válidos redireciona corretamente e cria o estoque."""
        dados_validos = {"produto": self.produto.id, "quantia": 10}

        resposta = self.client.post(self.url, dados_validos)

        self.assertRedirects(resposta, reverse("estoque"))
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(Estoque.objects.filter(id=1).exists())

    def test_form_invalid(self):
        """Testa se o formulário de criação de estoque com quantia inválida (menor que 0) retorna erro de validação."""
        dados_invalidos = {
            "produto": self.produto.id,
            "quantia": -1,  # quantia não pode ser menor que 0
        }

        resposta = self.client.post(self.url, dados_invalidos)

        self.assertEqual(resposta.status_code, 200)
        self.assertFormError(
            resposta.context["form"],
            "quantia",
            "Certifique-se que este valor seja maior ou igual a 0.",
        )


class ApagarEstoqueTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser(
            "admin", "admin@email.com", "admin"
        )
        cls.usuario_comum = User.objects.create_user(
            "usuario", "usuario@email.com", "usuario"
        )

    def setUp(self):
        self.produto = Produto.objects.create(
            nome="Produto Teste",
            descricao="Produto feito para testes",
            preco=10.99,
            ativo=True,
            categoria="vasos",
        )
        self.estoque = Estoque.objects.create(produto=self.produto, quantia=10)
        self.url = reverse("apagar_estoque", kwargs={"pk": self.estoque.id})

    def test_apagar_superusuario(self):
        """Testa se o superusuário consegue apagar um estoque e é redirecionado para a lista de estoque."""
        self.client.login(username="admin", password="admin")

        resposta = self.client.post(self.url)

        self.assertEqual(Estoque.objects.count(), 0)
        self.assertRedirects(resposta, reverse("estoque"))

    def test_apagar_usuario_comum(self):
        """Testa se um usuário comum não pode apagar um estoque e recebe um status de erro 403."""
        self.client.login(username="usuario", password="usuario")

        resposta = self.client.post(self.url)

        self.assertEqual(Estoque.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)

    def test_apagar_sem_metodo_post(self):
        """Testa se ao tentar apagar um estoque sem usar o método POST, o servidor retorna erro 403."""
        self.client.login(username="admin", password="admin")

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 403)
