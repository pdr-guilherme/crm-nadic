"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from crm import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.IndexView.as_view(), name="index"),
    path("produtos/", views.ProdutoList.as_view(), name="produtos"),
    path("produtos/novo/", views.ProdutoCreateForm.as_view(), name="criar_produto"),
    path(
        "produto/<int:pk>/editar/", views.ProdutoUpdate.as_view(), name="editar_produto"
    ),
    path("produto/<int:pk>/apagar/", views.apagar_produto, name="apagar_produto"),
    path("estoque/", views.EstoqueList.as_view(), name="estoque"),
    path("estoque/novo/", views.EstoqueCreateForm.as_view(), name="criar_estoque"),
    path("estoque/<int:pk>/editar/", views.EstoqueUpdate.as_view(), name="editar_estoque"),
    path("estoque/<int:pk>/apagar/", views.apagar_estoque, name="apagar_estoque"),
    path("clientes/", views.ClienteList.as_view(), name="clientes"),
    path("clientes/novo/", views.ClienteFormCreate.as_view(), name="criar_cliente"),
    path("clientes/<int:pk>/editar/", views.ClienteUpdate.as_view(), name="editar_cliente"),
    path("clientes/<int:pk>/apagar/", views.apagar_cliente, name="apagar_cliente"),
    path("leads/", views.LeadList.as_view(), name="leads"),
    path("leads/novo/", views.LeadFormCreate.as_view(), name="criar_lead"),
    path("leads/<int:pk>/editar/", views.LeadUpdate.as_view(), name="editar_lead"),
    path("leads/<int:pk>/apagar/", views.apagar_lead, name="apagar_lead"),
    path("leads/<int:pk>/converter/", views.ConverterLeadView.as_view(), name="converter_lead"),
    path("vendas/", views.VendaList.as_view(), name="vendas"),
    path("vendas/novo/", views.VendaFormCreate.as_view(), name="criar_venda"),
    path("vendas/<int:pk>/editar/", views.VendaUpdate.as_view(), name="editar_venda"),
    path("vendas/<int:pk>/apagar/", views.apagar_venda, name="apagar_venda")
]
