# Test graphe aléatoire
from glutton_graph import greedy_coloring, greedy_coloring_tons
from graph_utils import generate_random_graph, generate_circular_graph, display_coloring

n = 10  # Nombre de sommets
p = 0.5  # Probabilité d'ajouter une arête

random_graph = generate_random_graph(n, p)
coloring = greedy_coloring(graph=random_graph)
tons_coloring = greedy_coloring_tons(graph=random_graph,a=3,b=2)

print(f"Graphe aléatoire :\n{random_graph}\n")
print("Coloration : ")
display_coloring(coloring=coloring)
print("Tons coloration : ")
print(tons_coloring)

