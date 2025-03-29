from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from crm.models import Lead


class LeadCreateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser(
            "admin", "admin@email.com", "admin"
        )
        cls.url = reverse("criar_lead")

    def setUp(self):
        self.client.login(username="admin", password="admin")

    def test_form_valid(self):
        dados_validos = {
            "nome": "Lead comum",
            "telefone": "(11) 99122-1331",
            "email": "lead@email.com",
            "endereco": "Ruas das Flores, 123",
            "fonte": "Viu na rua",
            "status": "novo",
            "produto_interesse": "Qualquer coisa",
            "notas": "",
        }

        resposta = self.client.post(self.url, dados_validos)

        self.assertRedirects(resposta, reverse("leads"))
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(Lead.objects.filter(id=1).exists())

    def test_form_invalid(self):
        dados_invalidos = {
            "nome": "",  # como que não tem nome
            "telefone": "(11) 99122-1331",
            "email": "lead@email.com",
            "endereco": "Ruas das Flores, 123",
            "fonte": "Viu na rua",
            "status": "novo",
            "produto_interesse": "Qualquer coisa",
            "notas": "",
        }

        resposta = self.client.post(self.url, dados_invalidos)

        self.assertEqual(resposta.status_code, 200)
        self.assertFormError(
            resposta.context["form"], "nome", "Este campo é obrigatório."
        )


class ApagarLeadTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser(
            "admin", "admin@email.com", "admin"
        )
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
            notas="",
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
