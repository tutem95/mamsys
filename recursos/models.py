from decimal import Decimal

from django.db import models

from general.models import (
    CategoriaMaterial,
    Company,
    Equipo,
    Proveedor,
    RefEquipo,
    Rubro,
    Subrubro,
    TipoMaterial,
    Unidad,
)


class Material(models.Model):
    MONEDA_CHOICES = [
        ("ARS", "Pesos Argentinos (ARS)"),
        ("USD", "Dólares Estadounidenses (USD)"),
    ]

    nombre = models.CharField(max_length=200)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="materiales",
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materiales",
    )
    tipo = models.ForeignKey(
        TipoMaterial, on_delete=models.PROTECT, related_name="materiales"
    )
    categoria = models.ForeignKey(
        CategoriaMaterial, on_delete=models.PROTECT, related_name="materiales"
    )
    unidad_de_venta = models.ForeignKey(
        Unidad, on_delete=models.PROTECT, related_name="materiales_vendidos"
    )
    cantidad_por_unidad_venta = models.DecimalField(
        max_digits=10, decimal_places=4, default=1
    )
    precio_unidad_venta = models.DecimalField(max_digits=12, decimal_places=4)
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES, default="ARS")

    def precio_por_unidad_analisis(self):
        """
        Precio analítico (UA): cantidad por unidad de venta × precio de venta.
        """
        if (
            self.cantidad_por_unidad_venta is not None
            and self.precio_unidad_venta is not None
        ):
            return self.cantidad_por_unidad_venta * self.precio_unidad_venta
        return Decimal("0")

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ["nombre"]
        unique_together = ("company", "nombre")

    def __str__(self):
        return self.nombre

    @classmethod
    def actualizar_precios_por_porcentaje(cls, queryset, porcentaje):
        if not isinstance(porcentaje, Decimal):  # Asegúrate de que el porcentaje sea Decimal
            porcentaje = Decimal(str(porcentaje))

        factor = Decimal("1") + (porcentaje / Decimal("100"))

        # Usar F() expressions para evitar race conditions y hacer la actualización en una sola consulta SQL
        from django.db.models import F

        queryset.update(precio_unidad_venta=F("precio_unidad_venta") * factor)

        # Opcional: Podrías retornar el número de elementos actualizados
        return queryset.count()

class ManoDeObra(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="mano_de_obra",
    )
    rubro = models.ForeignKey(
        Rubro, on_delete=models.PROTECT, related_name="mano_de_obra"
    )
    subrubro = models.ForeignKey(
        Subrubro, on_delete=models.PROTECT, related_name="mano_de_obra"
    )
    tarea = models.CharField(max_length=255)
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.PROTECT,
        related_name="mano_de_obra",
    )
    ref_equipo = models.ForeignKey(
        RefEquipo,
        on_delete=models.PROTECT,
        related_name="mano_de_obra",
    )
    cantidad_por_unidad_venta = models.DecimalField(
        max_digits=10, decimal_places=4, default=1
    )
    unidad_de_venta = models.ForeignKey(
        Unidad, on_delete=models.PROTECT, related_name="mano_de_obra_unidades"
    )
    precio_unidad_venta = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        verbose_name = "Mano de Obra"
        verbose_name_plural = "Mano de Obra"
        ordering = ["rubro__nombre", "subrubro__nombre", "tarea"]
        unique_together = ("company", "rubro", "subrubro", "tarea", "equipo", "ref_equipo")

    def __str__(self):
        return f"{self.tarea} ({self.subrubro.nombre} - {self.equipo.nombre})"

    def precio_por_unidad_analisis(self):
        """UA = cantidad por unidad de venta × precio de venta."""
        if (
            self.cantidad_por_unidad_venta is not None
            and self.precio_unidad_venta is not None
        ):
            return self.cantidad_por_unidad_venta * self.precio_unidad_venta
        return Decimal("0")

    @classmethod
    def actualizar_precios_por_porcentaje(cls, queryset, porcentaje):
        if not isinstance(porcentaje, Decimal):
            porcentaje = Decimal(str(porcentaje))
        factor = Decimal("1") + (porcentaje / Decimal("100"))
        from django.db.models import F
        queryset.update(precio_unidad_venta=F("precio_unidad_venta") * factor)
        return queryset.count()

