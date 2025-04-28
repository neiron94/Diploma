from sage.all import Graph, graphs, load, Integer
import random
import os
import argparse

# === Graph Generators ===

def generate_regular_bipartite(n, d):
    if n < 2:
        raise ValueError("At least 2 vertices are required")
    if d < 1:
        raise ValueError("Degree must be at least 1")
    if n % 2 != 0:
        raise ValueError("n must be even for perfect bipartite regularity")
    if d > n // 2:
        raise ValueError("Degree too high for bipartite regular graph")

    group1 = list(range(n // 2))
    group2 = list(range(n // 2, n))

    G = Graph()
    G.add_vertices(group1 + group2)

    edges = set()

    max_attempts = 100  # Avoid infinite loops
    for attempt in range(max_attempts):
        G.clear()
        degree_group1 = {u: 0 for u in group1}
        degree_group2 = {v: 0 for v in group2}
        edges.clear()

        possible_pairs = [(u, v) for u in group1 for v in group2]
        random.shuffle(possible_pairs)

        for u, v in possible_pairs:
            if degree_group1[u] < d and degree_group2[v] < d and (u, v) not in edges:
                G.add_edge(u, v)
                edges.add((u, v))
                degree_group1[u] += 1
                degree_group2[v] += 1

        # Check if we succeeded
        if all(degree == d for degree in degree_group1.values()) and all(
                degree == d for degree in degree_group2.values()):
            return G

    raise RuntimeError("Failed to generate regular bipartite graph after many attempts.")


def generate_complete_bipartite(n):
    p = random.randint(1, n-1)
    q = n - p
    return graphs.CompleteBipartiteGraph(p, q)

def generate_bipartite(n, density):
    if not (0 <= density <= 1):
        raise ValueError("Density must be between 0 and 1")
    if n < 2:
        raise ValueError("At least 2 vertices are needed")

    vertices = list(range(n))
    random.shuffle(vertices)

    # Random split
    split_point = random.randint(1, n-1)
    group1 = vertices[:split_point]
    group2 = vertices[split_point:]

    G = Graph()
    G.add_vertices(vertices)

    for u in group1:
        for v in group2:
            if random.random() < density:
                G.add_edge(u, v)

    return G

def generate_complete(n):
    return graphs.CompleteGraph(n)

def generate_cycle(n):
    return graphs.CycleGraph(n)

def generate_cactus(n):
    if n < 1:
        raise ValueError("Number of vertices must be positive")

    G = Graph()
    G.add_vertex(0)
    node_counter = 1

    while node_counter < n:
        # Choose a node already in the graph to attach something to
        base = random.choice(G.vertices())

        remaining = n - node_counter

        # Randomly decide to add:
        # - a single edge
        # - a cycle of length 3–5 (ensuring cactus property)
        action = random.choice(['edge', 'cycle']) if remaining >= 2 else 'edge'

        if action == 'edge':
            G.add_edge(base, node_counter)
            node_counter += 1
        else:
            cycle_length = random.randint(2, remaining)
            cycle_nodes = [node_counter + i for i in range(cycle_length)]
            G.add_edges([(base, cycle_nodes[0])] +
                        [(cycle_nodes[i], cycle_nodes[i + 1]) for i in range(cycle_length - 1)] +
                        [(cycle_nodes[-1], base)])
            node_counter += cycle_length

    return G

def generate_tree(n):
    return graphs.RandomTree(n)

def generate_random_graph(n, p):
    return graphs.RandomGNP(n, p)

def generate_regular(d, n):
    if (d*n) % 2 != 0:
        raise ValueError("degree * n must be even!")
    return graphs.RandomRegular(d, n)

def generate_graph(graph_type, n, density, degree):
    match graph_type:
        case "regular_bipartite":
            return generate_regular_bipartite(n, degree)
        case "complete_bipartite":
            return generate_complete_bipartite(n)
        case "bipartite":
            return generate_bipartite(n, density)
        case "tree":
            return generate_tree(n)
        case "random":
            return generate_random_graph(n, density)
        case "regular":
            return generate_regular(degree, n)
        case "cactus":
            return generate_cactus(n)
        case "cycle":
            return generate_cycle(n)
        case "complete":
            return generate_complete(n)
        case _:
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
        try:
            original_graph = generate_graph(graph_type, n, density, degree)
            graph_set = [original_graph] + [shuffle_labels(original_graph) for _ in range(set_size - 1)]
            file_path = os.path.join(output_dir, f"{n}.g6")
            with open(file_path, "w") as file:
                for g in graph_set:
                    file.write(g.graph6_string() + "\n")
        except Exception as e:
            print(f"Exception during graph generation: {e}")
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
        try:
            graph_set = generate_non_isomorphic_graphs(graph_type, n, density, degree, set_size)
            file_path = os.path.join(output_dir, f"{n}.g6")
            with open(file_path, "w") as file:
                for g in graph_set:
                    file.write(g.graph6_string() + "\n")
        except Exception as e:
            print(f"Exception during graph generation: {e}")
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