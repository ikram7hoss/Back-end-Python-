# TP Python - Analyseur de notes

donnees = [
    ("Sara", "Math", 12, "G1"),
    ("Sara", "Info", 14, "G1"),
    ("Ahmed", "Math", 9, "G2"),
    ("Adam", "Chimie", 18, "G1"),
    ("Sara", "Math", 11, "G1"),
    ("Bouchra", "Info", "abc", "G2"),
    ("", "Math", 10, "G1"),
    ("Yassine", "Info", 22, "G2"),
    ("Ahmed", "Info", 13, "G2"),
    ("Adam", "Math", None, "G1"),
    ("Sara", "Chimie", 16, "G1"),
    ("Adam", "Info", 7, "G1"),
    ("Ahmed", "Math", 9, "G2"),
    ("Hana", "Physique", 15, "G3"),
    ("Hana", "Math", 8, "G3"),
]

# -------------------------
# PARTIE 1 : VALIDATION
# -------------------------

def valider(ligne):
    nom, matiere, note, groupe = ligne

    if not nom:
        return False, "nom vide"
    if not matiere:
        return False, "matiere vide"
    if not groupe:
        return False, "groupe vide"
    if note is None:
        return False, "note vide"

    try:
        note = float(note)
    except:
        return False, "note non numerique"

    if note < 0 or note > 20:
        return False, "note hors intervalle"

    return True, ""


def nettoyer(donnees):
    valides = []
    erreurs = []
    doublons = set()

    compteur = {}
    for ligne in donnees:
        compteur[ligne] = compteur.get(ligne, 0) + 1

    deja_vu = set()

    for ligne in donnees:
        if compteur[ligne] > 1 and ligne not in deja_vu:
            doublons.add(ligne)
            deja_vu.add(ligne)

        ok, raison = valider(ligne)

        if ok:
            nom, matiere, note, groupe = ligne
            valides.append((nom, matiere, float(note), groupe))
        else:
            erreurs.append((ligne, raison))

    return valides, erreurs, doublons


valides, erreurs, doublons = nettoyer(donnees)

# -------------------------
# PARTIE 2 : STRUCTURATION
# -------------------------

def organiser_par_etudiant(valides):
    notes = {}
    for nom, matiere, note, groupe in valides:
        notes.setdefault(nom, {})
        notes[nom].setdefault(matiere, [])
        notes[nom][matiere].append(note)
    return notes


def organiser_par_groupe(valides):
    groupes = {}
    for nom, matiere, note, groupe in valides:
        groupes.setdefault(groupe, set())
        groupes[groupe].add(nom)
    return groupes


notes_par_etudiant = organiser_par_etudiant(valides)
groupes = organiser_par_groupe(valides)

# -------------------------
# PARTIE 3 : MOYENNES
# -------------------------

def somme_recursive(liste, i=0):
    if i >= len(liste):
        return 0
    return liste[i] + somme_recursive(liste, i + 1)


def moyenne(liste):
    if not liste:
        return 0
    return somme_recursive(liste) / len(liste)


def calculer_moyennes(notes_par_etudiant):
    resultats = {}

    for nom, matieres in notes_par_etudiant.items():
        toutes = []
        moy_par_matiere = {}

        for matiere, notes in matieres.items():
            moy_par_matiere[matiere] = moyenne(notes)
            toutes.extend(notes)

        resultats[nom] = {
            "par_matiere": moy_par_matiere,
            "generale": moyenne(toutes)
        }

    return resultats


moyennes = calculer_moyennes(notes_par_etudiant)

# -------------------------
# PARTIE 4 : ANOMALIES
# -------------------------

SEUIL_GROUPE = 10
SEUIL_ECART = 8


def detecter_anomalies(notes_par_etudiant, groupes):
    alertes = {
        "notes_multiples": [],
        "groupes_faibles": [],
        "ecarts_importants": []
    }

    # notes multiples
    for nom, matieres in notes_par_etudiant.items():
        for matiere, notes in matieres.items():
            if len(notes) > 1:
                alertes["notes_multiples"].append((nom, matiere, notes))

    # groupes faibles
    for groupe, etudiants in groupes.items():
        toutes = []
        for nom in etudiants:
            for notes in notes_par_etudiant[nom].values():
                toutes.extend(notes)

        if moyenne(toutes) < SEUIL_GROUPE:
            alertes["groupes_faibles"].append(groupe)

    # grands ecarts
    for nom, matieres in notes_par_etudiant.items():
        toutes = []
        for notes in matieres.values():
            toutes.extend(notes)

        if len(toutes) >= 2:
            ecart = max(toutes) - min(toutes)
            if ecart >= SEUIL_ECART:
                alertes["ecarts_importants"].append((nom, ecart))

    return alertes


alertes = detecter_anomalies(notes_par_etudiant, groupes)

# -------------------------
# AFFICHAGE
# -------------------------

print("VALIDES :", valides)
print("ERREURS :", erreurs)
print("DOUBLONS :", doublons)

print("\nMOYENNES :")
for nom, infos in moyennes.items():
    print(nom, "->", round(infos["generale"], 2))

print("\nALERTES :", alertes)