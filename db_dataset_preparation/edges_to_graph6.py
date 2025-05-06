from sage.all import Graph
import sys
import os

def read_edges_from_file(filename):
    edges = []
    with open(filename, "r") as f:
        # Skip first line. Boltzmann generator writes additional info there.
        next(f)

        # Read and process each line (each edge)
        for line in f:
            line = line.strip()
            # Skip last line. Boltzmann generator puts "0 0" there.
            if line == "" or line.startswith("#") or line.startswith("0 0"):
                continue

            # Add edge to list of edges
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Invalid edge line: {line}")
            u, v = map(int, parts)
            edges.append((u, v))

    return edges

def main():
    if len(sys.argv) < 3:
        print("Usage: sage -python edges_to_graph6.py <input_file> <output_dir>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2]

    edges = read_edges_from_file(input_file)

    # Create Sage Graph from edges list
    G = Graph(edges)

    # All graphs with more than 2000 nodes are ignored
    if G.order() > 2000:
        print(f"Skip graph with {G.order()} vertices")
        return

    # Save graph6
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{G.order()}.g6")
    with open(output_path, "w") as f:
        f.write(G.graph6_string() + "\n")

    print(f"Graph saved in graph6 format to {output_path}")

if __name__ == "__main__":
    main()