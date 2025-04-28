from math import degrees
# Commentaire pas utile mais moi besoin
def DSATUR(graphe):
    # On initialise un tableau clé-valeur qui représente le couple sommet-degré ; le nombre de voisins
    # que possède un sommet
    degree = {
        sommet: len(voisins)
        for sommet, voisins in graphe.items()
    }

    # On initialise un tableau clé-valeur qui représente le couple sommet-couleur
    couleurs = {
        sommet: None
        for sommet in graphe
    }

    # Ensemble des sommets non coloriés
    sommets_non_colories = set(graphe.keys())

    # On choisit le sommet avec le plus haut degré et on le colorie
    premier_sommet = max(degree, key=degree.get)

    # On lui attribue une couleur : 1
    couleurs[premier_sommet] = 1

    # On l'enlève ensuite de la liste des sommets non coloriés
    sommets_non_colories.remove(premier_sommet)

    # On initialise un tableau clé-valeur qui représente le couple sommet-saturation
    saturation = {
        sommet: 0
        for sommet in graphe
    }

    # On augmente la saturation de tous les voisins du premier sommet
    for voisin in graphe[premier_sommet]:
        if couleurs[voisin] is None:
            saturation[voisin] += 1

    # Tant que tous les sommets n'ont pas été coloriés
    while sommets_non_colories:
        # On va chercher le sommet avec le plus haut degré de saturation, au début il est à -1
        saturation_maximum = -1

        # Stockage des sommets qui ont le même plus haut degré de saturation
        candidats = []

        # On parcourt tous les sommets non coloriés
        for sommet in sommets_non_colories:
            # S'il possède une saturation plus élevée que celle actuelle, on l'actualise
            if saturation[sommet] > saturation_maximum:
                saturation_maximum = saturation[sommet]
                candidats = [sommet]
            # Si elle est égale, on l'ajoute dans la liste des potentiels candidats
            elif saturation[sommet] == saturation_maximum:
                candidats.append(sommet)

        # Il faut ensuite résoudre l'égalité, on va choisir le sommet avec le degré le plus élevé
        if len(candidats) > 1:
            sommet_choisi = max(candidats, key=lambda sommet: degree[sommet])
        else:
            # Si la liste ne comporte qu'un élément, on le choisit
            sommet_choisi = candidats[0]

        # On récupère la liste des couleurs des voisins du sommet qui a été choisi
        couleurs_voisins = set(couleurs[voisin]
                               for voisin in graphe[sommet_choisi]
                               if couleurs[voisin] is not None)


        # On trouve la première couleur disponible qui n'est pas utilisée par les voisins
        couleur = 1
        while couleur in couleurs_voisins:
            couleur += 1

        # On attribue cette couleur au sommet choisi
        couleurs[sommet_choisi] = couleur

        # On enlève le sommet choisi de la liste des sommets non coloriés
        sommets_non_colories.remove(sommet_choisi)

        # On met à jour la saturation de tous les voisins non coloriés du sommet choisi
        for voisin in graphe[sommet_choisi]:
            if couleurs[voisin] is None:
                # Compte les couleurs uniques parmi les voisins coloriés
                couleurs_uniques = set(couleurs[n]
                                       for n in graphe[voisin]
                                       if couleurs[n] is not None)

                # Met à jour la saturation du voisin
                saturation[voisin] = len(couleurs_uniques)

    # Retourne le tableau clé-valeur des couleurs attribuées à chaque sommet
    return couleurs

def dsatur_par_tons(graphe, b):
    # Initialisation des degrés
    degree = {
        sommet: len(voisins)
        for sommet, voisins in graphe.items()
    }

    # Initialisation des ensembles de couleurs attribuées aux sommets
    couleurs = {
        sommet: set()
        for sommet in graphe
    }

    # Ensemble des sommets non coloriés
    sommets_non_colories = set(graphe.keys())

    # Choix du sommet ayant le plus haut degré
    premier_sommet = max(degree, key=degree.get)

    # On lui assigne les b premières couleurs : {1, 2, ..., b}
    couleurs[premier_sommet] = set(range(1, b + 1))

    # On enlève le sommet choisi
    sommets_non_colories.remove(premier_sommet)

    # Initialisation des saturations
    saturation = {
        sommet: 0
        for sommet in graphe
    }

    # On met à jour la saturation des voisins du premier sommet
    for voisin in graphe[premier_sommet]:
        if not couleurs[voisin]:
            couleurs_utilisees = set()
            for n in graphe[voisin]:
                couleurs_utilisees.update(couleurs[n])
            saturation[voisin] = len(couleurs_utilisees)

    # Initialisation du nombre total de couleurs utilisées
    a = b

    # Tant que tous les sommets n'ont pas été coloriés
    while sommets_non_colories:
        # On va chercher le sommet avec le plus haut degré de saturation, au début il est à -1
        saturation_max = -1
        candidats = []
        for sommet in sommets_non_colories:
            if saturation[sommet] > saturation_max:
                saturation_max = saturation[sommet]
                candidats = [sommet]
            elif saturation[sommet] == saturation_max:
                candidats.append(sommet)

        # S'il y a égalité, on choisit celui avec le plus haut degré
        if len(candidats) > 1:
            sommet_choisi = max(candidats, key=lambda s: degree[s])
        else:
            sommet_choisi = candidats[0]

        # On récupère les couleurs déjà utilisées par les voisins
        couleurs_interdites = set()
        for voisin in graphe[sommet_choisi]:
            couleurs_interdites.update(couleurs[voisin])

        # On cherche un ensemble de b couleurs disjoint de couleurs_interdites
        couleur_courante = 1
        couleurs_attribuees = set()
        while len(couleurs_attribuees) < b:
            if couleur_courante not in couleurs_interdites:
                couleurs_attribuees.add(couleur_courante)
            couleur_courante += 1

        # Mise à jour du nombre total de couleurs utilisées
        a = max(a, max(couleurs_attribuees))

        # On attribue des couleurs au sommet
        couleurs[sommet_choisi] = couleurs_attribuees

        # On enlève le sommet choisi des sommets non colorié
        sommets_non_colories.remove(sommet_choisi)

        # On met à jour des saturations des voisins non coloriés
        for voisin in graphe[sommet_choisi]:
            if not couleurs[voisin]:
                couleurs_utilisees = set()
                for n in graphe[voisin]:
                    couleurs_utilisees.update(couleurs[n])
                saturation[voisin] = len(couleurs_utilisees)

    #  On retourne la plus petite valeur de a trouvée pour une (a, b)-coloration
    return a, couleurs