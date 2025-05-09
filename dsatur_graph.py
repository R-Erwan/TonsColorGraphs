import itertools

import numpy as np
import pandas as pd
import seaborn as sns
import time
from matplotlib import pyplot as plt

from graph_utils import generate_circular_graph, generate_random_graph, shortest_path_length, bfs_distances

def dsatur(graphe):
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

def respecte_contrainte_coloration(couleurs, sommet, tons_candidats, distances):
    """Vérifie la contrainte |C(u) ∩ C(v)| < d(u,v) avec tous les sommets déjà colorés."""
    for autre, tons_autre in couleurs.items():
        if autre == sommet or not tons_autre:
            continue
        if autre in distances:
            d = distances[autre]
            if len(tons_candidats & tons_autre) >= d:
                return False
    return True

def dsatur_tons(graphe, b):
    degree = {sommet: len(voisins) for sommet, voisins in graphe.items()}
    couleurs = {sommet: set() for sommet in graphe}
    sommets_non_colories = set(graphe.keys())

    premier_sommet = max(degree, key=degree.get)
    couleurs[premier_sommet] = set(range(1, b + 1))
    sommets_non_colories.remove(premier_sommet)

    saturation = {sommet: 0 for sommet in graphe}
    a = b

    for voisin in graphe[premier_sommet]:
        if not couleurs[voisin]:
            couleurs_utilisees = set()
            for n in graphe[voisin]:
                couleurs_utilisees.update(couleurs[n])
            saturation[voisin] = len(couleurs_utilisees)

    while sommets_non_colories:
        max_sat = -1
        candidats = []
        for sommet in sommets_non_colories:
            if saturation[sommet] > max_sat:
                max_sat = saturation[sommet]
                candidats = [sommet]
            elif saturation[sommet] == max_sat:
                candidats.append(sommet)

        sommet_choisi = max(candidats, key=lambda s: degree[s])

        distances = bfs_distances(graphe, sommet_choisi)

        trouve = False
        max_ton_test = a

        while not trouve:
            for combinaison in itertools.combinations(range(1, max_ton_test + 1), b):
                tons_candidats = set(combinaison)
                if respecte_contrainte_coloration(couleurs, sommet_choisi, tons_candidats, distances):
                    couleurs[sommet_choisi] = tons_candidats
                    a = max(a, max(tons_candidats))
                    trouve = True
                    break
            if not trouve:
                max_ton_test += 1  # On augmente a

        sommets_non_colories.remove(sommet_choisi)

        for voisin in graphe[sommet_choisi]:
            if not couleurs[voisin]:
                couleurs_utilisees = set()
                for n in graphe[voisin]:
                    couleurs_utilisees.update(couleurs[n])
                saturation[voisin] = len(couleurs_utilisees)

    return a, couleurs

def dsatur_stats(max_n=10, p=0.5, max_b=5, iteration=20, algo='tons', circular=False, t=1):
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
                    random_graph = generate_circular_graph(n, t)
                else:
                    random_graph = generate_random_graph(n, p)

                if algo == 'tons':
                    a_b, _ = dsatur_tons(random_graph, b=b)
                    a_values.append(a_b)
                else:
                    a_b, _ = dsatur(random_graph)
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

def perf_stats_nodes_dsatur(node_min=2, nodes_max=10, p=0.5, max_b=2, iteration=5, algo="both", circular=False, t=1):
    """
    Génère des statistiques sur les algorithmes de coloration, en fonction du nombre de sommets,
    du paramètre b (nombre de couleurs par sommet) et du temps d'exécution.

    :param algo: both | simple | tons
    :param node_min: Le nombre de sommets minimum
    :param nodes_max: Le nombre de sommets maximal
    :param p: Probabilité d'ajout d'arêtes dans le graphe aléatoire
    :param max_b: Plus grande valeur de b à tester pour greedy_coloring_tons
    :param iteration: Nombre de répétitions pour moyenne
    :return: DataFrame avec colonnes: n, b, time_dsatur (s), time_dsatur_tone(s)
    """
    data = {
        "n": [],
        "b": [],
        "time_dsatur": [],
        "time_dsatur_tons": []
    }

    total_iterations = (nodes_max - node_min + 1) * iteration * (max_b if algo != "simple" else 1)
    progress = 0

    for n in range(node_min, nodes_max + 1):
        for b in range(1, max_b + 1):
            total_time_dsatur = 0
            total_time_dsatur_tons = 0

            for _ in range(iteration):
                if circular:
                    graph = generate_circular_graph(n,t)
                else:
                    graph = generate_random_graph(n, p)

                # Temps pour greedy_coloring
                if algo == "both" or algo == "simple":
                    start = time.perf_counter()
                    _, _ = dsatur(graph)
                    total_time_dsatur += time.perf_counter() - start

                if algo == "both" or algo == "tons":
                    start = time.perf_counter()
                    _, _ = dsatur_tons(graph, b=b)
                    total_time_dsatur_tons += time.perf_counter() - start

                progress += 1
                percentage = (progress / total_iterations) * 100
                print(f"Progression: {progress}/{total_iterations} ({percentage:.2f}%)", end="\r", flush=True)

            avg_time_greedy = total_time_dsatur / iteration if algo != "tons" else 0
            avg_time_tons = total_time_dsatur_tons / iteration if algo != "simple" else 0

            data["n"].append(n)
            data["b"].append(b)
            data["time_dsatur"].append(avg_time_greedy)
            data["time_dsatur_tons"].append(avg_time_tons)

            # Si on ne teste pas les tons, pas besoin de faire plusieurs b
            if algo == "simple":
                break

    return pd.DataFrame(data)

