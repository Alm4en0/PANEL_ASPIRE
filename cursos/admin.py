from django.contrib import admin
from django.utils.html import format_html

from .models import CategoriaCurso, SubCategoriaCurso, Curso, Plan, Venta, PlanCurso, InscripcionCurso, VentaCurso, ModuloCurso, RecursoCurso, VentaPago, RegistroLanding, VentaPaypal

class CategoriaCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'estado', 'codigo', 'imagen_categoria')
    search_fields = ('nombre', 'descripcion', 'codigo')
    list_filter = ('estado',)

    @admin.display(description='Imagen')
    def imagen_categoria(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;"/>', obj.imagen.url)
        return '-'

class SubCategoriaCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoria_curso', 'nombre', 'descripcion', 'estado', 'codigo', 'imagen_subcategoria')
    search_fields = ('nombre', 'descripcion', 'codigo')
    list_filter = ('estado',)

    @admin.display(description='Imagen')
    def imagen_subcategoria(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;"/>', obj.imagen.url)
        return '-'

class CursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'subcategoria_curso', 'codigo', 'nombre', 'descripcion', 'duracion', 'estado', 'imagen_display', 'link')
    search_fields = ('codigo', 'nombre', 'descripcion')
    list_filter = ('estado',)

    @admin.display(description='Imagen')
    def imagen_display(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;"/>', obj.imagen.url)
        return '-'

class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'estado')
    search_fields = ('nombre',)
    list_filter = ('estado',)

class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'alumno', 'fecha_venta_formatted', 'monto')
    search_fields = ('alumno__username',)
    list_filter = ('fecha_venta',)

    @admin.display(description='Fecha de Venta')
    def fecha_venta_formatted(self, obj):
        if obj.fecha_venta:
            return obj.fecha_venta.strftime("%d-%m-%Y %H:%M:%S")
        return '-'

class PlanCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'plan', 'curso')
    search_fields = ('plan__nombre', 'curso__nombre')
    list_filter = ('plan',)

class InscripcionCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'curso', 'fecha_registro_formatted')
    search_fields = ('usuario__username', 'curso__nombre')
    list_filter = ('fecha_registro',)

    @admin.display(description='Fecha de Registro')
    def fecha_registro_formatted(self, obj):
        if obj.fecha_registro:
            return obj.fecha_registro.strftime("%d-%m-%Y %H:%M:%S")
        return '-'

class VentaCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'venta', 'plan_curso', 'cantidad', 'fecha_venta_formatted')
    search_fields = ( 'curso__nombre',)
    list_filter = ('fecha_venta',)

    @admin.display(description='Fecha de Venta')
    def fecha_venta_formatted(self, obj):
        if obj.fecha_venta:
            return obj.fecha_venta.strftime("%d-%m-%Y %H:%M:%S")
        return '-'

class ModuloCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'curso', 'nombre', 'descripcion','estado', 'link', 'duracion')
    search_fields = ('curso__nombre',)
    list_filter = ('curso', 'estado',)

class RecursoCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'curso', 'descripcion', 'nombre_recurso', 'url_recurso')
    search_fields = ('curso__nombre', 'descripcion', 'nombre_recurso', 'url_recurso')
    list_filter = ('curso',)

class VentaPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'venta', 'monto', 'fecha_registro_formatted')
    search_fields = ('venta__plan__nombre',)
    list_filter = ('fecha_registro',)

    @admin.display(description='Fecha de Registro')
    def fecha_registro_formatted(self, obj):
        if obj.fecha_registro:
            return obj.fecha_registro.strftime("%d-%m-%Y %H:%M:%S")
        return '-'

class RegistroLandingAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'correo', 'celular', 'fecha_registro_formatted')
    search_fields = ('nombre','apellido', 'correo' ,'celular',)
    list_filter = ('fecha_registro',)

    @admin.display(description='Fecha de Registro')
    def fecha_registro_formatted(self, obj):
        if obj.fecha_registro:
            return obj.fecha_registro.strftime("%d-%m-%Y %H:%M:%S")
        return '-'

class VentaPaypalAdmin(admin.ModelAdmin):
    list_display = ('id', 'curso', 'usuario','monto', 'fecha_registro_formatted')
    search_fields = ('curso__nombre',)
    list_filter = ('fecha_registro',)

    @admin.display(description='Fecha de Registro')
    def fecha_registro_formatted(self, obj):
        if obj.fecha_registro:
            return obj.fecha_registro.strftime("%d-%m-%Y %H:%M:%S")
        return '-'

admin.site.register(VentaPaypal, VentaPaypalAdmin)
admin.site.register(CategoriaCurso, CategoriaCursoAdmin)
admin.site.register(SubCategoriaCurso, SubCategoriaCursoAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Venta, VentaAdmin)
admin.site.register(PlanCurso, PlanCursoAdmin)
admin.site.register(InscripcionCurso, InscripcionCursoAdmin)
admin.site.register(VentaCurso, VentaCursoAdmin)
admin.site.register(ModuloCurso, ModuloCursoAdmin)
admin.site.register(RecursoCurso, RecursoCursoAdmin)
admin.site.register(VentaPago, VentaPagoAdmin)
admin.site.register(RegistroLanding, RegistroLandingAdmin)