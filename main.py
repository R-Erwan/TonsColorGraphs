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
from classic_graph import G1


def all(n=5, p=0.5, b=2, alpha_only=False, circular=False, t=1, graph=None):
    """
    Execute all algos with predefined graph, or with random generated graph
    :param n: Nodes
    :param p: Probability
    :param b: Nombre de tons
    :param alpha_only: Display only stats about alpha number
    :param circular: Use circular graph
    :param t: For ciruclar graph
    :param graph: Personnal graph
    """
    if graph is not None:
        random_graph = graph
    elif circular:
        random_graph = generate_circular_graph(n,t)
    else:
        random_graph = generate_random_graph(n, p)

    alpha_g, coloring = greedy_coloring(graph=random_graph)
    alpha_gt, tons_coloring = greedy_coloring_tons(graph=random_graph, b=b)
    dsatur_coloring = dsatur(random_graph)
    alpha_dsatur = alpha(dsatur_coloring)

    print(f"===== Random graph n = {n}, p = {p} ===== ") if graph is None else print("===== Graph predefined =====")
    if not alpha_only:
        print(random_graph,"\n")

    print(f"Greedy Coloring, alpha = {alpha_g} ")
    if not alpha_only:
        display_coloring(coloring=coloring)

    print(f"\nGreedy tons coloring, b = {b}, alpha = {alpha_gt}")
    if not alpha_only:
        display_tone_coloring(coloring=tons_coloring)

    print(f"\nDSATUR Coloring, alpha = {alpha_dsatur}")
    if not alpha_only:
        display_coloring(coloring=dsatur_coloring)
    print("")


stats = greedy_stats(max_n=10, p=0.5, max_b=5, iteration=1)
print_stats_table(stats)
plot_stats(stats)
# all(n=5,p=0.5,b=2,alpha_only=False)

# all(b=1,alpha_only=False,graph=G1)
# all(b=2,alpha_only=False,graph=G1)
# all(b=3,alpha_only=False,graph=G1)

