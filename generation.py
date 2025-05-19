from sage.all import Graph, graphs, load, Integer
import random
import os
import argparse

NON_ISO_MAX_ATTEMPTS = 30
REGULAR_BIPARTITE_MAX_ATTEMPTS = 100

# === Custom Graph Generators ===
def generate_random(n, d):
    # Compute number of edges
    max_edges = n * (n - 1) // 2
    num_edges = round(d * max_edges)

    # Start from empty graph
    G = graphs.EmptyGraph()
    for i in range(n):
        G.add_vertex()

    # Randomly choose from all possible edges
    all_possible_edges = list({(i, j) for i in range(n) for j in range(i + 1, n)})
    edges = random.sample(all_possible_edges, num_edges)

    # Fill empty graph with edges
    for u, v in edges:
        G.add_edge(u, v)

    return G

def generate_random_connected(n, d):
    if not (0 <= d <= 1):
        raise ValueError("Density must be between 0 and 1")
    if n < 1:
        raise ValueError("Number of nodes must be at least 1")

    # Compute number of edges to add
    min_edges = n - 1
    max_edges = n * (n - 1) // 2
    num_additional_edges = round(d * (max_edges - min_edges))

    # Start from tree (guarantee connectivity)
    G = graphs.RandomTree(n)

    # Find edges that are not already in the graph
    existing_edges = set(G.edges(labels=False))
    all_possible_edges = {(i, j) for i in range(n) for j in range(i + 1, n)}
    remaining_edges = list(all_possible_edges - existing_edges)

    # Get random sample from available edges
    additional_edges = random.sample(remaining_edges, num_additional_edges)

    # Add edges to the initial tree
    for u, v in additional_edges:
        G.add_edge(u, v)

    return G

def generate_cactus(n):
    if n < 1:
        raise ValueError("Number of vertices must be positive")

    G = Graph()
    G.add_vertex(0)
    node_counter = 1 # count of existing nodes = index of next node

    while node_counter < n:
        # Choose a node already in the graph to attach something to
        base = random.choice(G.vertices())

        remaining = n - node_counter

        # Randomly decide to add:
        # - a single edge
        # - a cycle
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

    # Add all vertexes to graph (without edges)
    G = Graph()
    G.add_vertices(vertices)

    # Connect each vertex from u to each vertex from v with probability = density
    for u in group1:
        for v in group2:
            if random.random() < density:
                G.add_edge(u, v)

    return G

