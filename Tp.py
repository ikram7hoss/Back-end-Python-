# =============================================================================
# ANALYSEUR D'INSCRIPTIONS, DE NOTES ET DE COHÉRENCE PÉDAGOGIQUE
# Université Abdelmalek Essaadi – FST Tanger
# Département Génie Informatique | Développement Web Avancé (Backend Python)
# Prof. Sara AHSAIN | 2025/2026
# =============================================================================

# ---------------------------------------------------------------------------
# DONNÉES BRUTES
# ---------------------------------------------------------------------------

donnees = [
    ("Sara",    "Math",     12,    "G1"),
    ("Sara",    "Info",     14,    "G1"),
    ("Ahmed",   "Math",     9,     "G2"),
    ("Adam",    "Chimie",   18,    "G1"),
    ("Sara",    "Math",     11,    "G1"),    # doublon partiel (même étudiant/matière, note différente)
    ("Bouchra", "Info",     "abc", "G2"),   # note non numérique
    ("",        "Math",     10,    "G1"),   # nom vide
    ("Yassine", "Info",     22,    "G2"),   # note hors plage [0,20]
    ("Ahmed",   "Info",     13,    "G2"),
    ("Adam",    "Math",     None,  "G1"),   # note None
    ("Sara",    "Chimie",   16,    "G1"),
    ("Adam",    "Info",     7,     "G1"),
    ("Ahmed",   "Math",     9,     "G2"),   # doublon exact avec ligne 3
    ("Hana",    "Physique", 15,    "G3"),
    ("Hana",    "Math",     8,     "G3"),
]

MATIERES_CONNUES = {"Math", "Info", "Chimie", "Physique"}   # référentiel pédagogique


# =============================================================================
# PARTIE 1 : NETTOYAGE ET VALIDATION
# =============================================================================

def valider(enregistrement):
    """
    Valide un enregistrement (nom, matiere, note, groupe).

    Retourne (True, "") si valide,
    sinon (False, "raison explicite").
    """
    nom, matiere, note, groupe = enregistrement

    if not isinstance(nom, str) or nom.strip() == "":
        return False, "raison : nom vide ou invalide"

    if not isinstance(matiere, str) or matiere.strip() == "":
        return False, "raison : matière vide ou invalide"

    if not isinstance(groupe, str) or groupe.strip() == "":
        return False, "raison : groupe vide ou invalide"

    if note is None:
        return False, "raison : note absente (None)"

    try:
        note_float = float(note)
    except (TypeError, ValueError):
        return False, f"raison : note non numérique ('{note}')"

    if not (0 <= note_float <= 20):
        return False, f"raison : note hors plage [0,20] (valeur={note_float})"

    return True, ""


def nettoyer_et_diviser(donnees):
    """
    Parcourt toutes les données et les répartit en :
      - valides        : liste de tuples (nom, matiere, note_float, groupe)
      - erreurs        : liste de dicts {"ligne": ..., "raison": ...}
      - doublons_exact : set des tuples bruts répétés exactement
    """
    valides = []
    erreurs = []
    doublons_exact = set()

    vus = {}  # tuple_brut -> nombre d'occurrences

    for enreg in donnees:
        vus[enreg] = vus.get(enreg, 0) + 1

    deja_signale = set()

    for enreg in donnees:
        # Détecter les doublons exacts
        if vus[enreg] > 1 and enreg not in deja_signale:
            doublons_exact.add(enreg)
            deja_signale.add(enreg)

        est_valide, raison = valider(enreg)

        if est_valide:
            nom, matiere, note, groupe = enreg
            valides.append((nom.strip(), matiere.strip(), float(note), groupe.strip()))
        else:
            erreurs.append({"ligne": enreg, "raison": raison})

    return valides, erreurs, doublons_exact


# Exécution du nettoyage
valides, erreurs, doublons_exact = nettoyer_et_diviser(donnees)


# =============================================================================
# PARTIE 2 : STRUCTURATION
# =============================================================================

def extraire_matieres(valides):
    """Retourne un set de toutes les matières distinctes présentes."""
    return {matiere for (_, matiere, _, _) in valides}


def construire_notes_par_etudiant(valides):
    """
    Retourne un dict hiérarchique :
      { nom_etudiant : { matiere : [note, ...] } }
    """
    notes = {}
    for nom, matiere, note, _ in valides:
        if nom not in notes:
            notes[nom] = {}
        if matiere not in notes[nom]:
            notes[nom][matiere] = []
        notes[nom][matiere].append(note)
    return notes


