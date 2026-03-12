from abc import ABC, abstractmethod
from dataclasses import dataclass


class Boisson(ABC):

    @abstractmethod
    def cout(self):
        pass

    @abstractmethod
    def description(self):
        pass

    # surcharge opérateur + permet de combiner deux boissons
    def __add__(self, other):

        desc = self.description() + " + " + other.description()
        prix = self.cout() + other.cout()

        # classe interne pour représenter la combinaison
        class BoissonCombinee(Boisson):

            def cout(self):
                return prix

            def description(self):
                return desc

        return BoissonCombinee()

    # petit affichage simple
    def afficher_commande(self):
        print("Commande :", self.description())
        print("Prix :", f"{self.cout():.1f}€")


# boissons de base
class Cafe(Boisson):

    def cout(self):
        return 2.0

    def description(self):
        return "Café simple"


class The(Boisson):

    def cout(self):
        return 1.5

    def description(self):
        return "Thé"



#  on ajoute des ingrédients
class DecorateurBoisson(Boisson):

    def __init__(self, boisson):
        self._boisson = boisson


class Lait(DecorateurBoisson):

    def cout(self):
        return self._boisson.cout() + 0.5

    def description(self):
        return self._boisson.description() + ", Lait"


class Sucre(DecorateurBoisson):

    def cout(self):
        return self._boisson.cout() + 0.2

    def description(self):
        return self._boisson.description() + ", Sucre"


# ingrédient ajouté 
class Caramel(DecorateurBoisson):

    def cout(self):
        return self._boisson.cout() + 0.7

    def description(self):
        return self._boisson.description() + ", Caramel"


@dataclass
class Client:
    nom: str
    numero: int
    points_fidelite: int = 0



class Commande:

    def __init__(self, client):
        self.client = client
        self.boissons = []

    def ajouter_boisson(self, boisson):
        self.boissons.append(boisson)

    # calcul du total
    def prix_total(self):
        return sum(b.cout() for b in self.boissons)

    def afficher(self):

        print("\n========================================")
        print("Commande de :", self.client.nom)
        print("========================================")

        for b in self.boissons:
            print("-", b.description(), "→", f"{b.cout():.1f}€")

        print("----------------------------------------")
        print("TOTAL :", f"{self.prix_total():.1f}€")
        print("========================================")


# commande sur place
class CommandeSurPlace(Commande):

    def afficher(self):
        print("\nCommande sur place pour", self.client.nom)
        super().afficher()


# commande à emporter
class CommandeEmporter(Commande):

    def afficher(self):
        print("\nCommande à emporter pour", self.client.nom)
        super().afficher()


# système de fidélité
class Fidelite:

    def ajouter_points(self, client, montant):

        points = int(montant)
        client.points_fidelite += points

        print(points, "points ajoutés pour", client.nom)
        print("Total points :", client.points_fidelite)


class CommandeFidele(Commande, Fidelite):

    # validation de la commande
    def valider(self):

        self.afficher()
        self.ajouter_points(self.client, self.prix_total())


# Tests
if __name__ == "__main__":

    print("==================================================")
    print("Test 1 : commande simple")
    print("==================================================")

    boisson = Cafe()
    boisson = Lait(boisson)
    boisson = Sucre(boisson)

    boisson.afficher_commande()

    print("\n==================================================")
    print("Test 2 : combinaison de boissons")
    print("==================================================")

    cafe = Cafe()
    the = The()

    menu = cafe + the

    print("Description :", menu.description())
    print("Prix total :", f"{menu.cout():.1f}€")

    print("\n==================================================")
    print("Test 3 : système complet")
    print("==================================================")

    # création client
    ikram = Client("Ikram", 42)

    # boissons commandées
    b1 = Caramel(Lait(Cafe()))
    b2 = Sucre(The())

    # commande avec fidélité
    commande = CommandeFidele(ikram)

    commande.ajouter_boisson(b1)
    commande.ajouter_boisson(b2)

    commande.valider()

    print("Points de fidélité de Ikram :", ikram.points_fidelite)