from dsatur_graph import dsatur_tons, dsatur
from glutton_graph import (
    greedy_coloring,
    greedy_coloring_tons,
    greedy_stats,
    print_stats_table,
    plot_stats,
    max_perf_stats, plot_perf_multi
)
from graph_utils import (
    generate_random_graph,
    generate_circular_graph,
    display_coloring,
    display_tone_coloring, alpha,
)
import time
import pandas as pd

def all_algo_exec(n=5, p=0.5, b=2, alpha_only=False, circular=False, t=1, graph=None):
    """
    Execution de tous les algos avec un graphe prédéfini ou aléatoire
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

    # Mesure temps pour DSATUR Tons
    start = time.perf_counter()
    alpha_gt, tons_coloring = dsatur_tons(random_graph, b=b)
    end = time.perf_counter()
    print(f"\nDSATUR tons, b = {b}, alpha = {alpha_gt}, temps = {end - start:.6f}s")
    if not alpha_only:
        display_tone_coloring(coloring=tons_coloring)



# ===== GLUTTON ALGO STATS =====
#
# # 1 - HeatMap random graph n - b(1-4)
# results = greedy_stats(max_n=10,p=0.5,max_b=4,iteration=5,algo="tons",circular=False)
# print_stats_table(results)
# plot_stats(results)
#
# # 2 - HeatMap circular graph n - b(1-4) - t(1-3)
# results = greedy_stats(max_n=20,p=0.5,max_b=4,iteration=1,algo="tons",circular=True,t=1)
# print_stats_table(results)
# plot_stats(results)
#
# results = greedy_stats(max_n=20,p=0.5,max_b=4,iteration=1,algo="tons",circular=True,t=3)
# print_stats_table(results)
# plot_stats(results)
#
# results = greedy_stats(max_n=20,p=0.5,max_b=4,iteration=1,algo="tons",circular=True,t=4)
# print_stats_table(results)
# plot_stats(results)
#
# # 3 Perfs random graph b (2-5)
# results = []
# for b in range(2, 6):
#     df_b = max_perf_stats(node_min=1, p=0.5, b=b, algo="tons", max_avg_time=1,circular=False)
#     df_b["b"] = b
#     results.append(df_b)
#
# df_all = pd.concat(results, ignore_index=True)
# plot_perf_multi(df_all)
#
#
# # 4 Perfs circular graph b(1-5) - t = 2
# results = []
# for b in range(2, 6):
#     df_b = max_perf_stats(node_min=1, p=0.5, b=b, algo="tons", max_avg_time=1,circular=True,t=2)
#     df_b["b"] = b
#     results.append(df_b)
#
# df_all = pd.concat(results, ignore_index=True)
# plot_perf_multi(df_all)
#
#
