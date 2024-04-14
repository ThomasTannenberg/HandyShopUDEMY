from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),

    path('warenkorb/', views.warenkorb, name='warenkorb'),

    path('kasse/', views.kasse, name='kasse'),

    path('login/', views.loginSeite, name='login'),

    path('logout/', views.logoutBenutzer, name='logout'),

    path('reg/', views.regBenutzer, name='reg'),

    # keine HTML-Seite, sondern nur eine Funktion als API für die Webseite
    # soll nicht vom user gesehen werden
    # verarbeitung als JSONs
    path('artikel_backend/', views.artikelBackend, name='artikel_backend')
]
