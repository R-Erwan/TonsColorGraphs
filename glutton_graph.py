import pandas as pd
import seaborn as sns
import itertools
import matplotlib.pyplot as plt
import numpy as np


from graph_utils import generate_random_graph, shortest_path_length

# Algos

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

def greedy_coloring_tons(graph,b):
    """
   Algorithme glouton pour trouver le plus petit a dans une (a, b)-coloration par tons.

   :param graph: Graphe sous forme d'un dictionnaire d'adjacence.
   :param b: Nombre de couleurs par sommet.
   :return: Tuple (a_min, coloring) où a_min est le plus petit a trouvé et coloring est un dictionnaire sommet -> ensemble de couleurs.
    """
    nodes = list(graph.keys())
    a = b  # On commence avec b couleurs et on augmente si nécessaire
    coloring = {node: set() for node in nodes}

    # Fonction pour vérifier si une assignation est valide
    def is_valid_coloring(node, colors_set):
        for neighbor in nodes:
            if neighbor != node:
                d = shortest_path_length(graph, node, neighbor)
                if len(coloring[neighbor] & colors_set) >= d:
                    return False
        return True

    # Assigner les couleurs aux sommets
    for node in nodes:
        assigned = False
        for color_set in itertools.combinations(range(1, a + 1), b):
            color_set = set(color_set)
            if is_valid_coloring(node, color_set):
                coloring[node] = color_set
                assigned = True
                break

        # Si aucune combinaison ne fonctionne, augmenter a
        while not assigned:
            a += 1
            for color_set in itertools.combinations(range(1, a + 1), b):
                color_set = set(color_set)
                if is_valid_coloring(node, color_set):
                    coloring[node] = color_set
                    assigned = True
                    break

    return a, coloring

# Misc functions

def greedy_stats(max_n=10, p=0.5, max_b=5, iteration=20):
    """
    Génère des statistiques sur l'algorithme de coloration glouton par tons avec affichage de progression.

    :param max_n: Nombre maximal de sommets du graphe.
    :param p: Probabilité d'ajouter une arête dans le graphe aléatoire.
    :param max_b: Valeur maximale de b (nombre de couleurs par sommet).
    :param iteration: Nombre d'itérations par combinaison (n, b).
    :return: Un dictionnaire avec les résultats sous forme de tableau.
    """
    stats = {b: [] for b in range(1, max_b + 1)}
    total_iterations = max_n * max_b * iteration  # Nombre total d'itérations
    progress = 0  # Compteur de progression

    for n in range(1, max_n + 1):
        for b in range(1, max_b + 1):
            a_values = []  # Liste des valeurs de a obtenues

            for _ in range(iteration):
                random_graph = generate_random_graph(n, p)
                a_b, _ = greedy_coloring_tons(random_graph, b=b)
                a_values.append(a_b)

                # Mettre à jour la progression
                progress += 1
                percentage = (progress / total_iterations) * 100
                print(f"Progression: {progress}/{total_iterations} ({percentage:.2f}%)", end="\r", flush=True)

            # Calcul de la moyenne de a pour ce couple (n, b)
            avg_a = np.mean(a_values)
            stats[b].append(avg_a)

    print("\nAnalyse terminée !")  # Affichage final pour éviter l'écrasement de la dernière ligne
    return stats

def print_stats_table(stats):
    """
    Affiche les statistiques sous forme de tableau avec pandas.

    :param stats: Dictionnaire {b: [valeurs de a pour chaque n]}
    """
    df = pd.DataFrame(stats)
    df.index.name = "n"
    df.columns.name = "b"

    print(df.to_string(float_format="{:.0f}".format))  # Affichage avec 2 décimales

def plot_stats(stats):
    """
    Affiche une heatmap montrant l'évolution du nombre de couleurs utilisées
    en fonction de n pour différentes valeurs de b.

    :param stats: Dictionnaire {b: [valeurs de a pour chaque n]}
    """
    # Trier les clés (b) pour garantir un affichage ordonné
    b_values = sorted(stats.keys())
    n_values = range(1, len(next(iter(stats.values()))) + 1)

    # Convertir les données en tableau numpy
    data = np.array([stats[b] for b in b_values])

    plt.figure(figsize=(10, 6))
    sns.heatmap(data, annot=True, cmap="coolwarm", xticklabels=n_values, yticklabels=b_values, fmt=".2f")

    plt.xlabel("Nombre de sommets (n)")
    plt.ylabel("Valeur de b")
    plt.title("Carte de chaleur du nombre de couleurs utilisées")
    plt.show()