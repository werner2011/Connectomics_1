from neuromaps import datasets, stats 
map_a = datasets.fetch_annotation(source="margulies2016")
map_b = datasets.fetch_annotation(source="neurosynth")

r, p = stats.compare_images(
    map_a,
    map_b,
    metric="pearsonr",
    nan_policy="omit"
)

print("r =", r)
print("p =", p)