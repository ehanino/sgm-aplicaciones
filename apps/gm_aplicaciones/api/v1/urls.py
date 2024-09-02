from django.urls import path

from .views import ApplicationAPIView, AuthenticacionAPIView

urlpatterns = [
    path('v1/aplicaciones/', ApplicationAPIView.as_view(), name='listar-crear-aplicacion'),
    path('v1/aplicaciones/<uuid:id>/', ApplicationAPIView.as_view(), name='detalle-actualizar-eliminar-aplicacion'),
    path('v1/aplicaciones/authentication/', AuthenticacionAPIView.as_view(), name='autenticacion-aplicacion'),
]
