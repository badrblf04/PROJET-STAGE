from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
import uuid


class EmiratesTangermed(models.Model):
    HEURE_CHOICES = [
        ('08:00', '8:00 AM'),
        ('16:00', '4:00 PM'),
    ]
    date = models.DateField(default=timezone.now)
    heure_prelevement = models.CharField(max_length=5, choices=HEURE_CHOICES, blank=True)
    administration = models.IntegerField()
    cellule1 = models.FloatField()
    cellule2 = models.FloatField()
    mezannine = models.FloatField()
    tgbt = models.FloatField()
    date_and_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.heure_prelevement:
            # Si l'heure de prélèvement n'est pas définie, utilisez la logique existante
            now = timezone.now().time()
            if now < timezone.datetime.strptime('16:00', '%H:%M').time():
                self.heure_prelevement = '08:00'
            else:
                self.heure_prelevement = '16:00'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.heure_prelevement}"

    class Meta:
        verbose_name = "Emirates Tangermed"
        verbose_name_plural = "TANGER MED"

class CustomUser(AbstractUser):
    # Ré-implémentation des groupes et des permissions avec des noms uniques
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='customuser_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='customuser_permissions')

    def __str__(self):
        return self.email

class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token {self.token} for user {self.user}"

class Tac(models.Model):
    HEURE_CHOICES = [
        ('08:00', '8:00 AM'),
        
    ]
    date = models.DateField()
    heure_prelevement = models.CharField(max_length=5, choices=HEURE_CHOICES, default='08:00')
    q1_clim_hvac = models.FloatField(null=True, blank=True)
    q2_local_de_charge = models.FloatField(null=True, blank=True)
    q7_eclairage_z1 = models.FloatField(null=True, blank=True)
    q8_admin = models.FloatField(null=True, blank=True)
    q9_eclairage_z2 = models.FloatField(null=True, blank=True)
    q10_eclairage_z3 = models.FloatField(null=True, blank=True)
    tgbt = models.FloatField(null=True, blank=True)
    date_and_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.heure_prelevement:
            self.heure_prelevement = '08:00'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.heure_prelevement}"

    class Meta:
        verbose_name = "Tac"
        verbose_name_plural = "TAC"