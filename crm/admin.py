from django.contrib import admin
from .models import Cliente, Lead, Produto, Estoque


class ProdutoAdmin(admin.ModelAdmin):
    fields = ("nome", "descricao", "preco", "categoria", "ativo")
    list_display = ("nome", "preco", "categoria", "ativo")
    list_filter = ("ativo",)


class EstoqueAdmin(admin.ModelAdmin):
    fields = ("produto", "quantia")
    list_display = ("produto", "quantia")


class ClienteAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Dados do cliente", {"fields": ["nome"]}),
        ("Informações de contato", {"fields": ["telefone", "email", "endereco"]}),
        ("Outros dados", {"fields": ["fonte", "status", "notas"]})
    ]
    list_display = ("nome", "telefone", "email", "endereco", "status")
    list_filter = ("status",)


class LeadAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Dados do Lead", {"fields": ["nome"]}),
        ("Informações de contato", {"fields": ["telefone", "email", "endereco"]}),
        ("Outros dados", {"fields": ["fonte", "status", "notas", "produto_interesse", "data_conversao"]})
    ]
    list_display = ("nome", "telefone", "email", "endereco", "status")
    list_filter = ("status", )


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Estoque, EstoqueAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Lead, LeadAdmin)
