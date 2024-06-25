from rest_framework import serializers
from cursos.models import CategoriaCurso, SubCategoriaCurso, Curso, Plan, Venta, PlanCurso, InscripcionCurso, VentaCurso, ModuloCurso, RecursoCurso, VentaPago, RegistroLanding
from user.models import CustomUser


class CategoriaCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaCurso
        fields = ['nombre','imagen']

class SubCategoriaCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoriaCurso
        fields = '__all__'
        
class CursoSerializer(serializers.ModelSerializer):
    plan_precio = serializers.SerializerMethodField()
    categoria_curso = serializers.SerializerMethodField()

    class Meta:
        model = Curso
        fields = ['id', 'nombre', 'descripcion', 'duracion', 'imagen', 'plan_precio', 'categoria_curso','link']

    def get_plan_precio(self, obj):
        plan_curso = PlanCurso.objects.filter(curso=obj).first()
        if plan_curso:
            plan = plan_curso.plan
            return plan.precio
        return "No Plan Available"

    def get_categoria_curso(self, obj):
        subcategoria_curso = obj.subcategoria_curso
        if subcategoria_curso:
            categoria_curso = subcategoria_curso.categoria_curso
            if categoria_curso:
                return categoria_curso.nombre
        return "No Categoría Available"




class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['precio']

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class PlanCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanCurso
        fields = '__all__'

class InscripcionCursoSerializer(serializers.ModelSerializer):
    curso_nombre = serializers.SerializerMethodField()
    curso_imagen = serializers.SerializerMethodField()
    categoria_nombre = serializers.SerializerMethodField()
    subcategoria_nombre = serializers.SerializerMethodField()

    def get_curso_nombre(self, obj):
        return obj.curso.nombre

    def get_curso_imagen(self, obj):
        request = self.context.get('request')
        imagen_url = obj.curso.imagen.url if obj.curso.imagen else None
        return request.build_absolute_uri(imagen_url) if imagen_url else None

    def get_categoria_nombre(self, obj):
        return obj.curso.subcategoria_curso.categoria_curso.nombre

    def get_subcategoria_nombre(self, obj):
        return obj.curso.subcategoria_curso.nombre

    class Meta:
        model = InscripcionCurso
        fields = ['id', 'usuario', 'curso', 'curso_nombre', 'curso_imagen', 'categoria_nombre', 'subcategoria_nombre', 'fecha_registro']

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

class RegistroLandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroLanding
        fields = '__all__'


""" API PARA USUARIOS """

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username', 'first_name', 'last_name','genero', 'email', 'password','dni','celular','foto_perfil']

    def create(self, validated_data):
        # Use the `create_user` method for creating a new user which handles password hashing
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            genero=validated_data['genero'],
            email=validated_data['email'],
            password=validated_data['password'],
            dni=validated_data['dni'],
            celular=validated_data['celular'],
            foto_perfil=validated_data['foto_perfil'],
        )
        return user 