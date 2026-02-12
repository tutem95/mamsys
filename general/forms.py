from django import forms

from .models import CategoriaMaterial, Equipo, Proveedor, RefEquipo, Rubro, Subrubro, TipoMaterial, Unidad


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

