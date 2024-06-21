from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
import json
from rest_framework import generics
from cursos.models import CategoriaCurso, SubCategoriaCurso, Curso, Plan, Venta, PlanCurso, InscripcionCurso, VentaCurso, ModuloCurso, RecursoCurso, VentaPago, RegistroLanding, VentaPaypal
from .serializers import CategoriaCursoSerializer, SubCategoriaCursoSerializer, CursoSerializer, PlanSerializer, VentaSerializer, PlanCursoSerializer, InscripcionCursoSerializer, VentaCursoSerializer, ModuloCursoSerializer, RecursoCursoSerializer, VentaPagoSerializer, RegistroLandingSerializer,CustomUserSerializer
from user.models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest

@api_view(['POST'])
def iniciar_pago_paypal(request):
    try:
        cursos = request.data.get('cursos', [])
        user_id = request.data.get('user_id')
        user = get_object_or_404(CustomUser, pk=user_id)

        venta = Venta.objects.create(alumno=user, fecha_venta=timezone.now(), monto=0)

        monto_total = 0
        for curso_data in cursos:
            plan_curso = get_object_or_404(PlanCurso, pk=curso_data['plan_curso_id'])
            cantidad = curso_data.get('cantidad', 1)
            monto_total += plan_curso.plan.precio * cantidad
            VentaCurso.objects.create(venta=venta, plan_curso=plan_curso, cantidad=cantidad, fecha_venta=venta.fecha_venta)

        venta.monto = monto_total
        venta.save()

        client_id = settings.PAYPAL_CLIENT_ID
        client_secret = settings.PAYPAL_CLIENT_SECRET
        environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
        client = PayPalHttpClient(environment)

        request = OrdersCreateRequest()
        request.prefer('return=representation')
        request.request_body({
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "USD",
                    "value": str(monto_total)
                }
            }]
        })

        response = client.execute(request)

        if response.status_code == 201:
            order_id = response.result.id
            return Response({'order_id': order_id}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No se pudo iniciar el pago con PayPal'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def confirmar_pago_paypal(request):
    try:
        order_id = request.data.get('order_id')
        venta = get_object_or_404(Venta, id=request.data.get('venta_id'))

        client_id = settings.PAYPAL_CLIENT_ID
        client_secret = settings.PAYPAL_CLIENT_SECRET
        environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
        client = PayPalHttpClient(environment)

        request = OrdersCaptureRequest(order_id)
        response = client.execute(request)

        if response.result.status == 'COMPLETED':
            venta.estado = True
            venta.save()
            VentaPago.objects.create(venta=venta, monto=venta.monto, fecha_registro=timezone.now())
            return Response({'message': 'Pago completado correctamente'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No se pudo completar el pago en PayPal'}, status=status.HTTP_400_BAD_REQUEST)

    except Venta.DoesNotExist:
        return Response({'error': 'Venta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#####
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
        return Response({"token": token.key, "username": user.username, "user": serializer.data}, status=status.HTTP_200_OK)

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

@api_view(['POST'])
def save_payment(request):
    try:
        data = request.data  # Utilizar request.data en lugar de json.loads(request.body)
        payments = data.get('payments', [])

        # Verificar si payments es una lista o un objeto individual
        if isinstance(payments, list):
            # Si es una lista de pagos
            for payment_data in payments:
                curso_id = payment_data.get('curso_id')
                usuario_id = payment_data.get('usuario_id')
                monto = float(payment_data.get('monto'))

                # Validaciones básicas
                if not curso_id or not usuario_id or not monto:
                    return JsonResponse({'error': 'Todos los campos son requeridos en cada pago.'}, status=400)

                # Obtener instancias de Curso y Usuario
                try:
                    curso = Curso.objects.get(id=curso_id)
                except Curso.DoesNotExist:
                    return JsonResponse({'error': f'Curso con id {curso_id} no encontrado.'}, status=404)

                try:
                    usuario = CustomUser.objects.get(id=usuario_id)
                except CustomUser.DoesNotExist:
                    return JsonResponse({'error': f'Usuario con id {usuario_id} no encontrado.'}, status=404)

                # Crear y guardar la nueva instancia de VentaPaypal
                VentaPaypal.objects.create(
                    curso_id=curso.id,
                    usuario_id=usuario.id,
                    monto=monto,
                )

                # También crear la inscripción al curso
                InscripcionCurso.objects.create(
                    curso_id=curso.id,
                    usuario_id=usuario.id,
                )

        elif isinstance(payments, dict):
            # Si es un solo pago (no una lista)
            curso_id = payments.get('curso_id')
            usuario_id = payments.get('usuario_id')
            monto = float(payments.get('monto'))

            # Validaciones básicas
            if not curso_id or not usuario_id or not monto:
                return JsonResponse({'error': 'Todos los campos son requeridos en cada pago.'}, status=400)

            # Obtener instancias de Curso y Usuario
            try:
                curso = Curso.objects.get(id=curso_id)
            except Curso.DoesNotExist:
                return JsonResponse({'error': f'Curso con id {curso_id} no encontrado.'}, status=404)

            try:
                usuario = CustomUser.objects.get(id=usuario_id)
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': f'Usuario con id {usuario_id} no encontrado.'}, status=404)

            # Crear y guardar la nueva instancia de VentaPaypal
            VentaPaypal.objects.create(
                curso_id=curso.id,
                usuario_id=usuario.id,
                monto=monto,
            )

            # También crear la inscripción al curso
            InscripcionCurso.objects.create(
                curso_id=curso.id,
                usuario_id=usuario.id,
            )

        else:
            return JsonResponse({'error': 'El campo payments debe ser una lista o un objeto JSON.'}, status=400)

        return JsonResponse({'message': 'Pagos guardados correctamente'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


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

class InscripcionCursoListCreate(generics.ListAPIView):
    serializer_class = InscripcionCursoSerializer
    permission_classes = [permissions.IsAuthenticated]  # Asegura que el usuario esté autenticado

    def get_queryset(self):
        user = self.request.user
        return InscripcionCurso.objects.filter(usuario=user)

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

#MOVIL
@api_view(['POST'])
def loginMovil(request):
    try:
        email = request.data['email']
        password = request.data['password']

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_401_UNAUTHORIZED)
        
        token, _ = Token.objects.get_or_create(user=user)
        serializer = CustomUserSerializer(instance=user)

        # Incluir el username en la respuesta
        return Response({"token": token.key, "username": user.username, "user": serializer.data}, status=status.HTTP_200_OK)

    except KeyError:
        return Response({"error": "Datos incompletos"}, status=status.HTTP_400_BAD_REQUEST)