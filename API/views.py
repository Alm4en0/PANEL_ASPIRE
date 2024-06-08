from django.shortcuts import render

from rest_framework import generics
from cursos.models import CategoriaCurso, SubCategoriaCurso, Curso, Plan, Venta, PlanCurso, InscripcionCurso, VentaCurso, ModuloCurso, RecursoCurso, VentaPago, RegistrosLanding
from .serializers import CategoriaCursoSerializer, SubCategoriaCursoSerializer, CursoSerializer, PlanSerializer, VentaSerializer, PlanCursoSerializer, InscripcionCursoSerializer, VentaCursoSerializer, ModuloCursoSerializer, RecursoCursoSerializer, VentaPagoSerializer, RegistrosLandingSerializer,CustomUserSerializer

from user.models import CustomUser

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

class RegistrosLandingListCreate(generics.ListCreateAPIView):
    queryset = RegistrosLanding.objects.all()
    serializer_class = RegistrosLandingSerializer

class RegistrosLandingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegistrosLanding.objects.all()
    serializer_class = RegistrosLandingSerializer


""" Vistas para usuarios """


class CustomUserListCreate(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class CustomUserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
