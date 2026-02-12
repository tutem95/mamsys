from django import forms

from .models import (
    CategoriaMaterial,
    CotizacionDolar,
    Equipo,
    Obra,
    Proveedor,
    RefEquipo,
    Rubro,
    Subrubro,
    TipoDolar,
    TipoMaterial,
    Unidad,
)


class RubroForm(forms.ModelForm):
    class Meta:
        model = Rubro
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "input",
                    "placeholder": "Ej: Obra gruesa",
                    "autocomplete": "off",
                }
            )
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request


class UnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ["nombre"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ej: m2, kg, hora",
                    "autocomplete": "off",
                }
            )
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request


class TipoMaterialForm(forms.ModelForm):
    class Meta:
        model = TipoMaterial
        fields = ["nombre"]

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ["nombre"]

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request


class CategoriaMaterialForm(forms.ModelForm):
    class Meta:
        model = CategoriaMaterial
        fields = ["tipo", "nombre"]

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request
        if request and request.company:
            self.fields["tipo"].queryset = TipoMaterial.objects.filter(company=request.company)


class SubrubroForm(forms.ModelForm):
    class Meta:
        model = Subrubro
        fields = ["rubro", "nombre"]

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request
        if request and request.company:
            self.fields["rubro"].queryset = Rubro.objects.filter(company=request.company)


class RefEquipoForm(forms.ModelForm):
    class Meta:
        model = RefEquipo
        fields = ["equipo", "nombre"]

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request
        if request and request.company:
            self.fields["equipo"].queryset = Equipo.objects.filter(company=request.company)


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ["nombre", "direccion", "telefono", "email"]

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request


class TipoDolarForm(forms.ModelForm):
    class Meta:
        model = TipoDolar
        fields = ["nombre"]

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request


class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ["nombre", "direccion", "pisos", "m2_construibles", "m2_vendibles", "valor_terreno"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ej: Edificio Centro"}),
            "direccion": forms.TextInput(attrs={"placeholder": "Calle, número, ciudad"}),
            "pisos": forms.TextInput(attrs={"placeholder": "Ej: PB + 2 pisos"}),
            "m2_construibles": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "m2_vendibles": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "valor_terreno": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request
        self.fields["direccion"].required = False
        self.fields["pisos"].required = False
        self.fields["m2_construibles"].required = False
        self.fields["m2_vendibles"].required = False
        self.fields["valor_terreno"].required = False

