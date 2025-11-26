from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..models import Book
from ..serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
	"""CRUD completo para libros."""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [AllowAny]
	filterset_fields = ['autor', 'categoria', 'editorial']
	search_fields = ['titulo', 'autor', 'isbn']
	ordering_fields = ['anio_publicacion', 'titulo']


class PrestamosSemanaAPIView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		prestamos = request.data.get('prestamosPorDia')
		if not isinstance(prestamos, list) or len(prestamos) != 7:
			return Response({'detail': 'prestamosPorDia debe ser un arreglo de 7 números.'}, status=status.HTTP_400_BAD_REQUEST)
		try:
			numeros = [float(x) for x in prestamos]
		except (TypeError, ValueError):
			return Response({'detail': 'Todos los elementos de prestamosPorDia deben ser números.'}, status=status.HTTP_400_BAD_REQUEST)

		total = sum(numeros)
		promedio = total / 7
		if total < 10:
			mensaje = "Poca actividad de préstamo"
		elif total <= 30:
			mensaje = "Actividad normal"
		else:
			mensaje = "Alta demanda de libros"

		return Response({'totalPrestamos': total, 'promedioDiario': promedio, 'mensaje': mensaje})


class PrestamosMultaAPIView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		try:
			dias = float(request.data.get('diasRetraso', 0))
			multa_por_dia = float(request.data.get('multaPorDia', 0))
		except (TypeError, ValueError):
			return Response({'detail': 'diasRetraso y multaPorDia deben ser números.'}, status=status.HTTP_400_BAD_REQUEST)

		if dias <= 0:
			multa = 0
			mensaje = "Sin retraso"
		else:
			multa = dias * multa_por_dia
			if multa <= 5:
				mensaje = "Retraso leve"
			elif multa <= 15:
				mensaje = "Retraso moderado"
			else:
				mensaje = "Retraso grave, revisar con administración"

		return Response({'diasRetraso': dias, 'multa': multa, 'mensaje': mensaje})
