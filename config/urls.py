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
from django.urls import path, include

from crm import views

produto_urls = [
    path("", views.ProdutoList.as_view(), name="produtos"),
    path("novo/", views.ProdutoCreateForm.as_view(), name="criar_produto"),
    path("<int:pk>/ver/", views.ProdutoDetail.as_view(), name="ver_produto"),
    path("<int:pk>/editar/", views.ProdutoUpdate.as_view(), name="editar_produto"),
    path("<int:pk>/apagar/", views.apagar_produto, name="apagar_produto"),
]

estoque_urls = [
    path("", views.EstoqueList.as_view(), name="estoque"),
    path("novo/", views.EstoqueCreateForm.as_view(), name="criar_estoque"),
    path("<int:pk>/ver/", views.EstoqueDetail.as_view(), name="ver_estoque"),
    path("<int:pk>/editar/", views.EstoqueUpdate.as_view(), name="editar_estoque"),
    path("<int:pk>/apagar/", views.apagar_estoque, name="apagar_estoque"),
]

cliente_urls = [
    path("", views.ClienteList.as_view(), name="clientes"),
    path("novo/", views.ClienteFormCreate.as_view(), name="criar_cliente"),
    path("<int:pk>/ver/", views.ClienteDetail.as_view(), name="ver_cliente"),
    path("<int:pk>/editar/", views.ClienteUpdate.as_view(), name="editar_cliente"),
    path("<int:pk>/apagar/", views.apagar_cliente, name="apagar_cliente"),
]

lead_urls = [
    path("", views.LeadList.as_view(), name="leads"),
    path("novo/", views.LeadFormCreate.as_view(), name="criar_lead"),
    path("<int:pk>/ver/", views.LeadDetail.as_view(), name="ver_lead"),
    path("<int:pk>/editar/", views.LeadUpdate.as_view(), name="editar_lead"),
    path("<int:pk>/apagar/", views.apagar_lead, name="apagar_lead"),
    path(
        "<int:pk>/converter/", views.ConverterLeadView.as_view(), name="converter_lead"
    ),
]

venda_urls = [
    path("", views.VendaList.as_view(), name="vendas"),
    path("novo/", views.VendaFormCreate.as_view(), name="criar_venda"),
    path("<int:pk>/ver/", views.VendaDetail.as_view(), name="ver_venda"),
    path("<int:pk>/editar/", views.VendaUpdate.as_view(), name="editar_venda"),
    path("<int:pk>/apagar/", views.apagar_venda, name="apagar_venda"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.IndexView.as_view(), name="index"),
    path("produtos/", include(produto_urls)),
    path("estoque/", include(estoque_urls)),
    path("clientes/", include(cliente_urls)),
    path("leads/", include(lead_urls)),
    path("vendas/", include(venda_urls)),
]
