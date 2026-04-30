from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'paises', views.PaisViewSet, basename='pais')
router.register(r'provincias', views.ProvinciaViewSet, basename='provincia')
router.register(r'cantones', views.CantonViewSet, basename='canton')
router.register(r'niveles-educativos', views.NivelEducativoViewSet, basename='niveleducativo')
router.register(r'grados', views.GradoViewSet, basename='grado')
router.register(r'personas', views.PersonaViewSet, basename='persona')
router.register(r'roles', views.RolViewSet, basename='rol')
router.register(r'personas-roles', views.PersonaRolViewSet, basename='personarol')
router.register(r'alumnos', views.AlumnoViewSet, basename='alumno')
router.register(r'profesores', views.ProfesorViewSet, basename='profesor')
router.register(r'periodos-lectivos', views.PeriodoLectivoViewSet, basename='periodolectivo')
router.register(r'paralelos', views.ParaleloViewSet, basename='paralelo')
router.register(r'matriculas', views.MatriculaViewSet, basename='matricula')
router.register(r'asignaturas', views.AsignaturaViewSet, basename='asignatura')
router.register(r'materias', views.MateriaViewSet, basename='materia')
router.register(r'profesores-materias', views.ProfesorMateriaViewSet, basename='profesormateria')
router.register(r'unidades-academicas', views.UnidadAcademicaViewSet, basename='unidadacademica')
router.register(r'materias-asignadas', views.MateriaAsignadaViewSet, basename='materiaasignada')
router.register(r'sesiones-clase', views.SesionClaseViewSet, basename='sesionclase')
router.register(r'asistencias', views.AsistenciaViewSet, basename='asistencia')
router.register(
    r'calificaciones-mensuales',
    views.CalificacionMensualViewSet,
    basename='calificacionmensual',
)
router.register(
    r'calificaciones-unidad',
    views.CalificacionUnidadViewSet,
    basename='calificacionunidad',
)

urlpatterns = [
    path('', include(router.urls)),
]
