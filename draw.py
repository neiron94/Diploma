import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def visualize(data_file, output_dir, title, only_isomorphic):
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "data.png")
    output_file_scaled = os.path.join(output_dir, "data_scaled.png")

    # Read the CSV file
    df = pd.read_csv(data_file, delimiter=',')

    # Split data based on is_isomorphic value
    iso_data = df[df['is_isomorphic'] == True]
    non_iso_data = None
    if not only_isomorphic:
        non_iso_data = df[df['is_isomorphic'] == False]

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
    if not only_isomorphic:
        plt.title('Algorithm Performance on Isomorphic ' + title)
    else:
        plt.title('Algorithm Performance on Isomorphic vs Non-Isomorphic ' + title)
    plt.legend()
    plt.grid(True)

    # Save the plot as an image
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Plot saved as '{output_file}'")

    # Set y-axis to logarithmic scale
    plt.yscale('log')

    # Save the scaled plot as an image
    plt.savefig(output_file_scaled, dpi=300, bbox_inches='tight')
    print(f"Scaled plot saved as '{output_file_scaled}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize isomorphism algorithm performance.")
    parser.add_argument("--data_file", type=str, help="File with data to visualize.")
    parser.add_argument("--output_dir", type=str, help="Relative path of output directory.")
    parser.add_argument("--title", type=str, help="Title of plot.")
    parser.add_argument("--oi", type=bool, default=False, help="If True plots only isomorphic results.")

    args = parser.parse_args()
    visualize(args.data_file, args.output_dir, args.title, args.oi)