def construire_groupes(valides):
    """
    Retourne un dict :
      { groupe : set(étudiants) }
    """
    groupes = {}
    for nom, _, _, groupe in valides:
        if groupe not in groupes:
            groupes[groupe] = set()
        groupes[groupe].add(nom)
    return groupes


# Exécution de la structuration
matieres_distinctes   = extraire_matieres(valides)
notes_par_etudiant    = construire_notes_par_etudiant(valides)
groupes_etudiants     = construire_groupes(valides)


# =============================================================================
# PARTIE 3 : CALCULS ET STATISTIQUES (avec récursivité)
# =============================================================================

def somme_recursive(lst, index=0):
    """Calcule la somme d'une liste de nombres par récursivité."""
    if index >= len(lst):
        return 0
    return lst[index] + somme_recursive(lst, index + 1)


def moyenne(lst):
    """Calcule la moyenne d'une liste non vide."""
    if not lst:
        return None
    return somme_recursive(lst) / len(lst)


def calculer_moyennes(notes_par_etudiant):
    """
    Retourne un dict :
      {
        nom : {
            "par_matiere"    : { matiere : moyenne },
            "moyenne_generale": float
        }
      }
    """
    resultats = {}
    for nom, matieres in notes_par_etudiant.items():
        moy_par_matiere = {m: moyenne(notes) for m, notes in matieres.items()}
        toutes_notes = [n for notes in matieres.values() for n in notes]
        resultats[nom] = {
            "par_matiere":      moy_par_matiere,
            "moyenne_generale": moyenne(toutes_notes)
        }
    return resultats


moyennes_etudiants = calculer_moyennes(notes_par_etudiant)


# =============================================================================
# PARTIE 4 : ANALYSE AVANCÉE ET DÉTECTION D'ANOMALIES
# =============================================================================

SEUIL_MOYENNE_GROUPE = 10.0   # seuil en dessous duquel un groupe est en difficulté
SEUIL_ECART_NOTES    = 8.0    # écart min/max jugé très important

def detecter_anomalies(notes_par_etudiant, moyennes_etudiants,
                       groupes_etudiants, valides,
                       matieres_distinctes,
                       seuil_groupe=SEUIL_MOYENNE_GROUPE,
                       seuil_ecart=SEUIL_ECART_NOTES):
    """
    Détecte quatre catégories d'anomalies et les retourne dans un dict :
      {
        "notes_multiples"     : [...],
        "profils_incomplets"  : [...],
        "groupes_faibles"     : [...],
        "ecarts_importants"   : [...]
      }
    """
    alertes = {
        "notes_multiples":    [],   # 1. plusieurs notes pour une même matière
        "profils_incomplets": [],   # 2. matières manquantes
        "groupes_faibles":    [],   # 3. groupe avec moyenne < seuil
        "ecarts_importants":  []    # 4. grand écart min/max
    }

    # --- 1. Notes multiples pour une même matière -------------------------
    for nom, matieres in notes_par_etudiant.items():
        for matiere, notes in matieres.items():
            if len(notes) > 1:
                alertes["notes_multiples"].append({
                    "etudiant": nom,
                    "matiere":  matiere,
                    "notes":    notes
                })

    # --- 2. Profils incomplets (matières absentes) ------------------------
    for nom, matieres in notes_par_etudiant.items():
        matieres_manquantes = matieres_distinctes - set(matieres.keys())
        if matieres_manquantes:
            alertes["profils_incomplets"].append({
                "etudiant":           nom,
                "matieres_manquantes": matieres_manquantes
            })

    # --- 3. Groupes avec moyenne générale faible -------------------------
    for groupe, etudiants in groupes_etudiants.items():
        toutes_notes_groupe = []
        for nom in etudiants:
            for notes in notes_par_etudiant[nom].values():
                toutes_notes_groupe.extend(notes)
        moy_groupe = moyenne(toutes_notes_groupe)
        if moy_groupe is not None and moy_groupe < seuil_groupe:
            alertes["groupes_faibles"].append({
                "groupe":  groupe,
                "moyenne": round(moy_groupe, 2)
            })

    # --- 4. Écarts importants entre note min et max ----------------------
    for nom, matieres in notes_par_etudiant.items():
        toutes_notes = [n for notes in matieres.values() for n in notes]
        if len(toutes_notes) >= 2:
            ecart = max(toutes_notes) - min(toutes_notes)
            if ecart >= seuil_ecart:
                alertes["ecarts_importants"].append({
                    "etudiant": nom,
                    "note_min": min(toutes_notes),
                    "note_max": max(toutes_notes),
                    "ecart":    round(ecart, 2)
                })

    return alertes