def max_perf_stats_dsatur(node_min=2, p=0.5, b=2, algo="both", max_avg_time=1, circular=False, t=1):
    """
    Génère des statistiques sur les algorithmes de coloration, en augmentant le nombre de sommets.
    S'arrête dès qu'un des algorithmes dépasse max_avg_time secondes pour un seul test.

    :param algo: both | simple | tons
    :param node_min: Le nombre de sommets minimum
    :param p: Probabilité d'ajout d'arêtes dans le graphe aléatoire
    :param b: Nombre de couleurs pour greedy_coloring_tons
    :param max_avg_time: Temps maximum toléré en secondes avant arrêt
    :return: DataFrame avec colonnes: n, time_dsatur (s), time_dsatur_tons (s)
    """
    data = {
        "n": [],
        "time_dsatur": [],
        "time_dsatur_tons": []
    }

    n = node_min
    try:
        while True:
            print(f"Perf n = {n}", flush=True, end="\r")

            if circular:
                graph = generate_circular_graph(n, t)
            else:
                graph = generate_random_graph(n, p)

            time_dsatur = 0
            time_dsatur_tons = 0

            if algo in ("both", "simple"):
                start = time.perf_counter()
                _, _ = dsatur(graph)
                time_dsatur = time.perf_counter() - start

            if algo in ("both", "tons"):
                start = time.perf_counter()
                _, _ = dsatur_tons(graph, b=b)
                time_dsatur_tons = time.perf_counter() - start

            data["n"].append(n)
            data["time_dsatur"].append(time_dsatur)
            data["time_dsatur_tons"].append(time_dsatur_tons)

            # Condition d’arrêt
            if (algo in ("both", "simple") and time_dsatur > max_avg_time) or \
               (algo in ("both", "tons") and time_dsatur_tons > max_avg_time):
                print(f"\n⏱️ Arrêt à n = {n} : temps d'exécution supérieur à {max_avg_time} secondes.")
                break

            n += 1

    except KeyboardInterrupt:
        print(f"\n⛔ Interruption clavier détectée à n = {n}. Résultats partiels enregistrés.")

    return pd.DataFrame(data)

def plot_perf(df):

    """
    Affiche des courbes de performance pour greedy_coloring et greedy_coloring_tons
    avec une courbe par valeur de b.

    :param df: DataFrame contenant les colonnes n, b, ti, time_dsatur, time_dsatur_tons
    """

    plt.figure(figsize=(12, 7))

    # Courbes pour dsatur_tons
    for b in sorted(df['b'].unique()):
        subset = df[df['b'] == b]
        sns.lineplot(data=subset, x="n", y="time_dsatur_tons", label=f"DSatur Tons Coloring (b={b})")

    # Une seule courbe pour dsatur si les temps sont les mêmes quel que soit b
    if df["time_dsatur"].sum() > 0:
        sns.lineplot(data=df[df["b"] == 1], x="n", y="time_dsatur", label="DSatur Coloring (b=1)", linestyle="--",
                     color="black")

    plt.xlabel("Nombre de sommets (n)")
    plt.ylabel("Temps d'exécution moyen (s)")
    plt.title("Comparaison des temps d'exécution selon b (tons et greedy)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_perf_multi_dsatur(df):
    """
    Affiche les courbes d'exécution pour greedy_coloring_tons
    avec une courbe par valeur de b.

    :param df: DataFrame avec colonnes: n, time_tons, b
    """
    plt.figure(figsize=(12, 7))

    for b in sorted(df['b'].unique()):
        subset = df[df['b'] == b]
        sns.lineplot(data=subset, x="n", y="time_dsatur_tons", label=f"Tons Coloring (b={b})")

    plt.xlabel("Nombre de sommets (n)")
    plt.ylabel("Temps d'exécution (s)")
    plt.title("Temps d'exécution de Dsatur_tons en fonction de n pour différentes valeurs de b")
    plt.legend()
    plt.grid(True)
    plt.show()





