import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def visualize(data_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "data.png")
    output_file_scaled_y = os.path.join(output_dir, "data_scaled_y.png")
    output_file_scaled_xy = os.path.join(output_dir, "data_scaled_xy.png")

    # Read the CSV file
    df = pd.read_csv(data_file, delimiter=',')

    # Split data based on is_isomorphic value
    iso_data = df[df['is_isomorphic'] == True]
    non_iso_data = df[df['is_isomorphic'] == False]
    only_isomorphic = non_iso_data.empty

    # Create the plot
    plt.figure(figsize=(20, 12))

    # Plot isomorphic results
    plt.scatter(iso_data['node_count'], iso_data['average_time'], color='blue', marker='o', label='Isomorphic')

    # Plot non-isomorphic results
    if not only_isomorphic:
        plt.scatter(non_iso_data['node_count'], non_iso_data['average_time'], color='red', marker='x', label='Non-Isomorphic')

    # Add labels and legend
    plt.xlabel('Node Count')
    plt.ylabel('Average Time (seconds)')
    plt.legend()
    plt.grid(True)

    # Save the plot as an image
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Plot saved as '{output_file}'")

    # Set y-axis to logarithmic scale
    plt.yscale('log')

    # Save the scaled-y plot as an image
    plt.savefig(output_file_scaled_y, dpi=300, bbox_inches='tight')
    print(f"Scaled-y plot saved as '{output_file_scaled_y}'")

    # Set x-axis to logarithmic scale
    plt.xscale('log')

    # Save the scaled-xy plot as an image
    plt.savefig(output_file_scaled_xy, dpi=300, bbox_inches='tight')
    print(f"Scaled-xy plot saved as '{output_file_scaled_xy}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize isomorphism algorithm performance.")
    parser.add_argument("--data_file", type=str, help="File with data to visualize.")
    parser.add_argument("--output_dir", type=str, help="Relative path of output directory.")

    args = parser.parse_args()
    visualize(args.data_file, args.output_dir)