alertes = detecter_anomalies(
    notes_par_etudiant, moyennes_etudiants,
    groupes_etudiants, valides,
    matieres_distinctes
)


# =============================================================================
# AFFICHAGE DES RÉSULTATS
# =============================================================================

SEPARATEUR = "=" * 65

def afficher_resultats():
    print(SEPARATEUR)
    print("  ANALYSEUR DE NOTES – RÉSULTATS COMPLETS")
    print(SEPARATEUR)

    # ---- Partie 1 --------------------------------------------------------
    print("\n📋 PARTIE 1 — NETTOYAGE ET VALIDATION")
    print("-" * 45)

    print(f"\n✅ Enregistrements VALIDES ({len(valides)}) :")
    for v in valides:
        print(f"   {v}")

    print(f"\n❌ Enregistrements INVALIDES ({len(erreurs)}) :")
    for e in erreurs:
        print(f"   Ligne  : {e['ligne']}")
        print(f"   {e['raison']}")

    print(f"\n🔁 Doublons EXACTS détectés ({len(doublons_exact)}) :")
    for d in doublons_exact:
        print(f"   {d}")

    # ---- Partie 2 --------------------------------------------------------
    print("\n\n🗂️  PARTIE 2 — STRUCTURATION")
    print("-" * 45)

    print(f"\n📚 Matières distinctes : {matieres_distinctes}")

    print("\n👤 Notes par étudiant (hiérarchique) :")
    for nom, matieres in notes_par_etudiant.items():
        print(f"   {nom} :")
        for matiere, notes in matieres.items():
            print(f"      {matiere} → {notes}")

    print("\n🏫 Groupes pédagogiques :")
    for groupe, etudiants in sorted(groupes_etudiants.items()):
        print(f"   {groupe} : {etudiants}")

    # ---- Partie 3 --------------------------------------------------------
    print("\n\n📊 PARTIE 3 — STATISTIQUES (somme récursive)")
    print("-" * 45)

    for nom, stats in sorted(moyennes_etudiants.items()):
        print(f"\n   {nom} — Moyenne générale : {stats['moyenne_generale']:.2f}")
        for matiere, moy in stats["par_matiere"].items():
            print(f"      {matiere} : {moy:.2f}")

    # ---- Partie 4 --------------------------------------------------------
    print("\n\n⚠️  PARTIE 4 — ANOMALIES DÉTECTÉES")
    print("-" * 45)

    print(f"\n1️⃣  Notes multiples pour une même matière ({len(alertes['notes_multiples'])}) :")
    if alertes["notes_multiples"]:
        for a in alertes["notes_multiples"]:
            print(f"   {a['etudiant']} / {a['matiere']} → notes : {a['notes']}")
    else:
        print("   Aucune.")

    print(f"\n2️⃣  Profils incomplets ({len(alertes['profils_incomplets'])}) :")
    if alertes["profils_incomplets"]:
        for a in alertes["profils_incomplets"]:
            print(f"   {a['etudiant']} manque : {a['matieres_manquantes']}")
    else:
        print("   Aucun.")

    print(f"\n3️⃣  Groupes avec moyenne < {SEUIL_MOYENNE_GROUPE} ({len(alertes['groupes_faibles'])}) :")
    if alertes["groupes_faibles"]:
        for a in alertes["groupes_faibles"]:
            print(f"   {a['groupe']} → moyenne : {a['moyenne']}")
    else:
        print("   Aucun.")

    print(f"\n4️⃣  Écarts min/max importants (≥ {SEUIL_ECART_NOTES}) ({len(alertes['ecarts_importants'])}) :")
    if alertes["ecarts_importants"]:
        for a in alertes["ecarts_importants"]:
            print(f"   {a['etudiant']} → min={a['note_min']}  max={a['note_max']}  écart={a['ecart']}")
    else:
        print("   Aucun.")

    print("\n" + SEPARATEUR)
    print("  FIN DE L'ANALYSE")
    print(SEPARATEUR)


if __name__ == "__main__":
    afficher_resultats()