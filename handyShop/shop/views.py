from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm  # , AuthenticationForm
from . forms import EigeneUserCreationForm

# Create your views here.


def shop(request):
    artikels = Artikel.objects.all()
    ctx = {'artikels': artikels}
    return render(request, 'shop/shop.html', ctx)


def warenkorb(request):
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung, created = Bestellung.objects.get_or_create(
            kunde=kunde, erledigt=False)
        artikels = bestellung.bestellteartikel_set.all()
    else:
        artikels = []
        bestellung = []

    ctx = {"artikels": artikels, "bestellung": bestellung}
    return render(request, 'shop/warenkorb.html', ctx)


def kasse(request):
    if request.user.is_authenticated:
        kunde = request.user.kunde
        bestellung, created = Bestellung.objects.get_or_create(
            kunde=kunde, erledigt=False)
        artikels = bestellung.bestellteartikel_set.all()
    else:
        artikels = []
        bestellung = []

    ctx = {"artikels": artikels, "bestellung": bestellung}
    return render(request, 'shop/kasse.html', ctx)


def artikelBackend(request):
    daten = json.loads(request.body)
    artikelID = daten['artikelID']
    action = daten['action']
    kunde = request.user.kunde
    artikel = Artikel.objects.get(id=artikelID)
    bestellung, created = Bestellung.objects.get_or_create(
        kunde=kunde, erledigt=False)
    bestellteArtikel, created = BestellteArtikel.objects.get_or_create(
        bestellung=bestellung, artikel=artikel)

    if action == 'bestellen':
        bestellteArtikel.menge = (bestellteArtikel.menge + 1)
        messages.info(request, "Artikel hinzugefügt")
    elif action == 'entfernen':
        bestellteArtikel.menge = 0
        messages.info(request, "Artikel komplett entfernt")
    elif action == 'minus':
        bestellteArtikel.menge = (bestellteArtikel.menge - 1)
        messages.info(request, "Artikel entfernt")

    bestellteArtikel.save()

    if bestellteArtikel.menge <= 0:
        bestellteArtikel.delete()

    return JsonResponse("Artikel hinzugefügt", safe=False)


def loginSeite(request):
    seite = 'login'
    if request.method == 'POST':
        benutzername = request.POST['benutzername']
        passwort = request.POST['passwort']

        benutzer = authenticate(
            request, username=benutzername, password=passwort)

        if benutzer is not None:
            login(request, benutzer)
            return redirect('shop')
        else:
            messages.error(
                request, "Benutzername oder Passwort nicht korrekt.")

    return render(request, 'shop/login.html', {'seite': seite})


def logoutBenutzer(request):
    logout(request)
    return redirect('shop')


def regBenutzer(request):
    seite = 'reg'
    form = EigeneUserCreationForm

    if request.method == 'POST':
        form = EigeneUserCreationForm(request.POST)
        if form.is_valid():
            benutzer = form.save(commit=False)
            benutzer.save()

            kunde = Kunde(name=request.POST['username'], benutzer=benutzer)
            kunde.save()
            bestellung = Bestellung(kunde=kunde)
            bestellung.save()

            login(request, benutzer)
            return redirect('shop')
        else:
            messages.error(request, "Fehlerhafte Eingabe!")

    ctx = {'form': form, 'seite': seite}
    return render(request, 'shop/login.html', ctx)
