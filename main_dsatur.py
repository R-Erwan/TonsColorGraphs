# ===== DSATUR ALGO STATS =====
import pandas as pd

from dsatur_graph import dsatur_stats, max_perf_stats_dsatur, plot_perf_multi_dsatur
from glutton_graph import plot_stats, print_stats_table

# ===== DSatur ALGO STATS =====

# 1 - HeatMap random graph n - b(1-4)
results = dsatur_stats(max_n=10, p=0.5, max_b=4, iteration=5, algo="tons", circular=False)
print_stats_table(results)
plot_stats(results)

# 2 - HeatMap circular graph n - b(1-4) - t(1-3)
results = dsatur_stats(max_n=20, p=0.5, max_b=4, iteration=1, algo="tons", circular=True, t=1)
print_stats_table(results)
plot_stats(results)

results = dsatur_stats(max_n=20, p=0.5, max_b=4, iteration=1, algo="tons", circular=True, t=3)
print_stats_table(results)
plot_stats(results)

results = dsatur_stats(max_n=20, p=0.5, max_b=4, iteration=1, algo="tons", circular=False, t=4)
print_stats_table(results)
plot_stats(results)

# 3 Perfs random graph b (2-5)
results = []
for b in range(2, 6):
    df_b = max_perf_stats_dsatur(node_min=1, p=0.5, b=b, algo="tons", max_avg_time=0.2, circular=True)
    df_b["b"] = b
    results.append(df_b)

df_all = pd.concat(results, ignore_index=True)
plot_perf_multi_dsatur(df_all)
