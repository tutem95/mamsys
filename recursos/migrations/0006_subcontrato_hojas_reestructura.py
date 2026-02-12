# Migración: Subcontrato nueva estructura + HojaPreciosSubcontrato

import django.db.models.deletion
from django.db import migrations, models


def migrar_subcontratos(apps, schema_editor):
    """Migra Subcontrato de estructura antigua a nueva."""
    Subcontrato = apps.get_model("recursos", "Subcontrato")
    Rubro = apps.get_model("general", "Rubro")
    Subrubro = apps.get_model("general", "Subrubro")

    for s in Subcontrato.objects.all():
        company = s.company
        if not company:
            continue
        # Rubro y Subrubro por defecto
        rubro, _ = Rubro.objects.get_or_create(
            company=company, nombre="General", defaults={"nombre": "General"}
        )
        subrubro, _ = Subrubro.objects.get_or_create(
            company=company, rubro=rubro, nombre="General", defaults={"nombre": "General"}
        )
        s.rubro_new = rubro
        s.subrubro_new = subrubro
        s.tarea_new = s.descripcion or ""
        s.unidad_de_venta_new = s.unidad_de_analisis
        s.precio_unidad_venta_new = s.precio_por_unidad
        s.cantidad_por_unidad_venta = 1
        s.save()


def reverse_migrar(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0004_equipo"),
        ("recursos", "0005_alter_manodeobra_equipo"),
    ]

    operations = [
        migrations.AlterUniqueTogether(name="subcontrato", unique_together=set()),
        # Campos nuevos
        migrations.AddField(
            model_name="subcontrato",
            name="rubro_new",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="subcontratos_temp",
                to="general.rubro",
            ),
        ),
        migrations.AddField(
            model_name="subcontrato",
            name="subrubro_new",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="subcontratos_temp",
                to="general.subrubro",
            ),
        ),
        migrations.AddField(
            model_name="subcontrato",
            name="tarea_new",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="subcontrato",
            name="proveedor_new",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="subcontratos_temp",
                to="general.proveedor",
            ),
        ),
        migrations.AddField(
            model_name="subcontrato",
            name="cantidad_por_unidad_venta",
            field=models.DecimalField(
                decimal_places=4, default=1, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="subcontrato",
            name="unidad_de_venta_new",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="subcontratos_venta_temp",
                to="general.unidad",
            ),
        ),
        migrations.AddField(
            model_name="subcontrato",
            name="precio_unidad_venta_new",
            field=models.DecimalField(
                decimal_places=4, max_digits=12, null=True
            ),
        ),
        migrations.RunPython(migrar_subcontratos, reverse_migrar),
        # Remover campos viejos
        migrations.RemoveField(model_name="subcontrato", name="descripcion"),
        migrations.RemoveField(model_name="subcontrato", name="proveedor"),
        migrations.RemoveField(model_name="subcontrato", name="unidad_de_analisis"),
        migrations.RemoveField(model_name="subcontrato", name="precio_por_unidad"),
        # Renombrar campos nuevos
        migrations.RenameField(
            model_name="subcontrato", old_name="rubro_new", new_name="rubro"
        ),
        migrations.RenameField(
            model_name="subcontrato", old_name="subrubro_new", new_name="subrubro"
        ),
        migrations.RenameField(
            model_name="subcontrato", old_name="tarea_new", new_name="tarea"
        ),
        migrations.RenameField(
            model_name="subcontrato", old_name="proveedor_new", new_name="proveedor"
        ),
        migrations.RenameField(
            model_name="subcontrato",
            old_name="unidad_de_venta_new",
            new_name="unidad_de_venta",
        ),
        migrations.RenameField(
            model_name="subcontrato",
            old_name="precio_unidad_venta_new",
            new_name="precio_unidad_venta",
        ),
        migrations.AlterField(
            model_name="subcontrato",
            name="rubro",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="subcontratos",
                to="general.rubro",
            ),
        ),
        migrations.AlterField(
            model_name="subcontrato",
            name="subrubro",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="subcontratos",
                to="general.subrubro",
            ),
        ),
        migrations.AlterField(
            model_name="subcontrato",
            name="tarea",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="subcontrato",
            name="proveedor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="subcontratos",
                to="general.proveedor",
            ),
        ),
        migrations.AlterField(
            model_name="subcontrato",
            name="cantidad_por_unidad_venta",
            field=models.DecimalField(
                decimal_places=4, default=1, max_digits=10
            ),
        ),
        migrations.AlterField(
            model_name="subcontrato",
            name="unidad_de_venta",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="subcontratos_venta",
                to="general.unidad",
            ),
        ),
        migrations.AlterField(
            model_name="subcontrato",
            name="precio_unidad_venta",
            field=models.DecimalField(decimal_places=4, max_digits=12),
        ),
        migrations.AlterUniqueTogether(
            name="subcontrato",
            unique_together={("company", "rubro", "subrubro", "tarea")},
        ),
        # Crear modelos de hojas de subcontratos
        migrations.CreateModel(
            name="HojaPreciosSubcontrato",
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
                        related_name="hojas_precios_subcontrato",
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
                        to="recursos.hojapreciossubcontrato",
                    ),
                ),
            ],
            options={
                "verbose_name": "Hoja de Precios Subcontrato",
                "verbose_name_plural": "Hojas de Precios Subcontrato",
                "ordering": ["-creado_en"],
                "unique_together": {("company", "nombre")},
            },
        ),
        migrations.CreateModel(
            name="HojaPrecioSubcontrato",
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
                    "moneda",
                    models.CharField(
                        choices=[
                            ("ARS", "Pesos Argentinos (ARS)"),
                            ("USD", "Dólares Estadounidenses (USD)"),
                        ],
                        default="ARS",
                        max_length=3,
                    ),
                ),
                (
                    "hoja",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="detalles",
                        to="recursos.hojapreciossubcontrato",
                    ),
                ),
                (
                    "subcontrato",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="hojas_precios",
                        to="recursos.subcontrato",
                    ),
                ),
            ],
            options={
                "verbose_name": "Precio de Subcontrato en Hoja",
                "verbose_name_plural": "Precios de Subcontrato en Hoja",
                "ordering": [
                    "subcontrato__rubro__nombre",
                    "subcontrato__subrubro__nombre",
                    "subcontrato__tarea",
                ],
            },
        ),
    ]
