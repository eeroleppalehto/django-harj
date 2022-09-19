from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from .models import Tapahtuma

def tapahtumalistaus(request):
    tapahtumat = Tapahtuma.objects.all()
    context = {
        'tapahtumat' : tapahtumat,
    }
    return render(request, 'listaus.html', context)
    # return HttpResponse(vastaus)

def varaa_tapahtuma(request, id):
    

    tapahtuma = Tapahtuma.objects.get(id=id)
    context = {
        'tapahtuma': tapahtuma
    }

    if request.method == "POST":
        tapahtuma.varaa(request.user)
        context["varattu"] = varattu
    else:
        varattu = tapahtuma.onko_varattu(request.user)
        context["varattu"] = False

    return render(request, "varaa.html", context)