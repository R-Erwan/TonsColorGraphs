# Test graphe aléatoire
from glutton_graph import greedy_coloring, greedy_coloring_tons
from graph_utils import generate_random_graph, generate_circular_graph, display_coloring, display_tone_coloring

def all(n,p,b=2,alphaOnly=False):
    random_graph = generate_random_graph(n, p)
    alpha_g, coloring = greedy_coloring(graph=random_graph)
    alpha_gt, tons_coloring = greedy_coloring_tons(graph=random_graph, b=b)

    print(f"Graphe aléatoire n = {n}, p = {p}")
    if not alphaOnly:
        print(random_graph)

    print(f"\nGreedy Coloring, alpha = {alpha_g} ")
    if not alphaOnly:
        display_coloring(coloring=coloring)

    print(f"\nGreedy tons coloring, b = {b}, alpha = {alpha_gt}")
    if not alphaOnly:
        display_tone_coloring(coloring=tons_coloring)



all(n=5,p=0.5,b=2,alphaOnly=False)