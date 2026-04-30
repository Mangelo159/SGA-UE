"""
Dominio académico: catálogos geográficos, personas y roles, periodos lectivos,
paralelos, matrículas y la oferta de materias por curso.

Flujo habitual: un Alumno tiene Matricula en un Paralelo (grado + sección en un año).
Asignatura es el catálogo (nombre/código); Materia es la oferta en un paralelo concreto.
MateriaAsignada enlaza matrícula con cada materia cursada. UnidadAcademica define
quimestres o trimestres por periodo lectivo. Calificaciones mensuales (libreta) y por
unidad se registran aparte. SesionClase y Asistencia apoyan el trabajo del docente.
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Pais(models.Model):
    """País del catálogo geográfico. Ej.: Ecuador (ISO ECU)."""

    nombre = models.CharField(max_length=120, help_text='Nombre del país, ej. Ecuador.')
    codigo_iso = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        unique=True,
        help_text='Código ISO de 3 letras, ej. ECU. Opcional.',
    )

    class Meta:
        verbose_name = 'país'
        verbose_name_plural = 'países'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class Provincia(models.Model):
    """División administrativa dentro de un país; el nombre no se repite por país. Ej.: Pichincha en Ecuador."""

    pais = models.ForeignKey(
        Pais,
        on_delete=models.CASCADE,
        related_name='provincias',
        help_text='País al que pertenece esta provincia.',
    )
    nombre = models.CharField(max_length=120, help_text='Ej. Pichincha, Guayas.')

    class Meta:
        verbose_name = 'provincia'
        verbose_name_plural = 'provincias'
        ordering = ['pais', 'nombre']
        constraints = [
            models.UniqueConstraint(fields=['pais', 'nombre'], name='uniq_provincia_nombre_por_pais'),
        ]

    def __str__(self) -> str:
        return f'{self.nombre} ({self.pais})'


class Canton(models.Model):
    """Cantón dentro de una provincia; el nombre no se repite en la misma provincia. Ej.: Quito en Pichincha."""

    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        related_name='cantones',
        help_text='Provincia a la que pertenece este cantón.',
    )
    nombre = models.CharField(max_length=120, help_text='Ej. Quito, Cuenca.')

    class Meta:
        verbose_name = 'cantón'
        verbose_name_plural = 'cantones'
        ordering = ['provincia', 'nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['provincia', 'nombre'],
                name='uniq_canton_nombre_por_provincia',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.nombre} ({self.provincia})'


class NivelEducativo(models.Model):
    """Etapa del sistema educativo para ordenar y agrupar grados. Ej.: Educación General Básica, Bachillerato."""

    nombre = models.CharField(max_length=120)
    orden = models.PositiveSmallIntegerField(
        default=0,
        help_text='Número para listar niveles en secuencia (menor = antes).',
    )

    class Meta:
        verbose_name = 'nivel educativo'
        verbose_name_plural = 'niveles educativos'
        ordering = ['orden', 'nombre']

    def __str__(self) -> str:
        return self.nombre


class Grado(models.Model):
    """Curso o año de estudio. Ej.: Décimo año, Primero de bachillerato. Puede existir sin nivel asignado."""

    nivel_educativo = models.ForeignKey(
        NivelEducativo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grados',
        help_text='Nivel al que pertenece este grado; puede quedar vacío.',
    )
    nombre = models.CharField(max_length=120, help_text='Ej. 3.º EGB, Décimo año.')
    orden = models.PositiveSmallIntegerField(
        default=0,
        help_text='Orden dentro del listado de grados.',
    )

    class Meta:
        verbose_name = 'grado'
        verbose_name_plural = 'grados'
        ordering = ['orden', 'nombre']

    def __str__(self) -> str:
        return self.nombre


class Persona(models.Model):
    """Datos de una persona física. Alumno y Profesor enlazan aquí (1:1). La cuenta Django es opcional."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='persona',
        help_text='Usuario para iniciar sesión; no toda persona tiene cuenta.',
    )
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    identificacion = models.CharField(
        max_length=32,
        unique=True,
        null=True,
        blank=True,
        help_text='Cédula u otro documento; único en el sistema si se informa.',
    )
    email = models.EmailField(blank=True, default='')
    telefono = models.CharField(max_length=32, blank=True, default='')
    canton = models.ForeignKey(
        Canton,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personas',
        help_text='Cantón de residencia o referencia; opcional.',
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'persona'
        verbose_name_plural = 'personas'
        ordering = ['apellidos', 'nombres']

    def __str__(self) -> str:
        return f'{self.apellidos}, {self.nombres}'


class Rol(models.Model):
    """Tipo de rol en la institución (catálogo). Ej.: codigo=director, nombre=Director."""

    codigo = models.SlugField(
        max_length=64,
        unique=True,
        help_text='Identificador corto sin espacios, ej. director, secretario.',
    )
    nombre = models.CharField(max_length=120, help_text='Nombre legible del rol.')

    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roles'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class PersonaRol(models.Model):
    """Asigna un rol a una persona; una sola fila por par persona+rol. Ej.: Ana Pérez es Directora desde 2024-01-01."""

    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name='persona_roles',
    )
    rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        related_name='persona_roles',
    )
    fecha_inicio = models.DateField(
        null=True,
        blank=True,
        help_text='Cuándo comenzó a tener este rol; opcional.',
    )
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        help_text='Si tiene valor, el rol ya no aplica después de esta fecha.',
    )

    class Meta:
        verbose_name = 'rol de persona'
        verbose_name_plural = 'roles de persona'
        constraints = [
            models.UniqueConstraint(
                fields=['persona', 'rol'],
                name='uniq_persona_rol',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.persona} — {self.rol}'


class Alumno(models.Model):
    """Quien estudia: una Persona con código interno de estudiante. Ej.: EST-2025-0042."""

    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name='alumno',
        help_text='Ficha de la persona que es alumno (una sola por persona).',
    )
    codigo_estudiante = models.CharField(
        max_length=32,
        unique=True,
        help_text='Código único del estudiante en la institución.',
    )

    class Meta:
        verbose_name = 'alumno'
        verbose_name_plural = 'alumnos'
        ordering = ['codigo_estudiante']

    def __str__(self) -> str:
        return f'{self.persona} ({self.codigo_estudiante})'


