from django.db import models
# Import the User model from Django for creating relationships.
from django.contrib.auth.models import User

# The 'Kunde' model represents a customer in the system.


class Kunde(models.Model):
    # Creates a one-to-one relationship with the Django User model.
    benutzer = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        # String representation of the model, showing the customer's name.
        return self.name

# The 'Artikel' model defines an item that can be ordered.


class Artikel(models.Model):
    name = models.CharField(max_length=100)
    beschreibung = models.TextField()  # Description of the item.
    preis = models.FloatField()  # Price of the item.
    # Image of the item.
    # Media root and URL settings are required for this field.
    # Needs Pillow pip install pillow
    bild = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name  # String representation showing the item's name.

# The 'Bestellung' model represents an order placed by a customer.


class Bestellung(models.Model):
    # Link to the customer making the order.
    kunde = models.ForeignKey(
        Kunde, on_delete=models.SET_NULL, null=True, blank=True)
    # The date the order was placed.
    bestelldatum = models.DateTimeField(auto_now_add=True)
    # Indicates whether the order has been completed.
    erledigt = models.BooleanField(default=False, null=True, blank=True)
    # Typo fixed: removed '200' which seemed to be mistakenly added.
    auftrags_id = models.CharField(max_length=100, null=True)
    # Many-to-many relationship allowing multiple items to be included in a single order.
    artikel = models.ManyToManyField(Artikel)

    def __str__(self):
        return str(self.id)  # String representation showing the order ID.

    @property
    def get_gesamtpreis(self):
        return sum(artkikel.get_summe for artkikel in self.bestellteartikel_set.all())

    @property
    def get_gesamtmenge(self):
        return sum(artkikel.menge for artkikel in self.bestellteartikel_set.all())

# The 'BestellteArtikel' model connects items to orders, including quantity.


class BestellteArtikel(models.Model):
    # Link to an item.
    artikel = models.ForeignKey(
        Artikel, on_delete=models.SET_NULL, null=True, blank=True)
    # Link to an order.
    bestellung = models.ForeignKey(
        Bestellung, on_delete=models.SET_NULL, null=True, blank=True)
    # Quantity of the item ordered.
    menge = models.IntegerField(default=0, null=True, blank=True)
    # Date when the item was added to the order.
    datum = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # String representation showing the name of the ordered item.
        return self.artikel.name

    @property
    def get_summe(self):
        return self.menge * self.artikel.preis

# The 'Adresse' model stores address information for a customer or an order.


class Adresse(models.Model):
    # Link to a customer.
    kunde = models.ForeignKey(
        Kunde, on_delete=models.SET_NULL, null=True, blank=True)
    # Link to an order. Missing comma fixed.
    bestellung = models.ForeignKey(
        Bestellung, on_delete=models.SET_NULL, null=True, blank=True)
    adresse = models.CharField(max_length=100)
    plz = models.CharField(max_length=100)  # Postal code.
    stadt = models.CharField(max_length=100)  # City.
    land = models.CharField(max_length=100)  # Country.
    # Date the address was added.
    datum = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.adresse  # String representation showing the address.
