from django.conf import settings
from django.db import models


class Company(models.Model):
    """
    Empresa/tenant. Todas las filas de catálogos y recursos pertenecen a una company.
    """
    nombre = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class CompanyMembership(models.Model):
    """Usuario pertenece a una empresa por membership. En login se setea la company activa."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="company_memberships",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    class Meta:
        verbose_name = "Membership empresa"
        verbose_name_plural = "Memberships empresa"
        unique_together = ("user", "company")

    def __str__(self):
        return f"{self.user} @ {self.company.nombre}"


class Rubro(models.Model):
    nombre = models.CharField(max_length=100)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="rubros",
    )

    class Meta:
        verbose_name = "Rubro"
        verbose_name_plural = "Rubros"
        ordering = ["nombre"]
        unique_together = ("company", "nombre")

    def __str__(self):
        return self.nombre

class Unidad(models.Model):
    nombre = models.CharField(max_length=50)  # Ej: 'm2', 'kg', 'hora'
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="unidades",
    )

    class Meta:
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"
        ordering = ["nombre"]
        unique_together = ("company", "nombre")

    def __str__(self):
        return self.nombre


class Subrubro(models.Model):
    nombre = models.CharField(max_length=100)
    rubro = models.ForeignKey(Rubro, on_delete=models.CASCADE, related_name="subrubros")
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="subrubros",
    )

    class Meta:
        verbose_name = "Subrubro"
        verbose_name_plural = "Subrubros"
        ordering = ["rubro__nombre", "nombre"]
        unique_together = ("company", "rubro", "nombre")

    def __str__(self):
        return f"{self.nombre} ({self.rubro.nombre})"


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="proveedores",
    )

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["nombre"]
        unique_together = ("company", "nombre")

    def __str__(self):
        return self.nombre


class TipoMaterial(models.Model):
    nombre = models.CharField(max_length=100)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="tipos_material",
    )

    class Meta:
        verbose_name = "Tipo de Material"
        verbose_name_plural = "Tipos de Material"
        ordering = ["nombre"]
        unique_together = ("company", "nombre")

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    """Equipos de trabajo para mano de obra (ej: Equipo Naty, Equipo Diego)."""
    nombre = models.CharField(max_length=100)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="equipos",
    )

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
        ordering = ["nombre"]
        unique_together = ("company", "nombre")

    def __str__(self):
        return self.nombre


class RefEquipo(models.Model):
    """
    Referencia de equipo: subcategoría de Equipo (como Subrubro es a Rubro).
    Se indica a qué equipo pertenece.
    """
    nombre = models.CharField(max_length=100)
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="ref_equipos",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="ref_equipos",
    )

    class Meta:
        verbose_name = "Ref. Equipo"
        verbose_name_plural = "Ref. Equipos"
        ordering = ["equipo__nombre", "nombre"]
        unique_together = ("company", "equipo", "nombre")

    def __str__(self):
        return f"{self.nombre} ({self.equipo.nombre})"


class CategoriaMaterial(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoMaterial, on_delete=models.CASCADE, related_name="categorias")
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="categorias_material",
    )

    class Meta:
        verbose_name = "Categoría de Material"
        verbose_name_plural = "Categorías de Material"
        ordering = ["tipo__nombre", "nombre"]
        unique_together = ("company", "tipo", "nombre")

    def __str__(self):
        return self.nombre