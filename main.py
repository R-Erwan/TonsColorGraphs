from dsatur_graph import dsatur
from glutton_graph import (
    greedy_coloring,
    greedy_coloring_tons,
    greedy_stats,
    print_stats_table,
    plot_stats,
    perf_stats_nodes, plot_perf, max_perf_stats
)
from graph_utils import (
    generate_random_graph,
    generate_circular_graph,
    display_coloring,
    display_tone_coloring, alpha,
)
from classic_graph import G1
import time


def all(n=5, p=0.5, b=2, alpha_only=False, circular=False, t=1, graph=None):
    """
    Execute all algos with predefined graph, or with random generated graph
    """
    if graph is not None:
        random_graph = graph
    elif circular:
        random_graph = generate_circular_graph(n, t)
    else:
        random_graph = generate_random_graph(n, p)

    print(f"===== Random graph n = {n}, p = {p} ===== ") if graph is None else print("===== Graph predefined =====")
    if not alpha_only:
        print(random_graph, "\n")

    # Mesure temps pour Greedy Coloring
    start = time.perf_counter()
    alpha_g, coloring = greedy_coloring(graph=random_graph)
    end = time.perf_counter()
    print(f"Greedy Coloring, alpha = {alpha_g}, temps = {end - start:.6f}s")
    if not alpha_only:
        display_coloring(coloring=coloring)

    # Mesure temps pour Greedy Tons Coloring
    start = time.perf_counter()
    alpha_gt, tons_coloring = greedy_coloring_tons(graph=random_graph, b=b)
    end = time.perf_counter()
    print(f"\nGreedy tons coloring, b = {b}, alpha = {alpha_gt}, temps = {end - start:.6f}s")
    if not alpha_only:
        display_tone_coloring(coloring=tons_coloring)

    # Mesure temps pour DSATUR
    start = time.perf_counter()
    dsatur_coloring = dsatur(random_graph)
    alpha_dsatur = alpha(dsatur_coloring)
    end = time.perf_counter()
    print(f"\nDSATUR Coloring, alpha = {alpha_dsatur}, temps = {end - start:.6f}s")
    if not alpha_only:
        display_coloring(coloring=dsatur_coloring)
    print("")



# stats = greedy_stats(max_n=10, p=0.5, max_b=4, iteration=10,algo="tons")
# print_stats_table(stats)
# plot_stats(stats)
# all(n=5,p=0.5,b=2,alpha_only=False)

# all(b=1,alpha_only=False,graph=G1)
# all(b=2,alpha_only=False,graph=G1)
# all(b=3,alpha_only=True,graph=G1)

# stats = perf_stats_nodes(2,400,0.5,2,1,algo="both")
# plot_perf(stats)

stats = max_perf_stats(node_min=1,p=0.5,b=1,algo="simple",max_avg_time=3)
plot_perf(stats)