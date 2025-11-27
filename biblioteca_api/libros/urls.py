from rest_framework import routers
from django.urls import path, include
from .views import BookViewSet, PrestamosSemanaAPIView, PrestamosMultaAPIView, MesaCuentaTotalAPIView, MesasDescuentoAPIView
router = routers.DefaultRouter()
router.register(r'libros', BookViewSet, basename='libro')

urlpatterns = [
    path('', include(router.urls)),
    path('prestamos/semana', PrestamosSemanaAPIView.as_view(), name='prestamos-semana'),
    path('prestamos/multa', PrestamosMultaAPIView.as_view(), name='prestamos-multa'),
    path('cuenta', MesaCuentaTotalAPIView.as_view(), name='cuenta'),
    path('descuento', MesasDescuentoAPIView.as_view(), name='descuento' ),
]
