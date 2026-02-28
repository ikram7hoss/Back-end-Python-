#Exercice 1

age = int (input("votre Age : "))
if age <= 12:
    print("vous etes mineur -Enfant-")
elif age <= 17:
    print("vous etes mineur -Adolescent-")
elif age <= 64:
    print("vous etes majeur -Adult-")
else:
    print("vous etes Senior -Senior-")

 #Exercice 2

 contacts = []

while True:
    print("\n1. Ajouter")
    print("2. Afficher")
    print("3. Quitter")

    choix = input("Votre choix : ")

    if choix == "1":
        nom = input("Nom : ")
        contacts.append(nom)
        print("Contact ajouté !")

    elif choix == "2":
        for index, contact in enumerate(contacts, start=1):
            print(index, contact)

    elif choix == "3":
        break

    #Exercice 3

    mot_de_passe = "python123"

while True:
    saisie = input("Entrez le mot de passe : ")
    
    if saisie == mot_de_passe:
        print("Accès autorisé !")
        break
    else:
        print("Mot de passe incorrect, réessayez.")
```
#Exercice 4

a = float(input("Entrez le premier nombre : "))
b = float(input("Entrez le deuxième nombre : "))

print("1. Addition")
print("2. Soustraction")
print("3. Multiplication")
print("4. Division")

choix = input("Votre choix : ")

if choix == "1":
    print("Résultat :", a + b)

elif choix == "2":
    print("Résultat :", a - b)

elif choix == "3":
    print("Résultat :", a * b)

elif choix == "4":
    if b == 0:
        print("Erreur : division par zéro impossible !")
    else:
        print("Résultat :", a / b)

else:
    print("Choix invalide.")
```