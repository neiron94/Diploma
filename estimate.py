import pandas as pd
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


def compute_metrics(y_true, y_pred):
    rss = np.sum((y_true - y_pred) ** 2)
    r2 = r2_score(y_true, y_pred)
    return rss, r2

def exponential(x, a, b, c):
    return a * b ** (c * x)


def quasi_polynomial(log_x, alpha, beta, c):
    return alpha + beta * (log_x ** c) * np.log(2)


def polynomial3(x, a):
    return a * x ** 3


def polynomial2(x, a):
    return a * x ** 2


def polynomial(x, a, b):
    return a * x ** b

def estimate(data_file, output_dir):
    # data_file = "processed/regular/3/10_1000_10_5/1736474468.csv"
    # data_file = "processed/tree/10_500_10_5/1737938586.csv"
    # output_dir = "test_out/"
    # data_file = "processed/random/0.9/10_1000_10_5/1735779679.csv"
    # data_file = "processed/tree/10_3000_10_5/1735856912.csv"
    os.makedirs(output_dir, exist_ok=True)
    output_picture = os.path.join(output_dir, "estimation.png")
    output_metrics = os.path.join(output_dir, "metrics.csv")
    data = (pd.read_csv(data_file, delimiter=','))
    x = np.array(data['node_count'])
    y = np.array(data['average_time'])

    log_x = np.log(x)
    log_y = np.log(y)

    # Fit the data
    popt_exp = curve_fit(exponential, x, y,
                         p0=(1, 1, 1))
    popt_quasi = curve_fit(quasi_polynomial,
                           log_x, log_y,
                           bounds=([-np.inf, 0, 1.5], [np.inf, np.inf, np.inf]))
    popt_poly = curve_fit(polynomial, x, y)
    popt_poly2 = curve_fit(polynomial2, x, y)
    popt_poly3 = curve_fit(polynomial3, x, y)

    # Generate predictions
    y_exp = exponential(x, *(popt_exp[0]))
    y_quasi = np.exp(quasi_polynomial(log_x, *(popt_quasi[0])))
    y_poly = polynomial(x, *(popt_poly[0]))
    y_poly2 = polynomial2(x, *(popt_poly2[0]))
    y_poly3 = polynomial3(x, *(popt_poly3[0]))

    # Count and save metrics as CSV
    metrics = []
    for func_name, y_pred, popt in zip(
            ["exponential", "quasi_polynomial", "polynomial", "polynomial2", "polynomial3"],
            [y_exp, y_quasi, y_poly, y_poly2, y_poly3],
            [popt_exp, popt_quasi, popt_poly, popt_poly2, popt_poly3]
    ):
        rss, r2 = compute_metrics(y, y_pred)
        params = list(popt[0]) + [None] * (3 - len(popt[0]))
        metrics.append([func_name, rss, r2, *params])

    metrics_df = pd.DataFrame(metrics, columns=["functionName", "RSS", "r2", "parameter1", "parameter2", "parameter3"])
    metrics_df.to_csv(output_metrics, index=False)
    print(f"Metrics saved as '{output_metrics}'")

    # Plot the data and fits
    plt.figure(figsize=(16, 12))
    plt.scatter(x, y, label="Data", color="black", marker=".")
    plt.plot(x, y_exp, label="Exponential fit", color="blue")
    plt.plot(x, y_quasi, label="Quasi-Polynomial fit", color="red")
    plt.plot(x, y_poly, label="Polynomial fit", color="green")
    plt.plot(x, y_poly2, label="Polynomial2 fit", color="purple")
    plt.plot(x, y_poly3, label="Polynomial3 fit", color="brown")
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Function Fits")
    plt.savefig(output_picture, dpi=600, bbox_inches='tight')
    print(f"Plot saved as '{output_picture}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate best fitting function and visualize results.")
    parser.add_argument("--data_file", type=str, help="Relative path to CSV file with data for estimation.")
    parser.add_argument("--output_dir", type=str, help="Relative path of output directory for picture and CSV metric result.")

    args = parser.parse_args()
    estimate(args.data_file, args.output_dir)