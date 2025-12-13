from django.db import models

class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido1 = models.CharField(max_length=45)
    apellido2 = models.CharField(max_length=45, blank=True, null=True)
    email = models.EmailField(max_length=60, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'PROFESOR'
        verbose_name_plural = "Profesores"

    def __str__(self):
        return f"{self.nombre} {self.apellido1}"


class Asignatura(models.Model):
    id_asignatura = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'ASIGNATURA'
        verbose_name_plural = "Asignaturas"

    def __str__(self):
        return self.nombre


class Aula(models.Model):
    id_aula = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'AULA'
        verbose_name_plural = "Aulas"

    def __str__(self):
        return self.nombre


class HoraGuardia(models.Model):
    id_hora = models.AutoField(primary_key=True)
    dia = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    descripcion = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'HORA_GUARDIA'
        verbose_name_plural = "Horas de Guardia"

    def __str__(self):
        return f"{self.dia} ({self.hora_inicio} - {self.hora_fin})"


class Clase(models.Model):
    
    profesor = models.ForeignKey(
        Profesor, 
        on_delete=models.CASCADE, 
        db_column='id_profesor'
    )
    hora = models.ForeignKey(
        HoraGuardia, 
        on_delete=models.CASCADE, 
        db_column='id_hora'
    )
    aula = models.ForeignKey(
        Aula, 
        on_delete=models.CASCADE, 
        db_column='id_aula'
    )
    fecha = models.DateField(db_column='id_fecha')
    
    asignatura = models.ForeignKey(
        Asignatura, 
        on_delete=models.CASCADE, 
        db_column='id_asignatura'
    )
    falta_profe = models.BooleanField(default=False)

    class Meta:
        db_table = 'CLASE'
        verbose_name_plural = "Clases"
        unique_together = (('profesor', 'hora', 'aula', 'fecha', 'asignatura'),)

    def __str__(self):
        return f"Clase de {self.asignatura} - {self.fecha}"
