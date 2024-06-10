
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from rest_framework import generics
from cursos.models import CategoriaCurso, SubCategoriaCurso, Curso, Plan, Venta, PlanCurso, InscripcionCurso, VentaCurso, ModuloCurso, RecursoCurso, VentaPago, RegistrosLanding
from .serializers import CategoriaCursoSerializer, SubCategoriaCursoSerializer, CursoSerializer, PlanSerializer, VentaSerializer, PlanCursoSerializer, InscripcionCursoSerializer, VentaCursoSerializer, ModuloCursoSerializer, RecursoCursoSerializer, VentaPagoSerializer, RegistrosLandingSerializer,CustomUserSerializer

from user.models import CustomUser
from .permissions import IsAdminUser

@api_view(['POST'])
def login(request):

    user = get_object_or_404(CustomUser, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = CustomUserSerializer(instance=user)

    return Response({"token": token.key, "user": serializer.data }, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        # Crear el usuario pero no guardar aún en la base de datos
        user = CustomUser(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            username=serializer.validated_data['username'],
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

class CategoriaCursoListCreate(generics.ListCreateAPIView):
    queryset = CategoriaCurso.objects.all()
    serializer_class = CategoriaCursoSerializer
    permission_classes = [IsAdminUser] 

class CategoriaCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CategoriaCurso.objects.all()
    serializer_class = CategoriaCursoSerializer
    permission_classes = [IsAdminUser] 
    

class SubCategoriaCursoListCreate(generics.ListCreateAPIView):
    queryset = SubCategoriaCurso.objects.all()
    serializer_class = SubCategoriaCursoSerializer
    permission_classes = [IsAdminUser]

class SubCategoriaCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategoriaCurso.objects.all()
    serializer_class = SubCategoriaCursoSerializer
    permission_classes = [IsAdminUser] 

class CursoListCreate(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsAdminUser] 

class CursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsAdminUser] 

class PlanListCreate(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAdminUser] 

class PlanRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAdminUser] 

class VentaListCreate(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAdminUser] 

class VentaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAdminUser] 

class PlanCursoListCreate(generics.ListCreateAPIView):
    queryset = PlanCurso.objects.all()
    serializer_class = PlanCursoSerializer
    permission_classes = [IsAdminUser] 

class PlanCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlanCurso.objects.all()
    serializer_class = PlanCursoSerializer
    permission_classes = [IsAdminUser] 

class InscripcionCursoListCreate(generics.ListCreateAPIView):
    queryset = InscripcionCurso.objects.all()
    serializer_class = InscripcionCursoSerializer
    permission_classes = [IsAdminUser] 

class InscripcionCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = InscripcionCurso.objects.all()
    serializer_class = InscripcionCursoSerializer
    permission_classes = [IsAdminUser] 

class VentaCursoListCreate(generics.ListCreateAPIView):
    queryset = VentaCurso.objects.all()
    serializer_class = VentaCursoSerializer
    permission_classes = [IsAdminUser] 

class VentaCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = VentaCurso.objects.all()
    serializer_class = VentaCursoSerializer
    permission_classes = [IsAdminUser] 

class ModuloCursoListCreate(generics.ListCreateAPIView):
    queryset = ModuloCurso.objects.all()
    serializer_class = ModuloCursoSerializer
    permission_classes = [IsAdminUser] 

class ModuloCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ModuloCurso.objects.all()
    serializer_class = ModuloCursoSerializer
    permission_classes = [IsAdminUser] 

class RecursoCursoListCreate(generics.ListCreateAPIView):
    queryset = RecursoCurso.objects.all()
    serializer_class = RecursoCursoSerializer
    permission_classes = [IsAdminUser] 

class RecursoCursoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecursoCurso.objects.all()
    serializer_class = RecursoCursoSerializer
    permission_classes = [IsAdminUser] 

class VentaPagoListCreate(generics.ListCreateAPIView):
    queryset = VentaPago.objects.all()
    serializer_class = VentaPagoSerializer
    permission_classes = [IsAdminUser] 

class VentaPagoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = VentaPago.objects.all()
    serializer_class = VentaPagoSerializer
    permission_classes = [IsAdminUser] 

class RegistrosLandingListCreate(generics.ListCreateAPIView):
    queryset = RegistrosLanding.objects.all()
    serializer_class = RegistrosLandingSerializer
    permission_classes = [IsAdminUser] 

class RegistrosLandingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegistrosLanding.objects.all()
    serializer_class = RegistrosLandingSerializer
    permission_classes = [IsAdminUser] 


""" Vistas para usuarios """


class CustomUserListCreate(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser] 

class CustomUserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser] 
