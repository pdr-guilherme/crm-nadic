from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Estoque, Produto


class VerificarSuperusuarioMixinTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_user("usuario", "usuario@gmail.com", "987654")
        cls.super_usuario = User.objects.create_superuser(
            "admin", "admin@email.com", "admin"
        )
        cls.url_protegida = reverse("criar_produto")

    def test_mixin_sem_permissao(self):
        self.client.login(username="usuario", password="987654")
        resposta = self.client.get(self.url_protegida)
        self.assertEqual(resposta.status_code, 403)

    def test_mixin_com_permissao(self):
        self.client.login(username="admin", password="admin")
        resposta = self.client.get(self.url_protegida)
        self.assertEqual(resposta.status_code, 200)


class ProdutoCreateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_superuser("admin", "admin@email.com", "admin")
        cls.url = reverse("criar_produto")

    def test_form_valid(self):
        self.client.login(username="admin", password="admin")

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
        self.client.login(username="admin", password="admin")

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
        self.client.login(username="admin", password="admin")

        resposta = self.client.post(self.url)

        self.assertEqual(Produto.objects.count(), 0)
        self.assertRedirects(resposta, reverse("produtos"))

    def test_apagar_usuario_comum(self):
        self.client.login(username="usuario", password="usuario")

        resposta = self.client.post(self.url)

        self.assertEqual(Produto.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)

    def test_apagar_sem_metodo_post(self):
        self.client.login(username="admin", password="admin")

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 403)


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

    def test_form_valid(self):
        self.client.login(username="admin", password="admin")

        dados_validos = {"produto": self.produto.id, "quantia": 10}

        resposta = self.client.post(self.url, dados_validos)

        self.assertRedirects(resposta, reverse("estoque"))
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(Estoque.objects.filter(id=1).exists())

    def test_form_invalid(self):
        self.client.login(username="admin", password="admin")

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
        self.client.login(username="admin", password="admin")

        resposta = self.client.post(self.url)

        self.assertEqual(Estoque.objects.count(), 0)
        self.assertRedirects(resposta, reverse("estoque"))

    def test_apagar_usuario_comum(self):
        self.client.login(username="usuario", password="usuario")

        resposta = self.client.post(self.url)

        self.assertEqual(Estoque.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)

    def test_apagar_sem_metodo_post(self):
        self.client.login(username="admin", password="admin")

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 403)


class ClienteCreateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser("admin", "admin@email.com", "admin")
        cls.url = reverse("criar_cliente")

    def test_form_valid(self):
        self.client.login(username="admin", password="admin")

        dados_validos = {
            "nome": "Cliente comum",
            "telefone": "(11) 99122-1331",
            "email": "cliente@email.com",
            "endereco": "Ruas das Flores, 123",
            "fonte": "Viu na rua",
            "status": "ativo",
            "notas": ""
        }

        resposta = self.client.post(self.url, dados_validos)

        self.assertRedirects(resposta, reverse("clientes"))
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(Cliente.objects.filter(id=1).exists())

    def test_form_invalid(self):
        self.client.login(username="admin", password="admin")

        dados_invalidos = {
            "nome": "Cliente comum",
            "telefone": "(11) 99122-1331",
            "email": "cliente@email.com",
            "endereco": "", # mora na rua
            "fonte": "Viu na rua",
            "status": "ativo",
            "notas": ""
        }

        resposta = self.client.post(self.url, dados_invalidos)

        self.assertEqual(resposta.status_code, 200)
        self.assertFormError(resposta.context["form"], "endereco", "Este campo é obrigatório.")


class ApagarClienteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser("admin", "admin@email.com", "admin")
        cls.usuario_comum = User.objects.create_user(
            "usuario", "usuario@email.com", "usuario"
        )

    def setUp(self):
        self.cliente = Cliente.objects.create(
            nome="Cliente comum",
            telefone="(11) 99122-1331",
            email="cliente@email.com",
            endereco="Ruas das Flores, 123",
            fonte="Viu na rua",
            status="ativo",
            notas=""
        )
        self.url = reverse("apagar_cliente", kwargs={"pk": self.cliente.id})

    def test_apagar_superusuario(self):
        self.client.login(username="admin", password="admin")

        resposta = self.client.post(self.url)

        self.assertEqual(Cliente.objects.count(), 0)
        self.assertRedirects(resposta, reverse("clientes"))

    def test_apagar_usuario_comum(self):
        self.client.login(username="usuario", password="usuario")

        resposta = self.client.post(self.url)

        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)

    def test_apagar_sem_metodo_post(self):
        self.client.login(username="admin", password="admin")

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 403)