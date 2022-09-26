import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings
# from django.utils.translation import gettext_lazy as gl

class Tapahtuma(models.Model):
    """
    Varattava tapahtuma.
    
    Varaus tapahtuu lisäämälllä käyttäjä "osallistujat" listaan.

    Osallistujen maksimimäärä on määritelty "paikkoja"-kentällä
    """
    
    otsikko = models.CharField(max_length=200)
    kuvaus = models.TextField(blank=True)
    alku = models.DateTimeField()
    loppu = models.DateTimeField(null=True, blank=True)
    osallistujat = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True
    )
    paikkoja = models.IntegerField()
    nakyvissa = models.BooleanField(
        default=False, 
        verbose_name="Näkyvissä"
    )


    def __str__(self):
        alku = timezone.localtime(self.alku)
        # Ternary operator:
        # A if EHTO else B
        loppu = timezone.localtime(self.loppu) if self.loppu else None
        loppu_teksti = f"{loppu:%d.%m.%Y %H:%M}" if loppu else ""
        return f"{self.otsikko} ({alku:%d.%m.%Y %H:%M} -- {loppu_teksti})"

    @property
    def kesto(self) -> "datetime.timedelta | None":
        if not self.loppu:
            return None
        return self.loppu - self.alku
    
    @property
    def kesto_tuntia(self) -> "float | None":
        kesto = self.kesto
        return self.kesto.total_seconds() / 3600 if kesto  else None

    def varaa(self, user):
        """
        Varaa tämä tapahtuma annetulle käyttäjälle

        Palauta True, jos tapahtuma saatiin varattua annetulle käyttäjälle 
        tai jos oli jo varattu annetulle käyttäjälle.
        Jos tapahtuma on täynnä eikä varaus siis onnistunut, niin palauttaa False.
        """
        if user in self.osallistujat.all():
            return True
        osallistujia = self.osallistujat.all().count()
        if osallistujia + 1 > self.paikkoja:
            return False
        self.osallistujat.add(user)
        return True
    
    def poista_varaus(self, user):
        if not self.onko_varattu(user):
            return
        self.osallistujat.remove(user)

    def onko_varattu(self, user):
        """
        Onko tapahtuma varattu annetulle käyttäjälle?
        """
        return (user in self.osallistujat.all())

    @property
    def varauksia(self):
        return self.osallistujat.count()

    @property
    def onko_tilaa(self):
        return self.varauksia < self.paikkoja
    
    