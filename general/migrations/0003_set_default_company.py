# Data migration: crea empresa "Default" y asigna todas las filas existentes.
# Luego hace company no nullable.

import django.db.models.deletion
from django.db import migrations, models


def create_default_company_and_assign(apps, schema_editor):
    Company = apps.get_model("general", "Company")
    CompanyMembership = apps.get_model("general", "CompanyMembership")
    Rubro = apps.get_model("general", "Rubro")
    Unidad = apps.get_model("general", "Unidad")
    Subrubro = apps.get_model("general", "Subrubro")
    Proveedor = apps.get_model("general", "Proveedor")
    TipoMaterial = apps.get_model("general", "TipoMaterial")
    CategoriaMaterial = apps.get_model("general", "CategoriaMaterial")
    User = apps.get_model("auth", "User")

    default_company, _ = Company.objects.get_or_create(
        nombre="Default",
        defaults={"nombre": "Default"},
    )

    Rubro.objects.filter(company__isnull=True).update(company=default_company)
    Unidad.objects.filter(company__isnull=True).update(company=default_company)
    Subrubro.objects.filter(company__isnull=True).update(company=default_company)
    Proveedor.objects.filter(company__isnull=True).update(company=default_company)
    TipoMaterial.objects.filter(company__isnull=True).update(company=default_company)
    CategoriaMaterial.objects.filter(company__isnull=True).update(company=default_company)

    # Asignar todos los usuarios existentes a la empresa Default para que puedan entrar
    for user in User.objects.all():
        CompanyMembership.objects.get_or_create(
            user=user,
            company=default_company,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0002_add_company_multi_tenant"),
    ]

    operations = [
        migrations.RunPython(create_default_company_and_assign, noop),
        migrations.AlterField(
            model_name="categoriamaterial",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="categorias_material",
                to="general.company",
            ),
        ),
        migrations.AlterField(
            model_name="proveedor",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="proveedores",
                to="general.company",
            ),
        ),
        migrations.AlterField(
            model_name="rubro",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rubros",
                to="general.company",
            ),
        ),
        migrations.AlterField(
            model_name="subrubro",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subrubros",
                to="general.company",
            ),
        ),
        migrations.AlterField(
            model_name="tipomaterial",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tipos_material",
                to="general.company",
            ),
        ),
        migrations.AlterField(
            model_name="unidad",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="unidades",
                to="general.company",
            ),
        ),
    ]
