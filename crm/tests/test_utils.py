from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from crm.models import Cliente, Lead


class VerificarSuperusuarioMixinTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = User.objects.create_user(
            "usuario", "usuario@gmail.com", "usuario"
        )
        cls.super_usuario = User.objects.create_superuser(
            "admin", "admin@email.com", "admin"
        )
        cls.url_protegida = reverse("criar_produto")

    def test_mixin_sem_permissao(self):
        """Testa se um usuário sem permissão recebe erro 403 ao tentar acessar uma URL protegida."""
        self.client.login(username="usuario", password="usuario")
        resposta = self.client.get(self.url_protegida)
        self.assertEqual(resposta.status_code, 403)

    def test_mixin_com_permissao(self):
        """Testa se um superusuário com permissão consegue acessar uma URL protegida e recebe status 200."""
        self.client.login(username="admin", password="admin")
        resposta = self.client.get(self.url_protegida)
        self.assertEqual(resposta.status_code, 200)


class ConverterLeadViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser(
            "admin", "admin@email.com", "admin"
        )

    def setUp(self):
        self.client.login(username="admin", password="admin")
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
        """Testa se a conversão de um lead qualificado em cliente é bem-sucedida e cria um cliente com os dados do lead."""

        url = reverse("converter_lead", kwargs={"pk": self.lead_qualificado.pk})

        resposta = self.client.post(url)

        self.assertRedirects(resposta, reverse("clientes"))

        cliente = Cliente.objects.get(nome=self.lead_qualificado.nome)
        self.assertEqual(cliente.nome, self.lead_qualificado.nome)
        self.assertEqual(cliente.telefone, self.lead_qualificado.telefone)
        self.assertEqual(cliente.email, self.lead_qualificado.email)
        self.assertEqual(cliente.status, "ativo")

    def test_converter_lead_erro_status_inadequado(self):
        """Testa se a conversão de um lead com status inadequado (novo) retorna erro 400 com mensagem de erro."""
        url = reverse("converter_lead", kwargs={"pk": self.lead_novo.pk})

        resposta = self.client.post(url)

        self.assertEqual(resposta.status_code, 400)
        self.assertIn("Erro", resposta.content.decode())
