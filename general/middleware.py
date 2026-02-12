"""
Middleware multi-tenant: setea request.company desde la sesión.
El usuario debe tener membership en esa company.
Si está autenticado y no tiene company, redirige al selector (excepto en login/logout/selector).
"""
from django.shortcuts import redirect
from django.urls import resolve


def get_user_company(request):
    """Obtiene la company activa del usuario (por membership y sesión)."""
    if not request.user.is_authenticated:
        return None
    company_id = request.session.get("company_id")
    if not company_id:
        return None
    membership = request.user.company_memberships.filter(company_id=company_id).first()
    if not membership:
        return None
    return membership.company


# Rutas que no requieren company (login, selector, mensaje sin empresa, admin)
# Usar nombres sin namespace porque resolve().url_name los devuelve así
NO_COMPANY_PATHS = (
    "login",
    "logout",
    "company_select",
    "no_company",
)


class CompanyMiddleware:
    """
    Setea request.company. Si el usuario está autenticado y no tiene company,
    redirige al selector de empresa (salvo en login/logout/selector).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.company = None
        if request.user.is_authenticated:
            request.company = get_user_company(request)
            if request.company is None:
                try:
                    match = resolve(request.path_info)
                    if match.url_name not in NO_COMPANY_PATHS and not request.path.startswith("/admin/"):
                        return redirect("usuarios:company_select")
                except Exception:
                    pass
        response = self.get_response(request)
        return response
