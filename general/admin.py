from django.contrib import admin
from .models import CategoriaMaterial, Proveedor, Rubro, TipoMaterial, Unidad, Subrubro

@admin.register(Rubro)
class RubroAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    search_fields = ('nombre',) 

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    search_fields = ('nombre',) 

@admin.register(TipoMaterial)
class TipoMaterialAdmin(admin.ModelAdmin):
    search_fields = ('nombre',) 

@admin.register(CategoriaMaterial)
class CategoriaMaterialAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(Subrubro)
class SubrubroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rubro',)
    list_filter = ('rubro',)
    search_fields = ('nombre',)