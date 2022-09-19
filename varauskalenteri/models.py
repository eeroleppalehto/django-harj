from django.db import models

class Tapahtuma(models.Model):
    """docstring for ClassName."""
    
    otsikko = models.CharField(max_length=200)
    kuvaus = models.TextField()
    alku = models.DateTimeField()
    loppu = models.DateTimeField()


    def kesto(self):
        return self.loppu - self.alku

    