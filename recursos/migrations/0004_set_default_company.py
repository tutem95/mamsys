# Asigna empresa Default a materiales, mano de obra, subcontratos y hojas de precios existentes.
# Luego hace company no nullable.

import django.db.models.deletion
from django.db import migrations, models


def set_default_company(apps, schema_editor):
    Company = apps.get_model("general", "Company")
    Material = apps.get_model("recursos", "Material")
    ManoDeObra = apps.get_model("recursos", "ManoDeObra")
    Subcontrato = apps.get_model("recursos", "Subcontrato")
    HojaPrecios = apps.get_model("recursos", "HojaPrecios")

    default_company = Company.objects.filter(nombre="Default").first()
    if not default_company:
        return

    Material.objects.filter(company__isnull=True).update(company=default_company)
    ManoDeObra.objects.filter(company__isnull=True).update(company=default_company)
    Subcontrato.objects.filter(company__isnull=True).update(company=default_company)
    HojaPrecios.objects.filter(company__isnull=True).update(company=default_company)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("recursos", "0003_add_company"),
    ]

    operations = [
        migrations.RunPython(set_default_company, noop),
        migrations.AlterField(
            model_name="hojaprecios",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hojas_precios",
                to="general.company",
            ),
        ),
        migrations.AlterField(
            model_name="manodeobra",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mano_de_obra",
                to="general.company",
            ),
        ),
        migrations.AlterField(
            model_name="material",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="materiales",
                to="general.company",
            ),
        ),
        migrations.AlterField(
            model_name="subcontrato",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subcontratos",
                to="general.company",
            ),
        ),
    ]
