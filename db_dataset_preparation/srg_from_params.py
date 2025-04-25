from sage.graphs.strongly_regular_db import strongly_regular_graph
import csv
import os
import sys

def generate_graphs_from_csv(csv_file, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                v = int(row['v'])
                k = int(row['k'])
                l = int(row['lambda'])
                mu = int(row['mu'])

                # Try to generate the graph
                G = strongly_regular_graph(v, k, l, mu)
                output_path = os.path.join(output_dir, f"{v}.g6")

                with open(output_path, "w") as out:
                    out.write(G.graph6_string() + "\n")

                print(f"[OK] Generated graph with v={v} saved to {output_path}")
            except Exception as e:
                print(f"[ERROR] Could not generate graph for v={row.get('v')}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: sage -python generate_srg_from_csv.py <csv_file> <output_directory>")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_dir = sys.argv[2]
    generate_graphs_from_csv(csv_file, output_dir)