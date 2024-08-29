import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class BasicData(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    creator_user = models.UUIDField()

    class Meta:
        abstract = True

class Aplicacion(BasicData):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app_name = models.CharField(_("Nombre de la App"), max_length=100, unique=True)
    description = models.TextField(_("Descripción"), max_length=500)
    abbreviation = models.CharField(_("Nombre Comercial de la App"), max_length=20, unique=True)

    class Meta:
        verbose_name = _("Aplicación")
        verbose_name_plural = _("Aplicaciones")
        ordering = ['-created']

    def clean(self):
        if self.app_name and self.abbreviation:
            if Aplicacion.objects.filter(app_name__iexact=self.app_name).exclude(pk=self.pk).exists():
                raise ValidationError(_('Ya existe una aplicación con este nombre.'))
            if Aplicacion.objects.filter(abbreviation__iexact=self.abbreviation).exclude(pk=self.pk).exists():
                raise ValidationError(_('Ya existe una aplicación con esta abreviación.'))

    def save(self, *args, **kwargs):
        self.app_name = self.app_name.strip().upper()
        self.description = self.description.strip().upper()
        self.abbreviation = self.abbreviation.strip().upper()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.app_name