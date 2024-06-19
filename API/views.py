from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json


from rest_framework import generics
from cursos.models import CategoriaCurso, SubCategoriaCurso, Curso, Plan, Venta, PlanCurso, InscripcionCurso, VentaCurso, ModuloCurso, RecursoCurso, VentaPago, RegistroLanding
from .serializers import CategoriaCursoSerializer, SubCategoriaCursoSerializer, CursoSerializer, PlanSerializer, VentaSerializer, PlanCursoSerializer, InscripcionCursoSerializer, VentaCursoSerializer, ModuloCursoSerializer, RecursoCursoSerializer, VentaPagoSerializer, RegistroLandingSerializer,CustomUserSerializer

from user.models import CustomUser

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

@api_view(['POST'])
def login(request):
    try:
        email = request.data['email']
        password = request.data['password']

        user = get_object_or_404(CustomUser, email=email)

        if not user.check_password(password):
            return Response({"error": "Contraseña inválida"}, status=status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user)
        serializer = CustomUserSerializer(instance=user)
        return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

    except KeyError:
        return Response({"error": "Datos incompletos"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        # Crear el usuario pero no guardar aún en la base de datos
        user = CustomUser(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            username=serializer.validated_data['username'],
            genero=serializer.validated_data['genero'],
            email=serializer.validated_data['email'],
            dni=serializer.validated_data.get('dni', ''),
            celular=serializer.validated_data.get('celular', '')
        )
        
        # Configurar la contraseña usando el método correcto
        user.set_password(serializer.validated_data['password'])
        
        # Guardar el usuario en la base de datos
        user.save()

        # Crear el token para el nuevo usuario
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_curso_by_nombre(request, nombre):
    try:
        curso = Curso.objects.get(nombre)
        # Obtener un diccionario de los campos del objeto de modelo
        curso_dict = curso.values()
        # Devolver la respuesta JSON
        return JsonResponse(list(curso_dict), safe=False)
    except Curso.DoesNotExist:
        return JsonResponse({'error': 'Curso no encontrado'}, status=404)


@api_view(['POST'])
def comprar_curso(request):
    serializer = VentaCursoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

""" @api_view(['POST'])
def crear_venta(request):
    plan_id = request.data.get('plan_id')
    alumno_id = request.user.id  # Obtener el ID del usuario autenticado

    plan = Plan.objects.get(id=plan_id)
    alumno = CustomUser.objects.get(id=alumno_id)

    venta = Venta.objects.create(
        plan=plan,
        alumno=alumno,
        fecha_venta=timezone.now()
    )

    return Response({'venta_id': venta.id}, status=status.HTTP_201_CREATED) 
 """
@api_view(['POST'])
def save_payment(request):
    try:
        monto = float(request.data.get('monto'))
        fecha_registro = request.data.get('fecha_registro')

        # Crear una nueva instancia de Venta
        venta = Venta.objects.create(
            monto=monto,
            fecha_registro=fecha_registro,
            # otros campos necesarios para crear una Venta
        )

        # Guardar el pago en el modelo VentaPago
        pago = VentaPago.objects.create(
            venta=venta,
            monto=monto,
            fecha_registro=fecha_registro
        )

        # Guardar los cursos asociados a la venta
        cursos = request.data.get('cursos', [])
        for curso_id in cursos:
            curso = Curso.objects.get(id=curso_id)
            VentaCurso.objects.create(
                venta=venta,
                curso=curso,
                cantidad=1,  # Ajusta la cantidad según tus necesidades
                fecha_venta=fecha_registro,
                precio=curso.subcategoria_curso.plan.precio
            )

        return Response({'message': 'Pago guardado correctamente'})

    except Exception as e:
        return Response({'error': str(e)}, status=400)

""" # Configuración de PayPal
client_id = settings.PAYPAL_CLIENT_ID
client_secret = settings.PAYPAL_CLIENT_SECRET

environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment) """

""" @api_view(['POST'])
def iniciar_pago_paypal(request):
    try:
        # Obtener el ID del plan y el ID de usuario del cuerpo de la solicitud
        plan_id = request.data['plan_id']
        user_id = request.data['user_id']

        # Obtener el plan y el usuario asociados
        plan = get_object_or_404(Plan, pk=plan_id)
        user = get_object_or_404(settings.AUTH_USER_MODEL, pk=user_id)

        # Crear un objeto de venta en tu base de datos
        venta = Venta(plan=plan, alumno=user, monto=plan.precio)
        venta.save()

        # Crear la orden de PayPal
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        request.request_body({
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": str(plan.precio)
                }
            }]
        })

        response = client.execute(request)

        # Si se creó correctamente, actualizar el objeto de venta con el ID de PayPal
        if response.status_code == 201:
            order_id = response.result.id
            venta.paypal_id = order_id
            venta.save()
            return Response({'order_id': order_id}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No se pudo iniciar el pago con PayPal'}, status=status.HTTP_400_BAD_REQUEST)

    except KeyError:
        return Response({'error': 'Datos incompletos'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirmar_pago_paypal(request):
    try:
        order_id = request.data['order_id']
        venta = get_object_or_404(Venta, paypal_id=order_id)

        # Capturar el pago en PayPal
        request = OrdersCaptureRequest(order_id)
        response = client.execute(request)

        # Verificar si se capturó correctamente el pago
        if response.result.status == 'COMPLETED':
            # Actualizar el estado de la venta u otros registros necesarios
            venta.estado = True  # Opcional: actualizar el estado de la venta
            venta.save()

            return Response({'message': 'Pago completado correctamente'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se pudo completar el pago en PayPal'}, status=status.HTTP_400_BAD_REQUEST)

    except Venta.DoesNotExist:
        return Response({'error': 'Venta no encontrada'}, status=status.HTTP_404_NOT_FOUND) """

@api_view(['GET'])
def curso_detail(request):
    try:
        cursos = Curso.objects.all()
    except Curso.DoesNotExist:
        return Response({"error": "No se encontraron cursos"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CursoSerializer(cursos, many=True)
    return Response(serializer.data)



class CategoriaCursoListCreate(generics.ListCreateAPIView):
    queryset = CategoriaCurso.objects.all()
    serializer_class = CategoriaCursoSerializer

class CategoriaCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoriaCurso.objects.all()
    serializer_class = CategoriaCursoSerializer
    

class SubCategoriaCursoListCreate(generics.ListCreateAPIView):
    queryset = SubCategoriaCurso.objects.all()
    serializer_class = SubCategoriaCursoSerializer

class SubCategoriaCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategoriaCurso.objects.all()
    serializer_class = SubCategoriaCursoSerializer

class CursoListCreate(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class CursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class PlanListCreate(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class PlanRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class VentaListCreate(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class VentaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class PlanCursoListCreate(generics.ListCreateAPIView):
    queryset = PlanCurso.objects.all()
    serializer_class = PlanCursoSerializer

class PlanCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlanCurso.objects.all()
    serializer_class = PlanCursoSerializer

class InscripcionCursoListCreate(generics.ListCreateAPIView):
    queryset = InscripcionCurso.objects.all()
    serializer_class = InscripcionCursoSerializer

class InscripcionCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = InscripcionCurso.objects.all()
    serializer_class = InscripcionCursoSerializer

class VentaCursoListCreate(generics.ListCreateAPIView):
    queryset = VentaCurso.objects.all()
    serializer_class = VentaCursoSerializer

class VentaCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = VentaCurso.objects.all()
    serializer_class = VentaCursoSerializer

class ModuloCursoListCreate(generics.ListCreateAPIView):
    queryset = ModuloCurso.objects.all()
    serializer_class = ModuloCursoSerializer

class ModuloCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ModuloCurso.objects.all()
    serializer_class = ModuloCursoSerializer

class RecursoCursoListCreate(generics.ListCreateAPIView):
    queryset = RecursoCurso.objects.all()
    serializer_class = RecursoCursoSerializer

class RecursoCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecursoCurso.objects.all()
    serializer_class = RecursoCursoSerializer

class VentaPagoListCreate(generics.ListCreateAPIView):
    queryset = VentaPago.objects.all()
    serializer_class = VentaPagoSerializer

class VentaPagoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = VentaPago.objects.all()
    serializer_class = VentaPagoSerializer

class RegistroLandingListCreate(generics.ListCreateAPIView):
    queryset = RegistroLanding.objects.all()
    serializer_class = RegistroLandingSerializer

class RegistroLandingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegistroLanding.objects.all()
    serializer_class = RegistroLandingSerializer


#Vistas para usuarios


class CustomUserListCreate(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer