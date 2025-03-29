from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from crm.models import Produto


class ProdutoCreateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_superuser("admin", "admin@email.com", "admin")
        cls.url = reverse("criar_produto")

    def setUp(self):
        self.client.login(username="admin", password="admin")

    def test_form_valid(self):
        """Testa se o formulário de criação de produto com dados válidos redireciona corretamente e cria o produto."""
        dados = {
            "nome": "Produto Teste",
            "descricao": "Produto feito para testes",
            "preco": 10.99,
            "ativo": True,
            "categoria": "vasos",
        }

        resposta = self.client.post(self.url, dados)

        self.assertRedirects(resposta, reverse("produtos"))
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(Produto.objects.filter(nome="Produto Teste").exists())

    def test_form_invalid(self):
        """Testa se o formulário de criação de produto com categoria inválida retorna erro de validação."""
        dados_invalidos = {
            "nome": "Produto Teste",
            "descricao": "Produto feito para testes",
            "preco": 10.99,
            "ativo": True,
            "categoria": "",
        }

        resposta = self.client.post(self.url, dados_invalidos)

        self.assertEqual(resposta.status_code, 200)
        self.assertFormError(
            resposta.context["form"], "categoria", "Este campo é obrigatório."
        )


class ApagarProdutoTest(TestCase):
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
        self.url = reverse("apagar_produto", kwargs={"pk": self.produto.id})

    def test_apagar_superusuario(self):
        """Testa se o superusuário consegue apagar um produto e é redirecionado para a lista de produtos."""
        self.client.login(username="admin", password="admin")

        resposta = self.client.post(self.url)

        self.assertEqual(Produto.objects.count(), 0)
        self.assertRedirects(resposta, reverse("produtos"))

    def test_apagar_usuario_comum(self):
        """Testa se um usuário comum não pode apagar um produto e recebe um status de erro 403."""
        self.client.login(username="usuario", password="usuario")

        resposta = self.client.post(self.url)

        self.assertEqual(Produto.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)

    def test_apagar_sem_metodo_post(self):
        """Testa se ao tentar apagar um produto sem usar o método POST, o servidor retorna erro 403."""
        self.client.login(username="admin", password="admin")

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 403)
