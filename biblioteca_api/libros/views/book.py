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


class MesaCuentaTotalAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        precios = request.data.get('precio', [])

        if not isinstance(precios, list):
            return Response({'error': 'precio debe ser un arreglo'}, status=400)

        try:
            precios = [float(p) for p in precios]
        except (TypeError, ValueError):
            return Response({'error': 'El arreglo debe contener números'}, status=400)

        total = sum(precios)

        if total == 0:
            mensaje = 'vacio'
        elif total < 20.00:
            mensaje = 'Cuenta pequeña'
        elif 20.00 <= total < 60.00:
            mensaje = 'Cuenta alta'
        else:
            mensaje = 'Cuenta muy alta'

        return Response({
            'precio': precios,
            'total': total,
            'mensaje': mensaje
        })

class MesasDescuentoAPIView(APIView):
    permission_classes=[AllowAny]
    
    def post(self, request):
        
        try: 
            total = float(request.data.get('total',0))
            porcentaje = int(request.data.get('porcentaje', 0))
        except(TypeError,ValueError):
             return Response({'detail':'Ingrese los valores correctamente'},status=status.HTTP_400_BAD_REQUEST)
        
       
        if porcentaje == 0:
            return Response({'detail':'Ingrese un numero mayor a 0'},status=status.HTTP_400_BAD_REQUEST)
        else:
            monto_descuento = total*(porcentaje/100)
            monto_condescuento = total - monto_descuento
            return Response({'total': total, 'porcentaje': porcentaje, 'Monto con descuento': monto_condescuento})
            
        
            
          
        
                    
                
                    