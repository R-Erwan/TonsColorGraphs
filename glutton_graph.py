def greedy_coloring(graph):
    """
    Algorithme de coloration gloutonne pour un graphe donné en entrée.
    Le graphe est représenté par un dictionnaire d'adjacence.

    :param graph: dictionnaire représentant le graphe, où chaque clé est un sommet,
                  et la valeur est la liste des sommets adjacents.
    :return: un dictionnaire où les clés sont les sommets et les valeurs sont les couleurs attribuées.
    """
    coloring = {}  # Dictionnaire pour stocker la couleur de chaque sommet
    for node in graph:
        # Créer un ensemble des couleurs utilisées par les voisins du sommet
        neighbor_colors = set(coloring.get(neighbor) for neighbor in graph[node] if neighbor in coloring)

        # Trouver la première couleur qui n'est pas utilisée par les voisins
        color = 1
        while color in neighbor_colors:
            color += 1

        # Attribuer la couleur au sommet
        coloring[node] = color

    return coloring


def greedy_coloring_tons(graph, a, b):
    """
    Algorithme de coloration gloutonne pour une (a, b)-coloration par tons.

    :param graph: dictionnaire représentant le graphe sous forme d'adjacence
    :param a: nombre total de couleurs disponibles (de 1 à a)
    :param b: nombre maximal de couleurs partagées entre deux sommets adjacents
    :return: dictionnaire où les clés sont les sommets et les valeurs sont les ensembles de couleurs associés à chaque sommet
    """
    coloring = {}  # Dictionnaire pour stocker l'ensemble de couleurs de chaque sommet

    # Fonction qui vérifie si l'ensemble de couleurs du sommet est valide avec ses voisins
    def is_valid_coloring(node, colors_to_add):
        for neighbor in graph[node]:
            if neighbor in coloring:
                # Vérifie la contrainte sur le nombre de couleurs partagées
                if len(set(coloring[neighbor]) & set(colors_to_add)) >= b:
                    return False
        return True

    # On parcourt tous les sommets du graphe
    for node in graph:
        # Commence avec un ensemble vide de couleurs pour ce sommet
        colors_to_add = set()

        # Recherche les couleurs valides à attribuer au sommet
        for color in range(1, a + 1):
            if color not in colors_to_add:
                # Tente d'ajouter la couleur au sommet
                colors_to_add.add(color)

                # Si l'ajout de cette couleur est valide, on continue
                if is_valid_coloring(node, colors_to_add):
                    break
                else:
                    # Sinon, on annule l'ajout et on continue
                    colors_to_add.remove(color)

        # Si un ensemble de couleurs a été trouvé, on l'attribue au sommet
        coloring[node] = colors_to_add

    return coloring

