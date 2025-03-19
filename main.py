from dsatur_graph import dsatur
from glutton_graph import (
    greedy_coloring,
    greedy_coloring_tons,
    greedy_stats,
    print_stats_table,
    plot_stats,
)
from graph_utils import (
    generate_random_graph,
    generate_circular_graph,
    display_coloring,
    display_tone_coloring, alpha,
)


def all(n, p, b=2, alphaOnly=False):
    random_graph = generate_random_graph(n, p)
    alpha_g, coloring = greedy_coloring(graph=random_graph)
    alpha_gt, tons_coloring = greedy_coloring_tons(graph=random_graph, b=b)
    dsatur_coloring = dsatur(random_graph)
    alpha_dsatur = alpha(dsatur_coloring)

    print(f"Graphe aléatoire n = {n}, p = {p}")
    if not alphaOnly:
        print(random_graph)

    print(f"\nGreedy Coloring, alpha = {alpha_g} ")
    if not alphaOnly:
        display_coloring(coloring=coloring)

    print(f"\nGreedy tons coloring, b = {b}, alpha = {alpha_gt}")
    if not alphaOnly:
        display_tone_coloring(coloring=tons_coloring)

    print(f"\nDSATUR Coloring, alpha = {alpha_dsatur}")
    if not alphaOnly:
        display_coloring(coloring=dsatur_coloring)


# all(n=5,p=0.5,b=2,alphaOnly=False)
# stats = greedy_stats(max_n=40, p=0.5, max_b=5, iteration=1)
# print_stats_table(stats)
# plot_stats(stats)

all(n=5,p=0.5,alphaOnly=False)
