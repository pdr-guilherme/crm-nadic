from django.contrib import admin
from .models import Produto, Estoque


class ProdutoAdmin(admin.ModelAdmin):
    fields = ("nome", "descricao", "preco", "categoria", "ativo")
    list_display = ("nome", "preco", "categoria", "ativo")
    list_filter = ("ativo",)


class EstoqueAdmin(admin.ModelAdmin):
    fields = ("produto", "quantia")
    list_display = ("produto", "quantia")


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Estoque, EstoqueAdmin)