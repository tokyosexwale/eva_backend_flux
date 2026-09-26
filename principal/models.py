from django.db import models


class Director(models.Model):
    id_director = models.CharField(max_length=20, primary_key=True)  # ej: dir-001
    nombre = models.CharField(max_length=150)
    pais = models.CharField(max_length=100)
    estilo = models.CharField(max_length=150)
    obra_destacada = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField()

    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directores"

    def __str__(self):
        return self.nombre