class Subcontrato(models.Model):
    MONEDA_CHOICES = [
        ("ARS", "Pesos Argentinos (ARS)"),
        ("USD", "Dólares Estadounidenses (USD)"),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="subcontratos",
    )
    rubro = models.ForeignKey(
        Rubro, on_delete=models.PROTECT, related_name="subcontratos"
    )
    subrubro = models.ForeignKey(
        Subrubro, on_delete=models.PROTECT, related_name="subcontratos"
    )
    tarea = models.CharField(max_length=255)
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcontratos",
    )
    cantidad_por_unidad_venta = models.DecimalField(
        max_digits=10, decimal_places=4, default=1
    )
    unidad_de_venta = models.ForeignKey(
        Unidad, on_delete=models.PROTECT, related_name="subcontratos_venta"
    )
    precio_unidad_venta = models.DecimalField(max_digits=12, decimal_places=4)
    moneda = models.CharField(max_length=3, choices=MONEDA_CHOICES, default="ARS")

    class Meta:
        verbose_name = "Subcontrato"
        verbose_name_plural = "Subcontratos"
        ordering = ["rubro__nombre", "subrubro__nombre", "tarea"]
        unique_together = ("company", "rubro", "subrubro", "tarea")

    def __str__(self):
        return f"{self.tarea} ({self.subrubro.nombre})"

    def precio_por_unidad_analisis(self):
        """UA = cantidad por unidad de venta × precio de venta."""
        if (
            self.cantidad_por_unidad_venta is not None
            and self.precio_unidad_venta is not None
        ):
            return self.cantidad_por_unidad_venta * self.precio_unidad_venta
        return Decimal("0")

    @classmethod
    def actualizar_precios_por_porcentaje(cls, queryset, porcentaje):
        if not isinstance(porcentaje, Decimal):
            porcentaje = Decimal(str(porcentaje))
        factor = Decimal("1") + (porcentaje / Decimal("100"))
        from django.db.models import F
        queryset.update(precio_unidad_venta=F("precio_unidad_venta") * factor)
        return queryset.count()


class HojaPrecios(models.Model):
    """
    Representa una "hoja" de precios, similar a una pestaña de Excel.
    """

    nombre = models.CharField(max_length=100)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="hojas_precios",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    origen = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="copias",
        help_text="Hoja desde la que se creó esta copia, si aplica.",
    )

    class Meta:
        verbose_name = "Hoja de Precios"
        verbose_name_plural = "Hojas de Precios"
        ordering = ["-creado_en"]
        unique_together = ("company", "nombre")

    def __str__(self):
        return self.nombre


class HojaPrecioMaterial(models.Model):
    """
    Snapshot de precios de un material en una hoja dada.
    Permite consultar precios históricos sin afectar al Material actual.
    """

    hoja = models.ForeignKey(
        HojaPrecios, on_delete=models.CASCADE, related_name="detalles"
    )
    material = models.ForeignKey(
        Material, on_delete=models.PROTECT, related_name="hojas_precios"
    )
    cantidad_por_unidad_venta = models.DecimalField(max_digits=10, decimal_places=4)
    precio_unidad_venta = models.DecimalField(max_digits=12, decimal_places=4)
    moneda = models.CharField(
        max_length=3, choices=Material.MONEDA_CHOICES, default="ARS"
    )

    class Meta:
        verbose_name = "Precio de Material en Hoja"
        verbose_name_plural = "Precios de Material en Hoja"
        ordering = ["material__nombre"]

    def __str__(self):
        return f"{self.material.nombre} @ {self.hoja.nombre}"

    def precio_por_unidad_analisis(self):
        """UA = cantidad por unidad de venta × precio de venta."""
        if (
            self.cantidad_por_unidad_venta is not None
            and self.precio_unidad_venta is not None
        ):
            return self.cantidad_por_unidad_venta * self.precio_unidad_venta
        return Decimal("0")


class Mezcla(models.Model):
    """
    Mezcla de materiales. Vinculada a una hoja de precios de materiales.
    El costo se calcula sumando (cantidad × precio) de cada material.
    """
    nombre = models.CharField(max_length=200)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="mezclas",
    )
    unidad_de_mezcla = models.ForeignKey(
        Unidad, on_delete=models.PROTECT, related_name="mezclas"
    )
    hoja = models.ForeignKey(
        HojaPrecios,
        on_delete=models.CASCADE,
        related_name="mezclas",
        null=True,
        blank=True,
        help_text="Hoja de materiales para precios. Si vacío, usa precios actuales.",
    )

    class Meta:
        verbose_name = "Mezcla"
        verbose_name_plural = "Mezclas"
        ordering = ["nombre"]
        unique_together = ("company", "nombre", "hoja")

    def __str__(self):
        hoja_nom = self.hoja.nombre if self.hoja else "Actuales"
        return f"{self.nombre} ({hoja_nom})"

    def precio_por_unidad_mezcla(self):
        """Suma de (cantidad × precio) de cada material en la mezcla."""
        total = Decimal("0")
        for det in self.detalles.select_related("material", "material__unidad_de_venta").all():
            total += det.costo_en_hoja()
        return total


