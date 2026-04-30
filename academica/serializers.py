from rest_framework import serializers

from . import models


class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pais
        fields = '__all__'


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provincia
        fields = '__all__'


class CantonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Canton
        fields = '__all__'


class NivelEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NivelEducativo
        fields = '__all__'


class GradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grado
        fields = '__all__'


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Persona
        fields = '__all__'


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rol
        fields = '__all__'


class PersonaRolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonaRol
        fields = '__all__'


class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Alumno
        fields = '__all__'


class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profesor
        fields = '__all__'


class PeriodoLectivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PeriodoLectivo
        fields = '__all__'


class ParaleloSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Paralelo
        fields = '__all__'


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Matricula
        fields = '__all__'


class AsignaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asignatura
        fields = '__all__'


class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Materia
        fields = '__all__'


class ProfesorMateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfesorMateria
        fields = '__all__'


class UnidadAcademicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnidadAcademica
        fields = '__all__'


class MateriaAsignadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MateriaAsignada
        fields = '__all__'


class SesionClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SesionClase
        fields = '__all__'


class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Asistencia
        fields = '__all__'


class CalificacionMensualSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalificacionMensual
        fields = '__all__'


class CalificacionUnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CalificacionUnidad
        fields = '__all__'
