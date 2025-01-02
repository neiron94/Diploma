from sage.graphs.graph_generators import graphs
from sage.all import load
import random
import os
import argparse

def generate_graph(type, n, density):
    if type == "tree":
    	return generateTree(n)
    elif type == "random":
        return generateRandomGraph(n, density)
    else:
        raise ValueError(f"Unknown type of graphs: {type}")

def shuffle_labels(tree):
    permutation = list(tree.vertices())
    random.shuffle(permutation)
    return tree.relabel(permutation, inplace=False)

def isomorphic_graphs(type, density, start, end, step, output_dir, set_size):
    output_dir += "isomorphic"
    os.makedirs(output_dir, exist_ok=True)
    for n in range(start, end + 1, step):
        original_graph = generate_graph(type, n, density)
        isomorphic_graphs = [original_graph] + [shuffle_labels(original_graph) for _ in range(set_size - 1)]
        file_name = f"{n}.g6"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w") as file:
            for graph in isomorphic_graphs:
                file.write(graph.graph6_string() + "\n")
    print(f"Isomorphic dataset generated and saved in the '{output_dir}' directory.")

def generate_non_isomorphic_graphs(type, n, density, set_size):
    non_isomorphic_graphs = []
    seen_canonical_labels = set()
    while len(non_isomorphic_graphs) < set_size:
        graph = generate_graph(type, n, density)
        canonical_label = graph.canonical_label().copy(immutable=True)
        if canonical_label not in seen_canonical_labels:
            non_isomorphic_graphs.append(graph)
            seen_canonical_labels.add(canonical_label)
    return non_isomorphic_graphs

def non_isomorphic_graphs(type, density, start, end, step, output_dir, set_size):
    output_dir += "non_isomorphic"
    os.makedirs(output_dir, exist_ok=True)
    for n in range(start, end + 1, step):
        non_isomorphic_graphs = generate_non_isomorphic_graphs(type, n, density, set_size)
        file_name = f"{n}.g6"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w") as file:
            for graph in non_isomorphic_graphs:
                file.write(graph.graph6_string() + "\n")
    print(f"Non-isomorphic dataset generated and saved in the '{output_dir}' directory.")

if __name__ == "__main__":
    scripts_dir = "generation_scripts"
    for filename in os.listdir(scripts_dir):
        if filename.endswith(".sage"):
            load(os.path.join(scripts_dir, filename))

    parser = argparse.ArgumentParser(description="Generate graphs and save them in a specified directory.")
    parser.add_argument("--type", type=str, help="Type of graphs to generate.")
    parser.add_argument("--density", type=float, default=0.5, help="Density of graphs. For 'random' type.")
    parser.add_argument("--start", type=int, help="Starting number of nodes in the graphs.")
    parser.add_argument("--end", type=int, help="Ending number of nodes in the graphs.")
    parser.add_argument("--step", type=int, help="Step size for the number of nodes.")
    parser.add_argument("--set_size", type=int, help="Number of graphs to generate for each size.")
    parser.add_argument("--output_dir", type=str, help="Output directory for saving the graphs.")

    args = parser.parse_args()
    isomorphic_graphs(args.type, args.density, args.start, args.end, args.step, args.output_dir, args.set_size)
    non_isomorphic_graphs(args.type, args.density, args.start, args.end, args.step, args.output_dir, args.set_size)