import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def visualize(data_file, output_file, title):
    # Read the CSV file
    df = pd.read_csv(data_file, delimiter=',')

    # Split data based on is_isomorphic value
    iso_data = df[df['is_isomorphic'] == True]
    non_iso_data = df[df['is_isomorphic'] == False]

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot isomorphic results
    plt.scatter(iso_data['node_count'], iso_data['average_time'], color='blue', marker='o', label='Isomorphic')

    # Plot non-isomorphic results
    plt.scatter(non_iso_data['node_count'], non_iso_data['average_time'], color='red', marker='x', label='Non-Isomorphic')

    # Add labels and legend
    plt.xlabel('Node Count')
    plt.ylabel('Average Time (seconds)')
    plt.title('Algorithm Performance on Isomorphic vs Non-Isomorphic ' + title)
    plt.legend()
    plt.grid(True)

    # Save the plot as an image
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Plot saved as '{output_file}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualise isomorphism algorithm performance.")
    parser.add_argument("--data_file", type=str, help="File with data to visualise.")
    parser.add_argument("--output_file", type=str, help="Filename of output picture.")
    parser.add_argument("--title", type=str, help="Title of plot.")

    args = parser.parse_args()
    visualize(args.data_file, args.output_file, args.title)