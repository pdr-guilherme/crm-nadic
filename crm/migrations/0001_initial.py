# Generated by Django 5.1.7 on 2025-03-08 21:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Faturamento",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Produto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nome",
                    models.CharField(max_length=100, verbose_name="Nome do produto"),
                ),
                (
                    "descricao",
                    models.CharField(
                        max_length=255, verbose_name="Descrição do produto"
                    ),
                ),
                (
                    "preco",
                    models.DecimalField(
                        decimal_places=2, max_digits=7, verbose_name="Preço do produto"
                    ),
                ),
                (
                    "ativo",
                    models.BooleanField(default=True, verbose_name="Produto ativo"),
                ),
                (
                    "data_criacao",
                    models.DateField(auto_now_add=True, verbose_name="Data de criação"),
                ),
                (
                    "categoria",
                    models.CharField(
                        choices=[
                            ("plantas", "Plantas"),
                            ("vasos", "Vasos"),
                            ("flores", "Flores"),
                            ("buquê", "Buquê de Flores"),
                            ("arranjo", "Arranjo de Flores"),
                            ("cesta", "Cesta de Presente"),
                        ],
                        max_length=17,
                        verbose_name="Categoria do produto",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Estoque",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantia",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Quantidade em estoque"
                    ),
                ),
                (
                    "produto",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="crm.produto"
                    ),
                ),
            ],
        ),
    ]
