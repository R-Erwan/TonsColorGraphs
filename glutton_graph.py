from typing import Any

import pandas as pd
import seaborn as sns
import itertools
import matplotlib.pyplot as plt
import numpy as np
import time
from graph_utils import generate_random_graph, shortest_path_length, generate_circular_graph


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

def greedy_stats(max_n = 10, p = 0.5, max_b = 5, iteration = 20, algo = 'tons', circular = False, t = 1) :
    """
    Génère des statistiques sur l'algorithme de coloration glouton, sur le alpha.

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
                if circular:
                    random_graph = generate_circular_graph(n,t)
                else:
                    random_graph = generate_random_graph(n, p)

                if algo == 'tons':
                    a_b, _ = greedy_coloring_tons(random_graph, b=b)
                    a_values.append(a_b)
                else :
                    a_b, _ = greedy_coloring(random_graph)
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

def perf_stats_nodes(node_min=2, nodes_max=10, p=0.5, max_b=2, iteration=5, algo="both", circular=False, t=1):
    """
    Génère des statistiques sur les algorithmes de coloration, en fonction du nombre de sommets,
    du paramètre b (nombre de couleurs par sommet) et du temps d'exécution.

    :param algo: both | simple | tons
    :param node_min: Le nombre de sommets minimum
    :param nodes_max: Le nombre de sommets maximal
    :param p: Probabilité d'ajout d'arêtes dans le graphe aléatoire
    :param max_b: Plus grande valeur de b à tester pour greedy_coloring_tons
    :param iteration: Nombre de répétitions pour moyenne
    :return: DataFrame avec colonnes: n, b, time_greedy (s), time_tons (s)
    """
    data = {
        "n": [],
        "b": [],
        "time_greedy": [],
        "time_tons": []
    }

    total_iterations = (nodes_max - node_min + 1) * iteration * (max_b if algo != "simple" else 1)
    progress = 0

    for n in range(node_min, nodes_max + 1):
        for b in range(1, max_b + 1):
            total_time_greedy = 0
            total_time_tons = 0

            for _ in range(iteration):
                if circular:
                    graph = generate_circular_graph(n,t)
                else:
                    graph = generate_random_graph(n, p)

                # Temps pour greedy_coloring
                if algo == "both" or algo == "simple":
                    start = time.perf_counter()
                    _, _ = greedy_coloring(graph)
                    total_time_greedy += time.perf_counter() - start

                if algo == "both" or algo == "tons":
                    start = time.perf_counter()
                    _, _ = greedy_coloring_tons(graph, b=b)
                    total_time_tons += time.perf_counter() - start

                progress += 1
                percentage = (progress / total_iterations) * 100
                print(f"Progression: {progress}/{total_iterations} ({percentage:.2f}%)", end="\r", flush=True)

            avg_time_greedy = total_time_greedy / iteration if algo != "tons" else 0
            avg_time_tons = total_time_tons / iteration if algo != "simple" else 0

            data["n"].append(n)
            data["b"].append(b)
            data["time_greedy"].append(avg_time_greedy)
            data["time_tons"].append(avg_time_tons)

            # Si on ne teste pas les tons, pas besoin de faire plusieurs b
            if algo == "simple":
                break

    return pd.DataFrame(data)

def max_perf_stats(node_min=2, p=0.5, b=2, algo="both", max_avg_time=1,circular=False, t=1):
    """
    Génère des statistiques sur les algorithmes de coloration, en augmentant le nombre de sommets.
    S'arrête dès qu'un des algorithmes dépasse max_avg_time secondes pour un seul test.

    :param algo: both | simple | tons
    :param node_min: Le nombre de sommets minimum
    :param p: Probabilité d'ajout d'arêtes dans le graphe aléatoire
    :param b: Nombre de couleurs pour greedy_coloring_tons
    :param max_avg_time: Temps maximum toléré en secondes avant arrêt
    :return: DataFrame avec colonnes: n, time_greedy (s), time_tons (s)
    """
    data = {
        "n": [],
        "time_greedy": [],
        "time_tons": []
    }

    n = node_min
    try:
        while True:
            print(f"Perf n = {n}", flush=True, end="\r")

            if circular:
                graph = generate_circular_graph(n, t)
            else:
                graph = generate_random_graph(n, p)

            time_greedy = 0
            time_tons = 0

            if algo in ("both", "simple"):
                start = time.perf_counter()
                _, _ = greedy_coloring(graph)
                time_greedy = time.perf_counter() - start

            if algo in ("both", "tons"):
                start = time.perf_counter()
                _, _ = greedy_coloring_tons(graph, b=b)
                time_tons = time.perf_counter() - start

            data["n"].append(n)
            data["time_greedy"].append(time_greedy)
            data["time_tons"].append(time_tons)

            # Condition d’arrêt
            if (algo in ("both", "simple") and time_greedy > max_avg_time) or \
               (algo in ("both", "tons") and time_tons > max_avg_time):
                print(f"\n⏱️ Arrêt à n = {n} : temps d'exécution supérieur à {max_avg_time} secondes.")
                break

            n += 1

    except KeyboardInterrupt:
        print(f"\n⛔ Interruption clavier détectée à n = {n}. Résultats partiels enregistrés.")

    return pd.DataFrame(data)

# Prints and plots funct

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

def plot_perf(df):

    """
    Affiche des courbes de performance pour greedy_coloring et greedy_coloring_tons
    avec une courbe par valeur de b.

    :param df: DataFrame contenant les colonnes n, b, time_greedy, time_tons
    """
    plt.figure(figsize=(12, 7))

    # Courbes pour greedy_coloring_tons
    for b in sorted(df['b'].unique()):
        subset = df[df['b'] == b]
        sns.lineplot(data=subset, x="n", y="time_tons", label=f"Tons Coloring (b={b})")

    # Une seule courbe pour greedy_coloring si les temps sont les mêmes quel que soit b
    if df["time_greedy"].sum() > 0:
        sns.lineplot(data=df[df["b"] == 1], x="n", y="time_greedy", label="Greedy Coloring (b=1)", linestyle="--",
                     color="black")

    plt.xlabel("Nombre de sommets (n)")
    plt.ylabel("Temps d'exécution moyen (s)")
    plt.title("Comparaison des temps d'exécution selon b (tons et greedy)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_perf_multi(df):
    """
    Affiche les courbes d'exécution pour greedy_coloring_tons
    avec une courbe par valeur de b.

    :param df: DataFrame avec colonnes: n, time_tons, b
    """
    plt.figure(figsize=(12, 7))

    for b in sorted(df['b'].unique()):
        subset = df[df['b'] == b]
        sns.lineplot(data=subset, x="n", y="time_tons", label=f"Tons Coloring (b={b})")

    plt.xlabel("Nombre de sommets (n)")
    plt.ylabel("Temps d'exécution (s)")
    plt.title("Temps d'exécution de greedy_coloring_tons en fonction de n pour différentes valeurs de b")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
