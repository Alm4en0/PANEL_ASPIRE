from rest_framework import serializers
from cursos.models import CategoriaCurso, SubCategoriaCurso, Curso, Plan, Venta, PlanCurso, InscripcionCurso, VentaCurso, ModuloCurso, RecursoCurso, VentaPago, RegistrosLanding
from user.models import CustomUser
class CategoriaCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaCurso
        fields = '__all__'

class SubCategoriaCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoriaCurso
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class PlanCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanCurso
        fields = '__all__'

class InscripcionCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InscripcionCurso
        fields = '__all__'

class VentaCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaCurso
        fields = '__all__'

class ModuloCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuloCurso
        fields = '__all__'

class RecursoCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecursoCurso
        fields = '__all__'

class VentaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaPago
        fields = '__all__'

class RegistrosLandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrosLanding
        fields = '__all__'


""" API PARA USUARIOS """

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password','dni','celular']

    def create(self, validated_data):
        # Use the `create_user` method for creating a new user which handles password hashing
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            dni=validated_data['dni'],
            celular=validated_data['celular'],
        )
        return user 