class Profesor(models.Model):
    """Docente: una Persona con código interno de profesor. Ej.: DOC-015."""

    persona = models.OneToOneField(
        Persona,
        on_delete=models.CASCADE,
        related_name='profesor',
        help_text='Ficha de la persona que es docente (una sola por persona).',
    )
    codigo_docente = models.CharField(
        max_length=32,
        unique=True,
        help_text='Código único del docente en la institución.',
    )

    class Meta:
        verbose_name = 'profesor'
        verbose_name_plural = 'profesores'
        ordering = ['codigo_docente']

    def __str__(self) -> str:
        return f'{self.persona} ({self.codigo_docente})'


class PeriodoLectivo(models.Model):
    """Año o ciclo lectivo con fechas. Ej.: 2025-2026 del 2025-09-01 al 2026-07-15; es_actual marca el vigente."""

    class ModoDivisionAnual(models.TextChoices):
        TRIMESTRAL = 'trimestral', 'Trimestral (3 periodos)'
        QUIMESTRAL = 'quimestral', 'Quimestral (2 periodos)'

    nombre = models.CharField(max_length=64, help_text='Ej. 2025-2026, Ciclo 1 2025.')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    es_actual = models.BooleanField(
        default=False,
        help_text='Marcar el periodo que la institución considera activo ahora.',
    )
    modo_division_anual = models.CharField(
        max_length=16,
        choices=ModoDivisionAnual.choices,
        default=ModoDivisionAnual.QUIMESTRAL,
        help_text='Cómo se divide el año para calificaciones parciales (libretas por quimestre o trimestre).',
    )

    class Meta:
        verbose_name = 'periodo lectivo'
        verbose_name_plural = 'periodos lectivos'
        ordering = ['-fecha_inicio']

    def __str__(self) -> str:
        return self.nombre


