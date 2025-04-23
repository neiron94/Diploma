from sage.all import graphs, Graph
import sys
import os
import random

SET_SIZE = 5

def read_graph6_file(filename):
    with open(filename, 'r') as f:
        line = f.readline().strip()
        return Graph(line, format='graph6')

def shuffle_labels(graph):
    permutation = list(graph.vertices())
    random.shuffle(permutation)
    return graph.relabel(permutation, inplace=False)

def duplicate_all_graphs(input_dir, output_dir):
    if not os.path.isdir(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".g6"):
            input_path = os.path.join(input_dir, filename)
            try:
                original_graph = read_graph6_file(input_path)
                graph_set = [original_graph] + [shuffle_labels(original_graph) for _ in range(SET_SIZE - 1)]

                base_name = os.path.splitext(filename)[0]
                output_path = os.path.join(output_dir, base_name + ".g6")

                with open(output_path, "w") as file:
                    for g in graph_set:
                        file.write(g.graph6_string() + "\n")

                print(f"[OK] {filename} → {base_name}.g6")
            except Exception as e:
                print(f"[ERROR] Failed to process {filename}: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: sage -python graph6_iso_dup.py <input_directory> <output_directory>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    duplicate_all_graphs(input_dir, output_dir)

if __name__ == "__main__":
    main()