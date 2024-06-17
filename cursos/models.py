from django.conf import settings
from django.db import models

class CategoriaCurso(models.Model):
    nombre = models.CharField(max_length=255, null=False)
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    codigo = models.CharField(max_length=50, null=False)
    imagen = models.ImageField(upload_to='categoria_img/', null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoría de Curso'
        verbose_name_plural = 'Categorías de Cursos'

class SubCategoriaCurso(models.Model):
    categoria_curso = models.ForeignKey(CategoriaCurso, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    codigo = models.CharField(max_length=50, null=False)
    imagen = models.ImageField(upload_to='subcategoria_img/', null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Subcategoría de Curso'
        verbose_name_plural = 'Subcategorías de Cursos'

class Curso(models.Model):
    subcategoria_curso = models.ForeignKey(SubCategoriaCurso, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, null=False)
    nombre = models.CharField(max_length=255, null=False)
    descripcion = models.TextField()
    duracion = models.DurationField() 
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='curso_img/', null=False)
    link = models.URLField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

class Plan(models.Model):
    nombre = models.CharField(max_length=20, null=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'

class Venta(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    alumno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_venta = models.DateTimeField()

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

class PlanCurso(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Plan del Curso'
        verbose_name_plural = 'Planes de Cursos'

class InscripcionCurso(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Inscripción al Curso'
        verbose_name_plural = 'Inscripciones a Cursos'

class VentaCurso(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_venta = models.DateTimeField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Venta del Curso'
        verbose_name_plural = 'Ventas de Cursos'

class ModuloCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    descripcion = models.TextField(null=True)
    nombre = models.CharField(max_length=150, null=False)
    estado = models.BooleanField(default=True)
    link = models.URLField()
    duracion = models.DurationField(null=True) 
    

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Módulo del Curso'
        verbose_name_plural = 'Módulos del Curso'

class RecursoCurso(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    descripcion = models.TextField()
    nombre_recurso = models.CharField(max_length=200, null=False)
    url_recurso = models.URLField()

    def __str__(self):
        return self.nombre_recurso

    class Meta:
        verbose_name = 'Recurso del Curso'
        verbose_name_plural = 'Recursos del Curso'

class VentaPago(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pago de Venta'
        verbose_name_plural = 'Pagos de Venta'

class RegistroLanding(models.Model):
    nombre = models.CharField( max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    correo = models.EmailField (null=False)
    celular = models.CharField (max_length=15, null=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Registro en Landing'
        verbose_name_plural = 'Registros en Landing'
