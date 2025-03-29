from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from crm.models import Cliente


class ClienteCreateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser(
            "admin", "admin@email.com", "admin"
        )
        cls.url = reverse("criar_cliente")

    def setUp(self):
        self.client.login(username="admin", password="admin")

    def test_form_valid(self):
        """Testa se o formulário de criação de cliente com dados válidos redireciona corretamente e cria o cliente."""
        dados_validos = {
            "nome": "Cliente comum",
            "telefone": "(11) 99122-1331",
            "email": "cliente@email.com",
            "endereco": "Ruas das Flores, 123",
            "fonte": "Viu na rua",
            "status": "ativo",
            "notas": "",
        }

        resposta = self.client.post(self.url, dados_validos)

        self.assertRedirects(resposta, reverse("clientes"))
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(Cliente.objects.filter(id=1).exists())

    def test_form_invalid(self):
        """Testa se o formulário de criação de cliente com dados inválidos retorna erro de validação no campo 'endereco'."""
        dados_invalidos = {
            "nome": "Cliente comum",
            "telefone": "(11) 99122-1331",
            "email": "cliente@email.com",
            "endereco": "",  # mora na rua
            "fonte": "Viu na rua",
            "status": "ativo",
            "notas": "",
        }

        resposta = self.client.post(self.url, dados_invalidos)

        self.assertEqual(resposta.status_code, 200)
        self.assertFormError(
            resposta.context["form"], "endereco", "Este campo é obrigatório."
        )


class ApagarClienteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_usuario = User.objects.create_superuser(
            "admin", "admin@email.com", "admin"
        )
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
            notas="",
        )
        self.url = reverse("apagar_cliente", kwargs={"pk": self.cliente.id})

    def test_apagar_superusuario(self):
        """Testa se o superusuário consegue apagar um cliente e é redirecionado para a lista de clientes."""
        self.client.login(username="admin", password="admin")

        resposta = self.client.post(self.url)

        self.assertEqual(Cliente.objects.count(), 0)
        self.assertRedirects(resposta, reverse("clientes"))

    def test_apagar_usuario_comum(self):
        """Testa se um usuário comum não pode apagar um cliente e recebe um status de erro."""
        self.client.login(username="usuario", password="usuario")

        resposta = self.client.post(self.url)

        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)

    def test_apagar_sem_metodo_post(self):
        """Testa se ao tentar apagar um cliente sem usar o método POST, o servidor retorna erro 403."""
        self.client.login(username="admin", password="admin")

        resposta = self.client.get(self.url)

        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(resposta.status_code, 403)
