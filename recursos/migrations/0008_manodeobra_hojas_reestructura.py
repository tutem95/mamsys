# Migración: ManoDeObra nueva estructura + HojaPreciosManoDeObra

import django.db.models.deletion
from django.db import migrations, models


def migrar_mano_de_obra(apps, schema_editor):
    """Migra ManoDeObra de estructura antigua a nueva."""
    ManoDeObra = apps.get_model("recursos", "ManoDeObra")
    Rubro = apps.get_model("general", "Rubro")
    Subrubro = apps.get_model("general", "Subrubro")
    RefEquipo = apps.get_model("general", "RefEquipo")

    for md in ManoDeObra.objects.all():
        company = md.company
        if not company:
            continue
        # Rubro y Subrubro por defecto
        rubro, _ = Rubro.objects.get_or_create(
            company=company, nombre="General", defaults={"nombre": "General"}
        )
        subrubro, _ = Subrubro.objects.get_or_create(
            company=company, rubro=rubro, nombre="General",
            defaults={"nombre": "General"}
        )
        # RefEquipo por defecto para ese equipo
        ref_equipo, _ = RefEquipo.objects.get_or_create(
            company=company, equipo=md.equipo, nombre="General",
            defaults={"nombre": "General"}
        )
        md.rubro_new = rubro
        md.subrubro_new = subrubro
        md.tarea_new = md.descripcion_puesto or ""
        md.ref_equipo_new = ref_equipo
        md.cantidad_por_unidad_venta = 1
        md.unidad_de_venta_new = md.unidad_de_analisis
        md.precio_unidad_venta_new = md.precio_por_unidad
        md.save()


def reverse_migrar(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0005_refequipo"),
        ("recursos", "0007_alter_subcontrato_options"),
    ]

    operations = [
        migrations.AlterUniqueTogether(name="manodeobra", unique_together=set()),
        # Campos nuevos
        migrations.AddField(
            model_name="manodeobra",
            name="rubro_new",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mano_de_obra_temp",
                to="general.rubro",
            ),
        ),
        migrations.AddField(
            model_name="manodeobra",
            name="subrubro_new",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mano_de_obra_temp",
                to="general.subrubro",
            ),
        ),
        migrations.AddField(
            model_name="manodeobra",
            name="tarea_new",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="manodeobra",
            name="ref_equipo_new",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mano_de_obra_temp",
                to="general.refequipo",
            ),
        ),
        migrations.AddField(
            model_name="manodeobra",
            name="cantidad_por_unidad_venta",
            field=models.DecimalField(
                decimal_places=4, default=1, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="manodeobra",
            name="unidad_de_venta_new",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mano_de_obra_unidades_temp",
                to="general.unidad",
            ),
        ),
        migrations.AddField(
            model_name="manodeobra",
            name="precio_unidad_venta_new",
            field=models.DecimalField(decimal_places=4, max_digits=12, null=True),
        ),
        migrations.RunPython(migrar_mano_de_obra, reverse_migrar),
        # Remover campos viejos
        migrations.RemoveField(model_name="manodeobra", name="descripcion_puesto"),
        migrations.RemoveField(model_name="manodeobra", name="unidad_de_analisis"),
        migrations.RemoveField(model_name="manodeobra", name="precio_por_unidad"),
        # Renombrar
        migrations.RenameField(
            model_name="manodeobra", old_name="rubro_new", new_name="rubro"
        ),
        migrations.RenameField(
            model_name="manodeobra", old_name="subrubro_new", new_name="subrubro"
        ),
        migrations.RenameField(
            model_name="manodeobra", old_name="tarea_new", new_name="tarea"
        ),
        migrations.RenameField(
            model_name="manodeobra",
            old_name="ref_equipo_new",
            new_name="ref_equipo",
        ),
        migrations.RenameField(
            model_name="manodeobra",
            old_name="unidad_de_venta_new",
            new_name="unidad_de_venta",
        ),
        migrations.RenameField(
            model_name="manodeobra",
            old_name="precio_unidad_venta_new",
            new_name="precio_unidad_venta",
        ),
        migrations.AlterField(
            model_name="manodeobra",
            name="rubro",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mano_de_obra",
                to="general.rubro",
            ),
        ),
        migrations.AlterField(
            model_name="manodeobra",
            name="subrubro",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mano_de_obra",
                to="general.subrubro",
            ),
        ),
        migrations.AlterField(
            model_name="manodeobra",
            name="tarea",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="manodeobra",
            name="ref_equipo",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mano_de_obra",
                to="general.refequipo",
            ),
        ),
        migrations.AlterField(
            model_name="manodeobra",
            name="cantidad_por_unidad_venta",
            field=models.DecimalField(
                decimal_places=4, default=1, max_digits=10
            ),
        ),
        migrations.AlterField(
            model_name="manodeobra",
            name="unidad_de_venta",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="mano_de_obra_unidades",
                to="general.unidad",
            ),
        ),
        migrations.AlterField(
            model_name="manodeobra",
            name="precio_unidad_venta",
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
        migrations.AlterUniqueTogether(
            name="manodeobra",
            unique_together={("company", "rubro", "subrubro", "tarea", "equipo", "ref_equipo")},
        ),
        # Crear modelos de hojas de mano de obra
        migrations.CreateModel(
            name="HojaPreciosManoDeObra",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hojas_precios_mano_de_obra",
                        to="general.company",
                    ),
                ),
                (
                    "origen",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="copias",
                        to="recursos.hojapreciosmanodeobra",
                    ),
                ),
            ],
            options={
                "verbose_name": "Hoja de Precios Mano de Obra",
                "verbose_name_plural": "Hojas de Precios Mano de Obra",
                "ordering": ["-creado_en"],
                "unique_together": {("company", "nombre")},
            },
        ),
        migrations.CreateModel(
            name="HojaPrecioManoDeObra",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "cantidad_por_unidad_venta",
                    models.DecimalField(decimal_places=4, max_digits=10),
                ),
                (
                    "precio_unidad_venta",
                    models.DecimalField(decimal_places=4, max_digits=12),
                ),
                (
                    "hoja",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="detalles",
                        to="recursos.hojapreciosmanodeobra",
                    ),
                ),
                (
                    "mano_de_obra",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="hojas_precios",
                        to="recursos.manodeobra",
                    ),
                ),
            ],
            options={
                "verbose_name": "Precio de Mano de Obra en Hoja",
                "verbose_name_plural": "Precios de Mano de Obra en Hoja",
                "ordering": [
                    "mano_de_obra__rubro__nombre",
                    "mano_de_obra__subrubro__nombre",
                    "mano_de_obra__tarea",
                ],
            },
        ),
    ]
