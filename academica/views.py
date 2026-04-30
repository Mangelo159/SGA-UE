from rest_framework import viewsets

from . import models, serializers


class PaisViewSet(viewsets.ModelViewSet):
    queryset = models.Pais.objects.all()
    serializer_class = serializers.PaisSerializer


class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = models.Provincia.objects.select_related('pais').all()
    serializer_class = serializers.ProvinciaSerializer


class CantonViewSet(viewsets.ModelViewSet):
    queryset = models.Canton.objects.select_related('provincia__pais').all()
    serializer_class = serializers.CantonSerializer


class NivelEducativoViewSet(viewsets.ModelViewSet):
    queryset = models.NivelEducativo.objects.all()
    serializer_class = serializers.NivelEducativoSerializer


class GradoViewSet(viewsets.ModelViewSet):
    queryset = models.Grado.objects.select_related('nivel_educativo').all()
    serializer_class = serializers.GradoSerializer


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = models.Persona.objects.select_related('canton__provincia__pais').all()
    serializer_class = serializers.PersonaSerializer


class RolViewSet(viewsets.ModelViewSet):
    queryset = models.Rol.objects.all()
    serializer_class = serializers.RolSerializer


class PersonaRolViewSet(viewsets.ModelViewSet):
    queryset = models.PersonaRol.objects.select_related('persona', 'rol').all()
    serializer_class = serializers.PersonaRolSerializer


class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = models.Alumno.objects.select_related('persona').all()
    serializer_class = serializers.AlumnoSerializer


class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = models.Profesor.objects.select_related('persona').all()
    serializer_class = serializers.ProfesorSerializer


class PeriodoLectivoViewSet(viewsets.ModelViewSet):
    queryset = models.PeriodoLectivo.objects.all()
    serializer_class = serializers.PeriodoLectivoSerializer


class ParaleloViewSet(viewsets.ModelViewSet):
    queryset = models.Paralelo.objects.select_related('periodo_lectivo', 'grado').all()
    serializer_class = serializers.ParaleloSerializer


class MatriculaViewSet(viewsets.ModelViewSet):
    queryset = models.Matricula.objects.select_related('alumno__persona', 'paralelo').all()
    serializer_class = serializers.MatriculaSerializer


class AsignaturaViewSet(viewsets.ModelViewSet):
    queryset = models.Asignatura.objects.all()
    serializer_class = serializers.AsignaturaSerializer


class MateriaViewSet(viewsets.ModelViewSet):
    queryset = models.Materia.objects.select_related('asignatura', 'paralelo').all()
    serializer_class = serializers.MateriaSerializer


class ProfesorMateriaViewSet(viewsets.ModelViewSet):
    queryset = models.ProfesorMateria.objects.select_related(
        'profesor__persona',
        'materia__asignatura',
        'materia__paralelo',
    ).all()
    serializer_class = serializers.ProfesorMateriaSerializer


class UnidadAcademicaViewSet(viewsets.ModelViewSet):
    queryset = models.UnidadAcademica.objects.select_related('periodo_lectivo').all()
    serializer_class = serializers.UnidadAcademicaSerializer


class MateriaAsignadaViewSet(viewsets.ModelViewSet):
    queryset = models.MateriaAsignada.objects.select_related(
        'matricula__alumno__persona',
        'materia__asignatura',
        'materia__paralelo',
    ).all()
    serializer_class = serializers.MateriaAsignadaSerializer


class SesionClaseViewSet(viewsets.ModelViewSet):
    queryset = models.SesionClase.objects.select_related(
        'profesor_materia__profesor__persona',
        'profesor_materia__materia__asignatura',
        'profesor_materia__materia__paralelo',
    ).all()
    serializer_class = serializers.SesionClaseSerializer


class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = models.Asistencia.objects.select_related(
        'sesion_clase',
        'materia_asignada__matricula__alumno__persona',
        'materia_asignada__materia',
    ).all()
    serializer_class = serializers.AsistenciaSerializer


class CalificacionMensualViewSet(viewsets.ModelViewSet):
    queryset = models.CalificacionMensual.objects.select_related(
        'materia_asignada__matricula__alumno__persona',
        'materia_asignada__materia__asignatura',
    ).all()
    serializer_class = serializers.CalificacionMensualSerializer


class CalificacionUnidadViewSet(viewsets.ModelViewSet):
    queryset = models.CalificacionUnidad.objects.select_related(
        'materia_asignada__matricula__alumno__persona',
        'materia_asignada__materia__asignatura',
        'unidad_academica__periodo_lectivo',
    ).all()
    serializer_class = serializers.CalificacionUnidadSerializer
