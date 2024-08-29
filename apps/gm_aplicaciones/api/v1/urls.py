from django.urls import path

from .views import ApplicationAPIView

urlpatterns = [
    path('aplicaciones/', ApplicationAPIView.as_view(), name='listar-crear-aplicacion'),
]
