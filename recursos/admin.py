from django.contrib import admin
from .models import Material, ManoDeObra, Subcontrato # Importa todos los modelos de recursos

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    # Campos que se mostrarán como columnas en la tabla principal
    list_display = (
        'nombre',
        'proveedor',
        'tipo',
        'categoria',
        'unidad_de_venta',
        'cantidad_por_unidad_venta',
        'precio_unidad_venta',
        'get_precio_por_unidad_analisis_display', # Usamos este método para el display
        'moneda',
        'obtener_precio_en_ars_o_usd' # Mostrar precio convertido, si lo deseamos (más adelante)
    )

    # Campos por los que se puede filtrar en el panel lateral derecho
    list_filter = (
        'proveedor',
        'tipo',
        'categoria',
        'unidad_de_venta', # También podemos filtrar por unidad de venta
        'moneda',
    )

    # Campos por los que se puede buscar en la barra de búsqueda superior
    search_fields = (
        'nombre',
        'proveedor__nombre', # Permite buscar por el nombre del proveedor relacionado
        'tipo__nombre',      # Permite buscar por el nombre del tipo de material
        'categoria__nombre', # Permite buscar por el nombre de la categoría de material
    )

    # Campos que se convierten en enlaces a la página de edición del objeto relacionado
    raw_id_fields = ('proveedor', 'tipo', 'categoria', 'unidad_de_venta',) # Útil para muchos objetos, muestra ID en vez de select largo

    # Opcional: Campo para ordenar por defecto en la vista de lista
    ordering = ('nombre',)

    # Ahora, necesitamos definir el método para el display del precio de unidad de análisis
    # Haremos una pequeña modificación al modelo para asegurar que el display sea consistente
    # (Esto lo haremos en el modelo, no aquí, pero lo referenciamos)

    def get_precio_por_unidad_analisis_display(self, obj):
        # Formatea el precio para que se vea más legible en la tabla
        if obj.cantidad_por_unidad_venta and obj.cantidad_por_unidad_venta != 0:
            return f"{obj.precio_por_unidad_analisis():,.4f} {obj.moneda}/{obj.unidad_de_venta.nombre}"
        return "N/A"
    get_precio_por_unidad_analisis_display.short_description = "Precio U. Análisis" # Nombre de la columna
    get_precio_por_unidad_analisis_display.admin_order_field = 'precio_unidad_venta' # Permite ordenar por este campo (usando el precio original)

    def obtener_precio_en_ars_o_usd(self, obj):
        # Aquí irá la lógica para mostrar el precio en ARS o USD.
        # Por ahora, solo es un placeholder.
        # Este campo se completará cuando tengamos el modelo TipoDeCambio.
        return "N/A (Lógica de conversión pendiente)"
    obtener_precio_en_ars_o_usd.short_description = "Precio Conv."


# Registros simples para los otros modelos de recursos
admin.site.register(ManoDeObra)
admin.site.register(Subcontrato)