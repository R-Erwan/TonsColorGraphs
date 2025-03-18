def greedy_coloring(graph):
    """
    Algorithme de coloration gloutonne pour un graphe donné en entrée.
    Le graphe est représenté par un dictionnaire d'adjacence.

    :param graph: dictionnaire représentant le graphe, où chaque clé est un sommet,
                  et la valeur est la liste des sommets adjacents.
    :return: un dictionnaire où les clés sont les sommets et les valeurs sont les couleurs attribuées.
    """
    coloring = {}  # Dictionnaire pour stocker la couleur de chaque sommet
    alpha = 0
    for node in graph:
        # Créer un ensemble des couleurs utilisées par les voisins du sommet
        neighbor_colors = set(coloring.get(neighbor) for neighbor in graph[node] if neighbor in coloring)

        # Trouver la première couleur qui n'est pas utilisée par les voisins
        color = 1
        while color in neighbor_colors:
            color += 1

        # Attribuer la couleur au sommet
        coloring[node] = color
        alpha = max(alpha, color)

    return alpha, coloring


def greedy_coloring_tons(graph, b):
    """
    Algorithme glouton pour trouver le plus petit a dans une (a, b)-coloration par tons.

    :param graph: Graphe sous forme d'un dictionnaire d'adjacence.
    :param b: Nombre de couleurs par sommet.
    :return: Tuple (a_min, coloring) où a_min est le plus petit a trouvé et coloring est un dictionnaire sommet -> ensemble de couleurs.
    """
    # Initialisation : Commence avec a = b (valeur minimale possible pour a)
    a = b
    coloring = {}

    while True:  # On augmente a jusqu'à trouver une coloration valide
        coloring.clear()
        available_colors = list(range(1, a + 1))  # Les couleurs possibles

        for node in graph:
            used_colors = set()
            # Collecte des couleurs utilisées par les voisins
            for neighbor in graph[node]:
                if neighbor in coloring:
                    used_colors.update(coloring[neighbor])

            # Essayer d'assigner b couleurs à node tout en respectant les contraintes
            possible_colors = [c for c in available_colors if
                               sum(1 for n in graph[node] if c in coloring.get(n, set())) < b]

            if len(possible_colors) < b:
                break  # Échec : il faut plus de couleurs
            else:
                coloring[node] = set(possible_colors[:b])  # Attribuer b couleurs à ce sommet

        # Si tous les sommets ont été coloriés correctement, on a trouvé le bon a
        if len(coloring) == len(graph):
            return a, coloring

        a += 1  # Sinon, on augmente a et on recommence

