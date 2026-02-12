from django.contrib import admin
from .models import (
    CategoriaMaterial,
    Company,
    CompanyMembership,
    Equipo,
    Proveedor,
    RefEquipo,
    Rubro,
    Subrubro,
    TipoMaterial,
    Unidad,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("nombre",)


@admin.register(CompanyMembership)
class CompanyMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "company")
    list_filter = ("company",)

@admin.register(Rubro)
class RubroAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)
    list_filter = ('company',)


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


@admin.register(RefEquipo)
class RefEquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'equipo',)
    list_filter = ('equipo',)
    search_fields = ('nombre',)