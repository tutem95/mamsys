from django.contrib import admin
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Material, ManoDeObra, Subcontrato
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'proveedor', 'tipo', 'categoria',
        'unidad_de_venta', 'mostrar_cantidad', 'mostrar_precio',
        'moneda', 'mostrar_precio_analisis'
    )
    list_filter = ('proveedor', 'tipo', 'categoria', 'unidad_de_venta', 'moneda')
    search_fields = ('nombre', 'proveedor__nombre', 'categoria__nombre', 'tipo__nombre')
    actions = ['actualizar_precios_materiales']

    def mostrar_cantidad(self, obj):
        if obj.cantidad_por_unidad_venta is None:
            return "-"
        return f"{obj.cantidad_por_unidad_venta:,.2f}"
    mostrar_cantidad.short_description = "Cant. x Unidad Venta"

    def mostrar_precio(self, obj):
        if obj.precio_unidad_venta is None:
            return "-"
        return f"{obj.precio_unidad_venta:,.2f}"
    mostrar_precio.short_description = "Precio Unidad Venta"

    def mostrar_precio_analisis(self, obj):
        try:
            return f"{obj.precio_por_unidad_analisis():,.2f}"
        except:
            return "-"
    mostrar_precio_analisis.short_description = "Precio x Unidad Análisis"

    def actualizar_precios_materiales(self, request, queryset):
        changelist_url = reverse('admin:%s_%s_changelist' % (self.model._meta.app_label, self.model._meta.model_name))

        if 'apply' in request.POST:
            porcentaje_str = request.POST.get('porcentaje', '').replace(',', '.')

            # Usar getlist para obtener todos los IDs seleccionados
            selected_ids = request.POST.getlist('_selected_action')

            try:
                selected_ids = [int(pk) for pk in selected_ids]
            except ValueError:
                self.message_user(request, _("Error: Identificadores de materiales no válidos."), level=messages.ERROR)
                return HttpResponseRedirect(changelist_url)

            queryset = self.get_queryset(request).filter(pk__in=selected_ids)

            if not queryset.exists():
                self.message_user(request, _("Ningún material válido seleccionado para actualizar."), level=messages.WARNING)
                return HttpResponseRedirect(changelist_url)

            try:
                porcentaje = Decimal(porcentaje_str)
                if porcentaje == 0:
                    self.message_user(request, _("No se aplicó ningún cambio de precio ya que el porcentaje es 0%."), level=messages.WARNING)
                    return HttpResponseRedirect(changelist_url)

                updated_count = Material.actualizar_precios_por_porcentaje(queryset, porcentaje)

                self.message_user(request, _(f"Se actualizaron {updated_count} materiales con un porcentaje del {porcentaje}%."), level=messages.SUCCESS)
                return HttpResponseRedirect(changelist_url)

            except InvalidOperation:
                self.message_user(request, _("Error: Porcentaje no válido. Por favor, ingrese un número."), level=messages.ERROR)
                return HttpResponseRedirect(changelist_url)
            except Exception as e:
                self.message_user(request, _(f"Ocurrió un error inesperado al aplicar el porcentaje: {e}"), level=messages.ERROR)
                return HttpResponseRedirect(changelist_url)

        # Si es un GET o un POST sin 'apply', mostrar formulario
        selected_ids = queryset.values_list('pk', flat=True)
        context = {
            'title': _("Actualizar Precios de Materiales"),
            'queryset': queryset,
            'action_name': 'actualizar_precios_materiales',
            'selected_ids': list(selected_ids),
            'opts': self.model._meta,
            'media': self.media,
        }
        return render(request, 'admin/recursos/material/update_prices.html', context)

    actualizar_precios_materiales.short_description = _("Actualizar precios por porcentaje")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update-prices/', self.admin_site.admin_view(self.actualizar_precios_materiales), name='recursos_material_update_prices'),
        ]
        return my_urls + urls


admin.site.register(ManoDeObra)
admin.site.register(Subcontrato)
