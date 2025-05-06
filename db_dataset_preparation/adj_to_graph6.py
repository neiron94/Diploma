from sage.all import Graph, Matrix
import sys
import os

def read_adjacency_matrix(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        matrix = [list(map(int, line.strip())) for line in lines if line.strip()]
    return matrix

def convert_all_graphs(input_dir, output_dir):
    if not os.path.isdir(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    # Read all txt files
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            # If error occurred during file converting, skip this file
            try:
                # Read txt file
                matrix = read_adjacency_matrix(input_path)

                # Convert to Sage Matrix and then to Sage Graph
                M = Matrix(matrix)
                G = Graph(M, format='adjacency_matrix')

                # Take name of original file and add .g6 extension
                base_name = os.path.splitext(filename)[0]
                output_path = os.path.join(output_dir, base_name + ".g6")

                # Save graph6 file
                with open(output_path, "w") as f:
                    f.write(G.graph6_string() + "\n")

                print(f"[OK] {filename} → {base_name}.g6")
            except Exception as e:
                print(f"[ERROR] Failed to process {filename}: {e}")

def main():
    if len(sys.argv) < 3:
        print("Usage: sage -python adj_to_graph6.py <input_directory> <output_directory>")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    convert_all_graphs(input_dir, output_dir)

if __name__ == "__main__":
    main()