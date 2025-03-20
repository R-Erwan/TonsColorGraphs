import random
from colorama import Fore, Style
from collections import deque

COLOR_MAP = {
    1: Fore.RED,
    2: Fore.GREEN,
    3: Fore.YELLOW,
    4: Fore.BLUE,
    5: Fore.MAGENTA,
    6: Fore.CYAN,
    7: Fore.WHITE,
}

# Random generation
def generate_random_graph(n, p):
    """
    Génère un graphe aléatoire G(n, p) où n est le nombre de sommets
    et p la probabilité d'ajouter une arête entre deux sommets.
    """
    graph = {i: [] for i in range(n)}  # Initialiser un dictionnaire vide pour n sommets

    for i in range(n):
        for j in range(i + 1, n):  # Pour chaque paire de sommets non encore connectés
            if random.random() < p:  # On ajoute une arête avec probabilité p
                graph[i].append(j)
                graph[j].append(i)

    return graph

def generate_circular_graph(n, t):
    """
    Génère un graphe circulant Cn(1, t) de n sommets avec une distance t.
    """
    graph = {i: [] for i in range(n)}  # Initialiser un dictionnaire vide pour n sommets

    # Ajouter les arêtes du cycle
    for i in range(n):
        graph[i].append((i + 1) % n)  # Arête i -> i+1 (cycle)
        graph[(i + 1) % n].append(i)

    # Ajouter les arêtes supplémentaires de distance t
    for i in range(n):
        graph[i].append((i + t) % n)  # Arête i -> i+t (distance t)
        graph[(i + t) % n].append(i)

    return graph

# Coloring display
def display_coloring(coloring):
    """
    Affiche le coloriage d'un graphe en utilisant des couleurs dans le terminal.
    :param coloring: dictionnaire contenant les couleurs des sommets.
    """
    # On parcourt le dictionnaire de coloriage
    for node, color in coloring.items():
        # Choisir la couleur à afficher en fonction de la valeur de color
        if color == 1:
            color_code = Fore.RED
        elif color == 2:
            color_code = Fore.GREEN
        elif color == 3:
            color_code = Fore.YELLOW
        elif color == 4:
            color_code = Fore.BLUE
        elif color == 5:
            color_code = Fore.MAGENTA
        elif color == 6:
            color_code = Fore.CYAN
        else:
            color_code = Fore.WHITE  # Couleur par défaut

        # Afficher le sommet avec la couleur appropriée
        print(f"Sommet {node} : {color_code}{color}{Style.RESET_ALL}")

def display_tone_coloring(coloring):
    """
    Affiche une (a, b)-coloration par tons d'un graphe en utilisant des couleurs dans le terminal.

    :param coloring: Dictionnaire {sommet: ensemble de couleurs}.
    """
    for node, colors in coloring.items():
        color_str = ""
        for color in colors:
            color_code = COLOR_MAP.get(color, Fore.WHITE)  # Par défaut, blanc
            color_str += f"{color_code}{color} "

        print(f"Sommet {node} : {color_str}{Style.RESET_ALL}")

# Misc function for graphs
def alpha(coloring):
    """
    Retourne le nombre chromatique alpha à partir d'un dictionnaire de coloration.

    :param coloring: dictionnaire où les clés sont les sommets et les valeurs sont les couleurs attribuées.
    :return: la valeur alpha correspondant au nombre maximal de couleurs utilisées.
    """
    return max(coloring.values(), default=0)

def compute_distances(graph):
    """Calcule la distance entre toutes les paires de sommets avec BFS."""
    distances = {node: {} for node in graph}

    for start in graph:
        queue = deque([(start, 0)])  # (sommet, distance actuelle)
        visited = {start}

        while queue:
            node, dist = queue.popleft()
            distances[start][node] = dist  # Distance entre start et node

            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

    return distances

def get_nodes_at_distance_k(distances, x, k):
    """Retourne la liste des sommets à distance k du sommet x."""
    return [node for node, dist in distances.get(x, {}).items() if dist == k]

def shortest_path_length(graph, source, target):
    visited = {source}
    queue = [(source, 0)]
    while queue:
        node, dist = queue.pop(0)
        if node == target:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return float('inf')  # Si aucun chemin n'existe
