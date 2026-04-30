# Generated manually for schema: Asignatura=catálogo, Materia=oferta por paralelo.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Canton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
            ],
            options={
                'verbose_name': 'cantón',
                'verbose_name_plural': 'cantones',
                'ordering': ['provincia', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='NivelEducativo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('orden', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'nivel educativo',
                'verbose_name_plural': 'niveles educativos',
                'ordering': ['orden', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('codigo_iso', models.CharField(blank=True, max_length=3, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'país',
                'verbose_name_plural': 'países',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='PeriodoLectivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('es_actual', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'periodo lectivo',
                'verbose_name_plural': 'periodos lectivos',
                'ordering': ['-fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.SlugField(max_length=64, unique=True)),
                ('nombre', models.CharField(max_length=120)),
            ],
            options={
                'verbose_name': 'rol',
                'verbose_name_plural': 'roles',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('codigo', models.CharField(blank=True, db_index=True, default='', max_length=32)),
            ],
            options={
                'verbose_name': 'asignatura',
                'verbose_name_plural': 'asignaturas',
                'ordering': ['nombre'],
                'constraints': [
                    models.UniqueConstraint(
                        condition=models.Q(('codigo', ''), _negated=True),
                        fields=('codigo',),
                        name='uniq_asignatura_codigo_no_vacio',
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name='Grado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('orden', models.PositiveSmallIntegerField(default=0)),
                ('nivel_educativo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='grados', to='academica.niveleducativo')),
            ],
            options={
                'verbose_name': 'grado',
                'verbose_name_plural': 'grados',
                'ordering': ['orden', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='Paralelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seccion', models.CharField(max_length=16)),
                ('grado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paralelos', to='academica.grado')),
                ('periodo_lectivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paralelos', to='academica.periodolectivo')),
            ],
            options={
                'verbose_name': 'paralelo',
                'verbose_name_plural': 'paralelos',
                'ordering': ['periodo_lectivo', 'grado', 'seccion'],
            },
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horas_semanales', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materias', to='academica.asignatura')),
                ('paralelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materias', to='academica.paralelo')),
            ],
            options={
                'verbose_name': 'materia',
                'verbose_name_plural': 'materias',
                'ordering': ['paralelo', 'asignatura'],
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=150)),
                ('apellidos', models.CharField(max_length=150)),
                ('identificacion', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('telefono', models.CharField(blank=True, default='', max_length=32)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('canton', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='personas', to='academica.canton')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='persona', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'persona',
                'verbose_name_plural': 'personas',
                'ordering': ['apellidos', 'nombres'],
            },
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_estudiante', models.CharField(max_length=32, unique=True)),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='alumno', to='academica.persona')),
            ],
            options={
                'verbose_name': 'alumno',
                'verbose_name_plural': 'alumnos',
                'ordering': ['codigo_estudiante'],
            },
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_docente', models.CharField(max_length=32, unique=True)),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profesor', to='academica.persona')),
            ],
            options={
                'verbose_name': 'profesor',
                'verbose_name_plural': 'profesores',
                'ordering': ['codigo_docente'],
            },
        ),
        migrations.CreateModel(
            name='ProfesorMateria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profesor_materias', to='academica.materia')),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profesor_materias', to='academica.profesor')),
            ],
            options={
                'verbose_name': 'profesor materia',
                'verbose_name_plural': 'profesores materias',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provincias', to='academica.pais')),
            ],
            options={
                'verbose_name': 'provincia',
                'verbose_name_plural': 'provincias',
                'ordering': ['pais', 'nombre'],
            },
        ),
        migrations.AddField(
            model_name='canton',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cantones', to='academica.provincia'),
        ),
        migrations.CreateModel(
            name='PersonaRol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField(blank=True, null=True)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persona_roles', to='academica.persona')),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persona_roles', to='academica.rol')),
            ],
            options={
                'verbose_name': 'rol de persona',
                'verbose_name_plural': 'roles de persona',
            },
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('estado', models.CharField(choices=[('activa', 'Activa'), ('retirada', 'Retirada'), ('transferida', 'Transferida'), ('finalizada', 'Finalizada')], default='activa', max_length=16)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matriculas', to='academica.alumno')),
                ('paralelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matriculas', to='academica.paralelo')),
            ],
            options={
                'verbose_name': 'matrícula',
                'verbose_name_plural': 'matrículas',
                'ordering': ['-fecha'],
                'constraints': [models.UniqueConstraint(fields=('alumno', 'paralelo'), name='uniq_matricula_alumno_paralelo')],
            },
        ),
        migrations.AddConstraint(
            model_name='materia',
            constraint=models.UniqueConstraint(fields=('asignatura', 'paralelo'), name='uniq_materia_asignatura_paralelo'),
        ),
        migrations.AddConstraint(
            model_name='paralelo',
            constraint=models.UniqueConstraint(fields=('periodo_lectivo', 'grado', 'seccion'), name='uniq_paralelo_periodo_grado_seccion'),
        ),
        migrations.AddConstraint(
            model_name='profesormateria',
            constraint=models.UniqueConstraint(fields=('profesor', 'materia'), name='uniq_profesor_materia'),
        ),
        migrations.AddConstraint(
            model_name='provincia',
            constraint=models.UniqueConstraint(fields=('pais', 'nombre'), name='uniq_provincia_nombre_por_pais'),
        ),
        migrations.AddConstraint(
            model_name='canton',
            constraint=models.UniqueConstraint(fields=('provincia', 'nombre'), name='uniq_canton_nombre_por_provincia'),
        ),
        migrations.AddConstraint(
            model_name='personarol',
            constraint=models.UniqueConstraint(fields=('persona', 'rol'), name='uniq_persona_rol'),
        ),
    ]
