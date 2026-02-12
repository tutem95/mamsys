from django.urls import path

from . import views

app_name = "presupuestos"

urlpatterns = [
    path("", views.presupuesto_list, name="presupuesto_list"),
    path("nuevo/", views.presupuesto_create, name="presupuesto_create"),
    path("<int:pk>/rubros/", views.presupuesto_rubros, name="presupuesto_rubros"),
    path(
        "<int:pk>/rubros/<int:rubro_pk>/subrubros/",
        views.presupuesto_subrubros,
        name="presupuesto_subrubros",
    ),
    path(
        "<int:pk>/rubros/<int:rubro_pk>/subrubros/<int:subrubro_pk>/tareas/",
        views.presupuesto_tareas,
        name="presupuesto_tareas",
    ),
    path(
        "<int:pk>/item/<int:item_pk>/eliminar/",
        views.presupuesto_item_delete,
        name="presupuesto_item_delete",
    ),
]
