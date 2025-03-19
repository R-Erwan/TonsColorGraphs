

# Commentaire pas utile mais moi besoin

def dsatur(graphe):
    # Calcul le degré de chaque sommet
    degre = {sommet: len(voisins) for sommet, voisins in graphe.items()}
    
    # Init
    couleurs = {sommet: None for sommet in graphe}  # Couleurs assignées aux sommets (None = non colorié)
    saturation = {sommet: 0 for sommet in graphe}  # Degré de saturation de chaque sommet
    non_colores = set(graphe.keys())  # Ensemble des sommets non colorés
    
    # Colorie le sommet le plus eleve
    premier_noeud = max(degre, key=degre.get)
    couleurs[premier_noeud] = 0
    non_colores.remove(premier_noeud)
    
    # Update la saturation des voisins du premier sommet
    for voisin in graphe[premier_noeud]:
        if couleurs[voisin] is None:
            saturation[voisin] += 1
    
    while non_colores:
        # Find le sommet non colorié avec le plus haut degré de saturation
        sat_max = -1
        candidats = []
        for sommet in non_colores:
            if saturation[sommet] > sat_max:
                sat_max = saturation[sommet]
                candidats = [sommet]
            elif saturation[sommet] == sat_max:
                candidats.append(sommet)
        
        # Resout égalités en choisissant le sommet avec le degré le plus élevé
        if len(candidats) > 1:
            noeud_choisi = max(candidats, key=lambda sommet: degre[sommet])
        else:
            noeud_choisi = candidats[0]
        
        # Plus petite couleur possible non utilisée par les voisins
        couleurs_voisins = set(couleurs[voisin] for voisin in graphe[noeud_choisi] if couleurs[voisin] is not None)
        couleur = 0

        while couleur in couleurs_voisins:
            couleur += 1

        couleurs[noeud_choisi] = couleur
        non_colores.remove(noeud_choisi)
        
        # Update les degrés de saturation des voisins non coloriés
        for voisin in graphe[noeud_choisi]:
            if couleurs[voisin] is None:
                # Compte les couleurs uniques parmi les voisins coloriés
                couleurs_uniques = set(couleurs[n] for n in graphe[voisin] if couleurs[n] is not None)
                saturation[voisin] = len(couleurs_uniques)
    
    return couleurs


