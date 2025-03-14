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
    path("produtos/", views.ProdutoList.as_view(), name="produtos"),
    path("produtos/novo/", views.ProdutoCreateForm.as_view(), name="criar_produto"),
    path(
        "produto/<int:pk>/editar/", views.ProdutoUpdate.as_view(), name="editar_produto"
    ),
    path("produto/<int:pk>/apagar/", views.apagar_produto, name="apagar_produto"),
    path("estoque/", views.EstoqueList.as_view(), name="listar_estoque"),
    path("estoque/novo/", views.EstoqueCreateForm.as_view(), name="criar_estoque"),
    path("estoque/<int:pk>/editar/", views.EstoqueUpdate.as_view(), name="editar_estoque"),
    path("estoque/<int:pk>/apagar/", views.apagar_estoque, name="apagar_estoque")
]
