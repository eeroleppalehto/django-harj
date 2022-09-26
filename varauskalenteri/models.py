import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings

class Tapahtuma(models.Model):
    """docstring for ClassName."""
    
    otsikko = models.CharField(max_length=200)
    kuvaus = models.TextField(blank=True)
    alku = models.DateTimeField()
    loppu = models.DateTimeField(null=True, blank=True)
    osallistujat = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True
    )
    paikkoja = models.IntegerField()


    def __str__(self):
        alku = timezone.localtime(self.alku)
        # Ternary operator:
        # A if EHTO else B
        loppu = timezone.localtime(self.loppu) if self.loppu else None
        loppu_teksti = f"{loppu:%d.%m.%Y %H:%M}" if loppu else ""
        return f"{self.otsikko} ({alku:%d.%m.%Y %H:%M} -- {loppu_teksti})"


    def kesto(self) -> datetime.timedelta:
        return self.loppu - self.alku
    
    def kesto_tuntia(self):
        kesto = self.kesto()
        return self.kesto().total_seconds() / 3600

    def varaa(self, user):
        if user in self.osallistujat.all():
            return True
        osallistujia = self.osallistujat.all().count()
        if osallistujia + 1 > self.paikkoja:
            return False
        self.osallistujat.add(user)
        return True
    
    def onko_varattu(self, user):
        return (user in self.osallistujat.all())