def generate_regular_bipartite(n, d):
    if n < 2:
        raise ValueError("At least 2 vertices are required")
    if d < 1:
        raise ValueError("Degree must be at least 1")
    if n % 2 != 0:
        raise ValueError("n must be even for perfect bipartite regularity")
    if d > n // 2:
        raise ValueError("Degree too high for bipartite regular graph")

    # Parts of Regular Bipartite graph are always of the same size
    group1 = list(range(n // 2))
    group2 = list(range(n // 2, n))

    # Add all vertexes to graph (without edges)
    G = Graph()
    G.add_vertices(group1 + group2)

    edges = set()

    # Try multiple times to build a valid graph (to handle randomness)
    for attempt in range(REGULAR_BIPARTITE_MAX_ATTEMPTS):
        G.clear()   # Clear all edges for a new attempt
        degree_group1 = {u: 0 for u in group1}
        degree_group2 = {v: 0 for v in group2}
        edges.clear()

        # Generate all possible edges (u,v) with u in group1 and v in group2
        possible_pairs = [(u, v) for u in group1 for v in group2]
        random.shuffle(possible_pairs)  # Shuffle to randomize edge selection

        # Try to add edges while respecting the degree constraint
        for u, v in possible_pairs:
            if degree_group1[u] < d and degree_group2[v] < d and (u, v) not in edges:
                G.add_edge(u, v)
                edges.add((u, v))
                degree_group1[u] += 1
                degree_group2[v] += 1

        # Check if the graph is d-regular (every node in both groups has degree d)
        if all(degree == d for degree in degree_group1.values()) and all(
                degree == d for degree in degree_group2.values()):
            return G

    raise RuntimeError("Failed to generate regular bipartite graph after many attempts.")

# === Common Graph Generators ===

def generate_path(n):
    return graphs.PathGraph(n)

def generate_complete_bipartite(n):
    p = random.randint(1, n-1)
    q = n - p
    return graphs.CompleteBipartiteGraph(p, q)

def generate_complete(n):
    return graphs.CompleteGraph(n)

def generate_cycle(n):
    return graphs.CycleGraph(n)

def generate_tree(n):
    return graphs.RandomTree(n)

def generate_regular(d, n):
    if (d*n) % 2 != 0:
        raise ValueError("degree * n must be even!")
    return graphs.RandomRegular(d, n)

def generate_graph(graph_type, n, density, degree):
    match graph_type:
        case "path":
            return generate_path(n)
        case "regular_bipartite":
            return generate_regular_bipartite(n, degree)
        case "complete_bipartite":
            return generate_complete_bipartite(n)
        case "bipartite":
            return generate_bipartite(n, density)
        case "tree":
            return generate_tree(n)
        case "random":
            return generate_random(n, density)
        case "random_connected":
            return generate_random_connected(n, density)
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

# === Graph set generation ===

def generate_graphs(is_isomorphic, start, end, step, set_size, output_dir, graph_type, density, degree):
    output_dir = os.path.join(output_dir, "isomorphic" if is_isomorphic else "non_isomorphic")
    os.makedirs(output_dir, exist_ok=True)

    for n in range(start, end + 1, step):
        # If exception is thrown during generation, skip current n generation
        try:
            # Generate graph set
            if is_isomorphic:
                graph_set = generate_isomorphic_set(n, set_size, graph_type, density, degree)
            else:
                graph_set = generate_non_isomorphic_set(n, set_size, graph_type, density, degree)

            # Save graph set to file in subdirectory
            file_path = os.path.join(output_dir, f"{n}.g6")
            with open(file_path, "w") as file:
                for g in graph_set:
                    file.write(g.graph6_string() + "\n")

        except Exception as e:
            print(f"Exception during {"isomorphic" if is_isomorphic else "non-isomorphic"} graph generation: {e}")

    print(f"{"Isomorphic" if is_isomorphic else "Non-isomorphic"} dataset generated and saved in '{output_dir}'.")

def generate_isomorphic_set(n, set_size, graph_type, density, degree):
    # Generate first graph, then just shuffle its labeling
    original_graph = generate_graph(graph_type, n, density, degree)
    shuffled_graphs = [shuffle_labels(original_graph) for _ in range(set_size - 1)]
    return [original_graph] + shuffled_graphs

def shuffle_labels(graph):
    permutation = list(graph.vertices())
    random.shuffle(permutation)
    return graph.relabel(permutation, inplace=False)

def generate_non_isomorphic_set(n, set_size, graph_type, density, degree):
    non_isomorphic_graphs = []
    seen_canonical_labels = set()
    attempt = 0

    # Try to generate non-isomorphic graphs until set is filled or MAX_NON_ISO_ATTEMPTS is reached
    while len(non_isomorphic_graphs) < set_size and attempt < NON_ISO_MAX_ATTEMPTS:
        # Generate graph and take its canonical labeling
        graph = generate_graph(graph_type, n, density, degree)
        canonical_label = graph.canonical_label().copy(immutable=True)

        # If graph has unique canonical labeling, then it is not isomorphic to any preceding graph
        if canonical_label not in seen_canonical_labels:
            non_isomorphic_graphs.append(graph)
            seen_canonical_labels.add(canonical_label)

        # Increment attempt counter
        attempt += 1

    # If no non-isomorphic graph was generated, throw an error
    if len(non_isomorphic_graphs) >= 2:
        return non_isomorphic_graphs
    else:
        raise RuntimeError(f"Cannot generate non-isomorphic graphs for graph_type {graph_type}, n {n}, density {density}, degree {degree}, set_size {set_size}.")

# === Main Execution ===

if __name__ == "__main__":
    scripts_dir = "generation_scripts"
    if os.path.exists(scripts_dir):
        for filename in os.listdir(scripts_dir):
            if filename.endswith(".sage"):
                load(os.path.join(scripts_dir, filename))

    parser = argparse.ArgumentParser(description="Generate graphs and save them in a specified directory.")
    parser.add_argument("--type", type=str, required=True, help="Type of graphs to generate: tree, random, regular, etc.")
    parser.add_argument("--density", type=float, default=0.5, help="Density for some graph types. Default is 0.5.")
    parser.add_argument("--degree", type=int, default=3, help="Degree for some graph types. Default is 3.")
    parser.add_argument("--start", type=int, required=True, help="Starting number of nodes in the graphs.")
    parser.add_argument("--end", type=int, required=True, help="Ending number of nodes in the graphs.")
    parser.add_argument("--step", type=int, required=True, help="Step size for the number of nodes.")
    parser.add_argument("--set_size", type=int, required=True, help="Number of graphs to generate for each size.")
    parser.add_argument("--output_dir", type=str, required=True, help="Output directory for saving the graphs.")
    parser.add_argument("--oi", action="store_true", help="Only generate isomorphic graphs if set.")

    args = parser.parse_args()

    generate_graphs(True, args.start, args.end, args.step, args.set_size, args.output_dir, args.type, args.density, args.degree)
    if not args.oi:
        generate_graphs(False, args.start, args.end, args.step, args.set_size, args.output_dir, args.type, args.density, args.degree)
