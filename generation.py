from sage.all import Graph, graphs, load, Integer
import random
import os
import argparse

# === Graph Generators ===

def generate_tree(n):
    return graphs.RandomTree(n)

def generate_random_graph(n, p):
    return graphs.RandomGNP(n, p)

def generate_regular(d, n):
    if (d*n) % 2 != 0:
        raise ValueError("degree * n must be even!")
    return graphs.RandomRegular(d, n)

def generate_graph(graph_type, n, density, degree):
    if graph_type == "tree":
        return generate_tree(n)
    elif graph_type == "random":
        return generate_random_graph(n, density)
    elif graph_type == "regular":
        return generate_regular(degree, n)
    else:
        raise ValueError(f"Unknown type of graphs: {graph_type}")

# === Isomorphism ===

def shuffle_labels(graph):
    permutation = list(graph.vertices())
    random.shuffle(permutation)
    return graph.relabel(permutation, inplace=False)

def isomorphic_graphs(graph_type, density, degree, start, end, step, output_dir, set_size):
    output_dir = os.path.join(output_dir, "isomorphic")
    os.makedirs(output_dir, exist_ok=True)
    for n in range(start, end + 1, step):
        original_graph = generate_graph(graph_type, n, density, degree)
        graph_set = [original_graph] + [shuffle_labels(original_graph) for _ in range(set_size - 1)]
        file_path = os.path.join(output_dir, f"{n}.g6")
        with open(file_path, "w") as file:
            for g in graph_set:
                file.write(g.graph6_string() + "\n")
    print(f"Isomorphic dataset generated and saved in '{output_dir}'.")

def generate_non_isomorphic_graphs(graph_type, n, density, degree, set_size):
    non_isomorphic_graphs = []
    seen_canonical_labels = set()
    while len(non_isomorphic_graphs) < set_size:
        graph = generate_graph(graph_type, n, density, degree)
        canonical_label = graph.canonical_label().copy(immutable=True)
        if canonical_label not in seen_canonical_labels:
            non_isomorphic_graphs.append(graph)
            seen_canonical_labels.add(canonical_label)
    return non_isomorphic_graphs

def non_isomorphic_graphs(graph_type, density, degree, start, end, step, output_dir, set_size):
    output_dir = os.path.join(output_dir, "non_isomorphic")
    os.makedirs(output_dir, exist_ok=True)
    for n in range(start, end + 1, step):
        graph_set = generate_non_isomorphic_graphs(graph_type, n, density, degree, set_size)
        file_path = os.path.join(output_dir, f"{n}.g6")
        with open(file_path, "w") as file:
            for g in graph_set:
                file.write(g.graph6_string() + "\n")
    print(f"Non-isomorphic dataset generated and saved in '{output_dir}'.")

# === Main Execution ===

if __name__ == "__main__":
    scripts_dir = "generation_scripts"
    if os.path.exists(scripts_dir):
        for filename in os.listdir(scripts_dir):
            if filename.endswith(".sage"):
                load(os.path.join(scripts_dir, filename))

    parser = argparse.ArgumentParser(description="Generate graphs and save them in a specified directory.")
    parser.add_argument("--type", type=str, required=True, help="Type of graphs to generate: tree, random, or regular.")
    parser.add_argument("--density", type=float, default=0.5, help="Density for 'random' graphs. Default is 0.5.")
    parser.add_argument("--degree", type=int, default=3, help="Degree for 'regular' graphs. Default is 3.")
    parser.add_argument("--start", type=int, required=True, help="Starting number of nodes in the graphs.")
    parser.add_argument("--end", type=int, required=True, help="Ending number of nodes in the graphs.")
    parser.add_argument("--step", type=int, required=True, help="Step size for the number of nodes.")
    parser.add_argument("--set_size", type=int, required=True, help="Number of graphs to generate for each size.")
    parser.add_argument("--output_dir", type=str, required=True, help="Output directory for saving the graphs.")
    parser.add_argument("--oi", action="store_true", help="Only generate isomorphic graphs if set.")

    args = parser.parse_args()

    isomorphic_graphs(args.type, args.density, args.degree, args.start, args.end, args.step, args.output_dir, args.set_size)
    if not args.oi:
        non_isomorphic_graphs(args.type, args.density, args.degree, args.start, args.end, args.step, args.output_dir, args.set_size)