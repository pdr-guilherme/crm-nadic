from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Cliente, Estoque, Produto, Lead, Venda


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


class LeadCreateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser("admin", "admin@email.com", "admin")
        cls.url = reverse("criar_lead")

    def test_form_valid(self):
        self.client.login(username="admin", password="admin")

        dados_validos = {
            "nome": "Lead comum",
            "telefone": "(11) 99122-1331",
            "email": "lead@email.com",
            "endereco": "Ruas das Flores, 123",
            "fonte": "Viu na rua",
            "status": "novo",
            "produto_interesse": "Qualquer coisa",
            "notas": ""
        }

        resposta = self.client.post(self.url, dados_validos)

        self.assertRedirects(resposta, reverse("leads"))
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(Lead.objects.filter(id=1).exists())

    def test_form_invalid(self):
        self.client.login(username="admin", password="admin")

        dados_invalidos = {
            "nome": "", # como que não tem nome
            "telefone": "(11) 99122-1331",
            "email": "lead@email.com",
            "endereco": "Ruas das Flores, 123",
            "fonte": "Viu na rua",
            "status": "novo",
            "produto_interesse": "Qualquer coisa",
            "notas": ""
        }

        resposta = self.client.post(self.url, dados_invalidos)

        self.assertEqual(resposta.status_code, 200)
        self.assertFormError(resposta.context["form"], "nome", "Este campo é obrigatório.")



class ApagarLeadTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser("admin", "admin@email.com", "admin")
        cls.usuario_comum = User.objects.create_user(
            "usuario", "usuario@email.com", "usuario"
        )

    def setUp(self):
        self.lead = Lead.objects.create(
            nome="Lead comum",
            telefone="(11) 99122-1331",
            email="lead@email.com",
            endereco="Ruas das Flores, 123",
            fonte="Viu na rua",
            status="novo",
            produto_interesse="Qualquer coisa",
            notas=""
        )
        self.url = reverse("apagar_lead", kwargs={"pk": self.lead.id})

    def test_apagar_superusuario(self):
        self.client.login(username="admin", password="admin")

        resposta = self.client.post(self.url)

        self.assertEqual(Lead.objects.count(), 0)
        self.assertRedirects(resposta, reverse("leads"))

    def test_apagar_usuario_comum(self):
        self.client.login(username="usuario", password="usuario")

        resposta = self.client.post(self.url)

        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)

    def test_apagar_sem_metodo_post(self):
        self.client.login(username="admin", password="admin")

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 403)


class ConverterLeadViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser("admin", "admin@email.com", "admin")

    def setUp(self):
        self.lead_qualificado = Lead.objects.create(
            nome="Lead Qualificado",
            telefone="123456789",
            email="lead@email.com",
            endereco="Rua bem Real, 123",
            fonte="Website",
            status="qualificado",
            produto_interesse="vasos",
            responsavel=self.super_usuario,
        )

        self.lead_novo = Lead.objects.create(
            nome="Lead Novo",
            telefone="987654321",
            email="leadnovo@exemplo.com",
            endereco="Avenidaaaaaa, 456",
            fonte="E-mail",
            status="novo",
            produto_interesse="vasos",
            responsavel=self.super_usuario,
        )

    def test_converter_lead_sucesso(self):
        self.client.login(username="admin", password="admin")
        url = reverse("converter_lead", kwargs={"pk": self.lead_qualificado.pk})

        resposta = self.client.post(url)

        self.assertRedirects(resposta, reverse("clientes"))

        cliente = Cliente.objects.get(nome=self.lead_qualificado.nome)
        self.assertEqual(cliente.nome, self.lead_qualificado.nome)
        self.assertEqual(cliente.telefone, self.lead_qualificado.telefone)
        self.assertEqual(cliente.email, self.lead_qualificado.email)
        self.assertEqual(cliente.status, "ativo")

    def test_converter_lead_erro_status_inadequado(self):
        self.client.login(username="admin", password="admin")
        url = reverse("converter_lead", kwargs={"pk": self.lead_novo.pk})

        # Faz uma requisição GET
        resposta = self.client.post(url)

        # Verifica se a resposta contém uma mensagem de erro
        self.assertEqual(resposta.status_code, 400)
        self.assertIn("Erro", resposta.content.decode())


class VendaFormCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser("admin", "admin@email.com", "admin")
        cls.cliente = Cliente.objects.create(
            nome="Cliente comum",
            telefone="(11) 99122-1331",
            email="cliente@email.com",
            endereco="Ruas das Flores, 123",
            fonte="Viu na rua",
            status="ativo",
            notas=""
        )
        cls.produto1 = Produto.objects.create(
            nome="Produto Teste 1",
            descricao="Produto de Teste 1",
            preco=10.99,
            categoria="flores",
            ativo=True
        )
        cls.produto2 = Produto.objects.create(
            nome="Produto Teste 2",
            descricao="Produto de Teste 2",
            preco=20.99,
            categoria="vasos",
            ativo=True
        )
        cls.estoque1 = Estoque.objects.create(produto=cls.produto1, quantia=10)
        cls.estoque2 = Estoque.objects.create(produto=cls.produto2, quantia=0)

        cls.url = reverse("criar_venda")

    def test_form_valid(self):
        self.client.login(username="admin", password="admin")

        dados_validos = {
            "cliente": self.cliente.id,
            "produtos": [self.produto1.id],
            "status": "concluida",
            "forma_pagamento": "Cartão de Crédito",
        }

        resposta = self.client.post(self.url, dados_validos)


        self.assertRedirects(resposta, reverse("vendas"))
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(Venda.objects.filter(cliente=self.cliente).exists())

        self.estoque1.refresh_from_db()
        self.assertEqual(self.estoque1.quantia, 9)

    def test_form_invalid(self):
        self.client.login(username="admin", password="admin")

        dados_invalidos = {
            "cliente": self.cliente.id,
            "produtos": [self.produto2.id], # produto sem estoque
            "status": "concluida",
            "forma_pagamento": "Cartão de Crédito",
        }

        resposta = self.client.post(self.url, dados_invalidos)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, f"{self.produto2.nome} não disponível, tente novamente")


class ApagarVendaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser("admin", "admin@email.com", "admin")
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
            notas=""
        )

    def setUp(self):
        self.produto1 = Produto.objects.create(
            nome="Produto Teste 1",
            descricao="Produto de Teste 1",
            preco=10.99,
            categoria="flores",
            ativo=True
        )
        self.produto2 = Produto.objects.create(
            nome="Produto Teste 2",
            descricao="Produto de Teste 2",
            preco=20.99,
            categoria="vasos",
            ativo=True
        )
        self.estoque1 = Estoque.objects.create(produto=self.produto1, quantia=10)
        self.estoque2 = Estoque.objects.create(produto=self.produto2, quantia=5)

        self.venda = Venda.objects.create(cliente=self.cliente, forma_pagamento="Crédito", status="concluida")
        self.venda.produtos.set([self.produto1, self.produto2])

        self.url = reverse("apagar_venda", kwargs={"pk": self.venda.id})

    def test_apagar_superusuario(self):
        self.client.login(username="admin", password="admin")

        resposta = self.client.post(self.url)

        self.assertEqual(Venda.objects.count(), 0)
        self.assertRedirects(resposta, reverse("vendas"))

    def test_apagar_usuario_comum(self):
        self.client.login(username="usuario", password="usuario")

        resposta = self.client.post(self.url)

        self.assertEqual(Venda.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)

    def test_apagar_sem_metodo_post(self):
        self.client.login(username="admin", password="admin")

        resposta = self.client.get(self.url)

        self.assertEqual(Venda.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)