class UnidadAcademica(models.Model):
    """Quimestre, trimestre u otro bloque dentro del periodo lectivo (fechas y orden)."""

    periodo_lectivo = models.ForeignKey(
        PeriodoLectivo,
        on_delete=models.CASCADE,
        related_name='unidades_academicas',
        help_text='Año lectivo al que pertenece esta unidad.',
    )
    orden = models.PositiveSmallIntegerField(
        help_text='1 = primera unidad del año, 2 = segunda, etc.',
    )
    nombre = models.CharField(
        max_length=64,
        help_text='Ej. Primer quimestre, Segundo trimestre.',
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        verbose_name = 'unidad académica'
        verbose_name_plural = 'unidades académicas'
        ordering = ['periodo_lectivo', 'orden']
        constraints = [
            models.UniqueConstraint(
                fields=['periodo_lectivo', 'orden'],
                name='uniq_unidad_orden_por_periodo',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.nombre} ({self.periodo_lectivo})'

    def clean(self) -> None:
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha fin debe ser posterior o igual a la fecha inicio.')
        if self.periodo_lectivo_id and self.fecha_inicio and self.fecha_fin:
            pl = self.periodo_lectivo
            if self.fecha_inicio < pl.fecha_inicio or self.fecha_fin > pl.fecha_fin:
                raise ValidationError('Las fechas de la unidad deben estar dentro del periodo lectivo.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Paralelo(models.Model):
    """Grupo clase: un grado en un periodo con su sección (A, B…). Ej.: Décimo A en 2025-2026."""

    periodo_lectivo = models.ForeignKey(
        PeriodoLectivo,
        on_delete=models.CASCADE,
        related_name='paralelos',
        help_text='Año o ciclo en el que existe este grupo.',
    )
    grado = models.ForeignKey(
        Grado,
        on_delete=models.CASCADE,
        related_name='paralelos',
        help_text='Curso o año de este paralelo.',
    )
    seccion = models.CharField(
        max_length=16,
        help_text='Letra o identificador de sección, ej. A, B, 1.',
    )

    class Meta:
        verbose_name = 'paralelo'
        verbose_name_plural = 'paralelos'
        ordering = ['periodo_lectivo', 'grado', 'seccion']
        constraints = [
            models.UniqueConstraint(
                fields=['periodo_lectivo', 'grado', 'seccion'],
                name='uniq_paralelo_periodo_grado_seccion',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.grado} {self.seccion} — {self.periodo_lectivo}'


class Matricula(models.Model):
    """Inscripción de un alumno en un paralelo concreto; una matrícula por par alumno+paralelo."""

    class Estado(models.TextChoices):
        ACTIVA = 'activa', 'Activa'
        RETIRADA = 'retirada', 'Retirada'
        TRANSFERIDA = 'transferida', 'Transferida'
        FINALIZADA = 'finalizada', 'Finalizada'

    alumno = models.ForeignKey(
        Alumno,
        on_delete=models.CASCADE,
        related_name='matriculas',
        help_text='Estudiante inscrito.',
    )
    paralelo = models.ForeignKey(
        Paralelo,
        on_delete=models.CASCADE,
        related_name='matriculas',
        help_text='Grupo (grado + sección + periodo) en el que queda matriculado.',
    )
    fecha = models.DateField(help_text='Fecha de la matrícula o ingreso a ese paralelo.')
    estado = models.CharField(
        max_length=16,
        choices=Estado.choices,
        default=Estado.ACTIVA,
        help_text='Situación actual de la matrícula (activa, retirada, etc.).',
    )

    class Meta:
        verbose_name = 'matrícula'
        verbose_name_plural = 'matrículas'
        ordering = ['-fecha']
        constraints = [
            models.UniqueConstraint(
                fields=['alumno', 'paralelo'],
                name='uniq_matricula_alumno_paralelo',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.alumno} → {self.paralelo} ({self.get_estado_display()})'


class Asignatura(models.Model):
    """Catálogo institucional (sin paralelo). Ej.: Matemática con código MAT-10."""

    nombre = models.CharField(max_length=150)
    codigo = models.CharField(
        max_length=32,
        blank=True,
        default='',
        db_index=True,
        help_text='Opcional; si se informa y no está vacío, debe ser único.',
    )

    class Meta:
        verbose_name = 'asignatura'
        verbose_name_plural = 'asignaturas'
        ordering = ['nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['codigo'],
                name='uniq_asignatura_codigo_no_vacio',
                condition=~models.Q(codigo=''),
            ),
        ]

    def __str__(self) -> str:
        return self.nombre


class Materia(models.Model):
    """Oferta en un paralelo: una asignatura del catálogo dictada en ese curso-sección-año. Ej.: MAT en 10mo A (5 h/sem)."""

    asignatura = models.ForeignKey(
        Asignatura,
        on_delete=models.CASCADE,
        related_name='materias',
        help_text='Asignatura del catálogo que se ofrece en este paralelo.',
    )
    paralelo = models.ForeignKey(
        Paralelo,
        on_delete=models.CASCADE,
        related_name='materias',
        help_text='Grupo (grado + sección + periodo) donde se dicta.',
    )
    horas_semanales = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Carga horaria semanal acordada para esta oferta; opcional.',
    )

    class Meta:
        verbose_name = 'materia'
        verbose_name_plural = 'materias'
        ordering = ['paralelo', 'asignatura']
        constraints = [
            models.UniqueConstraint(
                fields=['asignatura', 'paralelo'],
                name='uniq_materia_asignatura_paralelo',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.asignatura} — {self.paralelo}'


class MateriaAsignada(models.Model):
    """Materia cursada por un estudiante en una matrícula concreta (paralelo)."""

    class Estado(models.TextChoices):
        CURSANDO = 'cursando', 'Cursando'
        CONVALIDADA = 'convalidada', 'Convalidada'
        RETIRADA = 'retirada', 'Retirada de la materia'

    matricula = models.ForeignKey(
        Matricula,
        on_delete=models.CASCADE,
        related_name='materias_asignadas',
        help_text='Matrícula del estudiante en el paralelo.',
    )
    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        related_name='materias_asignadas',
        help_text='Oferta (asignatura en ese paralelo) que cursa.',
    )
    estado = models.CharField(
        max_length=16,
        choices=Estado.choices,
        default=Estado.CURSANDO,
    )
    fecha_asignacion = models.DateField(
        auto_now_add=True,
        help_text='Fecha en que se registró la asignación.',
    )

    class Meta:
        verbose_name = 'materia asignada'
        verbose_name_plural = 'materias asignadas'
        ordering = ['matricula', 'materia']
        constraints = [
            models.UniqueConstraint(
                fields=['matricula', 'materia'],
                name='uniq_materia_asignada_matricula_materia',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.matricula.alumno} — {self.materia}'

    def clean(self) -> None:
        if self.matricula_id and self.materia_id:
            if self.matricula.paralelo_id != self.materia.paralelo_id:
                raise ValidationError(
                    'La materia ofertada debe pertenecer al mismo paralelo que la matrícula.',
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ProfesorMateria(models.Model):
    """Docente asignado a una materia (oferta en paralelo). Ej.: DOC-015 imparte MAT en 10mo A."""

    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.CASCADE,
        related_name='profesor_materias',
        help_text='Docente asignado.',
    )
    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        related_name='profesor_materias',
        help_text='Oferta concreta (asignatura + paralelo) que imparte el profesor.',
    )

    class Meta:
        verbose_name = 'profesor materia'
        verbose_name_plural = 'profesores materias'
        constraints = [
            models.UniqueConstraint(
                fields=['profesor', 'materia'],
                name='uniq_profesor_materia',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.profesor} — {self.materia}'


class SesionClase(models.Model):
    """Registro de una clase dictada (apertura/cierre) por el docente."""

    class Estado(models.TextChoices):
        PLANIFICADA = 'planificada', 'Planificada'
        ABIERTA = 'abierta', 'Abierta'
        CERRADA = 'cerrada', 'Cerrada'

    profesor_materia = models.ForeignKey(
        ProfesorMateria,
        on_delete=models.CASCADE,
        related_name='sesiones_clase',
        help_text='Docente y materia ofertada de esta clase.',
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=16,
        choices=Estado.choices,
        default=Estado.PLANIFICADA,
    )
    tema = models.CharField(max_length=200, blank=True, default='')
    observaciones = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'sesión de clase'
        verbose_name_plural = 'sesiones de clase'
        ordering = ['-fecha', '-hora_inicio']

    def __str__(self) -> str:
        return f'{self.profesor_materia} — {self.fecha}'


class Asistencia(models.Model):
    """Asistencia de un estudiante a una sesión de clase."""

    class Estado(models.TextChoices):
        PRESENTE = 'presente', 'Presente'
        AUSENTE = 'ausente', 'Ausente'
        JUSTIFICADO = 'justificado', 'Justificado'
        ATRASO = 'atraso', 'Atraso'

    sesion_clase = models.ForeignKey(
        SesionClase,
        on_delete=models.CASCADE,
        related_name='asistencias',
    )
    materia_asignada = models.ForeignKey(
        MateriaAsignada,
        on_delete=models.CASCADE,
        related_name='asistencias',
        help_text='Inscripción del estudiante en la materia (debe coincidir con el paralelo de la sesión).',
    )
    estado = models.CharField(
        max_length=16,
        choices=Estado.choices,
        default=Estado.PRESENTE,
    )
    observacion = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        verbose_name = 'asistencia'
        verbose_name_plural = 'asistencias'
        ordering = ['sesion_clase', 'materia_asignada']
        constraints = [
            models.UniqueConstraint(
                fields=['sesion_clase', 'materia_asignada'],
                name='uniq_asistencia_sesion_materia_asignada',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.materia_asignada.matricula.alumno} — {self.get_estado_display()}'

    def clean(self) -> None:
        if self.sesion_clase_id and self.materia_asignada_id:
            pm = self.sesion_clase.profesor_materia
            ma = self.materia_asignada
            if pm.materia_id != ma.materia_id:
                raise ValidationError(
                    'La materia asignada al estudiante debe ser la misma que la de la sesión.',
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CalificacionMensual(models.Model):
    """Libreta o registro mensual por estudiante y materia (independiente del quimestre/trimestre)."""

    materia_asignada = models.ForeignKey(
        MateriaAsignada,
        on_delete=models.CASCADE,
        related_name='calificaciones_mensuales',
    )
    anio = models.PositiveSmallIntegerField(help_text='Año del mes de la libreta, ej. 2025.')
    mes = models.PositiveSmallIntegerField(help_text='Mes 1–12.')
    nota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Opcional si la UE usa solo observaciones cualitativas.',
    )
    observaciones = models.TextField(
        blank=True,
        default='',
        help_text='Informe o comentario para la libreta mensual.',
    )

    class Meta:
        verbose_name = 'calificación mensual'
        verbose_name_plural = 'calificaciones mensuales'
        ordering = ['-anio', '-mes', 'materia_asignada']
        constraints = [
            models.UniqueConstraint(
                fields=['materia_asignada', 'anio', 'mes'],
                name='uniq_calif_mensual_materia_anio_mes',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.materia_asignada} — {self.anio}-{self.mes:02d}'

    def clean(self) -> None:
        if self.mes is not None and not 1 <= self.mes <= 12:
            raise ValidationError('El mes debe estar entre 1 y 12.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CalificacionUnidad(models.Model):
    """Calificación por quimestre, trimestre u otra unidad académica del periodo."""

    materia_asignada = models.ForeignKey(
        MateriaAsignada,
        on_delete=models.CASCADE,
        related_name='calificaciones_unidad',
    )
    unidad_academica = models.ForeignKey(
        UnidadAcademica,
        on_delete=models.CASCADE,
        related_name='calificaciones',
        help_text='Quimestre o trimestre al que corresponde la nota.',
    )
    nota = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    observaciones = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'calificación por unidad'
        verbose_name_plural = 'calificaciones por unidad'
        ordering = ['unidad_academica', 'materia_asignada']
        constraints = [
            models.UniqueConstraint(
                fields=['materia_asignada', 'unidad_academica'],
                name='uniq_calif_unidad_materia_unidad',
            ),
        ]

    def __str__(self) -> str:
        return f'{self.materia_asignada} — {self.unidad_academica}'

    def clean(self) -> None:
        if self.materia_asignada_id and self.unidad_academica_id:
            periodo_mat = self.materia_asignada.matricula.paralelo.periodo_lectivo_id
            if self.unidad_academica.periodo_lectivo_id != periodo_mat:
                raise ValidationError(
                    'La unidad académica debe pertenecer al mismo periodo lectivo que el paralelo de la matrícula.',
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
