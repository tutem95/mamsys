# RefEquipo: subcategoría de Equipo (como Subrubro es a Rubro)

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("general", "0004_equipo"),
    ]

    operations = [
        migrations.CreateModel(
            name="RefEquipo",
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
                (
                    "equipo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ref_equipos",
                        to="general.equipo",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ref_equipos",
                        to="general.company",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ref. Equipo",
                "verbose_name_plural": "Ref. Equipos",
                "ordering": ["equipo__nombre", "nombre"],
                "unique_together": {("company", "equipo", "nombre")},
            },
        ),
    ]