class MezclaMaterial(models.Model):
    """Material que compone una mezcla, con su cantidad."""
    mezcla = models.ForeignKey(
        Mezcla, on_delete=models.CASCADE, related_name="detalles"
    )
    material = models.ForeignKey(
        Material, on_delete=models.PROTECT, related_name="mezclas"
    )
    cantidad = models.DecimalField(
        max_digits=12, decimal_places=4,
        help_text="Cantidad en unidad de venta del material (ej: bolsas, kg).",
    )

    class Meta:
        verbose_name = "Material en Mezcla"
        verbose_name_plural = "Materiales en Mezcla"
        ordering = ["material__nombre"]
        unique_together = ("mezcla", "material")

    def __str__(self):
        return f"{self.cantidad} {self.material.unidad_de_venta} de {self.material.nombre}"

    def costo_en_hoja(self):
        """Costo de este material en la mezcla según la hoja (o precios actuales)."""
        if self.mezcla.hoja:
            try:
                hp = HojaPrecioMaterial.objects.get(
                    hoja=self.mezcla.hoja, material=self.material
                )
                return self.cantidad * hp.precio_unidad_venta
            except HojaPrecioMaterial.DoesNotExist:
                return Decimal("0")
        return self.cantidad * self.material.precio_unidad_venta

    def precio_unidad_desde_hoja(self):
        """Precio unitario del material desde la hoja o actual."""
        if self.mezcla.hoja:
            try:
                hp = HojaPrecioMaterial.objects.get(
                    hoja=self.mezcla.hoja, material=self.material
                )
                return hp.precio_unidad_venta
            except HojaPrecioMaterial.DoesNotExist:
                return Decimal("0")
        return self.material.precio_unidad_venta


class HojaPreciosSubcontrato(models.Model):
    """Hoja de precios para subcontratos."""
    nombre = models.CharField(max_length=100)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="hojas_precios_subcontrato",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    origen = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="copias",
    )

    class Meta:
        verbose_name = "Hoja de Precios Subcontrato"
        verbose_name_plural = "Hojas de Precios Subcontrato"
        ordering = ["-creado_en"]
        unique_together = ("company", "nombre")

    def __str__(self):
        return self.nombre


class HojaPrecioSubcontrato(models.Model):
    """Snapshot de precios de un subcontrato en una hoja dada."""
    hoja = models.ForeignKey(
        HojaPreciosSubcontrato,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    subcontrato = models.ForeignKey(
        Subcontrato,
        on_delete=models.PROTECT,
        related_name="hojas_precios",
    )
    cantidad_por_unidad_venta = models.DecimalField(max_digits=10, decimal_places=4)
    precio_unidad_venta = models.DecimalField(max_digits=12, decimal_places=4)
    moneda = models.CharField(
        max_length=3, choices=Subcontrato.MONEDA_CHOICES, default="ARS"
    )

    class Meta:
        verbose_name = "Precio de Subcontrato en Hoja"
        verbose_name_plural = "Precios de Subcontrato en Hoja"
        ordering = ["subcontrato__rubro__nombre", "subcontrato__subrubro__nombre", "subcontrato__tarea"]

    def __str__(self):
        return f"{self.subcontrato.tarea} @ {self.hoja.nombre}"

    def precio_por_unidad_analisis(self):
        if (
            self.cantidad_por_unidad_venta is not None
            and self.precio_unidad_venta is not None
        ):
            return self.cantidad_por_unidad_venta * self.precio_unidad_venta
        return Decimal("0")


class HojaPreciosManoDeObra(models.Model):
    """Hoja de precios para mano de obra."""
    nombre = models.CharField(max_length=100)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="hojas_precios_mano_de_obra",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    origen = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="copias",
    )

    class Meta:
        verbose_name = "Hoja de Precios Mano de Obra"
        verbose_name_plural = "Hojas de Precios Mano de Obra"
        ordering = ["-creado_en"]
        unique_together = ("company", "nombre")

    def __str__(self):
        return self.nombre


class HojaPrecioManoDeObra(models.Model):
    """Snapshot de precios de mano de obra en una hoja dada."""
    hoja = models.ForeignKey(
        HojaPreciosManoDeObra,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    mano_de_obra = models.ForeignKey(
        ManoDeObra,
        on_delete=models.PROTECT,
        related_name="hojas_precios",
    )
    cantidad_por_unidad_venta = models.DecimalField(max_digits=10, decimal_places=4)
    precio_unidad_venta = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        verbose_name = "Precio de Mano de Obra en Hoja"
        verbose_name_plural = "Precios de Mano de Obra en Hoja"
        ordering = [
            "mano_de_obra__rubro__nombre",
            "mano_de_obra__subrubro__nombre",
            "mano_de_obra__tarea",
        ]

    def __str__(self):
        return f"{self.mano_de_obra.tarea} @ {self.hoja.nombre}"

    def precio_por_unidad_analisis(self):
        if (
            self.cantidad_por_unidad_venta is not None
            and self.precio_unidad_venta is not None
        ):
            return self.cantidad_por_unidad_venta * self.precio_unidad_venta
        return Decimal("0")